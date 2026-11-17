---
name: retry-optimizer
description: Optimize retry patterns for flaky or slow agents/services. Use when you see fixed-interval retries, repeated 30s/60s wait loops, Retrying... messages, wrapper timeouts, or performance bottlenecks caused by retry storms.
---

# Retry Optimizer

Optimize brittle retry loops into efficient backoff with jitter, circuit breaking, and bounded retries.

## When to Use

- Wrapper/agent keeps printing `Retrying in 30s...`
- Same command fails repeatedly with fixed sleep
- Retry storms under load
- No timeout / max-retry guard

## Quick Start

```bash
# Analyze current retry config
node skills/retry-optimizer/scripts/optimize.js analyze <config.json>

# Generate optimized config
node skills/retry-optimizer/scripts/optimize.js generate <config.json>

# Validate a retry config
node skills/retry-optimizer/scripts/optimize.js validate <config.json>
```

## Config Format

```json
{
  "retries": 3,
  "initialDelayMs": 1000,
  "maxDelayMs": 30000,
  "backoffFactor": 2,
  "jitterMs": 500,
  "timeoutMs": 5000,
  "retryOn": ["ECONNRESET", "ETIMEDOUT", "5xx"],
  "abortOn": ["4xx", "auth_failed"]
}
```

## Strategy

1. Replace fixed delay with exponential backoff
2. Add jitter to prevent synchronized retries
3. Cap max delay to avoid excessive waits
4. Set max retry limit to prevent infinite loops
5. Add per-attempt timeout
6. Classify errors: retryable vs abort

## Benchmark Results

| Scenario | Fixed Interval | Backoff + Jitter | Improvement |
|----------|---------------|------------------|-------------|
| 30s fixed (5 attempts) | 150,000ms | 32,208ms | **78.5% faster** |
| 60s fixed (5 attempts) | 300,000ms | 32,580ms | **89.1% faster** |
| 10s fixed (5 attempts) | 50,000ms | 16,315ms | **67.4% faster** |

Run benchmark:
```bash
node skills/retry-optimizer/scripts/benchmark.js
node skills/retry-optimizer/scripts/benchmark.js --scenarios=3 --attempts=5
```

## Notes

- Avoid unbounded retries; always set max retries
- Prefer backoff + jitter over fixed sleep
- Add circuit breaker for repeated failures
- Benchmark shows 67-89% reduction in total wait time
