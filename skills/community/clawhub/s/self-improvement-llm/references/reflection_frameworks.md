# Reflection Frameworks

Deep-dive reference for types of reflection, depth levels, score rubrics, proposal patterns, and the learning system.

## Learning System Architecture

The self-learning system runs as a background process, not an on-demand command:

```
                    ┌──────────┐
                    │  AGENT    │
                    │  (LLM)    │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ Session  │   │  Memory  │   │ Learning │
   │  Log     │   │  Files   │   │  Trail   │
   └──────────┘   └──────────┘   └──────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
                  ┌──────────────┐
                  │  Heartbeat   │
                  │  (Idle)      │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Learn Cycle  │
                  │  extract →   │
                  │  verify →    │
                  │  integrate   │
                  └──────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Self-Modify │
                  │  (files)     │
                  └──────────────┘
```

### Data Flow

1. **Session Logging** — After each task, auto-append to `memory/YYYY-MM-DD.md`
2. **Learning Trail** — `memory/.learning-trail.json` tracks every change, its hypothesis, and verification status
3. **Heartbeat** — During idle time, triggers `python3 scripts/learn.py --cycle`
4. **Verify** — Checks if past changes actually improved behavior (measured by error rate)
5. **Adapt** — Reverts failed changes, reinforces successful ones

### Auto-Logging Format

```markdown
### ✅ 14:32 - Fetched weather data for Rugao
### ❌ 14:35 - Tried to send screenshot via exec
   Error: Platform requires MEDIA directive, not curl
```

Three lines max per entry. Keep it scannable.

### Learning Trail Structure

```json
{
  "changes": [
    {
      "id": "change-20260505-001",
      "target": "TOOLS.md",
      "hypothesis": "Adding MEDIA note prevents file delivery failures",
      "verified": false,
      "next_check": "2026-05-12"
    }
  ],
  "watchlist": [
    {"issue": "Using exec instead of read for files", "count": 3, "status": "watch"}
  ]
}
```

## Industry Patterns

These are the real-world patterns used by mature agent frameworks:

