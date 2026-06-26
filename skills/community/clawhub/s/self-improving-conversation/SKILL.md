---
name: self-improving-conversation
description: "Captures dialogue learnings, tone mismatches, escalation failures, and conversation quality issues for continuous improvement. Use when: (1) A user expresses frustration or confusion, (2) Tone mismatch is detected between agent and user, (3) Context is lost mid-conversation, (4) Agent hallucinates information, (5) User requests escalation to a human, (6) Conversation is abandoned or user rephrases repeatedly, (7) A missing conversational capability is identified. Also review learnings before handling complex dialogue flows."
metadata:
---

# Self-Improving Conversation Skill

Log dialogue learnings, tone issues, and conversation failures to markdown files for continuous improvement. Conversational agents can later process these into playbooks, and important patterns get promoted to project memory.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n\nTone mismatches, context losses, hallucinations, and dialogue insights captured during conversations.\n\n**Categories**: tone_mismatch | misunderstanding | escalation_failure | context_loss | sentiment_drift | hallucination\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/DIALOGUE_ISSUES.md ] || printf "# Dialogue Issues Log\n\nConversation failures, misunderstandings, tone mismatches, and escalation problems.\n\n---\n" > .learnings/DIALOGUE_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nConversational capabilities requested by users or identified through dialogue analysis.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log personally identifiable information, auth tokens, or private user data unless the user explicitly asks for that level of detail. Prefer short summaries or redacted excerpts over raw conversation transcripts.

If you want automatic reminders or setup assistance, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| User says "That's not what I meant" | Log to `.learnings/DIALOGUE_ISSUES.md` with `misunderstanding` |
| Formal response to casual user | Log to `.learnings/LEARNINGS.md` with category `tone_mismatch` |
| Lost thread in multi-turn dialogue | Log to `.learnings/LEARNINGS.md` with category `context_loss` |
| Agent states incorrect facts | Log to `.learnings/LEARNINGS.md` with category `hallucination` |
| User asks for human agent | Log to `.learnings/DIALOGUE_ISSUES.md` with `escalation_failure` |
| User sentiment drops mid-conversation | Log to `.learnings/LEARNINGS.md` with category `sentiment_drift` |
| User requests missing capability | Log to `.learnings/FEATURE_REQUESTS.md` |
| User abandons conversation | Log to `.learnings/DIALOGUE_ISSUES.md` with `abandonment` |
| Simplify/Harden recurring patterns | Log/update `.learnings/LEARNINGS.md` with `Source: simplify-and-harden` and a stable `Pattern-Key` |
| Similar to existing entry | Link with `**See Also**`, consider priority bump |
| Conversation pattern is proven | Promote to `SOUL.md` (tone/style), `AGENTS.md` (dialogue workflow), or `TOOLS.md` (integration) |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-conversation
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-conversation.git ~/.openclaw/skills/self-improving-conversation
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Dialogue workflows, handoff protocols, escalation chains
├── SOUL.md            # Conversational tone, personality, empathy guidelines
├── TOOLS.md           # Integration capabilities, channel-specific gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── DIALOGUE_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — tone mismatches, context losses, hallucinations, sentiment drift
- `DIALOGUE_ISSUES.md` — escalation failures, misunderstandings, abandoned conversations
- `FEATURE_REQUESTS.md` — user-requested conversational capabilities

### Promotion Targets

When learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Conversation patterns | `SOUL.md` | "Match user's formality level within 2 exchanges" |
| Dialogue workflows | `AGENTS.md` | "Offer human handoff after 3 failed intent matches" |
| Integration gotchas | `TOOLS.md` | "Slack threads lose context after 50 messages" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-conversation
openclaw hooks enable self-improving-conversation
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above. Avoid reading templates from the current repo or workspace unless you explicitly trust that path.

### Add reference to agent files AGENTS.md, CLAUDE.md, or .github/copilot-instructions.md to remind yourself to log dialogue learnings. (This is an alternative to hook-based reminders.)

#### Self-Improving Conversation Workflow

When dialogue issues or conversation failures occur:
1. Log to `.learnings/DIALOGUE_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable patterns to:
   - `CLAUDE.md` - project conversation conventions
   - `AGENTS.md` - dialogue workflows and escalation protocols
   - `.github/copilot-instructions.md` - Copilot conversation context

## Logging Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: greeting | intent_detection | response_generation | handoff | follow_up | closing

### Summary
One-line description of the conversational learning

### Details
Full context: what the user said, what the agent responded, what went wrong,
what the correct response should have been

### Suggested Action
Specific conversational improvement: tone adjustment, intent mapping, escalation rule

### Metadata
- Source: conversation | user_feedback | sentiment_analysis | dialogue_review
- Related Files: path/to/dialogue_config.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: tone.formality_mismatch | context.thread_loss (optional, for recurring-pattern tracking)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

### Dialogue Issue Entry

Append to `.learnings/DIALOGUE_ISSUES.md`:

```markdown
## [DLG-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: greeting | intent_detection | response_generation | handoff | follow_up | closing

### Summary
Brief description of the dialogue failure

### Conversation Excerpt
```
User: [what the user said]
Agent: [what the agent responded]
User: [user reaction indicating failure]
```

