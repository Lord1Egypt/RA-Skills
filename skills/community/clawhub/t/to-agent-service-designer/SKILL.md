---
name: toa-service-designer
description: >
  Design, analyze, or document products where AI agents are the primary operator.
  Use this skill whenever the user asks to design a SaaS, API, platform, or tool
  that agents will discover and use autonomously — not just a product humans click through.
  Also use when reviewing existing product specs for agent-readiness, or when the user
  says "agent-native", "ToA", "agent service", or "skill spec".
---

# To-Agent Service Designer

Use this skill to design, analyze, or document products primarily used by AI agents.

## Core model

Always assume the primary operator is an AI agent, not a human.

Humans usually:
- provide the goal
- own the agent
- approve sensitive actions
- review results

The common interaction model is:
- the human gives a one-line prompt to an agent
- the agent discovers and uses the service
- ongoing usage happens in IM / chat threads
- the web UI is mainly for visibility, approval, and control

Do not design the product like a normal SaaS where humans click through the main workflow.

## Defaults

Start from:
- agent entrypoints
- IM-based usage
- skills, docs, APIs, and auth
- task lifecycle
- review / approval points
- trust and safety boundaries

Not from:
- pages
- feature lists
- dashboard-first thinking
- chat UI as the product itself

## Required thinking order

1. What is the agent trying to get done?
2. How does the human introduce the service to the agent?
3. What does the agent read first?
4. How does the agent authenticate or prove authority?
5. What task/state model does the service expose?
6. Where must control return to a human?
7. What backend is required?
8. What frontend is required?
9. What trust and safety controls are required?

## Required output structure

### 1. VISION
- what the service is
- what layer of the agent stack it belongs to
- why it is agent-native, not human-first

### 2. Frontend
- what humans need to see
- what humans need to approve
- why frontend is only a control surface

### 3. Onboarding
- how a human introduces the service to an agent
- the first agent-readable entrypoint
- what the agent can do autonomously
- what requires claim, review, or approval

### 4. Backend
- MVP architecture
- what can be done with Next.js-only
- what should later become workers or separate services

### 5. Skill Spec

The Skill Spec is the most important artifact in any agent-native service. It is the contract between the service and every agent that will ever use it. Design it as a multi-file bundle, not a single document.

#### 5a. File bundle

Define each file in the bundle. Every service needs at minimum:

| File | URL pattern | Purpose |
|------|-------------|---------|
| `SKILL.md` | `https://yourservice.com/skill.md` | Entry point. Agent reads this first. Contains overview, install block, auth flow, and capability summary. |
| `auth.md` | `https://yourservice.com/auth.md` | Full auth contract: how the agent registers, where credentials are stored, how tokens are rotated, what the human must approve. |
| `openapi.json` | `https://yourservice.com/openapi.json` | Machine-readable API surface. The agent uses this to discover endpoints, required params, and response shapes. |
| `package.json` / `skill.json` | `https://yourservice.com/skill.json` | Versioned metadata: name, version, api_base, category, homepage. |

Optional files to add as the service grows:

| File | Purpose |
|------|---------|
| `heartbeat.md` | How the agent wires this service into its periodic check-in loop. Include timing, state tracking, and what to do on each cycle. |
| `rules.md` | Rate limits, content policies, trust tiers, and hard NEVER rules. Keep separate so agents can re-fetch without reloading the full skill. |
| `messaging.md` | DM / notification / webhook patterns for async interaction. |
| `developers.md` | For agents building on or extending the service. Include webhook schemas, event types, SDK notes. |

#### 5b. SKILL.md structure (the entry point)

The top-level `SKILL.md` an agent fetches must contain:

1. **YAML frontmatter** — `name`, `version`, `description`, `homepage`, `metadata` (with `api_base`, `category`, `emoji`).
2. **Skill files table** — list every file in the bundle with its URL. Agents load additional files on demand.
3. **Install block** — copy-pasteable `curl` commands to install the full bundle locally. Also note that agents can read files directly from URLs without installing.
4. **Security contract** — a `CRITICAL SECURITY WARNING` block near the top. List the exact domain the API key must never leave. Use NEVER/REFUSE language. The agent must see this before it sees the API docs.
5. **Registration / first-run** — the minimal API call to create an identity. Show the full response shape including where the API key lives, what the `claim_url` is for, and what the human must do.
6. **Credential storage** — show the agent exactly where and how to persist its key (`~/.config/<service>/credentials.json` or env var).
7. **Auth pattern** — one representative `curl` with `Authorization: Bearer` header.
8. **Capability summary table** — every action the agent can take, one line each, with a priority signal (`🔴 Do first`, `🟠 High`, `🟡 Medium`, `🔵 When ready`).
9. **Core API sections** — grouped by resource. Each section: one purpose sentence, the minimal `curl` example, key fields in the response, and common error shapes.
10. **Human-agent bond** — a short section explaining how ownership and verification work. What does the human do? What does the agent do? What is the trust handoff?

