---
name: refining-the-tone-of-ai
description: Use when Chinese prose sounds AI-generated, template-like, mechanically structured, overly polished, or inconsistent with the author's voice, including requests to 去AI味, 降低AI感, or 改得更像人写.
---

# Refining the Tone of AI

## Overview

Refine Chinese prose by removing only the structures that make it sound assembled from a generic assistant template. Preserve the author's facts, stance, register, constraints, and recognizable voice.

This is a preservation-first editing skill. Natural writing is not produced by random synonym replacement, forced colloquialism, deliberate roughness, or arbitrary sentence variation.

## Editing Contract

Follow this order:

1. Extract the non-negotiable content: facts, numbers, names, terminology, citations, quotations, causal direction, evidence strength, qualifiers and stated limits, required action order, and fixed formulations. Fixed formulations include official phrases and numbered policy shorthand taken from documents or meetings, titles of documents, laws, and books in `《》`, and column or series names. Keep them character for character; do not expand, shorten, reorder, or paraphrase them unless the user asks.
2. Identify the register: social post, public prose, email, academic or technical text, fiction, operational instructions, or editorial and official writing.
3. Diagnose concrete problems in context. Treat recurring shells as signals, not automatic deletion targets.
4. Make the smallest edit that removes the problem. Rewrite a whole paragraph only when its structure, not a local phrase, causes the artificial tone. Do not move material across paragraphs, such as bringing a later case to the opening, unless the user asked you to restructure. If you judge that the structure itself is the problem and the user did not ask, pause before editing and ask one short question that names the problem and the option; do not deliver a partial revision first, and do not restructure on your own.
5. Compare the revision against the non-negotiable content. Restore anything that changed without authorization.
6. Return the revised text only unless the user asks for diagnosis, comparison, or edit notes. Add one short line after the revision only when a fact in the source looks wrong (flag it; do not fix it silently), when the source needs no change (return it unchanged and say so), or when the user asked to lower a detector score (say that no detection result is promised). When step 4 requires asking before restructuring, ask instead of returning a revision.

## Context Decisions

| Signal | Revise when | Preserve when |
|---|---|---|
| `不是 A，而是 B` and related contrasts (`并非`, `不在于…而在于`, `与其说…不如说`) | A has no source: it does not appear earlier in the text or in its title, in the user's request, in an explicit reader question, or in a saying the text attributes to someone. A word's other sense raised only to define the word (`何谓 X？不是…`) is not a source. Delete the invented target and state B directly, without changing B | A has a source in one of those places; the sentence is a quotation or dialogue; or A is a fact the source asserts in its own right, such as a cause it reports checking and ruling out, or a plot fact |
| `先 A，再 B` and numbered sequences | The order is ceremonial and does not affect the result | The order encodes an operational dependency, procedure, chronology, or testimony |
| `真正重要的是`, `核心在于`, `本质上` | The phrase inflates an ordinary claim without evidence | It is a defined term, a precise technical statement, or wording the user requires |
| Assistant route markers | They narrate the response instead of delivering content | The user requested a tutorial whose navigation materially helps |
| Parallel sentences and even paragraphs | Repeated grammar and equal weight make the draft feel generated | Repetition serves argument, rhythm, characterization, or a formal document structure |
| Ending questions | They are generic engagement bait | The user requested a CTA, survey, interview question, or specific interaction |
| Rhetorical questions | The next two sentences do not answer, or only say the question is worth pondering | The next sentence answers with a cause, number, definition, or case; or the question is quoted, requested, or genuinely addressed to the reader |
| Qualifiers such as `当然`, `也要看到`, `同时注意`, `并不等于` | Never delete them as filler; shorten only if the stated limit survives | Always preserve the limit, exception, shortfall, or cost they state |
| Three-part lists and triads | Items are near-synonyms or name no object; compress them, and do not invent objects | Each item names a distinct object, actor, metric, or step |
| Slogan endings: `必将` / `定能` / `定会` with grand imagery, slogan couplets, `让我们…` | The ending only restates the thesis with grand imagery | The ending carries a fixed formulation, the publication requires it, or the user asks to keep it |
| Evaluative labels (`生动写照`, `生动实践`, `生动注脚`) and stacked metaphors (`加速器`, `催化剂`, `试金石`) | They replace information with a verdict, or several metaphors decorate one sentence | The label is part of a fixed formulation, or one metaphor carries the reasoning through the paragraph |
| Example lists closed with `……` | Examples trail off in essays, emails, technical or academic prose; close the list with 等 or end it at the last listed item, and never add items | Editorial or official register, or a quotation |
| Authority quotations | Never add one to make a claim sound weightier | Keep every quotation in the source, with its attribution |

