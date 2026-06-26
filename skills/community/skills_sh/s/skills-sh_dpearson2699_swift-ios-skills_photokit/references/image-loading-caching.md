# Image Loading and Caching Patterns

Complete patterns for efficient image handling in iOS apps, from basic AsyncImage usage through production-ready caching and loading pipelines. All patterns use modern Swift async/await and target iOS 26 with Swift 6.3, backward-compatible to iOS 16 unless noted.

## Contents
- AsyncImage Patterns
- NSCache-Based In-Memory Cache
- URLCache-Based Disk Caching
- Image Downsampling with CGImageSource
- Image Prefetching for Lists and Grids
- HEIF/HEIC Handling
- Compression Before Upload
- Memory Budget Management
- Complete Image Loading Pipeline

## AsyncImage Patterns

AsyncImage (iOS 15+) provides built-in async image loading from a URL. Suitable for simple cases but has significant limitations for production use.

### Basic Usage

```swift
AsyncImage(url: URL(string: "https://example.com/photo.jpg"))
```

### Phase Handling

```swift
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
            .frame(width: 200, height: 200)
    case .success(let image):
        image
            .resizable()
            .aspectRatio(contentMode: .fill)
            .frame(width: 200, height: 200)
            .clipped()
    case .failure:
        Image(systemName: "photo")
            .font(.largeTitle)
            .foregroundStyle(.secondary)
            .frame(width: 200, height: 200)
    @unknown default:
        EmptyView()
    }
}
```

### Custom Transition

```swift
AsyncImage(url: imageURL, transaction: Transaction(animation: .easeIn(duration: 0.3))) { phase in
    switch phase {
    case .success(let image):
        image
            .resizable()
            .aspectRatio(contentMode: .fill)
            .transition(.opacity)
    default:
        Color.secondary.opacity(0.2)
    }
}
.frame(width: 200, height: 200)
.clipShape(.rect(cornerRadius: 12))
```

### Limitations

AsyncImage has several shortcomings for production apps:

- **No caching across redraws**: images re-download when the view is recreated.
- **No prefetching**: cannot load images ahead of scroll position.
- **No custom URLSession**: uses the shared session with no cache policy control.
- **No access to raw data**: cannot process, downsample, or persist the image data.
- **No cancellation control**: tied entirely to the view lifecycle.

For anything beyond simple, low-volume image display, use a custom loading pipeline.

---

## NSCache-Based In-Memory Cache

An actor-isolated in-memory image cache backed by NSCache. Thread-safe and automatically evicts entries under memory pressure.

```swift
import UIKit

actor ImageCache {
    static let shared = ImageCache()

    private let cache = NSCache<NSString, UIImage>()
    private var inFlightTasks: [URL: Task<UIImage?, Never>] = [:]

    init(countLimit: Int = 100, totalCostLimit: Int = 50 * 1024 * 1024) {
        cache.countLimit = countLimit
        cache.totalCostLimit = totalCostLimit  // 50 MB default
    }

    func image(for url: URL) -> UIImage? {
        cache.object(forKey: url.absoluteString as NSString)
    }

    func store(_ image: UIImage, for url: URL) {
        let cost = image.jpegData(compressionQuality: 1.0)?.count ?? 0
        cache.setObject(image, forKey: url.absoluteString as NSString, cost: cost)
    }

    func removeImage(for url: URL) {
        cache.removeObject(forKey: url.absoluteString as NSString)
    }

    func removeAll() {
        cache.removeAllObjects()
        inFlightTasks.removeAll()
    }

    /// Fetch an image with request coalescing. Multiple callers for the same URL
    /// share a single network request.
    func fetch(from url: URL, session: URLSession = .shared) async -> UIImage? {
        // Return cached image immediately
        if let cached = image(for: url) {
            return cached
        }

        // Coalesce duplicate in-flight requests
        if let existingTask = inFlightTasks[url] {
            return await existingTask.value
        }

        let task = Task<UIImage?, Never> {
            defer { inFlightTasks[url] = nil }

            guard let (data, response) = try? await session.data(from: url),
                  let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200,
                  let image = UIImage(data: data) else {
                return nil
            }

            store(image, for: url)
            return image
        }

        inFlightTasks[url] = task
        return await task.value
    }
}
```

