# Subtitle Cleanup Guide

Reference for the **interpretive** phase of transcript cleanup (Step 7 in SKILL.md). The deterministic phase (timestamp stripping, segment merging) is handled by `scripts/srt_to_sentences.py`. This document covers what the script cannot do: ASR error correction, filler removal, and lightweight sectioning.

---

## Output Language Principle

The cleaned transcript **stays in the source language of the video**. If the speaker spoke Japanese, the transcript is in Japanese; if they spoke English, it is in English; if they spoke Mandarin, it is in Mandarin. Translation only happens when the user explicitly requests it.

This document gives concrete word lists in **Chinese and English** because they are the two languages most commonly encountered. The lists are **examples**, not the full universe — when working on a video in another language (Japanese, Korean, French, etc.), use the same *categories* (stance words, hedge words, discourse connectives, fillers) and apply the same judgment to that language's vocabulary. The principles are language-agnostic; the example tables are not.

---

## Core Principles

1. **Preserve original wording.** The output is a transcript, not a summary or rewrite. The reader should hear the speaker's voice — in their own language.
2. **Edit conservatively.** When uncertain whether to remove a phrase, keep it.
3. **Domain-aware correction.** ASR errors cluster around proper nouns and jargon. Fix these aggressively; do not invent corrections for ambiguous content.
4. **Preserve argument order.** Do not reorder paragraphs or rearrange the speaker's logic flow.
5. **Do not translate** unless the user explicitly asks. The default is "same language as the source video."

---

## How to Identify ASR Errors

ASR engines (B站 AI 字幕、YouTube 自动字幕) systematically mishear in predictable categories. Instead of relying on a fixed dictionary, identify candidates by these signals:

### Signals of likely ASR error

| Signal | Example | Detection method |
|---|---|---|
| Word makes no sense in context | "...这个机制大有**弊益**..." | Re-read the sentence; if meaning breaks, suspect homophone |
| Strange transliterated foreign term | "塔科夫**莱克**" | Try reverse-mapping to common English suffixes (-like, -ish, -er) |
| Numbers stuck inside words | "塔科夫**1**2018年" | Extra digits often replace short connecting words (于/在/到) |
| Inconsistent capitalization in English | "arc raiders" | Compare against the proper noun's standard form |
| YouTube auto-captions with no punctuation | entire paragraph as one stream | Sentence-split by length + topic shift |
| Speaker self-reference garbled | "我**杀龟** prime" | Compare against video metadata (uploader name, title) |

### Correction discipline

Apply corrections only when **all three** are true:

1. The error is unambiguous (only one reasonable correct reading exists in context)
2. The correct form can be verified against external evidence — video title, video description, channel name, web search for poem/quote citations, or earlier/later occurrences in the same transcript
3. The correction does not change the speaker's argument, only its surface form

**When ambiguous, trim rather than annotate.** Do not put margin notes / confidence markers in the deliverable. The transcript is for a reader, not a reviewer. Choose one of:

- **Commit** to a correction if confidence is high (apply silently to the body)
- **Trim** the unresolvable fragment if it's at a natural boundary (sentence end, paragraph end, video end)
- **Keep the original ASR text verbatim** if the fragment is mid-flow and trimming would break continuity — readers can decode minor errors themselves better than they can decode meta-annotations

What you must NOT do in the deliverable:

```
原文：我们要研究[？此处识别为"车离"，可能为"撤离"或"车厘"]玩法    ← FORBIDDEN
```

If you find yourself wanting to write something like this, that's the signal you haven't decided yet. Decide first, then deliver.

### Build a per-video glossary first

Before doing line-by-line correction, **scan the full raw transcript once** and write down 5-15 likely proper nouns or jargon that recur with inconsistent ASR spellings. Verify each against:

- The video title and description (check the video page metadata)
- Channel name and uploader info
- Any on-screen text mentioned by the speaker

Then apply corrections consistently across the entire transcript. This avoids the trap of fixing "撤离" in paragraph 3 while leaving "车离" in paragraph 7.

