import AVFoundation
import Foundation

struct Config {
    var outputPath: String = ""
    var sampleRate: Double = 16000
    var maxWaitSeconds: Double = 30
    var maxRecordSeconds: Double = 25
    var silenceSeconds: Double = 1.2
    var minSpeechSeconds: Double = 0.35
    var speechThresholdDB: Float = -24
    var pollIntervalSeconds: Double = 0.1
}

enum CaptureError: Error, CustomStringConvertible {
    case usage(String)
    case permissionDenied
    case recorderInitFailed(String)
    case noSpeechDetected

    var description: String {
        switch self {
        case .usage(let message):
            return message
        case .permissionDenied:
            return "Microphone permission denied."
        case .recorderInitFailed(let message):
            return "Recorder initialization failed: \(message)"
        case .noSpeechDetected:
            return "No speech detected."
        }
    }
}

final class CaptureController: NSObject, AVAudioRecorderDelegate {
    private let config: Config
    private let recorder: AVAudioRecorder
    private let startDate = Date()
    private var speechStartDate: Date?
    private var lastSpeechDate: Date?
    private var stopReason = "max_record"
    private var consecutiveSpeechFrames = 0
    private let requiredSpeechFrames = 3

    init(config: Config) throws {
        self.config = config

        let outputURL = URL(fileURLWithPath: config.outputPath)
        let settings: [String: Any] = [
            AVFormatIDKey: kAudioFormatLinearPCM,
            AVSampleRateKey: config.sampleRate,
            AVNumberOfChannelsKey: 1,
            AVLinearPCMBitDepthKey: 16,
            AVLinearPCMIsBigEndianKey: false,
            AVLinearPCMIsFloatKey: false,
        ]

        do {
            recorder = try AVAudioRecorder(url: outputURL, settings: settings)
        } catch {
            throw CaptureError.recorderInitFailed(error.localizedDescription)
        }

        super.init()
        recorder.delegate = self
        recorder.isMeteringEnabled = true
        recorder.prepareToRecord()
    }

    func run() throws -> [String: Any] {
        if !recorder.record() {
            throw CaptureError.recorderInitFailed("record() returned false")
        }

        while recorder.isRecording {
            RunLoop.current.run(until: Date().addingTimeInterval(config.pollIntervalSeconds))
            tick()
        }

        let duration = recorder.currentTime
        let path = recorder.url.path
        let attributes = try? FileManager.default.attributesOfItem(atPath: path)
        let size = (attributes?[.size] as? NSNumber)?.intValue ?? 0

        if speechStartDate == nil {
            throw CaptureError.noSpeechDetected
        }

        return [
            "status": "ok",
            "path": path,
            "duration_seconds": duration,
            "size_bytes": size,
            "speech_detected": true,
            "stop_reason": stopReason,
        ]
    }

    private func tick() {
        recorder.updateMeters()
        let power = recorder.averagePower(forChannel: 0)
        let now = Date()
        let elapsed = now.timeIntervalSince(startDate)

        if power > config.speechThresholdDB {
            consecutiveSpeechFrames += 1
            if speechStartDate == nil && consecutiveSpeechFrames >= requiredSpeechFrames {
                speechStartDate = now
            }
            if speechStartDate != nil {
                lastSpeechDate = now
            }
        } else {
            consecutiveSpeechFrames = 0
        }

        if speechStartDate == nil && elapsed >= config.maxWaitSeconds {
            stopReason = "wait_timeout"
            recorder.stop()
            return
        }

        if let speechStartDate {
            let speechElapsed = now.timeIntervalSince(speechStartDate)
            let silenceElapsed = now.timeIntervalSince(lastSpeechDate ?? now)
            if speechElapsed >= config.minSpeechSeconds && silenceElapsed >= config.silenceSeconds {
                stopReason = "silence"
                recorder.stop()
                return
            }
        }

        if elapsed >= config.maxRecordSeconds {
            stopReason = "max_record"
            recorder.stop()
        }
    }
}

func parseArgs() throws -> Config {
    var config = Config()
    var index = 1
    let args = CommandLine.arguments

    while index < args.count {
        let arg = args[index]
        switch arg {
        case "--output":
            index += 1
            guard index < args.count else { throw CaptureError.usage("Missing value for --output") }
            config.outputPath = args[index]
        case "--sample-rate":
            index += 1
            guard index < args.count, let value = Double(args[index]) else { throw CaptureError.usage("Invalid value for --sample-rate") }
            config.sampleRate = value
        case "--max-wait-seconds":
            index += 1
            guard index < args.count, let value = Double(args[index]) else { throw CaptureError.usage("Invalid value for --max-wait-seconds") }
            config.maxWaitSeconds = value
        case "--max-record-seconds":
            index += 1
            guard index < args.count, let value = Double(args[index]) else { throw CaptureError.usage("Invalid value for --max-record-seconds") }
            config.maxRecordSeconds = value
        case "--silence-seconds":
            index += 1
            guard index < args.count, let value = Double(args[index]) else { throw CaptureError.usage("Invalid value for --silence-seconds") }
            config.silenceSeconds = value
        case "--min-speech-seconds":
            index += 1
            guard index < args.count, let value = Double(args[index]) else { throw CaptureError.usage("Invalid value for --min-speech-seconds") }
            config.minSpeechSeconds = value
        case "--speech-threshold-db":
            index += 1
            guard index < args.count, let value = Float(args[index]) else { throw CaptureError.usage("Invalid value for --speech-threshold-db") }
            config.speechThresholdDB = value
        default:
            throw CaptureError.usage("Unknown argument: \(arg)")
        }
        index += 1
    }

    if config.outputPath.isEmpty {
        throw CaptureError.usage("Missing required --output")
    }

    return config
}

func requestMicrophonePermission() throws {
    if #available(macOS 10.14, *) {
        let semaphore = DispatchSemaphore(value: 0)
        var granted = false
        AVCaptureDevice.requestAccess(for: .audio) { ok in
            granted = ok
            semaphore.signal()
        }
        semaphore.wait()
        if !granted {
            throw CaptureError.permissionDenied
        }
    }
}

func emitJSON(_ payload: [String: Any], exitCode: Int32) -> Never {
    if let data = try? JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted]),
       let text = String(data: data, encoding: .utf8) {
        print(text)
    }
    exit(exitCode)
}

do {
    let config = try parseArgs()
    try requestMicrophonePermission()
    let controller = try CaptureController(config: config)
    let result = try controller.run()
    emitJSON(result, exitCode: 0)
} catch let error as CaptureError {
    let status: String
    switch error {
    case .noSpeechDetected:
        status = "no_speech"
    case .permissionDenied:
        status = "permission_denied"
    default:
        status = "error"
    }
    emitJSON(
        [
            "status": status,
            "error": error.description,
        ],
        exitCode: status == "no_speech" ? 2 : 1
    )
} catch {
    emitJSON(
        [
            "status": "error",
            "error": error.localizedDescription,
        ],
        exitCode: 1
    )
}
