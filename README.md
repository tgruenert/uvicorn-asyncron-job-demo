# uvicorn-asyncron-job-demo

Demo of a long-running job controlled with REST start/stop commands using Python, FastAPI, and Uvicorn.

## Overview

This application demonstrates:
- An async background task that logs messages every 2 seconds
- A REST API built with FastAPI to control the background task
- Start and stop commands to manage the task lifecycle
- Comprehensive tests using pytest

## Features

- **Looping Function**: Logs a test message every 2 seconds
- **REST API Endpoints**:
  - `GET /` - Root endpoint with API information
  - `POST /start` - Start the background looping task
  - `POST /stop` - Stop the background looping task
  - `GET /status` - Get the current status of the background task

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tgruenert/uvicorn-asyncron-job-demo.git
cd uvicorn-asyncron-job-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the server using uvicorn:

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

Alternatively, you can run the main.py directly:

```bash
python main.py
```

### API Endpoints

#### Get API Information
```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "Async Job Demo API",
  "endpoints": {
    "start": "/start",
    "stop": "/stop",
    "status": "/status"
  }
}
```

#### Start the Background Task
```bash
curl -X POST http://localhost:8000/start
```

Response:
```json
{
  "status": "started",
  "message": "Background task started successfully"
}
```

#### Check Status
```bash
curl http://localhost:8000/status
```

Response:
```json
{
  "status": "running",
  "task_running": true
}
```

#### Stop the Background Task
```bash
curl -X POST http://localhost:8000/stop
```

Response:
```json
{
  "status": "stopped",
  "message": "Background task stopped successfully"
}
```

### Viewing Logs

When the background task is running, you'll see log messages in the console every 2 seconds:

```
2024-02-09 20:22:23,456 - __main__ - INFO - Test message at 2024-02-09T20:22:23.456789
2024-02-09 20:22:25,457 - __main__ - INFO - Test message at 2024-02-09T20:22:25.457890
...
```

## Running Tests

### Install Test Dependencies

All test dependencies are included in `requirements.txt`.

### Run All Tests

```bash
pytest test_main.py -v
```

### Run Specific Tests

```bash
# Test the start job functionality
pytest test_main.py::test_start_job -v

# Test the complete lifecycle
pytest test_main.py::test_job_lifecycle -v
```

### Run Tests with Coverage

```bash
pip install pytest-cov
pytest test_main.py --cov=main --cov-report=html
```

### Test Output Example

```bash
$ pytest test_main.py -v

test_main.py::test_root_endpoint PASSED                      [ 14%]
test_main.py::test_start_job PASSED                          [ 28%]
test_main.py::test_stop_job PASSED                           [ 42%]
test_main.py::test_status_endpoint PASSED                    [ 57%]
test_main.py::test_job_lifecycle PASSED                      [ 71%]
test_main.py::test_root_sync PASSED                          [ 85%]

============================== 6 passed in 8.23s ==============================
```

## Project Structure

```
uvicorn-asyncron-job-demo/
├── main.py           # Main application with FastAPI endpoints and looping function
├── test_main.py      # Test cases for the application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## How It Works

### Looping Function

The `looping_function()` is an async function that:
1. Runs in an infinite loop
2. Logs a message with the current timestamp every 2 seconds
3. Can be cancelled via `asyncio.CancelledError`

### Task Management

- The background task is managed as an asyncio Task
- Starting the task creates a new asyncio task that runs the looping function
- Stopping the task cancels the running asyncio task
- The application properly cleans up tasks on shutdown

### API Implementation

- Built with FastAPI for modern async Python web framework
- Runs on Uvicorn, a lightning-fast ASGI server
- All endpoints return JSON responses with status information

## Development

### Adding New Features

1. Modify `main.py` to add new endpoints or functionality
2. Add corresponding tests in `test_main.py`
3. Update this README with new documentation
4. Run tests to ensure everything works

### Code Quality

The code follows Python best practices:
- Async/await for non-blocking operations
- Proper exception handling
- Comprehensive logging
- Clean separation of concerns
- Well-documented functions

## License

This is a demo project for educational purposes.
