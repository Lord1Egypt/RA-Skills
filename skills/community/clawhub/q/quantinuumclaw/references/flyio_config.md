# Fly.io Configuration for Quantum Workloads

Comprehensive guide for deploying Selene quantum backend services to Fly.io. This document covers configuration optimization, scaling strategies, secrets management, and best practices for quantum computing applications.

## Table of Contents

1. [Quick Start](#quick-start)
2. [fly.toml Configuration](#flytoml-configuration)
3. [VM Sizing & Performance](#vm-sizing--performance)
4. [Secrets Management](#secrets-management)
5. [Regional Deployment](#regional-deployment)
6. [Scaling & Autoscaling](#scaling--autoscaling)
7. [Monitoring & Logs](#monitoring--logs)
8. [Cost Optimization](#cost-optimization)
9. [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# 1. Install flyctl
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Launch app (in service directory with fly.toml)
fly launch --now

# 4. Set secrets if needed
fly secrets set QUANTUM_API_KEY=your_key

# 5. Open in browser
fly open
```

## fly.toml Configuration

The `fly.toml` file defines your app configuration. Here's a complete example optimized for quantum workloads:

```toml
# fly.toml - Selene quantum service

app = "quantum-optimizer"  # Your app name (globally unique)
primary_region = "lhr"     # London - near Quantinuum hardware

[build]
  dockerfile = "Dockerfile"
  # Optional: buildpack alternative
  # builder = "paketobuildpacks/builder:base"

# Environment variables accessible in the container
[env]
  PORT = "8080"
  QUANTUM_HARDWARE = "h2"  # Quantinuum hardware to target
  # GUPPY_LOG_LEVEL = "INFO"  # Uncomment for verbose logging

# HTTP service configuration
[[http_services]]
  internal_port = 8080
  force_https = true

  # Autoscaling configuration
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero when idle
  max_machines_running = 5  # Maximum concurrent instances

  # Process types
  processes = ["app"]

  # Health checks
  [[http_services.checks]]
    interval = "10s"
    timeout = "2s"
    method = "GET"
    path = "/health"

  [[http_services.checks]]
    interval = "30s"
    timeout = "5s"
    method = "GET"
    path = "/api/info"

  [[http_services.tcp_checks]]
    interval = "10s"
    timeout = "2s"
    port = 8080

# Optional: TCP service for non-HTTP protocols
# [[tcp_services]]
#   internal_port = 9090
#   [[tcp_services.ports]]
#     port = 9090
#   [[tcp_services.checks]]
#     interval = "10s"
#     timeout = "2s"
```

### Configuration Fields Explained

| Field | Description | Recommendation |
|-------|-------------|----------------|
| `app` | Global app name | Use kebab-case, unique across Fly.io |
| `primary_region` | Default deployment region | Choose near your users OR quantum hardware (lhr, yyz, ewr) |
| `dockerfile` | Container build definition | Use multi-stage Dockerfile for smaller images |
| `auto_stop_machines` | Scale to zero when idle | `true` for cost savings on infrequent workloads |
| `min_machines_running` | Always-on instances | `0` for on-demand, `1` for always-warm |
| `max_machines_running` | Maximum concurrent VMs | `5` for moderate load, increase based on queue size |
| `force_https` | HTTPS redirect | `true` for production |
| `internal_port` | Container port | Must match your app's listening port |

## VM Sizing & Performance

### Choosing VM Size

Fly.io offers different VM sizes. Select based on quantum workload:

```toml
# Use [[vm]] section to specify size
[[vm]]
  size = "performance-2x"  # 2GB RAM, 2 vCPU - good for small circuits
# size = "performance-4x"  # 4GB RAM, 4 vCPU - medium circuits
# size = "performance-8x"  # 8GB RAM, 8 vCPU - large circuits, heavy sim
```

**Guidelines:**
- **Mock/small circuits (<20 qubits)**: `performance-1x` (1GB RAM) sufficient
- **Medium circuits (20-50 qubits)**: `performance-2x` or `performance-4x`
- **Large simulations (50+ qubits)**: `performance-8x` or larger
- **Real quantum hardware**: `performance-2x` usually sufficient (hardware does the work)

### Memory Considerations

Quantum circuit compilation can be memory-intensive:

```python
# In your Selene service, monitor memory usage
import psutil
import os

def log_memory():
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {mem_mb:.1f} MB")
```

If OOM errors occur, increase VM size or optimize circuit compilation.

## Secrets Management

### Setting Secrets

Never hardcode credentials. Use Fly.io secrets:

```bash
# Set individual secrets
fly secrets set \
  QUANTUM_API_KEY=your_quantinuum_api_key \
  HARDWARE_TYPE=h2 \
  --app quantum-optimizer

# Set from .env file
fly secrets import < .env
```

Secrets are injected as environment variables in your container.

### Accessing Secrets in Code

```python
import os

QUANTUM_API_KEY = os.getenv("QUANTUM_API_KEY")
HARDWARE_TYPE = os.getenv("HARDWARE_TYPE", "emulator")

if not QUANTUM_API_KEY:
    raise ValueError("QUANTUM_API_KEY environment variable not set")
```

### Secret Rotation

1. Update secret: `fly secrets set QUANTUM_API_KEY=new_key`
2. Restart app: `fly deploy --restart` (automatic on secret change)
3. Verify old key no longer works

## Regional Deployment

### Single Region

Default deployment to one region. Choose based on:

- **User proximity**: lhr (London), ewr (Newark), yyz (Toronto), syd (Sydney)
- **Quantum hardware**: Quantinuum hardware located in specific regions

```bash
fly launch --region lhr
```

### Multi-Region (Advanced)

For global low-latency, use Fly.io's global Anycast:

```toml
# In fly.toml
primary_region = "lhr"
  # Additional regions automatically route to primary

[[http_services]]
  # Same config as single-region
  # Fly.io will route users to nearest region
```

Multi-region requires:
- Stateless application (use external database)
- Replicated data stores (or read replicas)
- Consider data residency regulations

### Region-Specific Configuration

```python
import os

REGION = os.getenv("FLY_REGION", "lhr")

if REGION == "lhr":
    HARDWARE_ENDPOINT = "https://h2.quantinuum.com"
elif REGION == "yyz":
    HARDWARE_ENDPOINT = "https://h2-ca.quantinuum.com"
else:
    HARDWARE_ENDPOINT = "https://emulator.quantinuum.com"
```

## Scaling & Autoscaling

### Horizontal Autoscaling

Fly.io automatically adds/removes VMs based on load:

```toml
[[http_services]]
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  max_machines_running = 10

  # Scale based on request count
  [[http_services.concurrency]]
    type = "requests"
    value = 50  # Scale when > 50 concurrent requests per VM
```

### Queue-Based Scaling

For batch quantum jobs, scale based on queue length:

```python
# Add endpoint to expose queue size
@app.get("/api/admin/queue-size")
async def queue_size():
    return {"queue_size": job_queue.qsize()}

# Then in fly.toml, monitor via external service
# or use Fly.io's metrics for custom autoscaling
```

### Manual Scaling

```bash
# Increase max instances
fly scale count 5 --app quantum-optimizer

# Change VM size
fly scaling memory 4096 --app quantum-optimizer
fly scale vm performance-4x --app quantum-optimizer
```

## Monitoring & Logs

### Accessing Logs

```bash
# Stream logs
fly logs --app quantum-optimizer

# Follow logs (tail)
fly logs --tail --app quantum-optimizer

# Logs for specific VM
fly logs --vm <machine-id> --app quantum-optimizer

# View historical logs (last 1 hour)
fly logs --hours 1 --app quantum-optimizer
```

### Structured Logging

```python
import logging
import json
from datetime import datetime

logger = logging.getLogger("selene")

def log_quantum_job(job_id, params, result):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "job_id": job_id,
        "params": params,
        "result": result,
        "execution_time_ms": result.get("execution_time_ms")
    }
    logger.info(json.dumps(log_entry))
```

### Metrics & Dashboards

Fly.io provides built-in metrics. View in dashboard or via API:

```bash
# Get metrics for last hour
fly metrics --app quantum-optimizer
```

Key metrics to monitor:
- **HTTP request rate** (requests/sec)
- **Job queue size** (custom metric)
- **VM memory usage** (avoid OOM)
- **Response time** (quantum job latency)
- **Error rate** (4xx/5xx responses)

### Alerting

Set up alerts via Fly.io notifications or external monitoring:

```bash
# Add notification
fly notifications create \
  --event type=deployment_failed \
  --to email:you@example.com \
  --app quantum-optimizer
```

## Cost Optimization

### Estimate Costs

```bash
# Check current usage and cost
fly balance --org your-org
fly apps list --org your-org
```

Cost components:
- **VM hours**: Shared VMs = $0.000023/VM-sec ($0.083/VM-hr)
- **Volume storage**: $0.15/GB-month
- **Bandwidth**: 1TB included, $0.02/GB after

### Reduce Costs

1. **Scale to zero**: `min_machines_running = 0` for infrequent jobs
2. **Use smaller VMs**: Start small, increase only if needed
3. **Reduce VM count**: Set appropriate `max_machines_running`
4. **Cache results**: Avoid recomputation (see selene_api.md)
5. **Use emulator for dev**: `QUANTUM_HARDWARE=emulator` for testing
6. **Cleanup old jobs**: Implement job TTL, delete completed jobs

### Cost Monitoring

```bash
# Get detailed billing
fly org --json | jq '.billing'

# Set budget alerts
fly billing alerts create \
  --threshold 50 \
  --currency usd \
  --org your-org
```

## Troubleshooting

### App Won't Start

```bash
# Check build logs
fly logs --phase build

# SSH into VM for debugging
fly ssh --app quantum-optimizer

# Check process status
fly vm status --app quantum-optimizer
```

### Health Checks Failing

```bash
# Verify health endpoint
curl https://quantum-optimizer.fly.dev/health

# Check config
fly config show --app quantum-optimizer

# Temporarily disable health checks to deploy anyway
fly deploy --skip-health-checks --app quantum-optimizer
```

### Deploy Fails

```bash
# Clean build cache
fly deploy --clean --app quantum-optimizer

# Force rebuild without cache
fly deploy --no-cache --app quantum-optimizer

# Check Dockerfile syntax
docker build -t test-build .
```

### High Memory Usage

```bash
# Check per-VM metrics
fly metrics --app quantum-optimizer

# Increase VM size if OOM
fly scale memory 4096 --app quantum-optimizer

# Optimize Python memory
# Use generators, stream results, avoid loading all shots in memory
```

### Quantum Hardware Connection Issues

```python
# Add detailed logging for quantum backend
import logging
logging.basicConfig(level=logging.DEBUG)

# Check environment variables
import os
print(f"Region: {os.getenv('FLY_REGION')}")
print(f"Hardware: {os.getenv('QUANTUM_HARDWARE')}")
```

Common causes:
- API key not set or incorrect
- Hardware region mismatch
- Network egress blocked (outbound ports)
- Rate limiting on Quantinuum API

### Slow Performance

1. Profile your Python code: `python -m cProfile main.py`
2. Check Fly.io VM metrics for CPU throttling
3. Optimize quantum circuit (fewer gates, lower depth)
4. Increase VM size if CPU-bound
5. Implement caching for repeated computations

---

**Next:** See [lovable_patterns.md](./lovable_patterns.md) for frontend integration patterns
