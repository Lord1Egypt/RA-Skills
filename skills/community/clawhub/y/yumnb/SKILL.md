---
name: yumnb
description: "Yum NoteBook — a local-first NotebookLM alternative for AI agents, built for real source capture. Ingest a web URL, YouTube video, or screenshot, then generate (1) AI summary, (2) dual-host talk-show MP3 (edge-tts), (3) slide deck (image/table/bullet/flowchart) and optionally upload artifacts to OneDrive/Google Drive/S3/etc. and post a notification to Slack/Discord/Teams. Language and cloud destination are user-configurable; defaults to English with male+female English hosts. Use when: yumnb, study notes, summarize this link, turn this video into notes, help me understand this article."
argument-hint: "URL | YouTube link | path to screenshot (and optional --title / --language)"
---

# Yum NoteBook (yumnb) — Source → Summary + Talk-show + Slides

> **A local-first NotebookLM alternative for AI agents, built for real source capture.**

## What It Does

Given a source (URL / YouTube / screenshot / raw text), creates **one folder per
request** under `<output_dir>/<YYYYMMDD-HHMM-slug>/` containing:

1. **`source/`** — raw material (downloaded HTML, transcript, screenshot copy …)
2. **`summary.md`** — AI summary (one-liner / key points / facts / takeaways)
3. **`talkshow.txt` + `talkshow.mp3`** — dual-host script + MP3 (edge-tts)
4. **`deck.pptx`** — slide deck (bullets, tables, flow, images, summary)
5. **`links.json`** — record of what was generated and any share links

This “one request = one folder” model is intentional: many such folders can
accumulate into a local knowledge base that can be read, searched, narrated,
and presented later.

If a webhook is configured, a notification is posted to Slack / Discord /
Teams Workflow. If `deliver.provider` is configured, yumnb can also push the
finished outputs directly to an IM/chat surface through OpenClaw / Hermes
(Telegram / Discord / Teams / Slack / etc.).

You can position yumnb as a local-first, polite alternative to NotebookLM:
it keeps notebooks and generated artifacts as ordinary local files by default,
then only uploads or delivers them if you explicitly configure that.

## Two Ways to Run

### A. Fully-automatic (built-in AI provider)

Configure `ai.provider` in `config.yaml` (openai / anthropic / gemini /
ollama / cli) and run:

```bash
python -m yumnb auto "<URL or path>" [--title "short name"]
```

This runs ingest → AI summary → AI slide-plan → TTS → PPT → publish in one
shot.

### B. Step-by-step (agent-driven — you bring your own LLM)

If you're driving this from an agent CLI (GitHub Copilot CLI, Claude Code,
Cursor, Aider, …), set `ai.provider: none` and call the subcommands
individually. The agent reads the source, writes `summary.md` and
`deck.json` itself, then asks yumnb to render TTS / PPT / publish.

```bash
# 1) Pull raw material
python -m yumnb ingest "<URL>" [--title "..."]
#    → prints the note folder path

# 2) (Agent writes <folder>/summary.md following the schema in README)

# 3) Render dual-host MP3 from a talkshow script the agent wrote
python -m yumnb tts "<folder>/talkshow.txt" --output "<folder>/talkshow.mp3"

# 4) Render PPT from a deck.json the agent wrote
python -m yumnb ppt "<folder>/deck.json" --output "<folder>/deck.pptx"

# 5) Finalize + optional webhook / IM delivery
python -m yumnb publish "<folder>"
```

## Schemas the Agent Writes

### `summary.md`

```markdown
# <title>

> **Source**: <url or file>
> **Type**: youtube|url|image|text
> **Length**: <duration or word count>

## 🎯 One-line summary

## 📌 Key points (3-5)

## 🔑 Facts / data

## 💡 Takeaways

## 🤔 Open questions
```

### `deck.json` (rendered to `deck.pptx`)

