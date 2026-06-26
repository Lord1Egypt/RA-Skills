# Core ML Swift Integration Reference

Complete implementation patterns for loading, configuring, and running Core ML
models in Swift. All patterns target iOS 26+ with Swift 6.3, backward-compatible
to iOS 14 unless noted.

## Contents
- Actor-Based Model Loading and Caching
- Auto-Generated Class Usage
- Manual MLFeatureProvider
- Prediction in Async Workflows
- MLBatchProvider for Batch Inference
- Stateful Predictions with MLState (iOS 18+)
- Image Preprocessing
- MLMultiArray Creation and Manipulation
- MLTensor Advanced Operations
- Vision + Core ML Pipelines
- NaturalLanguage Integration
- MLComputePlan Detailed Usage (iOS 17.4+)
- Background Loading and Memory Management
- Error Handling Patterns
- Testing Patterns

## Actor-Based Model Loading and Caching

Use an actor to manage model lifecycle, prevent concurrent loading, and cache
compiled models persistently.

```swift
import CoreML

actor ModelManager {
    private var loadedModels: [String: MLModel] = [:]
    private let cacheDirectory: URL

    init() {
        let appSupport = FileManager.default.urls(
            for: .applicationSupportDirectory, in: .userDomainMask
        ).first!
        cacheDirectory = appSupport.appendingPathComponent("CompiledModels", isDirectory: true)
        try? FileManager.default.createDirectory(at: cacheDirectory, withIntermediateDirectories: true)
    }

    func model(named name: String, configuration: MLModelConfiguration = .init()) async throws -> MLModel {
        if let cached = loadedModels[name] {
            return cached
        }

        let compiledURL = try await compiledModelURL(for: name)
        let model = try await MLModel.load(contentsOf: compiledURL, configuration: configuration)
        loadedModels[name] = model
        return model
    }

    func unloadModel(named name: String) {
        loadedModels.removeValue(forKey: name)
    }

    func unloadAll() {
        loadedModels.removeAll()
    }

    private func compiledModelURL(for name: String) async throws -> URL {
        // Check for pre-compiled model in cache
        let cachedURL = cacheDirectory.appendingPathComponent("\(name).mlmodelc")
        if FileManager.default.fileExists(atPath: cachedURL.path) {
            return cachedURL
        }

        // Check for pre-compiled model in bundle
        if let bundledCompiledURL = Bundle.main.url(forResource: name, withExtension: "mlmodelc") {
            return bundledCompiledURL
        }

        // Compile from .mlpackage and cache
        guard let packageURL = Bundle.main.url(forResource: name, withExtension: "mlpackage") else {
            throw ModelManagerError.modelNotFound(name)
        }
        let tempCompiledURL = try await MLModel.compileModel(at: packageURL)

        // Move compiled model to persistent cache
        if FileManager.default.fileExists(atPath: cachedURL.path) {
            try FileManager.default.removeItem(at: cachedURL)
        }
        try FileManager.default.moveItem(at: tempCompiledURL, to: cachedURL)
        return cachedURL
    }
}

enum ModelManagerError: Error {
    case modelNotFound(String)
    case predictionFailed(String)
}
```

### Usage with SwiftUI

```swift
@MainActor
@Observable
final class ClassifierViewModel {
    var classLabel: String = ""
    var confidence: Double = 0
    var isLoading = false
    var errorMessage: String?

    private let modelManager = ModelManager()

    func classify(image: CGImage) async {
        isLoading = true
        defer { isLoading = false }

        do {
            let config = MLModelConfiguration()
            config.computeUnits = .all

            let model = try await modelManager.model(named: "ImageClassifier", configuration: config)

            let pixelBuffer = try createPixelBuffer(from: image, width: 224, height: 224)
            let input = try MLDictionaryFeatureProvider(dictionary: [
                "image": MLFeatureValue(pixelBuffer: pixelBuffer),
            ])
            let output = try model.prediction(from: input)

            classLabel = output.featureValue(for: "classLabel")?.stringValue ?? "Unknown"
            confidence = output.featureValue(for: "classLabelProbs")?
                .dictionaryValue[classLabel]?
                .doubleValue ?? 0
        } catch {
            errorMessage = "Classification failed: \(error.localizedDescription)"
        }
    }
}
```

