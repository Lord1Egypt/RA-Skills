#!/usr/bin/env swift
//
// qr-decode.swift
// QR Bridge - macOS CoreImage QR Decoder
//
// Zero-dependency QR code decoder using Apple's CoreImage framework.
// Outputs structured JSON for programmatic consumption.
//
// Usage: qr-decode <image-path>
// Output: JSON { ok, count, results: [{ message, symbology }], error? }
//

import Foundation
import CoreImage

// MARK: - Data Models

struct QRResult: Codable {
    let message: String
    let symbology: String
    let bounds: Bounds?

    struct Bounds: Codable {
        let x: Double
        let y: Double
        let width: Double
        let height: Double
    }
}

struct Output: Codable {
    let ok: Bool
    let count: Int
    let results: [QRResult]
    let file: String
    let error: String?
}

// MARK: - Helper

func jsonString<T: Encodable>(_ value: T) -> String {
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
    guard let data = try? encoder.encode(value) else { return "{}" }
    return String(data: data, encoding: .utf8) ?? "{}"
}

func fail(_ message: String, file: String = "") -> Never {
    let output = Output(ok: false, count: 0, results: [], file: file, error: message)
    print(jsonString(output))
    exit(1)
}

// MARK: - Main

guard CommandLine.arguments.count > 1 else {
    fail("Usage: qr-decode <image-path>")
}

let filePath = CommandLine.arguments[1]
let fileURL = URL(fileURLWithPath: filePath)

guard FileManager.default.fileExists(atPath: filePath) else {
    fail("File not found: \(filePath)", file: filePath)
}

guard let ciImage = CIImage(contentsOf: fileURL) else {
    fail("Could not load image. Supported formats: PNG, JPEG, TIFF, BMP, GIF, HEIC", file: filePath)
}

let context = CIContext()
let detector = CIDetector(
    ofType: CIDetectorTypeQRCode,
    context: context,
    options: [CIDetectorAccuracy: CIDetectorAccuracyHigh]
)

guard let features = detector?.features(in: ciImage) else {
    fail("CoreImage detector failed to initialize", file: filePath)
}

var results: [QRResult] = []

for feature in features {
    if let qr = feature as? CIQRCodeFeature, let msg = qr.messageString {
        let b = qr.bounds
        let bounds = QRResult.Bounds(
            x: Double(b.origin.x),
            y: Double(b.origin.y),
            width: Double(b.size.width),
            height: Double(b.size.height)
        )
        results.append(QRResult(
            message: msg,
            symbology: "QRCode",
            bounds: bounds
        ))
    }
}

let output: Output
if results.isEmpty {
    output = Output(
        ok: false,
        count: 0,
        results: [],
        file: filePath,
        error: "No QR codes detected in image. Try: higher resolution, better contrast, or crop to QR region."
    )
} else {
    output = Output(
        ok: true,
        count: results.count,
        results: results,
        file: filePath,
        error: nil
    )
}

print(jsonString(output))
exit(results.isEmpty ? 1 : 0)