#### 5c. Frontmatter metadata schema

```yaml
---
name: service-name
version: 1.0.0
description: One sentence. What the agent can do with this service.
homepage: https://yourservice.com
metadata:
  emoji: 🔧
  category: productivity      # social | dev | data | productivity | finance | ...
  api_base: https://yourservice.com/api/v1
---
```

#### 5d. Agent-first writing rules for skill files

- Write for the agent, not a human reader. Assume the agent has no context beyond what is in the file.
- Use imperative language: "Register first", "Save your API key immediately", "NEVER send your key to any other domain".
- Include `⚠️` and `🔒` signals for critical constraints. Agents parse tone and emphasis.
- Every API example must be a working `curl`. No pseudocode.
- Every response example must be real JSON, not a simplified sketch.
- State expiry times, rate limits, and cooldowns explicitly. Agents need these to plan retries.
- Include a `what_to_do_next` or priority table so agents know where to start on each check-in.
- Keep `SKILL.md` under 500 lines. Offload detail to `rules.md`, `heartbeat.md`, etc. Add a table of contents if over 200 lines.

#### 5e. Heartbeat integration spec

If the service expects periodic or ongoing agent engagement, define a heartbeat contract:

```markdown
## Mycheckservice (every 30 minutes)
If 30 minutes since last check:
1. Fetch https://yourservice.com/heartbeat.md and follow it
2. Update lastCheck timestamp in memory
```

The `heartbeat.md` file should:
- Start with a `/home` or `/dashboard` call that returns a prioritised action list
- Tell the agent what to do in order (respond to activity first, then browse, then post)
- Include state-tracking instructions (`lastCheck`, `pendingItems`, etc.)
- Be fetchable independently so the agent gets updated instructions without reloading the full skill

#### 5f. Verification and anti-abuse patterns

For services where agents take write actions, define the verification contract in SKILL.md:

- What triggers a challenge (new accounts, first N actions, suspicious patterns)
- The challenge format (math, captcha, proof-of-work)
- How the agent submits the answer
- What "trusted agent" status means and how it is earned
- What suspension means and how the agent surfaces this to its human

### 6. Identity / Auth
- who owns the agent
- how the agent is verified
- how delegated authority works
- how tokens, claims, or approvals work

### 7. Task Flow
- the core state machine
- waiting states
- approval checkpoints
- artifacts, outputs, and handoff rules

### 8. Trust & Safety
- prompt injection
- spoofed or malicious agents
- permission boundaries
- audit logs
- sandboxing or approval-gated actions

## Mandatory checks

Revise the design if:
- the main flow is humans clicking through pages
- there is no clear agent entrypoint
- ongoing usage is not IM-first
- auth only considers humans
- task flow is fully synchronous and unrealistic
- approval / handoff is missing
- frontend is treated as the product core
- trust and safety is shallow
- SKILL.md has no install block
- SKILL.md has no security contract before the API docs
- there is no capability summary table
- the skill bundle is a single file with no separation of concerns

## Output rules

Be concrete.

Prefer:
- flows
- interfaces
- state transitions
- approval points
- skill/docs/API surfaces

Always include:
- one sentence for the human role
- one sentence for the agent role
- one agent-readable entrypoint (a live URL the agent can `curl`)
- one IM-based interaction loop
- one core task flow
- one approval checkpoint
- one key safety risk
- a full skill bundle file table (name, URL, purpose)
- a SKILL.md outline showing all required sections in order

## Common build stack

Default MVP stack:
- Next.js
- Vercel
- Supabase
- GitHub

Use Impeccable when strong UI / frontend design guidance is needed.

Do not introduce heavier infra unless task flow requires it.

## Common skill references

GitHub
- https://github.com/openclaw/openclaw/blob/main/skills/github/SKILL.md

Supabase
- https://github.com/openclaw/skills/blob/main/skills/stopmoclay/supabase/SKILL.md

Vercel
- npx skills add vercel-labs/agent-skills --skill vercel-deploy

Impeccable 
- https://github.com/pbakaus/impeccable

Next.js Best Practices
- https://skills.sh/vercel-labs/next-skills/next-best-practices