### What ASR usually gets right (don't over-correct)

- Common verbs and adjectives in the source language
- Sentence-level grammar
- Frequent function words (Chinese 的/了/吗/呢, English articles and auxiliaries, Japanese particles like の/は/が, etc.)
- Numbers (digits, not number-words)

Most "errors" you spot in a quick read are actually correct. The rule of thumb: if you have to think about whether it's wrong, it probably isn't.

---

## Words to KEEP (do not remove)

**Read this section before reading the next one ("Filler Words to Remove").** Many seemingly-redundant words carry the speaker's stance, hedging, or emphasis. Removing them flattens the speaker's voice and is one of the most common over-cleanup mistakes.

### What categories to preserve (language-agnostic)

Regardless of source language, preserve words and phrases that fall into these categories:

1. **Stance / intensifier words** — signal the speaker's judgment, summary, or concession. Removing them changes meaning, not just style.
2. **Hedge words** — signal genuine uncertainty or qualification. Remove only when the word is clearly meaningless filler in context (rare).
3. **Discourse connectives** — structure the argument flow (contrast, cause, addition, result). Removing them produces choppy, hard-to-follow text.

The example tables below cover Chinese and English. For other languages, identify equivalents in the same categories.

### Examples — Chinese

```
Stance / intensifier:
确实、其实、的确、真的、本身、归根结底、总的来说、大体上、说到底、毕竟

Hedge:
可能、也许、应该、大概、似乎、看上去

Discourse connectives:
那么、不过、然而、但是、所以、因此、此外、另外
```

### Examples — English

```
Stance / intensifier:
actually (when emphasizing contrast), really, honestly, truly,
admittedly, ultimately, fundamentally, in essence

Hedge:
might, maybe, probably, presumably, seemingly, somewhat

Discourse connectives:
however, but, so, therefore, also, moreover, on the other hand
```

If a word in any of these categories looks like filler in a particular sentence, leave it. Better to keep a slightly redundant word than to alter the speaker's tone.

---

## Filler Words to Remove

Remove these only when they're clearly fillers (no semantic load). When a word listed below also appears in "Words to KEEP" with a different sense, default to keeping.

### What to identify as filler (language-agnostic)

1. **Hesitation sounds** — non-lexical vocalizations the speaker would not write down (English "um/uh", Chinese 嗯/啊/呃, Japanese えー/あの, etc.).
2. **Verbal tics** — short phrases the speaker uses reflexively between clauses without semantic load.
3. **Stalling deictics** — pronouns or demonstratives used as time-buying placeholders rather than to point at a referent.
4. **Same-meaning repeated tags** — confirmation tags repeated every sentence (English "right?", Chinese 对吧/是吧, Japanese ね).

The same word can be a filler in one sentence and a meaningful word in another — context decides. Examples below are starting points, not blanket-remove lists.

### Examples — Chinese

```
嗯、啊、呃、哎、那个 (when not deictic)、这个 (when not deictic)、
然后 (when used as verbal pause, not as a connective)、
就是说、也就是说、对吧、是吧、什么的、之类的、
我觉得吧、其实吧 (the 吧-suffixed redundant variants)
```

Note the distinction between `其实` (keep — see "Words to KEEP") and `其实吧` (often a redundant verbal tic — remove). Same for `然后` (connective, keep) vs filler `然后` (between every clause, remove some).

### Examples — English

```
um, uh, like (when not a comparison), you know, basically (when redundant),
sort of, kind of, I mean, right? (rhetorical), okay so (sentence-starter)
```

Same distinction: `actually` as "really" (keep) vs `actually` as a generic emphasis filler (remove).

---

## Sectioning Heuristics

The speaker often signals topic transitions with explicit phrases. Use these as natural cut points for `##` / `###` headings.

### Strong signals (insert `##` heading)

- "我们来聊一聊…"
- "今天我们谈…"
- "回到主题…"
- "下一个大类是…"
- "换一个角度看…"
- "Let's talk about…"
- "Moving on to…"

### Medium signals (insert `###` heading)

