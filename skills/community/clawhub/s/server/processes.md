# Process Supervision — Making It Survive Reboots, Crashes, and Logouts

Anything that must be running tomorrow is supervised today. This file is the unit file, the restart semantics, and the ways supervision quietly is not happening.

**Before writing a unit**, read `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there): the port, the user, and the naming convention for this box are already decided, and inventing a second convention is how two services end up fighting over 8000.

**Contents:** [The Minimum Unit](#the-minimum-unit) · [Type Is Not Cosmetic](#type-is-not-cosmetic) · [Restart Semantics and the Start Limit](#restart-semantics-and-the-start-limit) · [Ordering and Dependencies](#ordering-and-dependencies) · [Environment and Secrets](#environment-and-secrets) · [Limits the Unit Must Set](#limits-the-unit-must-set) · [Graceful Stop and Reload](#graceful-stop-and-reload) · [Socket Activation](#socket-activation) · [Timers Instead of Cron](#timers-instead-of-cron) · [Template Units for Many Instances](#template-units-for-many-instances) · [User Services](#user-services) · [PM2](#pm2) · [supervisord](#supervisord) · [When Supervision Is Not Happening](#when-supervision-is-not-happening) · [Write It Down](#write-it-down)

## The Minimum Unit

```ini
# /etc/systemd/system/api.service
[Unit]
Description=API service
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
User=api
Group=api
WorkingDirectory=/srv/api/current
ExecStart=/srv/api/current/bin/api
EnvironmentFile=/etc/api/env
Restart=on-failure
RestartSec=5
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

Apply: `systemctl daemon-reload`, then `systemctl enable --now api`. **`enable` is what makes it start at boot; `start` alone does not** — the most common way a service "randomly disappears" months later is that only `start` was ever run and the box finally rebooted. Verify with `systemctl is-enabled api`, never by assumption.

Validate before installing: `systemd-analyze verify /etc/systemd/system/api.service` catches typos in directive names that systemd otherwise ignores silently — an unknown directive is a warning in the journal, not an error, so a misspelled `Restart=on-faliure` means no restart at all and nothing tells you.

## Type Is Not Cosmetic

| Type | Considered started when | Use for |
|---|---|---|
| `simple` | The moment `ExecStart` is forked — before the app can serve anything | Nothing that other units depend on |
| `exec` | The binary has been executed successfully | Slightly better `simple`; catches a bad path immediately |
| `notify` | The app calls `sd_notify(READY=1)` | Anything with dependents — this is the only type that tells the truth |
| `forking` | The parent exits and the child is running (needs `PIDFile=`) | Legacy daemons that background themselves |
| `oneshot` | The command exits (use `RemainAfterExit=yes` to stay "active") | Migrations, warmups, one-time setup |

With `Type=simple`, a unit ordered `After=api.service` starts while the API is still loading, health checks fire against a closed port, and the proxy marks the upstream down at boot. If the app cannot do `sd_notify`, either use `oneshot` wrappers with a readiness poll or accept that ordering guarantees nothing and make dependents retry.

## Restart Semantics and the Start Limit

| Directive | Meaning | Sane value |
|---|---|---|
| `Restart=on-failure` | Restart on non-zero exit, signal, timeout, or watchdog | The default choice for services |
| `Restart=always` | Restart even after a clean exit | Only for processes that exit 0 when they should not |
| `RestartSec` | Delay before restarting | 5s — enough to stay under the start limit while a crash loop is happening |
| `StartLimitIntervalSec` / `StartLimitBurst` | The ban rule: default 5 starts within 10s and systemd **stops trying permanently** | Widen the interval rather than raising the burst |

The failure mode that costs the most: an app crashes on a bad config, systemd restarts it five times in ten seconds, gives up, and the unit sits in `failed` — so the service is down and *no longer trying* even after the underlying cause is fixed. `systemctl reset-failed api` clears the counter; `systemctl status` shows "start request repeated too quickly" and that string is the tell.

