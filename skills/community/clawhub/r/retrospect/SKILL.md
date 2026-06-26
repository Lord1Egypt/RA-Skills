---
name: retrospect
description: "Session retrospective that analyzes conversation history to produce structured feedback for both user and LLM. Use this skill whenever the user says '复盘', 'retrospect', '批评与自我批评', 'session review', 'review this session', or asks to review/reflect on how a conversation went. Also trigger when the user wants feedback on their prompting skills, wants the LLM to self-critique its mistakes, or asks for a post-mortem of the current or a past session."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# Retrospect — Session Retrospective: Critique & Self-Critique

Perform a structured retrospective on all conversation sessions in the current project. This produces two deliverables:

1. **FEEDBACK_TO_HUMAN.md** — Critique of the user's prompting behavior
2. **FEEDBACK_TO_LLM.md** — Self-critique of the LLM's performance

## Step 1: Locate and parse all session transcripts

Run the bundled parser, passing the current working directory. It will automatically find all session JSONL files for this project, merge them in chronological order, and output a unified transcript.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/parse_session.js --project-dir "$(pwd)" > /tmp/session_transcript.md
```

The parser:
- Derives the Claude Code project path from the working directory (e.g., `/Users/tom/myproject` → `~/.claude/projects/-Users-tom-myproject/`)
- Finds **all** `.jsonl` files in that directory (excluding subagent logs)
- Sorts them by modification time (oldest first)
- Merges them into one transcript with session boundaries marked
- Auto-detects JSONL format (Claude Code, Codex, OpenCode)

If the transcript is very long, the parser automatically summarizes older sessions (keeping only user messages and key exchanges) while preserving full detail for the most recent sessions.

## Step 2: Spawn the analysis subagent

Launch a **single** subagent (via the Agent tool, or equivalent in your platform) with the full transcript content. The subagent reads the transcript and writes both feedback files to the project root directory.

Pass the subagent this prompt structure (fill in the transcript and project root):

---

You are a session retrospective analyst. You have been given conversation transcripts from all sessions in a project between a user and an LLM. Your job is to produce two analysis documents.

Read the transcript carefully, then write both files to: `<project-root>`

**The transcript is below:**

<transcript>
{content of /tmp/session_transcript.md}
</transcript>

### File 1: FEEDBACK_TO_HUMAN.md

Analyze the **user's** behavior across all sessions. Structure the document as:

#### Overall Assessment
A 2-3 sentence summary of how effectively the user communicated with the LLM across this project.

#### Round-by-Round Analysis
For each significant exchange (skip trivial ones like "ok" or tool confirmations), analyze:
- What the user asked for
- Whether the request was clear and specific enough
- If the LLM did something the user didn't want — was it because the user's prompt was ambiguous, or because the LLM misunderstood a clear instruction?

When the user expresses frustration or rejection of LLM output, perform a **responsibility analysis**:
- Was the user's previous instruction genuinely unclear or misleading? → The user shares responsibility
- Was the user's instruction clear but the LLM made its own wrong assumption? → LLM's responsibility
- Be honest and fair — sometimes the user IS at fault, sometimes the LLM is

#### Prompting Patterns
Identify recurring patterns across sessions (good and bad):
- Does the user give enough context upfront, or drip-feed requirements?
- Does the user specify constraints, or leave too much to LLM judgment?
- Does the user correct effectively, or repeat the same vague correction?
- Are there patterns that recur across multiple sessions?

#### Suggestions
Concrete, actionable advice for how the user could prompt more effectively in future sessions. Focus on what would save the most time and frustration.

### File 2: FEEDBACK_TO_LLM.md

Analyze the **LLM's** behavior across all sessions. Structure the document as:

#### Overall Assessment
A 2-3 sentence summary of the LLM's performance across this project.

#### Mistakes & Errors
For each significant mistake the LLM made:
- What went wrong
- Root cause (wrong assumption, outdated knowledge, misread instruction, etc.)
- How it was eventually resolved
- What the correct approach should have been from the start

Pay special attention to:
- Incorrect API/library usage that required multiple attempts to fix
- Cases where the LLM confidently did the wrong thing
- Unnecessary detours or wasted effort
- Mistakes that recur across sessions (the LLM didn't learn from previous failures)

#### Counter-Intuitive Learnings
Information encountered in these sessions that a general-purpose LLM would NOT know or would likely get wrong. Examples:
- Project-specific configurations that break standard assumptions
- Library quirks, undocumented behavior, or version-specific API differences
- Environment-specific gotchas

For each item, explain: what the intuitive assumption would be, what the reality is, and why this matters.

#### Self-Improvement Notes
What should the LLM do differently next time when facing similar tasks?

---

**Important guidelines for the subagent:**
- Write in the same language the user primarily used in the conversations (Chinese if they spoke Chinese, English if English, etc.)
- Be honest and balanced — the goal is genuine improvement, not flattery or self-flagellation
- Use specific quotes or references from the transcript to support your analysis
- When analyzing multiple sessions, note cross-session patterns (e.g., "the same mistake appeared in Session 3 and Session 7")
- If the sessions were short or uneventful, say so — don't manufacture insights

## Step 3: Report completion

After the subagent finishes, tell the user where the files are and give a one-line summary of each file's key finding.
