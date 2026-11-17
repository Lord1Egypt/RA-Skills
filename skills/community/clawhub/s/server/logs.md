# Logs — Format, Rotation, Retention, Correlation

Logs are the only evidence you have after the fact, and the most common cause of a full disk. Both problems are solved by the same decisions.

**Before changing log configuration**, read `## Services` in `~/Clawic/data/server/memory.md` for where each service writes and which of them are chatty; a rotation policy applied to the wrong path is a policy that silently does nothing.

**Contents:** [Three Log Streams](#three-log-streams) · [Access Log Format](#access-log-format) · [Correlating a Request](#correlating-a-request) · [Application Logs](#application-logs) · [journald](#journald) · [logrotate Without Losing Lines](#logrotate-without-losing-lines) · [Disk: The Actual Failure](#disk-the-actual-failure) · [Retention](#retention) · [What Never Goes in a Log](#what-never-goes-in-a-log) · [Shipping Logs Off the Box](#shipping-logs-off-the-box) · [Reading Logs Fast](#reading-logs-fast) · [Write It Down](#write-it-down)

## Three Log Streams

| Stream | Written by | Answers |
|---|---|---|
| Access log | Proxy | Who asked for what, what status, how long, how big |
| Error log | Proxy | Why the proxy could not do its job — upstream refused, timeouts, TLS handshake failures |
| Application log | The app | What the code did and why it failed |

They are read together or not at all: a 502 in the access log has its cause in the proxy's error log, and the app's log tells you whether the request ever arrived. Keeping them on different retention schedules is how you get an access log for an incident whose application log has already rotated away.

## Access Log Format

The default format is missing the three fields you will want:

```nginx
log_format main '$remote_addr $request_id "$request" $status $body_bytes_sent '
                'rt=$request_time urt=$upstream_response_time '
                'ua="$http_user_agent" ref="$http_referer" host=$host';
```

| Field | Why |
|---|---|
| `$request_time` | Total, including sending the response to a slow client |
| `$upstream_response_time` | The app's share. The **difference** between the two is proxy and network, and that gap is where slow-client problems hide |
| `$request_id` | The join key across every log on the box (below) |
| `$host` | Which vhost matched, on a box serving several |
| `$upstream_addr` | Which backend served it, once there is more than one |

`$remote_addr` is the real client only if forwarded headers are handled correctly; otherwise it is the CDN and every log line is the same address (`proxy.md`).

JSON access logs (`escape=json`) are worth it the moment anything queries them — but keep the same field names as the plain format so a grep on either works the same way.

Turn access logging off for static assets (`access_log off` in the asset location): on a busy site that is most of the volume and none of the information (`static.md`).

## Correlating a Request

One id, generated at the outermost hop, present in every line:

- Proxy: `proxy_set_header X-Request-Id $request_id;` and `$request_id` in the log format.
- App: read the header, put it on the logger's context, emit it on every line including the stack trace.
- Downstream calls: forward the same header, so a failure three services away is one grep.

Without this, an incident investigation is three files sorted by timestamp and a hope that clocks agree. With it, `grep <id> /var/log/nginx/access.log /var/log/api/app.log` is the whole investigation.

## Application Logs

- **Write to stdout/stderr** and let the supervisor route it (journald, the container runtime's driver). An app managing its own files and its own rotation is an app that will fight logrotate.
- **Structured (JSON) for machines, one line per event.** A multi-line stack trace is one event and must not become forty lines in a log aggregator — most loggers can serialize the trace into a field.
- **Levels used honestly**: ERROR is something a human must act on; WARN is something worth reviewing later; INFO is the request lifecycle; DEBUG is off in production. An ERROR that fires ten thousand times a day trains everyone to ignore ERROR.
- **Sample high-volume events** rather than dropping them: 1% of successful health checks tells you the pattern at 1% of the cost.
- Log the *decision*, not just the outcome: "rejected upload: 12 MB over 10 MB limit" is actionable; "upload failed" costs an hour.

## journald

- `journalctl -u <unit> -n 200 --no-pager`, `-f` to follow, `-p err` to filter by priority, `--since '2 hours ago'`.
- **journald has its own limits and is not rotated by logrotate**: `SystemMaxUse` defaults to 10% of the filesystem, capped at 4 GB. A chatty service silently occupies gigabytes and the `/var/log` cleanup nobody did was never going to touch it.
- `journalctl --disk-usage` shows the real number; `journalctl --vacuum-time=14d` or `--vacuum-size=1G` reclaims it. Set `SystemMaxUse` in `journald.conf` rather than vacuuming by hand every quarter.
- Persistent vs volatile: if `/var/log/journal/` does not exist, the journal is in memory and **gone at reboot** — which is precisely when you wanted to read it. Create the directory to make it persistent.
- `journalctl -k | grep -i 'killed process'` finds OOM kills, the answer to a large fraction of "the service just disappeared" reports (`debug.md`).

## logrotate Without Losing Lines

The wrong way and the right way, and the difference is data:

```
# WRONG: copytruncate loses every line written between copy and truncate,
# and a process holding the fd keeps writing at the old offset, producing a
# sparse file that reappears at its old size.
/var/log/myapp/*.log { daily copytruncate rotate 14 }
```

```
# RIGHT: rename, create a fresh file, tell the process to reopen it.
/var/log/nginx/*.log {
    daily
    rotate 14
    missingok
    notifempty
    compress
    delaycompress
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /run/nginx.pid ] && kill -USR1 $(cat /run/nginx.pid)
    endscript
}
```

- `USR1` makes nginx reopen its log files; without it nginx keeps writing to the renamed (or deleted) file and `/var/log` shows an empty `access.log` while the disk fills. `lsof +L1` reveals deleted-but-open files.
- `delaycompress` exists because compressing the file the process may still be writing to corrupts it.
- `sharedscripts` sends the signal once for a glob, not once per matched file.
- Test with `logrotate -d /etc/logrotate.d/myapp` (dry run) and `-f` to force one real rotation — a rotation config is never verified by waiting a day.
- Apps that write their own files need their own reopen signal, or `copytruncate` becomes the least-bad option. Prefer stdout and let the supervisor own it.

## Disk: The Actual Failure

The failure chain is always the same: logs fill the disk, the database cannot write, the app throws errors, the errors are logged, and the disk fills faster. By the time anyone looks, several unrelated things are broken.

- Logs on the same partition as data means one can kill the other. A separate `/var/log` partition turns a total outage into a logging outage.
- Watch inodes too: millions of tiny rotated files exhaust inodes with the disk apparently half empty. `df -i` next to `df -h`, always.
- Alert at 80% and again at 90%; below 80% there is no urgency and above 90% there is no time.
- The monthly disk-and-rotation check belongs in `## Due` (`maintenance.md`); it takes two minutes and prevents the most boring outage there is.
- Container logs default to unbounded JSON files in most runtimes — `max-size` and `max-file` on the logging driver, or one talkative container fills the host (`containers.md`).

## Retention

Decide per stream, and write the number in `~/Clawic/data/server/artifacts/decision-logging.md`:

| Stream | Typical | Driven by |
|---|---|---|
| Access logs | 14-30 days on the box, longer if shipped | Debugging window and disk |
| Error logs | 30-90 days | Incidents get investigated late |
| Application logs | 14-30 days on the box | Volume |
| Audit or auth logs | As long as the regime requires | Compliance, not convenience |
| Anything with personal data | The shortest defensible period | Data protection: logs are a data store, and an IP address is personal data in some regimes |

Retention that exists only as a logrotate `rotate N` is retention nobody can state: the config holds a count, and the question is always in days.

## What Never Goes in a Log

- Passwords, tokens, API keys, session ids, cookies, `Authorization` headers — redact at the logger, not with a later grep.
- Full request bodies on authentication, payment, or profile endpoints.
- Query strings that carry tokens: log the path and drop the query, or allowlist the parameters worth keeping.
- Card numbers, national identifiers, health data — a log is a data store with the weakest access control on the box.
- Nothing from a log is ever copied verbatim into `~/Clawic/data/`. When an excerpt is genuinely part of a runbook or an incident record, secrets are replaced by their pointers first (`memory-template.md`).

Redaction is a code change, and the moment to make it is when you notice, because a log line written today is in the backup by tomorrow.

## Reading Logs Fast

| Question | One-liner |
|---|---|
| Top status codes in the last hour | `awk '{print $6}' access.log | sort | uniq -c | sort -rn` (adjust the field to your format) |
| Slowest endpoints | `awk '{print $NF, $4}' access.log | sort -rn | head -20` |
| Requests from one IP | `grep '^203\.0\.113\.' access.log` |
| Everything about one request | `grep <request-id> /var/log/nginx/access.log /var/log/api/*.log` |
| Errors since a deploy | `journalctl -u api --since '2026-07-25 17:40' -p err` |
| Is it a burst or steady? | Count per minute: `cut -d: -f1-2 access.log | uniq -c` |

Ad-hoc field numbers depend on the format, which is the strongest argument for JSON logs and `jq` the moment anyone does this twice a week.

## Write It Down

The logging decisions that outlive a session — where each service writes, the retention agreed per stream, the rotation signal a hand-rolled app needs, the request-id header in use — go to `~/Clawic/data/server/artifacts/decision-logging.md`, with its `## Boxes` line in `memory.md` the same turn. The disk-and-rotation check goes in `## Due`. A disk-full outage goes in `incidents/<year>.md` with what actually filled it, because the second time it will be the same thing (`memory-template.md`).
