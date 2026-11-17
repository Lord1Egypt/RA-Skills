# Capacity — Measuring Before Tuning

"Can it handle launch day?" is answered by a measurement, never by a configuration file. This is how to get a number you can defend, and what to do with it.

**Before answering any capacity question**, read `## Baselines` in `~/Clawic/data/server/memory.md` (or `baselines.md` if `## Boxes` points there). A previous measurement on this box, with its configuration recorded next to it, beats every formula in `workers.md`. Without prior numbers, say so and measure.

**Contents:** [What to Measure](#what-to-measure) · [Closed vs Open Loop](#closed-vs-open-loop) · [Test Design](#test-design) · [Finding the Saturation Point](#finding-the-saturation-point) · [Reading the Result](#reading-the-result) · [The Bottleneck Ladder](#the-bottleneck-ladder) · [Tuning Order](#tuning-order) · [Capacity Planning Arithmetic](#capacity-planning-arithmetic) · [Load Shedding](#load-shedding) · [Testing in Production, Safely](#testing-in-production-safely) · [Write It Down](#write-it-down)

## What to Measure

| Metric | Why it is the one that matters |
|---|---|
| p95 and p99 latency | The average hides everything. If p50 is 80ms and p99 is 9s, one user in a hundred thinks the site is broken, and that user is the one who complains |
| Throughput at an acceptable latency | "5,000 req/s" with p99 at 30 seconds is not capacity, it is a queue |
| Error rate under load | A server that sheds 2% of requests to stay fast may be the correct design; one that sheds 2% by accident is not |
| Saturated resource at the limit | CPU, memory, connections, descriptors, database, disk IO. The answer changes what you do next |
| Time to recover after the load stops | A system that takes ten minutes to drain a queue after a spike is fragile even if it survived |

Averages and totals are for dashboards. Percentiles and the saturating resource are for decisions.

## Closed vs Open Loop

The most common way a load test lies.

- **Closed loop** (the default in most tools): N virtual users, each sending the next request only after the last response. If the server slows down, the load automatically decreases. You can never observe the system past its saturation point, and latency looks better than reality — this is coordinated omission.
- **Open loop** (constant arrival rate, `--rate`/`constant-arrival-rate`): requests are sent on a schedule regardless of whether previous ones finished. This is how real traffic behaves, and it is the only mode that shows the queue building.

Use open loop for capacity work. Use closed loop only to model a fixed number of clients that genuinely wait, like an internal batch job.

## Test Design

- **Test one thing.** One endpoint, one payload size, one configuration. A mixed test tells you the system is slow; it does not tell you why.
- **Warm up first.** JIT compilation, connection pools, page cache, and CDN state all make the first 30 seconds unrepresentative. Discard them.
- **Generate load from another machine.** A load generator on the box competes for the CPU you are measuring and produces a number that is wrong in an unknown direction.
- **Use realistic payloads and realistic cache behavior.** Hammering one URL measures your cache; hitting a distribution of URLs measures your app. Both are useful, and they are different tests.
- **Keep keepalive on**, unless you are deliberately measuring handshake cost — otherwise you measure TCP and TLS setup and exhaust ephemeral ports on the generator (`workers.md`).
- **Change one variable between runs.** Two changes and a better number teaches nothing.

Tools: `k6` and `vegeta` for open-loop HTTP, `wrk`/`wrk2` for high throughput from one box, `oha`/`hey` for a quick check, `ab` for nothing serious (single-threaded, closed loop, no percentile fidelity).

## Finding the Saturation Point

Step the arrival rate and watch where latency stops being flat:

```
50 req/s   → p99  90ms   CPU 12%
100 req/s  → p99  95ms   CPU 24%
200 req/s  → p99 110ms   CPU 48%
340 req/s  → p99 180ms   CPU 82%     ← the knee
400 req/s  → p99 2.4s    CPU 96%     ← past it: the queue, not the work
450 req/s  → p99 9s + errors         ← collapse
```

The knee is your capacity: the highest rate where latency is still flat. Past it, every extra request adds queueing delay to every other request, which is why the degradation is not gradual — it is a cliff.

Plan against the knee, not the collapse point. A system running at its knee has zero headroom for a slow dependency, a backup, or a bot.

## Reading the Result

| Observation | Means |
|---|---|
| CPU at 100%, latency flat until the knee | Genuinely CPU-bound. More workers will not help; faster code or more cores will |
| CPU low, latency high | Waiting: database, an external API, a lock, a saturated thread pool. Adding workers may help; adding cores will not |
| Memory climbing steadily through the test | A leak or unbounded buffering. Fix before drawing any capacity conclusion |
| Errors before latency rises | A hard limit: connection pool, `pm.max_children`, file descriptors, upstream refusing |
| Latency fine, throughput capped at a round number | A configured limit is doing exactly what it was told |
| The generator's own CPU at 100% | You measured the generator. Rerun from a bigger box or two |
| Everything fine in the test, slow in production | The test is not representative: cache hit rate, payload size, concurrency mix, or a dependency that is only slow with real data |

## The Bottleneck Ladder

Check in this order; each rung invalidates the ones below it.

1. **The database.** A missing index or an N+1 query dwarfs every server-side tuning available. If p99 tracks a single query's duration, stop reading this file.
2. **The connection pool.** Requests waiting for a pooled connection look exactly like a slow app (`workers.md`).
3. **Worker count.** Too few and the queue grows; too many and memory swaps, which is worse than either.
4. **A per-process limit.** Descriptors, `pm.max_children`, thread pool size, `somaxconn`.
5. **The proxy.** Missing upstream keepalive, buffering to a slow disk, compression on large responses.
6. **The network.** Egress bandwidth, cross-machine round trips, TLS handshakes without resumption.
7. **The hardware.** Real, and the last thing to conclude — most single-box limits are one configuration value.

## Tuning Order

1. Measure and record the baseline (`## Baselines`).
2. Fix the top item on the ladder above.
3. Re-measure. If nothing improved, the diagnosis was wrong — revert the change rather than keeping it "just in case". Kept-just-in-case settings are how a config becomes unreadable.
4. Repeat until the knee is comfortably above projected peak, or until the next fix costs more than the hardware.

Reverting failed tuning is the discipline that separates a config someone can maintain from a pile of directives whose purpose nobody remembers.

## Capacity Planning Arithmetic

Convert business numbers into a rate before sizing anything:

```
peak_rps = daily_requests × peak_factor ÷ 86400
```

`peak_factor` is 3-5 for a consumer product with a daily rhythm, higher with a campaign or a scheduled event; a business-hours tool concentrates a day into ~8 hours, so 3× is the floor. Little's Law gives the concurrency behind it: `concurrent_requests = rps × average_seconds_per_request` — 200 req/s at 150ms is 30 in flight, which is what the worker and pool math must cover (`workers.md`).

Worked: 2M requests/day, peak factor 4 → `2,000,000 × 4 ÷ 86,400 ≈ 93 req/s` peak. Against a measured knee of 340 req/s that is 3.7× headroom — comfortable. Against a knee of 120 it is 1.3×, which will not survive a slow dependency.

Target 2-3× headroom over projected peak. Below 2× a single slow dependency takes the site down; above 5× you are paying for hardware to sit idle, unless the traffic is genuinely spiky.

## Load Shedding

Past the knee, refusing work quickly is better than accepting all of it slowly: a fast 503 lets a client retry or degrade, while an unbounded queue makes every user wait for a response that has already timed out at their end.

- Concurrency limit at the app (`--limit-concurrency`, a semaphore, a bounded queue) returning 503 with `Retry-After`.
- Rate limits at the proxy for abusive patterns (`proxy.md`).
- Timeouts everywhere, so a queued request is abandoned rather than served late to nobody (Rule 3).
- Priority: keep the health check and the login path working while shedding the expensive report endpoint.

## Testing in Production, Safely

Sometimes staging cannot reproduce it. When that is true:

- Off-peak, announced, with a defined abort condition ("stop at p99 > 1s or any 5xx above baseline") and someone watching.
- Start at 10% of the expected step and go up; a step that doubles at each rung reaches collapse before anyone reacts.
- Read-only endpoints first. Write endpoints pollute data and can exhaust ids, storage, or a payment sandbox.
- Have the revert ready before starting — for a config change, the previous file; for a deploy, the release directory (`deployment.md`).

## Write It Down

Every run produces a row in `## Baselines` in `memory.md`: date, service, the configuration measured (workers, threads, pool size, instance type), the result (knee rate, p95, p99), and the resource that saturated first (`memory-template.md`). Without the configuration column, the number is unreproducible and worthless six months later. The full output — the step table, the graphs, the tooling invocation — goes to `~/Clawic/data/server/artifacts/loadtest-<service>-<date>.md` with its `## Boxes` line added the same turn, because that is the document someone re-reads before the next launch.
