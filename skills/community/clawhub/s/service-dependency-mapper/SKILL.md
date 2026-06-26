---
name: service-dependency-mapper
description: Auto-discover and map service dependencies from code, configs, and runtime data. Generate dependency graphs, identify critical paths, find single points of failure, and assess blast radius for each service.
---

# Service Dependency Mapper

Map your service dependencies before an outage teaches you what they are. Auto-discover dependencies from code imports, config files, network traffic, and runtime traces — then generate dependency graphs, identify critical paths, and assess blast radius.

Use when: "map our services", "what depends on what", "service dependency graph", "blast radius analysis", "single point of failure", "what breaks if X goes down", "architecture visualization", or during incident planning.

## Commands

### 1. `discover` — Auto-Detect Service Dependencies

#### Step 1: Static Analysis — Code and Config

```bash
# Find service URLs in code
rg "https?://[a-z][-a-z0-9]*(\.[a-z][-a-z0-9]*)*[:/]" \
  --type-not binary -g '!node_modules' -g '!vendor' -g '!*.test.*' 2>/dev/null | \
  grep -v "example\.com\|localhost\|127\.0\.\|schema\.org" | head -30

# Find service names in Docker Compose
rg "depends_on|links:|container_name:" docker-compose*.yml 2>/dev/null

# Find service references in Kubernetes
rg "serviceName:|host:|backend:" k8s/ manifests/ helm/ 2>/dev/null

# Find database/cache connections
rg "DATABASE_URL|REDIS_URL|MONGO_URI|POSTGRES_|MYSQL_|AMQP_URL|KAFKA_BROKER" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null

# Find message queue producers/consumers
rg "publish\(|subscribe\(|produce\(|consume\(|\.queue\(|channel\." \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null | head -20

# Find gRPC/REST client instantiations
rg "GrpcClient|HttpClient|axios\.create|fetch\(.*service|\.NewClient" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null
```

#### Step 2: Runtime Analysis (if available)

```bash
# Kubernetes services
kubectl get services -A -o json | python3 -c "
import json, sys
svcs = json.load(sys.stdin)['items']
for svc in svcs:
    ns = svc['metadata']['namespace']
    name = svc['metadata']['name']
    stype = svc['spec']['type']
    ports = [str(p['port']) for p in svc['spec'].get('ports', [])]
    print(f'{ns}/{name} ({stype}) ports:{','.join(ports)}')
"

# Service mesh (Istio/Linkerd) — actual traffic dependencies
kubectl get destinationrules -A 2>/dev/null
istioctl proxy-config cluster <pod-name> 2>/dev/null | grep -v "BlackHole\|PassthroughCluster"
```

#### Step 3: Build Dependency Graph

```python
dependencies = {
    'api-gateway': {
        'depends_on': ['auth-service', 'user-service', 'order-service'],
        'type': 'sync',  # sync HTTP calls
        'criticality': 'critical',
    },
    'order-service': {
        'depends_on': ['postgres', 'payment-service', 'kafka'],
        'type': 'mixed',
        'criticality': 'critical',
    },
    'notification-service': {
        'depends_on': ['kafka', 'smtp-relay', 'redis'],
        'type': 'async',
        'criticality': 'low',
    },
}
```

#### Step 4: Generate Dependency Map

```markdown
# Service Dependency Map

## Graph (text representation)
```
[External Users]
    │
    ▼
[api-gateway] ─sync──► [auth-service] ─sync──► [postgres-auth]
    │ │
    │ ├─sync──► [user-service] ─sync──► [postgres-users]
    │ │                          └─async─► [redis-cache]
    │ │
    │ └─sync──► [order-service] ─sync──► [postgres-orders]
    │                │             └─sync──► [payment-service] ─► [Stripe API]
    │                │
    │                └─async──► [kafka]
    │                              │
    │                              ├──► [notification-service] ─► [SMTP]
    │                              └──► [analytics-service] ─► [ClickHouse]
```

## Critical Path
api-gateway → order-service → postgres-orders
(Failure here = orders cannot be placed)

## Single Points of Failure
1. 🔴 **postgres-orders** — no replica, single instance
2. 🔴 **api-gateway** — single entry point, no fallback
3. 🟡 **kafka** — 3 brokers but no multi-AZ
4. 🟡 **Stripe API** — external dependency, no fallback payment provider

## Blast Radius Analysis
| If this fails... | These break... | Users affected |
|-------------------|---------------|----------------|
| postgres-orders | order-service, api-gateway (partial) | 100% orders |
| auth-service | All authenticated endpoints | 100% users |
| kafka | notifications, analytics | 0% (graceful degradation) |
| redis-cache | user-service (slow, not down) | 0% (cache miss only) |
| Stripe API | payment-service, orders | 100% new orders |
```

### 2. `blast-radius` — Analyze Impact of Service Failure

For a given service, trace all dependents (recursively):
- Direct dependents (call this service)
- Transitive dependents (depend on direct dependents)
- User-facing impact (which user flows break?)
- Graceful degradation (can dependents function without this service?)

### 3. `visualize` — Generate Diagram

Output dependency graph in:
- Mermaid (for GitHub/GitLab markdown)
- DOT (for Graphviz)
- PlantUML
- D2

### 4. `health` — Assess Architecture Health

Score the architecture based on:
- Depth of dependency chain (deep chains = fragile)
- Fan-out per service (wide fan-out = complex failure modes)
- Circular dependencies (exist? how many?)
- Single points of failure count
- Ratio of sync vs async dependencies
- External dependency count and fallback coverage
