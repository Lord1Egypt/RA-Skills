# MLX Swift & llama.cpp Reference

Complete reference for running open-source LLMs on Apple platforms using
MLX Swift and llama.cpp.

## Contents

- [MLX Swift](#mlx-swift)
- [llama.cpp](#llamacpp)
- [Multi-Backend Architecture](#multi-backend-architecture)
- [Built-in Apple Frameworks](#built-in-apple-frameworks)
- [Performance Best Practices](#performance-best-practices)
- [Review Checklist](#review-checklist)

## MLX Swift

Apple's ML framework for Swift. Highest sustained generation throughput on
Apple Silicon via unified memory architecture.

### Key Characteristics

- Unified memory: operations run on CPU or GPU without data transfer
- Lazy computation: operations computed only when needed
- Automatic differentiation for training
- Metal GPU acceleration
- Research-oriented but increasingly used in production

### Loading and Running LLMs

```swift
import MLX
import MLXLLM
import MLXLMCommon
import MLXLMHFAPI
import MLXLMTokenizers

let container = try await LLMModelFactory.shared.loadContainer(
    from: HubClient.default,
    using: TokenizersLoader(),
    configuration: .init(id: "mlx-community/Qwen3-4B-4bit")
)

let session = ChatSession(container)
print(try await session.respond(to: "Hello"))

// Use ModelContainer directly when you need streaming control.
let input = try await container.prepare(input: UserInput(prompt: "Hello"))
let stream = try await container.generate(
    input: input,
    parameters: GenerateParameters(temperature: 0.0)
)
for await event in stream {
    if case .chunk(let text) = event {
        print(text, terminator: "")
    }
}
```

### Recommended Models by Device

| Device | RAM | Recommended Model | Disk Size | RAM Usage |
|---|---|---|---|---|
| iPhone 12-14 | 4-6 GB | SmolLM2-135M or Qwen 2.5 0.5B | ~278 MB | ~0.3 GB |
| iPhone 15 Pro+ | 8 GB | Gemma 3n E4B 4-bit | ~2.7 GB | ~3.5 GB |
| Mac 8 GB | 8 GB | Llama 3.2 3B 4-bit | ~1.8 GB | ~3 GB |
| Mac 16 GB+ | 16 GB+ | Mistral 7B 4-bit | ~4 GB | ~6 GB |

### Memory Management Rules

1. Never exceed 60% of total RAM on iOS
2. Set MLX cache limits:
   ```swift
   Memory.cacheLimit = 512 * 1024 * 1024 // 512 MB
   ```
3. Monitor memory pressure with `Memory.snapshot()` and reduce cache under pressure
4. Unload MLX and llama.cpp models on backgrounding or memory pressure; for MLX,
   also call `Memory.clearCache()` after generation-heavy phases
5. Use "Increased Memory Limit" entitlement for larger models on iOS
6. Pre-flight memory checks before loading models
7. Validate MLX Swift and llama.cpp on physical Apple Silicon; Simulator cannot
   exercise Metal-dependent inference, memory, or performance

### Model Lifecycle Management

```swift
@Observable
class ModelManager {
    private var model: ModelContainer?
    private var generationCount = 0

    func loadModel() async throws {
        model = try await LLMModelFactory.shared.loadContainer(
            from: HubClient.default,
            using: TokenizersLoader(),
            configuration: .init(id: "mlx-community/Qwen3-4B-4bit")
        )
    }

    func unloadModel() {
        model = nil
        Memory.clearCache()
    }
}
```

Key lifecycle patterns:
- Track active generation count to distinguish "loaded but idle" from
  "generating"
- Unconditional cancellation on app backgrounding
- 5-second delayed force-unload after backgrounding
- Platform-specific memory monitoring (UIKit on iOS, DispatchSource on macOS)

### Background Handling

```swift
// iOS: Observe app lifecycle
NotificationCenter.default.addObserver(
    forName: UIApplication.didEnterBackgroundNotification,
    object: nil, queue: .main
) { _ in
    modelManager.cancelGeneration()
    Task {
        try await Task.sleep(for: .seconds(5))
        modelManager.unloadModel()
    }
}
```

## llama.cpp

C/C++ LLM inference engine. Best cross-platform support. Uses GGUF model format.

### Swift Integration (swift-llama-cpp)

```swift
import SwiftLlamaCpp

let service = LlamaService(
    modelUrl: modelURL,
    config: .init(
        batchSize: 256,
        maxTokenCount: 4096,
        useGPU: true
    )
)

let messages = [
    LlamaChatMessage(role: .system, content: "You are helpful."),
    LlamaChatMessage(role: .user, content: "Hello")
]

let stream = try await service.streamCompletion(
    of: messages,
    samplingConfig: .init(temperature: 0.8)
)
for try await token in stream {
    print(token, terminator: "")
}
```

### GGUF Quantization Levels

| Level | Quality | Size | Use Case |
|---|---|---|---|
| Q2_K | Lowest | Smallest | Extreme memory constraints |
| Q4_K_M | Good | Balanced | Mobile devices (recommended) |
| Q5_K_M | Higher | Larger | When quality matters more |
| Q8_0 | Near-original | Largest | Desktop with ample RAM |

### llama.cpp vs MLX Swift

| Aspect | llama.cpp | MLX Swift |
|---|---|---|
| Model format | GGUF | Hugging Face / MLX format |
| Platform support | Cross-platform | Apple only |
| Throughput (Apple Silicon) | Good | Best |
| Model ecosystem | Broadest | mlx-community models |
| Maturity | Very mature | Evolving |
| Memory efficiency | Excellent | Good |

## Multi-Backend Architecture

When an app needs multiple AI backends:

### Fallback Chain Pattern

```swift
func respond(to prompt: String) async throws -> String {
    // Try Foundation Models first when available (system-integrated backend)
    if SystemLanguageModel.default.isAvailable {
        return try await foundationModelsRespond(prompt)
    }

    // Fall back to MLX Swift (best throughput)
    if canLoadMLXModel() {
        return try await mlxRespond(prompt)
    }

    // Fall back to llama.cpp (broadest compatibility)
    if llamaModelAvailable() {
        return try await llamaRespond(prompt)
    }

    throw AIError.noBackendAvailable
}
```

### Architecture Guidelines

1. Create a router that checks Foundation Models availability first
2. Fall back to MLX or llama.cpp when Foundation Models is unavailable
3. Define model tiers based on device capabilities
4. Serialize all model access through a coordinator actor to prevent contention
5. Ensure tool systems work across backends (schema translation may be needed)

### Coordinator Actor

```swift
actor ModelCoordinator {
    private var activeBackend: Backend?

    func withExclusiveAccess<T>(
        _ work: () async throws -> T
    ) async rethrows -> T {
        try await work()
    }

    enum Backend {
        case foundationModels
        case mlx
        case llamaCpp
    }
}
```

## Built-in Apple Frameworks

Before reaching for custom models, consider built-in frameworks:

### Natural Language Framework

No model downloads required:

- `NLLanguageRecognizer` -- Language detection
- `NLTokenizer` -- Word, sentence, paragraph tokenization
- `NLTagger` -- Parts of speech, named entity recognition, sentiment
- `NLEmbedding` -- Word and sentence vectors, similarity search

### Vision Framework

Built-in computer vision (legacy `VN*` API; for iOS 18+ prefer modern Swift equivalents like `RecognizeTextRequest`):

- `VNRecognizeTextRequest` -- OCR
- `VNClassifyImageRequest` -- Image classification
- `VNDetectFaceRectanglesRequest` -- Face detection
- `VNDetectHumanBodyPoseRequest` -- Body pose estimation

### Create ML

Training custom classifiers directly on device or Mac:

- Image classification
- Text classification
- Tabular data models
- Sound classification

## Performance Best Practices

1. Run outside debugger for accurate benchmarks (Xcode: Cmd-Opt-R, uncheck
   "Debug Executable")
2. Use `session.prewarm()` for Foundation Models before user interaction
3. Batch Vision framework requests in a single `perform()` call
4. Use `.fast` recognition level for real-time camera processing
5. Neural Engine (Core ML) is most energy-efficient for compatible operations
6. For MLX Swift, monitor token generation speed and adjust model size if
   below acceptable thresholds

## Review Checklist

- [ ] Model size appropriate for target device RAM
- [ ] Memory pressure monitoring implemented
- [ ] Models unloaded on app backgrounding
- [ ] MLX cache limits set appropriately
- [ ] Pre-flight memory check before loading large models
- [ ] Fallback strategy when model unavailable
- [ ] All model access serialized through coordinator
- [ ] Quantization level appropriate for quality/size tradeoff
- [ ] Energy efficiency considered (Neural Engine vs GPU)
- [ ] Physical device testing (not simulator) for Metal-dependent code
