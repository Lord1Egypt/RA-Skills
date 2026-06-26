---
name: sidekiq-job-analyzer
description: Analyze Sidekiq job configurations for reliability, performance, queue design, retry policies, and memory safety — optimize Ruby background processing.
metadata:
  tags: ["sidekiq", "ruby", "background-jobs", "redis", "performance"]
---

# Sidekiq Job Analyzer

Analyze Sidekiq job configurations for reliability, performance, queue design, retry policies, and memory safety. Audit worker classes, queue priorities, concurrency settings, and Redis usage. Use when jobs are slow, failing silently, or consuming too much memory.

## Usage

```
"Analyze my Sidekiq jobs for issues"
"Check queue configuration and priorities"
"Audit retry policies and error handling"
"Optimize Sidekiq performance and memory usage"
```

## How It Works

### 1. Job Discovery

```bash
# Find all Sidekiq workers/jobs
grep -rn "include Sidekiq::Job\|include Sidekiq::Worker" app/ lib/ | head -30
# Check Sidekiq config
cat config/sidekiq.yml 2>/dev/null
cat config/initializers/sidekiq.rb 2>/dev/null
# Check queue definitions
grep -rn "sidekiq_options" app/ lib/ | head -20
```

### 2. Job Configuration Audit

**Retry policies:**
- Jobs without explicit retry count (default: 25 retries over 21 days)
- Missing `dead: false` on non-critical jobs
- No custom error handling or `sidekiq_retries_exhausted` callback
- Retry with exponential backoff vs fixed intervals

**Queue design:**
- Too many queues (scheduler overhead)
- Critical jobs sharing queues with bulk operations
- Missing queue weights/priorities
- Jobs in wrong queues (heavy job in `default` blocking lightweight jobs)

**Idempotency:**
- Jobs that aren't safe to retry (double-sends, duplicate charges)
- Missing unique job constraints (sidekiq-unique-jobs)
- State mutations without proper locking

**Performance:**
- Long-running jobs blocking the queue
- Jobs that should be batched (Sidekiq Pro/Enterprise)
- Missing `pool` size for database-heavy workers
- Thread-safety issues in job code

### 3. Memory Analysis

- Jobs loading large datasets into memory
- Missing `find_each` / `find_in_batches` for ActiveRecord queries
- String concatenation in loops (memory fragmentation)
- Jobs that grow memory without bound
- Redis memory usage by queues and retry sets

### 4. Monitoring & Observability

- Sidekiq Web UI configured and accessible?
- Dead job monitoring and alerting
- Queue latency monitoring
- Error tracking integration (Sentry, Bugsnag)
- Custom metrics for business-critical jobs

### 5. Redis Configuration

- Redis connection pool sizing
- Redis memory limits and eviction policy
- Redis persistence settings for job durability
- Sentinel/Cluster for high availability

## Output

```
## Sidekiq Job Analysis

**Workers:** 23 | **Queues:** 5 | **Redis:** 512MB used

### 🔴 Critical (2)
1. **Non-idempotent payment job** — PaymentProcessor has no uniqueness guard
   If retried, can charge customer multiple times
   → Add `sidekiq_options unique: :until_executed`

2. **Memory leak in ReportGenerator** — loads all records per tenant
   Grows to 2GB+ for large tenants, triggers OOM kill
   → Use `find_in_batches(batch_size: 1000)` and stream output

### 🟡 Improvements (4)
3. Default retry count (25) on BulkEmailJob — 21 days of retries for marketing emails
4. Queue `default` has 15 different job types — split critical from bulk
5. No `sidekiq_retries_exhausted` handler on 18/23 workers
6. Missing dead job monitoring (12,847 dead jobs accumulated)

### 📊 Queue Health
| Queue | Jobs/hr | Latency | Workers |
|-------|---------|---------|---------|
| critical | 120 | 0.1s | 5 |
| default | 3,400 | 45s ⚠️ | 10 |
| mailers | 800 | 2s | 3 |
| reports | 50 | 5min ⚠️ | 2 |
| bulk | 12,000 | 30min | 5 |

### ✅ Good Practices
- Separate queues for different priorities
- Sentry integration for error tracking
- Redis Sentinel configured for HA
```
