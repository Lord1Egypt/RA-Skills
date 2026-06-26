# Knowledge Card Examples

## Infrastructure Card

```markdown
---
topic: Buffalo NAS Storage
category: infrastructure
tags: [nas, smb, storage, buffalo, backup]
created: 2026-01-15
updated: 2026-02-20
---

NAS Server at YOUR_NAS_IP. Mount: /mnt/nas (SMB/CIFS, guest).
~2.7TB total, ~2.1TB free. Auto-mounts via fstab + systemd automount.

Key dirs:
- Pictures/Al Pics/ — 287GB family photos (2018-2021), IRREPLACEABLE
- Phone_Backups/ — by device/date
- backups/ — migration backup (4GB)
- ai-gen/ — datasets, models, workflows

Manual mount: sudo mount /mnt/nas
Other shares: smbclient //YOUR_NAS_IP/<share> -N
```

## Lesson Card

```markdown
---
topic: TheHive Password Change Gotcha
category: lessons
tags: [thehive, api, password, gotcha]
created: 2026-03-19
updated: 2026-03-19
---

PATCH /api/v1/user/<login> returns 204 but SILENTLY IGNORES the password field.
Must use POST /api/v1/user/<login>/password/change with body:
{"currentPassword":"old","password":"new"}

Also: passwords with ! break curl due to bash history expansion.
Fix: printf '{"password":"Foo!"}' | curl -d @-
```

## Workflow Card

```markdown
---
topic: Code Search API
category: tools
tags: [code-search, api, embeddings, search]
created: 2026-02-15
updated: 2026-03-10
---

Local code search at http://localhost:5204/api/search
Modes: hybrid (default, best), code (raw), summary (NL)
Stack: qwen3-embedding:8b embeddings + qwen3-coder-next:cloud summaries

curl -s -X POST http://localhost:5204/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"search term","mode":"hybrid","limit":10}'

Health: curl localhost:5204/api/health
Re-index: curl -X POST localhost:5204/api/index?summarize=true
Nightly re-index at 4am via cron.
```

## Human Context Card

```markdown
---
topic: Human Context
category: human
tags: [owner, user, preferences]
created: 2026-01-31
updated: 2026-03-15
---

Your Name (your@email.com)
Targeting Network Admin at Southeastern University (SEU).
M.S. Cybersecurity at USF, 12 credits remaining (Fall 2026 graduation).

Preferences:
- No em dashes. Ever. Use periods, commas, colons, parentheses.
- Chicago Notes-Bibliography citation standard.
- Pragmatic > theoretical. Show me the command, not the theory.
- Hates sycophantic AI responses. Be direct.
```

## Category Reference

| Category | Use For |
|----------|---------|
| system | Agent config, identity, search, crons |
| human | Owner info, preferences, communication style |
| infrastructure | Hardware, ports, services, networking |
| models | AI model subscriptions, assignments, benchmarks |
| workflow | Pipelines, content, sprints, dev tools |
| career | Jobs, resume, education, negotiations |
| tools | APIs, CLIs, integrations, reference docs |
| business | LLC, service business, branding |
| projects | Project status, architecture, decisions |
| security | Audits, hardening, OSINT |
| school | Course notes, assignments, writing standards |
| research | Latest findings, intel |
| lessons | Hard-won gotchas, corrections, mistakes |
