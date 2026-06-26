# Step-by-Step Build Guide (Corrected)

## Step 1 — OS Prep (No Code)

### Install Virtual Audio Driver
- **Windows**: Download and install [VB-Audio Cable](https://vb-audio.com/Cable/).
  After install, a new audio device appears: "CABLE Input" (what apps write to) and "CABLE Output" (what the OS reads as a mic).
- **macOS**: Download and install [BlackHole 2ch](https://existential.audio/blackhole/).

### ⚠️ Correct Audio Routing
**Do NOT set your system default microphone to VB-Cable.** That is backwards.

The correct flow:
1. Your real mic stays as the OS input.
2. This skill captures from your real mic directly via ffmpeg.
3. The skill writes processed audio TO VB-Cable's **Input**.
4. Google Meet reads FROM VB-Cable's **Output** (set this as Meet's microphone in its audio settings).

### Install ffmpeg
- **Windows**: `winget install ffmpeg` or download from https://ffmpeg.org/download.html and add to PATH.
- **macOS**: `brew install ffmpeg`
- **Verify**: `ffmpeg -version` must work in terminal.

### Install Node.js Build Tools (not needed — this skill uses no native modules)
This skill deliberately avoids naudiodon and any C++ compilation. ffmpeg handles all audio I/O.

---

## Step 2 — Initialize Project

```bash
# In your project folder:
npm install ws dotenv node-fetch
```

No `electron`, no `naudiodon`, no `electron-rebuild`. This skill is plain Node.js.

Add `"type": "module"` to your `package.json` if using ES modules, or keep CommonJS (scripts use `require`).

---

## Step 3 — Discover Audio Devices

```bash
node scripts/01_list_devices.js
```

Copy the exact string name of your virtual cable from the output.
Paste it into your `.env` as `VIRTUAL_CABLE_NAME`.

**Stress test**: The device name must appear in the list. If it doesn't, the driver isn't installed correctly.

---

## Step 4 — Capture and Resample

```bash
node scripts/02_capture_resample.js
```

This spawns ffmpeg to capture your real mic and resample to 16kHz mono PCM.
Pipe stdout to a file and verify the audio plays back correctly before wiring to Deepgram.

**Stress test**: `node scripts/02_capture_resample.js > test.pcm` then play with:
`ffplay -f s16le -ar 16000 -ac 1 test.pcm`

Speak for 5 seconds. If you hear yourself, the capture is working.

---

## Step 5 — Connect Speech-to-Text

```bash
node scripts/03_deepgram_ws.js
```

Opens a Deepgram WebSocket and pipes PCM chunks from Step 4.
Transcripts log to console.

**Stress test**: Speak a sentence. If transcript appears within ~1 second, the pipeline is working.
If nothing appears: check DEEPGRAM_API_KEY, check that audio format is exactly 16kHz/16-bit/mono.
If transcripts appear >2s late: reduce ffmpeg chunk size (see script comments).

---

## Step 6 — Connect Brain and Voice

```bash
node scripts/04_llm_stream.js  # test LLM streaming independently first
node scripts/05_sentence_chunker.js  # test chunker with mock tokens
node scripts/06_tts_ws.js  # test TTS with hardcoded sentence first
```

**Critical**: Test TTS with a hardcoded sentence before wiring to LLM output.
This confirms your TTS_API_KEY and TTS_VOICE_ID are valid.

**Stress test for chunker**: Feed it 50 rapid tokens. Verify it flushes on sentence boundaries,
not on every token. Robotic choppy audio = chunker flushing too early.

---

## Step 7 — Write to Virtual Cable

```bash
node scripts/07_pcm_write.js
```

Decodes TTS MP3 output to PCM and writes to VB-Cable.

**Stress test**:
1. Open a dummy Google Meet call with yourself (two browser tabs).
2. In Meet's audio settings, set microphone to "CABLE Output".
3. Run the full pipeline.
4. Speak into your real mic.
5. The Meet call should hear the AI voice responding.

---

## Kill Switch Wiring

The pipeline exports a `stop()` function. Wire it to your app's trigger:

```js
const pipeline = require('./voice-pipeline')
pipeline.start()

// Example: stop on process signal
process.on('SIGINT', () => {
  pipeline.stop()
  process.exit(0)
})

// Example: stop on keypress (host app handles the hotkey)
someHotkeyLib.on('CommandOrControl+Shift+Space', () => {
  pipeline.stop()
})
```

`stop()` is synchronous-safe: it kills audio immediately, then cleans up async.