# Examples

## Demo — transcribe a short YouTube video

A real run captured on the **NVIDIA DGX Spark** (Whisper on CUDA). The video is
[`jNQXAC9IVRw`](https://www.youtube.com/watch?v=jNQXAC9IVRw) — "Me at the zoo",
19 seconds, the first video ever uploaded to YouTube.

### Command

```bash
bash scripts/yt-transcribe.sh "https://www.youtube.com/watch?v=jNQXAC9IVRw" --output-dir /tmp/yt-demo
```

### Output (real)

```console
=========================================
Processing: https://www.youtube.com/watch?v=jNQXAC9IVRw
=========================================
Fetching video info...
Category: Unsorted
Downloading audio...
[download] 100% of  246.27KiB in 00:00:00 at 984.74KiB/s
[ExtractAudio] Destination: .../Me_at_the_zoo_jNQXAC9IVRw.mp3
Download complete. Transcribing...
  Duration: 19s
  Model: base
  Device: cuda
  JS runtime: node:/path/to/node
Detected language: English

✓ Saved: /tmp/yt-demo/Unsorted/Me_at_the_zoo_jNQXAC9IVRw.txt
  Lines: 7

Summary: successes=1 skipped=0 failures=0
```

### Produced file

`examples/sample-output/Me_at_the_zoo_jNQXAC9IVRw.txt` is that transcript,
verbatim (Whisper mishears "trunks" as "punks" — real model output):

```text
URL: https://www.youtube.com/watch?v=jNQXAC9IVRw

Title: Me at the zoo

Alright, so here we are, one of the elephants.
The cool thing about these guys is that they have really, really, really long punks, and that's cool.
And that's pretty much all there is to say.
```

### Behaviour worth knowing

- **Idempotent**: re-running the same URL without `--output-dir` reports
  `✓ Already transcribed` and skips (no re-download/transcription).
- **Model** is auto-selected from the duration (`base` for a 19 s clip).
- Needs a **JavaScript runtime** for `yt-dlp` (here `node`); without one yt-dlp
  fails with a misleading `HTTP Error 403: Forbidden`.
- No API key, no secret, no upload: everything runs locally.
