# Output format

How a summary is presented depends on the mode.

- **Full mode**: youtube2md has already produced a complete, detailed Markdown summary. Output that Markdown **verbatim** as the final answer — do not condense it, re-summarize it, drop chapters or bullets, or reflow it into the compact template below. Append only the `Mode: full` line at the end. The package's detail (which scales with video length and the `--detail` level) is the deliverable; preserve it in full.
  - Since youtube2md 1.2.0 the package's own `## Summary` is a short orientation (a few sentences, at most 8) while `## Chapters` holds the detail. That asymmetry is intentional — pass it through untouched. Do not expand or re-narrate the Summary, and do not treat its brevity as a sign the run under-delivered.
- **Simple / transcript modes**: Claude authors the summary from the transcript. Use the structure below.

## Preferred structure — simple / transcript-derived summaries (Markdown)

```md
# <Video Title>

> [Watch on YouTube](<canonical_url>) | Duration: <MM:SS> | Published: <YYYY-MM-DD>

## Summary
<1 paragraph (3-8 sentences) orienting the reader: what the video covers, the through-line, and the conclusion/verdict it lands on — specifics go in the chapters>

## Chapters
### <Chapter 1 title>
- <fact-based bullet>
- <fact-based bullet>

### <Chapter 2 title>
- <fact-based bullet>
- <fact-based bullet>

## Key Takeaways
- <practical takeaway>
- <practical takeaway>
- <practical takeaway>

Mode: <full|simple|simple (fallback from full; no summarization provider available)>
```

For transcript-only requests, use the requested transcript format and end with:

```md
Mode: transcript
```

## Section rules

These rules apply to **simple / transcript-derived** summaries that Claude authors. In full mode the package's Markdown is passed through verbatim, so these counts do not apply — never trim the package output down to them.

- **Summary**: write one compact narrative paragraph, not fragmented mini-bullets. Orient the reader and state the conclusion/verdict (answer the title outright when it poses a question); leave the supporting facts, figures, and caveats to the chapter bullets rather than duplicating them here.
- **Chapters**: chronological sections with short headings; each section should have 2-4 bullets. Bullets should explain what changed or was learned in that section, not just restate the topic.
- **Key Takeaways**: 6-10 bullets, practical and decision-oriented. Emphasize what matters, why it matters, and any constraints.
- **Scale with length**: the counts above are baselines for a ~10-30 minute video. For longer or denser videos, expand the chapters and bullets proportionally rather than compressing everything into the minimum; the Summary paragraph stays short (a second paragraph only for very long videos).
- **Mode line**: always end each video result with one plain line showing the actual user-facing mode used: `Mode: full`, `Mode: simple`, `Mode: simple (fallback from full; no summarization provider available)`, or `Mode: transcript`.
- Keep numbers/units explicit when present (price, speed, ping, watts, distance, dates).
- For Korean videos or Korean user requests, write natural Korean with enough context; avoid overly compressed note-style Korean.

## Source-policy-aware usage

- **Full mode succeeded**: the youtube2md Markdown output (`.md`) **is** the final summary. Present it verbatim (appending only the mode line); do not treat it as raw material to re-summarize or shorten.
- **Simple mode**: Claude summarizes from the timestamped transcript text (`.txt`) written by the CLI extract path (`--extract-format timestamped-text`), using the structure above.
- **Transcript mode**: return transcript content or requested transcript artifact details, not a summary.

## Delivery — inline, never as a file

- Deliver the summary as **inline Markdown in the reply itself**, in full. This holds no matter how long it is — a 3-hour video with 100+ timestamped chapters still gets its complete summary pasted into the response.
- **Never** replace the summary with a file attachment, a download/link, or a meta-description of it (e.g. "the summary is long, so I attached it as a Markdown document with 116 chapters and key takeaways"). Length is never a reason to attach, truncate, collapse, or summarize-the-summary.
- The runner writes a `.md/.txt/.json` file as a side effect of running youtube2md; that file is an artifact, not the deliverable. Do not surface its path by default, and do not hand the file over in place of the content.
- Produce a file/export or share a path only when the user explicitly asks for one.

### Transports with a message-size cap

Channels cap a single message (Telegram ~4096 characters, Slack ~4000), but **the host splits long text for you — do not split it yourself.**

- Send the **entire** summary in one reply / one send call, however long it is. openclaw chunks outbound text at `textChunkLimit` (default 4,000 characters) and sends every chunk in a loop, so an 11,352-character summary goes out as 5 Telegram messages from a single send.
- **Never** hand-split into `(1/3)`, `(2/3)`, `(3/3)` parts and send them one call at a time. Under openclaw's codex-app-server backend, the first successful `message` tool call is **turn-terminal**: it interrupts the model turn (`turn.dynamic_tool_terminal_release`), so parts 2..n are never sent and the reader gets only part 1. Manual splitting causes the exact truncation it is meant to prevent.
- Symptom of having done it anyway: the reader sees a message literally starting with `(1/3)` and nothing after it. See troubleshooting entry 8a.
- Length is still never a reason to shorten, attach a file, or link to the output path.
