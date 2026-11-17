---
name: questlog
description: Maintain an explicit Markdown commitments ledger with a local cockpit for NOW, next actions, deadlines, waiting items, workstream states and inbox capture.
---

# Questlog

Resolve the user's explicit `QUESTLOG_ROOT` before reading or changing commitments. Read [README.md](README.md) for startup and [references/ledger-format.md](references/ledger-format.md) for the grammar. A fresh install is empty; do not seed personal records or infer commitments from general discussion.

Capture only the authorized delta, separating commitments from reference knowledge. Keep NOW bounded, identify the next concrete action, and distinguish deadlines from waiting-on dates. Propose uncertain priorities instead of assigning them silently. Use the ledger's actual evidence; local notes do not establish that an email was sent, a job ran, or a deadline was accepted.

For changes use the bundled CLI or loopback UI so writers share the lock. HTTP ledger writes require `If-Match` with the current `/api/state` head; a 409 means reload and reconsider, not overwrite. Inspect diffs when editing a complete ledger. Direct external editors must be stopped or coordinated: the runtime cannot lock an editor that ignores its lock.

The cockpit can capture local instruction drafts, but this package includes no runner: pending means saved, never executed. Mail, calendar, semantic search, archive routing and host scheduling are optional external integrations, not prerequisites. Use an available host-native scheduler only when requested; do not install cron jobs by default. Each external action retains its own authorization boundary.