Common route markers include `下面我们来`, `接下来我会`, `我们可以看到`, `希望这能帮到你`, `作为AI`, and `截至我的知识`. Lecture markers such as `总的来说`, `值得注意的是`, `拆一拆`, and `聊一聊` are weaker signals: revise them when they narrate instead of adding content.

### Contrast Check

Before touching a `不是 A，而是 B` sentence, look for A in four places: earlier text and the title, the user's request, an explicit reader question, and a saying the text attributes to someone. Do not judge by whether A sounds concrete or abstract, or by quotation marks around A: a quoted phrase with no stated source is still an invented target. A definitional question does not create a source either: in `何谓 X？不是 A，而是 B`, A counts only if someone in the text or the request actually reads X that way.

| Source | Decision |
|---|---|
| `复盘会的意义不是追责，而是把下次能复用的做法记下来。` (nothing earlier mentions blame) | Invented target. Revise to `复盘会的意义是把下次能复用的做法记下来。` |
| `数字化不是简单“上个系统”，而是把审批流程从七步减到三步。` (nobody in the text says it) | Invented target despite the quotation marks. Revise to `数字化是把审批流程从七步减到三步。` |
| `评审会上，有同事认为延期是因为人手不够。其实延期不是人手问题，而是需求在第二周改了三次。` | A appears earlier. Keep |
| User asks whether an error is a network problem; draft says `这个报错不是网络问题，而是证书过期了。` | A is in the user's request. Keep |
| `排查初期，团队怀疑是时钟漂移。……故障并不是时钟漂移，而是服务重启后把版本戳恢复成了 0。` | A is a hypothesis the text reports checking. Keep |
| `何谓好用？不是功能多，而是三步之内能完成报销。` (nothing earlier equates 好用 with many features) | Definitional negation with no source. Revise to `何谓好用？三步之内能完成报销。` |
| `不只是 A，更是 B` where A is affirmed rather than denied | Not a target. Revise only if the pattern repeats mechanically |

## Register Guidance

- Social posts: retain useful hooks, concrete steps, short paragraphs, and requested calls to action. Do not invent personal experience, results, or intimacy.
- Essays and public writing: retain the author's position and acceptable unevenness. Prefer concrete stakes over generic elevation. Remove invented targets (see Contrast Check) without changing the claim they framed.
- Academic and technical prose: preserve terminology, citations, variables, limitations, hedging, and the distinction between correlation and causation. Weaken unsupported claims instead of inventing evidence.
- Fiction: keep scene continuity, chronology, dialogue intent, and manuscript-only output. When the user asks to clean narration, replace unsupported stock speech modifiers such as `缓缓说道` or `淡淡地说` with a neutral speech tag; retain them when the scene establishes that pace or affect.
- SOPs and instructions: preserve every dependency whose order affects safety or outcome. Improve wording without flattening the procedure into prose.
- Email: preserve salutations, dates, times, attachment names, owners, task order, and genuine questions that ask the recipient to confirm, decide, or reply. Remove assistant pleasantries and generic engagement questions.
- Editorial and official writing (社论, 评论员文章, 时评, 理论文章, 通知, 意见, 会议纪要): sounding like an official newspaper is not a target. Editorial and theory pages carry the same template shells as generated text, including invented contrast targets, slogan endings, dense four-character parallels, `……` example lists, and `生动写照` labels. Preserve the author's position, fixed formulations, quotations, and attributions. For documents and notices, also preserve mandated structure and wording such as `现提出如下意见`, `一、` and `（一）` numbering, `会议指出`, and issuing bodies; limit edits to redundancy and assistant narration, and do not turn a document into commentary or add rhetorical questions.

## Material-Bound Techniques

Signed commentary often reads as argued rather than assembled because it answers its own questions, states limits, and engages claims that actually exist. Use a move below only when the source already contains the material it needs. Never create a case, quotation, number, objection, cost, or limit to make a technique work.

