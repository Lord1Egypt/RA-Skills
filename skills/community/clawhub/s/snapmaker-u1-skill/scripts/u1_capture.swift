// Local multiview reconstruction through Apple's RealityKit Object Capture.
// Build: xcrun swiftc -O -parse-as-library scripts/u1_capture.swift \
//   -o .runtime/apple/u1_capture -module-cache-path /private/tmp/u1-swift-cache

import Foundation
import RealityKit
import ImageIO
import CryptoKit
import Darwin

struct CaptureCLIError: Error {
    let code: String
    let message: String
}

struct CaptureOptions {
    let input: URL
    let output: URL
    let requestedOutput: URL
    let detail: String

    static let usage = "u1_capture doctor | u1_capture generate --input-dir PHOTOS --output-dir NEW_DIRECTORY [--detail reduced|medium|full]"
    static let imageExtensions: Set<String> = ["jpg", "jpeg", "png", "heic", "heif"]

    static func parse(_ arguments: [String]) throws -> CaptureOptions {
        var values: [String: String] = [:]
        var index = 0
        let accepted: Set<String> = ["--input-dir", "--output-dir", "--detail"]
        while index < arguments.count {
            let key = arguments[index]
            guard accepted.contains(key), values[key] == nil,
                  index + 1 < arguments.count,
                  !arguments[index + 1].isEmpty,
                  !arguments[index + 1].hasPrefix("--") else {
                throw CaptureCLIError(code: "invalid_arguments", message: "Unknown, repeated or missing argument. \(usage)")
            }
            values[key] = arguments[index + 1]
            index += 2
        }
        guard let input = values["--input-dir"], let output = values["--output-dir"] else {
            throw CaptureCLIError(code: "invalid_arguments", message: usage)
        }
        let detail = values["--detail"] ?? "medium"
        guard ["reduced", "medium", "full"].contains(detail) else {
            throw CaptureCLIError(code: "invalid_arguments", message: "Detail must be reduced, medium or full.")
        }
        let requestedOutput = URL(fileURLWithPath: output, isDirectory: true).standardizedFileURL
        return CaptureOptions(
            input: URL(fileURLWithPath: input, isDirectory: true).standardizedFileURL.resolvingSymlinksInPath(),
            output: requestedOutput.resolvingSymlinksInPath(),
            requestedOutput: requestedOutput,
            detail: detail
        )
    }

    func preflight() throws -> [[String: Any]] {
        func contains(_ ancestor: URL, _ descendant: URL) -> Bool {
            let first = ancestor.pathComponents
            return descendant.pathComponents.starts(with: first)
        }
        guard !contains(input, output), !contains(output, input) else {
            throw CaptureCLIError(code: "path_collision", message: "Input and output must be separate directories; neither may contain the other.")
        }
        var directory: ObjCBool = false
        guard FileManager.default.fileExists(atPath: input.path, isDirectory: &directory), directory.boolValue else {
            throw CaptureCLIError(code: "missing_input_directory", message: "Input must be an existing photo directory.")
        }
        // Check the spelling supplied by the caller as well as its resolved path:
        // an existing (including dangling) symlink is not a fresh output location.
        for url in [requestedOutput, output] {
            if (try? FileManager.default.attributesOfItem(atPath: url.path)) != nil {
                throw CaptureCLIError(code: "output_exists", message: "Refusing an existing output path: \(url.path)")
            }
        }
        let urls = try FileManager.default.contentsOfDirectory(
            at: input,
            includingPropertiesForKeys: [.isRegularFileKey, .isSymbolicLinkKey],
            options: [.skipsHiddenFiles]
        ).filter { Self.imageExtensions.contains($0.pathExtension.lowercased()) }
            .sorted { $0.lastPathComponent < $1.lastPathComponent }
        guard urls.count >= 2 else {
            throw CaptureCLIError(code: "insufficient_images", message: "Object Capture needs multiple overlapping photographs. Empty or single-photo folders are refused; two photos alone do not establish a sufficient capture set.")
        }
        var images: [[String: Any]] = []
        var digests = Set<String>()
        for url in urls {
            let resource = try url.resourceValues(forKeys: [.isRegularFileKey, .isSymbolicLinkKey])
            guard resource.isRegularFile == true, resource.isSymbolicLink != true else {
                throw CaptureCLIError(code: "invalid_image_path", message: "Photo entries must be regular files, not directories or symlinks: \(url.lastPathComponent)")
            }
            guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
                  let properties = CGImageSourceCopyPropertiesAtIndex(source, 0, nil) as? [CFString: Any],
                  let width = properties[kCGImagePropertyPixelWidth] as? NSNumber,
                  let height = properties[kCGImagePropertyPixelHeight] as? NSNumber,
                  width.intValue > 0, height.intValue > 0 else {
                throw CaptureCLIError(code: "invalid_image", message: "Cannot read photo metadata: \(url.lastPathComponent)")
            }
            let digest = try captureSHA256(url)
            digests.insert(digest)
            let size = try url.resourceValues(forKeys: [.fileSizeKey]).fileSize ?? 0
            images.append(["path": url.path, "sha256": digest, "bytes": size, "width": width.intValue, "height": height.intValue])
        }
        guard digests.count >= 2 else {
            throw CaptureCLIError(code: "insufficient_distinct_images", message: "Repeated copies of one photo are not a multiview capture set.")
        }
        return images
    }
}

