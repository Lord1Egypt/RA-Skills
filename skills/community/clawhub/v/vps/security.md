# Security — Exposure, Intrusion, and the Abuse Notice

Read when hardening a public box, when the provider sends an abuse notice or suspends the server, and when there is any reason to suspect an intruder. Access mechanics are in `access.md`, filtering is in `firewall.md`; this file covers what is exposed, how it goes wrong, and what to do afterwards.

**Before an audit or an incident**, read `## Exposure` and `## Hosts` in `~/Clawic/data/vps/memory.md`, and check `## Boxes` for a hardening baseline or a previous incident write-up on this host.

**Contents:** [Threat Model in Three Lines](#threat-model-in-three-lines) · [The Provider Account Is the Real Root](#the-provider-account-is-the-real-root) · [Baseline](#baseline) · [What Gets Compromised, In Order](#what-gets-compromised-in-order) · [Signs of Compromise](#signs-of-compromise) · [Compromise Response](#compromise-response) · [The Abuse Notice](#the-abuse-notice) · [Suspension](#suspension) · [Intrusion Prevention Tools](#intrusion-prevention-tools) · [Patch Discipline](#patch-discipline) · [Audit Checklist](#audit-checklist)

## Threat Model in Three Lines

- **Nobody is targeting you; everybody is scanning you.** A new address receives credential attempts within minutes of first responding. The attacker is a script with a list of default passwords and last year's vulnerabilities.
- **The three ways in, in order of real-world frequency**: a weak or reused credential on an exposed service; an unpatched public-facing application; a data store exposed with no authentication because a container published its port.
- **The goal is almost never your data.** It is your bandwidth and your CPU: spam, scanning, proxying, mining. Which is why the provider notices before you do.

## The Provider Account Is the Real Root

SKILL.md Rule 2, in operational terms. Nothing on the box defends against this, so it goes first:

- 2FA on the provider login, with recovery codes stored offline and outside the same password manager session.
- The account email is part of the perimeter: whoever can reset that mailbox can reset the provider account.
- API tokens scoped to the smallest capability that works, one per purpose, rotated when anyone with access leaves. Store the pointer only (`keychain:<entry>`).
- Team members get their own provider logins with the least role that works, never a shared one.
- A leaked API token is equivalent to root on every server in the account, plus the ability to delete every snapshot. Treat its exposure as a full compromise of the fleet, not of one box.

## Baseline

Non-negotiables for a public server. Anything unchecked here outranks feature work.

| Check | Passing looks like |
|---|---|
| Provider account | 2FA on, tokens scoped, recovery codes offline |
| SSH | Key-only, root login off, password auth off, verified from outside |
| Inbound | Default-deny at both layers; only 80/443 and a restricted SSH source open (`firewall.md`) |
| Data stores | Bound to localhost or the private interface, with authentication on regardless |
| Updates | Automatic security updates on, and a stated reboot policy that is actually followed |
| Users | One account per human, no shared logins, no passwordless sudo unless the user asked for it |
| Backups | 3-2-1 with one copy outside the provider account, restore timed (`backups.md`) |
| Exposure verified | Scanned from another machine, both IPv4 and IPv6, results in `## Exposure` |
| Secrets on disk | Application secrets in a file readable only by its service user, never in the repository, never in a world-readable `.env` |
| Logs | Retained long enough to investigate — a compromise found on day 20 with 7 days of logs cannot be understood |

## What Gets Compromised, In Order

1. **An exposed data store with no password.** Container-published port, default configuration, no authentication. Minutes to discovery.
2. **A public application with a known vulnerability.** A content management system, a forum, an admin panel, a monitoring dashboard, all unpatched.
3. **A weak credential on an exposed service.** SSH with passwords enabled, a database with a guessable password, a control panel.
4. **A supply-chain path** — a dependency, a plugin, a Docker image pulled from an untrusted namespace.
5. **A leaked key or token** — committed to a repository, pasted into a chat, left in a backup that was itself exposed.

The list is also the audit order. Items 1 to 3 are the overwhelming majority.

## Signs of Compromise

| Signal | Why it means what it means |
|---|---|
| Provider abuse notice or a bandwidth spike with flat traffic | The box is sending: spam, scans, or a proxy. This is how most owners find out |
| CPU pinned with no matching workload | Mining. Often hidden behind a process name that mimics a kernel thread |
| Unknown entries in `authorized_keys`, or a new sudo-capable user | Persistence installed |
| Cron, systemd timer, or unit file you did not create | Persistence, usually re-installing the payload after every cleanup |
| A binary in a temporary directory that is running | Almost always malicious; nothing legitimate does this |
| Outbound connections to addresses nothing should be talking to | Command and control, or exfiltration |
| Log files truncated, or a gap in a log's timeline | Someone tidied up. Absence of evidence is evidence here |
| Package manager reports a modified system binary | Rootkit — stop and go to the response below |

## Compromise Response

Ordered. Steps 1 and 2 are simultaneous if possible, and step 3 is the one people skip.

1. **Isolate at the provider layer**, not from inside the box. Deny all traffic in the provider firewall, or detach the network. An intruder with root can undo anything you do on the machine, including your firewall change.
2. **Do not reboot and do not clean up.** A reboot destroys volatile evidence, and cleanup destroys the timeline you need to know what was taken.
3. **Snapshot the disk for forensics before anything else.** It is cheap, it is one click, and it is the only chance to answer "what did they get" later. Keep it until the question is settled.
4. **Establish the entry point** from logs — authentication logs, web access logs, the application's own logs — and the time window. Without this you will re-open the same door on the new box.
5. **Rebuild from a fresh image** (Rule 6). Restore *data*, never binaries or configuration files, from a backup that predates the intrusion. A backup taken after the entry point may contain the persistence.
6. **Rotate everything the box could see**: every credential in its environment, database passwords, API tokens, any key stored on it, and any provider token it used. Assume all of it was read.
7. **Notify** if user data was on the box. Jurisdictional obligations attach to the discovery, and the clock started at discovery, not at the intrusion.
8. **Write the incident up** while the details are fresh.

## The Abuse Notice

An automated report from the provider that your address originated spam, scanning, or attack traffic. It has a deadline, typically measured in hours, and ignoring it leads to suspension.

- **Treat it as confirmed compromise** until proven otherwise. The provider is reporting observed traffic; your box was the source.
- **Reply inside the window even if you have not finished.** A holding reply that names what you are doing keeps the server online; silence does not.
- **Say what you found, what you did, and what prevents recurrence.** The provider's abuse team wants to close the ticket, not to argue.
- **The false-positive case exists** — a mail relay with a bad sender, a monitoring tool that looks like a scanner, a shared address whose previous tenant is the real subject. Verify before claiming it: check what your box actually sent in the reported window.
- Repeated notices from the same account end in account-level action, which is far worse than one suspended server (Rule 2).

## Suspension

- Access is usually cut but the disk is intact, and a rescue or recovery mode is normally still available so you can extract data and evidence.
- Get the data out before negotiating. Restoration timelines are not under your control.
- Rebuild elsewhere if the workload matters and the timeline is unclear; a suspended server is not a hosting strategy.
- Cause matters for the future: abuse means compromise, non-payment means billing (`costs.md`), and a policy violation means the workload may not be welcome on that provider at all.

## Intrusion Prevention Tools

- **Automated banning of repeated failures** (fail2ban and equivalents) is worth installing: it removes the log noise and stops the cheapest attacks. It stops zero targeted attacks, and it will eventually ban you (`access.md`).
- **A host intrusion-detection agent** that alerts on changed system binaries and new persistence is the highest-value optional addition, and only if someone reads the alerts. An unread alert stream is a cost with no benefit.
- **A web application firewall** in front of a public application catches opportunistic exploitation of known vulnerabilities. Patching is still the fix; this buys the days between disclosure and your maintenance window.
- **Rootkit scanners** produce false positives on a normal server and are not a substitute for rebuild-on-compromise. Useful as one signal, never as an all-clear.
- **Mandatory access control** (SELinux, AppArmor) is on by default on several distributions. Leave it on and learn to read its denials; disabling it because a denial was confusing removes a real containment layer.

## Patch Discipline

- Automatic **security** updates on, always. The failure mode is not a bad patch, it is a box that has not been updated in a year.
- Unattended upgrades do not restart what they patched, and never reboot for a kernel. A box showing "up to date" while running last year's kernel and yesterday's library in memory is the standard false sense of safety (`operations.md`).
- Full distribution upgrades are a maintenance event with a snapshot beforehand, not an automatic process.
- Applications you installed outside the package manager have no automatic path at all. They are the ones in the vulnerability list — keep their names and versions in the host's row in `## Hosts`, or accept that they will be your entry point.

## Audit Checklist

| Check | What tells you |
|---|---|
| Ports open from outside, IPv4 and IPv6 | A scan from another machine, not the local ruleset |
| Listening sockets on the box | Everything bound to a public address, with a reason for each |
| Users with a shell and users with sudo | Anyone unexpected, anyone who left the team |
| `authorized_keys` on every account | Keys nobody can identify |
| Cron jobs, timers, and enabled units | Persistence, and jobs left over from an experiment |
| Packages with known vulnerabilities pending | Whether the automatic updates are actually running |
| Reboot required marker | Kernel and library updates installed but not active |
| Failed authentication volume and ban list | Whether an attack is ongoing, and whether you are about to ban yourself |
| Provider account roles, tokens, and 2FA | Rule 2, the layer no host check covers |
| Backup restore timed within the quarter | An untested backup is not a control |

---

**Write it down.** An exposure sweep updates `## Exposure` in `~/Clawic/data/vps/memory.md`; anything it turned up that is not already inventoried goes to `~/Clawic/data/servers/servers.md` and `## Hosts`. A hardening baseline agreed with the user becomes `~/Clawic/data/vps/artifacts/hardening-baseline.md`. Any incident — abuse notice, suspension, or confirmed compromise — becomes `~/Clawic/data/vps/artifacts/incident-<yyyy-mm>-<host>.md` with the timeline, the entry point, what was rotated, and what changed afterwards, plus a line in `changes/<year>.md` for the rebuild. Add every `## Boxes` line in the same turn, and strip every credential from anything the user pastes in before it is written.