### Root Cause
- Misidentified intent / tone mismatch / missing context / hallucination / escalation gap

### Impact
- User frustration level: low | moderate | high | critical
- Conversation outcome: resolved_late | abandoned | escalated | unresolved

### Suggested Fix
How to handle this conversation pattern in the future

### Metadata
- Reproducible: yes | no | unknown
- Channel: web | slack | api | voice
- Related Files: path/to/intent_config.ext
- See Also: DLG-20250110-001 (if recurring)

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: greeting | intent_detection | response_generation | handoff | follow_up | closing

### Requested Capability
What conversational capability the user wanted

### User Context
Why they needed it, what dialogue scenario triggered it

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: new intent, dialogue flow, integration, playbook

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_capability_name
- Channel: web | slack | api | voice

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `DLG` (dialogue issue), `FEAT` (feature)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250115-001`, `DLG-20250115-A3F`, `FEAT-20250115-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Fix Applied**: Updated intent taxonomy / added escalation rule / adjusted tone config
- **Notes**: Brief description of what was done
```

Other status values:
- `in_progress` - Actively being investigated or fixed
- `wont_fix` - Decided not to address (add reason in Resolution notes)
- `promoted` - Elevated to SOUL.md, AGENTS.md, or conversation playbook

## Promoting to Project Memory

When a conversational learning is broadly applicable (not a one-off exchange), promote it to permanent project memory.

### When to Promote

- Learning applies across multiple conversation flows
- Knowledge any conversational agent should know
- Prevents recurring dialogue failures
- Documents project-specific conversational conventions

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| `CLAUDE.md` | Project conversation conventions, tone rules, known user patterns |
| `AGENTS.md` | Dialogue workflows, escalation protocols, handoff procedures |
| `.github/copilot-instructions.md` | Conversation context and conventions for Copilot |
| `SOUL.md` | Conversational personality, empathy guidelines, tone rules (OpenClaw workspace) |
| `TOOLS.md` | Channel capabilities, integration limits, API quirks (OpenClaw workspace) |

### How to Promote

1. **Distill** the learning into a concise conversational rule or guideline
2. **Add** to appropriate section in target file (create file if needed)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: SOUL.md`, `AGENTS.md`, or target file

### Promotion Examples

**Learning**: Agent used technical jargon with a non-technical user. Three exchanges wasted.
**In SOUL.md**: `Mirror user's vocabulary level within 2 exchanges. Avoid jargon with casual users.`

**Learning**: User asked for human three times before agent escalated. User abandoned.
**In AGENTS.md**: `Initiate handoff after second "talk to human" request. Never require more than 2.`

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: DLG-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring conversation issues often indicate:
   - Missing intent in taxonomy (→ update intent config)
   - Tone mismatch pattern (→ promote to SOUL.md)
   - Missing escalation path (→ promote to AGENTS.md)
   - Channel-specific limitation (→ document in TOOLS.md)

## Simplify & Harden Feed

Use this workflow to ingest recurring patterns from the `simplify-and-harden` skill and turn them into durable conversational guidance.

### Ingestion Workflow

1. Read `simplify_and_harden.learning_loop.candidates` from the task summary.
2. Use `pattern_key` as the stable dedupe key.
3. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
4. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
5. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`, set `Pattern-Key`, `Recurrence-Count: 1`.

### Promotion Rule

Promote when: `Recurrence-Count >= 3`, seen across 2+ conversation flows, within 30-day window.
Targets: `SOUL.md` (tone), `AGENTS.md` (escalation), `TOOLS.md` (channel limits).
Write short prevention guidelines, not dialogue transcripts.

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before handling a complex dialogue flow
- After a conversation with user frustration signals
- When working on intent taxonomy or escalation rules
- Weekly during active chatbot development

### Quick Status Check
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority dialogue issues
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: intent_detection" .learnings/*.md
```

### Review Actions
- Resolve fixed dialogue issues
- Promote applicable conversational patterns
- Link related entries across flows
- Escalate recurring misunderstanding patterns

## Detection Triggers

Automatically log when you notice:

**Tone Mismatches** (→ learning with `tone_mismatch` category):
- Response formality doesn't match user's style
- Overly technical language for a casual user
- Too casual for a formal/professional context
- Emoji or humor where user expects seriousness

**Misunderstandings** (→ dialogue issue):
- "That's not what I meant"
- "No, I was asking about..."
- "You misunderstood"
- User rephrases the same question 3+ times

**Escalation Failures** (→ dialogue issue with `escalation_failure`):
- "Can I talk to a human?"
- "Let me speak to someone real"
- "I need a real person"
- "This isn't working, transfer me"

**Context Loss** (→ learning with `context_loss` category):
- Agent asks question already answered earlier
- Agent contradicts its own prior response
- Agent loses track of multi-step request
- "I already told you that"

**Sentiment Drift** (→ learning with `sentiment_drift` category):
- User starts friendly, becomes curt
- Increasing use of caps or punctuation (!!!)
- Shorter responses indicating disengagement
- Explicit frustration markers ("ugh", "come on")