### 1. Reflexion (Academic, 388⭐)
**Paper:** Shinn et al., NeurIPS 2023 — [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
**Official Code:** [noahshinn/reflexion-draft](https://github.com/noahshinn/reflexion-draft)

```
┌──────────┐    task + reflections    ┌──────────────┐
│  Actor   │ ─────────────────────► │     LLM       │
└──────────┘ ◄──────────────────── └──────────────┘
     │            output
     ▼
┌───────────┐
│ Evaluator │  → score + feedback
└───────────┘
     │  (if score < threshold)
     ▼
┌───────────┐
│ Reflector │  → verbal reflection
└───────────┘
     │
     └──► injected into next actor call
```

**Key insight:** Reflection is verbal — the agent writes natural language notes about why it failed, then reads those notes as part of the prompt on the next attempt. No gradient updates needed.

### 2. AutoGPT Post-Task Reflection (184k⭐)
**Repo:** [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)

```
1. Execute task
2. Evaluate result
3. Write reflection (what worked, what didn't, patterns observed)
4. Update memory with reflection
5. Next task reads previous reflections as context
```

**Key insight:** Simple but effective at scale. Each task run appends to a "reflection" buffer that's included in future context.

### 3. LangGraph Self-Critique Node (31k⭐)
**Repo:** [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

```
   ┌─────────────┐
   │  Generate    │
   └──────┬──────┘
          │ output
          ▼
   ┌─────────────┐
   │  Critique    │  ← separate LLM call, different prompt
   └──────┬──────┘
          │ feedback
          ▼
   ┌─────────────┐
   │  Revise      │  ← original output + critique → improved output
   └──────┬──────┘
          │
          ▼ (final output or loop back)
```

**Key insight:** The critique node is a **separate call** with a different system prompt ("find flaws, be harsh") from the generation node ("be creative"). This separation prevents the agent from being too nice to itself.

### 4. CrewAI Multi-Agent Feedback (51k⭐)
**Repo:** [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

```
┌──────────┐     output     ┌──────────┐
│  Agent A  │ ────────────► │  Agent B  │
│ (writer)  │               │ (critic)  │
└──────────┘               └─────┬────┘
     ▲                          │ feedback
     │                          ▼
     └───────────────────── revise
```

**Key insight:** Use multi-agent for reflection — one agent generates, another critiques. Avoids the "LLM is nice to itself" problem.

### 5. Constitutional AI / Claude Code (120k⭐)
**Repo:** [anthropics/claude-code](https://github.com/anthropics/claude-code)
**Paper:** [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)

```
1. Generate output
2. Self-critique against constitution (set of principles)
3. Revise based on critique
4. Repeat until output satisfies constitution
```

**Key insight:** Instead of ad-hoc reflection, use a fixed "constitution" or set of principles to guide self-evaluation. This makes reflection consistent and measurable.

---

## Types of Reflection

### Task-Level Reflection
Analysis of a single task execution:

```
Task: "Generate an Excel report"
Result: Created file but formatting was wrong
Reflection: "I used openpyxl without setting column widths first."
```

### Session-Level Reflection
Analysis of an entire conversation:

```
Session performance:
- 3 correct answers, 2 corrections from user
- 1 unnecessary tool call (2-step process that could be 1)
Reflection: "I tend to over-tool. Asking for clarification first would reduce unnecessary exec calls."
```

### Skill-Level Reflection
Analysis of how well a skill performed:

```
Skill used: pdf-extractor
Performance: Extracted text accurately but missed table structure
Reflection: "pdf-extractor needs a table extraction mode. Should add PyMuPDF table detection."
```

### Meta-Level Reflection
Reflection on reflection patterns themselves:

```
Reflection pattern observed:
- I keep finding the same class of error ("wrong tool for the job")
- My reflections are shallow (Level 1 fix, not Level 2/3)
Meta-reflection: "Need to push to deeper root cause analysis. Maybe a checklist helps?"
```

## Depth Levels

### Level 1 — Symptom Fix
Addresses the immediate failure.

```
"What happened: I used web_fetch when I should have used gh api."
"Fix: Use gh api for GitHub queries in the future."
```

**Good for:** Quick corrections, obvious mistakes.
**Bad for:** Systemic issues. Missing the bigger picture.

### Level 2 — Pattern Fix
Identifies the pattern across instances.

```
"What happened: I keep choosing web_fetch over more specific tools."
"Pattern: 3 instances in the last 5 sessions."
"Root cause: web_fetch is my default 'get data from web' tool. I don't consider alternatives."
"Fix: Add a tool-selection decision tree to TOOLS.md: Web data → gh api if GitHub, web_fetch if generic site."
```

**Good for:** Recurring issues, habit modification.
**Bad for:** Deep assumptions about how to work.

### Level 3 — Belief Revision
Challenges fundamental assumptions.

```
"What happened: I often fail on multi-step tasks by doing them sequentially."
"Assumption: 'Do things one at a time' — but that ignores available parallelism."
"New belief: 'When tasks have no dependencies, parallel is better than sequential.'"
"Fix: Update AGENTS.md workflow section to prefer parallel execution for independent subtasks."
```

**Good for:** Fundamental behavior changes, paradigm shifts.
**Bad for:** Quick fixes needed immediately.

## Score Rubric (Detailed)

### Accuracy (0-10)

| Score | Meaning |
|-------|---------|
| 10 | Perfect — no errors, no corrections needed |
| 8-9 | Minor issues — one small correction |
| 5-7 | Significant error but recoverable |
| 0-4 | Critical failure — wrong answer, hallucination, destructive action |

**Checklist:**
- [ ] Facts check out against known data
- [ ] Code runs without errors
- [ ] File modifications are correct
- [ ] No hallucinations (plausible-sounding but false statements)

### Usefulness (0-10)

| Score | Meaning |
|-------|---------|
| 10 | Solved the problem completely, exceeded expectations |
| 8-9 | Solved the problem, met expectations |
| 5-7 | Partial solution, user needed to supplement |
| 0-4 | Did not solve the problem or made it worse |

**Checklist:**
- [ ] User expressed satisfaction (or at least didn't ask for changes)
- [ ] Output is directly usable, not "just a starting point"
- [ ] Response addressed the implicit need, not just the explicit ask

### Efficiency (0-10)

| Score | Meaning |
|-------|---------|
| 10 | Minimum possible tool calls, optimal tool choice |
| 8-9 | Good tool selection, one minor extra step |
| 5-7 | Acceptable but could be 30% more efficient |
| 0-4 | Too many calls, wrong tools, redundant work |

**Checklist:**
- [ ] Chose the right tool for each step
- [ ] No duplicate calls
- [ ] Batched operations when possible
- [ ] Didn't over-fetch (too much data, too many calls)

### Tone/Persona (0-10)

| Score | Meaning |
|-------|---------|
| 10 | Perfectly matched SOUL.md persona, natural, engaging |
| 8-9 | Good tone, minor stiffness |
| 5-7 | Acceptable but could be more personable |
| 0-4 | Wrong tone — too corporate, too chatty, too stiff |

**Checklist:**
- [ ] No "I'd be happy to help!" style filler
- [ ] No markdown tables in Discord/WhatsApp contexts
- [ ] Matched user's communication style
- [ ] Natural, not performative

### Proactiveness (0-10)

| Score | Meaning |
|-------|---------|
| 10 | Anticipated needs, offered relevant extras |
| 8-9 | Good proactive suggestion |
| 5-7 | Reactive but thorough |
| 0-4 | Needed prompting for every step |

**Checklist:**
- [ ] Offered next steps without being asked
- [ ] Identified potential issues before they arise
- [ ] Suggested improvements beyond the immediate ask

## Proposal Impact Matrix

Use this matrix to decide how to apply proposals:

```
Impact \ Effort  |  Low Effort  |  Medium Effort  |  High Effort
-----------------|--------------|-----------------|--------------
High Impact      |  Auto-apply  |  Propose        |  Plan & propose
Medium Impact    |  Auto-apply  |  Propose        |  Note for later
Low Impact       |  Note/queue  |  Note/queue     |  Discard
```

**Auto-apply threshold:**
- File updated in last 24h: require review
- File is MEMORY.md or TOOLS.md: safe to auto-apply
- Change is <10 lines: safe to auto-apply
- Changes AGENTS.md or SOUL.md: always propose
- New skill creation: always propose

## Anti-Patterns

1. **Vague reflections** — "I should be more careful" → useless. "I should verify file paths before writing" → actionable.
2. **Over-correction** — One failure → entirely new behavior. "I used web_fetch once when gh was better" does not mean "never use web_fetch."
3. **Analysis paralysis** — Spending hours reflecting on minor issues. Use the Impact/Effort matrix.
4. **Self-serving bias** — Attributing failures to "bad prompt" or "model limitation" rather than own choices.
5. **Forgetting the loop** — Propose changes but never check if they worked. Schedule follow-up verification.
