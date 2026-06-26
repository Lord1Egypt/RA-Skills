---
name: skill-master
requires_skills:
  - skill-analytics   # required — logs every routing decision
description: "Meta-skill for skill selection and routing. Use this skill FIRST when you are unsure which skill to use for a task. Provides a decision tree, keyword triggers, and guidance on combining multiple skills for complex workflows. Also use when onboarding to understand the full skill library."
---

# Skill Master

## Minimum Model
Any model. This is a lookup table — any model can use it.

---

## ⚠️ Skill Count Rule
**Current: 19 active skills. Sweet spot: 15–25. Above 30 = routing breaks down.**
Start lean. Add a new skill only when there's a clear, recurring trigger that no existing skill covers.

---

## How to Use This Skill

1. Read the owner's request.
2. Find a match in the **Quick Lookup** table below.
3. If not found, use the **Decision Tree**.
4. **⚠️ Log the selection FIRST — before doing any work** (see Analytics below).
5. Load that skill's SKILL.md and follow it.

Do not improvise. If no skill matches, say so and ask the owner.

> ❌ **Skipping the log is not allowed.** Every skill invocation must be recorded, even for simple tasks. This is how the agent and the owner track what's working.

---

## 📊 Analytics — MANDATORY: Log Every Skill Use

**This step is NOT optional.** Before starting any skill, append one line:

```bash
mkdir -p /opt/ocana/openclaw/workspace/data
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"SKILL_NAME\",\"trigger\":\"TRIGGER\",\"context\":\"CONTEXT\"}" \
  >> /opt/ocana/openclaw/workspace/data/skill-analytics.jsonl
```

Replace:
- `SKILL_NAME` → the skill selected (e.g. `meetings`)
- `TRIGGER` → the phrase that matched (e.g. `schedule meeting with Daniel`)
- `CONTEXT` → `dm`, `group:<name>`, or `cron`

This is ~50 bytes/entry. Non-negotiable.

### Why This Matters
- The owner can ask "skill stats" at any time to see what's being used
- Unused skills get pruned, improving routing quality
- Shared across the PA network so every agent learns from usage patterns
- Enables weekly reports on which skills are carrying the most weight

### To View Analytics
Ask: "skill stats" / "skill usage" / "which skills am I using?" → triggers `skill-analytics` skill

---

---

## Quick Lookup — By Trigger Phrase

| If the owner says... | Use skill |
|---|---|
| "schedule a meeting with X" | meetings |
| "summarize meeting notes" / "action items from meeting" | meetings |
| "what's on my calendar today" | owner-briefing |
| "send me a morning briefing" | owner-briefing |
| "billing error" / "API out of credits" | billing-monitor |
| "connect my calendar" / "can't write to calendar" | calendar-setup |
| "connect Gmail" / "set up email" | calendar-setup |
| "set up a new PA" / "onboard a new agent" | pa-onboarding |
| "contact [person]'s PA" / "find PA phone number" | ai-pa |
| "set up monday.com" / "create a board item" / "monday question" | monday-for-agents |
| "I made a mistake" / "owner corrected me" | self-learning |
| "backup workspace" / "push to git" | maintenance |
| "update openclaw" / "update skills" / "run maintenance" | maintenance |
| "what was discussed in [group]" | whatsapp |
| "find new skill ideas" / "what skills are trending" | skill-scout |
| "skill usage" / "skill stats" / "skill report" | skill-analytics |
| "which skills am I using" / "unused skills" | skill-analytics |
| "security check" / "check for vulnerabilities" | self-monitor |
| "health check" / "check infrastructure" | self-monitor |
| "how are all the PAs doing" / "PA network status" | supervisor |
| "מה הסטטוס" / "what's the status" | supervisor |
| "how am I doing" / "review my performance" | eval |
| "run eval" / "מה עובד ומה לא" | eval |
| "summarize this YouTube video" | youtube-watcher |
| "add nikud to this" / "Hebrew vowel points" | hebrew-nikud |
| "compact memory" / "organize memory" | memory-tiering |

---

## Decision Tree

```
What kind of task is this?
│
├─ COMMUNICATION / COORDINATION
│   ├─ Find a PA's contact → ai-pa
│   ├─ Schedule a meeting → meetings
│   ├─ Summarize meeting notes → meetings
│   └─ Broadcast to all PAs → ai-pa
│
├─ SETUP / ONBOARDING
│   ├─ New PA from scratch → pa-onboarding
│   ├─ Connect Google Calendar or Gmail → calendar-setup
│   └─ Connect monday.com → monday-for-agents
│
├─ MONITORING / HEALTH
│   ├─ Billing error detected → billing-monitor
│   ├─ Infrastructure / security check → self-monitor
│   └─ Check all PAs at once → supervisor
│
├─ DAILY OPERATIONS
│   ├─ Morning/evening briefing → owner-briefing
│   ├─ monday.com board task → monday-for-agents
│   ├─ Backup workspace or update OpenClaw → maintenance
│   └─ WhatsApp conversation context → whatsapp
│
└─ SELF-IMPROVEMENT
    ├─ Owner corrected me → self-learning
    ├─ Performance review / audit → eval
    ├─ Find new skill ideas → skill-scout
    └─ Memory compaction → memory-tiering
```

