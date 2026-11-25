// Local foreground extraction using Apple's system Vision framework.
// Build: xcrun swiftc -O -parse-as-library scripts/u1_vision.swift \
//   -o .runtime/apple/u1_vision -module-cache-path /private/tmp/u1-swift-cache
// macOS 14+: https://developer.apple.com/documentation/vision/vngenerateforegroundinstancemaskrequest

import Foundation
import CoreImage
import CoreGraphics
import ImageIO
import Vision

struct VisionCLIError: Error {
    let code: String
    let message: String
}

struct Options {
    let input: URL
    let output: URL
    let report: URL?
    let mode: String

    static let usage = "u1_vision --input PHOTO --output CUTOUT.png [--mode foreground|person] [--report REPORT.json]"

    static func parse(_ arguments: [String]) throws -> Options {
        var values: [String: String] = [:]
        var index = 0
        let accepted: Set<String> = ["--input", "--output", "--report", "--mode"]
        while index < arguments.count {
            let key = arguments[index]
            guard accepted.contains(key) else {
                throw VisionCLIError(code: "invalid_arguments", message: "Unknown argument: \(key). \(usage)")
            }
            guard values[key] == nil else {
                throw VisionCLIError(code: "invalid_arguments", message: "Repeated argument: \(key)")
            }
            guard index + 1 < arguments.count, !arguments[index + 1].hasPrefix("--"), !arguments[index + 1].isEmpty else {
                throw VisionCLIError(code: "invalid_arguments", message: "Missing value for \(key)")
            }
            values[key] = arguments[index + 1]
            index += 2
        }
        guard let input = values["--input"], let output = values["--output"] else {
            throw VisionCLIError(code: "invalid_arguments", message: usage)
        }
        let mode = values["--mode"] ?? "foreground"
        guard ["foreground", "person"].contains(mode) else {
            throw VisionCLIError(code: "invalid_arguments", message: "Mode must be foreground or person.")
        }
        func localURL(_ path: String) -> URL {
            URL(fileURLWithPath: path).standardizedFileURL.resolvingSymlinksInPath()
        }
        return Options(input: localURL(input), output: localURL(output), report: values["--report"].map(localURL), mode: mode)
    }

    func preflight() throws {
        guard input != output, report != input, report != output else {
            throw VisionCLIError(code: "path_collision", message: "Input, output and report must be different files; the original is never overwritten.")
        }
        var isDirectory: ObjCBool = false
        guard FileManager.default.fileExists(atPath: input.path, isDirectory: &isDirectory), !isDirectory.boolValue else {
            throw VisionCLIError(code: "missing_input", message: "Input image does not exist: \(input.path)")
        }
        guard output.pathExtension.lowercased() == "png" else {
            throw VisionCLIError(code: "invalid_arguments", message: "Output must have a .png extension to retain transparency.")
        }
        for path in [output, report].compactMap({ $0 }) {
            // attributesOfItem also identifies existing symbolic links.
            if (try? FileManager.default.attributesOfItem(atPath: path.path)) != nil {
                throw VisionCLIError(code: "output_exists", message: "Refusing to overwrite existing file: \(path.path)")
            }
        }
    }
}

