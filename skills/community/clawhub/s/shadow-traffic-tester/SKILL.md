---
name: shadow-traffic-tester
description: Set up and analyze shadow traffic testing to compare new service versions against production without user impact
---

# Shadow Traffic Tester

Configure shadow (dark) traffic mirroring to test a new service version against real production traffic without affecting users. Production requests are duplicated to the shadow service, responses are captured and compared to detect behavioral differences, latency regressions, and error rate changes. This skill covers Istio-based mirroring, Nginx mirror modules, and custom proxy-level solutions.

Use when: "shadow traffic", "dark traffic test", "mirror traffic", "traffic mirroring", "compare service versions", "shadow deployment", "canary comparison"

## Commands

### 1. `setup` --- Configure traffic mirroring

Set up the infrastructure to mirror live traffic to a shadow service version.

**Step 1 -- Identify the service mesh / ingress in use**

```bash
# Detect traffic management layer
echo "=== Checking for Istio ==="
kubectl get crd virtualservices.networking.istio.io 2>/dev/null && echo "Istio detected" || echo "No Istio"

echo ""
echo "=== Checking for Nginx Ingress ==="
kubectl get ingressclass -o jsonpath='{.items[*].metadata.name}' 2>/dev/null | grep -q nginx && echo "Nginx Ingress detected" || echo "No Nginx Ingress"

echo ""
echo "=== Checking for Linkerd ==="
kubectl get crd serviceprofiles.linkerd.io 2>/dev/null && echo "Linkerd detected" || echo "No Linkerd"

echo ""
echo "=== Checking for Envoy Gateway ==="
kubectl get crd gateways.gateway.networking.k8s.io 2>/dev/null && echo "Gateway API detected" || echo "No Gateway API"
```

**Step 2a -- Istio mirror configuration**

```bash
# Deploy shadow version alongside production
SERVICE_NAME="${1:-my-service}"
SHADOW_VERSION="${2:-v2}"
NAMESPACE="${3:-default}"

cat << 'ISTIOEOF'
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {SERVICE_NAME}-mirror
  namespace: {NAMESPACE}
spec:
  hosts:
  - {SERVICE_NAME}
  http:
  - route:
    - destination:
        host: {SERVICE_NAME}
        subset: production
      weight: 100
    mirror:
      host: {SERVICE_NAME}
      subset: shadow
    mirrorPercentage:
      value: 100.0
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: {SERVICE_NAME}-versions
  namespace: {NAMESPACE}
spec:
  host: {SERVICE_NAME}
  subsets:
  - name: production
    labels:
      version: v1
  - name: shadow
    labels:
      version: {SHADOW_VERSION}
ISTIOEOF
```

**Step 2b -- Nginx-based mirroring (no service mesh)**

For clusters without a service mesh, use a sidecar proxy approach:

```bash
cat << 'NGINXEOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: shadow-mirror-config
data:
  nginx.conf: |
    upstream production {
        server {SERVICE_NAME}.{NAMESPACE}.svc.cluster.local:80;
    }
    upstream shadow {
        server {SERVICE_NAME}-shadow.{NAMESPACE}.svc.cluster.local:80;
    }
    server {
        listen 8080;
        location / {
            proxy_pass http://production;
            mirror /mirror;
            mirror_request_body on;
        }
        location = /mirror {
            internal;
            proxy_pass http://shadow$request_uri;
            proxy_set_header X-Shadow-Request "true";
            # Shadow responses are discarded
        }
    }
NGINXEOF
```

**Step 3 -- Deploy the shadow service**

```bash
# Clone the production deployment with shadow labels
kubectl get deployment "$SERVICE_NAME" -n "$NAMESPACE" -o json | python3 -c "
import json, sys

deploy = json.load(sys.stdin)
# Modify for shadow
deploy['metadata']['name'] += '-shadow'
deploy['metadata'].pop('resourceVersion', None)
deploy['metadata'].pop('uid', None)
deploy['metadata'].pop('creationTimestamp', None)
deploy['metadata']['labels']['version'] = 'shadow'
deploy['metadata']['labels']['traffic-role'] = 'shadow'
deploy['spec']['selector']['matchLabels']['version'] = 'shadow'
deploy['spec']['template']['metadata']['labels']['version'] = 'shadow'
deploy['spec']['template']['metadata']['labels']['traffic-role'] = 'shadow'
# Set shadow image
for c in deploy['spec']['template']['spec']['containers']:
    c['image'] = c['image'].rsplit(':', 1)[0] + ':shadow'
# Reduce replicas for shadow (it only needs to handle, not serve)
deploy['spec']['replicas'] = max(1, deploy['spec'].get('replicas', 1) // 2)
print(json.dumps(deploy, indent=2))
" | kubectl apply -f -
```