func captureSHA256(_ url: URL) throws -> String {
    let handle = try FileHandle(forReadingFrom: url)
    defer { try? handle.close() }
    var digest = SHA256()
    while let data = try handle.read(upToCount: 8 * 1024 * 1024), !data.isEmpty {
        digest.update(data: data)
    }
    return digest.finalize().map { String(format: "%02x", $0) }.joined()
}

func captureJSON(_ value: [String: Any], pretty: Bool = false) throws -> Data {
    var options: JSONSerialization.WritingOptions = [.sortedKeys, .withoutEscapingSlashes]
    if pretty { options.insert(.prettyPrinted) }
    var data = try JSONSerialization.data(withJSONObject: value, options: options)
    data.append(0x0A)
    return data
}

func captureEmit(_ value: [String: Any]) throws {
    FileHandle.standardOutput.write(try captureJSON(value))
}

final class CaptureRecorder {
    let output: URL
    let log: FileHandle
    let started = Date()
    var report: [String: Any]

    init(options: CaptureOptions, images: [[String: Any]]) throws {
        output = options.output
        let path = output.appendingPathComponent("progress.jsonl")
        try Data().write(to: path, options: .withoutOverwriting)
        log = try FileHandle(forWritingTo: path)
        report = [
            "schema_version": 1,
            "status": "running",
            "engine": "RealityKit PhotogrammetrySession",
            "processing": "local_on_device",
            "external_upload_performed": false,
            "input_directory": options.input.path,
            "output_directory": options.output.path,
            "input_images": images,
            "input_image_count": images.count,
            "input_preprocessing": "Original full-frame files; no cropping, resizing or generated views",
            "detail": options.detail,
            "object_masking": "native_enabled",
            "sample_ordering": "unordered",
            "feature_sensitivity": "normal",
            "requested_format": "OBJ folder with materials/textures",
            "reconstruction_requested": false,
            "session_created": false,
            "request_errors": [[String: Any]](),
            "invalid_samples": [[String: Any]](),
            "skipped_sample_ids": [Int](),
            "automatic_downsampling": false,
            "stitching_incomplete": false,
            "visual_likeness_accepted": false,
            "geometry_validated": false,
            "slicing_verified": false,
            "ready_to_print": false
        ]
    }

    deinit { try? log.close() }

    func event(_ type: String, _ fields: [String: Any] = [:]) throws {
        var value = fields
        value["event"] = type
        value["elapsed_seconds"] = Date().timeIntervalSince(started)
        let data = try captureJSON(value)
        try log.write(contentsOf: data)
        FileHandle.standardOutput.write(data)
    }

