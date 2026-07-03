# youtube-summary behavior

This file defines how summaries are produced across modes.

## Modes and summary source

- **Full mode** (`run_youtube2md.sh <url> full ...`)
  - Use first when `OPENAI_API_KEY` is visible/available and external API use is acceptable.
  - `youtube2md` generates Markdown summary output.
  - The runner passes `--model gpt-5.4-mini` by default unless overridden.
  - Use generated `.md` as the canonical summary source.
  - Do not re-summarize from raw transcript unless the user asks for a rewritten style.

- **Simple mode** (`run_youtube2md.sh <url> extract ...`, internally `--extract-only` + prepared `.txt`)
  - Use for summary requests when `OPENAI_API_KEY` is unavailable, content is sensitive, external API use is not acceptable, or full mode falls back.
  - `youtube2md` generates transcript JSON.
  - Runner then executes `prepare.py` to generate transcript text (`.txt`) from `segments[].text`.
  - Summarize using the prepared `.txt` as the primary source.
  - In user-facing output, call this `simple` mode, not `extract` mode.

- **Transcript mode** (`run_youtube2md.sh <url> extract ...`, internally `--extract-only`)
  - Use only when the user asks for transcript extraction, transcript-only output, raw transcript, captions, or machine-readable transcript JSON.
  - Return transcript content or requested transcript artifact details, not a summary.
  - In user-facing output, call this `transcript` mode, not `extract` mode.

## youtube2md 1.0.2 behavior to preserve

- This skill runner defaults full mode to `gpt-5.4-mini`; override with the fifth runner argument or `YOUTUBE2MD_DEFAULT_MODEL`.
- The upstream youtube2md package defaults to `gpt-5-mini` only when no model is passed directly.
- Long transcripts are chunked internally by youtube2md; trust its Markdown result when full mode succeeds.
- Transcript retrieval tries captions first, then an alternate transcript parser, then Whisper STT when `OPENAI_API_KEY` is available.
- YouTube cookie env vars may improve captions/audio access for videos blocked to anonymous requests.

## Simple-mode summarization workflow

1. Load metadata (title, duration, publish date, URL/video id) from JSON when available.
2. Load transcript text from `.txt`.
3. Build a structured summary in this order:
   - `## Summary` (single dense paragraph)
   - `## Chapters` (chronological thematic sections)
   - `## Key Takeaways` (practical bullets)
4. Preserve factual values exactly when mentioned (prices, throughput, ping, wattage, dates).

## Summary density

- Prefer a compact but substantial summary: enough detail to preserve the argument, setup, evidence, caveats, and conclusion without becoming a transcript rewrite.
- Include the speaker's conclusion or stance when it is clear from the transcript.
- If the transcript is mostly exploratory, preserve that uncertainty instead of forcing a stronger conclusion.

## Chaptering heuristics

- Prefer **3-7 chapters** for ~10-30 minute videos.
- Use concise section titles (topic/action based).
- Keep each chapter bullet list factual (2-4 bullets).
- Chapter bullets should explain what changed, what was tested, what evidence appeared, or what the viewer learned in that section.
- Avoid duplicate bullets across chapters.

## Key takeaways heuristics

- Prefer **6-10 takeaways**.
- Prioritize user-facing decisions:
  - when to use / when not to use
  - performance expectations and variability
  - cost and operational tradeoffs
- Include caveats and constraints (installation conditions, environment assumptions).
- Make takeaways decision-useful: what matters, why it matters, and any constraint that changes the decision.

## Mode disclosure

- End every user-facing video result with the actual mode used.
- Use `Mode: full` when youtube2md full mode produced the summary Markdown.
- Use `Mode: simple` when the summary was generated from prepared transcript text.
- Use `Mode: simple (fallback from full; OPENAI_API_KEY unavailable)` when full mode was requested but the runner switched to simple mode.
- Use `Mode: transcript` when the user requested transcript-only output.
- Do not use `Mode: extract` in user-facing output; `extract` is only the internal CLI/runner name.

## Language and uncertainty

- Keep summary language aligned with transcript/user language (Korean transcript -> Korean summary unless requested otherwise).
- For Korean videos or Korean user requests, write natural Korean with complete context, not overly compressed bullet-note Korean.
- When transcript quality is noisy or speech is unclear, summarize stable facts and mark uncertain details as uncertain.

## Quality guardrails

- Do not hallucinate specs, pricing, benchmarks, or policy claims.
- Preserve uncertainty from unclear speech or ambiguous transcript segments instead of smoothing it into confident claims.
- Keep the tone concise and useful; do not add analysis that is not grounded in the video.
