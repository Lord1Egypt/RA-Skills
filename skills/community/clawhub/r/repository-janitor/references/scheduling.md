# Scheduling

This skill does not install or change schedules automatically.

For an approved daily audit, schedule the same explicit Python command used manually:
```text
python3 /absolute/skill/path/scripts/audit.py --config /private/config.json --fetch --github --persist --report
```
Choose the operator's business timezone, schedule, delivery route, and owner. A typical daily time is 03:00 local. Allow the process at least its configured 480-second audit budget plus report overhead. Capture stdout, process exit, and delivery receipt independently.

With OpenClaw, a `script` payload can run without an LLM and return `{notify: reportText}`. The installed tool contract uses `exec({command, timeoutSeconds, yieldMs})`. If execution returns a running session, poll that owned session using `process({action:"poll", sessionId, timeout:30000})` until completion within the script budget. Do not invent a run success when stdout is empty or the process fails. Keep the scheduler command path private and local.

Watchdog:
```text
python3 /absolute/skill/path/scripts/watchdog.py --job-id APPROVED_JOB_ID --config /private/config.json
```
Run it in a separate job, typically every 15 minutes. It reads the target job through the OpenClaw CLI and reports activation, overdue schedule, stale/failed execution, delivery problems, or incomplete audit coverage. The target must be accessible under the watchdog's legitimate scheduler authority.

Deduplicate using the scheduler's persisted state: compare the returned status with the previous status; notify on transitions into failure and once on recovery. Initial healthy observation is silent. Treat unparseable output or inaccessible metadata as unknown, not healthy. Test healthy, failed, stale, recovery, and delivery paths before calling monitoring fully verified.

If updating a legacy job fails because of owner/account scope, report the blocker and use the supported administrative workflow. Do not edit scheduler databases, borrow credentials, impersonate another owner, or create a duplicate daily job.

Watchdog thresholds assume a daily job: execution over 15 minutes, schedule overdue over one hour, or no execution within 27 hours. Adjust and test for other cadences. This same-host watchdog does not detect total host/Gateway failure while it is down.
