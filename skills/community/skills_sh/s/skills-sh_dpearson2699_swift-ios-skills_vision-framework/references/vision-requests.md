# Vision Request Patterns

Complete implementation patterns for Vision framework requests covering text
recognition, face detection, barcode scanning, segmentation, classification,
and video processing. All patterns target iOS 26+ with Swift 6.3 unless noted.

## Contents
- Complete Text Recognition Pipeline
- Face Detection with Landmarks
- Barcode Detection with All Symbologies
- Person Segmentation with Mask Application
- Instance Segmentation (iOS 18+)
- Image Classification
- Saliency Detection
- Rectangle Detection
- Horizon Detection
- Batch Processing Multiple Requests
- Video Frame Processing with CMSampleBuffer
- Object Tracking Across Video Frames
- Coordinate Normalization Utilities
- Performance Considerations

## Complete Text Recognition Pipeline

Full pipeline from image loading through text extraction with coordinate mapping.

```swift
import Vision
import UIKit

@MainActor
final class TextRecognizer {
    func recognizeText(in image: UIImage) async throws -> [RecognizedTextBlock] {
        guard let cgImage = image.cgImage else {
            throw TextRecognitionError.invalidImage
        }

        var request = RecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.recognitionLanguages = [
            Locale.Language(identifier: "en-US"),
        ]
        request.usesLanguageCorrection = true

        let observations = try await request.perform(on: cgImage)
        let imageSize = CGSize(
            width: cgImage.width,
            height: cgImage.height
        )

        return observations.compactMap { observation in
            guard let candidate = observation.topCandidates(1).first else { return nil }
            let imageRect = observation.boundingBox.toImageCoordinates(
                imageSize,
                origin: .upperLeft
            )
            return RecognizedTextBlock(
                text: candidate.string,
                confidence: candidate.confidence,
                boundingBox: imageRect
            )
        }
    }
}

struct RecognizedTextBlock: Sendable {
    let text: String
    let confidence: Float
    let boundingBox: CGRect
}

enum TextRecognitionError: Error {
    case invalidImage
}
```

### Text Recognition with Language Hints

```swift
func recognizeMultilingualText(in cgImage: CGImage) async throws -> [String] {
    var request = RecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = [
        Locale.Language(identifier: "en-US"),
        Locale.Language(identifier: "fr-FR"),
        Locale.Language(identifier: "de-DE"),
    ]
    request.usesLanguageCorrection = true
    request.customWords = ["iOS", "SwiftUI", "Xcode"]

    let observations = try await request.perform(on: cgImage)
    return observations.compactMap { $0.topCandidates(1).first?.string }
}
```

### Fast Text Recognition for Live Video

```swift
func recognizeTextFast(in sampleBuffer: CMSampleBuffer) async throws -> [String] {
    var request = RecognizeTextRequest()
    request.recognitionLevel = .fast
    request.recognitionLanguages = [Locale.Language(identifier: "en-US")]

    let observations = try await request.perform(on: sampleBuffer)
    return observations.compactMap { $0.topCandidates(1).first?.string }
}
```

### Legacy Text Recognition (Pre-iOS 18)

```swift
import Vision

func recognizeTextLegacy(
    in cgImage: CGImage,
    completion: @escaping ([String]) -> Void
) {
    let request = VNRecognizeTextRequest { request, error in
        guard error == nil,
              let observations = request.results as? [VNRecognizedTextObservation]
        else {
            completion([])
            return
        }
        let strings = observations.compactMap {
            $0.topCandidates(1).first?.string
        }
        completion(strings)
    }
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["en-US"]
    request.usesLanguageCorrection = true

    let handler = VNImageRequestHandler(cgImage: cgImage)
    DispatchQueue.global(qos: .userInitiated).async {
        try? handler.perform([request])
    }
}
```

## Face Detection with Landmarks

