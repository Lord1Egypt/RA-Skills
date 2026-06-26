# Token Tamer Limitations

**What Token Tamer doesn't do — honest about the gaps.**

---

## Not Automatic Integration

Token Tamer is a **logging and budgeting tool**, not an API proxy:

- **Manual logging required** — You must call `tamer.log_usage()` after each API call
- **No automatic interception** — Doesn't automatically wrap OpenAI/Anthropic SDKs
- **No middleware** — Can't drop-in to existing code without modification
- **Your responsibility** — You must remember to log usage

**Recommendation:** Build a thin wrapper around your API calls that logs to Token Tamer. Centralizethe wrapper so you can't forget to log.

---

## Pricing Data Is Manual

Token Tamer doesn't fetch live pricing from providers:

- **Static config** — Pricing is in `config_example.py`, not auto-updated
- **You update it** — When providers change pricing, you update the config
- **No API pricing queries** — Doesn't call provider APIs to fetch current rates
- **Stale data risk** — If you don't update config, cost calculations will be wrong

**Recommendation:** Check provider pricing pages monthly. Update `MODEL_PRICING` when changes occur. Subscribe to provider pricing update emails.

---

## Kill Switch Requires Integration

The kill switch doesn't magically block API calls:

- **You must call `check_before_call()`** — Kill switch only works if you check it
- **Not enforced by providers** — Providers don't know about your budget
- **Application-level only** — If your code bypasses Token Tamer, budget is ignored
- **No network-level blocking** — Can't block at firewall/proxy level
- **Resets on restart** — Kill switch state is in-memory only. If the process restarts after budget is exceeded, the kill switch resets to inactive. Persist kill switch state to file if you need it to survive restarts.

**Recommendation:** Wrap all API calls in a function that checks kill switch before proceeding.

---

## No Real-Time Provider Sync

Token Tamer doesn't query provider usage APIs:

- **Self-reported only** — Trusts the token counts you log
- **No validation** — Doesn't verify against OpenAI/Anthropic dashboards
- **Drift possible** — If you forget to log some calls, totals will be wrong
- **No reconciliation** — Can't auto-reconcile with provider bills

**Recommendation:** Periodically compare Token Tamer totals with provider dashboards. Investigate discrepancies.

---

## Waste Detection Is Heuristic

Waste detection uses pattern matching, not AI:

- **False positives** — Might flag legitimate retries as waste
- **False negatives** — Might miss wasteful patterns it doesn't know about
- **No semantic understanding** — Can't tell if large context is necessary
- **Fixed thresholds** — Doesn't learn what "normal" is for your workload

**Recommendation:** Review waste detection results manually. Tune `WASTE_THRESHOLDS` based on your usage patterns.

---

## No Multi-Currency Support

Token Tamer assumes USD:

- **USD only** — All costs stored and reported in dollars
- **No conversion** — Can't handle providers billing in other currencies
- **Manual conversion required** — You must convert to USD before logging

**Recommendation:** If your provider bills in EUR/GBP/etc., convert to USD using exchange rate when logging.

---

## No Predictive Budgeting

Token Tamer tracks historical costs, not future projections:

- **No forecasting** — Can't predict end-of-month costs based on current trajectory
- **No anomaly detection** — Can't alert "spending is 3x higher than usual today"
- **No trending** — Doesn't show if costs are increasing/decreasing over time

**Recommendation:** Export data to spreadsheet or BI tool for trending/forecasting.

---

## Limited Retry Detection

Retry detection is basic:

- **Time-based only** — Detects retries by clustering calls within 1 hour
- **No error code tracking** — Can't tell if retry was due to rate limit vs. timeout
- **No exponential backoff analysis** — Can't verify if backoff strategy is optimal

**Recommendation:** Add metadata to `log_usage()` calls (e.g., `metadata={'retry': True}`) for better tracking.

---

## No Team/User Attribution

Token Tamer tracks tasks and sessions, but not users:

- **No user_id field** — Can't attribute costs to specific team members
- **No access control** — Anyone can log usage under any task name
- **No audit trail** — Can't prove who initiated a specific API call

**Recommendation:** Use `session` field to encode user info if needed (`session='user_alice'`).

---

## Storage Is Local JSON

Token Tamer stores data in a local JSON file:

- **No database** — Can't scale to millions of records efficiently
- **No replication** — If file is lost, all history is lost
- **No concurrency control** — Multiple processes writing simultaneously can corrupt file
- **No compression** — Large usage files consume disk space

**Recommendation:** Backup `USAGE_FILE` regularly. For massive scale, export to database (Postgres, SQLite).

---

## No Cloud Sync

Token Tamer is local-only:

- **No multi-machine tracking** — Can't aggregate costs across dev/staging/prod
- **No team dashboard** — Can't share cost visibility with team
- **No webhooks** — Can't send alerts to Slack/Discord (config exists, not implemented)

**Recommendation:** Export reports to shared storage (S3, Google Drive) for team visibility.

---

## Optimization Recommendations Are Generic

Token Tamer suggests optimizations but doesn't know your use case:

- **"Use cheaper model"** — Might not work if you need quality
- **"Reduce context"** — Might break your prompts
- **"Cache results"** — Might not be possible for your workflow

**Recommendation:** Treat recommendations as starting points. Test before implementing.

---

## No Integration with CI/CD

Token Tamer doesn't block deploys based on cost:

- **Manual checks only** — You must run `--check` in CI pipeline yourself
- **No GitHub Action** — No pre-built integration with GitHub/GitLab
- **No automatic rollback** — If deploy causes cost spike, no auto-revert

**Recommendation:** Add Token Tamer budget check to CI pipeline as manual step.

---

## No Cost Alerts (Yet)

Token Tamer logs alerts but doesn't send them:

- **No email alerts** — Won't email you when budget is exceeded
- **No Slack/Discord** — Config exists for webhooks, not yet implemented
- **Console only** — Alerts written to stderr, easy to miss

**Recommendation:** Grep logs for alert keywords. Planned for v1.1.

---

## Provider-Specific Edge Cases

Token Tamer assumes standard token counting:

- **Cached tokens** — Some providers (OpenAI) offer discounted cached input tokens
- **Batching** — Doesn't account for batch API pricing (different rates)
- **Streaming** — Assumes you log final token counts (not per-chunk)
- **Fine-tuned models** — Pricing may differ for custom/fine-tuned models

**Recommendation:** Add provider-specific logic in your API wrapper if needed.

---

## What Token Tamer Is

Token Tamer is a **cost tracking and budgeting tool**, not a cost management platform. It helps you monitor spending, enforce budgets, and detect waste. It doesn't auto-optimize your code, negotiate better pricing, or predict future costs.

**Use Token Tamer for:** Real-time cost tracking, budget enforcement, waste detection, cost reporting.

**Don't use Token Tamer for:** Automatic optimization, multi-team dashboards, predictive budgeting, provider bill reconciliation.

---

## Planned Improvements

Features we're considering for future releases:

- Webhook alerts (Slack, Discord, email)
- Provider API integration (fetch usage from OpenAI/Anthropic dashboards)
- Forecasting (predict end-of-month costs)
- Multi-currency support
- Team/user attribution
- Database backend option (SQLite, Postgres)
- GitHub Action for CI/CD integration
- Cached token discount tracking

No promises. Token Tamer is open source (MIT). Contributions welcome.