func encodeJSON(_ value: [String: Any]) throws -> Data {
    var result = try JSONSerialization.data(withJSONObject: value, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
    result.append(0x0A)
    return result
}

func writeNewFile(_ data: Data, to path: URL) throws {
    try FileManager.default.createDirectory(at: path.deletingLastPathComponent(), withIntermediateDirectories: true)
    // The exclusive write also protects against a file appearing after preflight.
    try data.write(to: path, options: .withoutOverwriting)
}

@available(macOS 14.0, *)
func extractForeground(_ options: Options) throws -> [String: Any] {
    try options.preflight()
    guard let loaded = CIImage(contentsOf: options.input, options: [.applyOrientationProperty: true]) else {
        throw VisionCLIError(code: "invalid_image", message: "Input cannot be decoded as an image: \(options.input.path)")
    }
    let extent = loaded.extent.integral
    guard !extent.isNull, !extent.isInfinite, extent.width.isFinite, extent.height.isFinite, extent.width > 0, extent.height > 0,
          extent.width <= 100_000, extent.height <= 100_000, extent.width * extent.height <= 100_000_000 else {
        throw VisionCLIError(code: "invalid_image", message: "Input image has invalid dimensions or exceeds 100 million pixels.")
    }
    // Apply EXIF rotation/mirroring before both segmentation and compositing.
    // Normalize the origin so a rotated image's full frame remains unshifted.
    let image = loaded.transformed(by: CGAffineTransform(translationX: -extent.minX, y: -extent.minY))
    let bounds = CGRect(x: 0, y: 0, width: extent.width, height: extent.height)
    let width = Int(extent.width)
    let height = Int(extent.height)
    let handler = VNImageRequestHandler(ciImage: image, orientation: .up, options: [:])
    let mask: CIImage
    let requestName: String
    let instanceCount: Any
    let selection: String
    let maskResolution: [String: Int]
    if options.mode == "person" {
        let request = VNGeneratePersonSegmentationRequest()
        // Apple's accurate level adds matting refinement to the person mask.
        // This predicts a new matte; no erosion, dilation, mask intersection,
        // color replacement or arbitrary pixel trimming is applied.
        request.qualityLevel = .accurate
        request.outputPixelFormat = kCVPixelFormatType_OneComponent8
        do {
            try handler.perform([request])
        } catch {
            throw VisionCLIError(code: "vision_failed", message: "Apple Vision person-matting request failed: \(error.localizedDescription)")
        }
        guard let buffer = request.results?.first?.pixelBuffer else {
            throw VisionCLIError(code: "empty_foreground", message: "Apple Vision did not return a person matte.")
        }
        let maskWidth = CVPixelBufferGetWidth(buffer)
        let maskHeight = CVPixelBufferGetHeight(buffer)
        guard maskWidth > 0, maskHeight > 0 else {
            throw VisionCLIError(code: "empty_foreground", message: "Apple Vision returned an empty person matte.")
        }
        mask = CIImage(cvPixelBuffer: buffer).transformed(by: CGAffineTransform(scaleX: extent.width / CGFloat(maskWidth), y: extent.height / CGFloat(maskHeight))).cropped(to: bounds)
        requestName = "VNGeneratePersonSegmentationRequest"
        instanceCount = NSNull() // Person segmentation is not instance counting.
        selection = "people_in_person_matte"
        maskResolution = ["width": maskWidth, "height": maskHeight]
    } else {
        let request = VNGenerateForegroundInstanceMaskRequest()
        do {
            try handler.perform([request])
        } catch {
            throw VisionCLIError(code: "vision_failed", message: "Apple Vision foreground request failed: \(error.localizedDescription)")
        }
        guard let observation = request.results?.first, !observation.allInstances.isEmpty else {
            throw VisionCLIError(code: "empty_foreground", message: "Apple Vision did not identify any foreground instances.")
        }
        let buffer = try observation.generateScaledMaskForImage(forInstances: observation.allInstances, from: handler)
        guard CVPixelBufferGetWidth(buffer) == width, CVPixelBufferGetHeight(buffer) == height else {
            throw VisionCLIError(code: "mask_size_mismatch", message: "Apple Vision returned a mask that does not match the oriented input frame.")
        }
        mask = CIImage(cvPixelBuffer: buffer).cropped(to: bounds)
        requestName = "VNGenerateForegroundInstanceMaskRequest"
        instanceCount = observation.allInstances.count
        selection = "all_foreground_instances"
        maskResolution = ["width": width, "height": height]
    }
    let transparent = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: bounds)
    // Blending over clear pixels multiplies the original alpha by the mask,
    // preserving any transparency already present in the input image.
    let cutout = image.applyingFilter("CIBlendWithMask", parameters: [kCIInputBackgroundImageKey: transparent, kCIInputMaskImageKey: mask]).cropped(to: bounds)
    let context = CIContext(options: [.cacheIntermediates: false])
    guard let colorSpace = CGColorSpace(name: CGColorSpace.sRGB) else {
        throw VisionCLIError(code: "render_failed", message: "Cannot create the output sRGB color space.")
    }
    let pixelCount = width * height
    var pixels = [UInt8](repeating: 0, count: pixelCount * 4)
    pixels.withUnsafeMutableBytes { bytes in
        context.render(cutout, toBitmap: bytes.baseAddress!, rowBytes: width * 4, bounds: bounds, format: .RGBA8, colorSpace: colorSpace)
    }
    var minimum = UInt8.max
    var maximum: UInt8 = 0
    var transparentCount = 0
    var opaqueCount = 0
    var alphaTotal: UInt64 = 0
    for offset in stride(from: 3, to: pixels.count, by: 4) {
        let alpha = pixels[offset]
        minimum = min(minimum, alpha)
        maximum = max(maximum, alpha)
        alphaTotal += UInt64(alpha)
        if alpha == 0 { transparentCount += 1 }
        if alpha == 255 { opaqueCount += 1 }
    }
    guard maximum > 0, transparentCount < pixelCount else {
        throw VisionCLIError(code: "empty_foreground", message: "The composited foreground is entirely transparent; no output was written.")
    }
    guard let png = context.pngRepresentation(of: cutout, format: .RGBA8, colorSpace: colorSpace) else {
        throw VisionCLIError(code: "render_failed", message: "Cannot encode foreground as a transparent PNG.")
    }
    // Capture-quality analysis is advisory. A non-face subject or unavailable
    // face detector must never prevent an otherwise valid foreground mask.
    var faceReport: [String: Any] = ["status": "unavailable"]
    let faceRequest = VNDetectFaceCaptureQualityRequest()
    do {
        try handler.perform([faceRequest])
        let faces: [[String: Any]] = (faceRequest.results ?? []).map { face in
            let rectangle = face.boundingBox
            return [
                "capture_quality": face.faceCaptureQuality.map { $0 as Any } ?? NSNull(),
                "yaw_radians": face.yaw.map { $0 as Any } ?? NSNull(),
                "roll_radians": face.roll.map { $0 as Any } ?? NSNull(),
                "pitch_radians": face.pitch.map { $0 as Any } ?? NSNull(),
                "normalized_bounds_bottom_left": ["x": rectangle.minX, "y": rectangle.minY, "width": rectangle.width, "height": rectangle.height]
            ]
        }
        faceReport = ["status": "analyzed", "count": faces.count, "faces": faces]
    } catch {
        faceReport = ["status": "unavailable", "reason": error.localizedDescription]
    }
    faceReport["scope"] = "Input-photo detection and capture quality only; identity and 3D likeness are not assessed. Scores are advisory, not acceptance thresholds."
    let report: [String: Any] = [
        "schema_version": 1,
        "status": "foreground_extracted",
        "engine": "Apple Vision",
        "request": requestName,
        "mode": options.mode,
        "mask_quality": options.mode == "person" ? "accurate_with_matting_refinement" : "foreground_instance_default",
        "native_mask_dimensions": maskResolution,
        "processing": "local_on_device",
        "external_upload_performed": false,
        "input": options.input.path,
        "output": options.output.path,
        "instance_count": instanceCount,
        "selected_instances": selection,
        "dimensions": ["width": width, "height": height],
        "orientation_normalized": true,
        "full_frame_preserved": true,
        "output_color_space": "sRGB",
        "face_reference": faceReport,
        "alpha": [
            "minimum": Int(minimum),
            "maximum": Int(maximum),
            "mean": Double(alphaTotal) / Double(pixelCount),
            "transparent_pixels": transparentCount,
            "opaque_pixels": opaqueCount,
            "partial_pixels": pixelCount - transparentCount - opaqueCount,
            "nonzero_pixels": pixelCount - transparentCount,
            "foreground_fraction": Double(pixelCount - transparentCount) / Double(pixelCount)
        ],
        "review_required": options.mode == "person" ? "Compare hair, glasses, clothing, held objects and boundaries with the original. Person matting can omit accessories or non-person objects; this is segmentation, not 3D reconstruction." : "Inspect hair, glasses, clothing and mask boundaries. All detected foreground objects are retained; this is segmentation, not 3D reconstruction."
    ]
    let reportData = try encodeJSON(report)
    try writeNewFile(png, to: options.output)
    if let reportURL = options.report {
        try writeNewFile(reportData, to: reportURL)
    }
    return report
}

