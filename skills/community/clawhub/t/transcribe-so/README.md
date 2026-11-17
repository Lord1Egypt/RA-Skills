# transcribe-agent

Make any agent transcribe. One repo with three ways in: a pure-JSON CLI
(`transcribe-so`), an agent skill for `npx skills add`, and a Claude Code
plugin bundling the transcribe.so remote MCP server.

transcribe.so turns YouTube videos, podcasts, direct media URLs, and local
files into speaker-labelled transcripts with timestamped segments, chapters,
sections, cited Q&A, and subtitle files (SRT, VTT, karaoke VTT).

## Install

### 1. Agent skill (Claude Code, OpenClaw, any skills.sh-compatible agent)

```bash
npx skills add shsunmoonlee/transcribe-agent
```

This installs [SKILL.md](SKILL.md), which teaches the agent the CLI workflow,
hard rules, and exit codes.

### 2. Claude Code plugin (remote MCP server + skills + /transcribe command)

```
/plugin marketplace add shsunmoonlee/transcribe-agent
/plugin install transcribe-so@transcribe-agent
```

The plugin connects Claude to the remote MCP server at
`https://transcribe.so/mcp` (21 tools) and bundles the `transcribe-audio` and
`get-transcript` skills plus a one-shot `/transcribe` command. First tool call
triggers the OAuth browser flow; alternatively authenticate with a
`tsk_live_*` API key via `/mcp`.

### 3. CLI (any script, cron job, or agent with a shell)

```bash
npm install -g transcribe-so     # or: pnpm install -g transcribe-so
export TRANSCRIBE_API_KEY=tsk_live_...   # https://transcribe.so/settings/api-keys
transcribe-so me
```

## CLI in 30 seconds

```bash
# Price it (free), then transcribe under an explicit budget
transcribe-so quote --source youtube --url "https://www.youtube.com/watch?v=..."
transcribe-so run   --source youtube --url "https://www.youtube.com/watch?v=..." --max-usd 2

# Local file
transcribe-so upload ./interview.mp3         # prints upload_id (+ ffprobe duration)
transcribe-so run --source upload --upload-id <id> --duration <s> --max-usd 5

# Artifacts
transcribe-so result <id> | jq '.chapters[]'
transcribe-so subtitles <id> --format srt > out.srt
transcribe-so ask <id> -q "What did the guest say about pricing?"
```

Design contract, made for agents:

- stdout is pure JSON (the one exception: `subtitles` prints the raw subtitle
  body). All progress goes to stderr, so `| jq .` always works.
- Exit codes are meaningful: 0 ok, 1 API error, 2 usage, 3 auth, 4 payment,
  5 transient, 6 local `--max-usd` budget refusal.
- `create`/`run`/`quote` always send an `Idempotency-Key`; retries are safe.
- `run` refuses to spend more than `--max-usd` (required, no default).
- The CLI refuses to send your API key to a non-default host unless you pass
  `--allow-custom-host`.

Full command reference and workflow rules: [SKILL.md](SKILL.md). Worked
examples: [examples/](examples/).

## Pricing

Transcription is billed per minute from your transcribe.so wallet; quotes are
free (`quote` before committing). Clip renders are $0.05 per started 60 s.
Live Q&A uses a daily allowance, never the wallet. Details:
<https://transcribe.so/pricing>

## Privacy Policy

This tooling sends the media URLs, uploaded files, and questions you provide
to transcribe.so for processing. See the transcribe.so privacy policy at
<https://transcribe.so/privacy-policy> for data collection, usage, storage,
retention, and contact information. No data is collected by the CLI or plugin
itself beyond what the API and MCP tools transmit.

## Links

- Agent landing page: <https://transcribe.so/agent>
- Docs: <https://transcribe.so/developers/docs>
- OpenAPI: <https://transcribe.so/openapi.json>
- MCP server card: <https://transcribe.so/.well-known/mcp/server-card.json>
- Auth guide: <https://transcribe.so/auth.md>
- Support: support@transcribe.so
