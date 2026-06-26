import AVFoundation
import CoreMedia
import Foundation

struct Config {
    var sampleRate: Double = 16000
    var deviceName: String = ""
    var listDevices = false
    var durationSeconds: Double = 0
    var debugFormat = false
}

enum StreamError: Error, CustomStringConvertible {
    case permissionDenied
    case deviceNotFound(String)
    case sessionSetupFailed(String)

    var description: String {
        switch self {
        case .permissionDenied:
            return "Microphone permission denied."
        case .deviceNotFound(let name):
            return "Audio input device not found: \(name)"
        case .sessionSetupFailed(let message):
            return "Capture session setup failed: \(message)"
        }
    }
}

func allAudioDevices() -> [AVCaptureDevice] {
    AVCaptureDevice.DiscoverySession(
        deviceTypes: [.microphone, .external],
        mediaType: .audio,
        position: .unspecified
    ).devices
}

func emitJSON(_ payload: Any, exitCode: Int32) -> Never {
    if let data = try? JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted]),
       let text = String(data: data, encoding: .utf8)
    {
        print(text)
    }
    exit(exitCode)
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
            throw StreamError.permissionDenied
        }
    }
}

func parseArgs() -> Config {
    var config = Config()
    var index = 1
    let args = CommandLine.arguments

    while index < args.count {
        switch args[index] {
        case "--sample-rate":
            index += 1
            if index < args.count, let value = Double(args[index]) {
                config.sampleRate = value
            }
        case "--device-name":
            index += 1
            if index < args.count {
                config.deviceName = args[index]
            }
        case "--list-devices":
            config.listDevices = true
        case "--duration-seconds":
            index += 1
            if index < args.count, let value = Double(args[index]) {
                config.durationSeconds = value
            }
        case "--debug-format":
            config.debugFormat = true
        default:
            break
        }
        index += 1
    }
    return config
}

func chooseDevice(deviceName: String) throws -> AVCaptureDevice {
    let devices = allAudioDevices()
    if deviceName.isEmpty {
        if let first = devices.first {
            return first
        }
        throw StreamError.deviceNotFound("(default)")
    }

    if let exact = devices.first(where: { $0.localizedName == deviceName }) {
        return exact
    }
    if let fuzzy = devices.first(where: { $0.localizedName.localizedCaseInsensitiveContains(deviceName) }) {
        return fuzzy
    }
    throw StreamError.deviceNotFound(deviceName)
}

final class PCMStreamer: NSObject, AVCaptureAudioDataOutputSampleBufferDelegate {
    private let config: Config
    private let session = AVCaptureSession()
    private let queue = DispatchQueue(label: "realtime_interpreter.audio_capture")
    private var stopped = false
    private let stopLock = NSLock()
    private var interruptSource: DispatchSourceSignal?
    private var terminateSource: DispatchSourceSignal?
    private var didEmitFormatDebug = false

    init(config: Config) {
        self.config = config
        super.init()
    }