    func finish(_ status: String, error: Error? = nil) throws {
        report["status"] = status
        report["elapsed_seconds"] = Date().timeIntervalSince(started)
        report["next_steps"] = "Inspect actual color and clay mesh views for likeness, completeness and unwanted background; then scale, repair, verify color/filament mapping and slice using the U1 profile. Texture detail does not establish physical mesh detail."
        if let error {
            let failure = error as? CaptureCLIError
            report["code"] = failure?.code ?? "reconstruction_failed"
            report["message"] = failure?.message ?? error.localizedDescription
        }
        try captureJSON(report, pretty: true).write(to: output.appendingPathComponent("report.json"), options: .withoutOverwriting)
        try event("report_written", ["status": status, "path": output.appendingPathComponent("report.json").path, "ready_to_print": false])
    }
}

@available(macOS 14.0, *)
func captureDoctor() -> [String: Any] {
    return [
        "status": "availability_checked",
        "engine": "RealityKit PhotogrammetrySession",
        "supported": PhotogrammetrySession.isSupported,
        "minimum_macos": "14.0 for this helper",
        "maximum_input_images": PhotogrammetrySession.limits.maximumNumberOfInputImages,
        "maximum_input_dimension": PhotogrammetrySession.limits.maximumInputImageDimension,
        "input_requirement": "Multiple overlapping photographs of a static subject from different angles",
        "output_format": "OBJ folder with material and texture sidecars",
        "external_upload_performed": false,
        "reconstruction_executed": false,
        "ready_to_print": false,
        "context_note": "A sandbox can restrict host GPU/ML services. Availability is not a reconstruction or likeness result."
    ]
}

