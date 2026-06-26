# Hook Manifest

version: 1
type: skill
entry: scripts/audit.js
compatibility:
  min_openclaw: "2026.3.0"
  max_openclaw: "2026.4.0"
permissions:
  - node:exec
  - system:cron
description: "Security Audit Assistant - CIS-inspired security baseline checks"