- "第一个是…" / "第二个是…" / "最后一个是…"
- "首先…" / "其次…" / "最后…"
- "举个例子…"
- "First…", "Next…", "Finally…"

### Weak signals (paragraph break only, no heading)

- "另外…" / "顺便说一下…"
- "不过…" / "但是…" (these are arguments, not topic shifts)

### When the video has no structural signals

Some videos — casual chats, vlogs, reaction streams, freeform interviews — have no explicit "first / next / finally" markers and no topic-shift declarations. **Do not invent structure that isn't there.**

Decision rule:

- If a full read of the normalized transcript yields **fewer than 3 strong-or-medium signals**, do not add `##` / `###` headings at all
- Output the transcript as a single section under the video title (or as 2-3 untitled paragraphs separated by blank lines)
- The reader should still be able to follow because the speaker's natural flow carries the structure

Forcing artificial headings on unstructured speech makes the transcript feel like a fake summary written by an AI — exactly what this skill exists to avoid.

### Heading style rules

- Keep headings **short** — roughly ≤ 10 CJK characters or ≤ 6 words for alphabetic languages
- Keep headings **descriptive**, not interpretive (don't add value judgments not in the video)
- Match the speaker's terminology — if they say "局外体验", the heading is "局外体验" not "Long-term experience"; if they say "level streaming", keep "level streaming" not a translation
- Headings stay in the **source language** of the video

---

## Worked Example

For a full walkthrough on a real (87-second) Bilibili video — including ASR glossary, sectioning analysis, and the final deliverable — see **`worked_example.md`**. Read it once when learning the methodology; skip when you just need the rules above.

---

## Output Skeleton Template

The header label set follows the **source language**. Two common variants below; for other source languages, translate the labels into a natural local convention.

### English source

```markdown
# <Video title>

> **Source**: <platform> ｜**URL**: <URL>
> **Duration**: <mm:ss> ｜**Published**: <YYYY-MM-DD>
> **Captions**: <auto-generated / human-uploaded>

---

<paragraph 1...>

<paragraph 2...>

<paragraph 3...>
```

### Chinese source

```markdown
# <视频标题>

> **来源**：<平台> ｜**链接**：<URL>
> **时长**：<mm:ss> ｜**发布**：<YYYY-MM-DD>
> **字幕来源**：<AI 自动字幕 / 人工上传字幕>

---

<paragraph 1...>

<paragraph 2...>

<paragraph 3...>
```

If the video has clear structural signals, insert `##` / `###` headings between paragraphs; otherwise output continuous prose as above. Headings stay in the source language too.

The transcript is the deliverable to a reader. **Do not** include:
- Cleanup notes / "整理说明" / "Changes applied" tables
- Footnote references for ASR corrections
- Confidence/uncertainty annotations
- Margin notes meant for internal review
- Tool versions, file paths, or other technical metadata

If a particular passage cannot be cleaned with high confidence, prefer to **trim** the ambiguous fragment over inserting placeholder text or annotations in the deliverable.

---

## What NOT To Do

- **Do not paraphrase.** If the speaker didn't say a sentence, don't add it.
- **Do not summarize.** This is a transcript, not a study note. Keep all the speaker's examples and digressions.
- **Do not add citations or hyperlinks** the speaker didn't mention.
- **Do not add footnotes for ASR corrections.** Corrections go silently into the body text. If a passage is too ambiguous to fix, trim it rather than annotate.
- **Do not include a "changes applied" / "整理说明" table** in the deliverable. The reader wants the transcript, not a diff log.
- **Do not include margin notes / confidence markers / `[？...]` placeholders** in the final output. Those are internal artifacts; resolve them by either committing to a correction (when confident) or trimming the fragment (when not).
- **Do not reorder.** Preserve the speaker's argument sequence even if a different order seems more logical.
- **Do not fabricate corrections.** If an ASR fragment is ambiguous and unverifiable, trim it. Do not guess.
- **Do not translate** unless the user explicitly asks.
- **Do not impose structure on unstructured speech.** See § "When the video has no structural signals".