## Auto-Generated Class Usage

When you add a `.mlmodel` or `.mlpackage` to your Xcode project, Xcode
generates a Swift class with typed inputs and outputs.

```swift
import CoreML

// Xcode generates: MyImageClassifier, MyImageClassifierInput, MyImageClassifierOutput

// Synchronous prediction with generated types
func classifyWithGeneratedClass(pixelBuffer: CVPixelBuffer) throws -> (label: String, confidence: Double) {
    let config = MLModelConfiguration()
    config.computeUnits = .all

    let classifier = try MyImageClassifier(configuration: config)
    let input = MyImageClassifierInput(image: pixelBuffer)
    let output = try classifier.prediction(input: input)

    let topLabel = output.classLabel
    let topConfidence = output.classLabelProbs[topLabel] ?? 0
    return (topLabel, topConfidence)
}
```

### Accessing the Underlying MLModel

```swift
// Get the underlying MLModel from a generated class
let classifier = try MyImageClassifier(configuration: config)
let mlModel = classifier.model

// Useful for Vision integration
let vnModel = try VNCoreMLModel(for: mlModel)
```

## Manual MLFeatureProvider

Implement `MLFeatureProvider` when you need custom input construction.

```swift
import CoreML

final class CustomImageInput: MLFeatureProvider {
    let image: CVPixelBuffer
    let confidenceThreshold: Double

    var featureNames: Set<String> {
        ["image", "confidence_threshold"]
    }

    func featureValue(for featureName: String) -> MLFeatureValue? {
        switch featureName {
        case "image":
            return MLFeatureValue(pixelBuffer: image)
        case "confidence_threshold":
            return MLFeatureValue(double: confidenceThreshold)
        default:
            return nil
        }
    }

    init(image: CVPixelBuffer, confidenceThreshold: Double = 0.5) {
        self.image = image
        self.confidenceThreshold = confidenceThreshold
    }
}

// Usage
let input = CustomImageInput(image: pixelBuffer, confidenceThreshold: 0.7)
let output = try model.prediction(from: input)
```

## Prediction in Async Workflows

`MLModel.prediction(...)` is synchronous. Use Swift concurrency to keep loading,
preprocessing, and caller coordination off the main actor, then call prediction
without `await`.

### Single Prediction from an Actor

```swift
actor PredictionService {
    private let model: MLModel

    init(model: MLModel) {
        self.model = model
    }

    func predict(input: any MLFeatureProvider) async throws -> any MLFeatureProvider {
        try model.prediction(from: input)
    }
}
```

### Streaming Predictions

```swift
func classifyFrames(_ frames: AsyncStream<CVPixelBuffer>) async throws -> AsyncThrowingStream<String, Error> {
    let model = try await ModelManager().model(named: "Classifier")

    return AsyncThrowingStream { continuation in
        Task {
            do {
                for await frame in frames {
                    let input = try MLDictionaryFeatureProvider(dictionary: [
                        "image": MLFeatureValue(pixelBuffer: frame),
                    ])
                    let output = try model.prediction(from: input)
                    let label = output.featureValue(for: "classLabel")?.stringValue ?? "unknown"
                    continuation.yield(label)
                }
                continuation.finish()
            } catch {
                continuation.finish(throwing: error)
            }
        }
    }
}
```

## MLBatchProvider for Batch Inference

```swift
import CoreML

func batchClassify(images: [CVPixelBuffer], model: MLModel) throws -> [(label: String, confidence: Double)] {
    let batchInputs = try MLArrayBatchProvider(array: images.map { buffer in
        try MLDictionaryFeatureProvider(dictionary: [
            "image": MLFeatureValue(pixelBuffer: buffer),
        ])
    })

    let batchOutput = try model.predictions(fromBatch: batchInputs)

    var results: [(String, Double)] = []
    for i in 0..<batchOutput.count {
        let features = batchOutput.features(at: i)
        let label = features.featureValue(for: "classLabel")?.stringValue ?? "unknown"
        let probs = features.featureValue(for: "classLabelProbs")?.dictionaryValue ?? [:]
        let confidence = (probs[label] as? NSNumber)?.doubleValue ?? 0
        results.append((label, confidence))
    }
    return results
}
```

