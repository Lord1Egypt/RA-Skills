# Selene API Reference

Complete reference for the Selene quantum backend service. This document describes the API endpoints, request/response schemas, error handling, and integration patterns for quantum applications.

## Table of Contents

1. [Overview](#overview)
2. [API Endpoints](#api-endpoints)
3. [Request/Response Schemas](#requestresponse-schemas)
4. [Error Handling](#error-handling)
5. [Authentication & Security](#authentication--security)
6. [Performance & Scaling](#performance--scaling)
7. [Deployment Patterns](#deployment-patterns)
8. [Frontend Integration](#frontend-integration)

## Overview

Selene is the backend service layer for Guppy quantum applications. It provides RESTful APIs for executing quantum algorithms, managing jobs, and retrieving results.

**Base URL**: `https://your-app.fly.dev` (or `http://localhost:8080` locally)

**Features:**
- Quantum circuit execution
- Job queuing and management
- Result persistence
- Multi-tenant support
- Rate limiting
- Health monitoring

## API Endpoints

### Health Check

**GET** `/health`

Check service health and quantum backend status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "guppy_available": true,
  "quantum_hardware": "connected",
  "queue_size": 0,
  "version": "1.0.0"
}
```

**Status codes:**
- `200`: Healthy
- `503`: Service unavailable (maintenance, quantum offline)

### Service Information

**GET** `/api/info`

Returns service metadata and available endpoints.

**Response:**
```json
{
  "service": "quantum-optimizer",
  "description": "Portfolio optimization using quantum computing",
  "version": "1.0.0",
  "quantum_backend": "Quantinuum H2",
  "endpoints": [
    {"path": "/health", "method": "GET", "description": "Health check"},
    {"path": "/api/optimization/compute", "method": "POST", "description": "Run optimization"},
    {"path": "/api/jobs/{job_id}", "method": "GET", "description": "Get job status"},
    {"path": "/api/jobs/{job_id}/result", "method": "GET", "description": "Get job result"}
  ],
  "rate_limit": {
    "requests_per_minute": 60,
    "max_concurrent_jobs": 10
  }
}
```

### Execute Quantum Computation

**POST** `/api/{use_case}/compute`

Execute quantum algorithm with provided parameters.

**Path Parameters:**
- `use_case`: The quantum use case (optimization, chemistry, ml, random, etc.)

**Request Body:**
```json
{
  "params": {
    "shots": 1000,
    "precision": 0.01,
    "max_iterations": 100
  },
  "wait": true,
  "timeout_ms": 30000
}
```

**Field Descriptions:**
- `params` (object): Algorithm-specific parameters
- `wait` (boolean): If true, block until completion. If false, return job ID immediately.
- `timeout_ms` (number): Maximum time to wait (if wait=true). Default: 30000.

**Response (wait=true):**
```json
{
  "application": "quantum-optimizer",
  "use_case": "optimization",
  "timestamp": "2024-01-15T10:30:15Z",
  "job_id": "abc123",
  "status": "completed",
  "result": {
    "optimal_portfolio": [0.25, 0.35, 0.40],
    "expected_return": 0.124,
    "risk": 0.087,
    "confidence": 0.95
  },
  "statistics": {
    "shots": 1000,
    "execution_time_ms": 2450,
    "hardware_used": "Quantinuum H2"
  }
}
```

**Response (wait=false):**
```json
{
  "job_id": "abc123",
  "status": "queued",
  "message": "Job accepted, check status with GET /api/jobs/abc123"
}
```

### Job Status

**GET** `/api/jobs/{job_id}`

Check status of asynchronous quantum job.

**Response:**
```json
{
  "job_id": "abc123",
  "status": "running",  // queued, running, completed, failed
  "created_at": "2024-01-15T10:30:15Z",
  "started_at": "2024-01-15T10:30:16Z",
  "estimated_completion": "2024-01-15T10:30:18Z",
  "progress": 0.65,
  "queue_position": 2
}
```

### Job Result

**GET** `/api/jobs/{job_id}/result`

Retrieve result of completed job. Only available after job status is "completed".

**Response:**
```json
{
  "job_id": "abc123",
  "status": "completed",
  "completed_at": "2024-01-15T10:30:18Z",
  "result": {
    "optimal_portfolio": [0.25, 0.35, 0.40],
    "expected_return": 0.124,
    "risk": 0.087
  },
  "statistics": {
    "shots": 1000,
    "execution_time_ms": 2450,
    "hardware_used": "Quantinuum H2"
  },
  "download_url": "/api/jobs/abc123/download"
}
```

### Download Raw Results

**GET** `/api/jobs/{job_id}/download`

Download raw quantum measurement data (CSV or JSON).

**Query Parameters:**
- `format` (optional): `csv` or `json` (default: `json`)

**Response:**
File attachment with measurement shots.

## Request/Response Schemas

### Standard Result Structure

All quantum computation endpoints return results with this structure:

```typescript
interface QuantumResult {
  application: string;      // Service name
  use_case: string;         // Quantum use case identifier
  timestamp: string;        // ISO 8601 timestamp
  status: "success" | "error";
  result: any;              // Algorithm-specific result object
  statistics: {
    shots: number;          // Number of measurements
    execution_time_ms: number;
    hardware_used: string;
  };
}
```

### Job Object

```typescript
interface Job {
  job_id: string;
  status: "queued" | "running" | "completed" | "failed";
  created_at: string;
  started_at?: string;
  completed_at?: string;
  progress: number;         // 0-1
  queue_position?: number;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}
```

## Error Handling

### HTTP Status Codes

- `200`: Success
- `400`: Invalid request parameters
- `401`: Authentication required
- `403`: Authentication failed / insufficient permissions
- `404`: Job not found
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Quantum hardware unavailable

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_PARAMS",
    "message": "Invalid parameter: shots must be between 1 and 10000",
    "details": {
      "field": "shots",
      "received": 50000,
      "allowed_range": [1, 10000]
    }
  }
}
```

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_PARAMS` | Request parameters invalid | Check parameter types, ranges, required fields |
| `QUANTUM_ERROR` | Quantum execution failed | Check algorithm, retry with different parameters |
| `HARDWARE_UNAVAILABLE` | Quantum hardware offline | Retry with wait=true using longer timeout |
| `JOB_NOT_FOUND` | Job ID doesn't exist | Verify job_id, check if job was purged |
| `RATE_LIMITED` | Too many requests | Implement backoff, reduce request rate |
| `AUTH_FAILED` | API key invalid | Verify API key in request header |
| `TIMEOUT` | Job exceeded timeout | Increase timeout or reduce circuit complexity |

## Authentication & Security

### API Key Authentication

If enabled, include API key in request header:

```
Authorization: Bearer YOUR_API_KEY
```

Set API key via Fly.io secrets:

```bash
fly secrets set API_KEY=your_quantinuum_api_key --app your-app
```

Selene validates against environment variable `API_KEY` (if set).

### CORS

By default, Selene allows all origins for development. For production, configure allowed origins in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting

Default limits (configurable):
- 60 requests per minute per IP
- 10 concurrent jobs per API key

Rate limit response:

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 45 seconds."
  },
  "retry_after": 45
}
```

With `Retry-After` header indicating seconds to wait.

### Input Validation

Never trust client input. Validate all parameters:

```python
from pydantic import BaseModel, Field

class ComputeRequest(BaseModel):
    shots: int = Field(1000, ge=1, le=10000)
    precision: float = Field(0.01, ge=0.001, le=1.0)

@app.post("/api/optimization/compute")
async def compute(request: ComputeRequest):
    # request is validated automatically
    ...
```

## Performance & Scaling

### Job Queue

Long-running quantum jobs (> few seconds) should use asynchronous execution:

```javascript
// Frontend: Async job submission
const response = await fetch('/api/optimization/compute', {
  method: 'POST',
  body: JSON.stringify({params: {...}, wait: false})
});
const { job_id } = await response.json();

// Poll for completion
const poll = setInterval(async () => {
  const status = await fetch(`/api/jobs/${job_id}`);
  if (status.status === 'completed') {
    clearInterval(poll);
    const result = await fetch(`/api/jobs/${job_id}/result`);
    console.log(await result.json());
  }
}, 1000);
```

### Fly.io Configuration

See `flyio_config.md` for detailed Fly.io optimization. Key recommendations:

- **VM size**: Use ` Performance` VMs for quantum job processing
- **Regions**: Deploy to regions near quantum hardware (e.g., `lhr`, `yyz`)
- **Autoscaling**: Enable `auto_start_machines` and `auto_stop_machines` for burst workloads
- **Volumes**: Use volumes for persistent job history (optional)

### Caching

Implement result caching for identical computations:

```python
from redis import Redis
from functools import lru_cache

redis_client = Redis.from_url(os.getenv("REDIS_URL"))

def get_cache_key(params):
    return f"quantum:{hash(json.dumps(params, sort_keys=True)}}"

@app.post("/api/optimization/compute")
async def compute(request: ComputeRequest):
    cache_key = get_cache_key(request.params)

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Execute quantum job
    result = await run_quantum_job(request.params)

    # Cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(result))

    return result
```

## Deployment Patterns

### Stateless API (Recommended)

Backend is stateless. Job history stored in external database (PostgreSQL/Redis). Scale horizontally easily.

**Pros:** Easy scaling, resilient to restarts, multi-region possible
**Cons:** Requires external state storage

### Stateful with Volumes

Use Fly.io volumes for job persistence. Simpler but less scalable.

```bash
fly volumes create quantum_data --size 1 --region lhr
```

Mount in `fly.toml`:
```toml
[mounts]
  source = "quantum_data"
  destination = "/data"
```

**Pros:** Simple, no external dependencies
**Cons:** Cannot scale to multiple regions, single failure domain

### Background Worker Pattern

Separate API (fast request handling) from worker (quantum execution):

```python
# api.py - lightweight API
@app.post("/api/jobs")
async def submit_job(request: ComputeRequest):
    job_id = enqueue_job(request)  # Add to Redis/RabbitMQ queue
    return {"job_id": job_id}

# worker.py - separate process
def process_jobs():
    while True:
        job = dequeue_job()
        result = execute_quantum_circuit(job.params)
        store_result(job.id, result)
```

**Pros:** Better throughput, can scale workers independently
**Cons:** More complex deployment, needs message queue

## Frontend Integration

### Making API Calls

**Synchronous (wait=true):**

```javascript
async function runQuantum(params) {
  const response = await fetch('/api/optimization/compute', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({params, wait: true, timeout_ms: 30000})
  });
  return await response.json();
}
```

**Asynchronous (wait=false):**

```javascript
async function runQuantumAsync(params) {
  // Submit job
  const submitResponse = await fetch('/api/optimization/compute', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({params, wait: false})
  });
  const { job_id } = await submitResponse.json();

  // Poll for completion
  return pollJob(job_id);
}

async function pollJob(job_id, maxAttempts = 60) {
  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(`/api/jobs/${job_id}`);
    const job = await response.json();

    if (job.status === 'completed') {
      const resultResponse = await fetch(`/api/jobs/${job_id}/result`);
      return await resultResponse.json();
    } else if (job.status === 'failed') {
      throw new Error(job.error.message);
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  throw new Error('Job timeout');
}
```

### Error Handling in Frontend

```javascript
try {
  const result = await runQuantum(params);
  console.log('Quantum result:', result);
} catch (error) {
  if (error.code === 'RATE_LIMITED') {
    // Show retry-after countdown
    setTimeout(runQuantum, error.retry_after * 1000);
  } else if (error.code === 'QUANTUM_ERROR') {
    // Show user-friendly error
    alert('Quantum computation failed. Try different parameters.');
  } else {
    // Generic error
    console.error('API error:', error);
  }
}
```

### Real-Time Updates with WebSockets

For long-running jobs, consider WebSocket push notifications:

```python
# In Selene service - WebSocket endpoint
from fastapi import WebSocket

@app.websocket("/ws/jobs/{job_id}")
async def websocket_job_status(websocket: WebSocket, job_id: str):
    await websocket.accept()
    async for update in job_status_stream(job_id):
        await websocket.send_json(update)
```

Frontend:
```javascript
const ws = new WebSocket(`wss://${backendUrl}/ws/jobs/${job_id}`);
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  updateUI(update);
};
```

---

**See also:**
- [guppy_guide.md](./guppy_guide.md) - Quantum programming with Guppy
- [flyio_config.md](./flyio_config.md) - Fly.io deployment configuration
- [lovable_patterns.md](./lovable_patterns.md) - Frontend patterns for quantum apps
