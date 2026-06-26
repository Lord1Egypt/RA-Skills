# PaperKit Patterns

> **Beta-sensitive.** PaperKit is new in iOS/iPadOS 26, macOS 26, and visionOS 26. Verify all patterns against current Apple documentation before shipping.

Extended patterns, data persistence strategies, rendering, multi-platform considerations, and advanced `FeatureSet` usage for PaperKit.

## Contents

- [Data Persistence](#data-persistence)
- [Observation-Based Auto-Save](#observation-based-auto-save)
- [Forwards Compatibility and Thumbnails](#forwards-compatibility-and-thumbnails)
- [Rendering Markup to Images](#rendering-markup-to-images)
- [Multi-Platform Setup](#multi-platform-setup)
- [Full iOS Setup with Tool Picker and Insertion Menu](#full-ios-setup-with-tool-picker-and-insertion-menu)
- [Full macOS Setup with Toolbar](#full-macos-setup-with-toolbar)
- [Custom FeatureSet Patterns](#custom-featureset-patterns)
- [Programmatic Markup Construction](#programmatic-markup-construction)
- [Content Transformation](#content-transformation)
- [PencilKit Migration](#pencilkit-migration)
- [Error Handling](#error-handling)
- [Undo Support](#undo-support)
- [Document-Based App Integration](#document-based-app-integration)

## Data Persistence

### File-Based Save/Load

`PaperMarkup.dataRepresentation()` is async. Always call from an async context and handle errors.

```swift
import PaperKit

actor MarkupStore {
    private let fileURL: URL

    init(directory: URL, filename: String = "markup.paperkit") {
        self.fileURL = directory.appendingPathComponent(filename)
    }

    func save(_ markup: PaperMarkup) async throws {
        let data = try await markup.dataRepresentation()
        try data.write(to: fileURL, options: .atomic)
    }

    func load() throws -> PaperMarkup {
        let data = try Data(contentsOf: fileURL)
        return try PaperMarkup(dataRepresentation: data)
    }

    func loadOrCreate(bounds: CGRect) -> PaperMarkup {
        do {
            return try load()
        } catch {
            return PaperMarkup(bounds: bounds)
        }
    }
}
```

### Save Alongside Thumbnail

Store a rendered thumbnail next to the data file for use in file browsers or version-mismatch fallback. This is the pattern used by Notes.

```swift
func saveWithThumbnail(
    _ markup: PaperMarkup,
    dataURL: URL,
    thumbnailURL: URL,
    thumbnailSize: CGSize
) async throws {
    // Save data
    let data = try await markup.dataRepresentation()
    try data.write(to: dataURL, options: .atomic)

    // Render and save thumbnail. PaperMarkup.draw is async; await it before
    // creating the image data.
    if let cgImage = await render(markup: markup, size: thumbnailSize),
       let pngData = UIImage(cgImage: cgImage).pngData() {
        try pngData.write(to: thumbnailURL, options: .atomic)
    }
}
```

## Observation-Based Auto-Save

`PaperMarkupViewController` conforms to `Observable`. Use Observation framework tracking or the delegate for auto-save.

### Using Observations (from WWDC25 session)

```swift
let markups = Observations.untilFinished { [weak paperVC] in
    if let markup = paperVC?.markup {
        return .next(markup)
    }
    return .finish
}

Task { [weak self] in
    for await newMarkup in markups {
        try? await self?.store.save(newMarkup)
    }
}
```

### Using Delegate with Debouncing

Avoid saving on every stroke. Debounce saves to reduce disk I/O:

```swift
class MarkupViewController: UIViewController, PaperMarkupViewController.Delegate {
    var paperVC: PaperMarkupViewController!
    private var saveTask: Task<Void, Never>?

    func paperMarkupViewControllerDidChangeMarkup(
        _ controller: PaperMarkupViewController
    ) {
        saveTask?.cancel()
        saveTask = Task {
            try? await Task.sleep(for: .seconds(1))
            guard !Task.isCancelled else { return }
            guard let markup = controller.markup else { return }
            try? await store.save(markup)
        }
    }
}
```

## Forwards Compatibility and Thumbnails

When loading markup data created by a newer version of the app or OS, the data may contain features unsupported by the current `FeatureSet`. Handle this gracefully.

### Check on Load

```swift
func loadAndValidate(
    from url: URL,
    supportedFeatures: FeatureSet
) throws -> LoadResult {
    let data = try Data(contentsOf: url)
    let markup = try PaperMarkup(dataRepresentation: data)

    if markup.featureSet.isSubset(of: supportedFeatures) {
        return .editable(markup)
    } else {
        return .readOnly(markup)
    }
}

enum LoadResult {
    case editable(PaperMarkup)
    case readOnly(PaperMarkup)
}
```

### Show Thumbnail for Incompatible Content

If the loaded markup uses features the current app version does not support, show a pre-rendered thumbnail instead of a broken editor. This matches the Notes app behavior.

```swift
func handleVersionMismatch(
    markup: PaperMarkup,
    in view: UIImageView,
    size: CGSize
) async {
    if let cgImage = await render(markup: markup, size: size) {
        view.image = UIImage(cgImage: cgImage)
    }
}
```

### Strip Unsupported Content

Alternatively, remove unsupported elements and allow editing of the rest:

```swift
var markup = try PaperMarkup(dataRepresentation: data)
markup.removeContentUnsupported(by: appFeatureSet)
paperVC.markup = markup
```

This mutates the model in place, dropping any elements not representable by the given `FeatureSet`.

## Rendering Markup to Images

### Basic Rendering

```swift
func render(
    markup: PaperMarkup,
    size: CGSize,
    darkMode: Bool = false
) async -> CGImage? {
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    guard let context = CGContext(
        data: nil,
        width: Int(size.width),
        height: Int(size.height),
        bitsPerComponent: 8,
        bytesPerRow: 0,
        space: colorSpace,
        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
    ) else { return nil }

    let options = RenderingOptions(
        darkUserInterfaceStyle: darkMode,
        layoutRightToLeft: false
    )

    await markup.draw(
        in: context,
        frame: CGRect(origin: .zero, size: size),
        options: options
    )

    return context.makeImage()
}
```

### Rendering with Trait Collection

Use the current environment's traits for correct appearance:

```swift
let options = RenderingOptions(traitCollection: .current)
```

### Rendering Tight to Content

Use `contentsRenderFrame` to render only the area that has content:

```swift
let contentFrame = markup.contentsRenderFrame
let size = contentFrame.size

// Render just the content area
await markup.draw(
    in: context,
    frame: CGRect(origin: .zero, size: size),
    options: options
)
```

## Multi-Platform Setup

### Platform-Conditional Insertion UI

```swift
#if os(iOS) || os(visionOS) || targetEnvironment(macCatalyst)
import PaperKit

func setupPopoverInsertionUI(
    features: FeatureSet,
    markupVC: PaperMarkupViewController
) -> UIViewController {
    let editVC = MarkupEditViewController(
        supportedFeatureSet: features,
        additionalActions: []
    )
    editVC.delegate = markupVC
    return editVC
}
#endif

#if os(macOS)
import PaperKit

func setupToolbarInsertionUI(
    features: FeatureSet,
    markupVC: PaperMarkupViewController
) -> NSViewController {
    let toolbar = MarkupToolbarViewController(supportedFeatureSet: features)
    toolbar.delegate = markupVC
    return toolbar
}
#endif

#if targetEnvironment(macCatalyst)
import PaperKit

func setupCatalystToolbarInsertionUI(
    features: FeatureSet,
    markupVC: PaperMarkupViewController
) -> UIViewController {
    let toolbar = MarkupToolbarViewController(supportedFeatureSet: features)
    toolbar.delegate = markupVC
    return toolbar
}
#endif
```

`MarkupEditViewController` is available on iOS, iPadOS, Mac Catalyst, and visionOS for popover-style insertion. `MarkupToolbarViewController` is available on macOS and Mac Catalyst for toolbar-style insertion. Pass the same `FeatureSet` used by the `PaperMarkupViewController` to either controller.

### macOS Toolbar Properties

`MarkupToolbarViewController` exposes additional state:

| Property | Type | Description |
|---|---|---|
| `selectedDrawingTool` | `any PKTool` | Active drawing tool |
| `selectedDrawingToolItem` | `PKToolPickerItem` | Active tool picker item |
| `selectedIndirectPointerTouchMode` | `TouchMode` | Current pointer mode |
| `indirectPointerTouchModes` | `[TouchMode]` | Available pointer modes |

## Full iOS Setup with Tool Picker and Insertion Menu

Complete setup matching the WWDC25 session pattern:

```swift
import PaperKit
import PencilKit
import UIKit

class RecipeMarkupViewController: UIViewController, PaperMarkupViewController.Delegate {
    var paperVC: PaperMarkupViewController!
    var toolPicker: PKToolPicker!
    let store: MarkupStore

    init(store: MarkupStore) {
        self.store = store
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) { fatalError() }

    override func viewDidLoad() {
        super.viewDidLoad()

        let markup = store.loadOrCreate(bounds: view.bounds)
        let features = FeatureSet.latest

        // Markup controller
        paperVC = PaperMarkupViewController(
            markup: markup,
            supportedFeatureSet: features
        )
        paperVC.delegate = self

        addChild(paperVC)
        paperVC.view.frame = view.bounds
        paperVC.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(paperVC.view)
        paperVC.didMove(toParent: self)

        // Tool picker
        toolPicker = PKToolPicker()
        toolPicker.addObserver(paperVC)
        paperVC.pencilKitResponderState.activeToolPicker = toolPicker
        paperVC.pencilKitResponderState.toolPickerVisibility = .visible

        // Insertion menu button in tool picker accessory
        let insertButton = UIBarButtonItem(
            systemItem: .add,
            primaryAction: UIAction { [weak self] _ in
                self?.presentInsertionMenu()
            }
        )
        toolPicker.accessoryItem = insertButton
    }

    func presentInsertionMenu() {
        let editVC = MarkupEditViewController(
            supportedFeatureSet: paperVC.supportedFeatureSet,
            additionalActions: []
        )
        editVC.delegate = paperVC
        editVC.modalPresentationStyle = .popover
        if let popover = editVC.popoverPresentationController {
            popover.barButtonItem = toolPicker.accessoryItem
        }
        present(editVC, animated: true)
    }

    // MARK: - Delegate

    func paperMarkupViewControllerDidChangeMarkup(
        _ controller: PaperMarkupViewController
    ) {
        guard let markup = controller.markup else { return }
        Task { try? await store.save(markup) }
    }
}
```

## Full macOS Setup with Toolbar

```swift
import PaperKit
import PencilKit
import AppKit

class MacMarkupViewController: NSViewController {
    var paperVC: PaperMarkupViewController!
    let features = FeatureSet.latest

    override func viewDidLoad() {
        super.viewDidLoad()

        let markup = PaperMarkup(bounds: view.bounds)
        paperVC = PaperMarkupViewController(
            markup: markup,
            supportedFeatureSet: features
        )

        addChild(paperVC)
        paperVC.view.frame = view.bounds
        paperVC.view.autoresizingMask = [.width, .height]
        view.addSubview(paperVC.view)

        // macOS toolbar for insertion UI
        let toolbar = MarkupToolbarViewController(supportedFeatureSet: features)
        toolbar.delegate = paperVC

        addChild(toolbar)
        // Position toolbar at top of view
        let toolbarHeight: CGFloat = 44
        toolbar.view.frame = CGRect(
            x: 0, y: view.bounds.height - toolbarHeight,
            width: view.bounds.width, height: toolbarHeight
        )
        toolbar.view.autoresizingMask = [.width, .minYMargin]
        view.addSubview(toolbar.view)
    }
}
```

## Custom FeatureSet Patterns

### Annotation-Only Mode

For apps that need markup annotations without freeform drawing:

```swift
var features = FeatureSet.latest
features.remove(.drawing)
// User can insert shapes, text, images but cannot draw freehand
```

### Shapes-Only Mode

```swift
var features = FeatureSet.empty
features.insert(.shapeStrokes)
features.insert(.shapeFills)
features.shapes = [.rectangle, .ellipse, .arrowShape]
```

### Document Review Mode

```swift
var features = FeatureSet.latest
features.remove(.stickers)
features.remove(.images)
features.shapes = [.rectangle, .ellipse, .line, .arrowShape]
features.lineMarkerPositions = .single  // Single-ended arrows only
```

### HDR Creative Mode

```swift
var features = FeatureSet.latest
features.colorMaximumLinearExposure = view.window?.windowScene?.screen.potentialEDRHeadroom ?? 1.0
// Also set on tool picker:
toolPicker.colorMaximumLinearExposure = features.colorMaximumLinearExposure
```

## Programmatic Markup Construction

Build markup content in code without user interaction — useful for generating templates, reports, or test content.

### PencilKit Coexistence Boundary

Keep an existing `PKCanvasView` path when the app still needs custom brush behavior, raw `PKDrawing` / `PKStroke` analytics, or custom lasso workflows. Use PaperKit as a separate annotation layer for structured review elements and system insertion UI:

```swift
let reviewMarkup = PaperMarkup(bounds: pageBounds)
let reviewVC = PaperMarkupViewController(
    markup: reviewMarkup,
    supportedFeatureSet: reviewFeatures
)
reviewVC.contentView = pdfPageView
```

When the team is ready to make a saved PencilKit drawing visible in the PaperKit layer, append the drawing explicitly instead of replacing the low-level PencilKit editor wholesale:

```swift
var markup = PaperMarkup(bounds: pageBounds)
markup.append(contentsOf: existingPKDrawing)
```

### Building a Template

```swift
func createAnnotatedTemplate(size: CGSize) -> PaperMarkup {
    var markup = PaperMarkup(bounds: CGRect(origin: .zero, size: size))

    // Title text box
    markup.insertNewTextbox(
        attributedText: AttributedString("Document Title"),
        frame: CGRect(x: 20, y: 20, width: size.width - 40, height: 40),
        rotation: 0
    )

    // Decorative line separator
    let lineConfig = ShapeConfiguration(
        type: .line,
        fillColor: nil,
        strokeColor: UIColor.separator.cgColor,
        lineWidth: 1
    )
    markup.insertNewLine(
        configuration: lineConfig,
        from: CGPoint(x: 20, y: 70),
        to: CGPoint(x: size.width - 20, y: 70),
        startMarker: false,
        endMarker: false
    )

    // Annotation callout
    let calloutConfig = ShapeConfiguration(
        type: .chatBubble,
        fillColor: UIColor.systemYellow.withAlphaComponent(0.2).cgColor,
        strokeColor: UIColor.systemYellow.cgColor,
        lineWidth: 1.5
    )
    markup.insertNewShape(
        configuration: calloutConfig,
        frame: CGRect(x: 20, y: 90, width: 280, height: 80),
        rotation: 0
    )

    return markup
}
```

### Merging Multiple Markup Documents

```swift
var combined = PaperMarkup(bounds: totalBounds)
combined.append(contentsOf: page1Markup)
combined.append(contentsOf: page2Markup)
```

## Content Transformation

Apply affine transforms to all content in a markup model:

```swift
// Scale content to 50%
let scale = CGAffineTransform(scaleX: 0.5, y: 0.5)
markup.transformContent(scale)

// Translate content
let translate = CGAffineTransform(translationX: 100, y: 50)
markup.transformContent(translate)

// Combined transform
let transform = CGAffineTransform(scaleX: 0.5, y: 0.5)
    .translatedBy(x: 100, y: 50)
markup.transformContent(transform)
```

## PencilKit Migration

For apps already using PencilKit that want to adopt PaperKit:

### Append Existing PKDrawing

```swift
import PencilKit

func migrateDrawing(_ drawing: PKDrawing, to markup: inout PaperMarkup) {
    markup.append(contentsOf: drawing)
}
```

### Side-by-Side Drawing and Markup

PaperKit handles both layers internally. The `drawingTool` property accepts any `PKTool`:

```swift
paperVC.drawingTool = PKInkingTool(.pen, color: .black, width: 3)
paperVC.drawingTool = PKEraserTool(.bitmap)
paperVC.drawingTool = PKLassoTool()
```

## Error Handling

`MarkupError` covers deserialization failures:

| Case | Meaning |
|---|---|
| `.incorrectFormat` | Data is not PaperKit format |
| `.malformedData` | Data is corrupted |
| `.incompatibleFormatTooNew` | Data requires a newer PaperKit version |

```swift
do {
    let markup = try PaperMarkup(dataRepresentation: data)
    paperVC.markup = markup
} catch MarkupError.incompatibleFormatTooNew {
    // Show thumbnail fallback or upgrade prompt
    showUpgradePrompt()
} catch MarkupError.malformedData {
    // Data corrupted — offer to start fresh
    showCorruptionAlert()
} catch MarkupError.incorrectFormat {
    // Not PaperKit data
    showFormatError()
} catch {
    showGenericError(error)
}
```

## Undo Support

`PaperMarkupViewController` exposes an `undoManager` property. The controller registers undo actions automatically for user interactions. Connect it to the responder chain for standard undo/redo behavior.

```swift
// The undoManager is available after viewDidLoad
override var undoManager: UndoManager? {
    paperVC.undoManager
}
```

## Document-Based App Integration

PaperKit fits naturally into `UIDocument` subclasses:

```swift
class MarkupDocument: UIDocument {
    var markup: PaperMarkup?

    override func contents(forType typeName: String) throws -> Any {
        guard let markup else { throw CocoaError(.fileWriteUnknown) }
        // Use a synchronous wrapper or pre-computed data
        // Note: dataRepresentation() is async — pre-compute before save
        return precomputedData ?? Data()
    }

    override func load(fromContents contents: Any, ofType typeName: String?) throws {
        guard let data = contents as? Data else {
            throw CocoaError(.fileReadCorruptFile)
        }
        markup = try PaperMarkup(dataRepresentation: data)
    }
}
```

Since `dataRepresentation()` is async, pre-compute the data representation before the document system calls `contents(forType:)`. Trigger serialization in the delegate callback when markup changes.

### Searchable Content

`PaperMarkup.indexableContent` returns extractable text from text boxes, useful for Spotlight indexing:

```swift
if let searchText = markup.indexableContent {
    // Index with Core Spotlight
    let attributes = CSSearchableItemAttributeSet(contentType: .data)
    attributes.textContent = searchText
}
```
