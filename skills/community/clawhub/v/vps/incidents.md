# The Box Is Down — Splitting Provider From Machine

Read when a server is unreachable or misbehaving and nothing was deployed. The first question is never "what is broken on the box", it is **"is this mine at all"** — and answering it takes two minutes and saves hours.

**Before debugging**, check `## Boxes` in `~/Clawic/data/vps/memory.md` for a runbook naming this host and `## Pain Points` for a recurring cause; a box with a history usually has the same history again.

**Contents:** [Two Minutes of Triage](#two-minutes-of-triage) · [Provider-Side Causes](#provider-side-causes) · [Machine-Side Causes](#machine-side-causes) · [Your-Side Causes](#your-side-causes) · [Escalating to the Provider](#escalating-to-the-provider) · [Restore or Repair](#restore-or-repair) · [After It Is Over](#after-it-is-over)

## Two Minutes of Triage

In order. Each step splits the space in half.

1. **Provider status page and maintenance notices.** A location-wide event answers everything, and the answer is "wait" — checking it first prevents an hour of debugging your own configuration during someone else's outage.
2. **Does the address respond to anything?** Ping, then a port you know is open, from a network that is not yours.
3. **Does the provider console show the machine running?** A machine that is off, or stuck in a boot loop, is a completely different investigation from one that is up and not answering.
4. **Console in.** If the console gives a login prompt, the machine is alive and the problem is the network, the firewall, or a service (`access.md`).
5. **Check the four killers** (`operations.md`): disk, inodes, memory, steal. One of them explains most cases where the box is up and useless.
6. **Then** look at the application.

The single most useful habit: test from a second network before believing anything. A remarkable share of "the server is down" is a local network, a captive portal, or your own address having been banned (`access.md`).

## Provider-Side Causes

| Cause | How it presents | What to do |
|---|---|---|
| Node failure | Machine off or unreachable, console unavailable, status page silent at first | Open a ticket immediately; the provider usually migrates the instance to another node |
| Live migration | Brief unreachability or a spontaneous reboot, uptime reset, no logs explaining it | Nothing to fix; put the date in `changes/<year>.md`, it explains an unexplained reboot later |
| Scheduled maintenance | An email nobody read, then a reboot | Check the notices; put a monthly line in `## Due` to read them |
| Network event in the location | Whole location unreachable, other customers reporting the same | Wait; failover only if you already built it |
| Suspension | Console access to the account, no access to the machine, an email with a reason | `security.md` for abuse, `costs.md` for billing |
| Address change after a rebuild | Everything works, at an address nothing points to | Update DNS and the inventory |
| Storage backend degradation | Extreme IO wait, IO errors in the kernel log, filesystem remounted read-only | Provider ticket with the kernel log lines; do not just reboot and hope |

## Machine-Side Causes

| Cause | Distinguishing signal | Route |
|---|---|---|
| Disk full | Services fail to write, logins break, box still pings | `operations.md` |
| Filesystem remounted read-only | Everything fails to write at once, kernel log names it | Reboot and check the filesystem; if it recurs, the storage backend is suspect |
| Out of memory | A process is simply gone, the kernel log names it, no application error | `operations.md` |
| A service failed to start after a reboot | Works after manual start; not enabled at boot | Enable it, then ask why a reboot happened |
| Bad `/etc/fstab` after adding a volume | Boot stops entirely, console shows emergency mode | Rescue mode, `nofail` (`access.md`) |
| Failed or half-applied upgrade | Broken dependencies, a service that will not start | Snapshot, then repair from the console; rebuild if it is quicker (Rule 7) |
| Clock badly wrong | Certificate validation failures, authentication failures, nothing else obviously wrong | Time sync (`provisioning.md`) |
| Compromise | Unexplained load, unexplained traffic, unfamiliar processes | Stop and go to `security.md` — do not reboot |
| Certificate expired | Browser error, no server-side failure at all | Renewal mechanism; add expiry to the weekly check |

## Your-Side Causes

Worth eliminating early because they are free to check and embarrassing to miss:

- Your address is banned by the intrusion-prevention tool (`access.md`).
- Your network blocks the nonstandard SSH port.
- DNS caching on your machine still points at the old address after a migration.
- The domain expired, or the DNS host is the thing that is down — the server is perfectly fine and unreachable by name. Check the domain's expiry in `~/Clawic/data/domains/domains.md`.
- A stale host key entry after a rebuild, refusing the connection with a security warning.

## Escalating to the Provider

- **Open the ticket early.** It costs nothing and the queue is the long part. You can close it if you find the cause.
- Include what makes a ticket actionable: the instance identifier, the timestamps with timezone, exactly what you observe from outside, what the console shows, and the relevant kernel or system log lines. "It is down" produces a request for these and loses an hour.
- State clearly whether the machine is production and whether data is at risk. Providers do triage.
- **Ask for the specific action** you believe is needed — migrate the instance to another node, check the storage backend, confirm a network event — rather than asking them to investigate in general.
- If the machine is unreachable but its disk is intact, ask about rescue mode before asking about anything destructive.

## Restore or Repair

The decision to make explicitly rather than by drifting into one:

- **Repair** when the cause is understood, the fix is bounded, and the data is intact. Time-box it: if the box is not back within the recovery time your last drill measured, stop and restore.
- **Restore or rebuild** when the cause is unclear, when the machine is a rebuild-from-file box (Rule 7), or when a compromise is possible (Rule 6). Restoring to a **new** machine keeps the broken one available for diagnosis.
- **Always snapshot before either.** One click, and it is the only copy of the evidence.
- Announce the recovery estimate from the measured drill number, not from optimism (`backups.md`).

## After It Is Over

Write it up while it is fresh, and keep it short enough that it gets written:

- What was observed, and when — with timestamps.
- What it actually was, and how it was established.
- What was done, in order, including what did not work.
- What would have made it faster: a fallback that did not exist, an alert that was missing, a runbook that was wrong.
- One change to make now. Not five; the five never happen.

Recurring causes deserve a permanent home: an incident that happens twice is a `## Pain Points` entry, and its handling procedure is a runbook in `artifacts/`, not something to rediscover.

---

**Write it down.** Every incident that took longer than a few minutes becomes `~/Clawic/data/vps/artifacts/incident-<yyyy-mm>-<host>.md` with the timeline, the cause, and the one change — plus its `## Boxes` line with the read condition, so the next occurrence starts from the answer. Anything done to the machine goes in `~/Clawic/data/vps/changes/<year>.md`; a recurring pattern goes in `## Pain Points`; a fallback path that was missing goes in `## Hosts` so it is fixed before the next change. If the cause was a provider property (chronic steal, a location with repeated events), it belongs in that provider's row in `## Provider Accounts`, because it is an input to the next provider decision (`choosing.md`).