**Step 4 -- Verify mirroring is active**

```bash
# Check shadow pods are receiving traffic
echo "=== Shadow pod logs (last 20 lines) ==="
kubectl logs -l traffic-role=shadow -n "$NAMESPACE" --tail=20 2>/dev/null

# If using Istio, check Envoy stats
echo ""
echo "=== Istio mirror stats ==="
kubectl exec -n "$NAMESPACE" deploy/"$SERVICE_NAME" -c istio-proxy -- \
  pilot-agent request GET stats 2>/dev/null | grep -i mirror || echo "No Istio proxy stats available"
```

**Report template:**

```
## Shadow Traffic Setup Report

### Configuration
- Service: {SERVICE_NAME}
- Namespace: {NAMESPACE}
- Mirror method: {Istio/Nginx/Custom}
- Mirror percentage: {100}%
- Shadow image: {image:tag}

### Status
- Shadow pods running: {N}
- Mirror config applied: {yes/no}
- Traffic reaching shadow: {yes/no/pending}

### Next Steps
1. Let shadow run for {recommended_duration} to collect comparison data
2. Run `analyze` to compare response behaviors
```

---

### 2. `analyze` --- Compare shadow vs production responses

Collect and compare response data between the production and shadow service.

**Step 1 -- Collect comparison data**

For Istio-based setups, use access logs:

```bash
NAMESPACE="${1:-default}"
SERVICE_NAME="${2:-my-service}"

# Collect production access logs
echo "=== Gathering production access logs ==="
kubectl logs -l app="$SERVICE_NAME",version=v1 -n "$NAMESPACE" \
  --tail=1000 --since=1h 2>/dev/null > /tmp/prod-access.log

# Collect shadow access logs
echo "=== Gathering shadow access logs ==="
kubectl logs -l app="$SERVICE_NAME",traffic-role=shadow -n "$NAMESPACE" \
  --tail=1000 --since=1h 2>/dev/null > /tmp/shadow-access.log

echo "Production log lines: $(wc -l < /tmp/prod-access.log)"
echo "Shadow log lines: $(wc -l < /tmp/shadow-access.log)"
```

**Step 2 -- Compare status codes**

```bash
python3 << 'PYEOF'
import re
from collections import Counter

def extract_status_codes(logfile):
    codes = []
    with open(logfile) as f:
        for line in f:
            # Match common log formats: "HTTP/1.1" 200, status=200, response_code=200
            m = re.search(r'(?:HTTP/\d\.\d"\s+|status[=:]\s*|response_code[=:]\s*)(\d{3})', line)
            if m:
                codes.append(m.group(1))
    return Counter(codes)

prod = extract_status_codes('/tmp/prod-access.log')
shadow = extract_status_codes('/tmp/shadow-access.log')

all_codes = sorted(set(list(prod.keys()) + list(shadow.keys())))

print(f"{'STATUS':<8} {'PRODUCTION':>12} {'SHADOW':>12} {'DIFF':>12}")
print("-" * 48)
for code in all_codes:
    p = prod.get(code, 0)
    s = shadow.get(code, 0)
    diff = s - p
    marker = " ***" if abs(diff) > max(p * 0.1, 5) else ""
    print(f"{code:<8} {p:>12} {s:>12} {diff:>+12}{marker}")

prod_total = sum(prod.values())
shadow_total = sum(shadow.values())
prod_errors = sum(v for k, v in prod.items() if k.startswith(('4', '5')))
shadow_errors = sum(v for k, v in shadow.items() if k.startswith(('4', '5')))

print(f"\nProduction error rate: {prod_errors}/{prod_total} ({prod_errors/max(prod_total,1)*100:.1f}%)")
print(f"Shadow error rate:    {shadow_errors}/{shadow_total} ({shadow_errors/max(shadow_total,1)*100:.1f}%)")
PYEOF
```

