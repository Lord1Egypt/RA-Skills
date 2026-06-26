---
name: summarize-anything
description: "Extract, transcribe, clean, segment, and analyze long-form content from URLs, local media files, existing transcripts, and pasted text. Use when a user provides a podcast, video, interview, article, WeChat post, social video link, subtitle file, or transcript and wants: (1) text extraction, (2) whisper-based transcription, (3) cleaned transcripts, (4) rough speaker segmentation based on semantics, or (5) detailed summaries and insight memos."
---

# Summarize Anything

## Overview

Use this skill to turn long-form content into usable text and high-signal insights. The skill treats Codex as the workflow orchestrator: Codex decides how to acquire the content, when to call local tools, how to clean the transcript, how to assign rough speakers, and how to write the final insight memo.

## Workflow Decision Tree

1. Classify the input before doing any extraction work.
   Supported inputs:
   - A web article or social post URL
   - A video or podcast URL
   - A local audio or video file
   - An existing `txt`, `srt`, or `json` transcript
   - Text pasted directly into the prompt

2. Prefer direct text over transcription when possible, but require a full transcript body.
   - If the page already exposes readable article text, extract the text directly.
   - If the page exposes subtitles or captions, prefer those over ASR.
   - Treat direct text as successful only when a full usable transcript or article body is actually retrievable.
   - Show notes, metadata, chapter markers, comments, or internal transcript identifiers do not count as transcript acquisition.
   - If a full transcript body is not successfully retrieved, you must fall back to media acquisition and ASR.
   - Even when captions exist, still normalize them into a readable transcript and apply rough speaker segmentation if the user-facing output is conversational content.

3. Use local runtime tools for audio workflows.
   - For audio or video inputs, use the scripts in `scripts/`.
   - `scripts/ensure_whisper_cpp.sh` makes sure a local `whisper-cli` exists inside the skill runtime.
   - `scripts/ensure_whisper_model.sh` makes sure the requested ggml model exists inside the skill runtime.
   - `scripts/extract_audio.sh` converts video to wav when needed.
   - `scripts/run_whisper_cpp.sh` is the default entry point for transcription.
   - `scripts/runtime_status.sh` reports how much space the runtime currently uses.
   - `scripts/maintain_runtime.sh` warns or auto-cleans when the runtime grows beyond configured thresholds.
   - `scripts/cleanup_runtime.sh` clears temporary runtime state and can optionally prune models or build sources.

4. Treat transcript cleanup and speaker assignment as LLM tasks, not hard-rule tasks.
   - Use the model to fix obvious ASR errors from context.
   - Use the model to merge broken clauses into readable sentences.
   - Use semantic clues such as question-answer structure, self-introductions, name mentions, and topic handoffs for rough speaker segmentation.
   - Do not present speaker assignment as precise diarization unless the source explicitly supports it.
   - For interviews, podcasts, panels, and any multi-speaker conversational content, you must produce a cleaned transcript and a rough speaker-segmented transcript before writing the final insight memo, unless the user explicitly opts out.

5. Produce layered outputs instead of a single summary.
   Recommended artifacts:
   - Raw text or raw transcript
   - Cleaned transcript
   - Rough speaker transcript
   - Insight memo
   - For long-form content, expand the insight memo into a genuinely analytical memo rather than a longer recap.
   - Deliver the substantive summary directly in the assistant response. Do not hide the main analysis in a file unless the user explicitly asks for file-only output.
   - Treat any source with chapters, explicit section markers, or multiple major topic transitions as requiring a structure-aware memo, not just a summary.
   - When the user asks for a "detailed" or "in-depth" summary, default to analytical briefing depth rather than concise recap depth.

6. Personalize only when there is clear signal.
   - Use explicit preferences from the current prompt first.
   - If the environment provides a stable memory file and the workflow permits reading it, use it carefully.
   - If there is no reliable preference source, produce a general high-value insight memo instead of inventing a user profile.

## Operating Rules

### Output Language

- By default, respond in the language the user used in their message.
- If the user message is only a bare URL, file path, or other content-free pointer, use the dominant language of the source content.
- If the user message contains only a few tokens plus a URL and those tokens do not clearly indicate a preferred output language, use the dominant language of the source content.
- If the user explicitly asks for another language, follow that instruction.
- If the source is substantially bilingual, prefer the dominant spoken or written language of the source.
- Do not switch languages just because translated subtitles or metadata are available in another language.
- Translated subtitles, translated metadata, or platform-generated translation tracks do not by themselves determine the output language.

### Mandatory Fallback Rule

- For any audio or video source, you must obtain text one way or another before considering the job complete.
- If no directly readable full transcript is successfully acquired, you must attempt media acquisition and ASR before concluding the workflow.
- Do not stop after discovering:
  - a transcript identifier without transcript text
  - page metadata only
  - show notes only
  - chapter markers only
  - comments only
  - partial captions or partial text snippets