Batch prediction has two valid API labels:

```swift
// No explicit prediction options
let output = try model.predictions(fromBatch: batchInputs)

// Explicit prediction options
let options = MLPredictionOptions()
let outputWithOptions = try model.predictions(from: batchInputs, options: options)
```

Do not write `predictions(from:)` for the no-options batch path; the `from:`
label belongs to the overload that also takes `options:`.

## Stateful Predictions with MLState (iOS 18+)

`MLState` enables models that maintain internal state across predictions. This is
essential for sequence models (text generation, audio classification, time-series)
where each prediction depends on previous context.

```swift
import CoreML

/// Audio classification that accumulates context over time
actor AudioClassifier {
    private let model: MLModel
    private var state: MLState?

    init(model: MLModel) {
        self.model = model
    }

    /// Start a new classification session
    func beginSession() {
        state = model.makeState()
    }

    /// Classify the next audio frame using accumulated state
    func classify(audioFeatures: MLMultiArray) async throws -> String {
        guard let state else {
            throw ClassifierError.noActiveSession
        }

        let input = try MLDictionaryFeatureProvider(dictionary: [
            "audio_features": MLFeatureValue(multiArray: audioFeatures)
        ])

        let output = try model.prediction(from: input, using: state)
        return output.featureValue(for: "label")?.stringValue ?? "unknown"
    }

    /// End the session and release state
    func endSession() {
        state = nil
    }
}

enum ClassifierError: Error {
    case noActiveSession
}
```

### Key Rules for MLState

- **Serialized use:** `MLState` is `Sendable`, but predictions that use the same
  state must be serialized. `Sendable` permits transfer across concurrency
  domains; it does not permit concurrent predictions on one state. Do not read or
  write state buffers while a prediction is in flight.
- **Async options overload:** Use the synchronous `prediction(from:using:)`
  overload for simple serialized loops. If you need `MLPredictionOptions`, iOS
  18+ also provides async `prediction(from:using:options:)`; keep one in-flight
  prediction per state.
- **Independent streams:** Call `model.makeState()` per stream when processing
  multiple concurrent sequences (e.g., multiple audio channels).
- **Resettable:** Create a new state to reset accumulated context. There is no
  explicit reset method -- just discard the old state and create fresh.
- **Memory:** State holds model-specific internal buffers. Release it when the
  session ends to free memory.

## Image Preprocessing

### CVPixelBuffer from CGImage

```swift
import CoreVideo
import CoreGraphics

func createPixelBuffer(from cgImage: CGImage, width: Int, height: Int) throws -> CVPixelBuffer {
    let attrs: [CFString: Any] = [
        kCVPixelBufferCGImageCompatibilityKey: true,
        kCVPixelBufferCGBitmapContextCompatibilityKey: true,
    ]

    var pixelBuffer: CVPixelBuffer?
    let status = CVPixelBufferCreate(
        kCFAllocatorDefault,
        width, height,
        kCVPixelFormatType_32ARGB,
        attrs as CFDictionary,
        &pixelBuffer
    )
    guard status == kCVReturnSuccess, let buffer = pixelBuffer else {
        throw ImageError.pixelBufferCreationFailed
    }

    CVPixelBufferLockBaseAddress(buffer, [])
    defer { CVPixelBufferUnlockBaseAddress(buffer, []) }

    guard let context = CGContext(
        data: CVPixelBufferGetBaseAddress(buffer),
        width: width,
        height: height,
        bitsPerComponent: 8,
        bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
        space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
    ) else {
        throw ImageError.contextCreationFailed
    }

    context.draw(cgImage, in: CGRect(x: 0, y: 0, width: width, height: height))
    return buffer
}

enum ImageError: Error {
    case pixelBufferCreationFailed
    case contextCreationFailed
}
```

For `CIImage` sources, use `CIContext.render(_:to:)` into a `CVPixelBuffer`
created with `kCVPixelFormatType_32BGRA`.

## MLMultiArray Creation and Manipulation

