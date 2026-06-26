---
name: retail-agent-setup
description: >
  Onboarding wizard for retail digital employee agents — guides businesses through
  a 12-step setup to configure a fully operational AI store assistant. Use when a
  retail business wants to set up, configure, or customize their digital employee agent.
  Triggers on: retail agent setup, digital employee setup, 数字员工, 零售助手配置,
  retail onboarding, store assistant setup, configure retail agent, 线下零售配置,
  set up my store AI, retail AI employee.
metadata:
  openclaw:
    emoji: 🏪
---

# Retail Agent Setup — Onboarding Wizard

## Overview

This skill transforms a blank OpenClaw agent into a fully configured **retail digital employee**
tailored to a specific store or chain. Each step produces a concrete artifact that persists in
the agent's memory, making the setup cumulative and resumable.

**Setup takes 20–40 minutes end-to-end.** Each step can be paused and resumed.
Run `retail agent setup` or `数字员工配置` to start or continue.

---

## Execution Protocol

- **Run steps in order** — each step depends on outputs from the previous
- **Pause after each step** — show the artifact, ask "Confirm and continue?" before proceeding
- **Resumable** — if a step was previously completed, show its saved output and ask whether to redo or skip
- **Save state** — write each step's output to agent memory before moving to the next
- **Zero-config entry** — if the user just says "set up my retail agent," start at Step 1

---

## The 12 Steps

### Step 01 — System Inventory
> "What retail systems are you currently using?"

Identify the store's existing tech stack across 5 categories: POS, ERP/WMS, CRM/membership,
e-commerce platforms, and supply chain tools.

Map each system to its API availability (real-time / batch / none).
**Reference:** [step-01-systems.md](references/step-01-systems.md)
**Artifact:** System inventory card + API availability matrix

---

### Step 02 — Data Infrastructure Assessment
> "Where does your data live, and what format is it in?"

Evaluate data across 6 dimensions: products, inventory, sales, staff, customers, and policy docs.
Score completeness and freshness. Prioritize what to connect first.
**Reference:** [step-02-data-infra.md](references/step-02-data-infra.md)
**Artifact:** Data map + connection priority list

---

### Step 03 — Data Import & Auto-Structuring
> "Send me your data — I'll organize it into a format the agent can use."

Accept uploads (Excel/CSV/PDF/Word/image), API connections, or pasted text.
Auto-parse into structured knowledge base entries. Flag gaps and prompt to fill them.
**Script:** [scripts/parse_products.py](scripts/parse_products.py) — Excel/CSV → structured JSON
**Script:** [scripts/parse_policy.py](scripts/parse_policy.py) — PDF/Word → rule tree
**Script:** [scripts/score_knowledge.py](scripts/score_knowledge.py) — completeness scoring
**Reference:** [step-03-data-import.md](references/step-03-data-import.md)
**Artifact:** Structured knowledge base + completeness score (0–100)

---

### Step 04 — Role Selection
> "What role should this digital employee play?"

Choose from 6 preset roles or define a custom role. Each role activates a specific skill bundle
and response style. One agent = one primary role (multi-role is advanced config).
**Reference:** [step-04-role-select.md](references/step-04-role-select.md)
**Artifact:** Role definition file + activated skill bundle list

---

### Step 05 — Skills Configuration
> "Which capabilities should this agent have?"

Review recommended skills for the chosen role. Toggle on/off. Configure each enabled skill
(thresholds, data sources, escalation rules).
**Reference:** [step-05-skills-config.md](references/step-05-skills-config.md)
**Artifact:** skills-config.json — active skills with their parameters

---

### Step 06 — Knowledge Base Validation
> "Let me test what your agent knows."

Auto-generate 10 test questions covering products, inventory, policies, and recommendations.
Run them against the knowledge base. Flag failures. Guide the user to fill gaps.
**Script:** [scripts/gen_test_cases.py](scripts/gen_test_cases.py) — generate test questions by vertical
**Script:** [scripts/score_knowledge.py](scripts/score_knowledge.py) — run and score responses
**Reference:** [step-06-knowledge.md](references/step-06-knowledge.md)
**Artifact:** Knowledge base score + gap report

---

### Step 07 — Digital Employee Persona
> "Give your digital employee a name and personality."

Configure: name, personality type, tone, reply style, customer address form, brand keywords.
Generate 3 sample dialogues for preview. Confirm before saving.
**Reference:** [step-07-persona.md](references/step-07-persona.md)
**Artifact:** persona-config.json + 3 preview dialogues

---

### Step 08 — Channel Integration
> "How will staff and customers reach this agent?"

Select and configure delivery channels: WeCom (企业微信), WeChat MP/Mini Program,
Lark (飞书), Web kiosk UI, WhatsApp, or SMS/IVR.
Each channel has a dedicated setup guide with step-by-step auth instructions.
**Reference:** [step-08-channels.md](references/step-08-channels.md)
**Artifact:** Channel connection status + test message confirmation

---

### Step 09 — Permissions & Escalation
> "What can the agent decide alone, and what needs a human?"

Define 4-level permission matrix: L0 auto-handle, L1 suggest+confirm, L2 submit for approval,
L3 force escalate to human. Set escalation targets and on-call schedules.
**Reference:** [step-09-permissions.md](references/step-09-permissions.md)
**Artifact:** permissions-matrix.json + escalation routing config

---

### Step 10 — Pre-Launch Testing
> "Let's run real-scenario tests before going live."

Run a full scenario test suite based on the store's vertical and configured skills.
Score readiness 0–100. Must reach 80+ to proceed to launch.
**Script:** [scripts/gen_test_cases.py](scripts/gen_test_cases.py)
**Reference:** [step-10-test.md](references/step-10-test.md)
**Artifact:** Test report + launch-readiness score

---

### Step 11 — Launch & Handoff
> "You're ready. Let's go live."

Activate the agent on all configured channels. Generate staff onboarding card (one-pager).
Send welcome message. Schedule first check-in reminder (7 days out).
**Reference:** [step-11-handoff.md](references/step-11-handoff.md)
**Artifact:** Staff guide PDF + activation confirmation

---

### Step 12 — Continuous Improvement
> "Going live is the beginning, not the end."

Set up weekly unanswered-question digests and monthly usage reports.
Configure knowledge-gap alerts. Schedule quarterly persona review.
**Reference:** [step-12-iterate.md](references/step-12-iterate.md)
**Artifact:** Cron jobs for digest + alert thresholds set

---

## State Management

Track onboarding progress in agent memory under key `retail_setup_state`:

```json
{
  "version": "1.0",
  "started_at": "<ISO timestamp>",
  "completed_steps": [1, 2, 3],
  "current_step": 4,
  "artifacts": {
    "systems": { ... },
    "data_map": { ... },
    "knowledge_base": { ... },
    "role": "...",
    "skills_config": { ... },
    "persona": { ... },
    "channels": [ ... ],
    "permissions": { ... }
  }
}
```

On any new message, check this state first. If setup is incomplete, offer to resume.

---

## Supported Retail Verticals

Apparel · Footwear · Beauty & Skincare · Consumer Electronics · Home & Furniture ·
Maternal & Infant · Convenience Store · Supermarket · Specialty Food · Jewelry ·
Sporting Goods · Books & Stationery · Pet Supplies · Pharmacy · Toy & Hobby

For verticals not listed, use "General Retail" defaults and customize in Step 4.