```swift
import Vision

struct DetectedFace: Sendable {
    let boundingBox: NormalizedRect
    let landmarks: FaceLandmarkPoints?
    let roll: Measurement<UnitAngle>
    let yaw: Measurement<UnitAngle>
    let captureQuality: FaceObservation.CaptureQuality?
}

struct FaceLandmarkPoints: Sendable {
    let leftEye: [NormalizedPoint]
    let rightEye: [NormalizedPoint]
    let nose: [NormalizedPoint]
    let outerLips: [NormalizedPoint]
    let faceContour: [NormalizedPoint]
}

func detectFaces(in cgImage: CGImage) async throws -> [DetectedFace] {
    // Detect face rectangles
    let rectRequest = DetectFaceRectanglesRequest()
    let faces = try await rectRequest.perform(on: cgImage)

    // Detect landmarks for detailed features
    let landmarkRequest = DetectFaceLandmarksRequest()
    let landmarkFaces = try await landmarkRequest.perform(on: cgImage)

    // Detect capture quality for photo selection
    let qualityRequest = DetectFaceCaptureQualityRequest()
    let qualityFaces = try await qualityRequest.perform(on: cgImage)

    return faces.enumerated().map { index, face in
        let landmarks: FaceLandmarkPoints?
        if index < landmarkFaces.count,
           let lm = landmarkFaces[index].landmarks {
            landmarks = FaceLandmarkPoints(
                leftEye: lm.leftEye.points,
                rightEye: lm.rightEye.points,
                nose: lm.nose.points,
                outerLips: lm.outerLips.points,
                faceContour: lm.faceContour.points
            )
        } else {
            landmarks = nil
        }

        let quality: FaceObservation.CaptureQuality?
        if index < qualityFaces.count {
            quality = qualityFaces[index].captureQuality
        } else {
            quality = nil
        }

        return DetectedFace(
            boundingBox: face.boundingBox,
            landmarks: landmarks,
            roll: face.roll,
            yaw: face.yaw,
            captureQuality: quality
        )
    }
}
```

## Barcode Detection with All Symbologies

```swift
import Vision

struct DetectedBarcode: Sendable {
    let payload: String?
    let symbology: BarcodeSymbology
    let boundingBox: NormalizedRect
}

func detectBarcodes(
    in cgImage: CGImage,
    symbologies: [BarcodeSymbology] = [.qr, .ean13, .code128]
) async throws -> [DetectedBarcode] {
    var request = DetectBarcodesRequest()
    request.symbologies = symbologies

    let observations = try await request.perform(on: cgImage)
    return observations.map { barcode in
        DetectedBarcode(
            payload: barcode.payloadString,
            symbology: barcode.symbology,
            boundingBox: barcode.boundingBox
        )
    }
}

// Detect only QR codes with URL content
func detectQRCodes(in cgImage: CGImage) async throws -> [URL] {
    var request = DetectBarcodesRequest()
    request.symbologies = [.qr]

    let observations = try await request.perform(on: cgImage)
    return observations.compactMap { barcode in
        guard let payload = barcode.payloadString else { return nil }
        return URL(string: payload)
    }
}
```

### Supported Symbologies Reference

```swift
// 1D barcodes
let linearSymbologies: [BarcodeSymbology] = [
    .codabar, .code39, .code39Checksum, .code39FullASCII,
    .code39FullASCIIChecksum, .code93, .code93i, .code128,
    .ean8, .ean13, .gs1DataBar, .gs1DataBarExpanded,
    .gs1DataBarLimited, .i2of5, .i2of5Checksum, .itf14,
    .msiPlessey, .upce,
]

// 2D barcodes
let matrixSymbologies: [BarcodeSymbology] = [
    .qr, .aztec, .dataMatrix, .pdf417, .microPDF417, .microQR,
]
```

## Person Segmentation with Mask Application

### Modern API (iOS 18+)

```swift
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins

func segmentPerson(in cgImage: CGImage) async throws -> CIImage {
    var request = GeneratePersonSegmentationRequest()
    request.qualityLevel = .accurate  // .balanced, .fast

    let observation = try await request.perform(on: cgImage)
    let maskBuffer = observation.pixelBuffer

    let originalImage = CIImage(cgImage: cgImage)
    let maskImage = CIImage(cvPixelBuffer: maskBuffer)

    // Scale mask to match original image size
    let scaleX = originalImage.extent.width / maskImage.extent.width
    let scaleY = originalImage.extent.height / maskImage.extent.height
    let scaledMask = maskImage.transformed(by: CGAffineTransform(
        scaleX: scaleX, y: scaleY
    ))

    return scaledMask
}

// Apply background blur using person mask
func blurBackground(of cgImage: CGImage, blurRadius: Double = 20.0) async throws -> CIImage {
    let mask = try await segmentPerson(in: cgImage)
    let original = CIImage(cgImage: cgImage)

    let blurFilter = CIFilter.gaussianBlur()
    blurFilter.inputImage = original
    blurFilter.radius = Float(blurRadius)
    guard let blurredImage = blurFilter.outputImage else {
        throw SegmentationError.noMask
    }

    let blendFilter = CIFilter.blendWithMask()
    blendFilter.inputImage = original         // foreground (person)
    blendFilter.backgroundImage = blurredImage // blurred background
    blendFilter.maskImage = mask

    guard let result = blendFilter.outputImage else {
        throw SegmentationError.noMask
    }
    return result
}

enum SegmentationError: Error {
    case noMask
}
```

