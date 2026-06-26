---
name: weryai-podcast-generator
description: "Generate, query, and deliver WeryAI podcasts through the official podcast generation API. Use when the user needs podcast speaker lookup, podcast text generation, podcast audio generation, full text-to-audio podcast workflows, or when the user asks for a spoken multi-speaker podcast from a topic or question."
metadata: { "openclaw": { "emoji": "🎙️", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY", "WERYAI_BASE_URL"], "bins": ["node"], "node": ">=18" } } }
---

# WeryAI Podcast Generator

Generate podcasts through the official WeryAI podcast API. This skill covers the full workflow: list available voices, submit podcast text generation, trigger audio generation, and wait until the final audio is ready.

## Example Prompts

- `List the English podcast speakers available on WeryAI.`
- `Generate a short English podcast about AI in healthcare with two speakers and give me the final audio URL.`
- `Submit podcast text generation for this topic and stop after the text task is created.`
- `Generate podcast audio for this existing podcast task ID.`
- `Check whether this WeryAI podcast task already reached audio-success.`

## Quick Summary

- Main jobs: `speaker lookup`, `podcast text generation`, `podcast audio generation`, `podcast task status`, `full podcast wait`
- Required paid inputs: `query`, `speakers`, `language`
- Generation modes: `quick`, `debate`, `deep`
- Default mode: `quick`
- Preferred entrypoint: `wait.js` for end-to-end text -> audio flow
- Main trust signals: dry-run support, explicit speaker requirement, documented `debate` rule, podcast-aware polling on `content_status`

## Authentication and first-time setup

Before the first paid run:

1. Create a WeryAI account.
2. Open `https://www.weryai.com/api/keys`.
3. Create an API key and copy the secret value.
4. Add it to `WERYAI_API_KEY`.
5. Make sure the account has available balance before running paid podcast generation.

### Quick verification

Use one safe check before the first paid run:

```sh
node scripts/speakers.js --language en
node scripts/wait.js --json '{"query":"What is retrieval augmented generation?","speakers":["travel-girl-english","leo-9328b6d2"],"language":"en","mode":"quick"}' --dry-run
```

- `speakers.js` confirms the key is configured and the podcast voice list is reachable.
- `--dry-run` confirms the full request shape locally without spending credits.

## Prerequisites

- `WERYAI_API_KEY` must be set before calling the API.
- Optional override `WERYAI_BASE_URL` defaults to `https://api.weryai.com`. Only override it with a trusted host.
- Node.js `>=18` is required.
- Real `submit-text`, `generate-audio`, and `wait` runs may consume WeryAI credits.
- Paid `submit-text` and `wait` runs require explicit `speakers`; do not assume or auto-pick hidden speakers.

## Supported intents

- `podcast voices`, `podcast speakers`, `available voices` -> `speakers.js`
- `create a podcast from this topic`, `generate a podcast episode`, `make a spoken podcast` -> `wait.js`
- `submit podcast text only` -> `submit-text.js`
- `start podcast audio for this task` -> `generate-audio.js`
- `check this podcast task` -> `status.js`

## Generation modes

- `quick`: fastest default mode for short topic-driven podcast generation
- `debate`: structured two-speaker debate format
- `deep`: longer or more detailed generation mode

Important rule:

- `debate` mode requires exactly 2 speakers.

### Recommended guidance pattern

Use short operator-style guidance like this:

- General help: When the user asks "how to use this skill", DO NOT paste raw shell commands. Instead, explain the capabilities in natural language and give 2-3 prompt examples.

## Workflow

1. If the user has not chosen speakers yet, run `speakers.js --language <code>` first.
2. Confirm the final `query`, `speakers`, `language`, and `mode`.
3. Prefer `wait.js` for end-to-end delivery.
4. `wait.js` submits podcast text generation, polls until `content_status=text-success`, triggers audio generation, then polls until `content_status=audio-success`. Enforce bounded polling with a maximum timeout of 30 minutes (1800 seconds); do not run unbounded loops.
5. Return the final audio URLs and task state.

## Commands

```sh
# Full end-to-end run
node scripts/wait.js --json '{"query":"What are the breakthrough applications of artificial intelligence in healthcare?","speakers":["travel-girl-english","leo-9328b6d2"],"language":"en","mode":"quick"}'

# Inspect a podcast task
node scripts/status.js --task-id <task-id>
```

## User-facing delivery requirement

- Always render the final `audios` URLs directly to the user as clickable Markdown links. Do not just output the `taskId`.
- If multiple audio tracks are generated, render all of them using markdown links consecutively.
- Include a brief summary of the generation parameters used (e.g. from `requestSummary` or your initial choices).
- If timeout is reached before completion, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally to check the status when asked.

## Definition of Done

- `speakers.js` returns at least one speaker for the requested language, or a clear API failure.
- `submit-text.js` returns a real `taskId`.
- `wait.js` reaches `content_status=audio-success` and returns user-visible final audio URLs,
- or `wait.js` reaches timeout and returns the `taskId` plus an offer to check status again later,
- or a clear failure with task state and next step.

## Re-run Behavior

- Re-running `speakers.js` is read-only and safe.
- Re-running `status.js` is read-only and safe.
- Re-running `submit-text.js`, `generate-audio.js`, or `wait.js` may create or advance paid podcast work and may consume additional credits.

## Boundaries

- Do not use this skill for music-only generation; use `weryai-music-generator`.
- Do not use this skill for general chat or writing-only requests; use `weryai-chat` or other `text/*` skills.
- Do not invent undocumented podcast fields beyond `query`, `speakers`, `language`, `mode`, `scripts`, `webhook_url`, and `caller_id`.

## References

- Official podcast API summary: [references/podcast-api.md](references/podcast-api.md)
- Podcast speakers API: [Get Podcast Speakers List](https://docs.weryai.com/api-reference/podcast-generation/get-podcast-speakers-list)
- Podcast text generation API: [Submit Podcast Text Generation Task](https://docs.weryai.com/api-reference/podcast-generation/submit-podcast-text-generation-task)
- Podcast audio generation API: [Generate Podcast Audio](https://docs.weryai.com/api-reference/podcast-generation/generate-podcast-audio)
- Task status API: [Query Task Details](https://docs.weryai.com/api-reference/tasks/query-task-details)
