import Foundation
import Vision
import AppKit

// Swift 5.9+ 可以用 CommandLine.arguments，兼容旧版本用下面的方式
let args = ProcessInfo.processInfo.arguments

guard args.count >= 2 else {
    print("Usage: swift macvision_swift.swift <image_path>")
    exit(1)
}

let imagePath = args[1]

// 1. 加载图片
guard let image = NSImage(contentsOfFile: imagePath) else {
    print("❌ 无法加载图片: \(imagePath)")
    exit(1)
}

// 2. 转换为 CGImage（Vision 需要）
guard let tiffData = image.tiffRepresentation,
      let cgImage = NSBitmapImageRep(data: tiffData)?.cgImage else {
    print("❌ 无法转换图片")
    exit(1)
}

// 3. 设置信号量等待异步完成
let semaphore = DispatchSemaphore(value: 0)
var results: [(text: String, confidence: Float)] = []

// 4. 创建 OCR 请求
let request = VNRecognizeTextRequest { request, error in
    defer { semaphore.signal() }  // 关键：完成后释放信号量
    
    if let error = error {
        print("❌ 识别错误：\(error)")
        return
    }
    
    guard let observations = request.results as? [VNRecognizedTextObservation] else {
        print("❌ 无结果")
        return
    }
    
    for observation in observations {
        guard let candidate = observation.topCandidates(1).first else { continue }
        results.append((candidate.string, candidate.confidence))
    }
}

// 5. 配置识别参数
request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en-US"]  // 支持中文
request.usesLanguageCorrection = true  // 启用语言校正

// 6. 执行识别
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

do {
    try handler.perform([request])
    _ = semaphore.wait(timeout: .now() + 30)  // 等待最多 30 秒
    
    // 输出结果
    for (text, conf) in results {
        print("文本：\(text)")
        print("置信度：\(String(format: "%.2f", conf * 100))%")
    }
} catch {
    print("❌ 执行错误：\(error)")
}
