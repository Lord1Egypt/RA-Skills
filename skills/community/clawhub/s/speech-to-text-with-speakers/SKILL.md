---
name: speech-to-text-with-speakers
description: "Speech to Text With Speakers: Transcribe audio from file_id or public_url with three tiered actions for recordings up to 15, 30, or 60 minutes. Use when an agent needs speech to text with speakers, transcribe meeting recordings, generate subtitles and captions for videos, convert voice memos to searchable text, transcribe podcast episodes, transcribe extended, file id, public url through AgentPMT-hosted remote tool calls. Discovery terms: speech to text with speakers."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/speech-to-text-with-speakers
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/speech-to-text-with-speakers"}}
---
# Speech to Text With Speakers

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Turn any audio recording into clean, searchable text in seconds. Transcribe voice memos, meetings, interviews, podcasts, and webinars with accurate speech recognition that handles accents and background noise. Get plain text for quick reference, SRT or WebVTT subtitles for video captioning, or rich JSON output with word-level timestamps and speaker identification. Choose from three tiers based on recording length — up to 15, 30, or 60 minutes — and optionally enable speaker diarization to label who said what, profanity filtering, and alternative transcripts for maximum accuracy.

## Product Instructions
### Speech to Text

Transcribe audio with one tool and choose the action that matches the upload length.

#### Tool Call Format

```json
{
  "action": "get_instructions"
}
```

```json
{
  "action": "transcribe_quick",
  "file_id": "FILE_ID",
  "language_code": "en-US",
  "output_format": "text"
}
```

```json
{
  "action": "transcribe_standard",
  "public_url": "https://example.com/meeting.m4a",
  "output_format": "vtt",
  "enable_word_timestamps": true,
  "enable_diarization": true
}
```

```json
{
  "action": "transcribe_extended",
  "public_url": "https://example.com/interview.webm",
  "output_format": "json",
  "max_alternatives": 2
}
```

```json
{
  "action": "transcribe_standard",
  "file_id": "FILE_ID",
  "output_format": "json",
  "enable_word_timestamps": true,
  "remove_filler_words": false
}
```

#### Actions

- `transcribe_quick`: audio up to 15 minutes. Price: 100 credits.
- `transcribe_standard`: audio up to 30 minutes. Price: 150 credits.
- `transcribe_extended`: audio up to 60 minutes. Price: 200 credits.

#### Notes

- Provide either `file_id` or `public_url`.
- `public_url` must be an HTTPS URL and cannot point to private or internal network addresses.
- If `language_code` is omitted, the tool defaults to `en-US`.
- Supported output formats: `text`, `srt`, `vtt`, `json`.
- Optional controls: `enable_diarization`, `enable_word_timestamps`, `remove_filler_words`, `enable_profanity_filter`, `max_alternatives`.
- `remove_filler_words` defaults to `true`, which uses Google STT V2's cleaned transcript path.
- Set `remove_filler_words` to `false` to preserve disfluencies through Vercel AI Gateway using the `openai/whisper-1` gateway model slug. This path always requests word-level timestamps from the gateway for clipping workflows.
- `remove_filler_words=false` does not support `enable_diarization=true` or `max_alternatives` greater than `1`; use the default cleaned path for those features.
- Subtitle responses include inline subtitle content and may also include stored file links during normal platform invocations.

## When To Use
- Use this skill for `Speech to Text With Speakers` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: speech to text with speakers, transcribe meeting recordings, generate subtitles and captions for videos, convert voice memos to searchable text, transcribe podcast episodes, transcribe extended, file id, public url.
- Supported action names: `transcribe_extended`, `transcribe_quick`, `transcribe_standard`.

## Use Cases
- Transcribe meeting recordings
- Generate subtitles and captions for videos
- Convert voice memos to searchable text
- Transcribe podcast episodes
- Create interview transcripts with speaker labels
- Produce SRT or WebVTT subtitle files
- Build searchable audio archives
- Transcribe webinars and lectures
- Analyze customer call recordings
- Content repurposing from audio to text

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `transcribe_extended` (action slug: `transcribe-extended`): Transcribe audio up to 60 minutes. Price: `200` credits. Parameters: `enable_diarization`, `enable_profanity_filter`, `enable_word_timestamps`, `file_id`, `language_code`, `max_alternatives`, `output_format`, `public_url`, plus 1 more.
- `transcribe_quick` (action slug: `transcribe-quick`): Transcribe audio up to 15 minutes. Price: `100` credits. Parameters: `enable_diarization`, `enable_profanity_filter`, `enable_word_timestamps`, `file_id`, `language_code`, `max_alternatives`, `output_format`, `public_url`, plus 1 more.
- `transcribe_standard` (action slug: `transcribe-standard`): Transcribe audio up to 30 minutes. Price: `150` credits. Parameters: `enable_diarization`, `enable_profanity_filter`, `enable_word_timestamps`, `file_id`, `language_code`, `max_alternatives`, `output_format`, `public_url`, plus 1 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "speech-to-text-with-speakers"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "speech-to-text-with-speakers"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "speech-to-text-with-speakers"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "speech-to-text-with-speakers"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "speech-to-text-with-speakers"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "speech-to-text-with-speakers"
  }
}
```

## Call This Tool
Product slug: `speech-to-text-with-speakers`

Marketplace page: https://www.agentpmt.com/marketplace/speech-to-text-with-speakers

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Speech-to-Text-With-Speakers",
    "arguments": {
      "action": "transcribe_extended",
      "enable_diarization": false,
      "enable_profanity_filter": false,
      "enable_word_timestamps": false,
      "file_id": "example file id",
      "language_code": "example language code",
      "max_alternatives": 1,
      "output_format": "text",
      "public_url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "speech-to-text-with-speakers",
  "parameters": {
    "action": "transcribe_extended",
    "enable_diarization": false,
    "enable_profanity_filter": false,
    "enable_word_timestamps": false,
    "file_id": "example file id",
    "language_code": "example language code",
    "max_alternatives": 1,
    "output_format": "text",
    "public_url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `transcribe_extended` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/speech-to-text-with-speakers
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
