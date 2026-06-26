---
name: spring-boot-actuator-analyzer
description: Analyze Spring Boot Actuator endpoints for security, health checks, metrics exposure, and production configuration — audit info, health, and custom endpoints.
metadata:
  tags: ["spring-boot", "java", "actuator", "monitoring", "security"]
---

# Spring Boot Actuator Analyzer

Analyze Spring Boot Actuator configuration for security vulnerabilities, health check completeness, metrics exposure, and production readiness. Audit actuator endpoints, management port configuration, and custom health indicators.

## Usage

```
"Audit my Spring Boot Actuator configuration"
"Check Actuator security settings"
"Review health check endpoints"
"Are my Actuator endpoints production-safe?"
```

## How It Works

### 1. Configuration Discovery

```bash
# Find application properties
find . -name "application*.yml" -o -name "application*.yaml" -o -name "application*.properties" | head -10
# Check Actuator dependency
grep -r "actuator" build.gradle pom.xml 2>/dev/null
# Find custom health indicators
grep -rn "implements HealthIndicator\|extends AbstractHealthIndicator" src/ | head -10
```

### 2. Endpoint Security

**Critical checks:**
- Which endpoints are exposed to web? (`management.endpoints.web.exposure.include`)
- `*` wildcard exposes env, beans, configprops (sensitive data!)
- Management port same as application port (should be separate)
- Authentication configured on management endpoints
- CORS settings on actuator endpoints
- `/shutdown` endpoint enabled (remote shutdown risk)

**Recommended production config:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  server:
    port: 8081  # separate management port
  endpoint:
    health:
      show-details: when-authorized
    shutdown:
      enabled: false
```

### 3. Health Checks

- Database connectivity check present
- External service health indicators
- Custom health indicators for business logic
- Health check groups (liveness vs readiness)
- Kubernetes probe integration (/actuator/health/liveness, /readiness)
- Health check timeout configuration

### 4. Metrics

- Micrometer registry configured (Prometheus, Datadog, New Relic)
- Custom metrics for business KPIs
- JVM metrics exposed (memory, GC, threads)
- HTTP request metrics (latency, error rates)
- Cache metrics if using Spring Cache
- Database pool metrics

### 5. Info Endpoint

- Build info included (version, timestamp)
- Git info (commit, branch)
- Custom info contributors
- No sensitive data exposed in info endpoint

## Output

```
## Spring Boot Actuator Analysis

**Version:** Spring Boot 3.3.0 | **Actuator:** 3.3.0

### 🔴 Critical (2)
1. **All endpoints exposed** — application.yml
   `management.endpoints.web.exposure.include: "*"`
   Exposes /env (secrets), /beans, /configprops, /heapdump
   → Limit to: health,info,metrics,prometheus

2. **Management on same port** — no separate management port
   Actuator endpoints accessible on public-facing port 8080
   → Set management.server.port: 8081 (internal only)

### 🟡 Improvements (3)
3. Health details shown to everyone (`show-details: always`)
   → Change to `when-authorized`
4. No custom health indicators for external services
5. Missing Kubernetes probe endpoints (liveness/readiness groups)

### ✅ Good Practices
- Shutdown endpoint disabled
- Prometheus metrics registry configured
- Git and build info in /actuator/info
- Database health indicator auto-configured
```