### Legacy API (Pre-iOS 18)

```swift
func segmentPersonLegacy(in cgImage: CGImage) throws -> CVPixelBuffer {
    let request = VNGeneratePersonSegmentationRequest()
    request.qualityLevel = .accurate
    request.outputPixelFormat = kCVPixelFormatType_OneComponent8

    let handler = VNImageRequestHandler(cgImage: cgImage)
    try handler.perform([request])

    guard let maskBuffer = request.results?.first?.pixelBuffer else {
        throw SegmentationError.noMask
    }
    return maskBuffer
}
```

### Instance Segmentation (iOS 18+)

Separate masks per person for individual effects.

```swift
// Modern API (iOS 18+)
func segmentIndividualPeople(in cgImage: CGImage) async throws -> [CVPixelBuffer] {
    let request = GeneratePersonInstanceMaskRequest()
    let observation = try await request.perform(on: cgImage)

    let indices = observation.allInstances
    return try indices.map { index in
        try observation.generateMask(for: IndexSet(integer: index))
    }
}
```

```swift
// Legacy API (iOS 17+)
func segmentIndividualPeopleLegacy(in cgImage: CGImage) throws -> [CVPixelBuffer] {
    let request = VNGeneratePersonInstanceMaskRequest()
    let handler = VNImageRequestHandler(cgImage: cgImage)
    try handler.perform([request])

    guard let result = request.results?.first else { return [] }
    let indices = result.allInstances

    return try indices.map { index in
        try result.generateMask(forInstances: IndexSet(integer: index))
    }
}
```

## Image Classification

```swift
import Vision

func classifyImage(_ cgImage: CGImage, maxResults: Int = 5) async throws -> [(String, Float)] {
    let request = ClassifyImageRequest()
    let observations = try await request.perform(on: cgImage)

    return observations.prefix(maxResults).map { observation in
        (observation.identifier, observation.confidence)
    }
}
```

## Saliency Detection

Identify the most visually important or attention-grabbing regions.

```swift
// Attention-based saliency (what humans would look at)
func detectAttentionSaliency(in cgImage: CGImage) async throws -> [NormalizedRect] {
    let request = GenerateAttentionBasedSaliencyImageRequest()
    let saliency: SaliencyImageObservation = try await request.perform(on: cgImage)
    return saliency.salientObjects?.map(\.boundingBox) ?? []
}

// Objectness-based saliency (distinct objects)
func detectObjectSaliency(in cgImage: CGImage) async throws -> [NormalizedRect] {
    let request = GenerateObjectnessBasedSaliencyImageRequest()
    let saliency: SaliencyImageObservation = try await request.perform(on: cgImage)
    return saliency.salientObjects?.map(\.boundingBox) ?? []
}
```

## Rectangle Detection

Detect rectangular shapes for document edges, business cards, etc.

```swift
func detectRectangles(in cgImage: CGImage) async throws -> [NormalizedRect] {
    var request = DetectRectanglesRequest()
    request.minimumAspectRatio = 0.3
    request.maximumAspectRatio = 1.0
    request.minimumSize = 0.1
    request.maximumObservations = 5

    let observations = try await request.perform(on: cgImage)
    return observations.map(\.boundingBox)
}
```

## Horizon Detection

Detect the horizon angle for auto-straightening photos.

```swift
func detectHorizon(in cgImage: CGImage) async throws -> Measurement<UnitAngle> {
    let request = DetectHorizonRequest()
    let observation = try await request.perform(on: cgImage)
    return observation.angle
}
```

