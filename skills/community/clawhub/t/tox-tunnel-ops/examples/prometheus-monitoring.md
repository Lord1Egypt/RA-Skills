# Prometheus + Grafana Monitoring for ToxTunnel

## Scenario

You're running ToxTunnel as a real service (homelab, small team, contractor
gateway) and want to monitor it the same way you monitor everything else:
scrape `/metrics` into Prometheus, plot in Grafana, alert when things break.

## Key Principles

- **`metrics.enabled` is opt-in (defaults to `false`).** Nothing leaves the
  process until you flip the switch.
- **Default loopback bind.** `metrics.listen: 127.0.0.1:9100` only — widen it
  only when the scraper is on a network you trust. Prometheus exposition has
  no built-in auth.
- **Both modes can expose metrics.** Server and client emit different label
  sets; running metrics on both gives you a full picture.
- **Listen address is NOT hot-reloadable.** Changing `metrics.listen`
  requires a daemon restart.

## Server Config Excerpt

```yaml
mode: server
data_dir: /var/lib/toxtunnel        # mutable state — NOT under /etc
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: /etc/toxtunnel/rules.yaml

metrics:
  enabled: true
  listen: 127.0.0.1:9100          # KEEP loopback unless scraper is trusted
  path: /metrics
```

> **`data_dir` holds mutable state, so keep it out of `/etc`.** That directory
> carries the Tox identity (`tox_save.dat`), the pid file, the data-directory
> lock and the inspect socket — all written at runtime. `/var/lib/toxtunnel` is
> what the packaged Linux unit uses (`StateDirectory=toxtunnel`,
> `StateDirectoryMode=0750`), owned by the dedicated `toxtunnel` user; macOS
> equivalent is `/usr/local/var/toxtunnel`. Keep `/etc/toxtunnel` for
> `server.yaml` and `rules.yaml` only.
>
> **Run the daemon as that unprivileged account, not as root.** Nothing here
> needs root once the package is installed: the Tox port is 33445 and the targets
> are ordinary services. The packaged unit already does this; a hand-written one
> must set `User=`, `Group=` and `StateDirectory=` itself.


## Client Config Excerpt

```yaml
mode: client
data_dir: ~/.config/toxtunnel/client
tox:
  udp_enabled: true
  bootstrap_mode: auto
client:
  server_id: homelab
  forwards:
    - { local_port: 2222, local_address: 127.0.0.1, remote_host: 127.0.0.1, remote_port: 22 }

metrics:
  enabled: true
  listen: 127.0.0.1:9101          # use a different port if running on the same host
  path: /metrics
```

## Prometheus Scrape Config

**The scrape target must be an address Prometheus can actually reach**, and with
the loopback binds above that is *not* `toxtunnel-server.lan:9100` — nothing
listens on that host's external interface. Pick one of these three, and make the
targets match:

**(a) Prometheus on the same host as the daemon** — the simple case:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: toxtunnel-server
    static_configs:
      - targets: ['127.0.0.1:9100']
        labels: { role: server }
    scrape_interval: 15s

  - job_name: toxtunnel-client
    static_configs:
      - targets: ['127.0.0.1:9101']
        labels: { role: client }
    scrape_interval: 15s
```

**(b) Prometheus elsewhere, reached over a forward** — bring each remote metrics
port to a distinct **local** port on the Prometheus host, then scrape *that*:

```bash
# On the Prometheus host: SSH local-forwards (one per daemon)
ssh -N -L 19100:127.0.0.1:9100 admin@toxtunnel-server.lan &
ssh -N -L 19101:127.0.0.1:9101 admin@toxtunnel-client.lan &
```

```yaml
scrape_configs:
  - job_name: toxtunnel-server
    static_configs:
      - targets: ['127.0.0.1:19100']    # the forwarded port, not the remote host
        labels: { role: server, instance_host: toxtunnel-server.lan }
    scrape_interval: 15s

  - job_name: toxtunnel-client
    static_configs:
      - targets: ['127.0.0.1:19101']
        labels: { role: client, instance_host: toxtunnel-client.lan }
    scrape_interval: 15s