### Usage in SwiftUI

```swift
struct CachedImageView: View {
    let url: URL
    @State private var image: UIImage?

    var body: some View {
        Group {
            if let image {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else {
                Color.secondary.opacity(0.2)
                    .overlay(ProgressView())
            }
        }
        .task(id: url) {
            image = await ImageCache.shared.fetch(from: url)
        }
    }
}
```

---

## URLCache-Based Disk Caching

Configure URLCache for persistent image caching that survives app restarts. URLCache handles HTTP cache headers automatically.

### Configuring a Dedicated URLSession

```swift
enum ImageSessionConfiguration {
    static func makeSession() -> URLSession {
        let config = URLSessionConfiguration.default

        // 50 MB memory / 200 MB disk
        config.urlCache = URLCache(
            memoryCapacity: 50 * 1024 * 1024,
            diskCapacity: 200 * 1024 * 1024,
            directory: cacheDirectory
        )

        config.requestCachePolicy = .returnCacheDataElseLoad
        config.httpMaximumConnectionsPerHost = 6

        return URLSession(configuration: config)
    }

    private static var cacheDirectory: URL {
        FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("ImageCache", isDirectory: true)
    }
}
```

### Cache-Aware Request

```swift
func cachedImageData(from url: URL, session: URLSession) async throws -> Data {
    let request = URLRequest(url: url, cachePolicy: .returnCacheDataElseLoad)
    let (data, _) = try await session.data(for: request)
    return data
}
```

### Force Refresh (Bypass Cache)

```swift
func refreshImageData(from url: URL, session: URLSession) async throws -> Data {
    let request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalCacheData)
    let (data, _) = try await session.data(for: request)
    return data
}
```

### Cache Cleanup

```swift
func cleanImageCache(session: URLSession) {
    session.configuration.urlCache?.removeAllCachedResponses()
}

func removeCachedImage(for url: URL, session: URLSession) {
    let request = URLRequest(url: url)
    session.configuration.urlCache?.removeCachedResponse(for: request)
}
```

---

## Image Downsampling with CGImageSource

Loading a full-resolution image into memory then scaling it in the view wastes significant memory. Downsampling at decode time creates a smaller bitmap directly.

### Downsample Function

```swift
import ImageIO
import UIKit

func downsample(data: Data, to pointSize: CGSize, scale: CGFloat = UITraitCollection.current.displayScale) -> UIImage? {
    let maxDimensionInPixels = max(pointSize.width, pointSize.height) * scale

    let options: [CFString: Any] = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels
    ]

    guard let source = CGImageSourceCreateWithData(data as CFData, nil),
          let cgImage = CGImageSourceCreateThumbnailAtIndex(source, 0, options as CFDictionary) else {
        return nil
    }

    return UIImage(cgImage: cgImage)
}
```

### Downsample from URL

```swift
func downsample(url: URL, to pointSize: CGSize, scale: CGFloat = UITraitCollection.current.displayScale) -> UIImage? {
    let maxDimensionInPixels = max(pointSize.width, pointSize.height) * scale

    let options: [CFString: Any] = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels
    ]

    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
          let cgImage = CGImageSourceCreateThumbnailAtIndex(source, 0, options as CFDictionary) else {
        return nil
    }

    return UIImage(cgImage: cgImage)
}
```

### When to Downsample

- Displaying thumbnails in a list or grid (a 4032x3024 photo for a 100x100 cell wastes ~46 MB per image).
- User-selected photos from the photo library.
- Images fetched from a server that are larger than the display size.
- Any time the source image dimensions exceed 2x the display point size.

