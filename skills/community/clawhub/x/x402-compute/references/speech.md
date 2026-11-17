# Text to speech (Grid speech)

Use this reference for text to speech, read-aloud, voiceovers, or operating a speech node. The
candidate is default off. Do not claim a model is live unless discovery returns it
(`kokoro-82m`, `chatterbox-turbo`).

## Availability and mode selection

```bash
curl "https://grid.x402compute.cc/v1/models"   # look for "kokoro-82m" / "chatterbox-turbo"
```

- A model missing from discovery is unavailable on Grid. Do not call a dark route, and do not
  substitute a chat model or another provider without asking.
- **Local** comes first for people on a Mac with Singularity Node: Voice Studio speaks on the
  device, and its optional Speech API (Overview > Speech API, `http://127.0.0.1:8094/v1`) is a
  plain OpenAI-compatible `POST /v1/audio/speech` for apps on that Mac. No wallet, no credits,
  nothing leaves the machine. Never fall back to Grid automatically.
- **Grid** is explicit opt-in and paid. Show the quote before the first paid request. The client
  seals the text to one reserved node before the Grid receives it; the Grid never sees the text or
  the audio.
- Grid models: `kokoro-82m` (Kokoro 82M, Apache-2.0: fast, 10 voices, adjustable speed) and
  `chatterbox-turbo` (Chatterbox Turbo, MIT: expressive, performs audio tags). Do not list
  Qwen3-TTS, Orpheus, Dia, voice cloning or voice design as Grid features: those are local-only.

## Audio tags (`chatterbox-turbo`)

Write tags in square brackets inside the text: `That was close. [laugh] Okay, again.`
Performed: `[laugh] [chuckle] [cough] [clear throat] [groan] [shush] [dramatic] [sarcastic]`
(also `[laughs]`, `[laughing]`, `[clears throat]`...). Any other `[word]` tag is removed by the node,
never read aloud; `kokoro-82m` removes all of them. Tags count as input bytes and are billed.

## Use the official SDK helper

The Grid request is not the OpenAI speech body. Use the official helper so the client verifies the
node identity, seals the text, verifies the signed result, decrypts it, and checks every binding.

TypeScript:

```typescript
import { writeFile } from "node:fs/promises";
import { GridClient } from "@singularity-layer/grid";

const grid = new GridClient({ apiKey: process.env.SGL_API_KEY! });
const speech = await grid.speak("Hello from a Singularity Layer node.", { voice: "af_heart" });
// Expressive, with tags (voice "aria", speed fixed at 1.00):
const fun = await grid.speak("You did it! [laugh] I knew you would.", { model: "chatterbox-turbo", voice: "aria" });
await writeFile("hello.m4a", speech.audio);   // AAC in an MP4 container
console.log(speech.durationSeconds, speech.costUsd);
```

Python:

```python
import os
from singularity_grid import GridClient

grid = GridClient(api_key=os.environ["COMPUTE_API_KEY"])
result = grid.speak_to_file("hello.m4a", "Hello from a Singularity Layer node.", voice="af_heart")
fun = grid.speak_to_file("fun.m4a", "You did it! [laugh]", model="chatterbox-turbo", voice="aria")
print(result.duration_seconds, result.cost_usd)
```

The helpers pay with prepaid credits (API key) and do not sign x402 payments. The direct x402
contract uses `use_credits=false` on reservation and an `X-Payment` challenge on submit.

## Contract

| Field | Exact value |
| --- | ---: |
| Protocol | `speech-v1` (both models) |
| Text | UTF-8, 1 to 1000 bytes, not blank, no NUL |
| `kokoro-82m` voices | `af_heart af_bella af_nicole bf_emma af_aoede af_kore af_sarah am_fenrir am_michael am_puck` |
| `kokoro-82m` speed | String with two decimals, `"0.50"` to `"2.00"` |
| `kokoro-82m` price | `max(100, bytes * 8)` micro-USDC: $8 per million bytes, $0.0001 minimum |
| `chatterbox-turbo` voice / speed | `aria` / `"1.00"` only |
| `chatterbox-turbo` price | `max(100, bytes * 15)` micro-USDC: $15 per million bytes, $0.0001 minimum |
| Output | m4a (AAC-LC, 24 kHz mono), at most 90 s |
| Operators | Keep 80% |

Split longer text into several requests of at most 1000 bytes each, at sentence boundaries.

## Two-request sealed contract

1. `POST /v1/audio/speech/reserve` sends only `model`, `model_revision`, `model_sha256`,
   `speech_protocol`, `request_id`, `voice`, `speed`, `input_bytes`, `use_credits`, and optional
   `node` / `max_price`.
2. Validate that the reservation repeats every binding and the quote; verify the node's signed
   X25519 key.
3. Seal the canonical request locally with `x25519-xchacha20poly1305-hkdf-v2`. The grid bills by
   the exact ciphertext length, so the plaintext must be the canonical JSON byte for byte.
4. `POST /v1/audio/speech` sends exactly `{reservation_token, enc}`.
5. Require the reserved node's Ed25519 signature (domain `speech`) before decryption, then check
   the result header (job, request, model, voice, speed, byte count, audio sha256) and the billed
   amount against the quote.

No failover: if a node fails, reserve again.

## Operating a speech node

Apple Silicon Mac only, one speech model per node. In the Singularity Node app (Grid mode), pick
the model under TTS: the app installs the speech runtime and the pinned model and starts serving.
From the CLI:

```bash
sgl start --model-name kokoro-82m \
  --tts-python "<venv>/bin/python" --tts-model-dir "<folder>/Kokoro-82M-bf16"
sgl start --model-name chatterbox-turbo \
  --tts-python "<venv>/bin/python" --tts-model-dir "<folder>/chatterbox-turbo-4bit"
```

Chatterbox Turbo runs at about real time on a 16 GB M-series Mac; faster Macs serve it better.

The node verifies every pinned model file and package version before it advertises the model.
