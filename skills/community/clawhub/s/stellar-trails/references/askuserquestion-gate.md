# AskUserQuestion Gate Template

This file contains the detailed AskUserQuestion gate pattern. Read this when:
- Task type is Document or Visualization
- User's request does NOT explicitly pin audience + style + length
- You need the 6-8 question template + skip conditions

## Mandate

In SPECIFY phase, if task type is Document or Visualization AND the user's original request does NOT already explicitly pin audience + style + length, invoke `AskUserQuestion` with 6-8 questions.

## The 6-8 Questions

1. **Audience** — who is this for (students / colleagues / clients / investors / executives / general public / domain reviewers)
2. **Purpose** — what should the audience do after consuming (inform / decide / pitch / sell / teach / review / launch / align on strategy)
3. **Length / Size** — calibrated to artifact type (e.g., PPT: short 1-8 / medium 8-12 / long 12+ slides; Doc: short ~500 / medium ~1,500 / long ~3,000+ words)
4. **Design Style** — primary look & feel (business formal / tech & futuristic / education & warm / minimal whitespace / editorial / dark premium)
5. **Must-include content** — multi-select: required sections, data points, citations, case studies, screenshots
6. **Format constraints** — page header/footer needs, speaker notes, info density (per-page word count)
7. **Deliverable shape** — cover/TOC/Q&A/appendix inclusion
8. **Language** — only ask if not inferable from user's input

## Question Construction Rules

Each question:
- 3-4 concrete options (NOT vague "formal / casual" — give specific palettes, style references, sample headlines)
- Mark exactly one option as `recommended` (the default if user doesn't answer)
- User is free to type their own answer — options are suggestions, not a closed list

## Skip Conditions (Do NOT Invoke AskUserQuestion)

- User explicitly says "skip questions" / "just do it" / "don't ask"
- User's original request already pinned audience AND style AND length (all three explicit)
- Task is trivial one-shot edit (single typo, single number change)
- Task type is Coding or Non-Coding (questions only for deliverable creation)
- Continuation of previous work where preferences were already confirmed

## Call Cadence

- AT MOST ONCE per run, very early — before any content-producing tool (Outline, Write, subagent delegation, file generation)
- Do NOT call any other tool in the same turn as AskUserQuestion

## After Answers Return

Proceed straight to PLAN phase (or SADC if not yet done). Do NOT loop back for more questions — one round is enough. The answers become authoritative requirements for the rest of the run.

## Why This Matters

Without AskUserQuestion, the agent guesses audience/style/length and often produces a deliverable that mismatches the user's mental model. Rework cost is high (regenerate entire document). With AskUserQuestion, one batched round of questions up front prevents hours of rework downstream. The user explicitly invoked Stellar Trails to enforce this discipline.