### Memory Savings

| Source Size | Display Size | Without Downsampling | With Downsampling |
|---|---|---|---|
| 4032x3024 | 100x100 pt @3x | ~46 MB | ~0.35 MB |
| 4032x3024 | 300x300 pt @3x | ~46 MB | ~3.1 MB |
| 1920x1080 | 100x100 pt @3x | ~7.9 MB | ~0.35 MB |

---

## Image Prefetching for Lists and Grids

Prefetch images before they scroll into view. Works with both UICollectionView data source prefetching and SwiftUI List.

### Prefetch Coordinator

```swift
@Observable
@MainActor
final class ImagePrefetcher {
    private let cache: ImageCache
    private let session: URLSession
    private var prefetchTasks: [URL: Task<Void, Never>] = [:]

    init(cache: ImageCache = .shared,
         session: URLSession = ImageSessionConfiguration.makeSession()) {
        self.cache = cache
        self.session = session
    }

    func prefetch(urls: [URL]) {
        for url in urls {
            guard prefetchTasks[url] == nil else { continue }

            prefetchTasks[url] = Task {
                _ = await cache.fetch(from: url, session: session)
                prefetchTasks[url] = nil
            }
        }
    }

    func cancelPrefetch(urls: [URL]) {
        for url in urls {
            prefetchTasks[url]?.cancel()
            prefetchTasks[url] = nil
        }
    }

    func cancelAll() {
        prefetchTasks.values.forEach { $0.cancel() }
        prefetchTasks.removeAll()
    }
}
```

### SwiftUI Integration with ScrollView and LazyVGrid

```swift
struct PhotoGrid: View {
    let photos: [Photo]
    @State private var prefetcher = ImagePrefetcher()

    private let columns = [GridItem(.adaptive(minimum: 100), spacing: 2)]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 2) {
                ForEach(photos) { photo in
                    CachedImageView(url: photo.thumbnailURL)
                        .aspectRatio(1, contentMode: .fill)
                        .clipped()
                        .onAppear {
                            prefetchNearby(photo)
                        }
                }
            }
        }
        .onDisappear {
            prefetcher.cancelAll()
        }
    }

    private func prefetchNearby(_ photo: Photo) {
        guard let index = photos.firstIndex(where: { $0.id == photo.id }) else { return }
        let prefetchRange = (index + 1)..<min(index + 10, photos.count)
        let urls = prefetchRange.map { photos[$0].thumbnailURL }
        prefetcher.prefetch(urls: urls)
    }
}
```

### UICollectionView Prefetching (UIKit Interop)

```swift
final class PhotoCollectionPrefetcher: NSObject, UICollectionViewDataSourcePrefetching {
    private let prefetcher = ImagePrefetcher()
    private let photos: [Photo]

    init(photos: [Photo]) {
        self.photos = photos
    }

    func collectionView(_ collectionView: UICollectionView,
                        prefetchItemsAt indexPaths: [IndexPath]) {
        let urls = indexPaths.map { photos[$0.item].thumbnailURL }
        prefetcher.prefetch(urls: urls)
    }

    func collectionView(_ collectionView: UICollectionView,
                        cancelPrefetchingForItemsAt indexPaths: [IndexPath]) {
        let urls = indexPaths.map { photos[$0.item].thumbnailURL }
        prefetcher.cancelPrefetch(urls: urls)
    }
}
```

---

## HEIF/HEIC Handling

HEIF (High Efficiency Image Format) is the default camera format on modern iPhones. Handle detection, display, and conversion.

### Detection

```swift
import UniformTypeIdentifiers

func isHEIF(data: Data) -> Bool {
    guard data.count >= 12 else { return false }
    // Check for 'ftyp' box at byte 4
    let ftypRange = data[4..<8]
    return ftypRange.elementsEqual("ftyp".utf8)
}

func isHEIF(url: URL) -> Bool {
    guard let type = UTType(filenameExtension: url.pathExtension) else { return false }
    return type.conforms(to: .heif) || type.conforms(to: .heic)
}
```

