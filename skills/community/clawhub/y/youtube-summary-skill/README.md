# youtube-summary

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that fetches YouTube video transcripts and generates structured summaries.

## What it does

Given a YouTube URL, this skill:

1. Fetches the video transcript (supports multiple languages with automatic fallback)
2. Produces a structured summary in English (default) or any specified language
3. Optionally saves the summary as a Markdown file

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (used to run the Python script with dependencies)

No global Python packages needed — `uv` handles the `youtube-transcript-api` dependency automatically.

## Installation

### Via ClawHub (recommended)

```bash
/plugin marketplace add ivanopassari/youtube-summary-skill
/plugin install youtube-summary
```

### Manual installation

Clone this repo into your Claude Code skills directory:

```bash
git clone https://github.com/ivanopassari/youtube-summary-skill.git \
  ~/.claude/skills/youtube-summary-skill
```

Or copy the files manually:

```bash
mkdir -p ~/.claude/skills/youtube-summary-skill
cp SKILL.md fetch_transcript.py ~/.claude/skills/youtube-summary-skill/
```

That's it. Claude Code will pick up the skill automatically on the next session.

## Usage

In Claude Code, type:

```
/youtube-summary https://www.youtube.com/watch?v=VIDEO_ID
```

To get a summary in a specific language, use the `--lang` flag:

```
/youtube-summary https://www.youtube.com/watch?v=VIDEO_ID --lang italian
/youtube-summary https://youtu.be/VIDEO_ID --lang spanish
```

If no language is specified, the summary is generated in **English**.

Supported URL formats:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- Bare video ID: `VIDEO_ID`

## Output example

### Video Summary

**Overview**
Brief introductory paragraph about the video's topic.

**Key Points**
- Main concepts discussed in the video
- Each point is concise but informative

**Notable Quotes**
> Notable quotes from the video

Section headings are automatically translated to match the chosen language.

## License

MIT
