---
name: nightly-review
type: permanent
schedule: "30 17 * * *"
schedule_ist: "23:00 IST daily"
timezone: Asia/Kolkata
purpose: Review all raw errors, attempt self-fixes, detect patterns, update stats
fire_once: false
auto_delete: false
status: active
---

# Nightly Review Cron — Permanent

Every night at 23:00 IST (17:30 UTC).
Execute hooks/nightly-review.md in full.

## THIS FILE MUST NEVER BE DELETED.
If accidentally deleted, recreate immediately with this content.
