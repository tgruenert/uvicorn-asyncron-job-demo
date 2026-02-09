import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app, background_task


@pytest.fixture
def client():
    """Fixture for synchronous test client"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint returns expected information"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert data["endpoints"]["start"] == "/start"
    assert data["endpoints"]["stop"] == "/stop"
    assert data["endpoints"]["status"] == "/status"


@pytest.mark.asyncio
async def test_start_job():
    """Test starting the background job"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Start the job
        response = await ac.post("/start")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
        
        # Wait a bit to let the job run
        await asyncio.sleep(0.5)
        
        # Check status
        response = await ac.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["task_running"] is True
        
        # Try to start again (should return already_running)
        response = await ac.post("/start")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "already_running"
        
        # Stop the job
        response = await ac.post("/stop")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_stop_job():
    """Test stopping the background job"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Start the job first
        await ac.post("/start")
        await asyncio.sleep(0.5)
        
        # Stop the job
        response = await ac.post("/stop")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "stopped"
        
        # Check status after stopping
        await asyncio.sleep(0.5)
        response = await ac.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "stopped"
        
        # Try to stop again (should return not_running)
        response = await ac.post("/stop")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "not_running"


@pytest.mark.asyncio
async def test_status_endpoint():
    """Test the status endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Check initial status
        response = await ac.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "task_running" in data


@pytest.mark.asyncio
async def test_job_lifecycle():
    """Test the complete lifecycle of starting, running, and stopping a job"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Initial status should be not running
        response = await ac.get("/status")
        initial_data = response.json()
        
        # Start the job
        response = await ac.post("/start")
        assert response.status_code == 200
        
        # Wait for job to run and produce some log messages
        await asyncio.sleep(3)
        
        # Verify job is running
        response = await ac.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        
        # Stop the job
        response = await ac.post("/stop")
        assert response.status_code == 200
        
        # Verify job has stopped
        await asyncio.sleep(0.5)
        response = await ac.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "stopped"


def test_root_sync(client):
    """Test the root endpoint using synchronous client"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