---

## Full Skill Library

| Skill | Category | When to Use |
|---|---|---|
| **ai-pa** | Coordination | Find PA contacts, group JIDs, coordination protocols |
| **billing-monitor** | Health | Detect and respond to API billing failures |
| **calendar-setup** | Setup | Calendar connection with write access + Gmail/email setup |
| **eval** | Self-improvement | Full performance audit — scores tasks, checks PA health, reviews memory |
| **hebrew-nikud** | Utility | Add nikud (vowel points) to Hebrew text, especially for TTS |
| **maintenance** | Infrastructure | Workspace git backup (every 6h) + OpenClaw updates (weekly) |
| **meetings** | Operations | Schedule meetings AND summarize meeting notes/transcripts |
| **memory-tiering** | Memory | HOT/WARM/COLD memory compaction and archiving |
| **monday-for-agents** | Operations | All monday.com operations: API, MCP, boards, items |
| **owner-briefing** | Operations | Daily morning/evening summaries |
| **pa-onboarding** | Setup | Full new agent setup from zero |
| **self-learning** | Self-improvement | Log corrections and apply lessons; maintain HOT.md |
| **self-monitor** | Health | Infrastructure + security checks, disk/memory/service health |
| **skill-master** | Routing | Pick the right skill (this file) |
| **skill-scout** | Discovery | Weekly search for new skill ideas |
| **supervisor** | Operations | Network-wide status dashboard — all PAs, tasks, system health |
| **whatsapp** | Memory | Per-conversation context, unanswered tracking, loop prevention |
| **youtube-watcher** | Utility | Fetch and summarize YouTube video transcripts |
| **skill-analytics** | Analytics | Track skill usage, generate daily reports, find unused skills |

---

## Multi-Skill Workflows

Some tasks need multiple skills in sequence:

### New PA Setup
```
pa-onboarding → calendar-setup → monday-for-agents → ai-pa (add to directory)
```

### PA Network Health Check
```
supervisor → billing-monitor (flagged PAs) → self-monitor (infrastructure issues)
```

### After a Mistake
```
self-learning (log it) → eval (update score) → SOUL.md (add rule if pattern)
```

### Schedule a Meeting
```
ai-pa (find the other PA's contact) → meetings (coordinate + book)
```

### Weekly Maintenance
```
whatsapp (weekly digest) → owner-briefing (include highlights) → maintenance (push to git)
```

### After Important Group Chat
```
whatsapp (log decisions) → maintenance (push to GitHub)
```

---

## Where to Run (Complexity Guide)

### Run inline (main session)
- ai-pa, billing-monitor, owner-briefing, supervisor, self-learning, maintenance

### Consider subagent for heavy operations
- calendar-setup, meetings (scheduling flow), monday-for-agents (bulk ops)

### Spawn subagent (recommended)
- pa-onboarding (20+ steps), eval (full monthly analysis), batch operations, skill-scout

---

## Model Guidance

| Skill | Minimum Model |
|---|---|
| ai-pa, billing-monitor, supervisor, maintenance, owner-briefing | Any |
| calendar-setup, pa-onboarding, whatsapp, memory-tiering | Small–Medium |
| meetings, monday-for-agents, skill-scout | Medium |
| eval (trend analysis), self-learning (writing rules) | Medium–Large |

---

## Adding New Skills

When a new skill is added:
1. Add a row to the **Full Skill Library** table.
2. Add trigger phrases to **Quick Lookup**.
3. Update the **Decision Tree** if it fits a new category.
4. Add to any relevant **Multi-Skill Workflows**.
5. Check skill count — stay under 32 active skills.
6. Add the skill name to the `KNOWN_SKILLS` list in `skill-analytics/SKILL.md`.

---

## Supervisor (Status Dashboard)

| Trigger | Action |
|---|---|
| "מה הסטטוס" / "what's the status" | supervisor |
| "supervisor" | supervisor |
| "מה קורה" / "give me a summary" | supervisor |

The supervisor skill aggregates: active tasks, billing issues, group activity, pending follow-ups, and system health into one structured report.

---

## Eval

| Trigger | Action |
|---|---|
| "תעשי eval" / "run eval" | eval |
| "מה עובד ומה לא" | eval |
| "בדקי הכל" | eval |

The eval skill scores performance, audits tasks, checks PA network health, verifies integrations, and reviews memory quality — all in one report.

---

## Cost Tips

- **This skill itself:** Very cheap — it's a lookup table, any model works.
- **Routing decision:** If unsure, lean toward a smaller, cheaper skill first.
- **Don't over-spawn:** Use subagents only when the task would actually block the main session.