@main
struct U1Vision {
    static func main() {
        do {
            let arguments = Array(CommandLine.arguments.dropFirst())
            if arguments == ["--help"] || arguments == ["-h"] {
                let help: [String: Any] = ["status": "help", "engine": "Apple Vision", "usage": Options.usage, "minimum_macos": "14.0", "modes": ["foreground", "person"], "default_mode": "foreground", "selection": "all foreground instances, or a people-only accurate matte", "output": "full-frame, orientation-normalized, transparent sRGB PNG", "existing_files": "refused", "report": "optional JSON file written on success"]
                FileHandle.standardOutput.write(try encodeJSON(help))
                return
            }
            let options = try Options.parse(arguments)
            guard #available(macOS 14.0, *) else {
                throw VisionCLIError(code: "unsupported_system", message: "Foreground instance segmentation requires macOS 14 or later.")
            }
            let report = try autoreleasepool { try extractForeground(options) }
            FileHandle.standardOutput.write(try encodeJSON(report))
        } catch {
            let failure = error as? VisionCLIError
            let report: [String: Any] = ["status": "error", "engine": "Apple Vision", "code": failure?.code ?? "processing_failed", "message": failure?.message ?? error.localizedDescription, "external_upload_performed": false]
            if let data = try? encodeJSON(report) {
                FileHandle.standardOutput.write(data)
            }
            exit(2)
        }
    }
}