```swift
import CoreML

let array = try MLMultiArray(shape: [1, 3, 224, 224], dataType: .float32)
for i in 0..<array.count { array[i] = NSNumber(value: Float.random(in: 0...1)) }

let values: [Float] = [1.0, 2.0, 3.0, 4.0, 5.0]
let mlArray = try MLMultiArray(values)

// Access elements
let element = array[[0, 0, 112, 112] as [NSNumber]].floatValue

// Convert to Swift array
func toFloatArray(_ multiArray: MLMultiArray) -> [Float] {
    let pointer = multiArray.dataPointer.assumingMemoryBound(to: Float.self)
    return Array(UnsafeBufferPointer(start: pointer, count: multiArray.count))
}

let featureValue = MLFeatureValue(multiArray: array)
```

## MLTensor Advanced Operations (iOS 18+)

```swift
import CoreML

// Creation patterns
let tensor1D = MLTensor([1.0, 2.0, 3.0, 4.0])
let zeros = MLTensor(zeros: [3, 224, 224], scalarType: Float.self)
let ones = MLTensor(ones: [2, 2], scalarType: Float.self)

// Reshaping
let reshaped = tensor1D.reshaped(to: [2, 2])
let expanded = tensor1D.expandingShape(at: 0)   // [1, 4]

// Arithmetic and reduction
let sum = tensor1D + ones.reshaped(to: [4])
let mean = tensor1D.mean()
let argmax = tensor1D.argmax()

// Activation functions
let softmaxed = tensor1D.softmax(alongAxis: -1)

// Interop with MLShapedArray / MLMultiArray
let shaped = await tensor1D.shapedArray(of: Float.self) // MLShapedArray<Float>
let multiArray = try MLMultiArray(shaped)
let shapedAgain = MLShapedArray<Float>(multiArray)

// Concatenation
let a = MLTensor([1.0, 2.0])
let b = MLTensor([3.0, 4.0])
let concatenated = MLTensor(concatenating: [a, b], alongAxis: 0)

// Normalization pattern (e.g., ImageNet preprocessing)
func normalize(_ tensor: MLTensor, mean: [Float], std: [Float]) -> MLTensor {
    let meanTensor = MLTensor(mean)
    let stdTensor = MLTensor(std)
    return (tensor - meanTensor) / stdTensor
}
```

## Vision + Core ML Pipelines

### Modern API (iOS 18+)

```swift
import Vision
import CoreML

@MainActor
@Observable
final class ObjectDetectionViewModel {
    var detections: [Detection] = []
    var isProcessing = false

    struct Detection: Identifiable {
        let id = UUID()
        let label: String
        let confidence: Float
        let boundingBox: CGRect
    }

    func detect(in image: CGImage) async {
        isProcessing = true
        defer { isProcessing = false }

        do {
            let config = MLModelConfiguration()
            config.computeUnits = .all

            let detector = try MyObjectDetector(configuration: config)
            let request = CoreMLRequest(model: .init(detector.model))

            let results = try await request.perform(on: image)
            detections = results.compactMap { observation in
                guard let object = observation as? RecognizedObjectObservation,
                      let topLabel = object.labels.first else { return nil }
                return Detection(
                    label: topLabel.identifier,
                    confidence: topLabel.confidence,
                    boundingBox: object.boundingBox
                )
            }
        } catch {
            detections = []
        }
    }
}
```

```swift
func classifyImage(_ image: CGImage) async throws -> [(label: String, confidence: Float)] {
    let classifier = try MyImageClassifier(configuration: .init())
    let request = CoreMLRequest(model: .init(classifier.model))

    let results = try await request.perform(on: image)
    return results.compactMap { observation in
        guard let classification = observation as? ClassificationObservation else { return nil }
        return (classification.identifier, classification.confidence)
    }
}
```

### Legacy API (Pre-iOS 18)

```swift
import Vision
import CoreML

func detectLegacy(in image: CGImage) async throws -> [VNRecognizedObjectObservation] {
    let config = MLModelConfiguration()
    config.computeUnits = .all

    let detector = try MyObjectDetector(configuration: config)
    let vnModel = try VNCoreMLModel(for: detector.model)

    let request = VNCoreMLRequest(model: vnModel)
    request.imageCropAndScaleOption = .scaleFill

    let handler = VNImageRequestHandler(cgImage: image)
    return try await Task.detached {
        try handler.perform([request])
        return request.results as? [VNRecognizedObjectObservation] ?? []
    }.value
}
```

