# Backend DevOps

Docker, Kubernetes, deployment strategies, and monitoring.

## Docker

### Best Practices
- Use multi-stage builds
- Minimize image size
- Use .dockerignore
- Don't run as root
- Use specific tags, not `latest`

### Example Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

## Kubernetes

### Core Concepts
- **Pods** - Smallest deployable unit
- **Services** - Network access to pods
- **Deployments** - Manage pod replicas
- **ConfigMaps** - Configuration data
- **Secrets** - Sensitive data

### Deployment Strategies
- **Rolling Update** - Gradual replacement
- **Blue-Green** - Two environments, switch traffic
- **Canary** - Gradual traffic shift

### Best Practices
- Use resource limits
- Health checks (liveness, readiness)
- Horizontal Pod Autoscaling
- Namespace isolation
- RBAC for security

## CI/CD Pipelines

### Stages
1. **Build** - Compile, test, package
2. **Test** - Run test suite
3. **Deploy** - Deploy to environment
4. **Verify** - Health checks, smoke tests

### Best Practices
- Fast feedback loops
- Parallel execution
- Cache dependencies
- Secure secrets management
- Automated rollback

## Deployment Strategies

### Blue-Green Deployment
- Two identical environments
- Deploy to inactive environment
- Switch traffic when ready
- Instant rollback

### Canary Deployment
- Deploy to subset of users
- Monitor metrics
- Gradually increase traffic
- Rollback if issues

### Rolling Deployment
- Gradual replacement
- Zero downtime
- Automatic rollback on failure

## Feature Flags

- 90% fewer failures
- Gradual feature rollout
- A/B testing
- Instant rollback
- Kill switches

## Monitoring

### Metrics
- **Application Metrics** - Response time, error rate, throughput
- **Infrastructure Metrics** - CPU, memory, disk, network
- **Business Metrics** - User actions, revenue, conversions

### Tools
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Datadog** - APM and monitoring
- **New Relic** - Application monitoring

## Logging

### Best Practices
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARN, ERROR)
- Include context (request ID, user ID)
- Centralized log aggregation
- Log retention policies

### Tools
- **ELK Stack** - Elasticsearch, Logstash, Kibana
- **Loki** - Log aggregation
- **Fluentd** - Log forwarding

## Tracing

### Distributed Tracing
- Track requests across services
- Identify bottlenecks
- Debug distributed systems

### Tools
- **OpenTelemetry** - Observability standard
- **Jaeger** - Distributed tracing
- **Zipkin** - Distributed tracing

## Health Checks

### Liveness Probe
- Is the application running?
- Restart if unhealthy

### Readiness Probe
- Is the application ready to serve traffic?
- Remove from load balancer if not ready

### Startup Probe
- Is the application starting up?
- Give time for initialization
