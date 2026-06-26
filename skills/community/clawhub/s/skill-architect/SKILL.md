---
name: skill-architect
description: 'Design and create new AI skills with the right internal structure — not just correct formatting. Works with any AI coding tool (Claude Code, Google Antigravity, Cursor, Windsurf, Cline, GitHub Copilot, etc.). Use this skill when someone wants to build a new skill and wants it to be well-structured from the ground up. Triggers on: "create a skill", "build a skill", "make a skill for X", "help me write a skill", "I want a skill that does X", "design a skill". Unlike a generic skill creator, skill-architect interviews you first to understand how the skill needs to work, then applies the right design pattern (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline, or combinations) before writing a single line — so the skill behaves correctly, not just looks correct.'
---

# Skill Architect

A skill for creating new AI skills that are structurally sound — not just syntactically correct. Works with any AI coding tool — Claude Code, Google Antigravity, Cursor, Windsurf, Cline, GitHub Copilot, and more.

Most skill-creation guides focus on format: how to write SKILL.md, what goes in frontmatter, how to organize directories. This skill focuses on **design**: before writing anything, we figure out what shape the skill's internal logic should take, using Google's 5 Agent Skill Design Patterns as a framework.

The core loop:
1. **Understand the intent** — what does the user want this skill to do?
2. **Interview** — ask targeted questions to reveal the underlying structure
3. **Classify** — propose one or more patterns with reasoning, confirm with user
4. **Scaffold** — build the SKILL.md from the appropriate pattern template
5. **Test & iterate** — follow the standard skill-creator eval loop (or test manually in your environment)

---

## Phase 1: Capture Intent

Start by understanding the user's goal at a high level. Extract from context first — they may have already described what they want.

Ask only what you don't already know:
- What should this skill enable Claude to do?
- When should it trigger? What kinds of user requests?
- What does a good output look like?

Don't ask all of these at once if the answer is already clear from context. Keep it conversational.

**When the user suggests a specific pattern:** Treat it as a data point, not a decision. Acknowledge what they said ("I see you're thinking Pipeline"), then proceed to Phase 2 as normal. Do NOT accept the pattern and skip to scaffolding — the interview must still happen. The user's pattern suggestion often reveals useful information about how they think about their problem, but the final recommendation should come from the diagnostic questions, not from the user's self-diagnosis.

**Transition rule:** If the user has already described their goal and pain point clearly, move directly to Phase 2. Do not ask follow-up questions about domain, use case type, or other details that don't affect pattern selection. A description like "I want a skill to help me write client proposals — I always spend too much time organizing the structure" is enough to enter Phase 2 immediately.

---

## Phase 2: Pattern Interview

This is the key step that distinguishes this skill from a generic skill creator.

Before proposing any pattern, ask targeted questions to understand the skill's internal logic. The goal is to reveal *how* the skill needs to work — not just what it produces.

**Critical rules:**
- Ask **one question at a time**. Wait for the answer before asking the next. This is a conversation, not a form.
- Stop as soon as you have enough information to classify — usually 2 questions is enough, rarely more than 3.
- Only ask questions that affect pattern selection. Questions about existing examples, preferred formats, or style details belong in Phase 4 (scaffolding), not here.
- Never re-confirm information the user already stated explicitly. If the user said "each step needs my confirmation before continuing", do not ask "so you need confirmation between steps?" — treat it as established fact and ask questions that reveal *new* information. Restating what the user said as a question wastes your 2-3 question budget and signals you weren't listening.
- Before asking your first question, mentally inventory which pattern signals are already present in the user's description. Common signals:
  - "consistent format every time" / "same structure" → Generator
  - "first... then... next... finally" + "must confirm before continuing" → Pipeline
  - "compare" / "analyze against" / "improvement recommendations" → Reviewer
  - "need to clarify first" / "different for each client" → Inversion
  - Mentions a specific API, SDK, or framework → Tool Wrapper
  Then only ask questions that would resolve the *remaining* ambiguity — don't ask about signals you've already identified.