```swift
func classifyImageLegacy(_ image: CGImage) async throws -> [(label: String, confidence: Float)] {
    let classifier = try MyImageClassifier(configuration: .init())
    let vnModel = try VNCoreMLModel(for: classifier.model)
    let request = VNCoreMLRequest(model: vnModel)
    request.imageCropAndScaleOption = .centerCrop

    let handler = VNImageRequestHandler(cgImage: image)
    return try await Task.detached {
        try handler.perform([request])
        guard let results = request.results as? [VNClassificationObservation] else { return [] }
        return results.prefix(5).map { ($0.identifier, $0.confidence) }
    }.value
}
```

## NaturalLanguage Integration

Use `NLModel` to load Core ML models trained for NLP tasks.

```swift
import NaturalLanguage

func analyzeSentiment(text: String) throws -> (label: String, confidence: Double)? {
    let modelURL = Bundle.main.url(forResource: "SentimentClassifier", withExtension: "mlmodelc")!
    let nlModel = try NLModel(contentsOf: modelURL)

    guard let label = nlModel.predictedLabel(for: text) else { return nil }
    let hypotheses = nlModel.predictedLabelHypotheses(for: text, maximumCount: 1)
    let confidence = hypotheses[label] ?? 0
    return (label, confidence)
}
```

## MLComputePlan Detailed Usage (iOS 17.4+)

```swift
import CoreML

func profileModel(at url: URL) async throws {
    let config = MLModelConfiguration()
    config.computeUnits = .all
    let computePlan = try await MLComputePlan.load(contentsOf: url, configuration: config)

    guard case let .program(program) = computePlan.modelStructure,
          let mainFunction = program.functions["main"] else {
        print("Model is not an ML program or has no main function")
        return
    }

    for operation in mainFunction.block.operations {
        let opName = operation.operatorName
        if let deviceUsage = computePlan.deviceUsage(for: operation) {
            print("  \(opName): \(deviceUsage.preferred)")
        }
        if let cost = computePlan.estimatedCost(of: operation) {
            print("    Estimated weight: \(cost.weight)")
        }
    }
}
```

### Interpreting MLComputePlan Results

| Device | Meaning | Action |
|---|---|---|
| Neural Engine | Best efficiency and speed for supported ops | Ideal -- no changes needed |
| GPU | Runs on Metal GPU | Good for large matrix ops |
| CPU | Fallback for unsupported operations | Investigate if many ops fall here |

If many critical operations fall back to CPU, try `.cpuAndGPU` compute units,
check for unsupported ANE operations, or re-convert with a different deployment target.

## Background Model Loading and App Lifecycle

Manage model loading and memory across app lifecycle transitions.

```swift
@MainActor
@Observable
final class AppModelState {
    var isModelReady = false
    private let modelManager = ModelManager()

    func warmup() async {
        do {
            let config = MLModelConfiguration()
            config.computeUnits = .all
            _ = try await modelManager.model(named: "MainClassifier", configuration: config)
            isModelReady = true
        } catch {
            isModelReady = false
        }
    }

    func handleBackground() async {
        await modelManager.unloadAll()
        isModelReady = false
    }
}

// SwiftUI integration
@main
struct MyApp: App {
    @State private var modelState = AppModelState()
    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(modelState)
                .task { await modelState.warmup() }
                .onChange(of: scenePhase) { _, newPhase in
                    Task {
                        if newPhase == .background {
                            await modelState.handleBackground()
                        } else if newPhase == .active {
                            await modelState.warmup()
                        }
                    }
                }
        }
    }
}
```

## Error Handling

```swift
import CoreML

func loadAndPredict(modelName: String, input: any MLFeatureProvider) async -> (any MLFeatureProvider)? {
    let config = MLModelConfiguration()
    config.computeUnits = .all

    do {
        guard let url = Bundle.main.url(forResource: modelName, withExtension: "mlmodelc") else {
            print("Model \(modelName) not found in bundle")
            return nil
        }
        let model = try await MLModel.load(contentsOf: url, configuration: config)
        return try model.prediction(from: input)
    } catch {
        print("Model error: \(error)")
        return nil
    }
}
```

