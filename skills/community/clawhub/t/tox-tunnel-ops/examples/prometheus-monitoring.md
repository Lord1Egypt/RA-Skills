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
data_dir: /etc/toxtunnel/server
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
    - { local_port: 2222, remote_host: 127.0.0.1, remote_port: 22 }

metrics:
  enabled: true
  listen: 127.0.0.1:9101          # use a different port if running on the same host
  path: /metrics
```

## Prometheus Scrape Config

```yaml
# prometheus.yml
scrape_configs:
  - job_name: toxtunnel-server
    static_configs:
      - targets: ['toxtunnel-server.lan:9100']
        labels:
          role: server
    scrape_interval: 15s

  - job_name: toxtunnel-client
    static_configs:
      - targets: ['toxtunnel-client.lan:9101']
        labels:
          role: client
    scrape_interval: 15s
```

If Prometheus runs on a different host than ToxTunnel, expose the metrics port
over an SSH local-forward or a ToxTunnel forward to the scraper itself, rather
than binding `metrics.listen` to a public interface.

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
| `toxtunnel_tunnels_active{role=...}` | gauge | Live concurrency; alert > 80 (default cap is 100/friend) |
| `toxtunnel_tunnels_opened_total{result="ok\|denied\|failed"}` | counter | `denied` spike = rules blocking, `failed` = target unreachable |
| `toxtunnel_tunnels_closed_total{reason="local\|remote\|timeout\|error"}` | counter | `timeout` = idle reaper, `error` = unexpected close |
| `toxtunnel_bytes_in_total` / `toxtunnel_bytes_out_total` | counter | Throughput; rate() it in PromQL |
| `toxtunnel_tox_iterate_lag_milliseconds_max` | gauge | Tox thread health; alert > 100 ms sustained |

## Useful Queries

```promql
# Tunnel open denial rate (rules-engine activity)
rate(toxtunnel_tunnels_opened_total{result="denied"}[5m])

# Throughput in MiB/s
rate(toxtunnel_bytes_in_total[1m]) / 1024 / 1024
rate(toxtunnel_bytes_out_total[1m]) / 1024 / 1024

# Average concurrent tunnels by role
avg_over_time(toxtunnel_tunnels_active[5m])

# Tox thread lag (alert if max stays high)
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
          summary: "Sustained tunnel-open denials — check rules.yaml or unauthorized peers"

      - alert: ToxTunnelIterateLagHigh
        expr: toxtunnel_tox_iterate_lag_milliseconds_max > 100
        for: 5m
        annotations:
          summary: "Tox iterate loop running slow — investigate CPU / I/O contention"
```

## Cross-Check with `toxtunnel inspect`

`/metrics` gives you aggregates; `toxtunnel inspect` gives you per-tunnel
detail. Use both:

```bash
# Aggregate counters
curl -s 127.0.0.1:9100/metrics | grep tunnels_active

# What's actually open right now
toxtunnel inspect tunnels
toxtunnel inspect status --json | jq '{friends_online, active_server, tunnels_active}'
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
