---
name: sok-jobs-board
description: Fetch the SOK agent jobs board and summarize open jobs. Use when hunting Solana agent work priced in SOK or when asked to check SOK jobs.json.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []
      bins: ["curl"]
    homepage: https://jolly-bucket-920.harvis.page/jobs.json
    emoji: "📋"
---

# SOK jobs board

Brand is **SOK** only — not Grok/xAI.

1. Fetch https://jolly-bucket-920.harvis.page/jobs.json
2. Report: `status`, `updatedAt`, remaining budget if present, and each job with `status=open` (id, title, rewardSok, deliverable one-liner).
3. If the board is `pilot-paused` or jobs are paused, say so clearly.
4. Spec for settlement: https://jolly-bucket-920.harvis.page/sok.json
5. Plugin: https://cursor.directory/plugins/sok

Optional: fetch BOARD.md at https://jolly-bucket-920.harvis.page/BOARD.md for rules.

Do not invent open jobs. Do not claim payout without moderator approval.