## Batch Processing Multiple Requests

Run multiple requests on the same image simultaneously for efficiency.

```swift
func analyzeImage(_ cgImage: CGImage) async throws -> ImageAnalysisResult {
    async let textResults = {
        var req = RecognizeTextRequest()
        req.recognitionLevel = .accurate
        return try await req.perform(on: cgImage)
    }()

    async let faceResults = {
        let req = DetectFaceRectanglesRequest()
        return try await req.perform(on: cgImage)
    }()

    async let barcodeResults = {
        var req = DetectBarcodesRequest()
        req.symbologies = [.qr, .ean13]
        return try await req.perform(on: cgImage)
    }()

    let text = try await textResults
    let faces = try await faceResults
    let barcodes = try await barcodeResults

    return ImageAnalysisResult(
        recognizedText: text.compactMap { $0.topCandidates(1).first?.string },
        faceCount: faces.count,
        barcodePayloads: barcodes.compactMap(\.payloadString)
    )
}

struct ImageAnalysisResult: Sendable {
    let recognizedText: [String]
    let faceCount: Int
    let barcodePayloads: [String]
}
```

### Legacy Batch Processing

With the legacy API, pass multiple requests to a single handler call.

```swift
func analyzeImageLegacy(_ cgImage: CGImage) throws {
    let textRequest = VNRecognizeTextRequest { request, error in
        // Handle text results
    }
    let faceRequest = VNDetectFaceRectanglesRequest { request, error in
        // Handle face results
    }
    let barcodeRequest = VNDetectBarcodesRequest { request, error in
        // Handle barcode results
    }

    let handler = VNImageRequestHandler(cgImage: cgImage)
    try handler.perform([textRequest, faceRequest, barcodeRequest])
}
```

## Video Frame Processing with CMSampleBuffer

Process live camera frames from AVCaptureSession.

```swift
import AVFoundation
import Vision

final class VisionVideoProcessor: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate, Sendable {
    private let processingQueue = DispatchQueue(label: "vision.processing", qos: .userInitiated)

    func setupCapture(session: AVCaptureSession) {
        let output = AVCaptureVideoDataOutput()
        output.setSampleBufferDelegate(self, queue: processingQueue)
        output.alwaysDiscardsLateVideoFrames = true

        if session.canAddOutput(output) {
            session.addOutput(output)
        }
    }

    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection
    ) {
        Task {
            do {
                var request = RecognizeTextRequest()
                request.recognitionLevel = .fast
                let observations = try await request.perform(on: sampleBuffer)
                let strings = observations.compactMap {
                    $0.topCandidates(1).first?.string
                }
                // Dispatch results to main actor for UI update
                await MainActor.run {
                    // Update UI with recognized strings
                }
            } catch {
                // Handle error
            }
        }
    }
}
```

### Object Tracking Across Video Frames

#### Modern API (iOS 18+)

`TrackObjectRequest` is a stateful request that maintains tracking context
internally. No need for a separate sequence handler.

```swift
import Vision

final class ObjectTracker {
    private var request: TrackObjectRequest?

    /// Initialize tracking with a bounding box in normalized coordinates
    func startTracking(boundingBox: NormalizedRect) {
        let observation = DetectedObjectObservation(boundingBox: boundingBox)
        request = TrackObjectRequest(detectedObject: observation)
    }

    /// Track object in next video frame
    func track(in pixelBuffer: CVPixelBuffer) async throws -> NormalizedRect? {
        guard let request else { return nil }

        let results = try await request.perform(on: pixelBuffer)
        guard let tracked = results.first else {
            request = nil
            return nil
        }

        return tracked.boundingBox
    }

    func stopTracking() {
        request = nil
    }
}
```

#### Legacy API

```swift
final class LegacyObjectTracker {
    private var sequenceHandler = VNSequenceRequestHandler()
    private var currentObservation: VNDetectedObjectObservation?

    func startTracking(boundingBox: CGRect) {
        currentObservation = VNDetectedObjectObservation(boundingBox: boundingBox)
    }

    func track(in pixelBuffer: CVPixelBuffer) throws -> CGRect? {
        guard let observation = currentObservation else { return nil }

        let trackRequest = VNTrackObjectRequest(detectedObjectObservation: observation)
        trackRequest.trackingLevel = .accurate

        try sequenceHandler.perform([trackRequest], on: pixelBuffer)

        guard let result = trackRequest.results?.first as? VNDetectedObjectObservation,
              result.confidence > 0.3 else {
            currentObservation = nil
            return nil
        }

        currentObservation = result
        return result.boundingBox
    }

    func stopTracking() {
        currentObservation = nil
    }
}
```

