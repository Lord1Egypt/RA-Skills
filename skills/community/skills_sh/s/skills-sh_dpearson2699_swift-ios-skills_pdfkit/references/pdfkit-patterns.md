# PDFKit Patterns

Extended patterns for PDFKit: form filling, creating PDFs programmatically,
watermarks, printing, merging documents, custom page overlays, document
outlines, and custom annotation drawing.

## Contents

- [Form Filling](#form-filling)
- [Creating PDFs Programmatically](#creating-pdfs-programmatically)
- [Watermarks](#watermarks)
- [Merging Documents](#merging-documents)
- [Printing](#printing)
- [Document Outlines](#document-outlines)
- [Custom Annotation Subclasses](#custom-annotation-subclasses)
- [Custom Page Subclasses](#custom-page-subclasses)
- [Page Overlay Lifecycle](#page-overlay-lifecycle)
- [Rendering Pages to Images](#rendering-pages-to-images)
- [Page Rotation and Cropping](#page-rotation-and-cropping)
- [Burning In Annotations](#burning-in-annotations)
- [Document Permissions](#document-permissions)
- [Coordinator Pattern for PDFView](#coordinator-pattern-for-pdfview)

## Form Filling

PDF forms use widget annotations. Each widget has a `fieldName`, a
`widgetFieldType`, and a `widgetStringValue`.

### Reading Form Fields

```swift
func extractFormFields(from document: PDFDocument) -> [(name: String, value: String)] {
    var fields: [(String, String)] = []
    for pageIndex in 0..<document.pageCount {
        guard let page = document.page(at: pageIndex) else { continue }
        for annotation in page.annotations {
            guard annotation.widgetFieldType == .text,
                  let name = annotation.fieldName else { continue }
            fields.append((name, annotation.widgetStringValue ?? ""))
        }
    }
    return fields
}
```

### Filling Text Fields

```swift
func fillTextField(in document: PDFDocument, fieldName: String, value: String) {
    for pageIndex in 0..<document.pageCount {
        guard let page = document.page(at: pageIndex) else { continue }
        for annotation in page.annotations {
            if annotation.widgetFieldType == .text,
               annotation.fieldName == fieldName {
                annotation.widgetStringValue = value
                return
            }
        }
    }
}
```

### Filling Checkbox Fields

```swift
func setCheckbox(in document: PDFDocument, fieldName: String, checked: Bool) {
    for pageIndex in 0..<document.pageCount {
        guard let page = document.page(at: pageIndex) else { continue }
        for annotation in page.annotations {
            if annotation.widgetFieldType == .button,
               annotation.widgetControlType == .checkBoxControl,
               annotation.fieldName == fieldName {
                annotation.buttonWidgetState = checked ? .onState : .offState
                return
            }
        }
    }
}
```

### Creating Widget Annotations

```swift
// Text field widget
func createTextField(
    bounds: CGRect,
    fieldName: String,
    placeholder: String = ""
) -> PDFAnnotation {
    let widget = PDFAnnotation(bounds: bounds, forType: .widget, withProperties: nil)
    widget.widgetFieldType = .text
    widget.fieldName = fieldName
    widget.widgetStringValue = placeholder
    widget.font = UIFont.systemFont(ofSize: 12)
    widget.backgroundColor = UIColor.systemGray6
    return widget
}

// Checkbox widget
func createCheckbox(bounds: CGRect, fieldName: String) -> PDFAnnotation {
    let widget = PDFAnnotation(bounds: bounds, forType: .widget, withProperties: nil)
    widget.widgetFieldType = .button
    widget.widgetControlType = .checkBoxControl
    widget.fieldName = fieldName
    widget.buttonWidgetState = .offState
    return widget
}

// Radio button widget
func createRadioButton(
    bounds: CGRect,
    groupName: String,
    stateString: String
) -> PDFAnnotation {
    let widget = PDFAnnotation(bounds: bounds, forType: .widget, withProperties: nil)
    widget.widgetFieldType = .button
    widget.widgetControlType = .radioButtonControl
    widget.fieldName = groupName
    widget.buttonWidgetStateString = stateString
    return widget
}

// Choice widget (dropdown)
func createDropdown(
    bounds: CGRect,
    fieldName: String,
    options: [String]
) -> PDFAnnotation {
    let widget = PDFAnnotation(bounds: bounds, forType: .widget, withProperties: nil)
    widget.widgetFieldType = .choice
    widget.fieldName = fieldName
    widget.choices = options
    widget.isListChoice = false  // false = dropdown, true = list box
    return widget
}
```

### Building a Simple Form

```swift
func buildForm() -> PDFDocument {
    let document = PDFDocument()
    let page = PDFPage()
    let pageBounds = CGRect(x: 0, y: 0, width: 612, height: 792) // Letter size
    page.setBounds(pageBounds, for: .mediaBox)

    // Name field
    let nameField = createTextField(
        bounds: CGRect(x: 100, y: 700, width: 200, height: 24),
        fieldName: "name",
        placeholder: ""
    )
    page.addAnnotation(nameField)

    // Agree checkbox
    let checkbox = createCheckbox(
        bounds: CGRect(x: 100, y: 660, width: 20, height: 20),
        fieldName: "agree"
    )
    page.addAnnotation(checkbox)

    document.insert(page, at: 0)
    return document
}
```

## Creating PDFs Programmatically

### From Images

```swift
func createPDFFromImages(_ images: [UIImage]) -> PDFDocument {
    let document = PDFDocument()
    for (index, image) in images.enumerated() {
        if let page = PDFPage(image: image) {
            document.insert(page, at: index)
        }
    }
    return document
}
```

### From Images with Options

```swift
func createPDFFromImage(
    _ image: UIImage,
    mediaBox: CGRect? = nil,
    compressionQuality: CGFloat = 0.8
) -> PDFPage? {
    var options: [PDFPage.ImageInitializationOption: Any] = [
        .compressionQuality: compressionQuality
    ]
    if let box = mediaBox {
        options[.mediaBox] = NSValue(cgRect: box)
    }
    return PDFPage(image: image, options: options)
}
```

### Using Core Graphics

For full control over PDF layout, use `UIGraphicsPDFRenderer`.

```swift
func createPDFWithCoreGraphics() -> Data {
    let pageRect = CGRect(x: 0, y: 0, width: 612, height: 792)
    let renderer = UIGraphicsPDFRenderer(bounds: pageRect)

    return renderer.pdfData { context in
        context.beginPage()

        // Draw title
        let title = "Document Title"
        let titleAttributes: [NSAttributedString.Key: Any] = [
            .font: UIFont.boldSystemFont(ofSize: 24),
            .foregroundColor: UIColor.black
        ]
        title.draw(at: CGPoint(x: 50, y: 50), withAttributes: titleAttributes)

        // Draw body text
        let body = "This is the body text of the PDF document."
        let bodyAttributes: [NSAttributedString.Key: Any] = [
            .font: UIFont.systemFont(ofSize: 12),
            .foregroundColor: UIColor.darkGray
        ]
        let bodyRect = CGRect(x: 50, y: 100, width: 512, height: 600)
        body.draw(in: bodyRect, withAttributes: bodyAttributes)

        // Draw a line
        context.cgContext.setStrokeColor(UIColor.gray.cgColor)
        context.cgContext.setLineWidth(1)
        context.cgContext.move(to: CGPoint(x: 50, y: 90))
        context.cgContext.addLine(to: CGPoint(x: 562, y: 90))
        context.cgContext.strokePath()
    }
}
```

### Loading Core Graphics PDF into PDFDocument

```swift
let pdfData = createPDFWithCoreGraphics()
let document = PDFDocument(data: pdfData)
```

## Watermarks

Add watermarks by subclassing `PDFPage` and overriding `draw(with:to:)`.

### Text Watermark

```swift
class WatermarkedPage: PDFPage {
    var watermarkText: String = "CONFIDENTIAL"

    override func draw(with box: PDFDisplayBox, to context: CGContext) {
        super.draw(with: box, to: context)

        UIGraphicsPushContext(context)
        context.saveGState()

        let pageBounds = bounds(for: box)
        let center = CGPoint(x: pageBounds.midX, y: pageBounds.midY)

        // Rotate around center
        context.translateBy(x: center.x, y: center.y)
        context.rotate(by: -.pi / 4)  // -45 degrees
        context.translateBy(x: -center.x, y: -center.y)

        let attributes: [NSAttributedString.Key: Any] = [
            .font: UIFont.boldSystemFont(ofSize: 72),
            .foregroundColor: UIColor.red.withAlphaComponent(0.15)
        ]

        let textSize = watermarkText.size(withAttributes: attributes)
        let textOrigin = CGPoint(
            x: center.x - textSize.width / 2,
            y: center.y - textSize.height / 2
        )
        watermarkText.draw(at: textOrigin, withAttributes: attributes)

        context.restoreGState()
        UIGraphicsPopContext()
    }
}
```

### Applying Watermarks via Document Delegate

```swift
class WatermarkDelegate: NSObject, PDFDocumentDelegate {
    func classForPage() -> AnyClass {
        WatermarkedPage.self
    }
}

// Usage
let delegate = WatermarkDelegate()
document.delegate = delegate
pdfView.document = document
```

### Image Watermark

```swift
class ImageWatermarkedPage: PDFPage {
    var watermarkImage: UIImage?

    override func draw(with box: PDFDisplayBox, to context: CGContext) {
        super.draw(with: box, to: context)

        guard let image = watermarkImage?.cgImage else { return }

        let pageBounds = bounds(for: box)
        let imageSize = CGSize(width: 200, height: 200)
        let imageRect = CGRect(
            x: pageBounds.midX - imageSize.width / 2,
            y: pageBounds.midY - imageSize.height / 2,
            width: imageSize.width,
            height: imageSize.height
        )

        context.saveGState()
        context.setAlpha(0.1)
        context.draw(image, in: imageRect)
        context.restoreGState()
    }
}
```

## Merging Documents

### Append All Pages

```swift
func mergeDocuments(_ documents: [PDFDocument]) -> PDFDocument {
    let merged = PDFDocument()
    var insertIndex = 0
    for document in documents {
        for pageIndex in 0..<document.pageCount {
            guard let page = document.page(at: pageIndex) else { continue }
            merged.insert(page, at: insertIndex)
            insertIndex += 1
        }
    }
    return merged
}
```

### Extract Page Range

```swift
func extractPages(
    from document: PDFDocument,
    range: ClosedRange<Int>
) -> PDFDocument {
    let extracted = PDFDocument()
    var insertIndex = 0
    for pageIndex in range {
        guard pageIndex >= 0,
              pageIndex < document.pageCount,
              let page = document.page(at: pageIndex) else { continue }
        extracted.insert(page, at: insertIndex)
        insertIndex += 1
    }
    return extracted
}
```

### Split Document

```swift
func splitDocument(_ document: PDFDocument, pagesPerChunk: Int) -> [PDFDocument] {
    var chunks: [PDFDocument] = []
    var chunkDoc = PDFDocument()
    var chunkIndex = 0

    for pageIndex in 0..<document.pageCount {
        guard let page = document.page(at: pageIndex) else { continue }
        chunkDoc.insert(page, at: chunkIndex)
        chunkIndex += 1

        if chunkIndex >= pagesPerChunk {
            chunks.append(chunkDoc)
            chunkDoc = PDFDocument()
            chunkIndex = 0
        }
    }

    if chunkDoc.pageCount > 0 {
        chunks.append(chunkDoc)
    }

    return chunks
}
```

## Printing

### Using UIPrintInteractionController

```swift
func printPDF(document: PDFDocument, from viewController: UIViewController) {
    guard let data = document.dataRepresentation() else { return }

    let printController = UIPrintInteractionController.shared
    let printInfo = UIPrintInfo(dictionary: nil)
    printInfo.outputType = .general
    printInfo.jobName = "PDF Document"

    printController.printInfo = printInfo
    printController.printingItem = data
    printController.present(animated: true)
}
```

### Print a Specific Page Range

```swift
func printPageRange(
    document: PDFDocument,
    range: ClosedRange<Int>,
    from viewController: UIViewController
) {
    let subset = extractPages(from: document, range: range)
    guard let data = subset.dataRepresentation() else { return }

    let printController = UIPrintInteractionController.shared
    let printInfo = UIPrintInfo(dictionary: nil)
    printInfo.outputType = .general
    printController.printInfo = printInfo
    printController.printingItem = data
    printController.present(animated: true)
}
```

## Document Outlines

`PDFOutline` represents the table of contents (bookmarks) of a PDF.

### Reading Outlines

```swift
func printOutline(_ outline: PDFOutline, level: Int = 0) {
    let indent = String(repeating: "  ", count: level)
    if let label = outline.label {
        print("\(indent)\(label)")
    }
    for i in 0..<outline.numberOfChildren {
        if let child = outline.child(at: i) {
            printOutline(child, level: level + 1)
        }
    }
}

// Usage
if let root = document.outlineRoot {
    printOutline(root)
}
```

### Creating Outlines

```swift
func buildOutline(for document: PDFDocument) {
    let root = PDFOutline()

    func destination(for pageIndex: Int) -> PDFDestination? {
        guard pageIndex >= 0,
              pageIndex < document.pageCount,
              let page = document.page(at: pageIndex) else { return nil }
        return PDFDestination(page: page, at: .zero)
    }

    let chapter1 = PDFOutline()
    chapter1.label = "Chapter 1"
    chapter1.destination = destination(for: 0)
    root.insertChild(chapter1, at: 0)

    let section1_1 = PDFOutline()
    section1_1.label = "Section 1.1"
    section1_1.destination = destination(for: 2)
    chapter1.insertChild(section1_1, at: 0)

    let chapter2 = PDFOutline()
    chapter2.label = "Chapter 2"
    chapter2.destination = destination(for: 5)
    root.insertChild(chapter2, at: 1)

    document.outlineRoot = root
}
```

### Navigating to an Outline Entry

```swift
func goToOutlineEntry(_ outline: PDFOutline, in pdfView: PDFView) {
    if let destination = outline.destination {
        pdfView.go(to: destination)
    } else if let action = outline.action {
        pdfView.perform(action)
    }
}
```

## Custom Annotation Subclasses

Override `draw(with:in:)` to render custom annotation graphics.

```swift
class CircleStampAnnotation: PDFAnnotation {
    override func draw(with box: PDFDisplayBox, in context: CGContext) {
        super.draw(with: box, in: context)

        UIGraphicsPushContext(context)
        context.saveGState()

        let insetBounds = bounds.insetBy(dx: 2, dy: 2)
        let path = UIBezierPath(ovalIn: insetBounds)
        path.lineWidth = 3

        UIColor.systemRed.setStroke()
        path.stroke()

        // Draw centered text
        let text = "REVIEWED"
        let attributes: [NSAttributedString.Key: Any] = [
            .font: UIFont.boldSystemFont(ofSize: 10),
            .foregroundColor: UIColor.systemRed
        ]
        let textSize = text.size(withAttributes: attributes)
        let textOrigin = CGPoint(
            x: bounds.midX - textSize.width / 2,
            y: bounds.midY - textSize.height / 2
        )
        text.draw(at: textOrigin, withAttributes: attributes)

        context.restoreGState()
        UIGraphicsPopContext()
    }
}
```

### Registering Custom Annotations via Delegate

```swift
class AnnotationDelegate: NSObject, PDFDocumentDelegate {
    func `class`(forAnnotationType annotationType: String) -> AnyClass {
        switch annotationType {
        case "CircleStamp":
            return CircleStampAnnotation.self
        default:
            return PDFAnnotation.self
        }
    }
}
```

## Custom Page Subclasses

Override `draw(with:to:)` for page-level custom drawing like headers,
footers, or decorative borders.

```swift
class HeaderFooterPage: PDFPage {
    var headerText: String = ""
    var footerText: String = ""

    override func draw(with box: PDFDisplayBox, to context: CGContext) {
        super.draw(with: box, to: context)

        UIGraphicsPushContext(context)
        context.saveGState()

        let pageBounds = bounds(for: box)
        let attributes: [NSAttributedString.Key: Any] = [
            .font: UIFont.systemFont(ofSize: 10),
            .foregroundColor: UIColor.gray
        ]

        // Header (top of page in PDF coordinates)
        if !headerText.isEmpty {
            let headerSize = headerText.size(withAttributes: attributes)
            let headerOrigin = CGPoint(
                x: pageBounds.midX - headerSize.width / 2,
                y: pageBounds.maxY - 30
            )
            headerText.draw(at: headerOrigin, withAttributes: attributes)
        }

        // Footer (bottom of page in PDF coordinates)
        if !footerText.isEmpty {
            let footerSize = footerText.size(withAttributes: attributes)
            let footerOrigin = CGPoint(
                x: pageBounds.midX - footerSize.width / 2,
                y: 20
            )
            footerText.draw(at: footerOrigin, withAttributes: attributes)
        }

        context.restoreGState()
        UIGraphicsPopContext()
    }
}
```

## Page Overlay Lifecycle

`PDFView.pageOverlayViewProvider` is weak. Store the provider on a view
controller, SwiftUI coordinator, or another object that outlives the `PDFView`.

PDFKit requests overlay views for pages it is preparing or displaying, then
calls the lifecycle hooks as pages enter and leave the visible range. Keep
overlay state outside the view so scrolling does not discard edits.

```swift
class PageOverlayProvider: NSObject, PDFPageOverlayViewProvider {
    private var pageNotes: [PDFPage: String] = [:]

    func pdfView(_ view: PDFView, overlayViewFor page: PDFPage) -> UIView? {
        let textView = UITextView()
        textView.text = pageNotes[page] ?? ""
        textView.backgroundColor = .clear
        return textView
    }

    func pdfView(
        _ view: PDFView,
        willEndDisplayingOverlayView overlayView: UIView,
        for page: PDFPage
    ) {
        if let textView = overlayView as? UITextView {
            pageNotes[page] = textView.text
        }
    }
}
```

Overlay views are UIKit/AppKit views, not PDF content. Before calling
`write(to:)` or `dataRepresentation()`, convert overlay data into PDF
annotations, custom annotation appearance streams, or rendered page content.
Use `.burnInAnnotationsOption` when saved annotations should become permanent
page content.

## Rendering Pages to Images

### Single Page

```swift
func renderPage(_ page: PDFPage, scale: CGFloat = 2.0) -> UIImage? {
    let pageBounds = page.bounds(for: .mediaBox)
    let size = CGSize(
        width: pageBounds.width * scale,
        height: pageBounds.height * scale
    )

    let renderer = UIGraphicsImageRenderer(size: size)
    return renderer.image { ctx in
        ctx.cgContext.scaleBy(x: scale, y: scale)

        // White background
        UIColor.white.setFill()
        ctx.fill(CGRect(origin: .zero, size: size))

        // PDFPage draw uses bottom-left origin; flip the context
        ctx.cgContext.translateBy(x: 0, y: pageBounds.height)
        ctx.cgContext.scaleBy(x: 1, y: -1)

        page.draw(with: .mediaBox, to: ctx.cgContext)
    }
}
```

### Thumbnail Shortcut

The simpler `thumbnail(of:for:)` method handles coordinate flipping
internally.

```swift
let thumbnail = page.thumbnail(of: CGSize(width: 200, height: 260), for: .mediaBox)
```

## Page Rotation and Cropping

### Rotation

```swift
// Rotate a page (must be a multiple of 90)
page.rotation = 90   // 0, 90, 180, or 270
```

### Cropping

Set the crop box to display only a portion of the page.

```swift
let pageBounds = page.bounds(for: .mediaBox)
let cropRect = pageBounds.insetBy(dx: 50, dy: 50)
page.setBounds(cropRect, for: .cropBox)
```

## Burning In Annotations

Write annotations permanently into the PDF content so they cannot be removed.

```swift
func burnInAnnotations(_ document: PDFDocument, to url: URL) -> Bool {
    document.write(to: url, withOptions: [
        .burnInAnnotationsOption: true
    ])
}
```

After burning in, annotations become part of the page content and are no
longer editable or removable as separate objects.

## Document Permissions

Check what operations the PDF allows.

```swift
func checkPermissions(_ document: PDFDocument) {
    let status = document.permissionsStatus  // .none, .user, .owner

    let canCopy = document.allowsCopying
    let canPrint = document.allowsPrinting
    let canComment = document.allowsCommenting
    let canFillForms = document.allowsFormFieldEntry
    let canAssemble = document.allowsDocumentAssembly
    let canModify = document.allowsDocumentChanges
    let canAccessibility = document.allowsContentAccessibility
}
```

### Writing with Access Permissions

```swift
func saveWithRestrictions(_ document: PDFDocument, to url: URL) {
    let permissions: PDFAccessPermissions = [
        .allowsLowQualityPrinting,
        .allowsContentCopying,
        .allowsCommenting
    ]
    document.write(to: url, withOptions: [
        .ownerPasswordOption: "ownerSecret",
        .userPasswordOption: "userPass",
        .accessPermissionsOption: permissions.rawValue
    ])
}
```

## Coordinator Pattern for PDFView

A reusable coordinator that handles delegate callbacks, notifications, and
annotation hit detection for a SwiftUI-wrapped PDFView.

```swift
import SwiftUI
import PDFKit

struct ManagedPDFView: UIViewRepresentable {
    let document: PDFDocument
    @Binding var currentPageIndex: Int
    var onAnnotationTapped: ((PDFAnnotation) -> Void)?

    func makeUIView(context: Context) -> PDFView {
        let pdfView = PDFView()
        pdfView.autoScales = true
        pdfView.displayMode = .singlePageContinuous
        pdfView.document = document
        pdfView.delegate = context.coordinator
        context.coordinator.attach(to: pdfView)
        return pdfView
    }

    func updateUIView(_ pdfView: PDFView, context: Context) {
        if pdfView.document !== document {
            pdfView.document = document
        }
        if currentPageIndex >= 0,
           currentPageIndex < document.pageCount,
           let page = document.page(at: currentPageIndex),
           pdfView.currentPage !== page {
            pdfView.go(to: page)
        }
    }

    static func dismantleUIView(_ uiView: PDFView, coordinator: Coordinator) {
        NotificationCenter.default.removeObserver(coordinator)
    }

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    class Coordinator: NSObject, PDFViewDelegate {
        let parent: ManagedPDFView

        init(_ parent: ManagedPDFView) {
            self.parent = parent
            super.init()
        }

        func attach(to pdfView: PDFView) {
            NotificationCenter.default.removeObserver(self)
            NotificationCenter.default.addObserver(
                self,
                selector: #selector(pageChanged),
                name: .PDFViewPageChanged,
                object: pdfView
            )
            NotificationCenter.default.addObserver(
                self,
                selector: #selector(annotationHit),
                name: .PDFViewAnnotationHit,
                object: pdfView
            )
        }

        deinit {
            NotificationCenter.default.removeObserver(self)
        }

        @objc func pageChanged(_ notification: Notification) {
            guard let pdfView = notification.object as? PDFView,
                  let page = pdfView.currentPage,
                  let doc = pdfView.document else { return }
            let index = doc.index(for: page)
            if parent.currentPageIndex != index {
                parent.currentPageIndex = index
            }
        }

        @objc func annotationHit(_ notification: Notification) {
            guard let annotation = notification.userInfo?["PDFAnnotationHit"] as? PDFAnnotation
            else { return }
            parent.onAnnotationTapped?(annotation)
        }

        func pdfViewWillClick(onLink sender: PDFView, with url: URL) {
            UIApplication.shared.open(url)
        }
    }
}
```
