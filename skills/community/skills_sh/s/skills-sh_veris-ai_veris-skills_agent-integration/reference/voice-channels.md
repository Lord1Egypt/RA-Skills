# Voice Channels (`voice_ws`)

Use this reference when the actor needs to talk to the agent over a real-time audio channel — phone-call analogues, voicebots, kiosk agents, anything where the system under test is a voice agent rather than a text chatbot.

The canonical Veris voice channel is `voice_ws`. It carries PCM16 / 24 kHz / mono audio over a WebSocket, in **one of two framings** selectable via the `protocol` field. The agent (or a small bridge process — see [infrastructure-patterns.md Pattern 9](infrastructure-patterns.md#pattern-9-transport-bridge)) must produce and consume audio in whichever framing the channel is configured for.

| `protocol` | Framing | Maps cleanly to |
|---|---|---|
| `binary` (default) | Bare PCM16 bytes per WS message; WS close = hangup | Gemini Live, ElevenLabs, Vapi, AssemblyAI, Cartesia |
| `json` | JSON envelope `{"type":"audio","audio":"<b64>"}` + `{"type":"end"}` | OpenAI Realtime, Twilio media streams, Deepgram |

Pick the framing that matches the agent's native transport. If neither matches and you can't reconfigure the framework, [Pattern 9](infrastructure-patterns.md#pattern-9-transport-bridge) covers the in-container bridge.

## Channel shape

```yaml
actor:
  channels:
    - type: voice_ws
      url: ws://localhost:8080/voice
      protocol: binary              # or "json"
      # Optional persona tuning:
      language: en-US
      wait_for_callee_first: true
```

Fields:

| Field | Required | Default | Meaning |
|---|---|---|---|
| `type` | yes | — | Must be `voice_ws`. |
| `url` | yes | — | The WebSocket the actor will dial. Always `ws://localhost:<port>/<path>` — the actor and agent share the sandbox network. `wss://` is also accepted for external endpoints, but the in-sandbox case is `ws://`. |
| `protocol` | no | `binary` | Wire framing — see the table above. |
| `language` | no | `en-US` | BCP-47 tag used by the actor's STT and TTS. Set this when testing non-English flows. |
| `wait_for_callee_first` | no | `true` | If `true`, the actor expects the agent to speak first ("Thanks for calling Acme Bank, this is …"). If `false`, the actor speaks first. Most phone-call analogues want `true`. |

The schema also accepts `max_call_duration_s` and `silence_timeout_s`, but those fields are not currently threaded through to the runner — the actor uses a hardcoded 600 s call cap and does not honor a per-config silence timeout. Don't rely on either knob for tuning; either change the runtime constant or wait for the fields to be wired through.

## Wire protocol

Audio is the same on both ends in either framing:

| Property | Value |
|---|---|
| Sample rate | 24,000 Hz |
| Sample format | signed 16-bit little-endian (`s16le`) |
| Channels | mono |
| Frame cadence | bridges should emit at 50 fps (20 ms / frame). The actor is tolerant of bursty input, but its own *output* pump sends at 50 fps — match it on the way in for symmetric behavior |
| End of call | `binary`: either side closes the WebSocket. `json`: either side closes the WS, or the agent sends `{"type":"end"}` first for a graceful hangup |

### Binary framing (`protocol: binary`)

Every WebSocket message is binary, and every binary message is raw PCM16 bytes — `Int16Array` little-endian. No envelope, no control plane, no JSON metadata. A text frame is a protocol violation (the actor will disconnect).

### JSON framing (`protocol: json`)

Every WebSocket message is text. The actor sends and accepts these message shapes:

```json
{"type": "audio", "audio": "<base64-encoded PCM16 24 kHz mono>"}
{"type": "end"}
```

The agent should respond with `{"type":"audio", ...}` messages of the same shape, and may send `{"type":"end"}` to signal a graceful hangup. Bytes inside `audio` are still raw PCM16 — the JSON layer is just an envelope to match the OpenAI Realtime / Twilio / Deepgram wire shapes.

## Turn detection and the trailing silence convention

The Veris voice actor uses server-side VAD with a ~1500 ms silence window to detect end-of-turn. That means: **after the agent finishes a turn, the bridge must keep sending audio frames** — specifically silence — for at least ~1700 ms so the actor's VAD can commit. If the agent stops emitting bytes entirely between turns, the actor's VAD never sees end-of-speech and the conversation deadlocks.

Speech-to-speech realtime models (OpenAI Realtime, Gemini Live, AWS Nova Sonic) emit audio deltas only while the model is actively speaking — they do **not** fill the gaps between turns with silence on their own. So a naive bridge that just forwards the model's deltas to the actor will hang after the first reply.

Two patterns that work:

1. **Pace a 20 ms frame clock and inject silence during gaps.** Drain the model's audio output into a queue, then run a separate 50 fps pump that pulls a frame from the queue if available or emits a 20 ms silent frame otherwise. This is what Veris's own actor does on its output path — see `sandbox/actors/app/channels/voice_base.py:_forward_audio_delta` in the platform repo for the canonical implementation. The bridge stays "always live" the way a real microphone would be.

2. **Pump explicit silence at turn end.** After detecting "agent turn complete" (on OpenAI Realtime that's the `response.done` event; on most frameworks there's an equivalent signal), send ~1700 ms of zero-valued PCM16 frames in a burst:

   ```python
   SAMPLE_RATE_HZ = 24000
   END_OF_TURN_SILENCE = b"\x00\x00" * (SAMPLE_RATE_HZ * 1700 // 1000)
   await actor_ws.send_bytes(END_OF_TURN_SILENCE)
   ```

   Simpler than the continuous pump, fine for one-turn-per-response shapes, but loses the "always live mic" semantics during long tool calls where the agent should still be hearing the caller.

If your simulation hangs after the agent's first reply (actor never sends a follow-up), missing silence is the first thing to check.

### Pipecat WS transports need explicit end-of-turn silence

Pipecat exposes a `TransportParams.audio_out_auto_silence` flag (defaults to `True`) that sounds like it does exactly the "always live mic" pump described above. **It is only honored by the WebRTC transports** — `SmallWebRTCTransport` and `DailyTransport`. The WebSocket transports — `WebsocketServerTransport` and `FastAPIWebsocketTransport` — ignore the flag and just stop sending bytes when the bot's audio queue drains. (Grep `audio_out_auto_silence` in the pipecat source to confirm; only the WebRTC transports reference it.)

So a Pipecat agent that serves `voice_ws` directly — the "case 1 / no bridge needed" green path described below — still hits the deadlock unless you wire silence in yourself. The bot greets, the WS goes quiet, the actor's VAD never sees `speech_stopped`, and the call runs out the simulation clock.

The fix is the end-of-turn-burst pattern from above, implemented as a Pipecat `FrameProcessor` inserted between the LLM and `transport.output()`:

```python
# app/processors.py
from pipecat.frames.frames import Frame, OutputAudioRawFrame, TTSStoppedFrame
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor


class TrailingSilenceProcessor(FrameProcessor):
    """After every bot turn, emit ~1700 ms of PCM silence so the Veris actor's
    VAD can commit end-of-speech."""

    def __init__(self, *, sample_rate=24000, num_channels=1,
                 silence_ms=1700, chunk_ms=20):
        super().__init__()
        samples_per_chunk = sample_rate * chunk_ms // 1000
        self._chunk_bytes = samples_per_chunk * 2 * num_channels  # PCM16
        self._n_chunks = silence_ms // chunk_ms
        self._sample_rate = sample_rate
        self._num_channels = num_channels

    async def process_frame(self, frame, direction):
        await super().process_frame(frame, direction)
        await self.push_frame(frame, direction)
        if isinstance(frame, TTSStoppedFrame) and direction == FrameDirection.DOWNSTREAM:
            silence = b"\x00" * self._chunk_bytes
            for _ in range(self._n_chunks):
                await self.push_frame(
                    OutputAudioRawFrame(
                        audio=silence,
                        sample_rate=self._sample_rate,
                        num_channels=self._num_channels,
                    ),
                    direction,
                )
```

Wire it into the pipeline only on the `voice_ws` path (the WebRTC browser path doesn't need it):

```python
Pipeline([
    transport.input(),
    user_aggregator,
    llm,
    TrailingSilenceProcessor(),   # WS path only
    transport.output(),
    assistant_aggregator,
])
```

The one trap to watch for: key the burst off `TTSStoppedFrame`, **not** `BotStoppedSpeakingFrame`. `TTSStoppedFrame` is emitted by the LLM / TTS service and flows downstream through your processor; `BotStoppedSpeakingFrame` is emitted by the *output transport itself*, downstream of any processor sitting before it, so a processor wired in this position will never see it and will silently do nothing.

The 1700 ms tail = 1500 ms (the actor's server-VAD silence window) + 200 ms safety. Tune the safety margin if you see late commits, but don't go below ~1600 ms.

## Choosing how the agent reaches `voice_ws`

The actor will always speak whichever framing the channel is configured for. The agent has three options for matching it:

1. **The framework natively speaks the configured framing.** Pipecat's `WebsocketServerTransport` configured with a `RawAudioFrameSerializer` matches `protocol: binary` (but see the [Pipecat WS transports note](#pipecat-ws-transports-need-explicit-end-of-turn-silence) above — you still need to add a silence-tail processor). A bare OpenAI Realtime endpoint already speaks `protocol: json` (the envelope is OpenAI's own wire format). With the right transport plugin, the agent serves `voice_ws` directly — no bridge process, no extra container.

2. **The framework speaks a different transport.** LiveKit Agents (WebRTC end-to-end), agents wired to SIP/Twilio media streams, custom in-house frameworks with incompatible message envelopes — all need a small bridge process inside the sandbox container that translates between the actor's framing and the framework's native transport. See [Pattern 9: Transport bridge](infrastructure-patterns.md#pattern-9-transport-bridge) for the architecture.

3. **The agent is custom and you control the wire format.** Implement a `voice_ws` handler directly in the agent — accept WS frames in the configured framing, route them into your speech/LLM stack, write response audio back. Minimum-viable voice agents typically take this path.

The first question to ask of any voice agent is which of these three applies. If the framework's transport is fixed and matches neither `binary` nor `json` framing, you are in case (2) and need a bridge — that's not a Veris limitation, it's a property of the framework.

Hosted runtimes are case (3) with a twist: the agent process serves `voice_ws` itself and bridges *outbound* to the vendor's cloud. See [Vapi](#vapi-hosted-runtime-server-tool-webhooks) below for the worked shape, including the public-webhook requirement its server tools add.

## Worked examples

### `protocol: binary` — bridge / Pipecat / direct PCM16 endpoint

```yaml
version: "1.0"

actor:
  channels:
    - type: voice_ws
      url: ws://localhost:8080/voice
      protocol: binary
      language: en-US
      wait_for_callee_first: true

agent:
  code_path: /agent
  entry_point: uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port 8080
  port: 8080
  environment:
    LOG_LEVEL: info
```

That's the whole config for an agent whose framework speaks PCM16 over WS directly (case 1) or one that bundles a `Pattern 9` bridge (case 2 — only the `entry_point` changes to `bash start.sh`).

### `protocol: json` — OpenAI Realtime / Twilio-style envelope

```yaml
version: "1.0"

actor:
  channels:
    - type: voice_ws
      url: ws://localhost:8080/voice
      protocol: json
      language: en-US
      wait_for_callee_first: true

agent:
  code_path: /agent
  entry_point: uv run --no-sync python -m app.realtime_server
  port: 8080
```

The agent receives `{"type":"audio","audio":"<b64 PCM16>"}` messages from the actor and replies with the same shape. The actor handles base64 encoding/decoding on its side; the agent's job is to (un)wrap the JSON envelope around the same PCM16 bytes it would handle in binary mode.

## Vapi: hosted runtime, server-tool webhooks

Vapi is a hosted voice runtime — endpointing, turn-taking, STT, the LLM call, and TTS all run on Vapi's cloud. There is no library to embed and no in-container media server (contrast the LiveKit shape in [Pattern 9](infrastructure-patterns.md#pattern-9-transport-bridge)): the agent process itself serves `voice_ws` (`protocol: binary`) and acts as an outbound bridge. Per actor connection it:

1. POSTs `https://api.vapi.ai/call` with an **inline assistant** (prompt, model, voice, transcriber, tools — config is per-call; there is no persistent agent record to pin) and a WebSocket transport: `transport.provider: vapi.websocket` with `audioFormat` `pcm_s16le` / `raw` / `24000`, matching the actor's audio contract exactly.
2. Dials the `transport.websocketCallUrl` Vapi returns and pumps PCM16 both ways between the actor WS and the Vapi WS.
3. Flushes the ~1700 ms end-of-turn silence burst when Vapi sends `speech-update` with `role=assistant`, `status=stopped`. Vapi streams audio only while the assistant is speaking, so the [trailing-silence convention](#turn-detection-and-the-trailing-silence-convention) applies in full.

### Tools require a public inbound URL

Tools are the integration's distinctive piece. Each Vapi tool carries a `server.url`; when the LLM picks one, Vapi's *cloud* POSTs a `tool-calls` webhook to that URL and takes the result from the HTTP response. There is no way to answer a tool call over the audio WebSocket — client→server messages on that socket carry only audio and call control. So the sandbox pod must be publicly reachable:

- **In-pod tunnel** — spawn `ngrok http $PORT` lazily on the first `/voice` call (needs `NGROK_AUTHTOKEN` set via `veris env vars set`, and the `ngrok` binary installed in `Dockerfile.sandbox`) and point each tool's `server.url` at the tunnel. Works out of the box for single calls and small batches.
- **Shared stable endpoint** — set `PUBLIC_BASE_URL` and skip the tunnel entirely: point every call at one public webhook and route inside it by `call.id`. Vapi correlates tool results purely by `toolCallId`, not by connection, so one stateless endpoint serves arbitrarily many concurrent calls. This is the production shape and the concurrency-safe one.

**Free-tier ngrok allows one agent session per authtoken**, so concurrent simulations contend for the single tunnel: losing pods retry the spawn with backoff, and under sustained concurrency they exhaust their retries, call setup fails, and the actor sees `callee_no_answer`. A batch where most calls fail to connect looks like a flaky agent when it's the tunnel — see [troubleshooting](../phases/troubleshooting.md#vapi-calls-fail-to-connect-under-concurrency-ngrok-contention).

### The silent string-result trap

The tool webhook must answer `{"results": [{"toolCallId": ..., "result": "<string>"}]}` with the result as a JSON **string** (`json.dumps(output, default=str)`), over HTTP 200. ElevenLabs at least fails loudly on this class of mistake (a `1008` disconnect); **Vapi fails silently**: a non-string `result` — or a non-200 response — is dropped, Vapi logs "No result returned", and the model continues with **no observation at all**. The agent appears to ignore its own tools. Keep results single-line strings, return failures as a string under the `error` key, and always return 200.

### Grader visibility

Vapi's server tools execute in your process via the webhook and never reach the spoken transcript, so they hit exactly the visibility gap described in the next section. Emit the `agent_tool_call` event from the single `/tool` dispatch point, on both the success and error paths.

## Making client-tool calls visible to the grader

This is the one place a voice integration adds Veris-aware code to the agent. It's a deliberate exception to the skill's no-Veris-specific-code rule (see [SKILL.md](../SKILL.md#reporting-client-tool-calls-to-the-grader-is-a-sanctioned-exception-voice-agents-only)) — keep it as minimal as the snippet below.

### The problem

For voice simulations the grader's trace is reconstructed from **two sources only**: the spoken transcript (the actor's STT'd turns and the agent's STT'd replies) and any `agent_tool_call` events the agent reports to the engine. Hosted speech-to-speech platforms run their tools as **client tools** — ElevenLabs Conversational AI, OpenAI Realtime function calls handled in your process, Gemini Live — or, like Vapi, as **server tools** the platform POSTs back to your webhook over HTTP. Either way the tool executes *inside your agent process* and the call and its result round-trip on the vendor's WebSocket (or webhook); they never appear in the spoken transcript.

So unless the agent reports them, the grader sees only words. It can't distinguish an agent that actually froze the card from one that only said it did, and it will false-flag real, completed actions (freezes, replacements, lookups) as hallucinations or "no tool call." Text/HTTP agents don't hit this — the OTel pipeline captures their tool calls automatically. Voice is the gap.

### The fix: emit an `agent_tool_call` event per tool

After each client tool runs, POST an event to the sandbox engine. The platform's trace renderer turns each one into an assistant `tool_calls` turn plus a `tool` result turn, interleaved with the spoken turns by timestamp — the same shape a text agent's trace has, so one grader works for both.

**Endpoint**

```
POST {ENGINE_URL}/simulations/{SIMULATION_ID}/events
```

Both values come from the agent's own environment, set by the sandbox: `SIMULATION_ID` is exported into the container, and `ENGINE_URL` defaults to `http://localhost:6100` (the engine port is fixed). Outside a simulation `SIMULATION_ID` is unset — that's the signal to no-op.

**Body**

```json
{
  "service": "agent",
  "event_type": "agent_tool_call",
  "data": { "name": "<tool name>", "arguments": { }, "result": "<any>" }
}
```

| Field | Required | Notes |
|---|---|---|
| `event_type` | yes | Must be exactly `agent_tool_call` — that's what the renderer keys on. |
| `data.name` | yes | The tool name. Becomes the assistant `tool_calls[].name`. The renderer errors if it's missing. |
| `data.arguments` | yes | The call arguments, as an object. Rendered as the call's arguments. |
| `data.result` | no | The tool's return value. If present, becomes the `tool` result turn; omit for tools with no return value. |
| `service` | yes | Use `"agent"`. |

Serialize the body with `default=str` so enums and datetimes in the args or result don't raise.

**Copy-paste hook**

```python
import os
import json
import logging

import httpx

logger = logging.getLogger(__name__)

_ENGINE_URL = os.environ.get("ENGINE_URL", "http://localhost:6100")
_SIMULATION_ID = os.environ.get("SIMULATION_ID")


def report_tool_call(name: str, arguments: dict, result: object) -> None:
    """Report a client-tool call to the Veris engine so it lands in the graded
    trace. No-op outside a simulation; never raises into the call path."""
    if not _SIMULATION_ID:
        return
    body = json.dumps(
        {
            "service": "agent",
            "event_type": "agent_tool_call",
            "data": {"name": name, "arguments": arguments, "result": result},
        },
        default=str,
    )
    try:
        httpx.post(
            f"{_ENGINE_URL}/simulations/{_SIMULATION_ID}/events",
            content=body,
            headers={"Content-Type": "application/json"},
            timeout=2.0,
        )
    except Exception as exc:
        logger.warning("[tool] could not report %s to engine: %s", name, exc)
```

Call it from the single place every client tool resolves — right after the real tool runs, before you hand the result back to the vendor SDK:

```python
def handler(**arguments):
    result = tool_fn(**arguments)
    report_tool_call(name, arguments, result)     # observe, don't reshape
    return json.dumps(result, default=str)        # vendor wants a string — see the pitfall below
```

### Keep it an exception, not a wrapper

Three constraints keep this honest — they are what make it instrumentation rather than the kind of shim the skill forbids:

- **No-op in production**, gated on `SIMULATION_ID`. No Veris-specific behavior ships to real callers.
- **Fire-and-forget, fail-soft** (short timeout, swallowed exceptions). Reporting must never break or delay the call.
- **Observe after the fact** — the same name/args/result the tool already produced, with no reshaping of anything the model sees.

If you find yourself changing arguments, rewriting results, or branching the agent's *behavior* on `SIMULATION_ID`, you've crossed from instrumentation into a wrapper — stop.

### Verify it worked

After a smoke simulation:

- Confirm `agent_tool_call` events appear in the sim's event stream (the engine records them alongside the spoken turns).
- Read the grader's justifications — they should reference your tools by name ("called `change_card_status` with …"). If the grader says the agent "made no tool call" or "fabricated" an action your agent logs show it performed, the emit is missing or `event_type` / `data.name` is wrong. See [troubleshooting.md](../phases/troubleshooting.md#grader-flags-a-voice-agent-for-hallucinating-tools-it-actually-called).

## Common pitfalls

- **Wrong sample rate.** If the agent emits 16 kHz or 48 kHz instead of 24 kHz, the actor's STT will fail silently — you'll see "actor never responds" rather than an error. Confirm 24 kHz end to end.
- **Stereo frames.** Mono only. A 2-channel PCM16 frame is twice the bytes for the same wall-clock audio and decodes to garbled audio.
- **WAV/RIFF headers.** Send raw PCM samples (or base64 of raw PCM in JSON mode), not a WAV file. If you're using a TTS that defaults to WAV, request `format: "pcm"` or `response_format: "pcm"`.
- **Framing mismatch.** A binary WS message in `protocol: json` mode (or a text/JSON message in `protocol: binary` mode) is a protocol violation — the actor will disconnect. Make sure the agent's transport and the channel's `protocol` field agree.
- **Missing silence between turns.** Covered above — the most common cause of "simulation hangs after the first turn."
- **Tool-result payloads must serialize as strings, not dicts.** Voice tool platforms (ElevenLabs `client_tool_result.result`, OpenAI Realtime `function_call_output.output`, Vapi tool webhooks) each validate the result field against their own schema — most expect a string. Returning a `model_dump()` dict from a Pydantic model gets rejected by the orchestrator (ElevenLabs disconnects with `1008 policy violation: ClientToolResultClientToOrchestratorEvent`) and the sim hangs until timeout instead of failing loudly. Vapi's variant is quieter still: a non-string `result` (or a non-200 response) is silently dropped — Vapi logs "No result returned" and the model continues with no observation, so nothing hangs and nothing errors. Wrap with `json.dumps(result, default=str)` — the `default=str` covers enums and datetimes that aren't natively JSON-serializable.
- **WebRTC frameworks need a real dispatch gate, not a `sleep`.** LiveKit Agents (and any framework whose worker is *dispatched* into rooms) registers with its media server asynchronously and self-throttles on CPU by default. Bring the actor-facing bridge up before the worker registers, or leave the prod-mode CPU throttle on, and a chunk of calls under load end in `callee_no_answer` with no audio — passing every single-call local test first. Gate on the worker's registration log line and pin its load function to zero — see [infrastructure-patterns.md → LiveKit dispatch gotchas](../reference/infrastructure-patterns.md#livekit-dispatch-gotchas).

## Not yet covered

- SIP / PSTN ingress. Veris currently exposes the voice channel only over WebSocket; calling the agent from a real phone number is a platform feature, not a `veris.yaml` channel option.
- DTMF events. Tone detection and dialed-digit handling are not part of the `voice_ws` channel today.
- Multi-channel audio (caller + agent recorded on separate channels). Recordings produced by the actor are mono mixed.