### Conversion to JPEG

```swift
func convertHEICToJPEG(data: Data, compressionQuality: CGFloat = 0.9) -> Data? {
    guard let image = UIImage(data: data) else { return nil }
    return image.jpegData(compressionQuality: compressionQuality)
}
```

### Conversion to PNG

```swift
func convertHEICToPNG(data: Data) -> Data? {
    guard let image = UIImage(data: data) else { return nil }
    return image.pngData()
}
```

### Conversion with CGImageDestination (More Control)

```swift
import ImageIO

func convertHEICToJPEG(sourceData: Data,
                        quality: CGFloat = 0.9,
                        preserveMetadata: Bool = true) -> Data? {
    guard let source = CGImageSourceCreateWithData(sourceData as CFData, nil),
          let cgImage = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
        return nil
    }

    let mutableData = NSMutableData()
    guard let destination = CGImageDestinationCreateWithData(
        mutableData, UTType.jpeg.identifier as CFString, 1, nil
    ) else {
        return nil
    }

    var options: [CFString: Any] = [
        kCGImageDestinationLossyCompressionQuality: quality
    ]

    // Preserve EXIF, GPS, and other metadata
    if preserveMetadata,
       let metadata = CGImageSourceCopyPropertiesAtIndex(source, 0, nil) {
        options[kCGImageDestinationMergeMetadata] = true
        CGImageDestinationAddImage(destination, cgImage, metadata)
    } else {
        CGImageDestinationAddImage(destination, cgImage, options as CFDictionary)
    }

    guard CGImageDestinationFinalize(destination) else { return nil }
    return mutableData as Data
}
```

---

## Compression Before Upload

Reduce file size before uploading to a server. Balance quality and size based on the use case.

### JPEG Compression with Target Size

```swift
func compressForUpload(image: UIImage,
                       maxBytes: Int = 1_000_000,
                       initialQuality: CGFloat = 0.9) -> Data? {
    var quality = initialQuality

    while quality > 0.1 {
        guard let data = image.jpegData(compressionQuality: quality) else { return nil }
        if data.count <= maxBytes {
            return data
        }
        quality -= 0.1
    }

    // Final attempt at minimum quality
    return image.jpegData(compressionQuality: 0.1)
}
```

### Resize and Compress

```swift
func resizeAndCompress(image: UIImage,
                       maxDimension: CGFloat = 1920,
                       compressionQuality: CGFloat = 0.8) -> Data? {
    let size = image.size
    let scale: CGFloat

    if max(size.width, size.height) > maxDimension {
        scale = maxDimension / max(size.width, size.height)
    } else {
        scale = 1.0
    }

    let newSize = CGSize(width: size.width * scale, height: size.height * scale)

    let renderer = UIGraphicsImageRenderer(size: newSize)
    let resized = renderer.image { _ in
        image.draw(in: CGRect(origin: .zero, size: newSize))
    }

    return resized.jpegData(compressionQuality: compressionQuality)
}
```

### HEIF Compression (Smaller Files)

```swift
func compressAsHEIF(image: UIImage, quality: CGFloat = 0.8) -> Data? {
    guard let cgImage = image.cgImage else { return nil }

    let mutableData = NSMutableData()
    guard let destination = CGImageDestinationCreateWithData(
        mutableData, UTType.heic.identifier as CFString, 1, nil
    ) else {
        return nil
    }

    let options: [CFString: Any] = [
        kCGImageDestinationLossyCompressionQuality: quality
    ]

    CGImageDestinationAddImage(destination, cgImage, options as CFDictionary)
    guard CGImageDestinationFinalize(destination) else { return nil }

    return mutableData as Data
}
```

---

## Memory Budget Management

