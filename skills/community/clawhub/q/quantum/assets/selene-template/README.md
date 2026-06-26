# Selene Quantum Service Template

Production-ready template for quantum computing web services using Guppy and FastAPI.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env to set QUANTUM_HARDWARE if using real hardware
   ```

3. **Customize the quantum algorithm:**
   - Edit `main.py`
   - Implement your quantum circuit in `QuantumService._run_real_quantum()` method
   - Update the API endpoint `/api/optimization/compute` for your use case
   - Modify `get_info()` to reflect your application

4. **Run locally:**
   ```bash
   python main.py
   ```
   Service starts at http://localhost:8080

5. **Test:**
   ```bash
   curl http://localhost:8080/health
   curl -X POST http://localhost:8080/api/optimization/compute \
     -H "Content-Type: application/json" \
     -d '{"params": {"shots": 1000}, "wait": true}'
   ```

## Deploy to Fly.io

1. **Install flyctl:** https://fly.io/docs/hands-on/install-flyctl/

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Launch app:**
   ```bash
   fly launch --now
   ```
   This will:
   - Create a Fly.io app
   - Set up build configuration
   - Deploy to London region (lhr)

4. **Set secrets (if using quantum hardware):**
   ```bash
   fly secrets set QUANTUM_API_KEY=your_key
   ```

5. **Open your app:**
   ```bash
   fly open
   ```

## Project Structure

```
.
├── main.py              # FastAPI service with quantum execution
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container definition for Fly.io
├── fly.toml            # Fly.io configuration
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Customizing for Your Quantum Use Case

### 1. Update Service Info

In `main.py`, modify `get_info()` endpoint:

```python
@app.get("/api/info")
async def get_info():
    return {
        "service": "your-app-name",
        "description": "Your quantum application description",
        # ...
    }
```

### 2. Implement Quantum Algorithm

Override `_run_real_quantum()` in `QuantumService` class:

```python
def _run_real_quantum(self, params: Dict[str, Any]) -> Dict[str, Any]:
    """Implement your quantum circuit using Guppy"""
    from guppy import quantum

    n_qubits = params.get("n_qubits", 2)

    with quantum() as q:
        qbits = q.qubits(n_qubits)

        # Your quantum circuit here
        q.h(qbits[0])
        q.cx(qbits[0], qbits[1])

        # Measure
        result = q.execute(shots=params.get("shots", 1000))

    return {
        "bitstring_counts": result,
        "most_frequent": max(result, key=result.get)
    }
```

### 3. Customize API Endpoints

Add or modify endpoints for your specific needs:

```python
@app.post("/api/your-use-case/compute")
async def your_endpoint(request: ComputeRequest):
    # Your logic here
    pass
```

## API Reference

See `../references/selene_api.md` for complete API documentation.

Key endpoints:
- `GET /health` - Service health check
- `GET /api/info` - Service metadata
- `POST /api/optimization/compute` - Execute quantum computation

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Service port (Fly.io sets this) | No (default: 8080) |
| `QUANTUM_HARDWARE` | Hardware target: h2, h1, emulator | No |
| `QUANTUM_API_KEY` | Quantinuum API key for real hardware | Only for real hardware |
| `DEBUG` | Enable debug mode | No (default: false) |

### fly.toml Configuration

Edit `fly.toml` to customize:
- `app` - Your Fly.io app name (must be unique globally)
- `primary_region` - Deployment region (lhr, yyz, ewr, etc.)
- `[[http_services.concurrency]]` - Auto-scaling thresholds
- `[[http_services.checks]]` - Health check paths

## Scaling

For high-volume applications:

1. **Enable autoscaling** in `fly.toml`:
   ```toml
   auto_stop_machines = true
   min_machines_running = 0
   max_machines_running = 10
   ```

2. **Add persistent storage** for job history:
   ```bash
   fly volumes create quantum_data --size 1
   ```
   Then mount in `fly.toml`:
   ```toml
   [mounts]
     source = "quantum_data"
     destination = "/data"
   ```

3. **Use external Redis** for multi-region job queues:
   ```bash
   fly redis create
   ```

## Monitoring

```bash
# Stream logs
fly logs --tail

# Check metrics
fly metrics

# SSH into VM for debugging
fly ssh

# View app status
fly status
```

## Developing with Guppy

### Install Guppy

```bash
# TODO: Update with actual Guppy installation instructions
pip install guppy
```

### Test Circuit Locally

```python
# test_circuit.py
from guppy import quantum

with quantum() as q:
    qbits = q.qubits(2)
    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])
    q.h(qbits[1])
    result = q.execute(shots=1000)
    print(result)
```

## Security Considerations

1. **API Authentication**: Set `API_KEY` secret and check in endpoints
2. **Rate Limiting**: Implement on public endpoints (use slowapi or similar)
3. **Input Validation**: Use Pydantic models for all requests
4. **CORS**: Restrict `allow_origins` in production
5. **Secrets**: Never commit `.env` - use Fly.io secrets only

## Troubleshooting

### Guppy Import Error
- Ensure Guppy is installed: `pip install guppy`
- Check Python version compatibility (3.10+ recommended)

### Deployment Fails
```bash
fly deploy --clean  # Clean build cache
fly logs --phase build  # Check build logs
```

### Health Check Failing
Verify `/health` endpoint returns 200. Test locally first:
```bash
curl http://localhost:8080/health
```

### Out of Memory
- Increase VM size in `fly.toml`: `size = "performance-4x"`
- Optimize quantum circuit for lower memory
- Use emulator for development, hardware for production

## Next Steps

- Implement your specific quantum algorithm
- Add authentication to API endpoints
- Set up result caching (Redis)
- Configure monitoring and alerts
- Frontend integration: See `../../lovable_patterns.md`
- Fly.io optimization: See `../../flyio_config.md`

---

**References:**
- [Guppy Programming Guide](../references/guppy_guide.md)
- [Selene API Reference](../references/selene_api.md)
- [Fly.io Configuration](../references/flyio_config.md)
- [Lovable Frontend Patterns](../references/lovable_patterns.md)
