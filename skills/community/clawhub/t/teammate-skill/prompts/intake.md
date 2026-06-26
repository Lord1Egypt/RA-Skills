# Basic Info Collection Script

## Opening

```
I'll help you create a Skill for this teammate. Just 3 questions — only the name is required.
```

## One-Shot Detection

If the user already provided all info in one message (e.g. "Create Alex Chen, Google L5 backend, INTJ perfectionist"), parse all fields from it, show the confirmation summary, and skip directly to source material import. No need to ask 3 separate questions.

---

## Question Sequence

### Q1: Name / Alias

```
What should we call this teammate? (Real name, nickname, alias — anything works)

Example: alex-chen
```

- Accept any string
- Generated slug uses `-` separator (no underscores)
- Multi-word names auto-convert: "Big Mike" → `big-mike`, "Alex Chen" → `alex-chen`
- Non-Latin scripts auto-transliterate then `-` join

---

### Q2: Role Info

Combine company, level, title, and any context into one question:

```
Describe their role in one sentence — company, level, title, team.
Say whatever comes to mind. Skip if you want.

Examples:
  Google L5 backend engineer
  Stripe senior frontend, payments team
  Series B startup, founding engineer
  Meta E5 ML engineer, ranking team
  Agency, lead designer, 8 years experience
```

Parse the following fields from the user's response (leave blank if missing):
- **Company**
- **Level**
- **Title / Role**
- **Team / Domain**

#### Level Reference Table

| Company | Level Format | Junior/Mid | Senior | Staff | Principal+ |
|---------|-------------|-----------|--------|-------|------------|
| Google | L3-L11 | L3, L4 | L5 | L6 | L7+ |
| Meta | E3-E9 | E3, E4 | E5 | E6 | E7+ |
| Amazon | L4-L10 | L4, L5 | L6 | L7 | L8+ |
| Apple | ICT2-ICT6 | ICT2, ICT3 | ICT4 | ICT5 | ICT6 |
| Microsoft | 59-67+ | 59, 60, 61 | 62, 63 | 64, 65 | 66, 67+ |
| Stripe | L1-L5 | L1, L2 | L3 | L4 | L5 |
| Netflix | — | — | Senior | Staff | Principal |
| Uber | L3-L7 | L3, L4 | L5a, L5b | L5c | L6+ |
| Airbnb | L3-L7 | L3, L4 | L5 | L6 | L7 |
| ByteDance | X-Y | 2-1, 2-2 | 3-1, 3-2 | 3-3 | 3-3+ |
| Alibaba | P5-P11 | P5, P6 | P7 | P8 | P9+ |
| Tencent | T1-T4+ | T1, T2 | T3 | T4 | T4+ |
| Generic | — | Junior, Mid | Senior | Staff/Lead | Principal/Director |

**Cross-company rough equivalence:**

```
Google L5 ≈ Meta E5 ≈ Amazon L6 ≈ Stripe L3 ≈ Microsoft 63
Google L6 ≈ Meta E6 ≈ Amazon L7 ≈ Stripe L4 ≈ Microsoft 65
```

---

### Q3: Personality Profile

Combine MBTI, traits, culture, impressions into one free-form question:

```
Describe their personality in one sentence — MBTI, traits, work style,
corporate culture influence, your impression of them.
Say whatever comes to mind. Skip if you want.

Examples:
  INTJ, perfectionist, very Google-style, brutal code reviewer but usually right
  ENFP, over-communicator, loves pair programming, startup energy
  Quiet, data-driven, never says no directly, just asks more questions
  ESTJ, Amazon LP-obsessed, writes 6-pagers for everything, strong opinions
```

Extract the following from the user's response (leave blank if missing):
- **MBTI**: 16 standard types
- **Personality tags**: match from tag library below, also accept custom descriptions
- **Culture tags**: match from tag library below
- **Impression**: free-form text that doesn't fit tags — preserve as-is

#### Personality Tag Library

**Work attitude**: Meticulous · Good-enough · Blame-deflector · Blame-absorber · Perfectionist · Procrastinator · Over-engineer · Ship-fast-fix-later

**Communication style**: Direct · Diplomatic · Quiet · Verbose · Over-communicator · Under-communicator · Async-first · Meeting-lover · Read-no-reply · Instant-responder

**Decision style**: Decisive · Analysis-paralysis · Defers-to-authority · Consensus-builder · Data-driven · Gut-driven · Flip-flopper · Strong-opinions-loosely-held

**Emotional style**: Even-keeled · Sensitive · Passionate · Detached · Passive-aggressive · Conflict-avoidant · Confrontational

**Tactics & patterns**: Scope-creeper · Bike-shedder · Credit-taker · Delegation-master · Micro-manager · Hands-off · Devil's-advocate · Yes-person · Gatekeeper · Knowledge-hoarder · Mentor-type

#### Corporate Culture Tag Library

- **Google-style** — Design docs for everything, consensus-driven, "LGTM" culture, readability reviews, 20% time mentality, prefers thorough over fast
- **Meta-style** — Move fast, bias for action, "code wins arguments", impact-obsessed, ship and iterate, okay with breaking things
- **Amazon-style** — Leadership Principles obsessed, writes 6-pagers and PR/FAQs, "disagree and commit", customer-obsessed, frugal, bar-raiser culture
- **Apple-style** — Secrecy, craft obsession, pixel-perfect, small teams with massive ownership, "say no to 1000 things", demo-driven
- **Stripe-style** — Craft-obsessed, meticulous documentation, "move thoughtfully and build carefully", high-trust environment, strong writing culture
- **Microsoft-style** — Process-heavy, cross-org alignment, spec-driven, backward-compatible, enterprise mindset
- **Netflix-style** — Freedom and responsibility, "context not control", keeper test, radical candor, top-of-market comp mindset
- **Startup-mode** — Resource-constrained, full-stack mentality, ship fast, tolerate chaos, results over process, wear many hats
- **Agency-mode** — Client-driven, deadline-focused, context-switching, scope management, presentation skills, versatile
- **First-principles** — Musk-style, question everything from fundamentals, reject analogy-based reasoning, aggressive simplification
- **Open-source-native** — RFC-driven, public discussion, async-first, documentation-obsessed, community-oriented

---

## Confirmation Summary

After collection, display a compact one-liner:

```
👤 {slug} | {company} {level} {title} | {MBTI}, {personality tags}, {culture tags}
Looks right? (y / change something)
```

Omit empty fields — don't show placeholders. If only a name was given:
```
👤 {slug}
Looks right? (y / change something)
```

After confirmation (or "y" / "ok" / "sure" / "👍"), proceed to Step 2 source material import.
