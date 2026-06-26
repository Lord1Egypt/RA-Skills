# Qwen3-ASR Reference (qwen3-asr-rs)

Pure-Rust speech-to-text engine for Qwen3-ASR models with Metal/CUDA acceleration.

Source: https://github.com/alan890104/qwen3-asr-rs | Crates.io: `qwen3-asr`

## Table of Contents

- [Setup](#setup)
- [Batch Transcription](#batch-transcription)
- [Streaming Transcription](#streaming-transcription)
- [Audio Requirements](#audio-requirements)
- [Performance](#performance)
- [Long Audio Handling](#long-audio-handling)

## Setup

### Model Download

```bash
pip install huggingface_hub

# 0.6B — 1.7GB, fast, recommended for real-time
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir models

# 1.7B — 4.5GB, higher accuracy
huggingface-cli download Qwen/Qwen3-ASR-1.7B --local-dir models_1.7b
```

### Build

```bash
git clone https://github.com/alan890104/qwen3-asr-rs.git
cd qwen3-asr-rs

# macOS (Metal GPU, default)
cargo build --release

# Linux/Windows (NVIDIA CUDA)
cargo build --release --no-default-features --features cuda

# CPU only
cargo build --release --no-default-features
```

### As Rust Dependency

```toml
# macOS Metal
[dependencies]
qwen3-asr = "0.2"

# NVIDIA CUDA
[dependencies]
qwen3-asr = { version = "0.2", default-features = false, features = ["cuda"] }

# CPU
[dependencies]
qwen3-asr = { version = "0.2", default-features = false }
```

## Batch Transcription

```rust
use qwen3_asr::{AsrInference, TranscribeOptions, best_device};

let device = best_device(); // auto: CUDA → Metal → CPU
let engine = AsrInference::load("models/", device)?;
let result = engine.transcribe("audio.wav", TranscribeOptions::default())?;

println!("Language: {}", result.language);
println!("Text: {}", result.text);
```

### Auto-download from HuggingFace (with `hub` feature)

```rust
let engine = AsrInference::from_pretrained(
    "Qwen/Qwen3-ASR-0.6B",
    Path::new("models/"),
    device,
)?;
```

## Streaming Transcription

For real-time low-latency transcription (~2s latency):

```rust
use qwen3_asr::StreamingOptions;

let mut state = engine.init_streaming(StreamingOptions::default());

for chunk in mic_chunks { // 16kHz f32 samples
    if let Some(result) = engine.feed_audio(&mut state, &chunk)? {
        println!("Live: {}", result.text);
    }
}

let final_result = engine.finish_streaming(&mut state)?;
println!("Final: {}", final_result.text);
```

## Audio Requirements

- **Format**: WAV (via `hound` crate) or raw f32 samples
- **Sample rate**: 16 kHz (resampled automatically via `rubato`)
- **Channels**: Mono
- **Input**: Local file path or `&[f32]` sample array

Convert with ffmpeg:
```bash
ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav
```

## Performance

Apple Mac mini M4 (16GB), Metal backend:

| Model | Avg RTF | Load Time | Memory |
|-------|---------|-----------|--------|
| 0.6B BF16 | 0.230 | 489ms | 1.9GB |
| 1.7B BF16 | 0.319 | 4250ms | 4.6GB |

RTF < 1.0 = faster than real-time. Both models run 3-7x faster than real-time on M4.

## Long Audio Handling

### Constraints

- Qwen3-ASR officially supports single speech up to **20 minutes**
- Streaming mode: memory/latency grows with session duration
  - <2 min: smooth
  - ~10 min: ~1s/step, acceptable
  - ~20 min: ~3-5s/step, upper limit
  - \>20 min: not feasible

### Strategy: Split and Batch

For podcast episodes (often 30-120 min), split audio at silence boundaries and batch-transcribe:

```rust
// Split with ffmpeg first, then:
for seg_file in segment_files {
    let result = engine.transcribe(&seg_file, TranscribeOptions::default())?;
    transcript.push(result.text);
}
let full_text = transcript.join("\n\n");
```

Split with ffmpeg:
```bash
# Detect silence points
ffmpeg -i episode.wav -af "silencedetect=noise=-30dB:d=2" -f null - 2>&1 | grep silence_end

# Split at specific times
ffmpeg -i episode.wav -f segment -segment_times 120.5,240.3,360.1 \
  -ar 16000 -ac 1 segment_%03d.wav
```

### Strategy: Streaming with Session Reset

For long-running streams, reset sessions at silence boundaries:

```rust
let mut state = engine.init_streaming(StreamingOptions::default());
loop {
    let chunk = read_audio();
    if vad_detects_silence(&chunk) {
        let result = engine.finish_streaming(&mut state)?;
        save(&result);
        // Pass last ~200 chars as context for continuity
        let ctx = result.text.chars().rev().take(200).collect::<String>();
        let mut opts = StreamingOptions::default().with_initial_text(ctx);
        state = engine.init_streaming(opts);
    } else {
        engine.feed_audio(&mut state, &chunk)?;
    }
}
```
