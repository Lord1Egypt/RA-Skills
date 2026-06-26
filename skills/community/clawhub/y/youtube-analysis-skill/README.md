# YouTube Analysis Skill

An OpenClaw agent skill for analysing YouTube videos with real depth — not just auto-generated captions.

## What it does

1. Extracts the full transcript via `summarize` (yt-dlp / YouTube transcript API)
2. Assesses transcript quality and flags noisy auto-captions
3. Uses the main chat model to synthesise summary + analytical insights

## Installation

```bash
clawhub install youtube-analysis-skill
```

Or install from GitHub:

```bash
git clone https://github.com/sidonsoft/youtube-analysis-skill.git
mv youtube-analysis-skill ~/.openclaw/skills/youtube-analysis
```

## Usage

When a user provides a YouTube URL, the skill activates automatically. Drop a URL and ask for a summary or analysis.

## Output

- **Summary** — concise, grounded in the transcript
- **Analysis** — implications, connections, credibility assessment, gaps

Transcript first. Analysis second. Confidence is stated explicitly when auto-captions are the only source.

## Requirements

- OpenClaw
- `summarize` tool (part of the OpenClaw toolkit — included by default)
- Main chat model access (MiniMax M2.7 or equivalent)

## License

Apache 2.0
