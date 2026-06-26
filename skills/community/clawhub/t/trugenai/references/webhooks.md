# Webhooks & Callbacks Reference

Event callbacks let you react to real-time conversation events for analytics, UI updates, and workflow automation.

## Enable Webhooks for an Agent

Set `callback_url` and `callback_events` when creating or updating an agent:

```json
{
  "callback_url": "https://yourdomain.com/webhooks/trugen",
  "callback_events": [
    "call_ended",
    "participant_left",
    "agent.started_speaking",
    "agent.stopped_speaking",
    "agent.interrupted",
    "user.started_speaking",
    "user.stopped_speaking",
    "utterance_committed",
    "max_call_duration_timeout"
  ]
}
```

## Webhook Payload Format

```json
{
  "timestamp": 1764760139.6834729,
  "conversation_id": "471f0520-cea1-487a-9bcc-37ba37717d81",
  "type": "pipeline",
  "event": {
    "name": "agent.started_speaking",
    "payload": { "text": "Hi, how are you?" }
  }
}
```

## All Event Types

| Event | Payload | Use Case |
|-------|---------|----------|
| `call_ended` | `{}` | Clean up resources, trigger post-call workflows |
| `participant_left` | `{ "id": "PA_xxx" }` | Mark conversation ended, cleanup |
| `agent.started_speaking` | `{ "text": "..." }` | Show speaking indicator in UI |
| `agent.stopped_speaking` | `{ "text": "..." }` | Hide indicator, enable user input |
| `agent.interrupted` | `{}` | Log interruptions, adjust LLM behavior |
| `user.started_speaking` | `{}` | Pause agent, show recording state |
| `user.stopped_speaking` | `{}` | Mark turn boundary for transcription |
| `utterance_committed` | `{ "text": "..." }` | Store transcript, trigger analytics |
| `max_call_duration_timeout` | `{ "call_duration": 60.0, "max_call_duration": 60 }` | Show session ended UI, log duration |

## Webhook Handler Example (Node/Express)

```javascript
import express from "express";
const app = express();
app.use(express.json());

app.post("/webhooks/trugen", (req, res) => {
  const { timestamp, conversation_id, type, event } = req.body;

  switch (event.name) {
    case "agent.started_speaking":
      // Update UI to show agent is speaking
      break;
    case "user.started_speaking":
      // Stop agent TTS, mark user as active
      break;
    case "utterance_committed":
      // Store transcript: event.payload.text
      break;
    case "participant_left":
      // End session, clean up resources
      break;
    case "max_call_duration_timeout":
      // Show "session ended" message
      break;
  }

  // Always respond quickly with 2xx
  res.status(200).send("ok");
});

app.listen(3000);
```

## Best Practices

1. **Respond 2xx immediately** — Acknowledge then offload heavy work to background jobs
2. **Idempotency** — Design handlers to safely process the same event multiple times
3. **Logging** — Log by `conversation_id` and `event.name` for debugging
4. **Security** — Use HTTPS for `callback_url`; restrict by IP, signing secret, or auth token