With `RestartSec=5`, five restarts take 25 seconds, comfortably clear of a 10-second window — which is exactly why the default of 100ms is dangerous and 5s is not.

## Ordering and Dependencies

- `After=` orders; `Requires=` and `Wants=` create dependencies. **Ordering without a dependency does nothing if the other unit was never asked to start**, and a dependency without ordering starts both at once. Almost always you want both.
- `network-online.target` requires `Wants=` as well as `After=`, and it is only meaningful if a network-wait service is enabled. An app that binds a specific IP needs it; an app that binds `0.0.0.0` usually does not.
- A service reading from a mounted disk needs `RequiresMountsFor=/srv/data`, not `After=local-fs.target` — network mounts arrive late and the app starts before its data exists.
- `Requires=postgresql.service` on the same box means a database restart takes the app down with it. `Wants=` plus application-level retry is usually the better contract; databases are restarted more often than apps.

## Environment and Secrets

- `EnvironmentFile=/etc/api/env` with mode `0640`, owned `root:api`. **Never `Environment=DATABASE_URL=postgres://user:pass@…` in the unit**: unit files are world-readable and every value shows up in `systemctl show`.
- Secrets are visible in `/proc/<pid>/environ` to the service's own user regardless of how they are delivered — that is a reason to run the service as a dedicated user, not a reason to skip environment files.
- systemd credentials (`LoadCredential=`) keep a secret out of the environment entirely and expose it as a file readable only by the unit — worth it for high-value keys on systemd ≥247.
- What gets written to `~/Clawic/data/`: the *path* and the variable names, never the values — `EnvironmentFile=/etc/api/env` and `DATABASE_URL=<env:DATABASE_URL>` (`memory-template.md`).

## Limits the Unit Must Set

A service does **not** inherit the `ulimit` from your interactive shell. Whatever you tested by hand is not what the unit gets.

| Directive | Why |
|---|---|
| `LimitNOFILE=65535` | The soft default of 1024 caps concurrent connections plus open files at roughly 500 real clients; `Too many open files` is the symptom |
| `MemoryMax=2G` | Bounds one service's OOM to itself; without it the kernel picks a victim and it is often the database |
| `MemoryHigh=1500M` | Throttles before killing — an app that slows down is easier to diagnose than one that vanishes |
| `TasksMax=4096` | A thread or fork leak takes the whole box's PID space otherwise |
| `CPUQuota=200%` | Two cores' worth; useful to keep a batch job from starving the web path |
| `OOMPolicy=stop` | Do not restart into the same OOM loop forever |

`systemctl show api -p MemoryMax,LimitNOFILE` prints what is actually in force — read it rather than the file, because a drop-in in `/etc/systemd/system/api.service.d/` may be overriding you.

## Graceful Stop and Reload

- On stop, systemd sends `SIGTERM` to every process in the cgroup, waits `TimeoutStopSec` (90s by default), then `SIGKILL`. An app that ignores SIGTERM waits the full 90 seconds on every deploy.
- The app's shutdown contract: stop accepting new connections, finish in-flight requests, close pools, exit. That has to be shorter than `TimeoutStopSec`, and the deploy's health gate must be longer than it.
- `ExecReload=/bin/kill -HUP $MAINPID` gives `systemctl reload` for apps that reload config on HUP. Without `ExecReload`, `reload` fails and people reach for `restart`, which drops connections (SKILL.md Rule 6).
- `KillMode=mixed` sends SIGTERM only to the main process and SIGKILL to the rest at timeout — correct when the app manages its own children (Gunicorn, Puma) and wants to shut them down in order.

## Socket Activation

systemd owns the listening socket, hands it to the app, and holds incoming connections while the app restarts:

```ini
# api.socket
[Socket]
ListenStream=127.0.0.1:8000
[Install]
WantedBy=sockets.target
```