- A media job is incomplete unless one of the following is true:
  - a full transcript body was acquired directly
  - ASR was attempted on the source media
  - the source media was inaccessible and the blocker is explicitly reported

### Input Acquisition

- For articles and posts, first try normal page extraction.
- For complex social platforms, inspect the rendered page, scripts, or network requests for article text, captions, or media URLs.
- If the page is blocked, try alternate extraction paths that stay within the environment's available tools.
- For podcast or video URLs, follow this escalation path:
  1. Try direct page text extraction.
  2. Try subtitle, caption, or transcript endpoints exposed by page data, scripts, or network requests.
  3. If no full transcript is actually retrievable, immediately test whether the media URL is accessible.
  4. If the media is accessible, download or extract the media and run ASR.
  5. Only stop before ASR if the media itself is inaccessible or the user explicitly asks not to transcribe.
- If the content still cannot be acquired, explain the blocker briefly and ask for the minimum missing artifact, such as pasted text, a local file, or screenshots.

### Transcription

- Use `scripts/run_whisper_cpp.sh` as the default transcription entry point.
- Default to the `small` model unless the user asks for a different latency/quality tradeoff.
- Keep runtime artifacts inside the skill's `runtime/` tree when possible.
- Write user-facing outputs into a dedicated top-level workspace directory such as `output/summarize-anything/<job-id>/` unless the user requested another path.
- Do not scatter final artifacts across multiple top-level folders like `output/` and `outputs/`.
- If the source is not already text-first, always return a transcript artifact to the user, even if the immediate request emphasizes summary or insight.
- If direct transcript acquisition fails but the media is accessible, ASR is mandatory rather than optional.

### Transcript Cleaning

- Clean aggressively enough to improve readability, but do not rewrite the speaker's meaning.
- Fix:
  - obvious ASR homophones from context
  - malformed punctuation
  - split clauses that should be one sentence
  - repeated filler introduced by ASR
- Preserve:
  - the original stance
  - uncertainties
  - hedging
  - examples and numbers unless clearly wrong

Read `references/transcript-cleaning.md` when doing substantial cleanup.

### Rough Speaker Segmentation

- Only claim rough or semantic speaker assignment unless the source provides true diarization.
- Apply rough speaker segmentation to subtitle-derived transcripts too. Do not assume platform subtitles already align with speakers.
- Execution order for multi-speaker content: raw acquisition -> cleaned transcript reconstruction -> rough speaker grouping -> insight memo.
- Do not skip speaker grouping just because the user asked for a summary.
- Use:
  - moderator prompts
  - explicit self-introductions
  - direct address such as “胡老师你怎么看”
  - topic transitions
  - speaking style continuity
- Mark uncertain boundaries conservatively.

Read `references/speaker-segmentation.md` for the segmentation rubric.

### Insight Memos

- Avoid generic summaries.
- Match depth to source length. A multi-hour podcast or interview should not collapse into a handful of bullets unless the user explicitly asks for a short version.
- For long-form content, give the user enough analysis that they can understand the internal structure, strongest arguments, tensions, and implications without opening a sidecar memo file.
- When the source is conversational, write the memo after reviewing the speaker-segmented transcript, not directly from raw subtitles alone.
- Do not treat headings, neat outlines, or section count as the goal. The goal is to complete the minimum analysis actions described in `references/insight-template.md`.
- For multi-hour content, do at least two passes before writing:
  - pass 1: recover the structure of the source from chapters or inferred topic shifts
  - pass 2: synthesize cross-cutting claims, tensions, worldview, and implications across those sections
- Separate:
  - what was said
  - what is genuinely novel
  - what is actionable
  - what remains uncertain
- Quote or paraphrase a small number of representative moments from different parts of the source when that helps anchor the analysis.
- Do not stop at "the speaker said X." Explain why X matters, what assumption it rests on, and how it connects to other moments in the source.
- Highlight implications for knowledge workers, builders, researchers, operators, or other explicitly requested audiences.
- For Codex/OpenClaw-style users, include workflow and agentic takeaways when relevant.
- If files are also created, mention them after the in-chat analysis rather than replacing the in-chat analysis with a pointer.
- Prioritize analytical density over surface coverage. A longer response that mostly paraphrases, walks chapter-by-chapter, or lists topics is worse than a somewhat shorter response with real interpretation.
- For substantial interviews, explicitly identify:
  - the source's real central question
  - the speaker's answer to that question
  - the deeper worldview, frame, or narrative beneath the explicit claims
  - what the speaker is arguing against, resisting, or trying to redefine
  - which claims are strongest, weakest, most speculative, or most strategic