## Coordinate Normalization Utilities

Vision uses normalized coordinates (0...1) with bottom-left origin. These
utilities convert to UIKit/SwiftUI coordinate systems.

```swift
import Vision
import UIKit

enum VisionCoordinateConverter {
    /// Convert modern Vision NormalizedRect to image-pixel coordinates
    static func toImageCoordinates(
        _ normalizedRect: NormalizedRect,
        imageSize: CGSize
    ) -> CGRect {
        normalizedRect.toImageCoordinates(imageSize, origin: .upperLeft)
    }

    /// Convert legacy normalized Vision rect to image-pixel coordinates
    static func toImageCoordinates(
        _ normalizedRect: CGRect,
        imageWidth: Int,
        imageHeight: Int
    ) -> CGRect {
        VNImageRectForNormalizedRect(normalizedRect, imageWidth, imageHeight)
    }

    /// Convert legacy normalized Vision point to image-pixel coordinates
    static func toImageCoordinates(
        _ normalizedPoint: CGPoint,
        imageWidth: Int,
        imageHeight: Int
    ) -> CGPoint {
        VNImagePointForNormalizedPoint(normalizedPoint, imageWidth, imageHeight)
    }

    /// Convert modern Vision rect directly to UIKit/image coordinates
    static func toUIKitCoordinates(
        _ normalizedRect: NormalizedRect,
        viewSize: CGSize
    ) -> CGRect {
        normalizedRect.toImageCoordinates(viewSize, origin: .upperLeft)
    }

    /// Convert an array of modern normalized points to UIKit points
    static func toUIKitPoints(
        _ normalizedPoints: [NormalizedPoint],
        viewSize: CGSize
    ) -> [CGPoint] {
        normalizedPoints.map {
            $0.toImageCoordinates(viewSize, origin: .upperLeft)
        }
    }

    /// Convert an array of legacy normalized points to UIKit points
    static func toUIKitPoints(
        _ normalizedPoints: [CGPoint],
        viewSize: CGSize
    ) -> [CGPoint] {
        normalizedPoints.map { point in
            CGPoint(
                x: point.x * viewSize.width,
                y: (1.0 - point.y) * viewSize.height  // flip Y
            )
        }
    }
}
```

## Performance Considerations

### Recognition Level Selection

| Use Case | Level | Typical Latency |
|---|---|---|
| Live camera preview | `.fast` | ~30ms per frame |
| Photo library scan | `.accurate` | ~200-500ms per image |
| Batch document OCR | `.accurate` | ~200-500ms per page |
| Barcode scanner | `.fast` or `.balanced` | ~15-50ms per frame |

### Memory Management

- Reuse `VNSequenceRequestHandler` across video frames (do not recreate per frame)
- For batch processing, process one image at a time to avoid memory spikes
- Release `CVPixelBuffer` references promptly after processing
- Use `autoreleasepool` in tight loops processing many images

```swift
func batchProcess(images: [CGImage]) async throws -> [[String]] {
    var allResults: [[String]] = []

    for image in images {
        var request = RecognizeTextRequest()
        request.recognitionLevel = .accurate
        let obs = try await request.perform(on: image)
        let result = obs.compactMap { $0.topCandidates(1).first?.string }
        allResults.append(result)
    }
    return allResults
}
```

### Threading

- Modern API (`perform(on:)`) is async and safe to call from any context
- Legacy API: create `VNImageRequestHandler` and call `perform` on a background queue
- Never block the main thread with Vision requests
- `VNSequenceRequestHandler` is not thread-safe -- use from a single serial queue

### Request Reuse

Most modern stateless request structs are cheap to create. Use a fresh request
for independent still-image work, and keep stateful final-class requests such as
`TrackObjectRequest` only for the frame sequence that needs their state.

For the legacy API, `VNImageRequestHandler` is tied to a single image. Create a
new handler for each image you process. `VNSequenceRequestHandler` can be reused
across frames in a sequence.
