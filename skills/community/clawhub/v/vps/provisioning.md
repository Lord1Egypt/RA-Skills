# Provisioning — First Boot to Something You Would Trust

Read before creating a server, and when a box exists but nobody can say what was done to it. The ordered list in SKILL.md is the summary; this is the reasoning, the automation, and the parts people skip.

**Before creating anything**, read `~/Clawic/data/servers/servers.md` and `## Hosts` in `memory.md`: naming, region, private-network plan, and snapshot policy should match the fleet that already exists, and `config.yaml` may already declare the distro, architecture, admin username, and SSH port.

**Contents:** [Create It Right](#create-it-right) · [Cloud-Init Is the Whole Point](#cloud-init-is-the-whole-point) · [Distribution Choice](#distribution-choice) · [The Irreversible Decisions](#the-irreversible-decisions) · [Swap and Memory Floor](#swap-and-memory-floor) · [Time, Locale, Hostname](#time-locale-hostname) · [Automatic Updates](#automatic-updates) · [Baseline Verification](#baseline-verification) · [Rebuilding Instead of Repairing](#rebuilding-instead-of-repairing)

## Create It Right

Decisions made in the creation dialog that are painful or impossible to change later:

| Decision | Why it is hard to change | Default |
|---|---|---|
| SSH key injected at creation | A root password sent by email travels through mail and lives in an inbox forever | Always inject the key; never accept the emailed password path |
| Region | Data has to be moved to change it, and private networking is location-scoped | Nearest to users; same location as the rest of the fleet |
| Disk size | Growth is one-way; shrinking is a migration | One step below the guess (Rule 5) |
| Architecture | Changing means a rebuild and a full compatibility pass | Follow `cpu_arch`; run the dependency check first |
| Private network / VPC | Attaching later is possible but re-addressing is disruptive | Attach at creation if there will ever be a second box |
| Hostname | Trivial to change, but it propagates into certificates, logs, monitoring, and PTR | Follow the declared scheme; decide it before creation |
| IPv6 | Free almost everywhere and increasingly expected | Enable |

## Cloud-Init Is the Whole Point

Every mainstream provider accepts user-data at creation. This converts Rule 7 from an aspiration into the default path.

A first-boot configuration worth having covers: the admin user and its authorized key, sudo without password only if the user asked for it, package update, the handful of packages the box always needs, swap, timezone, the host firewall with the SSH port allowed *before* enabling, sshd hardening, and automatic security updates. That is the whole First Hour, executed before you first log in.

- **Keep it in the project repository, not in the provider's web form.** The form is a copy; the repo is the source. A configuration that only exists in a console text box is lost with the account.
- **Version it.** Note the version used in `changes/<year>.md` when a host is created, so "why is this box different" has an answer.
- Cloud-init runs once. Changing it does not change existing servers — that is Ansible's job, or a rebuild.
- **Failures are silent from the outside.** The box boots either way. Verify the result rather than assuming it; the baseline check below is exactly that verification.
- If the provider does not support user-data, a single idempotent shell script in the repo achieves the same thing at the cost of one manual step.

## Distribution Choice

- **Debian stable** — the default for a server you want to think about rarely: long support, conservative updates, small base. Its "old" package versions are the point, not a defect; the application's own dependencies come from the language runtime or a container, not from the OS.
- **Ubuntu LTS** — the same bargain with newer packages and the largest volume of third-party instructions written against it. Correct when a vendor's install docs assume it.
- **Rocky / Alma** — when compliance, a vendor certification, or existing muscle memory says RHEL-family. SELinux is enforcing by default, which is a feature and a source of confusing permission denials.
- **Alpine** — small and fast, and the musl libc breaks a real fraction of prebuilt binaries. Fine as a container base, avoid as the host OS unless the user knows exactly why they want it.
- **Rolling distributions** — a server that changes underneath you on every update. Not for something you are on call for.
- **Distro version at creation matters**: installing the previous release means an in-place major upgrade sooner. Take the current stable release unless a dependency forbids it.

## The Irreversible Decisions

Flag these *before* the step, never after:

- **Disk growth.** One-way at every provider.
- **Architecture.** Changing means recreating the machine.
- **The hostname baked into a certificate.** Reissuing is cheap; discovering the mismatch during a cutover is not.
- **Filesystem layout.** A separate volume for data is easy at creation and awkward later; it is also what lets you resize storage without touching the machine (`resizing.md`).
- **Encryption at rest.** If the threat model calls for it, it is a creation-time decision — retrofitting means a full data move.

## Swap and Memory Floor

- Enable swap on anything under 4 GB. Without it, a single memory spike during a deploy or a build causes the kernel to kill the largest process, which is usually the database and not the cause.
- Swap is not extra RAM; it is a shock absorber. A box that swaps continuously is undersized (`resizing.md`).
- `vm.swappiness` around 10 on a server: use swap under pressure, do not page out a working set opportunistically.
- On tiny boxes, compressed RAM (zram) gives a similar cushion without disk IO, and can coexist with a small disk swap file.
- Size a swap file at roughly the size of RAM up to about 4 GB; more than that on a small VPS just consumes the disk you cannot shrink.

## Time, Locale, Hostname

- **UTC unless the user declared otherwise.** Every log correlation across hosts, and every conversation with a provider's support, is easier in UTC. If the user wants local time, that is a declared preference, recorded in `config.yaml`.
- Time synchronization is on by default in modern distributions; verify it rather than installing a second daemon. Two time daemons fighting is a real and confusing failure.
- Set the hostname in both the system and the hosts file; a mismatch produces sudo delays and mail-related warnings that look like network problems.
- Locale unset produces warnings from half the tooling. Set it once at provisioning.

## Baseline Verification

Run this after cloud-init and before the box carries anything real. Each check exists because it silently fails in a way you would not notice for weeks:

| Check | Passing looks like |
|---|---|
| Second session works | A new SSH session as the admin user, key-only, on the configured port |
| Fallback proven | The provider console opens and accepts a login (Rule 1) |
| Root SSH and password auth disabled | The daemon rejects both, verified from outside, not read from the config file |
| Host firewall active, default-deny inbound | Ruleset shows the policy and the SSH allow, in that order |
| Provider firewall active | Same policy one layer out (`firewall.md`) |
| Nothing unexpected listening | The listening-socket list contains only what you put there — a stock image occasionally ships an enabled service you did not ask for |
| Swap present | Present and sized as intended |
| Automatic security updates enabled | The timer exists and has run, not merely that the package is installed |
| Time synchronized | Clock is in sync and the source is a single daemon |
| Backups configured, one restore tested | A restore has completed once, with the time noted (`backups.md`) |

## Rebuilding Instead of Repairing

A provisioned-from-file box changes what "broken" means. When something is deeply wrong — an upgrade half-applied, a configuration nobody can explain, a suspected compromise — the cheapest path is often: snapshot for forensics, create a replacement from the same user-data, restore data, move the address or the DNS record, destroy the old one.

The gate is your own measure from Rule 7: if a rebuild takes under 30 minutes, rebuild. If it takes longer, the box is a pet — fix it this time, and spend the next hour making the rebuild cheap, because Rule 6 will eventually require it whether or not you are ready.

---

**Write it down.** A newly created host gets, in the same turn: its row in `~/Clawic/data/servers/servers.md` (`Name` + `Provider` identity, monthly cost with currency, access reference as a pointer), its VPS-only attributes in `## Hosts` in `memory.md` (image, snapshot policy, private address, what it serves), and a line in `~/Clawic/data/vps/changes/<year>.md` recording the creation and the user-data version used. If the box will be reachable by a domain, its row also goes to `~/Clawic/data/domains/domains.md`. Ports opened during provisioning go to `## Exposure`.
