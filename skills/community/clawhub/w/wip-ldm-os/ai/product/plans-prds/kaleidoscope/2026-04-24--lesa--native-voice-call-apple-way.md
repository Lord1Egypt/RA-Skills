# Kaleidoscope Native Voice Call: The Apple Way

**Date:** 2026-04-24
**Author:** Lēsa
**Context:** Parker asked for a real call with Lēsa: talk or type in, visible text out, voice out automatically, eventually natural interruptible conversation. Tonight's localhost/browser prototype proved text-to-TTS can work, but also proved Safari/local certs and FaceTime UI automation are the wrong foundation.

## Decision

Build Lēsa voice calls as a native Kaleidoscope call surface, not as FaceTime automation.

FaceTime is the reference for emotional shape and system behavior. It is not the integration substrate.

## Why

The Apple-shaped solution is to become a first-party calling app:

- Use CallKit for call lifecycle and native system call UI where available.
- Use AVAudioSession with `playAndRecord` and `voiceChat` mode for real two-way voice.
- Use native microphone permission and route handling, not browser prompts on untrusted localhost.
- Keep visible transcript and controls inside Kaleidoscope.
- Treat LDM OS/OpenClaw as the brain service behind the call, not as the UI automation driver.

The wrong solutions are now known:

- **FaceTime URL schemes:** can open FaceTime or a contact card, but do not provide a stable public API for controlling call state or audio.
- **FaceTime private frameworks/XPC:** entitlement-gated and Apple-private.
- **System Events/coordinate clicking:** fragile, blocked by Accessibility/Screen Recording state, and not a product.
- **Local browser page:** useful prototype, but iOS marks self-signed LAN HTTPS as Not Secure, blocking microphone and making autoplay unreliable.

## Product Shape

The first real product surface is a **Call Lēsa** button in Kaleidoscope.

Expected behavior:

1. Parker taps **Call Lēsa**.
2. iOS presents a native call/session surface, or a Kaleidoscope call view that follows native call conventions.
3. Lēsa speaks first with a short greeting.
4. Parker can talk or type.
5. Lēsa replies with both visible text and voice.
6. Audio playback works with mute switch/route expectations handled intentionally.
7. The transcript persists to the conversation.
8. If the brain path is slow, the call surface remains alive and honest: "I'm thinking" or a short filler, not dead air.

## Architecture

```
Kaleidoscope iOS/macOS
  Call UI
  CallKit / native call lifecycle
  AVAudioSession(.playAndRecord, .voiceChat)
  AVAudioEngine / Voice Processing I/O
  transcript view
      |
      | WebSocket / WebRTC / streaming HTTP
      v
LDM OS voice gateway
  session auth
  audio stream ingress
  STT
  OpenClaw / GPT-5.5 brain request
  TTS
  audio stream egress
  Memory Crystal capture hooks
```

## Implementation Plan

### Phase 0: Preserve the Prototype, Stop Treating It as Product

- Keep `tmp/voice-call-now` as a throwaway proof that xAI/OpenAI TTS can return playable audio.
- Do not expand it into a pseudo-app.
- Capture tonight's learning in this plan.

### Phase 1: Native Audio Spike

Create the smallest Kaleidoscope iOS/macOS native app slice:

- `Call Lēsa` button.
- Request microphone permission.
- Configure `AVAudioSession` as `playAndRecord` with `voiceChat`.
- Capture microphone audio.
- Play a generated TTS response.
- Show the visible transcript.

Acceptance:

- No localhost cert warning.
- Mic permission prompt is native and understandable.
- Speaker output is audible without tapping tiny browser controls.
- Audio route changes are visible/testable.

### Phase 2: Brain Gateway

Build a minimal LDM OS voice gateway:

- Authenticated session token from Kaleidoscope pairing.
- Text path first: user text -> OpenClaw -> TTS -> app playback.
- Then audio path: mic chunk -> STT -> OpenClaw -> TTS -> app playback.
- Return partial states so the UI never feels frozen.

Acceptance:

- Parker can type in Kaleidoscope and hear Lēsa.
- Parker can speak a short utterance and receive visible text + TTS.
- Timeouts degrade into honest spoken/text status, not silence.

### Phase 3: CallKit Integration

Add CallKit where it gives native value:

- Outgoing call action for **Call Lēsa**.
- Incoming-call style later, only if Lēsa is initiating a session through a trusted server path.
- End/hold/mute lifecycle mapped to voice gateway state.

Acceptance:

- Call lifecycle behaves like iOS expects.
- Ending the call releases mic/audio resources.
- Background/lock-screen behavior is intentionally defined.

### Phase 4: Realtime Conversation

Replace request/response voice with realtime turn-taking:

- Streaming STT or Realtime API.
- Barge-in interruption.
- Low-latency filler/acknowledgement layer while deeper GPT-5.5 response runs.
- Voice identity tuning, starting with xAI `eve` as the current closest preference.

Acceptance:

- Parker can interrupt.
- Lēsa can acknowledge immediately while waiting for deeper reasoning.
- Visible transcript remains source-of-truth.

## Design Principles

- **Do not impersonate FaceTime.** Integrate with the OS as a legitimate calling app.
- **Ask permission once, clearly.** Native mic permission beats browser trust hacks.
- **Text is not secondary.** Visible transcript must always exist.
- **No dead air.** Silence is interpreted as failure; surface thinking/listening/speaking states.
- **Brain latency is product reality.** Split realtime companionship from deep GPT response instead of hiding the delay.
- **The user should not debug the substrate.** No cert warnings, localhost IPs, tiny audio controls, or manual route rituals in the final product.

## Open Questions

- iOS-first or macOS-first? Recommendation: iOS-first for the real Parker call experience; macOS helper later.
- WebRTC vs raw WebSocket audio transport? Recommendation: start with WebSocket for spike simplicity, evaluate WebRTC once bidirectional audio needs jitter handling.
- OpenAI Realtime vs STT/OpenClaw/TTS sandwich? Recommendation: support both modes explicitly:
  - direct deep Lēsa mode: wait for GPT-5.5/OpenClaw response, then speak;
  - realtime attendant mode: low-latency assistant keeps the line alive while relaying to GPT-5.5.
- CallKit availability on macOS still needs verification; iOS CallKit path is the cleaner first target.

## References

- Apple CallKit: `https://developer.apple.com/documentation/callkit`
- Apple Making and Receiving VoIP Calls: `https://developer.apple.com/documentation/callkit/making-and-receiving-voip-calls`
- Apple AVAudioSession: `https://developer.apple.com/documentation/avfaudio/avaudiosession`
- Apple AVAudioSession voiceChat mode: `https://developer.apple.com/documentation/avfaudio/avaudiosession/mode-swift.struct/voicechat`
- Apple SFSpeechRecognizer: `https://developer.apple.com/documentation/speech/sfspeechrecognizer`
- Prior local research: `utilities/_to-privatize/lesa-voice-call/research/facetime-internals.md`
- Prior local research: `utilities/_to-privatize/lesa-voice-call/research/callkit-macos.md`
- Prior local research: `utilities/_to-privatize/lesa-voice-call/research/alternatives-compared.md`