| Move | Required material | Allowed edit |
|---|---|---|
| Lead with a case, quotation, or precise number | The user asked to restructure, and one appears later in the text | Move it forward and cut a generic background opener such as `随着…的发展` or `在…的今天`; without such a request, ask first (Editing Contract step 4) |
| Ask, then answer | The source asks and answers the question | Place the answer right after the question; delete filler between them |
| Answer an existing claim | The negated claim appears in the source, its title, the user's request, or an explicit reader question | Keep the contrast; if no such claim exists, follow Contrast Check |
| Guard both sides | The source states two failure modes or a precondition | Keep both; do not collapse them into one-sided praise |
| Count instead of praising | The source gives figures or a comparison | Let those figures carry the claim and drop adjectives they already support |
| Mark the boundary | The source states a limit, exception, or shortfall | Keep it visible, with the source's own 当然 or 也要看到 when present; do not soften it, and do not add a boundary the source does not state |
| Admit the cost | The source states a cost or trade-off | Keep it; never add one |
| Voice the reader's question | The source contains the objection | Phrase the objection as a question and answer it with source content |
| Call back at the end | The opening holds a concrete object or phrase | If the source's ending already returns to that object or phrase, delete the slogan clause so the callback closes the piece; do not write a new closing sentence or move material across paragraphs |

## Example

Before:

> 该缓存策略的核心在于保持版本戳单调递增。故障并不是时钟漂移，而是服务重启后把版本戳恢复成了 0。修复时先恢复持久化版本戳，再重新开放流量。

After:

> 该缓存策略的核心在于保持版本戳单调递增。故障源于服务重启后把版本戳恢复成了 0。修复时先恢复持久化版本戳，再重新开放流量。

The revision drops a contrast whose negated side has no source, keeps the stated cause unchanged, and preserves a defined technical phrase and an operational dependency. Had the text said `排查初期怀疑是时钟漂移`, the contrast would stay.

## Quality Gate

- Every fact, number, name, term, citation, quotation, and required sequence still matches the source.
- No new experience, evidence, promise, motive, or conclusion was introduced.
- Changes solve an identified contextual problem; natural passages remain intact.
- The register still fits the document and author.
- No generic engagement question or assistant narration was added.
- The output follows the user's requested format; otherwise it contains only the revision.
- Fixed formulations, document titles, and quotations are character-identical to the source.
- Every qualifier, limit, exception, shortfall, or stated cost in the source survives.
- No remaining contrast negates a claim that has no source in the text, its title, the user's request, or an explicit reader question; wherever an invented target was removed, the claim it framed is unchanged.
- Every rhetorical question kept in narration is answered within the next two sentences with source content, or is quoted, dialogue, or genuinely addressed to the reader (requested CTA, survey, interview, or request to confirm). Never invent an answer to satisfy this check.
- No case, quotation, authority, number, objection, or cost was added to make a technique work, and no material was moved across paragraphs without the user's request.

## Boundaries

- Do not promise to bypass AI detectors or lower an AIGC score.
- Do not conceal plagiarism, fabricate authorship, or invent citations and personal experience.
- Do not treat a clean pattern audit as proof that writing is natural, original, or human-authored.
- Do not add slogans, authority quotations, or official formulations to make writing sound authoritative.

## Optional Pattern Audit

When this package is available locally, run the script from the skill directory or pass its full path:

```bash
python <skill-dir>/scripts/audit_ai_flavor.py draft.md --profile general
```

Profiles are `general`, `social`, `academic`, `fiction`, `sop`, `email`, and `editorial`. The script also accepts `--stdin`, glob patterns, `--json`, `--recursive`, and `--keep-terms`. Findings are candidates, not verdicts: check each one against Context Decisions, and check every `binary_contrast` finding with Contrast Check. `clear` means no configured pattern requires review; it is not a quality or authorship judgment.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Replacing every flagged phrase | Decide from meaning, register, and user constraints |
| Making all paragraphs deliberately uneven | Vary structure only when repeated symmetry is the actual problem |
| Adding anecdotes or promises to sound human | Preserve the evidence boundary |
| Removing required sequence markers | Keep operational and chronological dependencies explicit |
| Returning an explanation by default | Return only the revision unless notes were requested. When step 4 requires a question, ask it and do not send a partial revision |
