# Deployment Options

Supertonic runs across multiple runtimes and platforms. Choose based on your environment.

## Python SDK

```bash
pip install supertonic
```

- First run auto-downloads ~400MB model from Hugging Face
- Models cached in `~/.cache/supertonic3/`
- Minimal dependencies: onnxruntime, numpy, soundfile, huggingface-hub

## CLI

```bash
supertonic tts "Your text" -o output.wav --voice M3 --steps 10
```

## Multi-Runtime Support

| Runtime | Platform | Notes |
|---------|----------|-------|
| Python | Desktop, server, edge | Primary SDK |
| Node.js | Server, Electron apps | Via ONNX Runtime Node |
| Browser (WebGPU) | Client-side web | Runs in browser, no server needed |
| Java | JVM apps, Android | Via ONNX Runtime Java |
| C++ | Embedded, high-performance games | Native integration |
| C# | .NET apps, Unity | Via ONNX Runtime .NET |
| Go | Backend services, CLI tools | Via ONNX Runtime Go |
| Swift/iOS | iOS apps, macOS | Native iOS deployment |
| Rust | Systems programming, WebAssembly | Via ONNX Runtime Rust |
| Flutter | Cross-platform mobile | Via platform channels |

## Hardware Requirements

- **CPU**: Any x86_64 or ARM64 with SSE4/NEON support
- **RAM**: ~500MB for model + inference
- **Storage**: ~400MB for model files
- **GPU**: Not required (CPU inference is fast enough)

## Speed Benchmarks (Supertonic-3, 2 inference steps)

| Hardware | Real-time Factor |
|----------|-----------------|
| Apple M4 Pro | 167× |
| Consumer desktop CPU | 50–100× |
| Raspberry Pi 4 | 5–10× |

## Use Cases

- **E-readers**: Offline audiobook generation
- **IoT devices**: Voice alerts without connectivity
- **Privacy-first apps**: No voice data leaves device
- **Gaming**: Dynamic NPC dialogue
- **Accessibility**: Screen readers, assistive devices
- **Content creation**: Rapid voiceover drafts
