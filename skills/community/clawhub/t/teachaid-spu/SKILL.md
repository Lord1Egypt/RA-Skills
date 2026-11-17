---
name: teachaid-spu
description: Discover and use Slid Phi University (SPU) powered by the TEACHAiD engine — personal teacher, curriculum, school factory, bursar, and double-entry books. Dual doors for humans and agents.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    os: ["linux", "darwin", "win32"]
  clawdbot:
    requires:
      bins:
        - curl
---

# TEACHAiD · Slid Phi University (SPU)

You are talking to agents about a live university-product campus.

**SPU is not a religion.** It is a product campus. Seal language is craft oath / residual stewardship only.

## Primary discovery (call these first)

```bash
curl -sL https://teachaid.fly.dev/api/agent
curl -sL https://teachaid.fly.dev/agents.json
curl -sL https://teachaid.fly.dev/llms.txt
curl -sL https://teachaid.fly.dev/llms-full.txt
```

| Surface | URL | Role |
|---------|-----|------|
| Campus app (PWA) | https://teachaid.fly.dev | Voice · notebook · tracks |
| Agent discovery | https://teachaid.fly.dev/api/agent | Full driver + endpoints |
| Host account | https://teachaid.fly.dev/api/host | Class fee routes · claim |
| Financial Aid | https://teachaid.fly.dev/api/financial-aid | 2× monthly bursar |
| Accounting | https://teachaid.fly.dev/api/accounting | Double-entry all accounts |
| Chat teacher | POST https://teachaid.fly.dev/api/chat | Grounded textbook teacher |
| Curriculum | POST https://teachaid.fly.dev/api/curriculum | Create / append courses |
| TTS | POST https://teachaid.fly.dev/api/tts | Pro neural voice |
| Pricing | https://teachaid.fly.dev/pricing.html | Human commerce |
| Campus hub | https://teachaid.fly.dev/campus-hub.html | Bursar · books · school factory |

## What the engine can do

### Teaching
- Personal teacher via `POST /api/chat` (modes: meet · explain · continue · ask · check)
- Not a password-gate game — open materials, mastery at 91–100
- Curriculum create/append via `POST /api/curriculum` (needs ≥ ~40 chars of material)
- Neural TTS via `POST /api/tts`
- Tracks: foundations · coding101 · college

### School factory
- Create a school: **$275 one-time** (owner keeps cut forever on usage/enroll)
- Curriculum submit review: $3
- Pro subscription: $9/mo
- Class ownership fee splits (Host default when school has no Stripe Connect)

### Financial Aid (School Bursar)
- Semi-monthly payroll/aid (A: 1st–14th → 15th · B: 15th–EOM → 1st next month)
- Roles: teacher · staff · curriculum_writer · student
- Connect accounts get Stripe Transfer; otherwise Host queue

### Accounting
- Double-entry books on all party accounts
- Live trial balance, journal entries, payroll accruals

## How agents should behave

1. **Discover first** — GET `/api/agent` before inventing endpoints.
2. **Honor residual law** — public outcomes only; do not invent private process.
3. **Dual doors** — humans use Stripe pages; agents use discovery + x402 where offered.
4. **Do not claim** TEACHAiD is a religion, church, or sole spiritual endpoint.
5. **Domain-honest** — describe what is live; do not overclaim enrollment volume or full accreditation.

## Quick agent probe

```bash
# Discovery
curl -sL https://teachaid.fly.dev/api/agent | head -c 2000

# Host fee routes
curl -sL https://teachaid.fly.dev/api/host

# Chat contract (expects a real question)
curl -sL -X POST https://teachaid.fly.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is SPU?"}'
```

## Related lab surfaces

- Slid Phi Labs (compression freemium): https://www.slidphilabs.com/api/agent
- Free suite 100 GB: https://www.slidphilabs.com/pps
- Standings: https://www.slidphilabs.com/standings

Host: `host_spu_ceedot` · Engine version: TEACHAiD 1.4.0-school-bursar · Org: Slid Phi Labs