**Step 3 -- Compare response latencies**

```bash
python3 << 'PYEOF'
import re, statistics

def extract_latencies(logfile):
    latencies = []
    with open(logfile) as f:
        for line in f:
            # Match duration patterns: duration=0.035s, response_time=35ms, latency=35
            m = re.search(r'(?:duration|response_time|latency)[=:]\s*([0-9.]+)\s*(ms|s)?', line)
            if m:
                val = float(m.group(1))
                unit = m.group(2) or 'ms'
                latencies.append(val * 1000 if unit == 's' else val)
    return latencies

prod_lat = extract_latencies('/tmp/prod-access.log')
shadow_lat = extract_latencies('/tmp/shadow-access.log')

def report(name, data):
    if not data:
        print(f"{name}: no latency data found")
        return
    print(f"{name}:")
    print(f"  p50: {statistics.median(data):.1f}ms")
    print(f"  p90: {sorted(data)[int(len(data)*0.9)]:.1f}ms")
    print(f"  p99: {sorted(data)[int(len(data)*0.99)]:.1f}ms")
    print(f"  max: {max(data):.1f}ms")
    print(f"  avg: {statistics.mean(data):.1f}ms")

report("Production", prod_lat)
print()
report("Shadow", shadow_lat)

if prod_lat and shadow_lat:
    p50_diff = statistics.median(shadow_lat) - statistics.median(prod_lat)
    pct = p50_diff / max(statistics.median(prod_lat), 0.1) * 100
    print(f"\nMedian latency change: {p50_diff:+.1f}ms ({pct:+.1f}%)")
    if abs(pct) > 20:
        print("WARNING: Significant latency regression detected")
PYEOF
```

**Step 4 -- Detect behavioral differences**

```bash
# If structured logging, compare response body patterns
# This requires application-level logging of response shapes
echo "=== Checking for response body differences ==="
echo "(requires application-level structured logging of response schemas)"

# Check for new error patterns in shadow
echo ""
echo "=== Error patterns unique to shadow ==="
rg -i 'error|exception|panic|fatal' /tmp/shadow-access.log | \
  awk '{print $NF}' | sort | uniq -c | sort -rn | head -20
```

---

### 3. `report` --- Generate comprehensive diff analysis

**Step 1 -- Aggregate all findings**

Combine status code analysis, latency comparison, and behavioral differences into a single report.

```bash
python3 << 'PYEOF'
import json
from datetime import datetime

report = {
    "generated": datetime.utcnow().isoformat() + "Z",
    "service": "{SERVICE_NAME}",
    "namespace": "{NAMESPACE}",
    "duration": "{test_duration}",
    "verdict": "PENDING",
    "findings": []
}

# Assess overall verdict
# PASS: error rate delta < 1%, p50 latency delta < 10%, no new error patterns
# WARN: error rate delta 1-5%, latency delta 10-25%
# FAIL: error rate delta > 5%, latency delta > 25%, new crash patterns

print(json.dumps(report, indent=2))
PYEOF
```

**Report template:**

```
## Shadow Traffic Analysis Report

**Service:** {SERVICE_NAME} | **Duration:** {hours}h | **Verdict:** {PASS/WARN/FAIL}

### Status Code Comparison
| Code | Production | Shadow | Delta | Flag |
|------|-----------|--------|-------|------|

### Latency Comparison
| Percentile | Production | Shadow | Delta |
|-----------|-----------|--------|-------|
| p50       |           |        |       |
| p90       |           |        |       |
| p99       |           |        |       |

### Error Analysis
- New error types in shadow: {list}
- Error rate change: {production_rate}% -> {shadow_rate}%

### Behavioral Differences
- Response schema changes: {list or "none detected"}
- New log patterns: {list or "none"}

### Recommendation
{PROMOTE / INVESTIGATE / ROLLBACK shadow deployment}

### Cleanup
To remove shadow infrastructure:
  kubectl delete deployment {SERVICE_NAME}-shadow -n {NAMESPACE}
  kubectl delete virtualservice {SERVICE_NAME}-mirror -n {NAMESPACE}  # if Istio
```
