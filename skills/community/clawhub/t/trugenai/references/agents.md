# Agents API Reference

## Create Agent (Full Config)

`POST /v1/ext/agent`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/agent \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data @- <<EOF
{
  "agent_name": "Sample AI Agent",
  "agent_system_prompt": "You're a helpful AI agent.",
  "config": {
    "timeout": 240,
    "memory": {
      "isEnabled": false,
      "instruction": "sample memory instruction for the agent"
    }
  },
  "knowledge_base": [
    { "id": "4a0365e4-ced5-42f0-8933-b6880a0ce044", "name": "new kb 123" }
  ],
  "record": true,
  "callback_url": "https://yourdomain.com/webhooks/trugen",
  "callback_events": [
    "participant_left",
    "max_call_duration_warning",
    "max_call_duration_timeout",
    "action_found"
  ],
  "avatars": [
    {
      "avatar_key_id": "665a1170",
      "config": {
        "llm": {
          "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
          "provider": "groq"
        },
        "stt": {
          "provider": "deepgram",
          "model": "flux-general-en",
          "min_endpointing_delay": 0.3,
          "max_endpointing_delay": 0.4
        },
        "tts": {
          "provider": "elevenlabs",
          "model_id": "eleven_turbo_v2_5",
          "voice_id": "ZUrEGyu8GFMwnHbvLhv2"
        }
      },
      "persona_name": "Sample AI Agent",
      "persona_prompt": "You're a helpful AI agent.",
      "conversational_context": "Sample Conversational Context",
      "idle_timeout": {
        "timeout": 30,
        "filler_phrases": [
          "Hey it's been a while since we last spoke, are we still connected?",
          "I notice we haven't talked for a bit, is everything okay?"
        ]
      },
      "welcome_message": {
        "wait_time": 2,
        "messages": [
          "Hi, how are you doing today?",
          "Hello, how can I help you?"
        ]
      },
      "exit_message": {
        "max_call_duration": 300,
        "messages": [
          "We are at the end of our call, thank you for your time.",
          "Thank you for your time today."
        ]
      },
      "exit_heads_up_message": {
        "callout_before": 10,
        "messages": [
          "We are almost at the end of our call, thank you for your time.",
          "Thank you for your time. We will see you next time."
        ]
      }
    }
  ]
}
EOF
```

## Key Agent Fields

| Field | Description |
|-------|-------------|
| `agent_name` | Display name for the agent |
| `agent_system_prompt` | Global behavioral instructions |
| `config.timeout` | Session inactivity timeout (seconds) |
| `config.memory.isEnabled` | Enable persistent memory across sessions |
| `avatars[].avatar_key_id` | ID of the visual avatar to use |
| `avatars[].config.llm` | LLM provider/model selection |
| `avatars[].config.stt` | Speech-to-text provider/model |
| `avatars[].config.tts` | Text-to-speech provider/voice |
| `avatars[].persona_name` | Avatar persona name |
| `avatars[].persona_prompt` | Per-avatar system prompt |
| `avatars[].welcome_message` | Greeting spoken at session start |
| `avatars[].exit_message` | Farewell spoken at session end |
| `avatars[].exit_heads_up_message` | Warning before session ends |
| `avatars[].idle_timeout` | What to say when user is silent |
| `record` | Whether to record the call |
| `callback_url` | Webhook HTTPS endpoint for events |
| `callback_events` | List of events to subscribe to |
| `tool` | List of tool IDs attached to this agent |
| `mcp` | List of MCP IDs attached to this agent |

## Get Agent by ID

`GET /v1/ext/agent/{id}`

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/agent/{id} \
  --header 'x-api-key: <api-key>'
```

**Response:** Full agent object including `avatars`, `knowledge_base`, `tool`, `mcp`, `config`, `callback_url`, `callback_events`, `record`, `created_at`, `updated_at`.

## List All Agents

`GET /v1/ext/agents`

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/agents \
  --header 'x-api-key: <api-key>'
```

Returns an array of all agents with full configuration.

## Update Agent

`PUT /v1/ext/agent/{id}`

```bash
curl --request PUT \
  --url https://api.trugen.ai/v1/ext/agent/{id} \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "id": "b63c2a53-266b-4b43-a71b-7ea8b5e2e916",
    "agent_name": "Customer Support Agent",
    "agent_system_prompt": "You are a helpful AI assistant that handles customer service inquiries.",
    "avatars": [
      {
        "avatar_key_id": "1e4ea106",
        "persona_name": "Sofia - Friendly Support",
        "persona_prompt": "Speak in a warm, engaging tone and provide clear answers.",
        "config": {
          "llm": { "model": "meta-llama/llama-4-maverick-17b-128e-instruct", "provider": "groq" },
          "stt": { "model": "flux-general-en", "provider": "deepgram", "min_endpointing_delay": 0.3, "max_endpointing_delay": 0.4 },
          "tts": { "model_id": "eleven_turbo_v2_5", "provider": "elevenlabs", "voice_id": "ZUrEGyu8GFMwnHbvLhv2" }
        }
      }
    ],
    "knowledge_base": [
      { "id": "ac79226e-73e1-41fe-8cde-469ae4e244fa", "name": "Product Support Articles", "description": "Contains FAQs and troubleshooting guides." }
    ],
    "config": {
      "maxCallDuration": 1800,
      "conversationalContext": "customer-support",
      "memory": { "isEnabled": false, "instruction": "sample memory instruction" }
    },
    "callback_url": "",
    "callback_events": [
      "participant_left", "agent.started_speaking", "agent.stopped_speaking",
      "agent.interrupted", "user.started_speaking", "user.stopped_speaking",
      "utterance_committed", "max_call_duration_timeout"
    ],
    "record": true,
    "is_active": true
  }'
```

**Response:** `{ "id": "...", "message": "Agent updated successfully" }`

## Delete Agent

`DELETE /v1/ext/agent/{id}`

```bash
curl --request DELETE \
  --url https://api.trugen.ai/v1/ext/agent/{id} \
  --header 'x-api-key: <api-key>'
```

**Response:** `{ "id": "...", "message": "Agent deleted successfully" }`

## Create Agent from Template

`POST /v1/ext/agentbytemplate`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/agentbytemplate \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "avatar_ids": ["1e4ea106", "665a1170"],
    "template_id": "76d9ff1d-b1d5-4dee-9b9a-d4c4d58c9c55"
  }'
```

Alternative endpoint (also valid): `POST /v1/agent/bytemplate` (requires `email` field).

**Response:** `{ "id": "...", "message": "Agent created successfully" }`