With a matching `api.service` (`Requires=api.socket`), a restart never produces a refused connection — clients wait in the backlog instead. The app has to accept a pre-opened fd (systemd's activation protocol); frameworks that cannot are not candidates. This is the cheapest real zero-downtime restart available on a single box, and it also solves "port already in use" permanently, because the socket has exactly one owner.

## Timers Instead of Cron

For anything this skill schedules — certificate checks, restore drills, log sweeps — a timer beats a cron line: it logs to the journal, it has `Persistent=true` for missed runs after downtime, and it can depend on other units.

```ini
# restore-drill.timer
[Timer]
OnCalendar=quarterly
Persistent=true
RandomizedDelaySec=1h
```

`systemctl list-timers` shows the next run for everything. Host-level cron semantics and their environment traps belong to the `linux` skill; the recurring items *this* skill tracks belong in the `## Due` table of `memory.md` regardless of what triggers them.

## Template Units for Many Instances

`api@.service` with `%i` as the instance name runs N copies from one file: `systemctl enable --now api@8001 api@8002`, then load-balance across them in the proxy. This is how you use every core with a single-threaded runtime without a process manager (`workers.md`), and how a game server hosts several worlds from one unit file (`selfhosted.md`).

## User Services

`systemctl --user` units live in `~/.config/systemd/user/` and need `loginctl enable-linger <user>` to run without an active login session — otherwise they stop when the user logs out, which is the exact problem supervision was supposed to solve. Fine for a personal box; for anything shared, a system unit with a dedicated user is clearer.

## PM2

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api',
    script: './dist/index.js',
    instances: 'max',          // one per core; a number is better once you know the box
    exec_mode: 'cluster',
    max_memory_restart: '512M',
    env: { NODE_ENV: 'production', PORT: 3000 }
  }]
};
```

- `pm2 reload api` restarts workers one at a time and keeps serving; `pm2 restart` does not. Use `reload` in the deploy path.
- **`pm2 startup` then `pm2 save` is mandatory**, and it is the step everyone skips: without both, nothing comes back after a reboot. `pm2 save` must be re-run after the app list changes, or the box boots with last month's process list.
- `instances: 'max'` on a shared box takes every core including the database's. Set a number.
- Cluster mode requires the app to be stateless across workers: in-memory sessions, in-process caches and local WebSocket rooms break the moment there are two workers (`workers.md`).
- PM2's own logs grow forever unless `pm2-logrotate` is installed (`logs.md`).

## supervisord

Still the right answer inside images that need several processes and on hosts without systemd. Key points: `autostart=true`, `autorestart=unexpected`, `startretries` (default 3, then `FATAL` and no more attempts — same trap as the systemd start limit), `stopasgroup=true` and `killasgroup=true` so children die with the parent, and `stopsignal=TERM`. Supervisord itself must be started by something; on a systemd host that means a unit, which is one indirection too many unless an image requires it.

## When Supervision Is Not Happening

| Looks supervised | Actually |
|---|---|
| `systemctl start` was run, `enable` was not | Gone after the next reboot; `is-enabled` says `disabled` |
| PM2 running, no startup unit / no `pm2 save` | Gone after the next reboot, and PM2 reports everything fine until then |
| Container running, `restart: no` (the default with `docker run`) | Gone after a daemon restart or a host reboot |
| `nohup`, `screen`, `tmux` | Gone when the session, the box, or the OOM killer decides |
| Unit in `failed` after a crash loop | Down and not retrying — the start limit was hit (above) |
| Unit ordered after a network mount that arrives late | Starts, fails to find its data, and the restart limit bans it before the mount appears |

Check the whole box in one pass: `systemctl list-units --state=failed` and `systemctl list-unit-files --state=enabled` together answer "what is broken" and "what will come back".

## Write It Down

Every service you supervise gets its row in `## Services` — name, host, runtime, listen address including the interface, supervisor and unit name, public vhost, restart policy, data path (`memory-template.md`). A unit file that took real work to get right (limits raised for a measured reason, an ordering that finally fixed a boot race) goes to `~/Clawic/data/server/artifacts/working-unit-<service>.md` with the reason for each non-default value, and its `## Boxes` line in the same turn. Values in the unit that are secrets are written as pointers, never literals.