Monitor and respond to memory pressure to keep your image pipeline stable.

### Memory Warning Observer

```swift
@Observable
@MainActor
final class MemoryMonitor {
    var isUnderPressure = false

    init() {
        NotificationCenter.default.addObserver(
            forName: UIApplication.didReceiveMemoryWarningNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.handleMemoryWarning()
        }
    }

    private func handleMemoryWarning() {
        isUnderPressure = true

        Task {
            await ImageCache.shared.removeAll()
        }

        // Reset after a delay
        Task {
            try? await Task.sleep(for: .seconds(10))
            isUnderPressure = false
        }
    }
}
```

### Process Memory Usage

```swift
func currentMemoryUsageMB() -> Double {
    var info = mach_task_basic_info()
    var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size) / 4
    let result = withUnsafeMutablePointer(to: &info) {
        $0.withMemoryRebound(to: integer_t.self, capacity: Int(count)) {
            task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
        }
    }
    guard result == KERN_SUCCESS else { return 0 }
    return Double(info.resident_size) / (1024 * 1024)
}
```

### Adaptive Cache Sizing

```swift
actor AdaptiveImageCache {
    private let cache = NSCache<NSString, UIImage>()

    init() {
        let totalMemory = ProcessInfo.processInfo.physicalMemory
        // Use at most 10% of physical memory for image cache
        let budgetBytes = Int(totalMemory / 10)
        cache.totalCostLimit = budgetBytes
        cache.countLimit = 200
    }

    func image(for url: URL) -> UIImage? {
        cache.object(forKey: url.absoluteString as NSString)
    }

    func store(_ image: UIImage, for url: URL) {
        let cost = cgImageMemorySize(image)
        cache.setObject(image, forKey: url.absoluteString as NSString, cost: cost)
    }

    /// Estimate the decoded bitmap size in bytes.
    private func cgImageMemorySize(_ image: UIImage) -> Int {
        guard let cgImage = image.cgImage else { return 0 }
        return cgImage.bytesPerRow * cgImage.height
    }

    func purge() {
        cache.removeAllObjects()
    }
}
```

---

## Complete Image Loading Pipeline

A production-ready pipeline that combines in-memory caching, disk caching via URLCache, downsampling, and request coalescing.

### ImageLoader Actor

