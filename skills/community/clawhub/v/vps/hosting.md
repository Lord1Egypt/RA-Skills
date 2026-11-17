# What Runs On It — Layout, Isolation, and Multiple Sites

Read when deciding how to organise what lives on a server: one project or several, containers or system services, panel or no panel, and how deploys happen. The configuration of the individual pieces belongs to their own skills; this file is the layout decision and the parts that are specific to a rented box.

**Before proposing a layout**, read `## Hosts` in `~/Clawic/data/vps/memory.md` for what each machine already serves and the declared `isolation_model` in `config.yaml`: a fleet with a consistent shape is worth more than a locally optimal new box.

**Contents:** [The Layout Decision](#the-layout-decision) · [Several Sites on One Box](#several-sites-on-one-box) · [Containers or System Services](#containers-or-system-services) · [Control Panels](#control-panels) · [Where Things Live on Disk](#where-things-live-on-disk) · [Deploys Without a Pipeline](#deploys-without-a-pipeline) · [TLS](#tls) · [Isolating Tenants and Clients](#isolating-tenants-and-clients) · [What Does Not Belong on This Box](#what-does-not-belong-on-this-box)

## The Layout Decision

Four shapes, in ascending order of complexity. Pick the simplest that satisfies a real constraint:

| Shape | Correct when | Cost |
|---|---|---|
| One service, one box | The service matters, or it is the only thing you have | One plan price per service |
| Several projects on one box behind a reverse proxy | Personal projects, low-stakes sites, staging | One project's runaway process affects all of them |
| One box per client or per environment | Different owners, different uptime expectations, billing separation | Per-box overhead: address, backup, patching, attention |
| Application box plus data box | The database deserves its own sizing and failure domain (`resizing.md`) | Network latency between them, two machines to operate |

The forcing question is not "will it fit" — it usually will — but **"what happens when one of these needs a reboot, or is compromised?"** Everything on the box shares that answer.

## Several Sites on One Box

- A single reverse proxy terminating TLS and routing by hostname is the standard shape: one address, many domains, one place where certificates are managed.
- Each application listens only on localhost. Nothing else has a public port (`firewall.md`).
- **Give each application its own system user.** Shared users mean one compromised application reads every other application's secrets and database credentials — the cheapest isolation available and the most commonly skipped.
- Per-service resource limits through the service manager, so one runaway process cannot take the box down with it (`operations.md`).
- Separate log files or units per site, or debugging any of them becomes archaeology.
- The realistic ceiling is memory, not the number of sites. A handful of small dynamic sites plus a shared database fits comfortably on a modest box; each additional application runtime is the cost.

## Containers or System Services

| | Containers | System services |
|---|---|---|
| Dependency isolation | Strong — each app carries its own | Shared system libraries, which occasionally conflict |
| Reproducibility | The image is the artifact; Rule 7 nearly free | Depends on the provisioning file being honest |
| Firewall interaction | The runtime writes rules ahead of the host firewall (`firewall.md`) | Straightforward |
| Disk consumption | Images, layers, and volumes grow silently and fill disks | Predictable |
| Memory overhead | Small per container, real when there are twenty | None |
| Debugging | One layer between you and the process | Direct |
| Correct when | Multiple apps, unfamiliar stacks, an existing image-based workflow | A single well-understood service on a small box |

Both are legitimate. The container-specific rules that matter on a rented box: publish ports to localhost only, prune images on a cadence in `## Due`, set memory limits per container, and never assume the host firewall protects a published port.

## Control Panels

- A panel gives a non-specialist a working path to routine hosting tasks — sites, mailboxes, certificates, databases — and that is a genuine benefit for the person who will not read a log file.
- The costs are structural: a large privileged attack surface that is itself a public application, an expectation of owning the machine's configuration, and a strong tendency to fight anything you automate.
- **Panel and configuration management do not coexist.** Choose one. A box where both edit the reverse proxy configuration is a box where changes vanish.
- If a panel is used, it is the highest-value patch target on the machine and its admin interface should not be publicly reachable — restrict it by source or put it behind the VPN (`networking.md`).
- Lightweight deployment tooling is a middle ground: it gives a friendly path to deploying applications without claiming ownership of the entire host.

## Where Things Live on Disk

Conventions matter mostly for being consistent across the fleet, which is what makes a runbook portable:

- One directory root for project data, with a directory per project. Declared in `config.yaml` under conventions so every box matches.
- **Application data on a separate volume where it will grow** — it makes storage resizable and survives a rebuild (`resizing.md`).
- Nothing important in a home directory: home directories are personal, and personal directories disappear when a person is offboarded.
- Secrets in a file readable only by the service user, referenced by the service manager, never in the repository and never world-readable. This skill records the pointer only.
- Anything hand-edited outside the provisioning file is a future restore failure — either put it in the file or make sure it is backed up (`backups.md`).

## Deploys Without a Pipeline

The realistic path on a single VPS, and it is fine:

- **Pull, do not push.** The server fetches from the repository or the registry; the developer's machine does not need credentials to the server beyond SSH.
- **A deploy is a script on the server**, committed to the repository: fetch, build or pull, run migrations, restart, health check. Written once, it removes the entire class of "what did I run last time".
- **Health-check before declaring success**, and keep the previous artifact so rollback is a restart rather than a rebuild.
- Zero downtime on a single box is achievable with a socket handover or a brief proxy-level drain, and for most workloads a two-second gap during a deploy at a quiet hour costs less than the machinery to avoid it.
- Migrations are the risky step: expand-contract, applied once, with a snapshot before anything irreversible.
- The deploy user should not be root, and should be able to restart only its own service.

## TLS

The VPS-side facts; certificate and proxy configuration belong to the `nginx` skill.

- Automatic issuance and renewal is standard and free. The only real decisions are which validation method and where renewal runs.
- **HTTP validation needs port 80 reachable**, which means both firewall layers must allow it — including during a migration, before traffic has moved.
- **DNS validation** is the answer for wildcards and for hosts with no public HTTP, and it needs an API credential for the DNS provider, stored in the user's secret store with only a pointer recorded here.
- **Certificate expiry is a scheduled outage you agreed to.** Renewal failures are silent: the renewal timer failed weeks ago, and nothing said anything. Monitor the expiry date externally (`operations.md`), not the renewal job.
- After a migration, verify the certificate on the new host *before* moving DNS (`migration.md`).

## Isolating Tenants and Clients

When the box serves someone else's work, the bar rises:

- One system user per client, and preferably one box per client where the budget allows. A shared box means one client's compromise is every client's incident, and that conversation is unpleasant in proportion to the number of clients.
- Separate database users and separate databases, never a shared account with access to everything.
- Backups per client, restorable independently — the request "restore just our data from Tuesday" arrives eventually.
- Agree what happens on offboarding before onboarding: data export format, deletion timeline, who owns the domain and the DNS.
- The client themselves is a person: their record belongs in `~/Clawic/data/contacts/contacts.md`, and infrastructure boxes reference them **by name only**, never duplicating the record.

## What Does Not Belong on This Box

- **Anything that must not go down when this box goes down**, including the monitoring that watches it and the DNS that points at it.
- **Your backups**, unless they are also somewhere else (`backups.md`).
- **A mail server**, unless mail is the product (`email.md`).
- **An observability stack** that consumes more memory than the application it observes, on a single-server setup.
- **Secrets for other systems** beyond what this machine needs. Every credential on the box is a credential in the blast radius (`security.md`).
- **The only copy of anything.** Ever.

---

**Write it down.** What each host serves — applications, domains, isolation model, per-service users, where data lives — goes in `## Hosts` in `~/Clawic/data/vps/memory.md`, keyed by the same `Name` as `~/Clawic/data/servers/servers.md`. Every domain the box serves goes to the shared `~/Clawic/data/domains/domains.md` pointing at the host by name. Ports the layout requires go to `## Exposure`. A layout decision that took real thought — one box or several, containers or not, panel or not — becomes `~/Clawic/data/vps/artifacts/architecture-<scope>.md` with what was chosen, what was rejected, and what would trigger a revisit, with its `## Boxes` line added in the same turn. Clients are referenced by name; their record lives in `contacts/`.