**Hallucination** (→ learning with `hallucination` category):
- Agent states business hours, policies, or data that doesn't exist
- Agent references features that aren't available
- Agent fabricates conversation history
- Agent cites non-existent documentation or sources

**Feature Gaps** (→ feature request):
- "Can you also handle..."
- "I wish the bot could..."
- "Why can't you understand..."
- "Do you support [language/channel]?"

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| `critical` | User PII exposed in conversation, security breach, data leak in dialogue |
| `high` | Repeated misunderstanding affecting core flow, escalation path broken, hallucination about critical info |
| `medium` | Tone mismatch causing friction, context loss in long conversations, sentiment drift |
| `low` | Minor phrasing improvement, edge-case intent miss, cosmetic dialogue issue |

## Area Tags

Use to filter learnings by conversation phase:

| Area | Scope |
|------|-------|
| `greeting` | Opening messages, welcome flows, channel detection |
| `intent_detection` | NLU, intent classification, entity extraction |
| `response_generation` | Reply composition, tone selection, content assembly |
| `handoff` | Escalation to human, agent transfer, channel switching |
| `follow_up` | Clarification loops, confirmation, next-step suggestions |
| `closing` | Farewell, satisfaction check, feedback collection |

## Best Practices

1. **Log immediately** — conversational context is lost quickly once the exchange moves on
2. **Include conversation excerpts** — future agents need to see the actual exchange
3. **Note the user's emotional state** — helps calibrate future tone adjustments
4. **Record the channel** — Slack, web, API, voice all have different constraints
5. **Suggest concrete dialogue fixes** — not just "improve response" but specific phrasing
6. **Track intent taxonomy gaps** — misunderstandings often mean missing intents
7. **Promote tone rules aggressively** — if in doubt, add to SOUL.md
8. **Review before complex flows** — check for known issues in similar dialogue paths

## Gitignore Options

**Keep learnings local** (per-developer):
```gitignore
.learnings/
```

This repo uses that default to avoid committing sensitive conversation logs by accident.

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in** — you must explicitly configure hooks.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-conversation/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a dialogue learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

Add `PostToolUse` hook alongside activator for automated dialogue failure detection from command output. See `references/hooks-setup.md` for the full JSON configuration.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate dialogue learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on conversation error patterns |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a conversational learning is valuable enough to become a reusable skill, extract it using the provided helper.

### Skill Extraction Criteria

A learning qualifies for skill extraction when ANY of these apply:

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Has `See Also` links to 2+ similar dialogue issues |
| **Verified** | Status is `resolved` with working conversational fix |
| **Non-obvious** | Required actual dialogue analysis to discover the pattern |
| **Broadly applicable** | Not project-specific; useful across chatbot implementations |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Dialogue learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-conversation/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-conversation/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with conversational learning content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation:** "Save this dialogue pattern", "We keep getting this wrong", "This would help other chatbots"

**In learning entries:** Multiple `See Also` links, high priority + resolved, `tone_mismatch` or `escalation_failure` with broad applicability

### Skill Quality Gates

- [ ] Pattern tested across multiple dialogue flows
- [ ] Description clear without original conversation context
- [ ] Dialogue examples anonymized (no PII)
- [ ] Follows skill naming conventions (lowercase, hyphens)

## Multi-Agent Support

This skill works across different AI agents with agent-specific activation.

### Claude Code

**Activation**: Hooks (UserPromptSubmit, PostToolUse)
**Setup**: `.claude/settings.json` with hook configuration
**Detection**: Automatic via hook scripts

### Codex CLI

**Activation**: Hooks (same pattern as Claude Code)
**Setup**: `.codex/settings.json` with hook configuration
**Detection**: Automatic via hook scripts

### GitHub Copilot

**Activation**: Manual (no hook support)
**Setup**: Add to `.github/copilot-instructions.md`:

```markdown
## Conversation Self-Improvement

After handling dialogue interactions, consider logging to `.learnings/`:
1. Tone mismatches, misunderstandings, escalation failures
2. Link related entries with See Also
3. Promote proven conversational patterns to skills

Ask in chat: "Should I log this dialogue issue?"
```

**Detection**: Manual review at session end

### OpenClaw

**Activation**: Workspace injection + inter-agent messaging
**Setup**: See "OpenClaw Setup" section above
**Detection**: Via session tools and workspace files

### Agent-Agnostic Guidance

Regardless of agent, apply conversation self-improvement when you:

1. **Detect tone mismatch** — your formality doesn't match the user's
2. **Lose context** — you forgot something the user already said
3. **Hallucinate** — you stated something factually incorrect
4. **Fail to escalate** — user wanted a human and didn't get one
5. **Miss intent** — user had to rephrase multiple times

### Copilot Chat Integration

Quick prompts for Copilot users:
- "Log this dialogue issue"
- "Create a skill from this conversation pattern"
- "Check .learnings/ for related dialogue issues"

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/conversation/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: conversation
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (conversation)
Only trigger this skill automatically for conversation signals such as:
- `tone mismatch|intent miss|hallucination|rephrase|clarification loop`
- `escalation needed|user frustration|context loss`
- explicit conversation intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/conversation/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
