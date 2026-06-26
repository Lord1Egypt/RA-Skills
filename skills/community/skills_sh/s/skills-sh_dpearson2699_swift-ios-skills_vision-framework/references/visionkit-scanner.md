# VisionKit Scanner Patterns

Complete implementation patterns for DataScannerViewController and
VNDocumentCameraViewController covering availability checking, configuration,
SwiftUI integration, delegate handling, custom overlays, and camera permissions.
All patterns target iOS 26+ with Swift 6.3 unless noted.

## Contents
- Camera Permission Setup
- DataScannerViewController
- Delegate Methods
- SwiftUI Integration
- Custom Overlay UI
- VNDocumentCameraViewController

## Camera Permission Setup

Add the camera usage description to Info.plist before using any scanner:

```xml
<key>NSCameraUsageDescription</key>
<string>Camera access is needed to scan text and barcodes.</string>
```

Request permission before presenting the scanner. The canonical order is:
Info.plist usage string, explicit camera access request, `isSupported` and
`isAvailable` checks, then present the scanner and call `startScanning()` after
presentation on the main actor.

```swift
import AVFoundation

func requestCameraAccess() async -> Bool {
    let status = AVCaptureDevice.authorizationStatus(for: .video)
    switch status {
    case .authorized:
        return true
    case .notDetermined:
        return await AVCaptureDevice.requestAccess(for: .video)
    case .denied, .restricted:
        return false
    @unknown default:
        return false
    }
}
```

## DataScannerViewController

`DataScannerViewController` provides a full-screen live camera scanner for text
and barcodes with built-in highlighting and interaction. Available on devices
with an A12 Bionic chip or later (iOS 16+), but unsupported for apps running in
visionOS.

### Availability Checking

Always check both hardware support and runtime availability before presenting.

```swift
import Vision
import VisionKit

func canUseDataScanner() -> Bool {
    // Hardware check: requires A12 Bionic or later
    guard DataScannerViewController.isSupported else {
        return false
    }
    // Runtime check: camera authorized and not restricted
    guard DataScannerViewController.isAvailable else {
        return false
    }
    return true
}
```

`isSupported` checks hardware and platform capability (A12+ and not visionOS).
`isAvailable` checks that the camera is authorized and not restricted by Screen
Time or device management. Both must be true.

For barcode scanner configuration, VisionKit uses `VNBarcodeSymbology` values in
`DataScannerViewController.RecognizedDataType.barcode(symbologies:)`. Do not
substitute modern Vision's `BarcodeSymbology` there.

### Configuration and Initialization

```swift
import VisionKit

func createTextScanner() -> DataScannerViewController {
    DataScannerViewController(
        recognizedDataTypes: [
            .text(languages: ["en"]),
        ],
        qualityLevel: .balanced,
        recognizesMultipleItems: true,
        isHighFrameRateTrackingEnabled: true,
        isPinchToZoomEnabled: true,
        isGuidanceEnabled: true,
        isHighlightingEnabled: true
    )
}

func createBarcodeScanner() -> DataScannerViewController {
    let barcodeSymbologies: [VNBarcodeSymbology] = [.qr, .ean13, .code128]

    DataScannerViewController(
        recognizedDataTypes: [
            .barcode(symbologies: barcodeSymbologies),
        ],
        qualityLevel: .fast,
        recognizesMultipleItems: false,
        isHighFrameRateTrackingEnabled: false,
        isPinchToZoomEnabled: false,
        isGuidanceEnabled: true,
        isHighlightingEnabled: true
    )
}

func createMixedScanner() -> DataScannerViewController {
    let barcodeSymbologies: [VNBarcodeSymbology] = [.qr, .ean13]

    DataScannerViewController(
        recognizedDataTypes: [
            .text(languages: ["en"]),
            .barcode(symbologies: barcodeSymbologies),
        ],
        qualityLevel: .balanced,
        recognizesMultipleItems: true,
        isHighFrameRateTrackingEnabled: true,
        isPinchToZoomEnabled: true,
        isGuidanceEnabled: true,
        isHighlightingEnabled: true
    )
}
```

### Recognized Data Types

