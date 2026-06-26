# Automation

## Runtime model

SherpaMind should run as a **long-lived local Python backend service**, not as a set of token-burning OpenClaw cron jobs.

Why:
- syncing/enrichment/public artifact refresh are backend chores, not conversational agent turns
- a service can wake on host startup and run internal timers without spending model tokens
- OpenClaw should query and consume SherpaMind outputs, not pretend to be the scheduler for a Python backend

## Service model

SherpaMind uses a user-level systemd service where available:
- unit name: `sherpamind.service`
- managed through `systemctl --user`
- executes the skill-local venv python with `-m sherpamind.cli service-run`

## Internal periodic lanes

The backend service owns the periodic work directly:
- hot open watcher/sync loop
- warm closed reconciliation loop
- cold closed audit loop
- priority enrichment loop
- public snapshot generation loop
- periodic service-state/health marker updates

The priority enrichment loop should stay retrieval-oriented rather than purely recency-oriented:
- open tickets first
- recently closed tickets next
- then broaden historical detail coverage across under-covered categories/accounts/technicians so the retrieval corpus gets deeper breadth over time instead of repeatedly clustering around one narrow slice of recent history

These run from internal Python timers, not OpenClaw cron.

The service also tracks real SherpaDesk request usage in SQLite and should use that to reserve the forecast hot/warm budget first, then spend spare hourly headroom opportunistically on cold audit and enrichment work instead of throttling cold depth with only a static conservative cadence.
Old request-event rows are pruned automatically by retention policy so the request log remains bounded.

Cold-history work should run in two phases:
- **bootstrap mode** until the historical corpus has completed one real full cold pass and closed-ticket detail coverage catches up
- **steady-state mode** after that, where cold re-audit/re-enrichment continues more slowly for drift correction and enrichment evolution

That first full-pass completion should be durable state, not guesswork.

The service should also repair stale derived retrieval artifacts when the current document materializer version no longer matches what is stored in `ticket_documents`. That keeps metadata/chunking improvements from depending on a human remembering to force a rematerialization pass.

## Install vs update behavior

### First install
- run `bootstrap-audit` first
- bootstrap the skill-local runtime
- migrate legacy state if needed
- initialize the DB
- stage the API key and connection settings
- validate discovery/seed behavior
- optionally generate initial public docs
- only then install/start the user service if unattended mode is actually wanted
- doctor the result
- clean up any legacy SherpaMind cron jobs

### Update / re-bootstrap
- rerun bootstrap safely
- preserve `.SherpaMind/{config,secrets,data,state,logs,runtime}` and `.SherpaMind/public`
- archive old repo-local `state/` leftovers once migrated
- reinstall/rewrite the systemd user unit idempotently
- restart the service safely
- doctor the runtime
- regenerate public artifacts if needed
- clean up any old SherpaMind cron jobs that no longer belong

## Commands

### Service management
- `python3 scripts/run.py install-service`
- `python3 scripts/run.py uninstall-service`
- `python3 scripts/run.py start-service`
- `python3 scripts/run.py stop-service`
- `python3 scripts/run.py restart-service`
- `python3 scripts/run.py service-status`
- `python3 scripts/run.py service-run` (foreground/debug)
- `python3 scripts/run.py service-run-once`

### Lifecycle helpers
- `python3 scripts/run.py setup`
- `python3 scripts/run.py doctor`
- `python3 scripts/run.py migrate-legacy-state`
- `python3 scripts/run.py cleanup-legacy-cron`

## Legacy cron cleanup

SherpaMind briefly used OpenClaw cron during refactor exploration. That is no longer the desired architecture.

`cleanup-legacy-cron` removes any old managed SherpaMind cron jobs so the system converges on the service-first model.

## Issue escalation

When install/runtime automation fails in a way that looks like a product gap, bug, or recurring operational problem, check:

- <https://github.com/kklouzal/SherpaMind/issues>

If a matching issue exists, add supporting detail.
If not, open a new issue with reproduction steps, observed behavior, expected behavior, and relevant host/runtime constraints.
Keep issue content anonymized and public-safe.

## Health checking

`doctor` should verify:
- runtime venv exists
- staged settings/secrets paths exist
- DB exists
- watch state exists
- systemd user service file exists
- service enabled/active state
- service log/state file presence
- legacy repo-local state presence (for upgrade hints)
- any leftover legacy SherpaMind cron jobs that should be cleaned up

When backend/runtime capabilities change, the skill-front/references should be reviewed in the same wave so the backend/skill/OpenClaw split remains coherent.
