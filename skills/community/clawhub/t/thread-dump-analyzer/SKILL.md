---
name: thread-dump-analyzer
description: Analyze thread dumps and goroutine dumps to diagnose deadlocks, thread pool exhaustion, contention hotspots, and blocked threads. Supports JVM thread dumps, Go goroutine dumps, Python threading dumps, and Node.js async stack traces.
---

# Thread Dump Analyzer

Diagnose concurrency issues from thread dumps. Find deadlocks, identify contention hotspots, detect thread pool exhaustion, and map blocked/waiting thread chains — across JVM, Go, Python, and Node.js runtimes.

Use when: "analyze thread dump", "application is hanging", "deadlock detected", "threads are stuck", "goroutine leak", "connection pool exhausted", "thread pool full", "application not responding", or when an application stops processing requests.

## Commands

### 1. `analyze` — Parse and Diagnose Thread Dump

#### Step 1: Capture Thread Dump

**JVM (Java/Kotlin/Scala):**
```bash
# Method 1: jstack
jstack $(pgrep -f 'java.*your-app') > /tmp/thread-dump.txt 2>&1

# Method 2: kill -3 (prints to stdout/stderr)
kill -3 $(pgrep -f 'java.*your-app')

# Method 3: jcmd
jcmd $(pgrep -f 'java.*your-app') Thread.print > /tmp/thread-dump.txt
```

**Go:**
```bash
# Method 1: SIGQUIT (prints all goroutines to stderr)
kill -QUIT $(pgrep -f 'your-go-app')

# Method 2: pprof endpoint
curl -s http://localhost:6060/debug/pprof/goroutine?debug=2 > /tmp/goroutine-dump.txt

# Method 3: runtime.Stack()
curl -s http://localhost:6060/debug/pprof/goroutine?debug=1 | head -50
```

**Python:**
```bash
# Method 1: faulthandler
kill -USR1 $(pgrep -f 'python.*your-app')

# Method 2: programmatic
python3 -c "
import threading, traceback, sys
for thread_id, frame in sys._current_frames().items():
    thread = next((t for t in threading.enumerate() if t.ident == thread_id), None)
    name = thread.name if thread else 'Unknown'
    print(f'\n--- Thread {name} ({thread_id}) ---')
    traceback.print_stack(frame)
"
```

**Node.js:**
```bash
# Async stack traces
kill -USR1 $(pgrep -f 'node.*your-app')
# Connect via chrome://inspect and capture
```

#### Step 2: Parse Thread States

Classify each thread/goroutine:

| State | JVM | Go | Meaning |
|-------|-----|-----|---------|
| **RUNNABLE** | RUNNABLE | running | Actively executing |
| **WAITING** | WAITING/TIMED_WAITING | select/chan receive | Waiting for signal |
| **BLOCKED** | BLOCKED | semacquire | Waiting for lock |
| **PARKED** | PARKING | sleep | Suspended |
| **I/O** | in native | IO wait/syscall | Waiting for I/O |

Count threads by state:
```
RUNNABLE: 15 (18%)
WAITING: 45 (54%)
BLOCKED: 12 (14%) ⚠️ HIGH
TIMED_WAITING: 10 (12%)
PARKED: 2 (2%)
```

If BLOCKED > 10% → likely contention issue.

#### Step 3: Detect Deadlocks

**JVM:** Look for "Found one Java-level deadlock" in dump output.

**Manual detection (any language):**
1. Find all BLOCKED threads and what lock they're waiting for
2. Find who holds each lock
3. Check for cycles: Thread A waiting for Lock 1 held by Thread B, Thread B waiting for Lock 2 held by Thread A

```
🔴 DEADLOCK DETECTED:
  Thread "worker-1" BLOCKED waiting for Lock@0x7f3a (held by "worker-3")
  Thread "worker-3" BLOCKED waiting for Lock@0x8b2c (held by "worker-1")
  → Circular dependency: worker-1 → Lock@0x7f3a → worker-3 → Lock@0x8b2c → worker-1
```

#### Step 4: Detect Thread Pool Exhaustion

```
Thread pool "http-handler" — 200/200 threads (100% utilized)
  180 threads BLOCKED on database connection pool
  15 threads WAITING on external API response
  5 threads RUNNABLE (processing)
  
⚠️ THREAD POOL EXHAUSTED: all handler threads consumed
Root cause: database connection pool is the bottleneck
  → Connection pool max: 20, all 20 in use
  → Average query time: 2.3s (normally 50ms) — likely slow query or lock contention
```

#### Step 5: Identify Contention Hotspots

Group blocked threads by the lock they're waiting on:

```markdown
## Lock Contention Hotspots

### Lock: DatabaseConnectionPool@0x7f3a — 85 threads waiting
- Held by: Thread "worker-42" (executing SQL query for 15 seconds)
- Waiters: 85 threads blocked for avg 8.3 seconds
- Impact: All incoming requests queued
- Fix: Investigate slow query in worker-42, increase pool size

### Lock: CacheManager@0x8b2c — 12 threads waiting
- Held by: Thread "cache-refresh-1" (loading cache from DB)
- Waiters: 12 threads blocked for avg 1.2 seconds
- Impact: Cache reads blocked during refresh
- Fix: Use read-write lock, or double-buffering for cache refresh
```

#### Step 6: Generate Report

```markdown
# Thread Dump Analysis

## Summary
- Total threads: 215
- Deadlocks: 0
- Thread pool utilization: 100% (EXHAUSTED)
- Top contention: DatabaseConnectionPool (85 blocked threads)
- Likely root cause: slow query holding all DB connections

## Thread State Distribution
- RUNNABLE: 15 (7%)
- BLOCKED: 97 (45%) 🔴
- WAITING: 85 (40%)
- TIMED_WAITING: 18 (8%)

## Root Cause Chain
1. Slow SQL query (15s) holding connection in worker-42
2. Connection pool (max 20) exhausted — all connections busy
3. 85 HTTP handler threads blocked waiting for connection
4. Thread pool (200) exhausted — all threads consumed
5. New requests rejected with 503

## Recommendations
1. IMMEDIATE: Kill slow query and investigate (likely missing index)
2. SHORT-TERM: Add query timeout (5s max)
3. MEDIUM-TERM: Increase connection pool to 50
4. LONG-TERM: Add circuit breaker on DB access
```

### 2. `compare` — Compare Two Thread Dumps

Take dumps at different times and highlight:
- New blocked threads
- Threads stuck in same state (not making progress)
- Growing thread count (leak)
- Changed contention patterns

### 3. `goroutine-leak` — Detect Go Goroutine Leaks

Specifically for Go applications:
- Compare goroutine counts over time
- Find goroutines stuck in channel receive with no sender
- Detect context leak (context not cancelled)
- Find leaked HTTP connections (response body not closed)