### Common Error Types

| Error | Cause | Fix |
|---|---|---|
| `MLModel` file not found | Wrong bundle path or missing target membership | Verify file is in correct target |
| Compilation failure | Corrupted `.mlpackage` or unsupported ops | Re-export from coremltools |
| Input shape mismatch | Wrong image dimensions or tensor shape | Match model's expected input shape |
| Out of memory | Model too large for device | Use smaller model or `.cpuOnly` compute |
| Compute unit fallback | Ops unsupported on requested device | Use `.all` or check `MLComputePlan` |

For MLTensor preprocessing, keep examples to source-confirmed operations. Do not
use `MLTensor(multiArray)`, `tensor.std()`, `tensor.standardDeviation()`, direct
lazy-buffer access, or synchronous extraction unless Apple documents that exact
API and availability.

## Testing Patterns

```swift
import Testing
import CoreML

struct ModelLoadingTests {
    @Test func loadModelSucceeds() async throws {
        let config = MLModelConfiguration()
        config.computeUnits = .cpuOnly // CPU for test stability
        let model = try MyImageClassifier(configuration: config)
        #expect(model.model.modelDescription.inputDescriptionsByName.count > 0)
    }

    @Test func predictionReturnsValidOutput() async throws {
        let config = MLModelConfiguration()
        config.computeUnits = .cpuOnly

        let model = try MyImageClassifier(configuration: config)
        let input = try createTestInput(width: 224, height: 224)
        let output = try model.prediction(input: input)

        #expect(!output.classLabel.isEmpty)
        #expect(output.classLabelProbs.values.allSatisfy { $0 >= 0 && $0 <= 1 })
    }

    @Test func predictionLatencyUnderThreshold() async throws {
        let config = MLModelConfiguration()
        config.computeUnits = .all

        let model = try MyImageClassifier(configuration: config)
        let input = try createTestInput(width: 224, height: 224)

        _ = try model.prediction(input: input) // Warm up

        let start = ContinuousClock.now
        for _ in 0..<10 {
            _ = try model.prediction(input: input)
        }
        let avgMs = (ContinuousClock.now - start) / 10

        #expect(avgMs < .milliseconds(50), "Average prediction time \(avgMs) exceeds 50ms")
    }
}

private func createTestPixelBuffer(width: Int, height: Int) throws -> CVPixelBuffer {
    var pixelBuffer: CVPixelBuffer?
    let status = CVPixelBufferCreate(
        kCFAllocatorDefault, width, height,
        kCVPixelFormatType_32ARGB, nil, &pixelBuffer
    )
    guard status == kCVReturnSuccess, let buffer = pixelBuffer else {
        throw ImageError.pixelBufferCreationFailed
    }
    return buffer
}
```

## Memory Management Best Practices

1. **Unload on background.** Unload models when `scenePhase == .background`
   and reload on return to foreground. iOS reclaims memory aggressively.
2. **Choose compute units by context.** Use `.all` by default. Consider
   `.cpuOnly` only when profiling or app policy shows accelerator contention,
   thermal state, energy budget, deterministic testing, or a legitimate
   background execution constraint makes CPU the right tradeoff.
   Do not claim GPU or Neural Engine are categorically unavailable for every
   background-adjacent task; background behavior depends on app mode, suspension,
   system policy, thermal state, energy, and contention.
3. **Prefer compiled models.** `.mlmodelc` loads faster and uses less transient
   memory than compiling `.mlpackage` at runtime. If a model is downloaded as
   `.mlmodel` or `.mlpackage`, compile once with `MLModel.compileModel(at:)`,
   move the `.mlmodelc` out of Core ML's temporary location, and cache it by
   model version. Do not call `compileModel(at:)` on every launch for the same
   model.
4. **Validate on physical devices.** Measure model load, first prediction,
   repeated predictions, background/foreground transitions, and low-memory
   behavior on the lowest-memory supported device.
5. **Share model instances.** Use an actor (like `ModelManager` above) to
   ensure only one instance of each model exists.
6. **Release batch providers promptly.** Large `MLArrayBatchProvider` instances
   hold references to all input data.