```swift
// Text with language hints
let textType: DataScannerViewController.RecognizedDataType =
    .text(languages: ["en", "fr", "de"])

// Text filtered by content type
let emailType: DataScannerViewController.RecognizedDataType =
    .text(textContentType: .emailAddress)
let urlType: DataScannerViewController.RecognizedDataType =
    .text(textContentType: .URL)
let phoneType: DataScannerViewController.RecognizedDataType =
    .text(textContentType: .telephoneNumber)
let addressType: DataScannerViewController.RecognizedDataType =
    .text(textContentType: .fullAddress)
let flightType: DataScannerViewController.RecognizedDataType =
    .text(textContentType: .flightNumber)
let trackingType: DataScannerViewController.RecognizedDataType =
    .text(textContentType: .shipmentTrackingNumber)

// Barcode with specific symbologies
let qrOnly: DataScannerViewController.RecognizedDataType =
    .barcode(symbologies: [.qr])
let retailBarcodes: DataScannerViewController.RecognizedDataType =
    .barcode(symbologies: [.ean8, .ean13, .upce, .code128])
```

### Quality Levels

| Level | Use Case | Notes |
|---|---|---|
| `.fast` | Barcode scanning, quick text grab | Lowest latency |
| `.balanced` | General purpose text + barcode | Default choice |
| `.accurate` | Detailed OCR, small text | Higher latency |

### Starting and Stopping

```swift
func presentScanner(_ scanner: DataScannerViewController,
                    from presenter: UIViewController) {
    scanner.delegate = presenter as? DataScannerViewControllerDelegate
    presenter.present(scanner, animated: true) {
        try? scanner.startScanning()
    }
}

func dismissScanner(_ scanner: DataScannerViewController) {
    scanner.stopScanning()
    scanner.dismiss(animated: true)
}
```

## Delegate Methods

Implement `DataScannerViewControllerDelegate` to handle recognized items and
scanner lifecycle events.

```swift
import VisionKit

final class ScannerCoordinator: NSObject, DataScannerViewControllerDelegate {

    var hasStartedScanning = false
    var onTextRecognized: ((String) -> Void)?
    var onBarcodeRecognized: ((String, VNBarcodeSymbology) -> Void)?

    // Called when the user taps on a recognized item
    func dataScanner(
        _ scanner: DataScannerViewController,
        didTapOn item: RecognizedItem
    ) {
        switch item {
        case .text(let text):
            onTextRecognized?(text.transcript)
        case .barcode(let barcode):
            if let payload = barcode.payloadStringValue {
                onBarcodeRecognized?(payload, barcode.observation.symbology)
            }
        @unknown default:
            break
        }
    }

    // Called when new items appear in the camera view
    func dataScanner(
        _ scanner: DataScannerViewController,
        didAdd addedItems: [RecognizedItem],
        allItems: [RecognizedItem]
    ) {
        for item in addedItems {
            switch item {
            case .text(let text):
                print("New text: \(text.transcript)")
            case .barcode(let barcode):
                print("New barcode: \(barcode.payloadStringValue ?? "nil")")
            @unknown default:
                break
            }
        }
    }

    // Called when items are updated (position or content changes)
    func dataScanner(
        _ scanner: DataScannerViewController,
        didUpdate updatedItems: [RecognizedItem],
        allItems: [RecognizedItem]
    ) {
        // Handle position or content updates
    }

    // Called when items leave the camera view
    func dataScanner(
        _ scanner: DataScannerViewController,
        didRemove removedItems: [RecognizedItem],
        allItems: [RecognizedItem]
    ) {
        // Clean up UI for removed items
    }

    // Called when the scanner becomes unavailable (e.g., camera revoked)
    func dataScannerDidChangeUnavailabilityReasons(
        _ scanner: DataScannerViewController
    ) {
        // Handle unavailability -- dismiss or show fallback
    }
}
```

### Async Sequence for Recognized Items

Use `recognizedItems` for a reactive stream of all currently visible items:

```swift
func observeRecognizedItems(_ scanner: DataScannerViewController) async {
    for await items in scanner.recognizedItems {
        let texts = items.compactMap { item -> String? in
            guard case .text(let text) = item else { return nil }
            return text.transcript
        }
        let barcodes = items.compactMap { item -> String? in
            guard case .barcode(let barcode) = item else { return nil }
            return barcode.payloadStringValue
        }
        await MainActor.run {
            // Update UI with current texts and barcodes
        }
    }
}
```

