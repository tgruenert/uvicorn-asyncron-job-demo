import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global task reference
background_task = None
task_running = False


async def looping_function():
    """
    A function that logs a test message every 2 seconds.
    Runs indefinitely until cancelled.
    """
    global task_running
    logger.info("Looping function started")
    task_running = True
    
    try:
        while True:
            logger.info(f"Test message at {datetime.now().isoformat()}")
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        logger.info("Looping function stopped")
        task_running = False
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application"""
    # Startup
    logger.info("Application starting up")
    yield
    # Shutdown
    global background_task
    if background_task and not background_task.done():
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass
    logger.info("Application shutting down")


# Create FastAPI application
app = FastAPI(title="Async Job Demo", lifespan=lifespan)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Async Job Demo API",
        "endpoints": {
            "start": "/start",
            "stop": "/stop",
            "status": "/status"
        }
    }


@app.post("/start")
async def start_job():
    """Start the looping background task"""
    global background_task, task_running
    
    if background_task and not background_task.done():
        return {
            "status": "already_running",
            "message": "Background task is already running"
        }
    
    background_task = asyncio.create_task(looping_function())
    return {
        "status": "started",
        "message": "Background task started successfully"
    }


@app.post("/stop")
async def stop_job():
    """Stop the looping background task"""
    global background_task, task_running
    
    if not background_task or background_task.done():
        return {
            "status": "not_running",
            "message": "Background task is not running"
        }
    
    background_task.cancel()
    try:
        await background_task
    except asyncio.CancelledError:
        pass
    
    return {
        "status": "stopped",
        "message": "Background task stopped successfully"
    }


@app.get("/status")
async def get_status():
    """Get the status of the background task"""
    global background_task, task_running
    
    if not background_task:
        status = "not_started"
    elif background_task.done():
        status = "stopped"
    elif task_running:
        status = "running"
    else:
        status = "unknown"
    
    return {
        "status": status,
        "task_running": task_running
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