```swift
import UIKit
import ImageIO

actor ImageLoader {
    static let shared = ImageLoader()

    private let memoryCache = NSCache<NSString, UIImage>()
    private let session: URLSession
    private var inFlightTasks: [URL: Task<UIImage?, Never>] = [:]

    init() {
        let config = URLSessionConfiguration.default
        config.urlCache = URLCache(
            memoryCapacity: 50 * 1024 * 1024,
            diskCapacity: 200 * 1024 * 1024
        )
        config.requestCachePolicy = .returnCacheDataElseLoad
        config.httpMaximumConnectionsPerHost = 6
        session = URLSession(configuration: config)

        let totalMemory = ProcessInfo.processInfo.physicalMemory
        memoryCache.totalCostLimit = Int(totalMemory / 10)
        memoryCache.countLimit = 200
    }

    /// Load an image, optionally downsampling to the given display size.
    func load(from url: URL, displaySize: CGSize? = nil) async -> UIImage? {
        let cacheKey = cacheKey(url: url, size: displaySize)

        // 1. Check memory cache
        if let cached = memoryCache.object(forKey: cacheKey as NSString) {
            return cached
        }

        // 2. Coalesce duplicate in-flight requests
        if let existing = inFlightTasks[url] {
            return await existing.value
        }

        let task = Task<UIImage?, Never> {
            defer { inFlightTasks[url] = nil }

            guard let (data, response) = try? await session.data(from: url),
                  let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return nil
            }

            // 3. Downsample if a display size is provided
            let image: UIImage?
            if let displaySize {
                image = Self.downsample(data: data, to: displaySize)
            } else {
                image = UIImage(data: data)
            }

            // 4. Store in memory cache
            if let image {
                let cost = Self.bitmapSize(of: image)
                memoryCache.setObject(image, forKey: cacheKey as NSString, cost: cost)
            }

            return image
        }

        inFlightTasks[url] = task
        return await task.value
    }

    /// Remove a specific URL from the memory cache.
    func evict(url: URL, displaySize: CGSize? = nil) {
        let key = cacheKey(url: url, size: displaySize)
        memoryCache.removeObject(forKey: key as NSString)
    }

    /// Purge all in-memory cached images.
    func purgeMemoryCache() {
        memoryCache.removeAllObjects()
        inFlightTasks.values.forEach { $0.cancel() }
        inFlightTasks.removeAll()
    }

    // MARK: - Private

    private func cacheKey(url: URL, size: CGSize?) -> String {
        if let size {
            return "\(url.absoluteString)_\(Int(size.width))x\(Int(size.height))"
        }
        return url.absoluteString
    }

    private static func downsample(data: Data, to pointSize: CGSize) -> UIImage? {
        let scale = UITraitCollection.current.displayScale
        let maxDimension = max(pointSize.width, pointSize.height) * scale

        let options: [CFString: Any] = [
            kCGImageSourceCreateThumbnailFromImageAlways: true,
            kCGImageSourceShouldCacheImmediately: true,
            kCGImageSourceCreateThumbnailWithTransform: true,
            kCGImageSourceThumbnailMaxPixelSize: maxDimension
        ]

        guard let source = CGImageSourceCreateWithData(data as CFData, nil),
              let cgImage = CGImageSourceCreateThumbnailAtIndex(source, 0, options as CFDictionary) else {
            return nil
        }

        return UIImage(cgImage: cgImage)
    }

    private static func bitmapSize(of image: UIImage) -> Int {
        guard let cgImage = image.cgImage else { return 0 }
        return cgImage.bytesPerRow * cgImage.height
    }
}
```

### SwiftUI View Using the Pipeline

```swift
struct PipelineImageView: View {
    let url: URL
    var displaySize: CGSize = CGSize(width: 300, height: 300)

    @State private var image: UIImage?
    @State private var isLoading = true

    var body: some View {
        ZStack {
            if let image {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else if isLoading {
                Color.secondary.opacity(0.15)
                    .overlay(ProgressView())
            } else {
                Color.secondary.opacity(0.15)
                    .overlay {
                        Image(systemName: "photo")
                            .font(.title2)
                            .foregroundStyle(.secondary)
                    }
            }
        }
        .frame(width: displaySize.width, height: displaySize.height)
        .clipped()
        .task(id: url) {
            isLoading = true
            image = await ImageLoader.shared.load(from: url, displaySize: displaySize)
            isLoading = false
        }
    }
}
```

### Memory Warning Integration

```swift
struct PhotoGridView: View {
    let photos: [Photo]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: [GridItem(.adaptive(minimum: 100), spacing: 2)], spacing: 2) {
                ForEach(photos) { photo in
                    PipelineImageView(
                        url: photo.thumbnailURL,
                        displaySize: CGSize(width: 100, height: 100)
                    )
                }
            }
        }
        .onReceive(NotificationCenter.default.publisher(
            for: UIApplication.didReceiveMemoryWarningNotification
        )) { _ in
            Task {
                await ImageLoader.shared.purgeMemoryCache()
            }
        }
    }
}
```

### When to Use Each Layer

| Scenario | Recommended Approach |
|---|---|
| Simple profile avatar | AsyncImage |
| Photo grid with scrolling | ImageLoader + downsampling + prefetch |
| Offline-capable gallery | ImageLoader + URLCache disk caching |
| Chat message images | ImageLoader + in-memory cache |
| Full-resolution photo viewer | ImageLoader without downsampling |
| Thumbnail in a widget | Downsample at fetch time, store in app group |
