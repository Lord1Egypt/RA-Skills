# Invocation Examples

## Article URL

Use when the user gives a web article, newsletter, or WeChat link.

```text
Use $summarize-anything to process this article URL.
Extract the article text directly if possible.
Then produce:
1. cleaned article text
2. a structured summary
3. a detailed insight memo focused on non-obvious takeaways
```

## Video or Podcast URL

Use when the user gives a social video, podcast episode, interview, or talk link.

```text
Use $summarize-anything to process this video or podcast URL.
Try to extract captions first; if captions are not available, acquire media and transcribe it with the skill-local whisper runtime.
Then produce:
1. raw transcript
2. cleaned transcript
3. rough speaker segmentation
4. a detailed in-chat insight memo with chapter or topic breakdown if the content is long-form
5. for multi-hour content, reconstruct the conversation arc first, then write an analytical memo that includes:
   - top-level thesis
   - major sections and why they matter
   - cross-cutting patterns
   - strongest claims and hidden assumptions
   - tensions, contradictions, and open questions
   - why the content matters beyond the conversation itself
5. mention any saved transcript files only after giving the full analysis
```

## Detailed Summary Request

Use when the user explicitly asks for a "detailed", "deep", or "thorough" summary.

```text
Use $summarize-anything on this content.
Do not give a compact recap.
Write it in an editorial long-form style, not as a sterile report.
Start with a short framing paragraph, then give a `总摘要`, then expand by major content arcs or layered themes.
Write an analytical briefing that first reconstructs the source's internal structure, then explains the deeper logic, strongest claims, tensions, and implications.
For long conversational content, explicitly separate:
1. what happened in the conversation
2. what the speaker seems to believe
3. what is genuinely non-obvious or decision-relevant
4. what remains ambiguous or weakly supported
```

## Existing Transcript

Use when the user already has `txt`, `srt`, or `json`.

```text
Use $summarize-anything on this transcript.
Clean obvious ASR errors conservatively, assign rough speakers based on semantics, and write a detailed in-chat insight memo.
```

## Codex / OpenClaw-Oriented Memo

Use when the user cares about builders, operators, or agentic workflows.

```text
Use $summarize-anything on this content.
In the final memo, emphasize:
- workflow implications
- agent or tool-use takeaways
- reusable decision patterns
- concrete next steps for Codex or OpenClaw users
```

## Explicit Personalization

Use when the user gives a role or preference in the prompt.

```text
Use $summarize-anything on this content.
Write the final insight memo for a founder audience with a strong product and strategy focus.
```