    func run() throws {
        let device = try chooseDevice(deviceName: config.deviceName)
        let input = try AVCaptureDeviceInput(device: device)
        let output = AVCaptureAudioDataOutput()
        output.audioSettings = [
            AVFormatIDKey: kAudioFormatLinearPCM,
            AVSampleRateKey: config.sampleRate,
            AVNumberOfChannelsKey: 1,
            AVLinearPCMBitDepthKey: 16,
            AVLinearPCMIsBigEndianKey: false,
            AVLinearPCMIsFloatKey: false,
            AVLinearPCMIsNonInterleaved: false,
        ]
        output.setSampleBufferDelegate(self, queue: queue)

        session.beginConfiguration()
        if session.canAddInput(input) {
            session.addInput(input)
        } else {
            throw StreamError.sessionSetupFailed("Cannot add audio input.")
        }
        if session.canAddOutput(output) {
            session.addOutput(output)
        } else {
            throw StreamError.sessionSetupFailed("Cannot add audio output.")
        }
        session.commitConfiguration()
        session.startRunning()

        signal(SIGINT, SIG_IGN)
        signal(SIGTERM, SIG_IGN)
        let interruptSource = DispatchSource.makeSignalSource(signal: SIGINT, queue: .main)
        interruptSource.setEventHandler { [weak self] in
            self?.stop()
            CFRunLoopStop(CFRunLoopGetMain())
        }
        interruptSource.resume()
        self.interruptSource = interruptSource

        let terminateSource = DispatchSource.makeSignalSource(signal: SIGTERM, queue: .main)
        terminateSource.setEventHandler { [weak self] in
            self?.stop()
            CFRunLoopStop(CFRunLoopGetMain())
        }
        terminateSource.resume()
        self.terminateSource = terminateSource

        if config.durationSeconds > 0 {
            let deadline = Date().addingTimeInterval(config.durationSeconds)
            while Date() < deadline {
                stopLock.lock()
                let isStopped = stopped
                stopLock.unlock()
                if isStopped {
                    break
                }
                Thread.sleep(forTimeInterval: 0.05)
            }
            stop()
            return
        }

        RunLoop.current.run()
        stop()
    }

    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection
    ) {
        stopLock.lock()
        let isStopped = stopped
        stopLock.unlock()
        if isStopped {
            return
        }

        guard let blockBuffer = CMSampleBufferGetDataBuffer(sampleBuffer) else {
            return
        }

        if config.debugFormat && !didEmitFormatDebug {
            didEmitFormatDebug = true
            emitFormatDebug(sampleBuffer)
        }

        var totalLength = 0
        var dataPointer: UnsafeMutablePointer<Int8>?
        let status = CMBlockBufferGetDataPointer(
            blockBuffer,
            atOffset: 0,
            lengthAtOffsetOut: nil,
            totalLengthOut: &totalLength,
            dataPointerOut: &dataPointer
        )
        if status != kCMBlockBufferNoErr || totalLength <= 0 || dataPointer == nil {
            return
        }

        let data = Data(bytes: dataPointer!, count: totalLength)
        FileHandle.standardOutput.write(data)
    }

    private func emitFormatDebug(_ sampleBuffer: CMSampleBuffer) {
        guard let description = CMSampleBufferGetFormatDescription(sampleBuffer),
              let streamDescriptionPointer = CMAudioFormatDescriptionGetStreamBasicDescription(description)
        else {
            FileHandle.standardError.write(Data("[capture] format unavailable\n".utf8))
            return
        }

        let asbd = streamDescriptionPointer.pointee
        let message = String(
            format: "[capture] actual format sample_rate=%.2f channels=%u bits_per_channel=%u bytes_per_frame=%u frames_per_packet=%u format_id=%u format_flags=%u\n",
            asbd.mSampleRate,
            asbd.mChannelsPerFrame,
            asbd.mBitsPerChannel,
            asbd.mBytesPerFrame,
            asbd.mFramesPerPacket,
            asbd.mFormatID,
            asbd.mFormatFlags
        )
        FileHandle.standardError.write(Data(message.utf8))
    }

    private func stop() {
        stopLock.lock()
        if stopped {
            stopLock.unlock()
            return
        }
        stopped = true
        stopLock.unlock()
        session.stopRunning()
    }
}

do {
    let config = parseArgs()

    if config.listDevices {
        let payload = allAudioDevices().map { device in
            [
                "localized_name": device.localizedName,
                "unique_id": device.uniqueID,
                "manufacturer": device.manufacturer,
                "model_id": device.modelID,
            ]
        }
        emitJSON(payload, exitCode: 0)
    }

    try requestMicrophonePermission()
    let streamer = PCMStreamer(config: config)
    try streamer.run()
} catch let error as StreamError {
    FileHandle.standardError.write(Data("[capture] \(error.description)\n".utf8))
    exit(1)
} catch {
    FileHandle.standardError.write(Data("[capture] \(error.localizedDescription)\n".utf8))
    exit(1)
}
