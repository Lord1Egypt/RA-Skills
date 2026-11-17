# Self-Hosting Other People's Software

Running packaged applications you did not write: media servers, file sync, dashboards, game servers. The failure modes are different from your own app — the code is fixed, so every problem is placement, permissions, data, or the reverse proxy.

**Before adding a service**, read `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there) for the ports in use and the box's memory budget, and `~/Clawic/data/domains/domains.md` for a free hostname. Half the pain of a self-hosted box is two services silently competing for the same port, path, or gigabyte.

**Contents:** [Decide Before Installing](#decide-before-installing) · [Subdomain, Not Subpath](#subdomain-not-subpath) · [The Data Directory Is the Application](#the-data-directory-is-the-application) · [Media Servers](#media-servers) · [File Sync and Documents](#file-sync-and-documents) · [Photos](#photos) · [Password and Secret Managers](#password-and-secret-managers) · [Home Automation](#home-automation) · [Git, CI, and Dev Tools](#git-ci-and-dev-tools) · [Game Servers](#game-servers) · [Remote Access Without Exposing Anything](#remote-access-without-exposing-anything) · [Single Sign-On in Front](#single-sign-on-in-front) · [Upgrades Break Differently Here](#upgrades-break-differently-here) · [Write It Down](#write-it-down)

## Decide Before Installing

Four questions, answered before the first `up -d`, because each one is expensive to change later:

1. **Where does its data live, and is that path backed up?** Almost every self-hosted app is a database plus a directory. Decide the host path now (`/srv/<app>/data`), not whatever the tutorial's volume was called.
2. **Is it exposed to the internet, or reachable only over a VPN?** Anything with a weak admin surface should never have a public hostname (below).
3. **How much memory does it want at rest?** Photo and media indexers, search, and anything with an embedded database are the reason small boxes swap. Sum the resting footprints against the box before adding the fourth service.
4. **Who upgrades it, and how often?** Self-hosted software with a public interface and no upgrade cadence becomes an incident on someone else's schedule.

## Subdomain, Not Subpath

Give each app its own hostname (`photos.example.com`), not a path on a shared one (`example.com/photos`). Subpath hosting requires the app to support a base-path setting, and rewrite its own asset URLs, cookies, redirects and WebSocket paths to match. Many do not, and the failure is partial: the login page renders, the app loads, and one feature silently 404s.

When a subpath is forced, the app must be *told* its base path (`--root-path`, `BASE_URL`, `SCRIPT_NAME`, `subfolder`), never just have the proxy strip the prefix (`proxy.md`).

Wildcard DNS (`*.example.com` → the box) makes adding a service one proxy block and no DNS change; pair it with a wildcard certificate or per-host issuance (`tls.md`).

## The Data Directory Is the Application

- Bind-mount to a path you chose, so backups are `tar` of a directory you can name rather than a volume you have to look up (`containers.md`).
- Config, database and user content are often three separate directories. Backing up one of the three is the most common self-hosting data loss, and it is discovered at restore time.
- **Databases are not backed up by copying their files while running.** Use the app's own export, or a database dump, or stop the container first. A file-level copy of a live database restores as corruption.
- `PUID`/`PGID` environment variables exist on most self-hosted images precisely because bind-mount ownership is the recurring problem. Set them to the host user that owns the directory.
- Media libraries are large and not re-downloadable in practice: they need a different backup strategy (and cadence) than a 200 MB config directory. Say which is which when you set it up.

## Media Servers

| Point | Detail |
|---|---|
| Jellyfin vs Plex vs Emby | Jellyfin is fully self-hosted with no account dependency; Plex has the better client ecosystem and a remote-access service that depends on their servers; Emby sits between. The dependency, not the feature list, is the decision |
| Hardware transcoding | The single biggest capacity factor. Without it, one 4K transcode saturates several CPU cores; with a passed-through GPU or QuickSync device it is nearly free. Direct play (no transcode) beats both — match client codecs and the problem disappears |
| Host networking | Media servers use discovery protocols (DLNA, client auto-discovery) that need broadcast traffic. `network_mode: host` is the usual answer, and it means the container's ports are the host's ports |
| Storage layout | Keep the library on its own mount; a media directory that fills the root filesystem takes the whole box down (`logs.md`) |
| Remote access | Prefer a VPN. If exposing, put it behind the proxy with HTTPS, and never expose the admin/setup wizard during initial setup — that is the window where it has no password |
| Streaming through a proxy | Long-lived responses and range requests: `proxy_buffering off` for the streaming route, a generous read timeout, and range support intact (`static.md`) |

## File Sync and Documents

- **Nextcloud** is a PHP application: its capacity is `pm.max_children` and its speed is the database plus the file backend (`workers.md`). It needs a large `client_max_body_size` and a matching `upload_max_filesize`/`post_max_size` for uploads to work at all (`static.md`), plus background jobs on a real schedule (cron, not "AJAX") or half its features quietly stop.
- Its `trusted_domains` list must contain the public hostname or you get a blank page with a warning — the first thing to check after putting it behind a proxy.
- **Syncthing** is peer-to-peer with no server component: no proxy needed for sync (it needs its own ports open, TCP and UDP for discovery), only for the admin UI, which should be loopback-only or VPN-only.
- Sync conflicts are the operational reality of both: know where the conflict copies land before a user asks.

## Photos

Photo managers (Immich and similar) are the heaviest common self-hosted workload: machine-learning indexing at import, a database, thumbnail generation, and originals you cannot re-download.

- Budget memory for the indexer separately from the web service; the ML component can be several gigabytes on its own and is often a separate container that can be limited or disabled.
- Uploads are large and slow from phones: the whole upload path (proxy body limit, timeouts, disk) must be sized for it, and resumable upload support in the client matters more than throughput.
- Originals and derivatives are different backup classes: derivatives can be regenerated, originals cannot. Back up originals off-box, always.

## Password and Secret Managers

Different risk class from everything else on the box, and the rules are stricter:

- Never on the public internet without a second factor in front of the login page, and preferably not on the public internet at all.
- Its data directory is the most valuable thing on the machine: encrypted at rest by the app, backed up off-box, and the backup itself is a target.
- Admin registration disabled after the first account (`SIGNUPS_ALLOWED=false` and equivalents) — an open registration endpoint on a vault is a vault someone else joins.
- Restore is tested, not assumed. A vault backup that cannot be restored is worse than none, because it is trusted.

## Home Automation

- Wants the local network: discovery protocols, mDNS, and often a USB radio dongle passed through to the container. `network_mode: host` plus a device mapping is the common shape.
- It is an availability-critical service in a house: a hub that restarts during an upgrade turns off the lights. Schedule upgrades, keep the previous image digest, and know which automations are safety-relevant.
- Never expose the interface directly; a VPN or an authenticating proxy in front, always. It controls physical things.
- Related device inventory (models, network names, locations) belongs in the shared `~/Clawic/data/devices/` box, not here — this skill records the *service*, not the hardware it talks to.

## Git, CI, and Dev Tools

- Self-hosted git (Forgejo, Gitea, GitLab) needs SSH as well as HTTPS: either a second host port for SSH or the proxy's stream module for TCP passthrough, and the app's advertised clone URL must match whichever you chose or every copied clone command is wrong.
- CI runners execute arbitrary code by design. Never on the same box as anything valuable, never with the container socket mounted, and with a disk they are allowed to fill.
- GitLab's resting memory footprint is in gigabytes; Forgejo and Gitea are in hundreds of megabytes. On a small box this is the entire decision.
- Registry storage grows without limit unless a retention policy exists — and it is a disk-full outage that arrives with no warning.

## Game Servers

- **UDP, and lots of it.** Port mapping must specify the protocol (`27015:27015/udp`); a TCP-only mapping produces a server that appears in no browser and accepts no players.
- Query and RCON ports are separate from the game port and each has different exposure: the query port is public by design, RCON must never be.
- `network_mode: host` for anything using LAN discovery or a wide dynamic port range; a fifty-port mapping list is a sign the container should be on host networking.
- One systemd template unit or one compose service per world/instance, so restarting one does not disconnect the others (`processes.md`).
- Save data is the whole asset: scheduled backups *and* a pre-update backup, because a version upgrade can be one-way for world data.
- Memory is the usual limit and it grows with world size and player count; these are the workloads most likely to be OOM-killed on a shared box, so give them an explicit limit rather than letting the kernel choose a victim (`containers.md`).

## Remote Access Without Exposing Anything

In order of preference:

1. **A mesh or WireGuard VPN** — nothing is published, admin interfaces stay on the private network, and phones connect transparently. Best default for anything personal.
2. **An authenticating reverse proxy** (forward-auth to an identity provider) — public hostname, but no request reaches the app unauthenticated.
3. **A tunnel from a provider** — no inbound ports at all, at the cost of a dependency that sees your traffic.
4. **Direct exposure with a strong app-level login** — acceptable for software designed for it (a media server for family, a public blog), never for an admin dashboard.

Port forwarding a database, a container dashboard, or a NAS management interface belongs to none of these categories: those are the services found and exploited within hours (`security.md`).

## Single Sign-On in Front

Putting one authentication layer in front of everything means each app's own weak login is no longer internet-reachable, and adding a service becomes a proxy block instead of a security decision. The cost is a new critical dependency: when the identity provider is down, nothing is reachable — including the tools you need to fix it. Keep one break-glass path (VPN plus direct access) that does not depend on it, and test that path before you need it.

Apps that manage their own sessions and do not understand forwarded identity end up with two logins in series. That is acceptable; silently trusting a header the app was not designed to receive is not.

## Upgrades Break Differently Here

You do not control the code, so the release notes are the whole risk assessment:

- Read them for a database migration or a breaking configuration change before pulling. Major-version jumps in self-hosted apps are frequently one-way.
- **Back up the data directory before an upgrade**, always, and know the previous image digest (`containers.md`).
- Do not skip major versions on anything that migrates its database: many projects only support sequential upgrades, and the failure appears after the migration has already run.
- Pin to a major-version tag rather than `latest`, so an unattended pull cannot cross a breaking boundary.
- The upgrade cadence goes in `## Due`; without one, the answer to "when did we last update it" is always "before the vulnerability" (`maintenance.md`).

## Write It Down

Every self-hosted app gets its `## Services` row: name, host, `compose <stack>` or unit, listen address, public hostname if any, restart policy, and **the data path** — that last column is what makes a restore possible (`memory-template.md`). Its hostname goes in the shared `~/Clawic/data/domains/domains.md`. Backup and upgrade cadences go in `## Due`. Hardware the service merely talks to is not this skill's data: if the user keeps a device inventory it lives in the shared `~/Clawic/data/devices/` box, and the `## Services` row names it in a note rather than duplicating it. The install decisions worth re-reading — why host networking, which PUID, what the pre-upgrade backup step is — go to `~/Clawic/data/server/artifacts/working-stack-<app>.md` with its `## Boxes` line the same turn, with every credential written as a pointer.