```

A ToxTunnel `forwards:` entry works the same way. The entry above sets
`local_address: 127.0.0.1`, so on **v0.4.13+** the forwarded metrics port is
loopback-only; on v0.4.12 and older it binds `0.0.0.0` and must be firewalled on
the Prometheus host.

**(c) Bind `metrics.listen` to a non-loopback address** — only when the network
in front of it is genuinely trusted (a private VPC, a WireGuard mesh, a
firewalled monitoring subnet). Prometheus exposition has no authentication, so
anything that can reach the port reads your tunnel topology and byte counts. If
you do this, set `listen: 10.x.y.z:9100` on a management interface rather than
`0.0.0.0:9100`, and keep the targets in sync.

## Steps

1. Add the `metrics:` block to `server.yaml` and/or `client.yaml`
2. Restart the daemon (metrics listen isn't hot-reloadable): `sudo systemctl restart toxtunnel`
3. Smoke-test from the same host:
   ```bash
   curl -s http://127.0.0.1:9100/metrics | grep '^toxtunnel_' | head -20
   ```
4. Add the scrape config to Prometheus, reload Prometheus
5. Confirm targets are `UP` in the Prometheus UI

## Key Metrics

| Metric | Type | What to watch |
|--------|------|---------------|
| `toxtunnel_build_info{version=...}` | gauge | Version sanity check across the fleet |
| `toxtunnel_friends_online` | gauge | Alert if 0 unexpectedly — Tox connectivity broken |
| `toxtunnel_tunnels_active{role=...}` | gauge | Live concurrency **process-wide**. `role` is `server` or `client` and is the metric's *only* label — there is **no per-friend breakdown**, so you cannot alert on one friend approaching the 100/friend cap from this. For per-friend detail use `toxtunnel inspect tunnels` |
| `toxtunnel_tunnels_opened_total{result="ok\|denied\|failed"}` | counter | `denied` = **any** server-side policy refusal: rules denial *or* rate limiter *or* the concurrent-tunnel cap. A spike is not necessarily a rules problem — cross-check `toxtunnel_rate_limit_open_rejected_total` before concluding. `failed` = DNS/connect failures on the target side |
| `toxtunnel_tunnels_closed_total{reason="local\|remote\|timeout\|error"}` | counter | `timeout` = **either** reaper (idle *or* the default-on half-close cap), `error` = unexpected close |
| `toxtunnel_bytes_in_total` / `toxtunnel_bytes_out_total` | counter | Throughput; rate() it in PromQL |
| `toxtunnel_tox_iterate_lag_ms` | gauge | **The Tox-thread wedge signal.** Milliseconds since the last `tox_iterate()` *returned*; climbs toward `watchdog.deadline_seconds` while the thread is stuck. Alert on this one |
| `toxtunnel_tox_iterate_lag_milliseconds_max` (+ `_count`, `_sum`) | summary | Maximum *completed* iterate duration since process start. Latches on one old slow call, and cannot move while a call is actually hung — a slow-toxcore trend, **not** a wedge alarm |
| `toxtunnel_watchdog_aborts_total` | counter | **Resets to 0 on every restart** — it is not seeded from `<data_dir>/abort_count`. Since the watchdog aborts the process, the counter is 0 by the time you look. Alert on `increase()`, and read the file for the durable count |

## Useful Queries

```promql
# Tunnel-open denial rate. Covers rules denials, rate-limit rejections AND the
# concurrent-tunnel cap — compare against the rate-limit counter to tell them apart.
rate(toxtunnel_tunnels_opened_total{result="denied"}[5m])
rate(toxtunnel_rate_limit_open_rejected_total[5m])

# Throughput in MiB/s
rate(toxtunnel_bytes_in_total[1m]) / 1024 / 1024
rate(toxtunnel_bytes_out_total[1m]) / 1024 / 1024

# Average concurrent tunnels by role (process-wide; no per-friend series exists)
avg_over_time(toxtunnel_tunnels_active[5m])

# Tox thread health: live heartbeat age (the wedge signal)
toxtunnel_tox_iterate_lag_ms

# Slow-toxcore trend, NOT a wedge alarm (see the table above)
toxtunnel_tox_iterate_lag_milliseconds_max
```

## Suggested Alertmanager Rules

```yaml
groups:
  - name: toxtunnel
    rules:
      - alert: ToxTunnelFriendsAllOffline
        expr: toxtunnel_friends_online == 0
        for: 2m
        annotations:
          summary: "ToxTunnel has no online friends — connectivity broken"

      - alert: ToxTunnelDenialSpike
        expr: rate(toxtunnel_tunnels_opened_total{result="denied"}[5m]) > 1
        for: 5m
        annotations:
          summary: "Sustained tunnel-open denials"
          description: >-
            Could be rules.yaml refusing an unauthorised peer, the rate limiter,
            or the concurrent-tunnel cap. Check
            toxtunnel_rate_limit_open_rejected_total to tell them apart before
            editing rules.

      # The live heartbeat-age gauge is the correct wedge signal. Trip well
      # below watchdog.deadline_seconds (30 s default) so the alert precedes
      # the abort rather than arriving after the restart.
      - alert: ToxTunnelThreadWedging
        expr: toxtunnel_tox_iterate_lag_ms > 5000
        for: 1m
        annotations:
          summary: "Tox thread has not completed an iterate in >5 s — heading for a watchdog abort"

      # Historical trend only: this is the max COMPLETED iterate duration since
      # process start, so it latches and cannot move during an actual wedge.
      - alert: ToxTunnelIterateSlow
        expr: toxtunnel_tox_iterate_lag_milliseconds_max > 100
        for: 15m
        annotations:
          summary: "Tox iterate loop has been slow at some point — investigate CPU / I/O contention"

      # The counter resets to 0 on restart (it is not seeded from
      # <data_dir>/abort_count), and the watchdog aborts the process — so alert
      # on the increase, never on an absolute value.
      - alert: ToxTunnelWatchdogAborted
        expr: increase(toxtunnel_watchdog_aborts_total[1h]) > 0
        annotations:
          summary: "Watchdog aborted the daemon — check the 'tox_thread wedge detected' log line"
```

## Cross-Check with `toxtunnel inspect`

`/metrics` gives you aggregates; `toxtunnel inspect` gives you per-tunnel
detail. Use both:

```bash
# Aggregate counters
curl -s 127.0.0.1:9100/metrics | grep tunnels_active

# What's actually open right now
toxtunnel inspect tunnels
toxtunnel inspect status --json | jq '{friends_online, tunnels_active, bytes_in, bytes_out}'
```

## Verification

```bash
# Metrics endpoint is up
curl -fsS http://127.0.0.1:9100/metrics > /dev/null && echo "metrics OK"

# Prometheus sees the target
curl -s http://prometheus.lan:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job | startswith("toxtunnel"))'
```

## Diagnostics

- `connection refused` to the metrics port → `metrics.enabled: false` or
  daemon didn't pick up the change (restart, not reload)
- All `toxtunnel_*` metrics show 0 → daemon is up but no friends connected
  yet; cross-reference `toxtunnel_friends_online`
- Wrong path → custom `metrics.path` configured; default is `/metrics`
- Cannot reach metrics from Prometheus host → listen is loopback (correct
  default); use an SSH local-forward or a ToxTunnel forward rather than
  binding the metrics port to a public interface
