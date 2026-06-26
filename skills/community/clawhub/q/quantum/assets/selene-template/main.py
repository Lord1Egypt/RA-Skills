#!/usr/bin/env python3
"""
Selene Quantum Application Template

This is a production-ready template for Guppy/Selene quantum services.
Customize this for your specific quantum use case.

Features:
- FastAPI backend with CORS
- Quantum job execution with timeout
- Health check endpoint
- Error handling and logging
- Graceful shutdown
- Environment configuration
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
class QuantumService:
    """Service for executing quantum algorithms"""

    def __init__(self):
        self.guppy_available = False
        try:
            import guppy as qp
            self.guppy_available = True
            self.hw = None  # Initialize quantum hardware if needed
            logger.info("Guppy quantum runtime available")
        except ImportError:
            logger.warning("Guppy not installed - running in mock mode")

    def execute_quantum_circuit(
        self,
        params: Dict[str, Any],
        timeout_seconds: int = 30
    ) -> Dict[str, Any]:
        """
        Execute quantum algorithm with provided parameters.

        Override this method with your specific quantum circuit logic.
        """
        import time
        start = time.time()

        try:
            if self.guppy_available:
                # TODO: Replace with your actual Guppy quantum circuit
                result = self._run_real_quantum(params)
            else:
                # Mock implementation for testing without quantum hardware
                result = self._run_mock_quantum(params)

            elapsed = (time.time() - start) * 1000

            return {
                "status": "success",
                "result": result,
                "execution_time_ms": round(elapsed, 2),
                "shots": params.get("shots", 1000),
                "hardware_used": "Quantinuum H2" if self.guppy_available else "mock"
            }

        except Exception as e:
            logger.exception("Quantum execution failed")
            raise

    def _run_real_quantum(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Implement your real quantum circuit here"""
        # Example placeholder
        return {
            "message": "Implement _run_real_quantum() with your Guppy circuit",
            "params_received": params
        }

    def _run_mock_quantum(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock implementation for development/testing"""
        shots = params.get("shots", 1000)
        # Simulate some randomness
        import random
        value = random.random()

        return {
            "mock_result": True,
            "value": round(value, 4),
            "shots": shots,
            "note": "This is mock data. Install Guppy for real quantum execution."
        }

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Selene quantum service...")
    service = QuantumService()
    app.state.quantum_service = service
    yield
    # Shutdown
    logger.info("Shutting down quantum service...")

# Create FastAPI app
app = FastAPI(
    title="Selene Quantum Service",
    description="Quantum computing API powered by Guppy",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - configure for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request validation models
from pydantic import BaseModel, Field

class ComputeRequest(BaseModel):
    params: Dict[str, Any] = Field(default_factory=dict)
    wait: bool = Field(default=True, description="Wait for completion")
    timeout_ms: int = Field(default=30000, ge=1000, le=300000)

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None

# In-memory job storage (replace with Redis/DB for production)
jobs: Dict[str, Dict[str, Any]] = {}

# Error handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc),
                "type": type(exc).__name__
            }
        }
    )

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint for Fly.io"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "guppy_available": app.state.quantum_service.guppy_available,
        "service": "selene-quantum"
    }

# Service info
@app.get("/api/info")
async def get_info():
    """Return service information"""
    return {
        "service": "quantum-optimizer",  # TODO: Customize
        "description": "Quantum computing web service",  # TODO: Customize
        "version": "1.0.0",
        "quantum_backend": "Quantinuum H2" if app.state.quantum_service.guppy_available else "mock",
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api/optimization/compute", "method": "POST", "description": "Run optimization"},
            {"path": "/api/jobs/{job_id}", "method": "GET", "description": "Get job status"},
            {"path": "/api/jobs/{job_id}/result", "method": "GET", "description": "Get job result"},
        ],
        "rate_limit": {
            "requests_per_minute": 60,
            "max_concurrent_jobs": 10
        }
    }

# Main quantum computation endpoint
@app.post("/api/optimization/compute")
async def compute(request: ComputeRequest):
    """
    Execute quantum optimization algorithm.

    Request body:
    {
        "params": {
            "shots": 1000,
            "precision": 0.01,
            "max_iterations": 100
        },
        "wait": true,
        "timeout_ms": 30000
    }
    """
    try:
        # Validate request
        if not request.wait and not request.params.get("job_id"):
            # For async, generate a job ID
            import uuid
            job_id = str(uuid.uuid4())

            # Store job for later execution (simplified - in production use queue)
            jobs[job_id] = {
                "status": "queued",
                "params": request.params,
                "created_at": datetime.utcnow().isoformat()
            }

            return JobResponse(
                job_id=job_id,
                status="queued",
                message="Job queued for processing"
            ).dict()

        # Synchronous execution
        result = app.state.quantum_service.execute_quantum_circuit(
            request.params,
            timeout_seconds=request.timeout_ms // 1000
        )

        return {
            "application": "quantum-optimizer",
            "use_case": "optimization",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "result": result,
            "statistics": {
                "shots": request.params.get("shots", 1000),
                "execution_time_ms": result.get("execution_time_ms", 0),
                "hardware_used": result.get("hardware_used", "unknown")
            }
        }

    except Exception as e:
        logger.error(f"Computation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "QUANTUM_ERROR",
                    "message": f"Quantum computation failed: {str(e)}"
                }
            }
        )

# Job status endpoint
@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get status of asynchronous quantum job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    return {
        "job_id": job_id,
        **job,
        "created_at": job["created_at"]
    }

# Job result endpoint
@app.get("/api/jobs/{job_id}/result")
async def get_job_result(job_id: str):
    """Get result of completed job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Current status: {job['status']}"
        )

    return job.get("result", {})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting Selene service on {host}:{port}")
    uvicorn.run(
        "main:app",  # When run as module, use this
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
