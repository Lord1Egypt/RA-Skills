# Resizing — Bigger, Smaller, or More Than One

Read when a box is running out of something, when it is obviously oversized, and when someone asks whether they need a second server. The controlling fact: **CPU and RAM resizes are reversible, disk growth is not** (SKILL.md Rule 5).

**Before recommending a resize**, read the host's row in `~/Clawic/data/servers/servers.md` (current type and monthly cost) and `## Hosts` in `memory.md` (disk history — a disk that was already grown cannot go back), plus `## Spend` for what the fleet currently costs.

**Contents:** [Diagnose the Constraint First](#diagnose-the-constraint-first) · [Vertical Resize](#vertical-resize) · [The Disk Is a One-Way Door](#the-disk-is-a-one-way-door) · [Separate Volumes](#separate-volumes) · [Downsizing](#downsizing) · [When One Box Is No Longer the Answer](#when-one-box-is-no-longer-the-answer) · [Horizontal Patterns](#horizontal-patterns) · [What Blocks Horizontal Scaling](#what-blocks-horizontal-scaling) · [Cheaper Than Any Resize](#cheaper-than-any-resize)

## Diagnose the Constraint First

Resizing the wrong dimension is expensive and permanent in one case out of three. Establish which resource is actually binding before touching anything:

| Symptom | Binding constraint | Not the answer |
|---|---|---|
| OOM kills, continuous swapping, low available memory | RAM | More vCPU |
| Sustained high user CPU across all cores, requests queueing behind compute | CPU | More RAM |
| High steal with low user CPU | Neither — noisy neighbour (`operations.md`) | Any resize on the same node |
| IO wait dominating, slow database queries on a small dataset | Disk throughput, or an unindexed query | A bigger plan, usually |
| Disk above 85% | Storage | A whole new plan tier, if a volume would do |
| Slow only under a specific job | Concurrency or a scheduling problem | Any resize |

The most common misdiagnosis: an unindexed database query presenting as "we need a bigger server". Query optimisation is free and permanent; a plan upgrade is monthly and hides the problem until it returns at the next tier.

## Vertical Resize

- Almost always the right first move: a reboot of a few minutes, no data movement, and reversible for CPU and RAM.
- **Step one size at a time and observe.** Plan families roughly double resources per step, so a two-step jump usually overshoots and you pay the difference indefinitely.
- Most providers offer both a **CPU/RAM-only** resize and a **full** resize that also grows the disk. Choose the first unless disk is genuinely the constraint, because the second is the irreversible one.
- Plan on doing it in a maintenance window: the machine is off during the operation, and the operation occasionally takes longer than advertised when the target node is busy.
- Snapshot before resizing. It costs a click and covers the rare case where the machine does not come back cleanly.
- After the resize, update the host's `Type` and `Monthly` in `servers.md` — an inventory with last year's plan sizes produces wrong cost answers for months.

## The Disk Is a One-Way Door

- Growing the root disk is irreversible at essentially every provider. Once grown, the plan cannot go back down, so the new size becomes the permanent floor of that machine's cost.
- Consequence: **the smallest disk that comfortably holds 18 months of growth is the right size**, not the largest you can afford.
- Growing usually requires extending the partition and the filesystem inside the machine as well. Providers vary in whether they do this automatically; a resized disk that shows the old size inside is this step, not a failure.
- Before growing, free space first (`operations.md`). Log files, container images, and package caches routinely account for more than the shortfall.
- Record every growth in `changes/<year>.md` with `Reversible? no`. Six months later, "why is this box on the expensive tier" has an answer.

## Separate Volumes

The structural fix for the one-way door, and worth doing at provisioning time:

- Application data on a **separate block volume** means storage grows and shrinks — or detaches and moves to another machine — without touching the plan.
- Volumes are usually priced per GB with no compute attached, so storage-heavy workloads get much cheaper than the equivalent plan upgrade.
- They also survive the instance: destroy and rebuild the machine, reattach the volume, and the data is untouched. This is what makes Rule 6 and Rule 7 cheap.
- Cost: a mount to configure, an entry in the filesystem table (with `nofail`, or a failed volume stops the boot — `access.md`), and slightly higher latency than local storage.
- Not for the database of a latency-sensitive workload, where local storage measurably wins.

## Downsizing

- CPU and RAM downsizes are supported on most providers and are the fastest saving available on an oversized fleet.
- **Evidence before downsizing**: at least 14 days of metrics. Sustained utilisation below roughly 20% with no periodic peak is a candidate; each step down roughly halves the compute cost.
- Check for the periodic load first — a nightly batch, a weekly report, a monthly close. Downsizing against a 14-day average that excluded the month-end job produces an outage on a predictable date.
- Memory is the risky dimension: a workload that fits with cache to spare degrades sharply once the cache is gone. Reduce memory one step, watch swap activity for a week.
- A disk that was grown blocks the downsize on providers where plan tiers bundle disk. The workaround is a migration to a new smaller instance, restoring from backup — which is the timed restore drill, done for profit (`backups.md`).

## When One Box Is No Longer the Answer

Three legitimate triggers. Growth alone is not one of them:

1. **Availability.** One box means every reboot, every failed upgrade, and every node failure is downtime. If that is unacceptable, the answer is two machines and a load balancer, not a bigger machine.
2. **Isolation.** Two workloads with different owners, different uptime expectations, or wildly different risk profiles (a public application and an internal database, a production site and a build agent) should not share a failure domain.
3. **A dimension that will not fit.** The largest plan is a real ceiling, and approaching it is the moment to design the split rather than to buy the top tier.

If none of the three applies, a bigger box is simpler, cheaper, and more reliable than two smaller ones. Distributed systems have failure modes that a single machine cannot have.

## Horizontal Patterns

Ordered by how much complexity they add:

| Pattern | Buys | Costs |
|---|---|---|
| Move static assets and uploads to object storage plus a CDN | Bandwidth, disk, and a large share of the load | Almost nothing; do this first |
| Split the database onto its own box | Isolation and independent sizing of the two constraints | Network latency between them, one more machine to operate |
| Two application servers behind a load balancer | Availability and rolling deploys | Shared session state and shared uploads must be solved first |
| Read replicas | Read scale | Replication lag becomes an application concern |
| Separate worker box for background jobs | The batch job stops affecting request latency | A queue, and a second deployment path |
| Managed database instead of self-run | Failover and patching handled | Several times the resource cost (`choosing.md`) |

## What Blocks Horizontal Scaling

Fix these before adding the second application server, or the second server makes things worse:

- **Sessions in local process memory** — users get logged out at random as requests land on different machines. Move them to a shared store or signed cookies.
- **Uploads written to the local filesystem** — half the files exist on each box. Move them to object storage or shared storage.
- **Cron jobs on every node** — the nightly job now runs twice, sending duplicate mail or double-charging. A single scheduler, or a lock.
- **Local caches assumed to be coherent** — invalidation on one box leaves the other serving stale data.
- **Database migrations on deploy** — with two nodes deploying, two processes attempt the same migration. Expand-contract, applied once.
- **The load balancer itself**, if it is a machine you run: it is now the single point of failure you were trying to remove. A provider load balancer is the right default here.

## Cheaper Than Any Resize

Before spending monthly money, in order of return:

1. **Add the missing database index.** Free, permanent, frequently a 10× improvement on the one query that dominates.
2. **Turn on caching** at the right layer — HTTP caching, a cache in front of expensive queries, a CDN for anything static.
3. **Turn off debug logging** left on since an incident: it consumes disk, IO, and CPU (`operations.md`).
4. **Move assets off the box** — the single largest reduction in both bandwidth and load for most web workloads.
5. **Set a memory limit on the greedy process** so it no longer forces the box to be sized for its worst moment.
6. **Then** resize.

---

**Write it down.** Every resize updates the host's `Type` and `Monthly` (with currency) in `~/Clawic/data/servers/servers.md`, and gets a row in `~/Clawic/data/vps/changes/<year>.md` with `Reversible?` — `no` for any disk growth, address release, or plan change that bundled disk. Disk size history and attached volumes go in `## Hosts`. If the resize was driven by a spend review or produces a saving, add the figure to `## Spend` → `### Optimization Log` with its currency. A decision to split into more than one machine is an architecture decision: write it to `~/Clawic/data/vps/artifacts/architecture-<scope>.md` with the trigger, the layout, and what was rejected, and add its `## Boxes` line in the same turn.