### Capturing a Photo

Capture a still image from the scanner for further processing:

```swift
func captureAndProcess(_ scanner: DataScannerViewController) async throws {
    let photo = try await scanner.capturePhoto()
    // photo is a UIImage -- process with Vision or save
}
```

## SwiftUI Integration

Wrap `DataScannerViewController` in `UIViewControllerRepresentable` for use
in SwiftUI views.

### Full DataScanner Representable

```swift
import SwiftUI
import AVFoundation
import Vision
import VisionKit

struct DataScannerRepresentable: UIViewControllerRepresentable {
    let recognizedDataTypes: Set<DataScannerViewController.RecognizedDataType>
    let qualityLevel: DataScannerViewController.QualityLevel
    let recognizesMultipleItems: Bool
    @Binding var recognizedText: [String]
    @Binding var recognizedBarcodes: [String]

    func makeUIViewController(context: Context) -> DataScannerViewController {
        let scanner = DataScannerViewController(
            recognizedDataTypes: recognizedDataTypes,
            qualityLevel: qualityLevel,
            recognizesMultipleItems: recognizesMultipleItems,
            isHighFrameRateTrackingEnabled: true,
            isPinchToZoomEnabled: true,
            isGuidanceEnabled: true,
            isHighlightingEnabled: true
        )
        scanner.delegate = context.coordinator
        return scanner
    }

    func updateUIViewController(
        _ controller: DataScannerViewController,
        context: Context
    ) {
        guard !context.coordinator.hasStartedScanning else { return }
        context.coordinator.hasStartedScanning = true
        Task { @MainActor in
            // SwiftUI has inserted the controller by the time update runs.
            try? controller.startScanning()
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(parent: self)
    }

    static func dismantleUIViewController(
        _ controller: DataScannerViewController,
        coordinator: Coordinator
    ) {
        controller.stopScanning()
    }

    @MainActor
    final class Coordinator: NSObject, DataScannerViewControllerDelegate {
        let parent: DataScannerRepresentable
        var hasStartedScanning = false

        init(parent: DataScannerRepresentable) {
            self.parent = parent
        }

        func dataScanner(
            _ scanner: DataScannerViewController,
            didTapOn item: RecognizedItem
        ) {
            switch item {
            case .text(let text):
                parent.recognizedText.append(text.transcript)
            case .barcode(let barcode):
                if let payload = barcode.payloadStringValue {
                    parent.recognizedBarcodes.append(payload)
                }
            @unknown default:
                break
            }
        }

        func dataScanner(
            _ scanner: DataScannerViewController,
            didAdd addedItems: [RecognizedItem],
            allItems: [RecognizedItem]
        ) {
            // Handle newly recognized items
        }

        func dataScanner(
            _ scanner: DataScannerViewController,
            didUpdate updatedItems: [RecognizedItem],
            allItems: [RecognizedItem]
        ) {
            // Handle item updates
        }

        func dataScanner(
            _ scanner: DataScannerViewController,
            didRemove removedItems: [RecognizedItem],
            allItems: [RecognizedItem]
        ) {
            // Handle removed items
        }
    }
}
```

### SwiftUI Scanner View

