import Foundation
import Vision
import AppKit

let args = Array(CommandLine.arguments.dropFirst())
for path in args {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("=== \(path) :: LOAD FAIL"); continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = true
    req.recognitionLanguages = ["zh-Hans", "en-US"]
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do { try handler.perform([req]) } catch { print("=== \(path) :: ERR \(error)"); continue }
    print("=== \(path) :: \(cg.width)x\(cg.height)")
    for ob in (req.results ?? []) {
        if let c = ob.topCandidates(1).first { print(c.string) }
    }
}
