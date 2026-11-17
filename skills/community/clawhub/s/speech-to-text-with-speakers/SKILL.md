---
name: speech-to-text-with-speakers
description: "Speech to Text With Speakers: Transcribe audio from file_id or public_url with three tiered actions for recordings up to 15, 30, or 60 minutes. Use when an agent needs speech to text with speakers, transcribe meeting recordings, generate subtitles and captions for videos, convert voice memos to searchable text, transcribe podcast episodes, get task, task id, list tasks through AgentPMT-hosted remote tool calls. Discovery terms: speech to text with speakers, transcribe meeting recordings."
version: 1.0.6
homepage: https://www.agentpmt.com/marketplace/speech-to-text-with-speakers
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/speech-to-text-with-speakers"}}
---
# Speech to Text With Speakers

## Freshness
Last updated: `2026-07-22`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Turn any audio recording into clean, searchable text in seconds. Transcribe voice memos, meetings, interviews, podcasts, and webinars with accurate speech recognition that handles accents and background noise. Get plain text for quick reference, SRT or WebVTT subtitles for video captioning, or rich JSON output with word-level timestamps and speaker identification. Choose from three tiers based on recording length — up to 15, 30, or 60 minutes — and optionally enable speaker diarization to label who said what, profanity filtering, and alternative transcripts for maximum accuracy.

## Product Instructions
### Speech to Text

Transcribe audio with one tool. Transcribe actions run as background tasks: the submit response returns a `task_id` immediately, and short clips usually complete inline in that same response. Poll `get_task` for anything still processing.

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
  "action": "get_task",
  "task_id": "TASK_ID"
}
```

```json
{
  "action": "list_tasks",
  "limit": 20
}
```

#### Actions

- `transcribe_quick`: audio up to 15 minutes. Price: 100 credits.
- `transcribe_standard`: audio up to 30 minutes. Price: 150 credits.
- `transcribe_extended`: audio up to 60 minutes. Price: 200 credits.
- `get_task`: check a transcription task's progress and retrieve its result. Price: 1 credit.
- `list_tasks`: list recent transcription tasks. Price: 1 credit.

#### Async task flow

- Every transcribe action returns a task envelope: `{action, task_id, status, ...}`. ALWAYS check `status` before polling — short clips finish within the submit request and return `status: "completed"` with `outputs` inline, costing zero polls.
- When `status` is `"processing"`, poll `get_task` with the returned `task_id` every 10-15 seconds. `progress` advances as the job moves through download, validation, and recognition.
- A completed task carries the full transcription payload in `outputs[0]`: the selected content inline (`text`, `srt_content`, `vtt_content`, or `json_data`), plus `speakers`, `word_count`, `confidence_score`, `audio_metadata`, and the File Manager artifact fields `result_file_id`/`result_signed_url`.
- A failed task carries `error`. Tier-limit failures also carry `error_details` with `recommended_actions` — resubmit with the suggested larger tier.
- If the service restarts mid-transcription, in-flight Google batch jobs resume automatically. Jobs that cannot resume are marked failed with an instruction to resubmit; they never sit in `processing` forever.

#### Billing

- Transcribe actions charge on submission. A task that later fails (for example, audio too long for the tier) is not auto-refunded — pick the tier from the recording length you already know, and check `error_details.recommended_actions` before resubmitting.

#### Notes

- Provide either `file_id` or `public_url`.
- `public_url` must be an HTTPS URL and cannot point to private or internal network addresses.
- Audio downloads are capped at 150MB. If a recording is larger, compress it to mp3 or m4a and retry.
- If `language_code` is omitted, the tool defaults to `en-US`.
- Supported output formats: `text`, `srt`, `vtt`, `json`.
- Optional controls: `enable_diarization`, `enable_word_timestamps`, `remove_filler_words`, `enable_profanity_filter`, `max_alternatives`.
- `remove_filler_words` defaults to `true`, which uses Google STT V2's cleaned transcript path.
- Set `remove_filler_words` to `false` to preserve disfluencies through Vercel AI Gateway using the `openai/whisper-1` gateway model slug. This path always requests word-level timestamps from the gateway for clipping workflows.
- `remove_filler_words=false` does not support `enable_diarization=true` or `max_alternatives` greater than `1`; use the default cleaned path for those features.
- `enable_diarization=true` supports audio up to 20 minutes (a provider limit). Longer recordings fail with guidance: disable diarization, or split the audio into 20-minute segments and transcribe them individually.
- With `enable_diarization=true`, `text` output is speaker-labelled one line per turn (`[0:04] Speaker 0: ...`), inline and in the stored `transcription.txt`, so it is readable without reformatting. Without diarization it is the flat transcript. Speaker numbers match the `speaker_tag` values in `speakers`/`json_data`.
- During invocations with File Manager storage available, `text` and `json` results are stored for every successful transcription; `srt` and `vtt` results are stored when the generated subtitle content is non-empty. The corresponding filenames are `transcription.txt`, `transcription.json`, `transcription.srt`, and `transcription.vtt`.
- Stored artifacts are returned through the `result_file_id` and `result_signed_url` fields in `outputs[0]`. Agents should use `result_file_id` for later File Manager operations.
- If transcription succeeds but artifact storage fails, the inline result remains available and `result_file_error` explains that the File Manager file could not be created.

## When To Use
- Use this skill for `Speech to Text With Speakers` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: speech to text with speakers, transcribe meeting recordings, generate subtitles and captions for videos, convert voice memos to searchable text, transcribe podcast episodes, get task, task id, list tasks.
- Supported action names: `get_task`, `list_tasks`, `transcribe_extended`, `transcribe_quick`, `transcribe_standard`.

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
Supported action count: `5`.
x402 availability: not enabled for this product.

- `get_task` (action slug: `get-task`): Check a transcription task's progress and retrieve its result. Completed tasks carry the full transcription payload in outputs[0]. Price: `1` credits. Parameters: `task_id`.
- `list_tasks` (action slug: `list-tasks`): List recent transcription tasks with status and progress. Price: `1` credits. Parameters: `limit`.
- `transcribe_extended` (action slug: `transcribe-extended`): Start an asynchronous transcription of audio up to 60 minutes. Returns a task_id immediately (short clips complete inline in the same response); poll get_task for the completed transcript and File Manager artifact. Price: `200` credits. Parameters: `enable_diarization`, `enable_profanity_filter`, `enable_word_timestamps`, `file_id`, `language_code`, `max_alternatives`, `output_format`, `public_url`, plus 1 more.
- `transcribe_quick` (action slug: `transcribe-quick`): Start an asynchronous transcription of audio up to 15 minutes. Returns a task_id immediately (short clips complete inline in the same response); poll get_task for the completed transcript and File Manager artifact. Price: `100` credits. Parameters: `enable_diarization`, `enable_profanity_filter`, `enable_word_timestamps`, `file_id`, `language_code`, `max_alternatives`, `output_format`, `public_url`, plus 1 more.
- `transcribe_standard` (action slug: `transcribe-standard`): Start an asynchronous transcription of audio up to 30 minutes. Returns a task_id immediately (short clips complete inline in the same response); poll get_task for the completed transcript and File Manager artifact. Price: `150` credits. Parameters: `enable_diarization`, `enable_profanity_filter`, `enable_word_timestamps`, `file_id`, `language_code`, `max_alternatives`, `output_format`, `public_url`, plus 1 more.

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
      "action": "get_task",
      "task_id": "example task id"
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
    "action": "get_task",
    "task_id": "example task id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_task` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

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