```json
{
  "title": "Deck title",
  "subtitle": "Source / date",
  "slides": [
    {"type": "title",      "title": "...", "subtitle": "..."},
    {"type": "bullets",    "title": "...", "bullets": ["...", "..."]},
    {"type": "table",      "title": "...", "headers": ["A","B"], "rows": [["1","2"]]},
    {"type": "flow",       "title": "...", "steps": ["Step 1","Step 2","Step 3"]},
    {"type": "image",      "title": "...", "image_path": "/abs/path.png", "caption": "..."},
    {"type": "two_column", "title": "...", "left": "bullet text", "image_path": "..."},
    {"type": "summary",    "title": "...", "text": "..."}
  ]
}
```

Recommended: **5–12 slides** — title, 1-2 overview, 3-6 main (bullets/table/
flow/image), 1 summary. Reuse images from `source/` (YouTube thumbnail,
HTML hero image, original screenshot).

### `talkshow.txt`

Lines tagged with `[<SpeakerName>]` where `<SpeakerName>` matches a voice
configured in `config.yaml` → `tts.voices`. Example:

```
[HostA] Welcome to the show — today we're chewing on…
[HostB] And by chewing I mean ruthlessly mocking, right?
[HostA] Pretty much.
```

## Prerequisites

- Python 3.9+
- Preferred first-run: `./scripts/bootstrap.sh`
- Or manual: `pip install -r requirements.txt`
- Plus the AI SDK matching your provider (only one): `openai` / `anthropic` /
  `google-generativeai` / `ollama` — or none if you use `provider: cli` /
  `none`.

## Notes

- `edge-tts` uses Microsoft's free online voices. No API key required.
- The intro/outro jingle is generated procedurally in pure Python — no
  external assets bundled.
- YouTube ingest order is: yt-dlp manual subtitles → yt-dlp auto subtitles →
  `youtube-transcript-api` fallback → description-only fallback.
- This skill carries no platform/tenant/organization-specific defaults.
  All endpoints and credentials come from `config.yaml` or environment
  variables (`YUMNB_*`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.).
- Direct IM delivery is channel-agnostic: configure `deliver.provider:
  openclaw` (or `hermes`) plus `deliver.openclaw.channel` + `target` to send
  the finished note to Telegram, Discord, Teams, Slack, and other supported
  surfaces via the local bridge.

## Language

`config.yaml` → `language` (default `en`). Influences both AI prompt
language and the default TTS voice pair. Override per-run with
`--language en|zh|ja|es|fr|de|...`.

Built-in default voice pairs (male + female, edge-tts):

| `language` | HostA (male)              | HostB (female)            |
| ---------- | ------------------------- | ------------------------- |
| `en`       | `en-US-AndrewNeural`      | `en-US-AvaNeural`         |
| `zh`       | `zh-CN-YunyangNeural` 云飞 | `zh-CN-XiaoxiaoNeural` 小晓 |
| `ja`       | `ja-JP-KeitaNeural`       | `ja-JP-NanamiNeural`      |
| `es`       | `es-ES-AlvaroNeural`      | `es-ES-ElviraNeural`      |
| `fr`       | `fr-FR-HenriNeural`       | `fr-FR-DeniseNeural`      |
| `de`       | `de-DE-ConradNeural`      | `de-DE-KatjaNeural`       |

Override any pair (or add new languages) under `tts.language_voices`.
Setting `tts.voices` directly always wins.

## Cloud upload (OneDrive / Google Drive / S3 / Dropbox / …)

`config.yaml` → `upload.provider: rclone` makes `publish` upload the
generated mp3 / pptx / summary to your configured cloud and inline the
shareable URLs in `links.json` and the notification payload — so users
get one-click mp3 + ppt links instead of local `file://` URIs.

```yaml
upload:
  provider: rclone
  rclone:
    remote: "onedrive:yumnb"   # or gdrive:yumnb, s3:bucket/yumnb, etc.
    share: true
```

Set it up once with `rclone config` (see https://rclone.org). yumnb
delegates everything to rclone so the same skill works with every
backend rclone supports.
