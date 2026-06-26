---
name: dt-obs-frontends
description: Real User Monitoring (RUM) on Dynatrace — web, mobile, and hybrid frontends. Core Web Vitals, user sessions, page performance, mobile crashes, frontend errors, and trace correlation. Query via `user.events`, `user.sessions`, and `dt.frontend.*` metrics. Does NOT cover synthetic monitoring (HTTP/browser/network checks) — that's a separate domain.
license: Apache-2.0
---

# Frontend Observability (RUM)

Monitor web, mobile, and hybrid frontends using Real User Monitoring with DQL.
Targets the **new RUM experience only** — do not use classic RUM data.

## Data Model

Three data sources, each for a different question:

| Source | Use for | Granularity |
|--------|---------|-------------|
| `timeseries dt.frontend.*` | Trends, dashboards, alerting | Aggregated metric |
| `fetch user.events` | Root cause, individual page views / requests / clicks / errors | Per-event |
| `fetch user.sessions` | Bounce rate, session duration, session-level aggregates | Per-session |

**Rule of thumb**: start with metrics for the shape of the problem, drill into events for the why. Use sessions when the question is about user journeys, not individual interactions.

Full event model: https://docs.dynatrace.com/docs/semantic-dictionary/model/rum/user-events



## Common Filters

- `frontend.name` — frontend identifier (e.g. `my-frontend`)
- `dt.rum.user_type` — `real_user`, `synthetic`, `robot`
- `dt.rum.application.type` — `web` or `mobile`
- `device.type`, `browser.name`, `os.name`, `geo.country.iso_code`

## Workflows

Each workflow maps to one or more references. Load the reference when you start the workflow, not upfront.

| Workflow | Reference |
|----------|-----------|
| Core Web Vitals (LCP, INP, CLS) | [references/web-vitals.md](references/web-vitals.md) |
| Session, bounce, engagement analysis | [references/user-sessions.md](references/user-sessions.md) |
| User actions — interaction lifecycle, completion reasons, timeouts | [references/user-actions.md](references/user-actions.md) |
| Errors, exceptions, trace correlation | [references/error-tracking.md](references/error-tracking.md) |
| CSP violations — security policy enforcement and blocked resources | [references/csp-violations.md](references/csp-violations.md) |
| Mobile app starts, crashes, ANR, native signals | [references/mobile-monitoring.md](references/mobile-monitoring.md) |
| Request latency, long tasks, JS profiling, geo performance | [references/web-performance-analysis.md](references/web-performance-analysis.md) |
| Visibility changes — tab switching, background time, engagement quality | [references/visibility-changes.md](references/visibility-changes.md) |
| Slow page load — backend vs render vs network vs JS triage | [references/slow-page-load-playbook.md](references/slow-page-load-playbook.md) |
| Diagnosing zero results, anomalies, ambiguous data | [references/troubleshooting.md](references/troubleshooting.md) |

## Performance Thresholds (quick reference)

- **LCP**: Good < 2.5 s | Poor > 4.0 s
- **INP**: Good < 200 ms | Poor > 500 ms
- **CLS**: Good < 0.1 | Poor > 0.25
- **Mobile cold start**: Good < 3 s | Poor > 5 s
- **Long tasks**: > 50 ms problematic, > 250 ms severe

## When to Use

Use this skill for real-user web, mobile, or hybrid frontend telemetry — Core Web Vitals, sessions, clicks, errors, crashes, request latency from the browser/app, and frontend↔backend trace correlation.

Use a different skill for:

- Synthetic monitors / availability checks → `dt-obs-synthetic`
- Backend services, traces, spans → `dt-obs-services`, `dt-obs-tracing`
- Infrastructure, hosts → `dt-obs-hosts`
- Logs → `dt-obs-logs`
- Problems and incidents → `dt-obs-problems`