```swift
import SwiftUI
import AVFoundation
import VisionKit

struct ScannerView: View {
    @State private var recognizedText: [String] = []
    @State private var recognizedBarcodes: [String] = []
    @State private var isShowingScanner = false
    @State private var scannerUnavailable = false

    var body: some View {
        VStack {
            if DataScannerViewController.isSupported {
                Button("Scan") {
                    Task { @MainActor in
                        guard await requestCameraAccess(),
                              DataScannerViewController.isAvailable else {
                            scannerUnavailable = true
                            return
                        }

                        scannerUnavailable = false
                        isShowingScanner = true
                    }
                }
                .fullScreenCover(isPresented: $isShowingScanner) {
                    let barcodeSymbologies: [VNBarcodeSymbology] = [.qr]

                    NavigationStack {
                        DataScannerRepresentable(
                            recognizedDataTypes: [
                                .text(languages: ["en"]),
                                .barcode(symbologies: barcodeSymbologies),
                            ],
                            qualityLevel: .balanced,
                            recognizesMultipleItems: true,
                            recognizedText: $recognizedText,
                            recognizedBarcodes: $recognizedBarcodes
                        )
                        .ignoresSafeArea()
                        .toolbar {
                            ToolbarItem(placement: .cancellationAction) {
                                Button("Done") {
                                    isShowingScanner = false
                                }
                            }
                        }
                    }
                }
            } else {
                ContentUnavailableView(
                    "Scanner Not Available",
                    systemImage: "camera.fill",
                    description: Text("This device does not support scanning.")
                )
            }

            if scannerUnavailable {
                ContentUnavailableView(
                    "Scanner Not Available",
                    systemImage: "camera.fill",
                    description: Text("Camera access is required to scan.")
                )
            }

            List {
                Section("Text") {
                    ForEach(recognizedText, id: \.self) { text in
                        Text(text)
                    }
                }
                Section("Barcodes") {
                    ForEach(recognizedBarcodes, id: \.self) { barcode in
                        Text(barcode)
                    }
                }
            }
        }
    }
}
```

### Starting the Scanner After Presentation

The scanner must be started after the view controller is fully presented.
Use `onAppear` with a coordinator flag or start in the completion handler:

```swift
struct AutoStartScannerRepresentable: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> DataScannerViewController {
        let scanner = DataScannerViewController(
            recognizedDataTypes: [.text(languages: ["en"])],
            qualityLevel: .balanced,
            recognizesMultipleItems: false,
            isHighFrameRateTrackingEnabled: true,
            isHighlightingEnabled: true
        )
        scanner.delegate = context.coordinator
        return scanner
    }

    func updateUIViewController(
        _ controller: DataScannerViewController,
        context: Context
    ) {
        guard !context.coordinator.hasStartedScanning else { return }
        context.coordinator.hasStartedScanning = true
        Task { @MainActor in
            // updateUIViewController runs after SwiftUI has inserted the controller.
            try? controller.startScanning()
        }
    }

    func makeCoordinator() -> ScannerCoordinator {
        ScannerCoordinator()
    }

    static func dismantleUIViewController(
        _ controller: DataScannerViewController,
        coordinator: ScannerCoordinator
    ) {
        controller.stopScanning()
    }
}
```

## Custom Overlay UI

Add custom views on top of the scanner for region-of-interest indicators,
instructions, or result display.

### Overlay with Region of Interest

```swift
struct ScannerWithOverlay: View {
    @State private var isShowingScanner = false
    @State private var lastScannedText = ""

    var body: some View {
        ZStack {
            AutoStartScannerRepresentable()
                .ignoresSafeArea()

            VStack {
                // Top instruction bar
                Text("Point camera at text or barcode")
                    .font(.subheadline)
                    .padding(.horizontal)
                    .padding(.vertical)
                    .background(.ultraThinMaterial, in: Capsule())
                    .padding(.top)

                Spacer()

                // Scan region indicator
                RoundedRectangle(cornerRadius: 12)
                    .strokeBorder(.white.opacity(0.6), lineWidth: 2)
                    .frame(width: 280, height: 180)

                Spacer()

                // Result display
                if !lastScannedText.isEmpty {
                    Text(lastScannedText)
                        .font(.body)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(.ultraThinMaterial)
                        .clipShape(.rect(cornerRadius: 12))
                        .padding()
                }
            }
        }
    }
}
```

## VNDocumentCameraViewController

`VNDocumentCameraViewController` provides a full-screen document camera with
auto-capture, perspective correction, and multi-page scanning. Available on
all devices running iOS 13+.

### UIKit Presentation

```swift
import VisionKit

final class DocumentScannerPresenter: NSObject,
    VNDocumentCameraViewControllerDelegate
{
    weak var presenter: UIViewController?

    func showDocumentScanner() {
        let scanner = VNDocumentCameraViewController()
        scanner.delegate = self
        presenter?.present(scanner, animated: true)
    }

    func documentCameraViewController(
        _ controller: VNDocumentCameraViewController,
        didFinishWith scan: VNDocumentCameraScan
    ) {
        controller.dismiss(animated: true)
        for pageIndex in 0..<scan.pageCount {
            let pageImage = scan.imageOfPage(at: pageIndex)
            // Process each scanned page image
        }
    }

    func documentCameraViewControllerDidCancel(
        _ controller: VNDocumentCameraViewController
    ) {
        controller.dismiss(animated: true)
    }

    func documentCameraViewController(
        _ controller: VNDocumentCameraViewController,
        didFailWithError error: Error
    ) {
        controller.dismiss(animated: true)
        // Handle scanning error
    }
}
```

