# SAP BTP Resilience Reference

## Overview

Building resilient applications ensures stability, high availability, and graceful degradation during failures. SAP BTP provides patterns and services to achieve enterprise-grade resilience.

## Key Resources

| Resource | Description |
|----------|-------------|
| Developing Resilient Apps on SAP BTP | Patterns and examples |
| Route Multi-Region Traffic | GitHub implementation |
| Architecting Multi-Region Resiliency | Discovery Center reference |

## Cloud Foundry Resilience

### Availability Zones

**Automatic Distribution:**
- Applications spread across multiple AZs
- No manual configuration required
- Platform handles placement

**During AZ Failure:**
- ~1/3 instances become unavailable (3-zone deployment)
- Remaining instances handle increased load
- Cloud Foundry reschedules to healthy zones

**Best Practice:**
Configure sufficient instances to handle load during zone failures:
```
Minimum instances = Normal load instances × 1.5
```

### Instance Configuration

```yaml
# manifest.yml
applications:
  - name: my-app
    instances: 3  # At least 3 for HA
    memory: 512M
    health-check-type: http
    health-check-http-endpoint: /health
```

### Health Checks

```javascript
// Express health endpoint
app.get('/health', (req, res) => {
  const health = {
    status: 'UP',
    checks: {
      database: checkDatabase(),
      messaging: checkMessaging()
    }
  };
  res.status(200).json(health);
});
```

## Kyma Resilience

### Istio Service Mesh

**Features:**
- Automatic retries
- Circuit breakers
- Timeouts
- Load balancing

### Configuration

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: my-app-dr
spec:
  host: my-app
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### Pod Distribution

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  template:
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: my-app
```

## ABAP Resilience

### Built-in Features

- Automatic workload distribution
- Work process management
- HANA failover support
- Session management

### Elastic Scaling

Automatic response to load:
- Scale between 1 ACU and configured max
- 0.5 ACU increments
- Metrics-based decisions

## Resilience Patterns

### Circuit Breaker

**Purpose**: Prevent cascading failures

**States:**
1. **Closed**: Normal operation
2. **Open**: Fail fast, skip calls
3. **Half-Open**: Test recovery

**Implementation (CAP - Node.js):**

> **Note**: The `opossum` library shown below is a third-party community package, not SAP-supported. Evaluate its maintenance status, compatibility with your CAP/Node.js versions, and security posture before production use. For Java applications, SAP Cloud SDK integrates with Resilience4j as the official resilience tooling.

```javascript
const CircuitBreaker = require('opossum');

const breaker = new CircuitBreaker(callRemoteService, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000
});

breaker.fallback(() => getCachedData());

const result = await breaker.fire(serviceParams);
```

### Retry with Exponential Backoff

**Purpose**: Handle transient failures

```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000;
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
```

### Bulkhead

**Purpose**: Isolate failures

```javascript
const Semaphore = require('semaphore');

const dbPool = Semaphore(10);  // Max 10 concurrent DB calls
const apiPool = Semaphore(20); // Max 20 concurrent API calls

async function callDatabase() {
  return new Promise((resolve, reject) => {
    dbPool.take(() => {
      performDbCall()
        .then(resolve)
        .catch(reject)
        .finally(() => dbPool.leave());
    });
  });
}
```

### Timeout

**Purpose**: Prevent hanging requests

```javascript
const timeout = (promise, ms) => {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), ms)
    )
  ]);
};

const result = await timeout(fetchData(), 5000);
```

### Graceful Degradation

**Purpose**: Provide reduced functionality instead of failing

```javascript
async function getProductDetails(id) {
  try {
    // Try full data
    return await getFromPrimaryService(id);
  } catch (error) {
    // Fallback to cached/reduced data
    const cached = await getFromCache(id);
    if (cached) return { ...cached, _degraded: true };

    // Final fallback
    return getBasicDetails(id);
  }
}
```

## Multi-Region Architecture

### Active-Passive

```
Region A (Primary)     Region B (Standby)
     ↓                      ↓
  Active                 Standby
     ↓                      ↓
  HANA Cloud           HANA Cloud (Replica)
```

**Failover**: Manual or automated switch

### Active-Active

```
        Global Load Balancer
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Region A              Region B
    ↓                   ↓
HANA Cloud           HANA Cloud
    ↓                   ↓
    └───── Replication ─┘
```

**Use Case**: Highest availability requirements

## Monitoring for Resilience

### Key Metrics

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate | > 1% | Alert, investigate |
| Latency p99 | > 2s | Scale, optimize |
| Circuit breaker trips | Any | Review dependencies |
| Retry rate | > 5% | Check downstream services |

### Alerting

```yaml
# SAP Alert Notification example
conditions:
  - name: high-error-rate
    propertyKey: error_rate
    predicate: GREATER_THAN
    propertyValue: "0.01"

actions:
  - name: page-oncall
    type: EMAIL
    properties:
      destination: oncall@example.com
```

## Best Practices

### Design

1. **Assume failure** - Everything can fail
2. **Design for graceful degradation**
3. **Implement health checks**
4. **Use async where possible**
5. **Plan for data consistency**

### Implementation

1. **Set timeouts** on all external calls
2. **Implement retries** with backoff
3. **Use circuit breakers** for dependencies
4. **Cache aggressively** where appropriate
5. **Log and monitor** all failures

### Operations

1. **Run chaos engineering** tests
2. **Practice disaster recovery**
3. **Monitor SLIs/SLOs**
4. **Automate failover** where possible

## Source Documentation

- Developing Resilient Applications: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/developing-resilient-applications-b1b929a.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/developing-resilient-applications-b1b929a.md)
- SAP BTP Resilience Guide: [https://help.sap.com/docs/btp/best-practices/developing-resilient-apps](https://help.sap.com/docs/btp/best-practices/developing-resilient-apps)
