---
name: Trugen AI
description: Build, configure, and deploy conversational video agents using the Trugen AI platform API. Use this skill when the user wants to create AI video avatars, manage knowledge bases, set up webhooks/callbacks, embed agents into websites, integrate with LiveKit, configure tools or MCPs, set up multilingual agents, or bring their own LLM to Trugen AI.
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - TRUGEN_API_KEY
    primaryEnv: TRUGEN_API_KEY
    homepage: https://docs.trugen.ai/docs/overview
---

# Trugen AI

Build real-time conversational video agents — AI-powered avatars that see, hear, speak, and reason with users in under 1 second of latency.

| | |
|---|---|
| **API Base URL** | `https://api.trugen.ai` |
| **Authentication** | `x-api-key: <your-api-key>` header on all requests |
| **Official Docs** | [docs.trugen.ai](https://docs.trugen.ai/docs/overview) |
| **Developer Portal** | [app.trugen.ai](https://app.trugen.ai) |

## Required Credentials

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `TRUGEN_API_KEY` | Primary API key for all Trugen API calls (sent as `x-api-key` header) | [Developer Portal](https://app.trugen.ai) |
| `TRUGEN_AVATAR_ID` | (Optional) Default avatar ID for LiveKit integration | [Developer Portal](https://app.trugen.ai) |

> **Security**: Never expose `TRUGEN_API_KEY` in client-side code. For widget/iFrame embeds, use a server-side proxy to keep keys secret. See [references/embedding.md](references/embedding.md) for details.

## Platform Pipeline

| Step | Component | Function |
|------|-----------|----------|
| 1 | **WebRTC** | Bidirectional audio/video streaming |
| 2 | **STT** (Deepgram) | Streaming speech-to-text |
| 3 | **Turn Detection** | Natural conversation boundary detection |
| 4 | **LLM** (OpenAI, Groq, custom) | Contextual response generation |
| 5 | **Knowledge Base** | Grounding answers in your data |
| 6 | **TTS** (ElevenLabs) | Natural, expressive speech synthesis |
| 7 | **Huma-01** | Neural avatar video generation with lip sync & microexpressions |

## Quickstart

1. Create an agent → `POST /v1/ext/agent` — see [references/agents.md](references/agents.md)
2. Embed via iFrame or Widget — see [references/embedding.md](references/embedding.md)

## API Endpoints Overview

| Resource | Endpoints | Reference |
|----------|-----------|-----------|
| **Agents** | Create, Get, List, Update, Delete, Create from Template | [agents.md](references/agents.md) |
| **Knowledge Base** | Create KB, Add Docs, Get, List, Update, Delete KB/Doc | [knowledge-base.md](references/knowledge-base.md) |
| **Templates** | Create, Get, List, Update, Delete persona templates | [templates.md](references/templates.md) |
| **Tools & MCPs** | Create/manage function-calling tools and MCP servers | [tools-and-mcps.md](references/tools-and-mcps.md) |
| **Webhooks** | Callback events, payload format, handler examples | [webhooks.md](references/webhooks.md) |
| **Embedding** | iFrame, Widget, LiveKit integration + avatar IDs | [embedding.md](references/embedding.md) |
| **Providers/Avatars** | Available LLMs, STT, TTS, avatars, languages, BYO-LLM | [providers-avatars-languages.md](references/providers-avatars-languages.md) |
| **Prompting** | Voice prompt strategies, guardrails, use case examples | [prompting-and-use-cases.md](references/prompting-and-use-cases.md) |

## Conversations

Retrieve transcripts for completed sessions:

`GET /v1/ext/conversation/{id}` — Returns agent_id, status, transcript array, recording_url.

## Workflow Guide

Determine what the user needs, then load the appropriate reference:

| Task | Reference File |
|------|---------------|
| Creating/managing agents | [agents.md](references/agents.md) |
| Attaching data/documents | [knowledge-base.md](references/knowledge-base.md) |
| Reusing personas across agents | [templates.md](references/templates.md) |
| Calling external APIs from agent | [tools-and-mcps.md](references/tools-and-mcps.md) |
| Reacting to conversation events | [webhooks.md](references/webhooks.md) |
| Embedding agent in website | [embedding.md](references/embedding.md) |
| Choosing LLM/voice/language | [providers-avatars-languages.md](references/providers-avatars-languages.md) |
| Writing effective prompts | [prompting-and-use-cases.md](references/prompting-and-use-cases.md) |

## Developer Resources

| Resource | Link |
|----------|------|
| Documentation | [docs.trugen.ai](https://docs.trugen.ai/docs/overview) |
| API Reference | [docs.trugen.ai/api-reference](https://docs.trugen.ai/api-reference/overview) |
| Developer Portal | [app.trugen.ai](https://app.trugen.ai) |
| Community Discord | [discord.gg/4dqc8A66FJ](https://discord.gg/4dqc8A66FJ) |
| Support | support@trugen.ai |
| GitHub Examples | [trugenai/trugen-examples](https://github.com/trugenai/trugen-examples) |
| Changelog | [docs.trugen.ai/changelog](https://docs.trugen.ai/docs/changelog) |