### SwiftUI Document Scanner

```swift
import SwiftUI
import VisionKit

struct DocumentScannerRepresentable: UIViewControllerRepresentable {
    @Binding var scannedImages: [UIImage]
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> VNDocumentCameraViewController {
        let scanner = VNDocumentCameraViewController()
        scanner.delegate = context.coordinator
        return scanner
    }

    func updateUIViewController(
        _ controller: VNDocumentCameraViewController,
        context: Context
    ) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(parent: self)
    }

    @MainActor
    final class Coordinator: NSObject, VNDocumentCameraViewControllerDelegate {
        let parent: DocumentScannerRepresentable

        init(parent: DocumentScannerRepresentable) {
            self.parent = parent
        }

        func documentCameraViewController(
            _ controller: VNDocumentCameraViewController,
            didFinishWith scan: VNDocumentCameraScan
        ) {
            parent.scannedImages = (0..<scan.pageCount).map { scan.imageOfPage(at: $0) }
            parent.dismiss()
        }

        func documentCameraViewControllerDidCancel(
            _ controller: VNDocumentCameraViewController
        ) {
            parent.dismiss()
        }

        func documentCameraViewController(
            _ controller: VNDocumentCameraViewController,
            didFailWithError error: Error
        ) {
            parent.dismiss()
        }
    }
}
```

### Document Scanner with OCR Pipeline

Combine document scanning with Vision text recognition for a complete OCR flow:

```swift
import SwiftUI
import VisionKit
import Vision

@MainActor
@Observable
final class DocumentOCRModel {
    var scannedPages: [UIImage] = []
    var extractedText: [String] = []
    var isProcessing = false

    func processScannedPages() async {
        isProcessing = true
        defer { isProcessing = false }

        extractedText = []
        for page in scannedPages {
            guard let cgImage = page.cgImage else { continue }
            do {
                var request = RecognizeTextRequest()
                request.recognitionLevel = .accurate
                request.recognitionLanguages = [Locale.Language(identifier: "en-US")]
                request.usesLanguageCorrection = true

                let observations = try await request.perform(on: cgImage)
                let pageText = observations
                    .compactMap { $0.topCandidates(1).first?.string }
                    .joined(separator: "\n")
                extractedText.append(pageText)
            } catch {
                extractedText.append("[Recognition failed]")
            }
        }
    }
}

struct DocumentOCRView: View {
    @State private var model = DocumentOCRModel()
    @State private var isShowingScanner = false

    var body: some View {
        NavigationStack {
            List {
                if model.isProcessing {
                    ProgressView("Recognizing text...")
                }
                ForEach(Array(model.extractedText.enumerated()), id: \.offset) { index, text in
                    Section("Page \(index + 1)") {
                        Text(text)
                            .font(.body)
                            .textSelection(.enabled)
                    }
                }
            }
            .navigationTitle("Document OCR")
            .toolbar {
                Button("Scan") {
                    isShowingScanner = true
                }
            }
            .fullScreenCover(isPresented: $isShowingScanner) {
                DocumentScannerRepresentable(scannedImages: $model.scannedPages)
            }
            .onChange(of: model.scannedPages) {
                Task { await model.processScannedPages() }
            }
        }
    }
}
```

## Performance Considerations

### DataScannerViewController

- Use `.fast` quality for barcode-only scanning
- Set `recognizesMultipleItems = false` when only one result is needed
- Disable `isHighFrameRateTrackingEnabled` for barcode scanning to save power
- Limit `recognizedDataTypes` to only what you need
- Stop scanning when processing results to avoid wasted CPU cycles

### VNDocumentCameraViewController

- Pages are returned as `UIImage` at full resolution -- resize before
  processing if memory is a concern
- Process pages sequentially to avoid memory spikes
- Use `autoreleasepool` when processing many pages in a loop