@available(macOS 14.0, *)
func captureGenerate(_ options: CaptureOptions) async throws {
    let images = try options.preflight()
    guard images.count <= PhotogrammetrySession.limits.maximumNumberOfInputImages else {
        throw CaptureCLIError(code: "too_many_images", message: "Photo count exceeds this device's advertised input limit.")
    }
    guard PhotogrammetrySession.isSupported else {
        throw CaptureCLIError(code: "unsupported_device_or_context", message: "Object Capture is not available in this execution context. Check the native doctor on the host Mac.")
    }
    let parent = options.output.deletingLastPathComponent()
    try FileManager.default.createDirectory(at: parent, withIntermediateDirectories: true)
    guard Darwin.mkdir(options.output.path, mode_t(0o700)) == 0 else {
        throw CaptureCLIError(code: errno == EEXIST ? "output_exists" : "output_creation_failed", message: "Cannot reserve a fresh output directory: \(String(cString: strerror(errno)))")
    }
    let recorder = try CaptureRecorder(options: options, images: images)
    do {
        var configuration = PhotogrammetrySession.Configuration()
        configuration.isObjectMaskingEnabled = true
        configuration.sampleOrdering = .unordered
        configuration.featureSensitivity = .normal
        let session = try PhotogrammetrySession(input: options.input, configuration: configuration)
        recorder.report["session_created"] = true
        let detail: PhotogrammetrySession.Request.Detail = options.detail == "full" ? .full : options.detail == "reduced" ? .reduced : .medium
        let modelFolder = options.output.appendingPathComponent("model", isDirectory: true)
        let request = PhotogrammetrySession.Request.modelFile(url: modelFolder, detail: detail)
        var requestCompleted = false
        var processingCompleted = false
        try recorder.event("session_created", ["input_images": images.count, "output_format": "OBJ folder", "model_folder": modelFolder.path])
        try session.process(requests: [request])
        recorder.report["reconstruction_requested"] = true
        for try await update in session.outputs {
            switch update {
            case .inputComplete:
                try recorder.event("input_complete")
            case .requestProgress(_, let fraction):
                try recorder.event("request_progress", ["fraction_complete": fraction])
            case .requestProgressInfo(_, let info):
                var fields: [String: Any] = [:]
                if let remaining = info.estimatedRemainingTime { fields["estimated_remaining_seconds"] = remaining }
                if let stage = info.processingStage { fields["stage"] = String(describing: stage) }
                try recorder.event("request_progress_info", fields)
            case .requestComplete(_, let result):
                guard case .modelFile(let url) = result else {
                    throw CaptureCLIError(code: "unexpected_result", message: "Object Capture returned a result other than a model file.")
                }
                requestCompleted = true
                recorder.report["framework_model_location"] = url.path
                try recorder.event("request_complete", ["model_location": url.path])
            case .requestError(_, let error):
                recorder.report["request_errors"] = [["message": error.localizedDescription]]
                try recorder.event("request_error", ["message": error.localizedDescription])
                session.cancel()
                throw CaptureCLIError(code: "request_failed", message: error.localizedDescription)
            case .invalidSample(let id, let reason):
                var samples = recorder.report["invalid_samples"] as? [[String: Any]] ?? []
                samples.append(["id": id, "reason": reason])
                recorder.report["invalid_samples"] = samples
                try recorder.event("invalid_sample", ["id": id, "reason": reason])
            case .skippedSample(let id):
                var ids = recorder.report["skipped_sample_ids"] as? [Int] ?? []
                ids.append(id)
                recorder.report["skipped_sample_ids"] = ids
                try recorder.event("skipped_sample", ["id": id])
            case .automaticDownsampling:
                recorder.report["automatic_downsampling"] = true
                try recorder.event("automatic_downsampling")
            case .stitchingIncomplete:
                recorder.report["stitching_incomplete"] = true
                try recorder.event("stitching_incomplete", ["review_required": true])
            case .processingComplete:
                processingCompleted = true
                try recorder.event("processing_complete")
            case .processingCancelled:
                throw CaptureCLIError(code: "processing_cancelled", message: "Object Capture cancelled reconstruction.")
            @unknown default:
                try recorder.event("framework_update", ["description": update.localizedDescription])
            }
            if processingCompleted { break }
        }
        guard requestCompleted, processingCompleted else {
            throw CaptureCLIError(code: "incomplete_processing", message: "Object Capture ended without a completed model request and processing-complete event.")
        }
        let enumerator = FileManager.default.enumerator(at: modelFolder, includingPropertiesForKeys: [.isRegularFileKey], options: [.skipsHiddenFiles])
        var files: [String] = []
        while let url = enumerator?.nextObject() as? URL {
            if (try? url.resourceValues(forKeys: [.isRegularFileKey]).isRegularFile) == true { files.append(url.path) }
        }
        let objFiles = files.filter { URL(fileURLWithPath: $0).pathExtension.lowercased() == "obj" }
        guard !objFiles.isEmpty else {
            throw CaptureCLIError(code: "missing_obj_output", message: "The completed request did not produce an OBJ file in the requested model folder.")
        }
        recorder.report["model_files"] = files.sorted()
        recorder.report["obj_files"] = objFiles.sorted()
        recorder.report["capture_quality_review_required"] = true
        try recorder.finish("completed")
    } catch {
        try? recorder.finish("error", error: error)
        throw error
    }
}

@main
struct U1Capture {
    static func main() async {
        do {
            let arguments = Array(CommandLine.arguments.dropFirst())
            if arguments == ["--help"] || arguments == ["-h"] {
                try captureEmit(["status": "help", "engine": "RealityKit PhotogrammetrySession", "usage": CaptureOptions.usage, "existing_outputs": "refused", "default_detail": "medium", "recommended_image_extensions": CaptureOptions.imageExtensions.sorted(), "ready_to_print": false])
                return
            }
            guard #available(macOS 14.0, *) else {
                throw CaptureCLIError(code: "unsupported_system", message: "This helper requires macOS 14 or later.")
            }
            if arguments == ["doctor"] {
                try captureEmit(captureDoctor())
                return
            }
            guard arguments.first == "generate" else {
                throw CaptureCLIError(code: "invalid_arguments", message: CaptureOptions.usage)
            }
            try await captureGenerate(CaptureOptions.parse(Array(arguments.dropFirst())))
        } catch {
            let failure = error as? CaptureCLIError
            try? captureEmit(["status": "error", "engine": "RealityKit PhotogrammetrySession", "code": failure?.code ?? "processing_failed", "message": failure?.message ?? error.localizedDescription, "external_upload_performed": false, "ready_to_print": false])
            exit(2)
        }
    }
}