**The core diagnostic questions** (pick the most relevant, one at a time):

1. Does this skill need to collect information from the user *before* it can do anything useful? Or can it act immediately on what's given?
2. Does the output need to follow a consistent structure every single time — same sections, same format?
3. Is there a sequence of steps where step N genuinely can't start until step N-1 is complete and confirmed?
4. Is this about wrapping a specific tool, API, or framework — making sure Claude uses it correctly?
5. Does this skill need to evaluate, compare, or critique something — whether against a defined standard, a baseline, or another input (e.g., competitor analysis, gap analysis)?

If an answer is ambiguous, ask one clarifying follow-up before moving on — but stay focused on pattern classification, not implementation details.

**Common misclassifications to watch for:**
- "Has steps" ≠ Pipeline. Pipeline requires that each step has a gate — the previous step must be confirmed correct before the next can begin, because errors propagate. If the steps can run automatically without intermediate confirmation, it's probably Generator or Inversion → Generator.
- "Asks the user questions" ≠ Inversion. Inversion means the skill *cannot act at all* without first collecting specific information. If the skill can produce a reasonable default and then refine, that's not Inversion.
- "Checks quality" ≠ Reviewer. Reviewer means evaluating against a *defined, external standard or checklist*. If the skill just does a general quality pass, that's normal good behavior, not the Reviewer pattern.

**These questions do NOT belong in Phase 2** — they are Phase 4 (scaffolding) questions:
- What output format do you want? (Markdown, Word, PPTX...)
- Do you have an existing example or template I can reference?
- What domain or industry is this for?
- What tone or style do you prefer?
- How long should the output be?

Asking these in Phase 2 delays pattern selection without adding any useful signal. Save them for after the pattern is confirmed.

---

## Phase 3: Pattern Classification

Once you have enough information, propose a pattern (or combination). Always explain your reasoning — don't just name a pattern.

Read `references/patterns.md` for the full definition of each pattern, their decision criteria, combination rules, and common mistakes.

**The 5 patterns:**

| Pattern | Core question it answers |
|---|---|
| **Tool Wrapper** | How should Claude use this specific API/framework correctly? |
| **Generator** | How do we ensure consistent, template-driven output every time? |
| **Reviewer** | How do we evaluate something against a defined standard? |
| **Inversion** | What information must we collect before we can act? |
| **Pipeline** | What sequence of steps must happen in order, with gates? |

**How to present your recommendation:**

```
Based on what you've described, I'd suggest: [Pattern(s)]

Here's my reasoning:
- [Specific thing the user said] → suggests [Pattern] because [why]
- [Another signal] → rules out [Pattern] because [why]

This means the skill will [brief description of how it will behave].

Does this match what you had in mind, or does something feel off?
```

**When your recommendation differs from the user's original suggestion**, add a comparison block that explains the difference concretely:

```
You mentioned [Pattern X]. Here's how it compares to what I'm suggesting:

- [Pattern X] is designed for [core characteristic] — e.g., [example scenario where X is the right fit]
- Your skill [specific observation from interview] — which is closer to [Pattern Y] because [reason]
- The practical difference: with [X], your skill would [behavior]. With [Y], it would [behavior].

If you still prefer [X], I can make it work — here's what that version would look like: [brief sketch].
```

This isn't about proving the user wrong. It's about giving them the information to make an informed choice. Always offer to proceed with their original suggestion if they prefer.

Give the user a clear path to push back. Common responses:
- "Yes, that makes sense" → proceed to scaffolding
- "I'm not sure" → offer to walk through the pattern definitions together
- "I think it's more like X" → update your recommendation and re-explain

Patterns can and should be combined. See `references/patterns.md` for combination guidance.

---

## Phase 4: Scaffold the Skill

Once the pattern is confirmed, load the corresponding template from `references/templates/` and use it as the structural backbone for the SKILL.md.

