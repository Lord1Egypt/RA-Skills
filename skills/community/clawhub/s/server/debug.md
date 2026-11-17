# Debugging — Symptom to Cause, Hop by Hop

The method: work from the hop closest to the app outward, and never skip a hop because it "cannot be that". Each step below either proves a hop good or names the fault.

**Before diagnosing**, read `## Services` and `## Baselines` in `~/Clawic/data/server/memory.md` (or the files `## Boxes` points to) and skim `incidents/<year>.md` if it exists: a symptom that already happened once has a written cause, and re-deriving it costs the same hours a second time.

**Contents:** [The Ladder](#the-ladder) · [Refused vs Timed Out vs Reset](#refused-vs-timed-out-vs-reset) · [Port Conflicts](#port-conflicts) · [Listening on the Wrong Thing](#listening-on-the-wrong-thing) · [Reading the Status Code](#reading-the-status-code) · [Slow, Not Broken](#slow-not-broken) · [It Works Sometimes](#it-works-sometimes) · [Worked Yesterday](#worked-yesterday) · [Correlating Across Hops](#correlating-across-hops) · [CORS](#cors) · [DNS and Name Resolution](#dns-and-name-resolution) · [Tools by Question](#tools-by-question) · [Write It Down](#write-it-down)

## The Ladder

Six checks, in this order, from the box itself. Each one that passes eliminates everything inside it.

1. **Is the process alive?** `systemctl status <unit>` / `docker compose ps`. Look at the *state*, not just the output — `activating`, `failed`, and `Restarting` are three different problems.
2. **Is it listening, and on what?** `ss -tlnp | grep <port>`. Read the Local Address column: `127.0.0.1:8000` is not `0.0.0.0:8000`.
3. **Does it answer locally?** `curl -sv http://127.0.0.1:8000/healthz`. If this fails, everything outward is irrelevant.
4. **Does the proxy reach it?** `curl -sv -H 'Host: example.com' http://127.0.0.1/`. Bypasses DNS and TLS, isolates the proxy's routing from everything else.
5. **Does it answer from outside the box?** From another machine: `curl -sv https://example.com/`. Failing only here means firewall, security group, or DNS.
6. **Does the client see something different?** Browser dev tools, another network, another DNS resolver. Corporate proxies, captive portals, and stale DNS live here.

Going in the other direction — starting from the browser — is how an afternoon disappears into a network problem that was a stopped unit.

## Refused vs Timed Out vs Reset

The three connection errors are three separate diagnoses and must never be treated alike:

| Error | Means | Look at |
|---|---|---|
| `Connection refused` | A machine answered with a TCP RST: nothing is listening on that port, or it is bound to a different interface | The listen address (step 2), then whether the right unit is running |
| `Connection timed out` | Nothing answered at all: packets are being dropped | Host firewall, cloud security group, wrong IP, network path |
| `Connection reset by peer` | Established, then torn down mid-conversation | The app crashing mid-request, a proxy killing the connection, an MTU/TLS mismatch |
| `No route to host` | Rejected by the network layer before reaching the host | Routing, or a firewall configured to reject rather than drop |
| Hangs with no error | Something is accepting and never answering | The accept queue, a stalled worker, or a timeout that is longer than your patience |

`refused` from outside while `curl 127.0.0.1` works on the box is loopback binding, ~90% of the time (SKILL.md Rule 7).

## Port Conflicts

```
ss -tlnp | grep :8000        # who holds it, with PID and process name
lsof -i :8000                # same, plus the user
fuser -n tcp 8000            # PIDs only, when the others are unavailable
```

Then **stop the supervisor, not the process**. Killing a supervised PID gets it restarted within `RestartSec` and the port is taken again a few seconds later, which reads like the kill failed. `systemctl stop <unit>` or `docker compose down` for that stack.

Two units defining the same port is the other case: `grep -rl ':8000' /etc/systemd/system/ /etc/nginx/` finds the second definition. Port allocation is a convention worth recording once (`config.yaml` → `conventions.port_range`) instead of rediscovering.

Inside a container, port conflicts happen at two levels: the published host port and the port inside the container. `docker compose ps` shows the mapping; a conflict on the host port fails at start, a conflict inside is invisible from outside.

## Listening on the Wrong Thing

| What `ss` shows | Reachable from |
|---|---|
| `127.0.0.1:8000` | Only the box itself (the correct state for an app behind a proxy) |
| `0.0.0.0:8000` | Everywhere the firewall allows — the correct state only for the proxy |
| `[::1]:8000` | IPv6 loopback only; a client resolving to IPv4 gets refused |
| `[::]:8000` | All IPv6, and usually all IPv4 too via dual-stack — check `net.ipv6.bindv6only` before assuming |
| Unix socket path | Only processes with filesystem permission on that path |

The IPv6 trap deserves its own line: an app bound to `[::1]` while the proxy connects to `127.0.0.1` produces `Connection refused` with everything apparently running. `localhost` resolves to both and the order varies by system, so name the address explicitly on both sides rather than relying on `localhost`.

Socket permission failures look identical to a dead upstream: the proxy reports 502 whether the socket is missing or unreadable. `ls -l` the socket and check the proxy user is in the owning group.

## Reading the Status Code

| Code | Emitted by | Means |
|---|---|---|
| 502 | Proxy | Upstream refused, closed, or spoke nonsense. The app is the suspect |
| 503 | Proxy or app | No upstream available (all marked down), or the app deliberately shedding load |
| 504 | Proxy | Upstream too slow — a timeout, and the number of seconds names which one |
| 499 | nginx only | The **client** disconnected before the response. Nothing is wrong with the server except its speed |
| 413 | Proxy or app | Body larger than a limit somewhere on the path |
| 400 after an upgrade attempt | Proxy | WebSocket headers missing (`proxy.md`) |
| 404 for every route behind a prefix | App | Path rewriting: the trailing slash on `proxy_pass` (`proxy.md`) |
| 301/302 loop | App + proxy | `X-Forwarded-Proto` not sent or not trusted (`proxy.md`) |
| 200 with wrong content | Proxy | Wrong upstream, wrong vhost matched, or a cache serving someone else's response |

A 500 is the app's own error and belongs in the application log; if the app log has nothing, the request never reached it and the code came from the proxy.

## Slow, Not Broken

Time the hops rather than guessing:

```
curl -w 'dns %{time_namelookup}  connect %{time_connect}  tls %{time_appconnect}  ttfb %{time_starttransfer}  total %{time_total}\n' -o /dev/null -s https://example.com/
```

- **High `time_namelookup`**: resolver, not the server.
- **High `time_connect`**: network latency or a full accept queue.
- **High `time_appconnect`**: TLS handshake — missing session resumption, or OCSP fetch on every connection (`tls.md`).
- **High `time_starttransfer` with low connect**: the app is thinking. Now it is an application problem, and the proxy is exonerated.
- **`total` far above `starttransfer`**: the response body is slow — large payload, no compression, or a stream.

Run the same curl from the box against the upstream directly. If `ttfb` is fast locally and slow from outside, the difference is entirely proxy or network; if it is slow locally, stop looking at infrastructure.

## It Works Sometimes

Intermittent failures have a short list of causes, and load is the discriminator:

| Pattern | Cause |
|---|---|
| Worse under load, fine when idle | Upstream keepalive shorter than the proxy's (Rule 4), or a pool/worker limit being hit |
| Every Nth request | One unhealthy upstream in a round-robin pool |
| Fails for some users only | DNS returning several records, IPv6 path broken, or a stale CDN edge |
| Fails at a fixed interval | A cron job, a worker recycle, a log rotation, a GC pause, a backup |
| Fails after a fixed uptime | A leak: memory, file descriptors, connections. Graph it against uptime |
| Only large requests | Body limit, buffer spilling to a full temp disk, or MTU |
| Only slow clients | Sync workers without a buffering proxy (`workers.md`) |

The two commands that separate "one bad upstream" from "everything is bad": hit the endpoint 100 times and count failures, then hit each upstream directly the same number of times.

## Worked Yesterday

Something changed. In descending order of likelihood, and all cheap to check:

1. A deploy — `deploys/<year>.md` and the release directory timestamps.
2. A certificate renewed without a reload (`tls.md`).
3. A package or kernel upgrade — unattended upgrades run on their own schedule and restart services.
4. Disk filled — logs, a database, or an upload directory. Then everything fails weirdly at once (`logs.md`).
5. A DNS or CDN change nobody associated with this service.
6. A dependency's certificate, API version, or rate limit changed on their side.
7. Traffic grew past a limit that was always there (`capacity.md`).

Check the boring ones first: `df -h`, `uptime`, `journalctl --since '2 days ago' -p err`, and the release directory's modification time answer most of this in a minute.

## Correlating Across Hops

Without a shared identifier, three logs are three unrelated stories. Generate a request id at the proxy, pass it upstream, log it everywhere:

```nginx
proxy_set_header X-Request-Id $request_id;
log_format withid '$remote_addr $request_id "$request" $status $request_time $upstream_response_time';
```

`$request_time` (total, including the client) minus `$upstream_response_time` (the app) is the proxy's own contribution — the difference is where slow clients and buffering show up. Both belong in the access-log format from day one (`logs.md`).

## CORS

CORS errors are browser-side and say nothing about the server being reachable; curl will happily succeed on a request the browser blocks.

- The failure is always a **missing or wrong response header** from the server: `Access-Control-Allow-Origin` must echo an allowed origin (not `*` when credentials are involved — that combination is rejected by every browser).
- Preflight: the browser sends `OPTIONS` first for non-simple requests. If the app or proxy answers `OPTIONS` with 404 or 405, everything else is irrelevant. Handle it, and return 204.
- `Access-Control-Allow-Credentials: true` requires an explicit origin and matching credentials mode on the client.
- Adding CORS headers at both the proxy and the app produces *duplicate* headers, which browsers reject outright. Pick one owner.
- In development, proxy the API through the dev server instead of relaxing production headers (`dev-servers.md`). A wildcard added "temporarily" to unblock a demo is still there a year later.

## DNS and Name Resolution

- `dig example.com` from the box and from outside; they can differ (split-horizon, `/etc/hosts`, a container's resolver).
- Propagation is not a thing that happens to you: old answers live for the TTL that was published *before* the change. Lower the TTL well ahead of a migration — that is the `dns` skill's territory, but the symptom lands here as "half the users see the old server".
- Inside containers, name resolution goes through the runtime's DNS, and a service name only resolves within its network (`containers.md`).
- `getent hosts example.com` shows what the system resolver returns, including `/etc/hosts` overrides, which `dig` bypasses entirely — a stale hosts entry from a test is a classic hour-long detour.

## Tools by Question

| Question | Tool |
|---|---|
| What is listening? | `ss -tlnp` |
| Who holds this port/file? | `lsof -i :PORT`, `lsof +L1` for deleted-but-open files |
| What is this process doing right now? | `strace -p PID -f -e trace=network` (sparingly, it slows the target) |
| Is traffic arriving at all? | `tcpdump -i any port 8000 -nn` |
| What did the service log? | `journalctl -u <unit> -n 200 --no-pager`, `-f` to follow |
| Why did it get OOM-killed? | `journalctl -k | grep -i 'killed process'` |
| Is the disk or inode table full? | `df -h`, `df -i` |
| What is the actual effective limit? | `systemctl show <unit> -p LimitNOFILE,MemoryMax`, `cat /proc/PID/limits` |
| Is TLS what I think it is? | `openssl s_client -connect host:443 -servername host` (`tls.md`) |
| Where is the time going? | The `curl -w` timing line above |

Host-level depth — permission and SELinux denials, disk and inode exhaustion, OOM analysis, boot failures — is the `linux` skill; come back here once the process itself is proven healthy.

## Write It Down

When a real outage is resolved, add a row to `~/Clawic/data/server/incidents/<year>.md`: date, service, symptom as the user saw it, the **real** cause, the fix, and how long it was down (`memory-template.md`). Write the real cause, not the first hypothesis. Two rows with the same cause mean the diagnostic sequence belongs in `~/Clawic/data/server/artifacts/runbook-<symptom>.md` — with its `## Boxes` line added the same turn — and any recurring check it implies belongs in `## Due`.