- Repeatedly move from:
  - what was said
  - to why it matters
  - what it assumes
  - what it reacts against
  - how it connects to other parts of the source
  - what follows from it

### Preferred Writing Style

- When the user asks for a detailed summary, default to an editorial analytical style rather than a sterile report style.
- Prefer opening with 1 short orienting paragraph that states:
  - what the source is ostensibly about
  - what its real central question is
  - the speaker's or source's core answer
- After that, prefer a `总摘要` or equivalent top-level synthesis section before the detailed breakdown.
- Then expand by major idea clusters, conversation arcs, or layered themes rather than by raw chronology alone.
- Use headings that sound like analytical section titles, not database labels.
- Favor prose-first explanation. Bullets are allowed for compact enumerations, but the default should feel like a well-edited long-form article.
- In Chinese, prefer writing that reads like a strong magazine-style or essay-style briefing:
  - clear thesis up front
  - smooth transitions
  - interpretation mixed with recap
  - selective emphasis on the most revealing moments
- Do not let the response become an outline dump, timestamp dump, or chapter paraphrase with decorative headings.
- When useful, use a structure similar to:
  - brief framing paragraph
  - `总摘要`
  - `按内容结构详细总结` or another natural equivalent
  - concluding section such as `最核心的观点`, `最有价值的地方`, or `值得注意的局限`
- If the source naturally supports it, surface 4-8 especially important claims or patterns near the end in a compact synthesis block.
- Preserve warmth and readability. The result should feel like a thoughtful human editor explaining why the source matters, not a transcript processor describing what appeared in sequence.

### Depth Over Structure

- Do not optimize for a fixed number of sections, a chapter-by-chapter recap, or a polished chronological notes dump.
- Optimize for depth.
- A response is not good enough if it mainly:
  - summarizes what was said in order
  - paraphrases the speaker more clearly without adding interpretation
  - presents observations without explaining why they matter
  - reads like an expanded recap rather than an argument about the source

### Evaluation Requirement

- For long-form interviews, lectures, and conversations, include judgment, not just explanation.
- At minimum, assess:
  - the strongest ideas or arguments
  - the weakest or least-supported claims
  - unresolved questions
  - what the speaker may be overstating, understating, romanticizing, or strategically framing

### Long-Form Enforcement

- For interview, podcast, or lecture content longer than 180 minutes, the final in-chat response must be a full analytical memo, not a short summary.
- The response must have substantial length for the chosen output language.
- As a normal minimum bar:
  - use roughly `1800-3000` characters when writing in Chinese, Japanese, or similarly dense scripts
  - use roughly `1200-2000` words when writing in English or similarly spaced languages
- Length is a support signal, not the goal. A response that meets the length bar but remains mostly recap, topic listing, or chronological summary still fails.
- The memo must explicitly cover:
  - the top-level thesis
  - the source's real central question
  - the conversation arc or source structure
  - cross-cutting themes or recurring tensions
  - what the speaker is arguing against
  - strongest claims
  - weakest or speculative claims
  - implications
  - unresolved questions
- If the answer feels compressible into a few paragraphs, or if it mainly reads like a better-organized recap, it is too shallow unless the user explicitly requested brevity.

Read `references/insight-template.md` before writing the final memo.

## Default Output Contract

When the user does not specify a format, aim for these four deliverables:

1. Raw acquisition artifact
   - article text, captions, or raw transcript
   - mandatory for non-text inputs

2. Cleaned transcript
   - readable paragraphs and corrected punctuation
   - mandatory for non-text inputs, including caption-derived inputs

3. Rough speaker transcript
   - semantic speaker tags with uncertainty kept conservative
   - expected for interviews, podcasts, panels, and subtitle-derived conversations unless the source already has reliable speaker tags

4. Insight memo
   - deep analysis that synthesizes the source rather than merely recapping it

For long-form content such as multi-hour podcasts, lectures, or interviews, the default memo should include:

1. A clear central thesis
2. Enough structure that the reader can recover the flow of the source
3. Cross-cutting patterns that recur across different parts of the source
4. The larger narrative, assumption, or worldview the speaker is reinforcing or pushing against
5. The most non-obvious or decision-relevant takeaways
6. Open questions, tensions, or disagreements that remain
7. What the speaker is implicitly arguing against
8. What parts of the argument appear strongest, weakest, or most speculative
9. Who should care and what they should update their view on

When the source is an interview, podcast, or lecture and the user asks for a detailed summary, prefer this response shape unless the user requests another format:

1. A short framing paragraph
2. `总摘要`
3. A detailed section organized by major content arcs or layered themes
4. A compact closing synthesis of core viewpoints, stakes, or implications

For especially long interview-style content, prefer this execution order:

1. Identify the source's real central question
2. Reconstruct the conversation arc by chapter or topic blocks
3. Identify the major claims, contrasts, or frames that organize the whole conversation
4. Test those claims against moments from multiple parts of the source
5. Write the memo as an analytical briefing, not as an expanded recap

In normal use, present the insight memo directly in the chat response.
Use files for transcript artifacts and optional supporting materials, not as a substitute for the main answer.

A multi-speaker media job is not complete if it returns only an insight memo without a cleaned transcript and a rough speaker transcript, unless the user explicitly requested summary-only output.

## Delivery Order

For long-form content, always do this order:

1. full in-chat analytical memo
2. brief note about transcript or artifact files
3. caveats about subtitle quality, translation quality, or speaker uncertainty

Never lead with artifact references.
Never compress the memo just because files were created.
Do not replace the in-chat analysis with a file pointer unless the user explicitly asked for file-only output.

## Failure Modes

The job is incomplete if the final in-chat answer is primarily:

- a short recap
- an executive summary under the long-form minimum bar
- a pointer to saved files
- a topic list without cross-section synthesis
- a chapter recap without evaluation, tensions, or implications
- a clearer paraphrase of the source that still does not identify deeper logic, assumptions, or stakes

Creating transcript files does not reduce the obligation to provide a full in-chat analytical memo.

## Bare URL Rule

If the user provides only a URL or media file without format instructions:

- infer the output language using the Output Language rules above
- default to the full long-form memo when the source itself is long-form
- do not default to brevity

## Not Sufficient For Completion

The following do not count as successful transcript acquisition:

- show notes
- chapter markers
- episode descriptions
- comments
- internal IDs such as `transcriptMediaId`
- evidence that a transcript may exist internally
- partial visible transcript snippets

If only these are available, continue to media download and ASR fallback.

## Required Checklist For Media URLs

Before finalizing a response for a media URL, verify all of the following:

- Did I obtain a full transcript body?
- If not, did I attempt media download or extraction?
- If media download or extraction was possible, did I run ASR?
- If I did not run ASR, is there a concrete blocker preventing media access?
- Am I relying only on show notes, metadata, or comments? If yes, the workflow is not complete unless the user explicitly requested summary-only output.

## Pre-Final Checklist

Before finalizing, verify all of the following:

- Is the response written in the correct output language?
- If the user message was only a bare URL or file, did I choose the source's dominant language rather than a translated metadata language?
- Is the in-chat analysis above the long-form minimum bar when the source is long-form?
- Did I explain the structure of the source, not just list topics?
- Did I synthesize claims across multiple sections or chapters?
- Did I include strengths, weaknesses, uncertainties, and implications?
- Did I identify the source's central argument rather than merely its visible topics?
- Did I explain what is genuinely insightful, contested, or strategically framed here, rather than just what was mentioned?
- If someone read only my response, would they understand the deeper logic of the source rather than just its table of contents?
- Am I relying on transcript files instead of the response body? If yes, expand the response.

## References

- Read `references/workflow.md` for the acquisition decision tree and output policy.
- Read `references/invocation-examples.md` for reusable prompt templates.
- Read `references/transcript-cleaning.md` when cleaning ASR-heavy transcripts.
- Read `references/speaker-segmentation.md` when the content is multi-speaker.
- Read `references/insight-template.md` before writing the final analysis.

## Skill Layout

- `SKILL.md`
  - The routing logic and operating rules.
- `agents/openai.yaml`
  - UI-facing metadata only.
- `scripts/`
  - Deterministic local helpers for runtime bootstrap and transcription.
- `references/`
  - Guidance for cleanup, segmentation, output shape, and example invocations.
- `runtime/`
  - Skill-managed runtime state created on demand.
  - `bin/` for local executables
  - `models/` for ggml models
  - `cache/` for downloads and reusable fetches
  - `src/` for locally built tool sources when needed
  - `work/` for temporary files and smoke-test artifacts

## Runtime Notes

- This skill is designed to feel self-contained.
- The first run may bootstrap local runtime dependencies into `runtime/`.
- Prefer reusing the skill-local runtime after bootstrap instead of depending on ambient system state.
- Prefer writing user-facing deliverables into the current workspace or a user-requested path, not into `runtime/`, unless the artifact is explicitly internal.
- Treat `runtime/work/` and `runtime/cache/` as reclaimable space.
- `scripts/maintain_runtime.sh` runs automatically in bootstrap and whisper flows.
- By default it warns at `1536MB` and auto-cleans `runtime/cache/` and `runtime/work/` at `2048MB`.
- Override thresholds with `CONTENT_INSIGHT_RUNTIME_WARN_MB` and `CONTENT_INSIGHT_RUNTIME_CLEAN_MB`.
- Use `scripts/runtime_status.sh` before or after large jobs when size matters.
- Use `scripts/cleanup_runtime.sh` after large jobs to clear temporary files.
