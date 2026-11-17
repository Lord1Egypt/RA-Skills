# Operations — The Four Killers and the Weekly Reality

Read when a box is slow, full, or behaving oddly with no deployment to blame, and when setting up the routine that keeps a server boring. `patch_window` sets when reboots happen; recurring work lives in `## Due`.

**At the start of a session that touches a live host**, check `## Due` in `~/Clawic/data/vps/memory.md` against today's date and state any overdue item in one line — overdue reboots and overdue restore drills are the two that matter.

**Contents:** [The Four Killers](#the-four-killers) · [Disk](#disk) · [Inodes](#inodes) · [Memory](#memory) · [Steal Time](#steal-time) · [Updates and the Reboot Nobody Does](#updates-and-the-reboot-nobody-does) · [Logs](#logs) · [Monitoring That Is Worth Its Cost](#monitoring-that-is-worth-its-cost) · [The Weekly Ten Minutes](#the-weekly-ten-minutes) · [Uptime Is Not the Goal](#uptime-is-not-the-goal)

## The Four Killers

Nearly every "the VPS is broken" report with no deployment behind it is one of four things, and they occur in this order of frequency:

| Killer | How it presents | Why it wins |
|---|---|---|
| Disk full | Services fail to write, then fail to start; logins break; the box still pings | Nothing warns you at 80%, and the last 5% disappears in an hour |
| Inodes exhausted | "No space left on device" with free space showing | Millions of small files; the error message is misleading |
| Out of memory | A process disappears; the site 502s; nothing in the application log | The kernel kills the largest process, which is rarely the guilty one |
| Steal time | Everything slow, CPU shows idle, no single culprit | The hypervisor is elsewhere; nothing on the box can fix it |

Check all four before debugging the application. Each takes seconds and eliminates a class of cause.

## Disk

- **Alert at 75%, act at 85%.** A full root filesystem breaks logging, package management, database writes, and sometimes SSH, all at once, and the recovery path is the console (`access.md`).
- **The usual consumers**, in order: log files and the journal; container images, build caches, and stopped containers; package manager caches; database write-ahead logs when a replica or archiver has stalled; backups written to the same disk they are backing up.
- **Deleted files held open** are the confusing case: usage tools disagree with each other because a deleted file still occupies space until the process holding it exits. Symptom: sums do not match. Fix: restart the holder, usually a log writer.
- **Alerts and metrics on a separate partition or volume** for data means a runaway application fills its own volume, not the root filesystem. This is a provisioning-time decision (`resizing.md`).
- Growing the disk is one-way (Rule 5). Free space first, grow second.

## Inodes

- A filesystem can be 30% full and completely unable to create a file. The error message says "no space", which sends everyone to the wrong tool.
- Causes: session or cache directories with millions of tiny files, a mail queue, an unpruned container store, a log directory rotating into infinity.
- Check inode usage whenever a "disk full" error contradicts a healthy-looking disk. It takes one command and resolves the contradiction immediately.
- The fix is deleting files, not growing the disk — inode counts are usually fixed at filesystem creation.

## Memory

- **Free memory near zero is normal.** The kernel uses everything spare for cache. The number that matters is available memory, not free memory; a monitoring rule written against the wrong one alerts constantly and teaches everyone to ignore it.
- **Swap is the shock absorber** (`provisioning.md`). No swap means the first spike kills a process instead of slowing down.
- **The out-of-memory killer picks by a badness score dominated by size**, so it kills the database rather than the build that caused the pressure. The fix is a memory limit on the greedy service, not a bigger box — and if it is the database that is genuinely growing, then it is a bigger box (`resizing.md`).
- **Continuous swapping is a sizing problem.** Occasional swap use is healthy; a box swapping steadily is running with an undersized working set and will have unpredictable latency until it is resized.
- Per-service memory limits through the service manager are the cheapest containment: a runaway worker dies alone instead of taking the database with it.

## Steal Time

- Steal is the percentage of time the virtual CPU was ready to run and the hypervisor gave the physical core to somebody else. It is visible in standard system monitors and is the only honest measure of noisy-neighbour impact.
- **Sustained above ~5% is a problem**; brief spikes are normal. It correlates with plan tier: budget shared plans are oversubscribed by design (`providers.md`).
- Nothing on the box fixes it. The options are: migrate the instance to another node — on many providers a stop-and-start relocates it — move to a different location, or move to dedicated vCPU.
- Distinguish it from your own load: high steal with low user CPU means the neighbour; high user CPU means you.

## Updates and the Reboot Nobody Does

- Automatic **security** updates on, always. The realistic failure is neglect, not a bad patch.
- **Unattended upgrades do not restart services and never reboot for a kernel.** A box that reports itself fully patched can be running last year's kernel and a vulnerable library still resident in memory. This is the most common false sense of safety in the domain.
- Two checks make it honest: does a reboot-required marker exist, and which running processes are still using deleted (replaced) libraries. Both have standard tooling on every distribution.
- **A stated reboot policy**, in `## Due` and driven by `patch_window`: monthly for most workloads, immediately for a remotely exploitable kernel or SSH issue. "When convenient" means never.
- Live kernel patching exists on some distributions and defers the reboot rather than removing it.
- **Reboot deliberately, not accidentally.** A box that has been up 400 days has never proven it boots. Every reboot is a test of the fstab, the service enablement, and the mount configuration — do it on a Tuesday morning by choice, not at 3am by surprise.
- Major distribution upgrades: snapshot first, read the release notes for the two packages you depend on most, and have the console open.

## Logs

- **The journal has a default size cap** (a fraction of the filesystem, with an upper bound) which is generous on a large disk and still surprising on a small one. Set an explicit cap on any box under 40 GB.
- **Rotate everything the application writes.** An unrotated application log is the single most common cause of a full disk after container images.
- Debug logging left on after an incident is the second. Turn it off in the same session it stops being needed.
- **Ship logs off the box** once there are two boxes, or once you need to investigate something after the box that produced it is gone. Until then, longer local retention beats a monitoring stack nobody configured — you cannot investigate a compromise found on day 20 with 7 days of logs (`security.md`).
- Retention has a floor set by investigation, not by disk: 30 days is a reasonable default for a public server.

## Monitoring That Is Worth Its Cost

The minimum that pays for itself on a single VPS, in order of value:

1. **External uptime check** on the actual service URL, from outside the box, alerting somewhere a human sees it. A check running on the server cannot report that the server is down.
2. **Disk usage alert at 75%.** The single highest-value threshold in this file.
3. **Backup age alert**, evaluated off-box (`backups.md`).
4. **Certificate expiry**, if anything terminates TLS on this box — expiry is a scheduled, entirely preventable outage.
5. **Memory available and swap activity**, to catch the sizing problem before the OOM killer does.
6. **Outbound traffic volume**, which catches both the runaway backup job and the compromise (`security.md`).

Beyond that, a metrics stack costs RAM on a box you are paying for and needs someone to read it. On one server, the provider's own graphs plus the six checks above beat a self-hosted observability stack that is itself the largest process on the machine.

## The Weekly Ten Minutes

| Check | Looking for |
|---|---|
| Disk and inode usage on every host | The slow climb, before it is an outage |
| Reboot-required markers | Patched but not active (above) |
| Backup age and the last drill date | Silent stoppage |
| Failed authentication volume | An ongoing attack, or your own tooling banning itself |
| Certificate expiry dates | Anything inside 21 days |
| Provider status and maintenance notices | Scheduled live migrations and node maintenance, which look like unexplained reboots afterwards |
| Anything running that you do not recognise | The cheapest compromise check there is |
| Hosts in the inventory that nobody owns | Next month's wasted spend (`costs.md`) |

## Uptime Is Not the Goal

- A single VPS has a realistic ceiling of a few nines including provider maintenance, and chasing more on one box is wasted effort — the next nine costs a second machine, a load balancer, and a replicated database (`resizing.md`).
- **Recovery time is the number that matters**, and it is set by the rebuild script and the timed restore, not by the plan tier.
- Provider live migrations and node failures happen. Design for a box that can disappear: state in a database with backups, sessions not held in local process memory, assets on object storage. A box you can lose is a box you can also resize, migrate, and rebuild cheaply.

---

**Write it down.** A recurring task that is agreed — reboot window, snapshot pruning, weekly check, restore drill — becomes a row in `## Due` in `~/Clawic/data/vps/memory.md` with its cadence, last run, and next due date, updated the moment it runs. A recurring problem that shapes future advice (a workload that OOMs monthly, a location with chronic steal) goes in `## Pain Points`. A change that alters what a host is — disk grown, swap added, volume attached — goes in `## Hosts` and in `changes/<year>.md`, with `Reversible?` filled in honestly.
