---
name: universal-verify
description: Verify, test and critique any AI-generated output (code, articles, images, video, slides, documents, web UI) before calling it done, then fix and re-check in a bounded loop so a human only reviews the few undecidable items. Use this whenever a generation task is about to be declared finished, or whenever the user mentions verify, test, review, QA, quality check, self-check, aesthetic review, 去AI味, 验证, 测试, 审美把关, 质检 — even if they do not name this skill. This skill judges output; it does not generate it.
---

# Universal Verify

## Overview

Agents usually skip real verification and hand everything to a human at the end.

## Principles (and why they matter)

- **Evidence before claims.** A claim like "tests pass" means nothing unless the command was run in this turn and its output was read. Hold back words like "perfect" or "done" until the report exists.
- **Deterministic checks beat judgment.** Commands, scripts, regex, schemas and pixel diffs are cheap and do not drift. Reserve model judges for things only a model can judge.
- **Isolate the judge.** A judge that shares the generator's context inherits its blind spots. Run judges as fresh subagents, ideally on a different model, giving them only the output, the rubric and the evidence.
- **Itemized, evidenced verdicts.** An overall score like "8/10" cannot be acted on. Each finding needs its own evidence and a fix hint.
- **Bounded loops.** Retrying tends to repeat the same error. Stop after 3 rounds and escalate to a human.

## Workflow

### 1. Spec — write the acceptance checklist
Turn the request, plus its implicit standards, into `checks.yaml` (schema: `references/report-format.md`). Each check has `id`, `criterion`, `method` (command | script | scorer | judge | human), `severity` (blocker | major | minor) and `evidence_required`. If the user gave no criteria, pull them from the matching domain pack. For subjective items such as "feels premium", write down what can be observed.

### 2. Triage — pick type and intensity
Read only the domain pack(s) you need:

| Output | Pack |
|---|---|
| Code, scripts, web app behavior | `references/code.md` |
| Articles, copy, reports, rewrites | `references/text.md` |
| Generated images | `references/image.md` |
| Generated video | `references/video.md` |
| Slides, docs, PDFs, web UI visuals | `references/doc-ui.md` |

Intensity:
- **L1 (draft or throwaway):** deterministic layer plus 1 judge.
- **L2 (default):** all layers, with 2–3 judges each covering one dimension.
- **L3 (production, financial or medical, brand hero assets):** all layers, cross-model judges, swapped-order re-judging, and a mandatory human sign-off card.

Multi-agent setups use about 15× more tokens, so don't run L3 on everything.

### 3. Layer 1 — deterministic checks
Run every command/script check. Log the command, exit code and key output. Bundled helpers:
- `scripts/ai_tone_lint.py <file>` — lexical AI-tone lint for Chinese and English (JSON output).
- `scripts/check_placeholders.py <file|dir>` — leftover TODO / lorem / xxx / {{var}} placeholders.
- `scripts/claims_diff.py <before> <after>` — numbers and named entities lost or changed in a rewrite.

If the output is fundamentally broken (doesn't build, crashes, wrong file type), jump to step 6 — judging it wastes tokens. A cheap, local blocker (a leftover TODO, one bad link) is not a reason to skip the judges: still run Layer 3, otherwise structural problems surface only in the next round.

If a command can't run in your environment (no shell, no network), run the equivalent in-process (import and call the code, inject a fake clock or stub) and label the evidence `in-process`. Never silently downgrade to reading the code.

### 4. Layer 2 — specialist scorers
Where a validated metric exists (VQAScore for image–prompt alignment, aesthetic predictors, VBench dimensions), score against a threshold. If none is available, skip this layer and say so in the report.

### 5. Layer 3 — isolated judges
For each `judge` dimension, spawn one single-purpose subagent. Its input is the output, that dimension's rubric, and the Layer 1/2 results. It returns findings as `{check_id, verdict: pass|fail|uncertain, confidence 0-100, severity, evidence, fix_hint}`.
- Drop findings with confidence below 70.
- If only one judge raised a blocker, have a second judge (preferably a different model) re-check it.
- Whenever you choose or rank among candidates (A/B, "pick the best of N"), compare the top two pairwise twice with the order swapped and record both verdicts in the report. If they disagree, mark it `uncertain`. Do this even in a self-judged pass; it costs one extra comparison.
- If you cannot spawn subagents, judge in a clearly separated pass that re-reads only the output and rubric, mark each finding `self-judged`, and cap its confidence at 80 so single-pass blockers still get a human card.
- Ignore confident tone or "I reflected carefully" in the output. That is not evidence.

### 6. Loop and escalate
Send blockers and majors back to the generator as a fix list. After the fix, re-run only the affected checks plus a quick regression pass. Stop after 3 rounds. Then emit the report, ending with at most 5 **human review cards** for anything still `uncertain`, `human`-method, or unresolved.

## Output

Use the template in `references/report-format.md`. Verdict: PASS | PASS_WITH_NOTES | FAIL | NEEDS_HUMAN.

## Anti-patterns
- "Let me double-check" inside the generator's own context, followed by PASS.
- A single holistic score with no evidence.
- AI-tone fixes that only swap words and leave the structural tells (moral-of-the-story endings, tidy closers, uniform paragraphs).
- Marking a citation "verified" when the number does not appear in the quoted source.