**Template files:**
- `references/templates/tool-wrapper.md`
- `references/templates/generator.md`
- `references/templates/reviewer.md`
- `references/templates/inversion.md`
- `references/templates/pipeline.md`
- `references/templates/combined.md` — for multi-pattern skills

Fill in the template with everything you've learned in the interview. Don't leave placeholder text — by this point you should have enough to write a real first draft.

**Always produce the full directory structure, not just SKILL.md.** Each pattern has required companion files:

```
skill-name/
├── SKILL.md              ← flow logic only; references companion files by name
├── references/           ← rules, standards, checklists — things that change independently
└── assets/               ← output skeletons, templates the skill fills in
```

**Pattern-specific structure requirements:**

- **Generator**: SKILL.md must reference `references/style-guide.md` (tone, voice, formatting rules) and `assets/[output]-template.md` (the structural skeleton). Never inline the template or style rules into SKILL.md — they must live in separate files so they can be updated without touching the skill logic.
- **Reviewer**: SKILL.md must reference `references/review-checklist.md`. The checklist lives outside SKILL.md so the review criteria can evolve independently.
- **Tool Wrapper**: SKILL.md must reference `references/conventions.md`. The API/framework rules belong in the reference file.
- **Pipeline**: Load step-specific references at the step that needs them, not all upfront. Each step should name the file it loads.
- **Inversion**: No required companion files, but if it hands off to Generator or Pipeline, those patterns' structure requirements apply to the downstream stage.

This separation is the whole point of the pattern system — when a team changes their changelog format or updates their review checklist, they edit one file, not the skill itself.

**Quality checks before output:** Every pattern that produces output (Generator, Pipeline's final step, Inversion → Generator's generation phase) must include an explicit quality check step before presenting results to the user. Use a checkbox-style checklist that verifies:
- Every template section is present and filled (no placeholders remain)
- Tone and formatting match the style guide
- Content is internally consistent (no contradictions between sections)
- All user-provided inputs are reflected in the output

This step catches structural gaps before the user sees the result. Do not skip it — even for simple skills.

**SKILL.md content rule:** SKILL.md describes *what to do and when to load which file*. It does not contain the actual templates, checklists, or domain rules. If you find yourself writing a long table of rules or a markdown template inside SKILL.md, stop and move it to a companion file.

Keep SKILL.md under 500 lines. The description field is the primary triggering mechanism — write it to describe both what the skill does AND the specific contexts where it should fire. Make it slightly "pushy" so the skill doesn't undertrigger.

---

## Phase 5: Test & Iterate

Follow the standard skill-creator eval loop:

1. Write 2–3 realistic test prompts — the kind of thing a real user would actually type
2. Share them with the user for confirmation before running
3. Run the prompts and evaluate results qualitatively
4. Improve based on feedback, repeat

**Environment-specific guidance:**

- **Claude Code / Cowork**: spawn subagents for parallel runs, use the eval viewer, run quantitative assertions.
- **Claude.ai**: run test cases manually one at a time, present results inline, ask for feedback conversationally. Skip quantitative benchmarking.
- **Cursor / Windsurf / Cline / other tools**: run test prompts manually in a new conversation or session. Paste the generated SKILL.md as custom instructions, then test with realistic prompts. Evaluate results conversationally and iterate.

After the skill is in good shape, offer to optimize the description field for better triggering accuracy.

---

## Principles

**The pattern is a scaffold, not a cage.** Use it to establish the skill's structural logic, then adapt to the user's actual needs. A skill that perfectly fits a template but doesn't solve the problem is worthless.

**Explain the why behind every design choice.** When you write the SKILL.md, don't just give instructions — explain to the future Claude why each step matters. Smart models follow reasoning better than rules.

**The interview is the most important part.** Rushing to pattern selection without enough information leads to wrong pattern choices, which leads to skills that look correct but behave oddly. The 2–3 questions in Phase 2 are load-bearing — don't skip them.

**Combinations are normal.** Real-world skills often need two patterns. Inversion → Generator is especially common. Pipeline + Reviewer is another. Don't feel pressure to pick exactly one.