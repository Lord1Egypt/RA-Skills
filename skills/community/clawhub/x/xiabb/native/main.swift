// XiaBB (虾BB) — Native macOS Voice-to-Text powered by Google Gemini
// Hold Globe (fn) key to speak. Real-time preview + accurate final transcription.
// Pure Swift, no external dependencies.

import AppKit
import AVFoundation
import CoreGraphics
import Foundation
import WebKit

// MARK: - Debug Logging

let logFileURL: URL = {
    let url = URL(fileURLWithPath: NSHomeDirectory()).appendingPathComponent("Library/Logs/XiaBB.log")
    // Rotate: keep previous log as .log.1 (preserves crash-time logs)
    let prev = url.deletingPathExtension().appendingPathExtension("log.1")
    let fm = FileManager.default
    if fm.fileExists(atPath: url.path) {
        try? fm.removeItem(at: prev)
        try? fm.moveItem(at: url, to: prev)
    }
    fm.createFile(atPath: url.path, contents: nil)
    return url
}()

// Persistent file handle — avoids open/seek/close on every log line
private let logFileHandle: FileHandle? = try? FileHandle(forWritingTo: logFileURL)
private let logLock = NSLock()

func log(_ msg: String) {
    let ts = DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .medium)
    // Sanitize: strip API keys from log output (e.g. ?key=AIza...)
    let sanitized = msg.replacingOccurrences(
        of: "key=[A-Za-z0-9_-]{10,}",
        with: "key=***REDACTED***",
        options: .regularExpression
    )
    let line = "[\(ts)] \(sanitized)\n"
    fputs(line, stderr)
    if let data = line.data(using: .utf8) {
        logLock.lock()
        logFileHandle?.seekToEndOfFile()
        logFileHandle?.write(data)
        logLock.unlock()
    }
}

// MARK: - Feature Tier

let isPro = false
// MARK: - Branding

#if CLAWBB
let APP_NAME = "ClawBB"
let APP_ID = "com.clawbb"
let APP_EMOJI = "🦞"
let APP_TAGLINE_ZH = "by Vibe Coders, for Vibe Coders"
let APP_TAGLINE_EN = "by Vibe Coders, for Vibe Coders"
#else
let APP_NAME = "XiaBB"
let APP_ID = "com.xiabb"
let APP_EMOJI = "🦞"
let APP_TAGLINE_ZH = "by Vibe Coders, for Vibe Coders"
let APP_TAGLINE_EN = "by Vibe Coders, for Vibe Coders"
#endif

// MARK: - Smart Modes

enum SmartMode: String {
    case dictation = "dictation"  // Globe only — pure transcription
    case translate = "translate"  // Globe+` — auto CN↔EN translation
    case prompt = "prompt"        // Globe+1 — optimize as AI prompt
    case email = "email"          // Globe+2 — polish as email
}

let SMART_MODE_PROMPTS: [SmartMode: String] = [
    .dictation: "", // uses buildPrompt() as-is
    .translate: """
        Listen to this audio carefully and transcribe it. Then:
        - If the speaker spoke primarily in Chinese, translate the ENTIRE output to English.
        - If the speaker spoke primarily in English, translate the ENTIRE output to Simplified Chinese (简体中文).
        - If mixed, determine the dominant language and translate everything to the OTHER language.
        Output ONLY the translated text. Do NOT include the original language. Proper punctuation and natural phrasing.
        """,
    .prompt: """
        Listen to this audio carefully. The speaker is casually describing what they want an AI to do. Your job is to transform their rough idea into a professional, detailed, production-quality prompt.

        Rules:
        1. NEVER invent details the speaker did not mention. Do NOT guess gender, clothing, objects, colors, or any specifics not stated. If the speaker said "a woman", it's a woman — never change it to a man. If they didn't mention clothing, don't add clothing.
        2. ENRICH only along dimensions the speaker implied: add quality parameters (8k, detailed), lighting, composition, camera angle, art style — but ONLY when they don't contradict or fabricate subject details.
        3. For IMAGE prompts: Improve technical quality (resolution, lighting, style keywords) but keep the EXACT subject description faithful to what was said. Never change who/what is in the image.
        4. For CODE/WRITING prompts: Add structure (format, edge cases, acceptance criteria) but don't change the core task.
        5. STRUCTURE the prompt with clear sections if complex (e.g. Role, Context, Task, Constraints, Output Format).
        6. Remove filler words, hesitation, and repetition.
        7. Output ONLY the final prompt. No meta-commentary, no explanation.
        8. CRITICAL — Language: You MUST output in the SAME language the speaker used. Chinese input → Chinese output. English → English. Do NOT translate to another language.
        """,
    .email: """
        Listen to this audio carefully. The speaker is describing what they want to communicate in an email.
        Write a professional, polite, well-formatted email based on what they said. Include a subject line on the first line prefixed with "Subject: ".
        Keep the tone appropriate — formal for business, friendly for colleagues. Fix grammar, add proper greetings and sign-off.
        Output ONLY the email, nothing else.
        If the speaker uses Chinese, write the email in Chinese. If English, in English. If mixed, use the dominant language.
        """
]

func smartModeLabel(_ mode: SmartMode) -> String {
    switch mode {
    case .dictation: return ""
    case .translate: return currentLang == "zh" ? "🔄 翻译模式" : "🔄 Translate"
    case .prompt: return currentLang == "zh" ? "⚡ Prompt 模式" : "⚡ Prompt Mode"
    case .email: return currentLang == "zh" ? "📧 邮件模式" : "📧 Email Mode"
    }
}

// MARK: - Constants
let SAMPLE_RATE: Double = 16000
let CHANNELS: UInt32 = 1
let DAILY_FREE_LIMIT = 250 // Gemini 2.5 Flash free tier: 250 RPD
let MODEL_REST = ProcessInfo.processInfo.environment["XIABB_MODEL"] ?? "gemini-2.5-flash"
let MODEL_LIVE = "gemini-2.5-flash-native-audio-latest"
let FN_FLAG: UInt64 = 0x800000 // NSEventModifierFlagFunction

let WS_URL_BASE = "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent"

let BASE_PROMPT = """
Transcribe this audio exactly as spoken, with proper punctuation.
- ALL Chinese MUST be Simplified (简体中文). Never output Traditional Chinese.
- Preserve original language per word (Chinese stays Chinese, English stays English).
- Do NOT translate. Output as a SINGLE paragraph. No line breaks.
- Output ONLY the transcribed text.
"""

// MARK: - Paths

let scriptDir: URL = {
    // Resources dir in .app bundle, fallback to ~/Tools/xiabb/
    if let resourcePath = Bundle.main.resourceURL {
        return resourcePath
    }
    return URL(fileURLWithPath: NSHomeDirectory()).appendingPathComponent("Tools/xiabb")
}()

let dataDir: URL = {
    // Config/usage data directory
    return URL(fileURLWithPath: NSHomeDirectory()).appendingPathComponent("Tools/xiabb")
}()

// MARK: - Custom Dictionary

let dictionaryFile = dataDir.appendingPathComponent("dictionary.json")

func loadDictionary() -> [String] {
    guard let data = try? Data(contentsOf: dictionaryFile),
          let arr = try? JSONSerialization.jsonObject(with: data) as? [String] else {
        // Default dictionary for Vibe Coding
        return ["Claude", "Claude Code", "OpenClaw", "Cursor", "Gemini", "Kimi", "DeepSeek",
                "Copilot", "ChatGPT", "Midjourney", "Perplexity",
                "VS Code", "Xcode", "GitHub", "GitLab", "Docker", "npm", "Homebrew", "Terminal", "iTerm",
                "API", "async", "await", "React", "Vue", "Python", "TypeScript", "JavaScript",
                "frontend", "backend", "deploy", "localhost", "webhook",
                "meeting", "deadline", "action items", "feedback", "standup", "sprint",
                "pull request", "code review", "Vibe Coding", "AI Agent"]
    }
    return arr
}

func saveDictionary(_ words: [String]) {
    if let data = try? JSONSerialization.data(withJSONObject: words) {
        try? data.write(to: dictionaryFile)
    }
}

func buildPrompt() -> String {
    let words = loadDictionary()
    if words.isEmpty { return BASE_PROMPT }
    let wordList = words.map { "\"\($0)\"" }.joined(separator: ", ")
    return BASE_PROMPT + "\n- IMPORTANT: The following words/names must be transcribed EXACTLY as specified (case-sensitive): \(wordList). Do NOT substitute similar-sounding words."
}
// MARK: - API Key

func loadAPIKey() -> String {
    if let envKey = ProcessInfo.processInfo.environment["GEMINI_API_KEY"], !envKey.isEmpty {
        return envKey
    }
    let keyFile = dataDir.appendingPathComponent(".api-key")
    if let data = try? String(contentsOf: keyFile, encoding: .utf8) {
        return data.trimmingCharacters(in: .whitespacesAndNewlines)
    }
    return ""
}

var apiKey = loadAPIKey()

// MARK: - T2S (Traditional → Simplified Chinese)

func t2s(_ text: String) -> String {
    let mutable = NSMutableString(string: text)
    CFStringTransform(mutable, nil, "Traditional-Simplified" as CFString, false)
    return mutable as String
}

// MARK: - Config

let configFile = dataDir.appendingPathComponent(".config.json")

func loadConfig() -> [String: Any] {
    guard let data = try? Data(contentsOf: configFile),
          let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
        return [:]
    }
    return json
}

func saveConfig(_ updates: [String: Any]) {
    var existing = loadConfig()
    for (k, v) in updates { existing[k] = v }
    if let data = try? JSONSerialization.data(withJSONObject: existing) {
        try? data.write(to: configFile)
    }
}

// MARK: - Themes / Skins

struct HUDTheme {
    let name: String
    let bgRed: CGFloat, bgGreen: CGFloat, bgBlue: CGFloat, bgAlpha: CGFloat
    let cornerRadius: CGFloat
    let textColor: NSColor
    let recordingColor: NSColor
    let successColor: NSColor
    let barColor: NSColor  // wave bar color during recording
    let fontSize: CGFloat
}

// Theme registry — designed for easy extension. Add new themes here.
// Future: load from .cbskin files (ZIP with theme.json + assets)
let themeList: [(id: String, theme: HUDTheme)] = [
    ("lobster", HUDTheme(
        name: "🦞 Lobster Red",
        bgRed: 0.157, bgGreen: 0.149, bgBlue: 0.145, bgAlpha: 0.93,  // #282828
        cornerRadius: 12,
        textColor: NSColor(calibratedRed: 0.922, green: 0.859, blue: 0.698, alpha: 1),  // #EBDBB2 cream
        recordingColor: NSColor(calibratedRed: 0.918, green: 0.412, blue: 0.384, alpha: 1),  // #EA6962 coral
        successColor: NSColor(calibratedRed: 0.663, green: 0.714, blue: 0.396, alpha: 1),  // #A9B665 green
        barColor: NSColor(calibratedRed: 0.918, green: 0.412, blue: 0.384, alpha: 1),  // #EA6962 coral
        fontSize: 13
    )),
    ("chill", HUDTheme(
        name: "🌿 Chill Green",
        bgRed: 0.06, bgGreen: 0.12, bgBlue: 0.08, bgAlpha: 0.92,
        cornerRadius: 16,
        textColor: NSColor(calibratedRed: 0.85, green: 1.0, blue: 0.9, alpha: 1),
        recordingColor: NSColor(calibratedRed: 0.3, green: 0.85, blue: 0.5, alpha: 1),
        successColor: NSColor(calibratedRed: 0.5, green: 1.0, blue: 0.7, alpha: 1),
        barColor: NSColor(calibratedRed: 0.3, green: 0.85, blue: 0.5, alpha: 1),
        fontSize: 13
    )),
    ("ocean", HUDTheme(
        name: "🌊 Ocean Blue",
        bgRed: 0.04, bgGreen: 0.08, bgBlue: 0.18, bgAlpha: 0.93,
        cornerRadius: 14,
        textColor: NSColor(calibratedRed: 0.75, green: 0.92, blue: 1.0, alpha: 1),
        recordingColor: NSColor(calibratedRed: 0.25, green: 0.65, blue: 1.0, alpha: 1),
        successColor: NSColor(calibratedRed: 0.3, green: 1.0, blue: 0.75, alpha: 1),
        barColor: NSColor(calibratedRed: 0.25, green: 0.65, blue: 1.0, alpha: 1),
        fontSize: 13
    )),
    ("sunset", HUDTheme(
        name: "🌅 Sunset Orange",
        bgRed: 0.16, bgGreen: 0.08, bgBlue: 0.04, bgAlpha: 0.93,
        cornerRadius: 14,
        textColor: NSColor(calibratedRed: 1.0, green: 0.93, blue: 0.82, alpha: 1),
        recordingColor: NSColor(calibratedRed: 1.0, green: 0.55, blue: 0.15, alpha: 1),
        successColor: NSColor(calibratedRed: 0.4, green: 0.9, blue: 0.5, alpha: 1),
        barColor: NSColor(calibratedRed: 1.0, green: 0.55, blue: 0.15, alpha: 1),
        fontSize: 13
    )),
]

let themes: [String: HUDTheme] = Dictionary(uniqueKeysWithValues: themeList.map { ($0.id, $0.theme) })

var currentTheme: HUDTheme = {
    let name = loadConfig()["theme"] as? String ?? "lobster"
    return themes[name] ?? themes["lobster"]!
}()

// MARK: - i18n

let strings: [String: [String: String]] = [
    "en": [
        "idle": "Idle",
        "recording": "Recording...",
        "transcribing": "Transcribing...",
        "listening": "Listening...",
        "finalizing": "Finalizing...",
        "copied": "Copied!",
        "left": "left",
        "start": "Start Recording",
        "stop": "Stop",
        "hotkey": "Hold Globe key to record",
        "configure_api": "Configure Gemini API Key...",
        "launch_login": "Launch at Login",
        "language": "Language",
        "quit": "Quit XiaBB",
        "daily_limit": "Daily limit reached",
        "update_available": "Update available",
        "update_now": "Download Update",
        "feedback": "Send Feedback",
        "check_update": "Check for Updates...",
        "up_to_date": "You're up to date!",
    ],
    "zh": [
        "idle": "待命",
        "recording": "录音中...",
        "transcribing": "识别中...",
        "listening": "聆听中...",
        "finalizing": "处理中...",
        "copied": "已复制!",
        "left": "剩余",
        "start": "开始录音",
        "stop": "停止",
        "hotkey": "按住 Globe 键录音",
        "configure_api": "配置 Gemini API Key...",
        "launch_login": "开机自动启动",
        "language": "语言 / Language",
        "quit": "退出 虾BB",
        "daily_limit": "今日额度已用完",
        "update_available": "有新版本可用",
        "update_now": "下载更新",
        "feedback": "反馈意见",
        "check_update": "检查更新...",
        "up_to_date": "已是最新版本!",
    ],
]

var currentLang: String = loadConfig()["lang"] as? String ?? "zh"

func L(_ key: String) -> String {
    return strings[currentLang]?[key] ?? strings["en"]?[key] ?? key
}

// MARK: - Usage Tracker

class UsageTracker {
    private let file = dataDir.appendingPathComponent(".usage.json")
    private var date: String
    private(set) var count: Int

    init() {
        let today = Self.today()
        if let data = try? Data(contentsOf: file),
           let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let d = json["date"] as? String, d == today,
           let c = json["count"] as? Int {
            date = d
            count = c
        } else {
            date = today
            count = 0
        }
    }

    static func today() -> String {
        let df = DateFormatter()
        df.dateFormat = "yyyy-MM-dd"
        return df.string(from: Date())
    }

    var remaining: Int { max(0, DAILY_FREE_LIMIT - count) }

    func statusLine() -> String { "\(count)/\(DAILY_FREE_LIMIT) (\(remaining) left)" }

    @discardableResult
    func increment() -> Int {
        let today = Self.today()
        if date != today { date = today; count = 0 }
        count += 1
        save()
        return count
    }

    private func save() {
        let json: [String: Any] = ["date": date, "count": count]
        if let data = try? JSONSerialization.data(withJSONObject: json) {
            try? data.write(to: file)
        }
    }
}

let usage = UsageTracker()

// MARK: - Sound Effects

func generateTone(frequencies: [(Double, Double)], duration: Double, attack: Double = 0.008, release: Double = 0.04, amplitude: Double = 0.05) -> Data {
    let sampleRate = 44100.0
    let numSamples = Int(sampleRate * duration)
    var samples = [Int16](repeating: 0, count: numSamples)

    for i in 0..<numSamples {
        let t = Double(i) / sampleRate
        var value = 0.0
        for (freq, amp) in frequencies {
            value += amp * sin(2.0 * .pi * freq * t)
        }
        // Envelope
        let attackSamples = Int(sampleRate * attack)
        let releaseSamples = Int(sampleRate * release)
        var env = 1.0
        if i < attackSamples {
            env = 0.5 * (1.0 - cos(.pi * Double(i) / Double(attackSamples)))
        } else if i > numSamples - releaseSamples {
            let ri = i - (numSamples - releaseSamples)
            env = 0.5 * (1.0 + cos(.pi * Double(ri) / Double(releaseSamples)))
        }
        samples[i] = Int16(clamping: Int(value * env * amplitude * 32767.0))
    }

    return makeWAVData(samples: samples, sampleRate: Int(sampleRate))
}

func makeWAVData(samples: [Int16], sampleRate: Int, channels: Int = 1) -> Data {
    var data = Data()
    let dataSize = samples.count * 2
    let fileSize = 36 + dataSize

    // RIFF header
    data.append(contentsOf: "RIFF".utf8)
    data.append(contentsOf: withUnsafeBytes(of: UInt32(fileSize).littleEndian) { Array($0) })
    data.append(contentsOf: "WAVE".utf8)

    // fmt chunk
    data.append(contentsOf: "fmt ".utf8)
    data.append(contentsOf: withUnsafeBytes(of: UInt32(16).littleEndian) { Array($0) })
    data.append(contentsOf: withUnsafeBytes(of: UInt16(1).littleEndian) { Array($0) }) // PCM
    data.append(contentsOf: withUnsafeBytes(of: UInt16(channels).littleEndian) { Array($0) })
    data.append(contentsOf: withUnsafeBytes(of: UInt32(sampleRate).littleEndian) { Array($0) })
    data.append(contentsOf: withUnsafeBytes(of: UInt32(sampleRate * channels * 2).littleEndian) { Array($0) })
    data.append(contentsOf: withUnsafeBytes(of: UInt16(channels * 2).littleEndian) { Array($0) })
    data.append(contentsOf: withUnsafeBytes(of: UInt16(16).littleEndian) { Array($0) }) // bits per sample

    // data chunk
    data.append(contentsOf: "data".utf8)
    data.append(contentsOf: withUnsafeBytes(of: UInt32(dataSize).littleEndian) { Array($0) })
    for s in samples {
        data.append(contentsOf: withUnsafeBytes(of: s.littleEndian) { Array($0) })
    }
    return data
}

func sfxStart() -> Data {
    // Two ascending tones (D5 → A5)
    let tone1 = generateTone(frequencies: [(587, 1.0), (1174, 0.2)], duration: 0.07, amplitude: 0.05)
    let tone2 = generateTone(frequencies: [(880, 1.0), (1760, 0.2)], duration: 0.07, amplitude: 0.06)
    // Combine with gap
    let sr = 44100
    let gap = [Int16](repeating: 0, count: Int(Double(sr) * 0.04))
    // Extract PCM from tone1 and tone2, combine, re-wrap
    return combineSounds([tone1, makeWAVData(samples: gap, sampleRate: sr), tone2])
}

func sfxStop() -> Data {
    generateTone(frequencies: [(880, 0.7), (698, 0.5)], duration: 0.12, amplitude: 0.05)
}

func sfxDone() -> Data {
    let tone1 = generateTone(frequencies: [(784, 1.0), (2352, 0.15)], duration: 0.10, amplitude: 0.05)
    let tone2 = generateTone(frequencies: [(1047, 1.0), (3141, 0.12)], duration: 0.18, amplitude: 0.06)
    return combineSounds([tone1, tone2])
}

func sfxError() -> Data {
    let sr = 44100
    let tone = generateTone(frequencies: [(330, 1.0)], duration: 0.08, amplitude: 0.05)
    let gap = [Int16](repeating: 0, count: Int(Double(sr) * 0.06))
    return combineSounds([tone, makeWAVData(samples: gap, sampleRate: sr), tone])
}

func combineSounds(_ wavDatas: [Data]) -> Data {
    // Extract PCM from each WAV, concatenate, re-wrap
    var allSamples = [Int16]()
    for wav in wavDatas {
        // Skip 44-byte WAV header
        if wav.count > 44 {
            let pcmData = wav.subdata(in: 44..<wav.count)
            pcmData.withUnsafeBytes { ptr in
                let bound = ptr.bindMemory(to: Int16.self)
                allSamples.append(contentsOf: bound)
            }
        }
    }
    return makeWAVData(samples: allSamples, sampleRate: 44100)
}

var currentSound: NSSound?
private let soundLock = NSLock()

func playSound(_ wavData: Data) {
    DispatchQueue.global(qos: .userInteractive).async {
        let sound = NSSound(data: wavData)
        sound?.play()
        soundLock.lock()
        currentSound = sound // prevent dealloc
        soundLock.unlock()
    }
}

// MARK: - Audio Input Check

/// Check if a real audio input device (microphone) is available.
/// Filters out virtual audio devices (Zoom, BlackHole, Soundflower, etc.)
/// that can't actually capture microphone audio.
func hasPhysicalAudioInput() -> Bool {
    let devices = AVCaptureDevice.DiscoverySession(
        deviceTypes: [.microphone, .external],
        mediaType: .audio,
        position: .unspecified
    ).devices

    // Filter out known virtual audio devices
    let virtualKeywords = ["zoom", "blackhole", "soundflower", "loopback",
                           "virtual", "aggregate", "multi-output"]
    let physical = devices.filter { dev in
        let name = dev.localizedName.lowercased()
        return !virtualKeywords.contains(where: { name.contains($0) })
    }

    let allNames = devices.map { $0.localizedName }
    let physicalNames = physical.map { $0.localizedName }
    log("🎤 Audio input devices: \(allNames), physical: \(physicalNames)")

    if physical.isEmpty {
        log("❌ No physical microphone found (only virtual: \(allNames))")
        return false
    }
    return true
}

// MARK: - Audio Recording

class AudioRecorder {
    private var engine: AVAudioEngine?
    private var converter: AVAudioConverter?
    private(set) var frames: [Data] = []
    private let lock = NSLock()
    var isRecording = false
    var noMicHandler: (() -> Void)?
    private var configObserver: NSObjectProtocol?
    // Serial queue for all AVAudioEngine operations — prevents concurrent installTap/removeTap crashes
    let audioQueue = DispatchQueue(label: "com.xiabb.audio")

    func start() {
        guard !isRecording else { return }

        // Check for physical microphone BEFORE touching AVAudioEngine
        guard hasPhysicalAudioInput() else {
            log("❌ No microphone connected. Please connect a mic and try again.")
            noMicHandler?()
            return
        }

        frames = []
        isRecording = true

        let engine = AVAudioEngine()
        self.engine = engine

        // Watch for audio config changes (mic disconnected/changed)
        configObserver = NotificationCenter.default.addObserver(
            forName: .AVAudioEngineConfigurationChange, object: engine, queue: nil
        ) { [weak self] _ in
            log("⚠️ Audio config changed (mic disconnected?)")
            guard let self = self, self.isRecording else { return }
            // Try to restart engine with new config
            do {
                try self.engine?.start()
                log("  Audio engine restarted after config change")
            } catch {
                log("  ❌ Audio engine restart failed: \(error)")
                self.isRecording = false
            }
        }

        let inputNode = engine.inputNode
        let hwFormat = inputNode.outputFormat(forBus: 0)

        // Validate hardware format
        guard hwFormat.sampleRate > 0 && hwFormat.channelCount > 0 else {
            log("❌ Invalid audio input format (no mic?): \(hwFormat)")
            isRecording = false
            cleanup()
            return
        }

        guard let targetFormat = AVAudioFormat(commonFormat: .pcmFormatInt16, sampleRate: SAMPLE_RATE, channels: 1, interleaved: true) else {
            log("❌ Cannot create target audio format")
            isRecording = false
            cleanup()
            return
        }

        guard let converter = AVAudioConverter(from: hwFormat, to: targetFormat) else {
            log("❌ Cannot create audio converter")
            isRecording = false
            cleanup()
            return
        }
        self.converter = converter

        let chunkSize: AVAudioFrameCount = AVAudioFrameCount(hwFormat.sampleRate * 0.1)

        // Safety: remove any existing tap before installing a new one
        inputNode.removeTap(onBus: 0)

        inputNode.installTap(onBus: 0, bufferSize: chunkSize, format: hwFormat) { [weak self] buffer, _ in
            guard let self = self, self.isRecording else { return }

            let ratio = SAMPLE_RATE / hwFormat.sampleRate
            let outputFrameCount = AVAudioFrameCount(Double(buffer.frameLength) * ratio)
            guard let outputBuffer = AVAudioPCMBuffer(pcmFormat: targetFormat, frameCapacity: outputFrameCount) else { return }

            var error: NSError?
            let status = converter.convert(to: outputBuffer, error: &error) { inNumPackets, outStatus in
                outStatus.pointee = .haveData
                return buffer
            }

            if let error = error {
                log("⚠️ Audio convert error: \(error.localizedDescription)")
                return
            }

            if status == .haveData || status == .endOfStream, outputBuffer.frameLength > 0 {
                let byteCount = Int(outputBuffer.frameLength) * Int(targetFormat.streamDescription.pointee.mBytesPerFrame)
                let data = Data(bytes: outputBuffer.int16ChannelData![0], count: byteCount)
                self.lock.lock()
                self.frames.append(data)
                self.lock.unlock()
            }
        }

        engine.prepare()
        do {
            try engine.start()
            log("🎙 Audio engine started (hw: \(hwFormat.sampleRate)Hz → 16000Hz)")
        } catch {
            log("❌ Audio engine start failed: \(error)")
            isRecording = false
            cleanup()
        }
    }

    private func cleanup() {
        if let o = configObserver { NotificationCenter.default.removeObserver(o) }
        configObserver = nil
    }

    func stop() -> [Data] {
        isRecording = false
        engine?.inputNode.removeTap(onBus: 0)
        engine?.stop()
        engine = nil
        converter = nil
        cleanup()
        lock.lock()
        let result = frames
        lock.unlock()
        print("🎙 Recording stopped (\(result.count) chunks)")
        return result
    }

    func getFramesSoFar() -> [Data] {
        lock.lock()
        let result = frames
        lock.unlock()
        return result
    }
}

// MARK: - WAV Encoder (for Gemini API)

func encodeToWAV(frames: [Data]) -> (Data, Double) {
    var allBytes = Data()
    for f in frames { allBytes.append(f) }
    let numSamples = allBytes.count / 2
    let duration = Double(numSamples) / SAMPLE_RATE

    var wav = Data()
    let dataSize = allBytes.count
    let fileSize = 36 + dataSize

    wav.append(contentsOf: "RIFF".utf8)
    wav.append(contentsOf: withUnsafeBytes(of: UInt32(fileSize).littleEndian) { Array($0) })
    wav.append(contentsOf: "WAVE".utf8)
    wav.append(contentsOf: "fmt ".utf8)
    wav.append(contentsOf: withUnsafeBytes(of: UInt32(16).littleEndian) { Array($0) })
    wav.append(contentsOf: withUnsafeBytes(of: UInt16(1).littleEndian) { Array($0) })
    wav.append(contentsOf: withUnsafeBytes(of: UInt16(1).littleEndian) { Array($0) })
    wav.append(contentsOf: withUnsafeBytes(of: UInt32(Int(SAMPLE_RATE)).littleEndian) { Array($0) })
    wav.append(contentsOf: withUnsafeBytes(of: UInt32(Int(SAMPLE_RATE) * 2).littleEndian) { Array($0) })
    wav.append(contentsOf: withUnsafeBytes(of: UInt16(2).littleEndian) { Array($0) })
    wav.append(contentsOf: withUnsafeBytes(of: UInt16(16).littleEndian) { Array($0) })
    wav.append(contentsOf: "data".utf8)
    wav.append(contentsOf: withUnsafeBytes(of: UInt32(dataSize).littleEndian) { Array($0) })
    wav.append(allBytes)

    return (wav, duration)
}

// MARK: - Gemini REST API

func transcribeREST(wavData: Data, mode: SmartMode = .dictation, completion: @escaping (Result<String, Error>) -> Void) {
    let b64 = wavData.base64EncodedString()
    guard let url = URL(string: "https://generativelanguage.googleapis.com/v1beta/models/\(MODEL_REST):generateContent") else {
        completion(.failure(NSError(domain: "XiaBB", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid URL"])))
        return
    }

    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.setValue(apiKey, forHTTPHeaderField: "x-goog-api-key")
    request.timeoutInterval = 30

    // Choose prompt based on smart mode, always include dictionary
    let promptText: String
    if mode == .dictation {
        promptText = buildPrompt()
    } else {
        var base = SMART_MODE_PROMPTS[mode] ?? buildPrompt()
        let words = loadDictionary()
        if !words.isEmpty {
            let wordList = words.map { "\"\($0)\"" }.joined(separator: ", ")
            base += "\n- IMPORTANT: These proper nouns/terms must be kept EXACTLY as written (case-sensitive, do NOT translate or alter): \(wordList)."
        }
        promptText = base
    }

    let body: [String: Any] = [
        "contents": [["parts": [
            ["text": promptText],
            ["inline_data": ["mime_type": "audio/wav", "data": b64]]
        ]]],
        "generationConfig": ["temperature": mode == .dictation ? 0.0 : 0.3, "maxOutputTokens": 4096]
    ]

    request.httpBody = try? JSONSerialization.data(withJSONObject: body)

    URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            log("[REST] Network error: \(error)")
            completion(.failure(error))
            return
        }
        guard let data = data else {
            completion(.failure(NSError(domain: "XiaBB", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
            return
        }

        // Log the raw response for debugging
        if let httpResp = response as? HTTPURLResponse {
            log("[REST] HTTP \(httpResp.statusCode), \(data.count) bytes")
        }

        do {
            guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
                let raw = String(data: data.prefix(500), encoding: .utf8) ?? "binary"
                log("[REST] Not a JSON object: \(raw)")
                completion(.failure(NSError(domain: "XiaBB", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])))
                return
            }

            // Check for error response
            if let error = json["error"] as? [String: Any],
               let message = error["message"] as? String {
                log("[REST] API error: \(message)")
                completion(.failure(NSError(domain: "Gemini", code: -1, userInfo: [NSLocalizedDescriptionKey: message])))
                return
            }

            // Parse candidates
            guard let candidates = json["candidates"] as? [[String: Any]],
                  let content = candidates.first?["content"] as? [String: Any],
                  let parts = content["parts"] as? [[String: Any]],
                  let text = parts.first?["text"] as? String else {
                // Check if this is a valid response with no text (e.g. silence)
                if let candidates = json["candidates"] as? [[String: Any]],
                   let content = candidates.first?["content"] as? [String: Any],
                   content["parts"] == nil {
                    log("[REST] No text in response — likely silence or unintelligible audio")
                    completion(.failure(NSError(domain: "XiaBB", code: -2, userInfo: [NSLocalizedDescriptionKey: "No speech detected"])))
                    return
                }
                let raw = String(data: data.prefix(500), encoding: .utf8) ?? "binary"
                log("[REST] Unexpected structure: \(raw)")
                completion(.failure(NSError(domain: "XiaBB", code: -1, userInfo: [NSLocalizedDescriptionKey: "Unexpected response format"])))
                return
            }

            let cleaned = t2s(text.trimmingCharacters(in: .whitespacesAndNewlines)
                .replacingOccurrences(of: "\n", with: " "))
            log("[REST] ✅ Transcribed: \(cleaned.prefix(100))")
            completion(.success(cleaned))
        } catch {
            log("[REST] JSON parse error: \(error)")
            completion(.failure(error))
        }
    }.resume()
}

// MARK: - Gemini Live WebSocket

class LiveSession: NSObject, URLSessionWebSocketDelegate {
    private var webSocket: URLSessionWebSocketTask?
    private var urlSession: URLSession?
    private var liveText = ""
    private var onTextUpdate: ((String) -> Void)?
    private var isActive = false
    private var chunksSent = 0

    func start(onTextUpdate: @escaping (String) -> Void) {
        self.onTextUpdate = onTextUpdate
        self.liveText = ""
        self.isActive = true
        self.chunksSent = 0

        let urlStr = "\(WS_URL_BASE)?key=\(apiKey)"
        guard let url = URL(string: urlStr) else {
            log("[live] Invalid WebSocket URL")
            return
        }

        log("[live] Connecting to WebSocket...")
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        urlSession = URLSession(configuration: config, delegate: self, delegateQueue: nil)
        webSocket = urlSession?.webSocketTask(with: url)
        webSocket?.resume()

        // Send setup message — include custom dictionary for accurate real-time transcription
        let dictWords = loadDictionary()
        let dictHint = dictWords.isEmpty ? "" : " These proper nouns must be transcribed exactly: \(dictWords.joined(separator: ", "))."
        let setup: [String: Any] = [
            "setup": [
                "model": "models/\(MODEL_LIVE)",
                "generationConfig": ["responseModalities": ["AUDIO"]],
                "systemInstruction": ["parts": [["text": "Listen and acknowledge briefly. ALL Chinese must be Simplified (简体中文).\(dictHint)"]]],
                "inputAudioTranscription": [:] as [String: Any],
            ]
        ]

        guard let setupData = try? JSONSerialization.data(withJSONObject: setup),
              let setupStr = String(data: setupData, encoding: .utf8) else {
            log("[live] Failed to serialize setup message")
            return
        }

        webSocket?.send(.string(setupStr)) { [weak self] error in
            if let error = error {
                if self?.isActive == true {
                    log("[live] Setup send error: \(error)")
                }
                return
            }
            log("[live] Setup message sent, waiting for response...")
            self?.receiveSetupResponse()
        }
    }

    // URLSessionWebSocketDelegate
    func urlSession(_ session: URLSession, webSocketTask: URLSessionWebSocketTask, didOpenWithProtocol protocol: String?) {
        log("[live] WebSocket opened (protocol: \(`protocol` ?? "none"))")
    }

    func urlSession(_ session: URLSession, webSocketTask: URLSessionWebSocketTask, didCloseWith closeCode: URLSessionWebSocketTask.CloseCode, reason: Data?) {
        log("[live] WebSocket closed (code: \(closeCode.rawValue))")
    }

    private func receiveSetupResponse() {
        webSocket?.receive { [weak self] result in
            switch result {
            case .success(let msg):
                switch msg {
                case .string(let text):
                    if text.contains("setupComplete") {
                        log("[live] ✅ Setup complete (string)")
                        self?.startReceiving()
                    } else {
                        log("[live] Unexpected setup response: \(text.prefix(300))")
                        self?.stop()
                    }
                case .data(let data):
                    // Log raw bytes to understand format
                    let hex = data.prefix(60).map { String(format: "%02x", $0) }.joined(separator: " ")
                    log("[live] Setup binary (\(data.count) bytes): \(hex)")
                    if let text = String(data: data, encoding: .utf8) {
                        log("[live] Setup as UTF-8: \(text.prefix(200))")
                        if text.contains("setupComplete") {
                            log("[live] ✅ Setup complete (from binary)")
                            self?.startReceiving()
                        } else {
                            // Maybe it's JSON with setup info, continue anyway
                            log("[live] ⚠️ No setupComplete in binary, starting anyway")
                            self?.startReceiving()
                        }
                    } else {
                        // Likely protobuf — start receiving anyway
                        log("[live] ⚠️ Non-UTF8 binary, assuming setup complete")
                        self?.startReceiving()
                    }
                @unknown default:
                    break
                }
            case .failure(let error):
                log("[live] Setup receive error: \(error)")
            }
        }
    }

    private var msgCount = 0

    private func startReceiving() {
        guard isActive else { return }
        webSocket?.receive { [weak self] result in
            guard let self = self, self.isActive else { return }
            switch result {
            case .success(let msg):
                self.msgCount += 1
                switch msg {
                case .string(let text):
                    self.handleMessage(text)
                case .data(let data):
                    // Try UTF-8 first
                    if let text = String(data: data, encoding: .utf8) {
                        self.handleMessage(text)
                    } else if self.msgCount <= 10 {
                        let hex = data.prefix(40).map { String(format: "%02x", $0) }.joined(separator: " ")
                        log("[live] Binary msg #\(self.msgCount): \(data.count) bytes — \(hex)...")
                    }
                @unknown default:
                    break
                }
                self.startReceiving() // Continue receiving
            case .failure(let error):
                if self.isActive {
                    log("[live] Receive error: \(error)")
                }
            }
        }
    }

    private func handleMessage(_ jsonStr: String) {
        // Log first few messages to debug
        if msgCount <= 5 {
            log("[live] Msg #\(msgCount): \(jsonStr.prefix(300))")
        }

        guard let data = jsonStr.data(using: .utf8),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            if msgCount <= 5 {
                log("[live] Failed to parse JSON for msg #\(msgCount)")
            }
            return
        }

        // Check for inputTranscription in serverContent
        if let sc = json["serverContent"] as? [String: Any] {
            if let it = sc["inputTranscription"] as? [String: Any],
               let chunk = it["text"] as? String, !chunk.isEmpty {
                liveText += chunk
                let display = t2s(liveText)
                log("[live] 📝 Chunk: \"\(chunk)\" → total: \"\(display.suffix(60))\"")
                DispatchQueue.main.async { [weak self] in
                    self?.onTextUpdate?(display)
                }
            }

            // Also check for modelTurn (the model's audio response) — we can ignore these
            if sc["modelTurn"] != nil {
                if msgCount <= 5 {
                    log("[live] Got modelTurn (ignored)")
                }
            }

            // Check turnComplete
            if let tc = sc["turnComplete"] as? Bool, tc {
                log("[live] Turn complete")
            }
        }
    }

    var currentText: String { return t2s(liveText) }

    func sendAudio(_ pcmData: Data) {
        guard isActive, let ws = webSocket else { return }
        let b64 = pcmData.base64EncodedString()
        let msg: [String: Any] = [
            "realtimeInput": [
                "mediaChunks": [[
                    "mimeType": "audio/pcm;rate=16000",
                    "data": b64
                ]]
            ]
        ]
        guard let data = try? JSONSerialization.data(withJSONObject: msg),
              let str = String(data: data, encoding: .utf8) else { return }
        ws.send(.string(str)) { [weak self] error in
            if let error = error {
                // Suppress "cancelled" errors during teardown to avoid log spam
                if self?.isActive == true {
                    log("[live] Audio send error: \(error)")
                }
            } else {
                self?.chunksSent += 1
            }
        }
    }

    func stop() {
        let sent = chunksSent
        isActive = false
        webSocket?.cancel(with: .goingAway, reason: nil)
        webSocket = nil
        urlSession?.invalidateAndCancel()
        urlSession = nil
        log("[live] Stopped — \(liveText.count) chars transcribed, \(sent) chunks sent")
    }
}

// MARK: - Onboarding Window (WKWebView-based)

func OB(_ key: String) -> String {
    // minimal shim for the menu item title used in XiaBBApp
    let zh: [String: String] = ["perm_menu": "设置向导..."]
    let en: [String: String] = ["perm_menu": "Setup Wizard..."]
    return (currentLang == "zh" ? zh[key] : en[key]) ?? key
}

// MARK: - Onboarding HTML

private let onboardingHTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XiaBB Setup</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --accent: #EA6962;
    --accent-light: #fef2f0;
    --accent-dark: #d65d57;
    --green: #22c55e;
    --green-light: #f0fdf4;
    --red: #EA6962;
    --red-light: #fef2f0;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-700: #374151;
    --gray-900: #111827;
  }

  body {
    font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    background: #ffffff;
    color: var(--gray-900);
    height: 550px;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
    user-select: none;
    -webkit-user-select: none;
  }

  .step {
    display: none;
    position: absolute;
    inset: 0;
    flex-direction: column;
    opacity: 0;
    transition: opacity 0.25s ease;
  }
  .step.active { display: flex; opacity: 1; }
  .step.fade-in { opacity: 1; }

  .step-bar {
    display: flex; align-items: center; justify-content: center;
    gap: 8px; padding: 18px 0 0; min-height: 48px;
  }
  .step-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--gray-200); transition: all 0.3s ease;
  }
  .step-dot.done   { background: var(--accent); }
  .step-dot.active { background: var(--accent); width: 20px; border-radius: 4px; }

  .step-content {
    flex: 1; overflow-y: auto; padding: 0 40px 16px;
    display: flex; flex-direction: column;
  }
  .step-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 32px 20px; border-top: 1px solid var(--gray-200);
    background: #ffffff; min-height: 64px;
  }

  h1 { font-size: 26px; font-weight: 700; line-height: 1.2; }
  h2 { font-size: 20px; font-weight: 600; line-height: 1.3; margin-bottom: 8px; }
  p  { font-size: 14px; color: var(--gray-500); line-height: 1.6; }
  .hint { font-size: 12px; color: var(--gray-400); margin-top: 6px; }

  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    padding: 9px 20px; border-radius: 10px; font-size: 14px; font-weight: 500;
    border: none; cursor: pointer; transition: all 0.15s ease; outline: none;
    -webkit-app-region: no-drag;
  }
  .btn-primary { background: var(--accent); color: #fff; font-weight: 600; box-shadow: 0 1px 3px rgba(234,105,98,0.3); }
  .btn-primary:hover { background: var(--accent-dark); }
  .btn-primary:active { transform: scale(0.97); }
  .btn-primary:disabled { background: var(--gray-200); color: var(--gray-400); box-shadow: none; cursor: not-allowed; }
  .btn-secondary { background: var(--gray-100); color: var(--gray-700); border: 1px solid var(--gray-200); }
  .btn-secondary:hover { background: var(--gray-200); }
  .btn-ghost { background: transparent; color: var(--gray-500); font-size: 13px; padding: 6px 12px; }
  .btn-ghost:hover { color: var(--gray-700); }
  .btn-large { padding: 13px 36px; font-size: 16px; font-weight: 600; border-radius: 12px; min-width: 200px; }

  .card {
    background: var(--gray-50); border: 1px solid var(--gray-200);
    border-radius: 12px; padding: 16px 20px; margin: 8px 0;
  }
  .card-row { display: flex; align-items: center; gap: 14px; }
  .card-icon { font-size: 22px; flex-shrink: 0; }
  .card-body { flex: 1; }
  .card-title { font-size: 14px; font-weight: 500; margin-bottom: 2px; }
  .card-desc  { font-size: 12px; color: var(--gray-500); }
  .card-action { flex-shrink: 0; }

  .badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500;
  }
  .badge-success { background: var(--green-light); color: #15803d; }
  .badge-pending { background: var(--gray-100);    color: var(--gray-500); }
  .badge-error   { background: var(--red-light);   color: #b91c1c; }
  .badge-loading { background: var(--accent-light);  color: var(--accent-dark); }

  .input-row { display: flex; gap: 8px; margin: 12px 0; }
  .input-field {
    flex: 1; padding: 9px 14px; border: 1.5px solid var(--gray-200);
    border-radius: 10px; font-size: 13px; font-family: "SF Mono", monospace;
    color: var(--gray-900); background: #ffffff; outline: none;
    transition: border-color 0.15s; -webkit-app-region: no-drag;
  }
  .input-field:focus { border-color: var(--accent); }
  .input-field.error   { border-color: var(--red); }
  .input-field.success { border-color: var(--green); }

  .status-row { min-height: 24px; margin-top: 6px; display: flex; align-items: center; gap: 8px; }

  .mic-viz {
    display: flex; align-items: flex-end; justify-content: center;
    gap: 3px; height: 56px; margin: 16px 0;
  }
  .mic-bar {
    width: 10px; background: var(--gray-200); border-radius: 3px;
    min-height: 4px; transition: height 0.06s ease-out, background 0.06s ease-out;
  }
  .mic-bar.active { background: var(--accent); }

  .app-icon {
    display: inline-flex; align-items: center; justify-content: center;
    background: #f9fafb; border-radius: 22%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.06);
    line-height: 1; flex-shrink: 0;
  }
  .app-icon-lg { width: 80px; height: 80px; font-size: 48px; border-radius: 18px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.14), 0 1px 4px rgba(0,0,0,0.10); }
  .app-icon-sm { width: 32px; height: 32px; font-size: 20px; border-radius: 7px; }
  .app-icon svg { width: 65%; height: 65%; display: block; }

  .step-header {
    display: flex; align-items: center; gap: 10px;
    padding: 14px 20px 0;
  }

  .globe-key {
    width: 72px; height: 72px; border-radius: 16px;
    background: var(--gray-100); border: 2px solid var(--gray-200);
    display: flex; align-items: center; justify-content: center;
    font-size: 36px; margin: 20px auto 16px; transition: all 0.15s ease;
  }
  .globe-key.pressed { background: #fdf0ee; border-color: var(--accent); transform: scale(1.10); box-shadow: 0 0 0 4px rgba(234,105,98,0.2); }
  .globe-key.detected { background: #fdf0ee; border-color: var(--accent); transform: scale(1.05); }

  /* Step 5 mock window */
  .mock-window {
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    overflow: hidden;
  }
  .mock-titlebar {
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .mock-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .mock-body {
    padding: 16px;
    min-height: 150px;
    font-size: 15px;
    line-height: 1.6;
    color: #1f2937;
  }

  @keyframes globePulse {
    0%   { box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
    70%  { box-shadow: 0 0 0 10px rgba(34,197,94,0); }
    100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
  }
  /* pulse removed — just two states: default (gray) and pressed (blue) */

  .checklist { list-style: none; margin: 16px 0; }
  .checklist li {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid var(--gray-100); font-size: 14px;
  }
  .checklist li:last-child { border-bottom: none; }
  .check-icon { font-size: 18px; }
  .check-label { flex: 1; }
  .check-status { font-size: 12px; color: var(--gray-400); }

  .divider { border: none; border-top: 1px solid var(--gray-100); margin: 12px 0; }

  .link-btn {
    color: var(--accent); font-size: 13px; cursor: pointer;
    text-decoration: none; display: inline-flex; align-items: center; gap: 4px;
    background: none; border: none; padding: 0; font-family: inherit;
    -webkit-app-region: no-drag;
  }
  .link-btn:hover { text-decoration: underline; }

  #step-0 { justify-content: center; text-align: center; }
  .welcome-content {
    padding: 24px 40px; display: flex; flex-direction: column; align-items: center;
  }
  .app-name { font-size: 22px; font-weight: 600; margin-bottom: 4px; color: var(--gray-500); }
  .app-brand { font-size: 52px; font-weight: 800; margin-bottom: 12px; color: var(--accent); font-style: italic; letter-spacing: -1px; }
  .app-desc { font-size: 15px; color: var(--gray-500); line-height: 1.7; max-width: 380px; font-style: italic; }

  /* Illustration placeholders */
  .illust {
    display: flex; align-items: center; justify-content: center;
    border-radius: 16px; overflow: hidden;
  }
  .illust-welcome {
    width: 180px; height: 180px; margin: 0 auto 8px;
    background: linear-gradient(135deg, #fef2f0 0%, #fff5f4 100%);
    border: 2px dashed var(--accent);
    opacity: 0.9;
  }
  .illust-float {
    position: absolute; opacity: 0.12; pointer-events: none;
  }
  .illust-float svg { width: 100%; height: 100%; }
  .step-illust {
    width: 64px; height: 64px; margin: 0 auto 12px;
    background: #fef2f0; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
  }
  .step-illust svg { width: 36px; height: 36px; opacity: 0.7; }

  /* Sketchy card style for fun */
  .card-sketchy {
    background: var(--gray-50);
    border: 2px solid var(--gray-200);
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
    padding: 16px 20px; margin: 8px 0;
    transition: transform 0.2s ease;
  }
  .card-sketchy:hover { transform: rotate(-0.5deg); }

  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner {
    width: 14px; height: 14px; border: 2px solid var(--gray-200);
    border-top-color: var(--accent); border-radius: 50%;
    animation: spin 0.7s linear infinite; flex-shrink: 0; display: inline-block;
  }

  @keyframes bounceIn {
    0%   { transform: scale(0.85); opacity: 0; }
    60%  { transform: scale(1.05); opacity: 1; }
    100% { transform: scale(1); }
  }
  .bounce-in { animation: bounceIn 0.4s ease; }

  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-thumb { background: var(--gray-200); border-radius: 10px; }
</style>
</head>
<body>

<!-- STEP 0: WELCOME -->
<div class="step active" id="step-0">
  <div class="welcome-content" style="flex:1; justify-content:center;">
    <!-- Lobster illustration placeholder -->
    <div class="illust illust-welcome">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="120" height="120" fill="#EA6962" opacity="0.6"><g transform="translate(0,512) scale(0.1,-0.1)" stroke="none"><path d="M1966 4593 c-52 -19 -61 -29 -47 -51 6 -11 16 -11 47 -3 179 50 341 -76 368 -284 l6 -50 -53 -29 c-123 -70 -241 -239 -254 -369 l-6 -57 150 0 c133 0 152 -2 166 -18 21 -23 22 -46 2 -66 -12 -12 -43 -15 -153 -15 -75 1 -143 0 -149 0 -8 -1 -13 -17 -13 -46 l0 -44 156 -3 c134 -3 158 -5 167 -20 8 -12 8 -24 -1 -42 l-12 -26 -155 0 -155 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -40 0 -40 83 -1 c268 -4 973 4 980 11 5 4 7 20 5 36 l-3 29 -158 5 c-125 4 -160 8 -167 20 -13 20 -12 33 3 53 10 14 36 17 167 19 l155 3 0 40 0 40 -155 3 c-131 2 -157 5 -167 19 -17 22 -16 38 3 57 13 13 42 16 165 16 l149 0 6 24 c3 14 3 34 -1 45 -6 20 -13 21 -155 21 -147 0 -150 0 -165 24 -13 19 -14 29 -5 45 10 20 19 21 165 21 l155 0 0 45 0 45 -145 0 c-132 0 -147 2 -165 20 -11 11 -20 25 -20 30 0 6 9 19 20 30 18 18 33 20 170 20 171 0 161 -7 135 95 -34 128 -117 243 -232 317 l-65 43 5 50 c13 122 81 226 180 274 42 20 58 23 120 18 40 -3 81 -7 92 -9 14 -2 21 3 23 19 3 19 -5 24 -49 37 -66 20 -102 20 -165 1 -68 -20 -140 -69 -180 -124 -39 -54 -74 -149 -74 -204 l0 -39 -52 9 c-67 10 -201 10 -253 0 l-41 -8 -11 63 c-15 88 -49 154 -110 216 -88 89 -205 121 -307 85z"/><path d="M1787 2982 c-13 -14 -17 -39 -17 -110 0 -87 1 -92 25 -108 l25 -16 0 -347 c0 -365 5 -410 50 -515 58 -137 181 -267 319 -340 72 -38 197 -76 248 -76 l33 0 0 -273 0 -274 -132 -7 c-198 -9 -394 -35 -468 -59 -56 -19 -65 -25 -65 -46 0 -30 41 -45 170 -66 251 -40 825 -45 1095 -11 142 18 260 50 260 70 0 35 -79 66 -220 85 -99 14 -317 31 -396 31 l-64 0 0 274 0 273 55 7 c290 34 541 271 594 560 7 35 11 196 11 390 0 320 1 332 20 344 18 11 20 23 20 112 0 114 -4 120 -85 120 -81 0 -85 -6 -85 -120 0 -89 2 -101 20 -112 19 -12 20 -23 20 -333 -1 -358 -9 -433 -58 -536 -67 -140 -194 -253 -342 -305 -100 -34 -323 -45 -440 -20 -221 46 -400 216 -455 431 -12 47 -15 128 -15 407 0 320 1 348 18 357 14 8 17 24 17 104 0 117 -6 127 -85 127 -42 0 -61 -5 -73 -18z"/><path d="M2030 2600 c0 -318 1 -345 21 -403 40 -121 116 -218 223 -286 166 -104 344 -115 523 -31 81 37 190 140 231 218 59 112 62 133 62 504 l0 338 -530 0 -530 0 0 -340z"/><path d="M1802 712 c3 -36 5 -38 70 -59 132 -44 282 -57 673 -58 362 0 492 8 655 41 108 23 130 36 130 80 0 31 -3 35 -17 29 -142 -59 -595 -94 -958 -75 -240 12 -409 32 -496 60 l-60 18 3 -36z"/></g></svg>
    </div>
    <div class="app-name" id="s0-title">欢迎使用</div>
    <div class="app-brand" id="s0-brand">虾BB</div>
    <div class="app-desc" id="s0-desc">by Vibe Coders, for Vibe Coders</div>
    <div style="height:20px"></div>
    <button class="btn btn-primary btn-large bounce-in" onclick="startSetup()" id="s0-btn">开始设置</button>
    <div style="height:12px"></div>
    <div class="hint" id="s0-hint">设置只需 2 分钟</div>
  </div>
</div>

<!-- STEP 1: API KEY -->
<div class="step" id="step-1">
  <div class="step-header">
    <div class="app-icon app-icon-sm"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="#000000"><g transform="translate(0,512) scale(0.1,-0.1)" stroke="none"><path d="M1966 4593 c-52 -19 -61 -29 -47 -51 6 -11 16 -11 47 -3 179 50 341 -76 368 -284 l6 -50 -53 -29 c-123 -70 -241 -239 -254 -369 l-6 -57 150 0 c133 0 152 -2 166 -18 21 -23 22 -46 2 -66 -12 -12 -43 -15 -153 -15 -75 1 -143 0 -149 0 -8 -1 -13 -17 -13 -46 l0 -44 156 -3 c134 -3 158 -5 167 -20 8 -12 8 -24 -1 -42 l-12 -26 -155 0 -155 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -40 0 -40 83 -1 c268 -4 973 4 980 11 5 4 7 20 5 36 l-3 29 -158 5 c-125 4 -160 8 -167 20 -13 20 -12 33 3 53 10 14 36 17 167 19 l155 3 0 40 0 40 -155 3 c-131 2 -157 5 -167 19 -17 22 -16 38 3 57 13 13 42 16 165 16 l149 0 6 24 c3 14 3 34 -1 45 -6 20 -13 21 -155 21 -147 0 -150 0 -165 24 -13 19 -14 29 -5 45 10 20 19 21 165 21 l155 0 0 45 0 45 -145 0 c-132 0 -147 2 -165 20 -11 11 -20 25 -20 30 0 6 9 19 20 30 18 18 33 20 170 20 171 0 161 -7 135 95 -34 128 -117 243 -232 317 l-65 43 5 50 c13 122 81 226 180 274 42 20 58 23 120 18 40 -3 81 -7 92 -9 14 -2 21 3 23 19 3 19 -5 24 -49 37 -66 20 -102 20 -165 1 -68 -20 -140 -69 -180 -124 -39 -54 -74 -149 -74 -204 l0 -39 -52 9 c-67 10 -201 10 -253 0 l-41 -8 -11 63 c-15 88 -49 154 -110 216 -88 89 -205 121 -307 85z"/><path d="M1787 2982 c-13 -14 -17 -39 -17 -110 0 -87 1 -92 25 -108 l25 -16 0 -347 c0 -365 5 -410 50 -515 58 -137 181 -267 319 -340 72 -38 197 -76 248 -76 l33 0 0 -273 0 -274 -132 -7 c-198 -9 -394 -35 -468 -59 -56 -19 -65 -25 -65 -46 0 -30 41 -45 170 -66 251 -40 825 -45 1095 -11 142 18 260 50 260 70 0 35 -79 66 -220 85 -99 14 -317 31 -396 31 l-64 0 0 274 0 273 55 7 c290 34 541 271 594 560 7 35 11 196 11 390 0 320 1 332 20 344 18 11 20 23 20 112 0 114 -4 120 -85 120 -81 0 -85 -6 -85 -120 0 -89 2 -101 20 -112 19 -12 20 -23 20 -333 -1 -358 -9 -433 -58 -536 -67 -140 -194 -253 -342 -305 -100 -34 -323 -45 -440 -20 -221 46 -400 216 -455 431 -12 47 -15 128 -15 407 0 320 1 348 18 357 14 8 17 24 17 104 0 117 -6 127 -85 127 -42 0 -61 -5 -73 -18z"/><path d="M2030 2600 c0 -318 1 -345 21 -403 40 -121 116 -218 223 -286 166 -104 344 -115 523 -31 81 37 190 140 231 218 59 112 62 133 62 504 l0 338 -530 0 -530 0 0 -340z"/><path d="M1802 712 c3 -36 5 -38 70 -59 132 -44 282 -57 673 -58 362 0 492 8 655 41 108 23 130 36 130 80 0 31 -3 35 -17 29 -142 -59 -595 -94 -958 -75 -240 12 -409 32 -496 60 l-60 18 3 -36z"/></g></svg></div>
    <div class="step-bar" id="dots-1" style="flex:1; padding:0; min-height:unset;"></div>
  </div>
  <div class="step-content" style="padding-top:10px;">
    <h2 id="s1-title">配置 API Key</h2>
    <p id="s1-desc">虾BB 使用 Google Gemini 进行语音识别。免费额度：每天 250 次，无需信用卡。</p>
    <div style="height:12px"></div>

    <div class="card" id="s1-existing" style="display:none">
      <div class="card-row">
        <div class="card-icon">🔑</div>
        <div class="card-body">
          <div class="card-title" id="s1-existing-label">已配置 Key</div>
          <div class="card-desc" id="s1-existing-masked"></div>
        </div>
        <div class="card-action">
          <button class="btn btn-secondary" style="font-size:12px;padding:6px 12px" onclick="changeKey()" id="s1-change-btn">更换</button>
        </div>
      </div>
    </div>

    <div id="s1-input-area">
      <div class="input-row">
        <input type="text" class="input-field" id="apiKeyInput" spellcheck="false"
               placeholder="粘贴 API Key..." oninput="onKeyInput()" onkeydown="onKeyDown(event)">
        <button class="btn btn-primary" id="validateBtn" onclick="doValidate()">验证</button>
      </div>
      <div class="status-row" id="keyStatusRow">
        <span id="keyStatusIcon"></span>
        <span id="keyStatusText"></span>
        <div id="keyStatusSpinner" class="spinner" style="display:none"></div>
      </div>
    </div>

    <div style="height:8px"></div>
    <button class="link-btn" onclick="openAIStudio()">前往 Google AI Studio 获取免费 Key →</button>
    <div class="hint" id="s1-hint">免费版每天 250 次请求</div>
  </div>
  <div class="step-nav">
    <button class="btn btn-ghost" onclick="goBack()" id="nav-back-1">返回</button>
    <button class="btn btn-primary" onclick="goNext()" id="nav-next-1" disabled>下一步</button>
  </div>
</div>

<!-- STEP 2: MICROPHONE -->
<div class="step" id="step-2">
  <div class="step-header">
    <div class="app-icon app-icon-sm"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="#000000"><g transform="translate(0,512) scale(0.1,-0.1)" stroke="none"><path d="M1966 4593 c-52 -19 -61 -29 -47 -51 6 -11 16 -11 47 -3 179 50 341 -76 368 -284 l6 -50 -53 -29 c-123 -70 -241 -239 -254 -369 l-6 -57 150 0 c133 0 152 -2 166 -18 21 -23 22 -46 2 -66 -12 -12 -43 -15 -153 -15 -75 1 -143 0 -149 0 -8 -1 -13 -17 -13 -46 l0 -44 156 -3 c134 -3 158 -5 167 -20 8 -12 8 -24 -1 -42 l-12 -26 -155 0 -155 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -40 0 -40 83 -1 c268 -4 973 4 980 11 5 4 7 20 5 36 l-3 29 -158 5 c-125 4 -160 8 -167 20 -13 20 -12 33 3 53 10 14 36 17 167 19 l155 3 0 40 0 40 -155 3 c-131 2 -157 5 -167 19 -17 22 -16 38 3 57 13 13 42 16 165 16 l149 0 6 24 c3 14 3 34 -1 45 -6 20 -13 21 -155 21 -147 0 -150 0 -165 24 -13 19 -14 29 -5 45 10 20 19 21 165 21 l155 0 0 45 0 45 -145 0 c-132 0 -147 2 -165 20 -11 11 -20 25 -20 30 0 6 9 19 20 30 18 18 33 20 170 20 171 0 161 -7 135 95 -34 128 -117 243 -232 317 l-65 43 5 50 c13 122 81 226 180 274 42 20 58 23 120 18 40 -3 81 -7 92 -9 14 -2 21 3 23 19 3 19 -5 24 -49 37 -66 20 -102 20 -165 1 -68 -20 -140 -69 -180 -124 -39 -54 -74 -149 -74 -204 l0 -39 -52 9 c-67 10 -201 10 -253 0 l-41 -8 -11 63 c-15 88 -49 154 -110 216 -88 89 -205 121 -307 85z"/><path d="M1787 2982 c-13 -14 -17 -39 -17 -110 0 -87 1 -92 25 -108 l25 -16 0 -347 c0 -365 5 -410 50 -515 58 -137 181 -267 319 -340 72 -38 197 -76 248 -76 l33 0 0 -273 0 -274 -132 -7 c-198 -9 -394 -35 -468 -59 -56 -19 -65 -25 -65 -46 0 -30 41 -45 170 -66 251 -40 825 -45 1095 -11 142 18 260 50 260 70 0 35 -79 66 -220 85 -99 14 -317 31 -396 31 l-64 0 0 274 0 273 55 7 c290 34 541 271 594 560 7 35 11 196 11 390 0 320 1 332 20 344 18 11 20 23 20 112 0 114 -4 120 -85 120 -81 0 -85 -6 -85 -120 0 -89 2 -101 20 -112 19 -12 20 -23 20 -333 -1 -358 -9 -433 -58 -536 -67 -140 -194 -253 -342 -305 -100 -34 -323 -45 -440 -20 -221 46 -400 216 -455 431 -12 47 -15 128 -15 407 0 320 1 348 18 357 14 8 17 24 17 104 0 117 -6 127 -85 127 -42 0 -61 -5 -73 -18z"/><path d="M2030 2600 c0 -318 1 -345 21 -403 40 -121 116 -218 223 -286 166 -104 344 -115 523 -31 81 37 190 140 231 218 59 112 62 133 62 504 l0 338 -530 0 -530 0 0 -340z"/><path d="M1802 712 c3 -36 5 -38 70 -59 132 -44 282 -57 673 -58 362 0 492 8 655 41 108 23 130 36 130 80 0 31 -3 35 -17 29 -142 -59 -595 -94 -958 -75 -240 12 -409 32 -496 60 l-60 18 3 -36z"/></g></svg></div>
    <div class="step-bar" id="dots-2" style="flex:1; padding:0; min-height:unset;"></div>
  </div>
  <div class="step-content" style="padding-top:10px;">
    <h2 id="s2-title">麦克风权限</h2>
    <p id="s2-desc">虾BB 需要麦克风权限来录制你的声音。</p>
    <div style="height:14px"></div>

    <div class="card">
      <div class="card-row">
        <div class="card-icon">🎙</div>
        <div class="card-body">
          <div class="card-title" id="s2-card-title">麦克风</div>
          <div class="card-desc" id="s2-status-desc">等待授权...</div>
        </div>
        <div class="card-action" id="s2-grant-area">
          <button class="btn btn-primary" style="font-size:13px" onclick="doRequestMic()" id="s2-grant-btn">允许</button>
        </div>
      </div>
    </div>

    <div class="mic-viz" id="micViz">
      <div class="mic-bar" id="bar0"  style="height:4px"></div>
      <div class="mic-bar" id="bar1"  style="height:4px"></div>
      <div class="mic-bar" id="bar2"  style="height:4px"></div>
      <div class="mic-bar" id="bar3"  style="height:4px"></div>
      <div class="mic-bar" id="bar4"  style="height:4px"></div>
      <div class="mic-bar" id="bar5"  style="height:4px"></div>
      <div class="mic-bar" id="bar6"  style="height:4px"></div>
      <div class="mic-bar" id="bar7"  style="height:4px"></div>
      <div class="mic-bar" id="bar8"  style="height:4px"></div>
      <div class="mic-bar" id="bar9"  style="height:4px"></div>
      <div class="mic-bar" id="bar10" style="height:4px"></div>
      <div class="mic-bar" id="bar11" style="height:4px"></div>
    </div>

    <p style="text-align:center; font-size:13px; color:var(--gray-500)" id="s2-q">说话时你能看到音量条在动吗？</p>
    <div style="display:flex; gap:10px; justify-content:center; margin-top:12px" id="s2-confirm-row">
      <button class="btn btn-primary" onclick="micYes()" id="s2-yes-btn">可以，继续</button>
      <button class="btn btn-secondary" onclick="micNo()" id="s2-no-btn">不行，换麦克风</button>
    </div>
  </div>
  <div class="step-nav">
    <button class="btn btn-ghost" onclick="goBack()" id="nav-back-2">返回</button>
    <button class="btn btn-primary" onclick="goNext()" id="nav-next-2" disabled>下一步</button>
  </div>
</div>

<!-- STEP 3: ACCESSIBILITY -->
<div class="step" id="step-3">
  <div class="step-header">
    <div class="app-icon app-icon-sm"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="#000000"><g transform="translate(0,512) scale(0.1,-0.1)" stroke="none"><path d="M1966 4593 c-52 -19 -61 -29 -47 -51 6 -11 16 -11 47 -3 179 50 341 -76 368 -284 l6 -50 -53 -29 c-123 -70 -241 -239 -254 -369 l-6 -57 150 0 c133 0 152 -2 166 -18 21 -23 22 -46 2 -66 -12 -12 -43 -15 -153 -15 -75 1 -143 0 -149 0 -8 -1 -13 -17 -13 -46 l0 -44 156 -3 c134 -3 158 -5 167 -20 8 -12 8 -24 -1 -42 l-12 -26 -155 0 -155 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -40 0 -40 83 -1 c268 -4 973 4 980 11 5 4 7 20 5 36 l-3 29 -158 5 c-125 4 -160 8 -167 20 -13 20 -12 33 3 53 10 14 36 17 167 19 l155 3 0 40 0 40 -155 3 c-131 2 -157 5 -167 19 -17 22 -16 38 3 57 13 13 42 16 165 16 l149 0 6 24 c3 14 3 34 -1 45 -6 20 -13 21 -155 21 -147 0 -150 0 -165 24 -13 19 -14 29 -5 45 10 20 19 21 165 21 l155 0 0 45 0 45 -145 0 c-132 0 -147 2 -165 20 -11 11 -20 25 -20 30 0 6 9 19 20 30 18 18 33 20 170 20 171 0 161 -7 135 95 -34 128 -117 243 -232 317 l-65 43 5 50 c13 122 81 226 180 274 42 20 58 23 120 18 40 -3 81 -7 92 -9 14 -2 21 3 23 19 3 19 -5 24 -49 37 -66 20 -102 20 -165 1 -68 -20 -140 -69 -180 -124 -39 -54 -74 -149 -74 -204 l0 -39 -52 9 c-67 10 -201 10 -253 0 l-41 -8 -11 63 c-15 88 -49 154 -110 216 -88 89 -205 121 -307 85z"/><path d="M1787 2982 c-13 -14 -17 -39 -17 -110 0 -87 1 -92 25 -108 l25 -16 0 -347 c0 -365 5 -410 50 -515 58 -137 181 -267 319 -340 72 -38 197 -76 248 -76 l33 0 0 -273 0 -274 -132 -7 c-198 -9 -394 -35 -468 -59 -56 -19 -65 -25 -65 -46 0 -30 41 -45 170 -66 251 -40 825 -45 1095 -11 142 18 260 50 260 70 0 35 -79 66 -220 85 -99 14 -317 31 -396 31 l-64 0 0 274 0 273 55 7 c290 34 541 271 594 560 7 35 11 196 11 390 0 320 1 332 20 344 18 11 20 23 20 112 0 114 -4 120 -85 120 -81 0 -85 -6 -85 -120 0 -89 2 -101 20 -112 19 -12 20 -23 20 -333 -1 -358 -9 -433 -58 -536 -67 -140 -194 -253 -342 -305 -100 -34 -323 -45 -440 -20 -221 46 -400 216 -455 431 -12 47 -15 128 -15 407 0 320 1 348 18 357 14 8 17 24 17 104 0 117 -6 127 -85 127 -42 0 -61 -5 -73 -18z"/><path d="M2030 2600 c0 -318 1 -345 21 -403 40 -121 116 -218 223 -286 166 -104 344 -115 523 -31 81 37 190 140 231 218 59 112 62 133 62 504 l0 338 -530 0 -530 0 0 -340z"/><path d="M1802 712 c3 -36 5 -38 70 -59 132 -44 282 -57 673 -58 362 0 492 8 655 41 108 23 130 36 130 80 0 31 -3 35 -17 29 -142 -59 -595 -94 -958 -75 -240 12 -409 32 -496 60 l-60 18 3 -36z"/></g></svg></div>
    <div class="step-bar" id="dots-3" style="flex:1; padding:0; min-height:unset;"></div>
  </div>
  <div class="step-content" style="padding-top:10px;">
    <h2 id="s3-title">辅助功能权限</h2>
    <p id="s3-desc">虾BB 需要辅助功能权限来检测 Globe 键（地球键）。授权后可能需要重启。</p>
    <div style="height:14px"></div>

    <div class="card">
      <div class="card-row">
        <div class="card-icon">⌨️</div>
        <div class="card-body">
          <div class="card-title" id="s3-card-title">辅助功能</div>
          <div class="card-desc" id="s3-status-desc">等待授权...</div>
        </div>
        <div class="card-action" id="s3-grant-area">
          <button class="btn btn-primary" style="font-size:13px" onclick="doRequestAcc()" id="s3-grant-btn">允许</button>
        </div>
      </div>
    </div>

    <div style="height:14px"></div>
    <p style="font-size:13px; color:var(--gray-500); text-align:center" id="s3-test-prompt">按下 Globe 键（地球键）测试</p>
    <div class="globe-key" id="globeKey">🌐</div>
    <p style="text-align:center; font-size:13px;" id="s3-detected-label"></p>

    <hr class="divider">
    <div style="display:flex; align-items:center; justify-content:space-between; margin-top:4px">
      <span class="hint" id="s3-restart-note">授权后若检测不到按键，可能需要重启虾BB。</span>
      <button class="btn btn-secondary" style="font-size:12px;padding:6px 14px" onclick="doRestart()" id="s3-restart-btn">重启</button>
    </div>
  </div>
  <div class="step-nav">
    <button class="btn btn-ghost" onclick="goBack()" id="nav-back-3">返回</button>
    <button class="btn btn-primary" onclick="goNext()" id="nav-next-3">下一步</button>
  </div>
</div>

<!-- STEP 4: TRY IT -->
<div class="step" id="step-5">
  <div class="step-header">
    <div class="app-icon app-icon-sm"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="#000000"><g transform="translate(0,512) scale(0.1,-0.1)" stroke="none"><path d="M1966 4593 c-52 -19 -61 -29 -47 -51 6 -11 16 -11 47 -3 179 50 341 -76 368 -284 l6 -50 -53 -29 c-123 -70 -241 -239 -254 -369 l-6 -57 150 0 c133 0 152 -2 166 -18 21 -23 22 -46 2 -66 -12 -12 -43 -15 -153 -15 -75 1 -143 0 -149 0 -8 -1 -13 -17 -13 -46 l0 -44 156 -3 c134 -3 158 -5 167 -20 8 -12 8 -24 -1 -42 l-12 -26 -155 0 -155 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -40 0 -40 83 -1 c268 -4 973 4 980 11 5 4 7 20 5 36 l-3 29 -158 5 c-125 4 -160 8 -167 20 -13 20 -12 33 3 53 10 14 36 17 167 19 l155 3 0 40 0 40 -155 3 c-131 2 -157 5 -167 19 -17 22 -16 38 3 57 13 13 42 16 165 16 l149 0 6 24 c3 14 3 34 -1 45 -6 20 -13 21 -155 21 -147 0 -150 0 -165 24 -13 19 -14 29 -5 45 10 20 19 21 165 21 l155 0 0 45 0 45 -145 0 c-132 0 -147 2 -165 20 -11 11 -20 25 -20 30 0 6 9 19 20 30 18 18 33 20 170 20 171 0 161 -7 135 95 -34 128 -117 243 -232 317 l-65 43 5 50 c13 122 81 226 180 274 42 20 58 23 120 18 40 -3 81 -7 92 -9 14 -2 21 3 23 19 3 19 -5 24 -49 37 -66 20 -102 20 -165 1 -68 -20 -140 -69 -180 -124 -39 -54 -74 -149 -74 -204 l0 -39 -52 9 c-67 10 -201 10 -253 0 l-41 -8 -11 63 c-15 88 -49 154 -110 216 -88 89 -205 121 -307 85z"/><path d="M1787 2982 c-13 -14 -17 -39 -17 -110 0 -87 1 -92 25 -108 l25 -16 0 -347 c0 -365 5 -410 50 -515 58 -137 181 -267 319 -340 72 -38 197 -76 248 -76 l33 0 0 -273 0 -274 -132 -7 c-198 -9 -394 -35 -468 -59 -56 -19 -65 -25 -65 -46 0 -30 41 -45 170 -66 251 -40 825 -45 1095 -11 142 18 260 50 260 70 0 35 -79 66 -220 85 -99 14 -317 31 -396 31 l-64 0 0 274 0 273 55 7 c290 34 541 271 594 560 7 35 11 196 11 390 0 320 1 332 20 344 18 11 20 23 20 112 0 114 -4 120 -85 120 -81 0 -85 -6 -85 -120 0 -89 2 -101 20 -112 19 -12 20 -23 20 -333 -1 -358 -9 -433 -58 -536 -67 -140 -194 -253 -342 -305 -100 -34 -323 -45 -440 -20 -221 46 -400 216 -455 431 -12 47 -15 128 -15 407 0 320 1 348 18 357 14 8 17 24 17 104 0 117 -6 127 -85 127 -42 0 -61 -5 -73 -18z"/><path d="M2030 2600 c0 -318 1 -345 21 -403 40 -121 116 -218 223 -286 166 -104 344 -115 523 -31 81 37 190 140 231 218 59 112 62 133 62 504 l0 338 -530 0 -530 0 0 -340z"/><path d="M1802 712 c3 -36 5 -38 70 -59 132 -44 282 -57 673 -58 362 0 492 8 655 41 108 23 130 36 130 80 0 31 -3 35 -17 29 -142 -59 -595 -94 -958 -75 -240 12 -409 32 -496 60 l-60 18 3 -36z"/></g></svg></div>
    <div class="step-bar" id="dots-5" style="flex:1; padding:0; min-height:unset;"></div>
  </div>
  <div class="step-content" style="padding-top:10px;">
    <h2 id="s4-title">📖 智能词汇表</h2>
    <p id="s4-desc" style="margin-bottom:20px;">其他语音工具会把 "Claude" 识别成 "cloud"，把 "OpenClaw" 识别成 "open cloud"。虾BB 不会。</p>
    <!-- Feature cards instead of raw word list -->
    <div style="display:flex; flex-direction:column; gap:14px;">
      <div style="background:#f9fafb; border-radius:255px 15px 225px 15px / 15px 225px 15px 255px; padding:16px 20px; border:2px solid #e5e7eb; transform:rotate(-0.5deg);">
        <div style="font-size:15px; font-weight:600; color:#1f2937; margin-bottom:4px;">🤖 40+ AI 工具词汇预置</div>
        <div style="font-size:13px; color:#6b7280; line-height:1.6;">Claude、OpenClaw、Cursor、Gemini、Kimi、DeepSeek、ChatGPT 等 AI 工具名称都能被精确识别，不再张冠李戴。</div>
      </div>
      <div style="background:#f9fafb; border-radius:255px 15px 225px 15px / 15px 225px 15px 255px; padding:16px 20px; border:2px solid #e5e7eb; transform:rotate(-0.5deg);">
        <div style="font-size:15px; font-weight:600; color:#1f2937; margin-bottom:4px;">💻 开发者常用英文术语</div>
        <div style="font-size:13px; color:#6b7280; line-height:1.6;">API、async、frontend、pull request、code review —— Vibe Coding 中常说的英文术语都在词库里。</div>
      </div>
      <div style="background:#f9fafb; border-radius:255px 15px 225px 15px / 15px 225px 15px 255px; padding:16px 20px; border:2px solid #e5e7eb; transform:rotate(-0.5deg);">
        <div style="font-size:15px; font-weight:600; color:#1f2937; margin-bottom:4px;">✏️ 支持自定义扩展</div>
        <div style="font-size:13px; color:#6b7280; line-height:1.6;" id="s4-dict-note">你可以随时在菜单栏添加自己的专属词汇 —— 公司名、项目名、同事英文名，说什么识别什么。</div>
      </div>
    </div>
  </div>
  <div class="step-nav">
    <button class="btn btn-ghost" onclick="goBack()" id="nav-back-5">返回</button>
    <button class="btn btn-primary" onclick="doFinish()" id="nav-next-5">开始使用虾BB</button>
  </div>
</div>

<!-- STEP 5: DICTIONARY -->
<div class="step" id="step-4">
  <div class="step-header">
    <div class="app-icon app-icon-sm"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="#000000"><g transform="translate(0,512) scale(0.1,-0.1)" stroke="none"><path d="M1966 4593 c-52 -19 -61 -29 -47 -51 6 -11 16 -11 47 -3 179 50 341 -76 368 -284 l6 -50 -53 -29 c-123 -70 -241 -239 -254 -369 l-6 -57 150 0 c133 0 152 -2 166 -18 21 -23 22 -46 2 -66 -12 -12 -43 -15 -153 -15 -75 1 -143 0 -149 0 -8 -1 -13 -17 -13 -46 l0 -44 156 -3 c134 -3 158 -5 167 -20 8 -12 8 -24 -1 -42 l-12 -26 -155 0 -155 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -45 0 -45 153 0 c161 0 177 -4 177 -45 0 -41 -16 -45 -177 -45 l-153 0 0 -40 0 -40 83 -1 c268 -4 973 4 980 11 5 4 7 20 5 36 l-3 29 -158 5 c-125 4 -160 8 -167 20 -13 20 -12 33 3 53 10 14 36 17 167 19 l155 3 0 40 0 40 -155 3 c-131 2 -157 5 -167 19 -17 22 -16 38 3 57 13 13 42 16 165 16 l149 0 6 24 c3 14 3 34 -1 45 -6 20 -13 21 -155 21 -147 0 -150 0 -165 24 -13 19 -14 29 -5 45 10 20 19 21 165 21 l155 0 0 45 0 45 -145 0 c-132 0 -147 2 -165 20 -11 11 -20 25 -20 30 0 6 9 19 20 30 18 18 33 20 170 20 171 0 161 -7 135 95 -34 128 -117 243 -232 317 l-65 43 5 50 c13 122 81 226 180 274 42 20 58 23 120 18 40 -3 81 -7 92 -9 14 -2 21 3 23 19 3 19 -5 24 -49 37 -66 20 -102 20 -165 1 -68 -20 -140 -69 -180 -124 -39 -54 -74 -149 -74 -204 l0 -39 -52 9 c-67 10 -201 10 -253 0 l-41 -8 -11 63 c-15 88 -49 154 -110 216 -88 89 -205 121 -307 85z"/><path d="M1787 2982 c-13 -14 -17 -39 -17 -110 0 -87 1 -92 25 -108 l25 -16 0 -347 c0 -365 5 -410 50 -515 58 -137 181 -267 319 -340 72 -38 197 -76 248 -76 l33 0 0 -273 0 -274 -132 -7 c-198 -9 -394 -35 -468 -59 -56 -19 -65 -25 -65 -46 0 -30 41 -45 170 -66 251 -40 825 -45 1095 -11 142 18 260 50 260 70 0 35 -79 66 -220 85 -99 14 -317 31 -396 31 l-64 0 0 274 0 273 55 7 c290 34 541 271 594 560 7 35 11 196 11 390 0 320 1 332 20 344 18 11 20 23 20 112 0 114 -4 120 -85 120 -81 0 -85 -6 -85 -120 0 -89 2 -101 20 -112 19 -12 20 -23 20 -333 -1 -358 -9 -433 -58 -536 -67 -140 -194 -253 -342 -305 -100 -34 -323 -45 -440 -20 -221 46 -400 216 -455 431 -12 47 -15 128 -15 407 0 320 1 348 18 357 14 8 17 24 17 104 0 117 -6 127 -85 127 -42 0 -61 -5 -73 -18z"/><path d="M2030 2600 c0 -318 1 -345 21 -403 40 -121 116 -218 223 -286 166 -104 344 -115 523 -31 81 37 190 140 231 218 59 112 62 133 62 504 l0 338 -530 0 -530 0 0 -340z"/><path d="M1802 712 c3 -36 5 -38 70 -59 132 -44 282 -57 673 -58 362 0 492 8 655 41 108 23 130 36 130 80 0 31 -3 35 -17 29 -142 -59 -595 -94 -958 -75 -240 12 -409 32 -496 60 l-60 18 3 -36z"/></g></svg></div>
    <div class="step-bar" id="dots-4" style="flex:1; padding:0; min-height:unset;"></div>
  </div>
  <!-- TWO-COLUMN TRY IT LAYOUT -->
  <div id="s5-body" style="display:flex; flex:1; flex-direction:row; overflow:hidden; padding:12px 20px 0;">
    <!-- LEFT COLUMN (55%) -->
    <div style="flex:0 0 55%; display:flex; flex-direction:column; padding-right:16px; overflow-y:auto;">
      <h2 id="s5-title" style="margin:0 0 6px; font-size:22px;">试试看</h2>
      <p id="s5-instruction" style="margin:0 0 12px; font-size:14px; color:var(--gray-500);">按住 Globe 键，念出下面这句话：</p>
      <!-- Quote card -->
      <div style="border-left:3px solid var(--accent); background:var(--accent-light); border-radius:0 10px 10px 0; padding:12px 14px; margin-bottom:14px;">
        <div style="font-size:13px; color:var(--accent-dark); font-weight:500; line-height:1.8; font-style:italic;" id="s5-sample-sentence">"无论是用 Claude Code 还是 OpenClaw，都能够成为一个出色的 Vibe Coder，享受 AI Agent 时代的无限自由。"</div>
      </div>
      <!-- Mic hint -->
      <div style="background:#f3f4f6; border-radius:8px; padding:8px 12px; margin-bottom:14px; display:flex; align-items:flex-start; gap:8px;">
        <span style="font-size:16px; line-height:1.4;">🎙</span>
        <span id="s5-press-hint" style="font-size:13px; color:var(--gray-500); line-height:1.5;">按住 Globe 键开始说话，松开后文字会出现在右边</span>
      </div>
      <!-- Status indicator -->
      <div id="s5-status" style="display:flex; align-items:center; gap:8px; min-height:28px;">
        <span id="s5-status-dot" style="width:10px; height:10px; border-radius:50%; background:#d1d5db; flex-shrink:0;"></span>
        <span id="s5-status-label" style="font-size:13px; color:var(--gray-500);">等待录音…</span>
      </div>
      <!-- Success note (hidden until transcription arrives) -->
      <div id="s5-done-note-box" style="display:none; background:var(--green-light); border:1.5px solid #bbf7d0; border-radius:10px; padding:10px 14px; margin-top:12px;">
        <p style="font-size:13px; color:#15803d; line-height:1.6; margin:0;" id="s5-done-note">注意到了吗？Claude Code、OpenClaw、Vibe Coder 都被精确识别了。</p>
      </div>
    </div>
    <!-- RIGHT COLUMN (45%) -->
    <div style="flex:0 0 45%; display:flex; flex-direction:column;">
      <!-- Mock window -->
      <div class="mock-window" style="flex:1; display:flex; flex-direction:column; min-height:0;">
        <div class="mock-titlebar">
          <div class="mock-dot" style="background:#ff5f57;"></div>
          <div class="mock-dot" style="background:#febc2e;"></div>
          <div class="mock-dot" style="background:#28c840;"></div>
          <span style="margin-left:6px; font-size:12px; color:#6b7280; font-weight:500;">虾BB</span>
        </div>
        <div class="mock-body" id="s5-mock-text" style="flex:1; overflow-y:auto;">
          <span id="s5-mock-placeholder" style="color:#928374; font-style:italic;">你的语音会出现在这里...</span>
        </div>
      </div>
    </div>
  </div>
  <div class="step-nav" id="s5-nav" style="padding-top:8px;">
    <button class="btn btn-ghost" onclick="goBack()" id="nav-back-4">返回</button>
    <div style="display:flex; gap:10px;">
      <button class="btn btn-ghost" onclick="goNext()" id="s5-skip-btn" style="font-size:13px; color:#928374;">跳过</button>
      <button class="btn btn-primary" onclick="goNext()" id="s5-start-btn" disabled style="opacity:0.4; cursor:not-allowed;">下一步</button>
    </div>
  </div>
</div>

<script>
var currentStep = 0;
var lang = 'zh';
var keyValidated = false;
var micConfirmed = false;
var barLevels = new Array(12).fill(0);

var S = {
  zh: {
    s0_title:'欢迎使用', s0_desc:'by Vibe Coders, for Vibe Coders',
    s0_btn:'开始设置', s0_hint:'设置只需 2 分钟',
    s1_title:'配置 API Key', s1_desc:'虾BB 使用 Google Gemini 进行语音识别。免费额度：每天 250 次，无需信用卡。',
    s1_hint:'免费版每天 250 次请求', s1_placeholder:'粘贴 API Key...',
    s1_validate:'验证', s1_validating:'验证中...', s1_existing:'已配置 Key', s1_change:'更换',
    s2_title:'麦克风权限', s2_desc:'虾BB 需要麦克风权限来录制你的声音。',
    s2_card_title:'麦克风', s2_granted:'已授权', s2_pending:'等待授权...',
    s2_grant_btn:'允许', s2_q:'说话时你能看到音量条在动吗？', s2_yes:'可以，继续', s2_no:'不行，换麦克风',
    s3_title:'辅助功能权限', s3_desc:'虾BB 需要辅助功能权限来检测 Globe 键（地球键）。授权后可能需要重启。',
    s3_card_title:'辅助功能', s3_granted:'已授权', s3_pending:'等待授权...',
    s3_grant_btn:'允许', s3_test_prompt:'按下 Globe 键（地球键）测试', s3_detected:'检测到 Globe 键！',
    s3_restart_note:'授权后若检测不到按键，可能需要重启虾BB。', s3_restart_btn:'重启',
    s4_title:'📖 智能词汇表', s4_desc:'虾BB 预置了 Vibe Coding 常用词汇，确保精准识别：',
    s4_dict_note:'你可以随时在菜单栏 → 自定义词汇表中添加更多词汇。',
    s5_title:'试试看', s5_instruction:'按住 Globe 键，念出下面这句话：',
    s5_sample:'"无论是用 Claude Code 还是 OpenClaw，都能够成为一个出色的 Vibe Coder。"',
    s5_press_hint:'按住 Globe 键开始说话，松开后文字会出现在右边',
    s5_done_note:'注意到了吗？Claude Code、OpenClaw、Vibe Coder 都被精确识别了。',
    s5_start:'开始使用虾BB',
    s5_status_idle:'等待录音…',
    s5_status_recording:'🔴 录音中…',
    s5_status_processing:'⏳ 识别中…',
    s5_status_done:'✅ 识别完成！',
    chk_key:'API Key', chk_key_ok:'已配置', chk_key_no:'未配置',
    chk_mic:'麦克风',  chk_mic_ok:'已授权', chk_mic_no:'未授权',
    chk_acc:'辅助功能',chk_acc_ok:'已授权', chk_acc_no:'未授权',
    back:'返回', next:'下一步', key_missing:'请输入 Key'
  },
  en: {
    s0_title:'Welcome to', s0_desc:'by Vibe Coders, for Vibe Coders',
    s0_btn:'Get Started', s0_hint:'Setup takes about 2 minutes',
    s1_title:'Gemini API Key', s1_desc:'XiaBB uses Google Gemini for transcription. Free tier: 250 requests/day, no credit card.',
    s1_hint:'Free tier: 250 requests per day', s1_placeholder:'Paste API Key...',
    s1_validate:'Validate', s1_validating:'Validating...', s1_existing:'Key configured', s1_change:'Change',
    s2_title:'Microphone Access', s2_desc:'XiaBB needs microphone access to capture your voice.',
    s2_card_title:'Microphone', s2_granted:'Granted', s2_pending:'Waiting...',
    s2_grant_btn:'Allow', s2_q:'Can you see the bars moving when you speak?', s2_yes:'Yes, continue', s2_no:'No, switch mic',
    s3_title:'Accessibility (Globe Key)', s3_desc:'XiaBB needs Accessibility to detect the Globe / fn key. A restart may be needed.',
    s3_card_title:'Accessibility', s3_granted:'Granted', s3_pending:'Waiting...',
    s3_grant_btn:'Allow', s3_test_prompt:'Press the Globe key to test', s3_detected:'Globe key detected!',
    s3_restart_note:'If the key is not detected after granting, restart XiaBB.', s3_restart_btn:'Restart',
    s4_title:'📖 Smart Dictionary', s4_desc:'XiaBB includes preset Vibe Coding vocabulary for accurate recognition:',
    s4_dict_note:'You can add more words anytime via menu bar → Custom Dictionary.',
    s5_title:'Try It Out', s5_instruction:'Hold Globe key and read the sentence below:',
    s5_sample:'"Whether using Claude Code or OpenClaw, you can become an outstanding Vibe Coder."',
    s5_press_hint:'Hold Globe key to start speaking — text will appear on the right when done',
    s5_done_note:'Notice how Claude Code, OpenClaw, Vibe Coder were all perfectly recognized.',
    s5_start:'Start Using XiaBB',
    s5_status_idle:'Waiting to record…',
    s5_status_recording:'🔴 Recording…',
    s5_status_processing:'⏳ Transcribing…',
    s5_status_done:'✅ Transcription complete!',
    chk_key:'API Key', chk_key_ok:'Configured', chk_key_no:'Missing',
    chk_mic:'Microphone', chk_mic_ok:'Granted', chk_mic_no:'Not granted',
    chk_acc:'Accessibility', chk_acc_ok:'Granted', chk_acc_no:'Not granted',
    back:'Back', next:'Next', key_missing:'Please enter a key'
  }
};
function t(k) { return (S[lang] && S[lang][k]) || (S.en[k]) || k; }

function setText(id, val) { var el = document.getElementById(id); if (el) el.textContent = val; }
function setPlaceholder(id, val) { var el = document.getElementById(id); if (el) el.placeholder = val; }
function setDisabled(id, v) { var el = document.getElementById(id); if (el) el.disabled = v; }

function applyLang() {
  setText('s0-title', t('s0_title')); setText('s0-desc', t('s0_desc'));
  setText('s0-btn', t('s0_btn')); setText('s0-hint', t('s0_hint'));
  setText('s1-title', t('s1_title')); setText('s1-desc', t('s1_desc'));
  setText('s1-hint', t('s1_hint')); setPlaceholder('apiKeyInput', t('s1_placeholder'));
  setText('validateBtn', t('s1_validate'));
  setText('s1-existing-label', t('s1_existing')); setText('s1-change-btn', t('s1_change'));
  setText('s2-title', t('s2_title')); setText('s2-desc', t('s2_desc'));
  setText('s2-card-title', t('s2_card_title')); setText('s2-status-desc', t('s2_pending'));
  setText('s2-grant-btn', t('s2_grant_btn')); setText('s2-q', t('s2_q'));
  setText('s2-yes-btn', t('s2_yes')); setText('s2-no-btn', t('s2_no'));
  setText('s3-title', t('s3_title')); setText('s3-desc', t('s3_desc'));
  setText('s3-card-title', t('s3_card_title')); setText('s3-status-desc', t('s3_pending'));
  setText('s3-grant-btn', t('s3_grant_btn')); setText('s3-test-prompt', t('s3_test_prompt'));
  setText('s3-restart-note', t('s3_restart_note')); setText('s3-restart-btn', t('s3_restart_btn'));
  setText('s4-title', t('s4_title')); setText('s4-desc', t('s4_desc'));
  setText('s4-dict-note', t('s4_dict_note'));
  setText('s5-title', t('s5_title')); setText('s5-instruction', t('s5_instruction'));
  setText('s5-sample-sentence', t('s5_sample')); setText('s5-press-hint', t('s5_press_hint'));
  setText('s5-done-note', t('s5_done_note'));
  setText('s5-start-btn', t('next'));
  setText('s5-status-label', t('s5_status_idle'));
  ['1','2','3','4'].forEach(function(n) {
    setText('nav-back-'+n, t('back'));
    setText('nav-next-'+n, t('next'));
  });
  setText('nav-back-5', t('back'));
  setText('nav-next-5', t('s5_start'));
}

function renderDots(stepEl, stepNum) {
  var container = stepEl.querySelector('.step-bar');
  if (!container) return;
  while (container.firstChild) container.removeChild(container.firstChild);
  for (var i = 1; i <= 5; i++) {
    var d = document.createElement('div');
    d.className = 'step-dot' + (i < stepNum ? ' done' : i === stepNum ? ' active' : '');
    container.appendChild(d);
  }
}

function showStep(n) {
  var steps = document.querySelectorAll('.step');
  for (var i = 0; i < steps.length; i++) steps[i].classList.remove('active','fade-in');
  var el = document.getElementById('step-'+n);
  if (!el) return;
  el.classList.add('active');
  if (n >= 1 && n <= 5) renderDots(el, n);
  void el.offsetWidth;
  el.classList.add('fade-in');
  currentStep = n;
  if (n === 2) {
    window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'startMicTest'});
  } else {
    window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'stopMicTest'});
  }
}

function startSetup() { showStep(1); }
function goBack() { if (currentStep > 0) showStep(currentStep - 1); }
function goNext() {
  if (currentStep < 5) showStep(currentStep + 1);
  else doFinish();
}

function onKeyInput() {
  keyValidated = false;
  setDisabled('nav-next-1', true);
  var input = document.getElementById('apiKeyInput');
  if (input) input.className = 'input-field';
  clearKeyStatus();
}
function onKeyDown(e) { if (e.key === 'Enter') doValidate(); }
function openAIStudio() {
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'openURL', url:'https://aistudio.google.com/apikey'});
}
function changeKey() {
  var ex = document.getElementById('s1-existing');
  var ia = document.getElementById('s1-input-area');
  if (ex) ex.style.display = 'none';
  if (ia) ia.style.display = '';
  keyValidated = false;
  setDisabled('nav-next-1', true);
}
function clearKeyStatus() {
  setText('keyStatusIcon', '');
  setText('keyStatusText', '');
  var sp = document.getElementById('keyStatusSpinner');
  if (sp) sp.style.display = 'none';
}
function setKeyStatus(icon, text, color, showSpinner) {
  setText('keyStatusIcon', icon);
  setText('keyStatusText', text);
  var ti = document.getElementById('keyStatusText');
  if (ti) ti.style.color = color || '';
  var sp = document.getElementById('keyStatusSpinner');
  if (sp) sp.style.display = showSpinner ? 'inline-block' : 'none';
}
function doValidate() {
  var input = document.getElementById('apiKeyInput');
  var key = input ? input.value.trim() : '';
  if (!key) {
    setKeyStatus('', t('key_missing'), 'var(--red)', false);
    return;
  }
  setDisabled('validateBtn', true);
  setText('validateBtn', t('s1_validating'));
  setKeyStatus('', t('s1_validating'), 'var(--accent-dark)', true);
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'validateKey', key:key});
}
function onKeyValidated(ok, msg) {
  setDisabled('validateBtn', false);
  setText('validateBtn', t('s1_validate'));
  var input = document.getElementById('apiKeyInput');
  if (ok) {
    keyValidated = true;
    if (input) input.className = 'input-field success';
    setKeyStatus('✅', msg, 'var(--green)', false);
    setDisabled('nav-next-1', false);
  } else {
    keyValidated = false;
    if (input) input.className = 'input-field error';
    setKeyStatus('❌', msg, 'var(--red)', false);
    setDisabled('nav-next-1', true);
  }
}
function showExistingKey(masked) {
  var ex = document.getElementById('s1-existing');
  var ia = document.getElementById('s1-input-area');
  var ms = document.getElementById('s1-existing-masked');
  if (ex) ex.style.display = '';
  if (ia) ia.style.display = 'none';
  if (ms) ms.textContent = masked;
  keyValidated = true;
  setDisabled('nav-next-1', false);
}

function doRequestMic() {
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'requestMic'});
}
function onMicPermission(granted) {
  var desc = document.getElementById('s2-status-desc');
  var area = document.getElementById('s2-grant-area');
  if (granted) {
    if (desc) { desc.textContent = '✅ ' + t('s2_granted'); desc.style.color = 'var(--green)'; }
    while (area && area.firstChild) area.removeChild(area.firstChild);
    if (area) {
      var badge = document.createElement('span');
      badge.className = 'badge badge-success';
      badge.textContent = '✅ ' + t('s2_granted');
      area.appendChild(badge);
    }
  } else {
    if (desc) { desc.textContent = t('s2_pending'); desc.style.color = ''; }
  }
}
function onMicLevel(level) {
  // Horizontal level meter: bars 0-11 left to right
  // Number of active bars based on level
  var activeBars = Math.round(level * 12);
  for (var i = 0; i < 12; i++) {
    var isActive = i < activeBars;
    // Each bar gets a slight random variation in height for organic look
    var noise = isActive ? (0.6 + 0.4 * Math.random()) : (0.15 + 0.15 * Math.random());
    // Bars towards center are taller (bell-curve shape)
    var shape = 1 - Math.abs(i - 5.5) / 6;
    var targetH = isActive
      ? Math.max(8, Math.round((14 + shape * 30) * noise * (level * 1.2 + 0.3)))
      : Math.max(4, Math.round(6 * noise));
    barLevels[i] = barLevels[i] * 0.55 + targetH * 0.45;
    var bar = document.getElementById('bar'+i);
    if (bar) {
      bar.style.height = Math.round(barLevels[i]) + 'px';
      if (isActive) bar.classList.add('active');
      else bar.classList.remove('active');
    }
  }
}
function micYes() {
  micConfirmed = true;
  setDisabled('nav-next-2', false);
  showStep(3);
}
function micNo() {
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'openURL', url:'x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone'});
}
function updatePermissionStatus(perm, granted) {
  if (perm === 'mic') {
    onMicPermission(granted);
    if (granted) window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'startMicTest'});
  } else if (perm === 'acc') {
    onAccessibilityGranted();
  }
}

function doRequestAcc() {
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'requestAccessibility'});
}
function onAccessibilityGranted() {
  var desc = document.getElementById('s3-status-desc');
  var area = document.getElementById('s3-grant-area');
  if (desc) { desc.textContent = '✅ ' + t('s3_granted'); desc.style.color = 'var(--green)'; }
  while (area && area.firstChild) area.removeChild(area.firstChild);
  if (area) {
    var badge = document.createElement('span');
    badge.className = 'badge badge-success';
    badge.textContent = '✅ ' + t('s3_granted');
    area.appendChild(badge);
  }
}
var globeDetectedOnce = false;
function onGlobeKeyDetected() {
  // Legacy: treat as a press event
  onGlobeKeyDown();
  setTimeout(onGlobeKeyUp, 200);
}
function onGlobeKeyDown() {
  var key = document.getElementById('globeKey');
  if (key) {
    key.classList.add('pressed');
  }
  // Mark first detection for step 3
  if (!globeDetectedOnce) {
    globeDetectedOnce = true;
    var lbl = document.getElementById('s3-detected-label');
    if (lbl) { lbl.textContent = '✅ ' + t('s3_detected'); lbl.style.color = 'var(--accent)'; lbl.style.fontWeight = '500'; }
  }
  // Step 5: update status indicator to "recording"
  if (currentStep === 5) {
    setS5Status('recording');
  }
}
function onGlobeKeyUp() {
  var key = document.getElementById('globeKey');
  if (key) {
    key.classList.remove('pressed');
  }
  // Step 5: update status indicator to "processing"
  if (currentStep === 5) {
    setS5Status('processing');
  }
}
function setS5Status(state) {
  var dot = document.getElementById('s5-status-dot');
  var lbl = document.getElementById('s5-status-label');
  if (!dot || !lbl) return;
  if (state === 'recording') {
    dot.style.background = '#ef4444';
    dot.style.boxShadow = '0 0 0 3px rgba(239,68,68,0.25)';
    lbl.textContent = t('s5_status_recording');
    lbl.style.color = '#ef4444';
  } else if (state === 'processing') {
    dot.style.background = '#f59e0b';
    dot.style.boxShadow = '0 0 0 3px rgba(245,158,11,0.2)';
    lbl.textContent = t('s5_status_processing');
    lbl.style.color = '#92400e';
  } else if (state === 'done') {
    dot.style.background = '#22c55e';
    dot.style.boxShadow = '0 0 0 3px rgba(34,197,94,0.2)';
    lbl.textContent = t('s5_status_done');
    lbl.style.color = '#15803d';
  } else {
    dot.style.background = '#d1d5db';
    dot.style.boxShadow = 'none';
    lbl.textContent = t('s5_status_idle');
    lbl.style.color = 'var(--gray-500)';
  }
}
function onTranscriptionResult(text) {
  // Show text in mock window with a fade-in effect
  var mockBody = document.getElementById('s5-mock-text');
  if (mockBody) {
    mockBody.innerHTML = '';
    var span = document.createElement('span');
    span.textContent = text;
    span.style.opacity = '0';
    span.style.transition = 'opacity 0.4s ease';
    mockBody.appendChild(span);
    // Trigger fade-in
    setTimeout(function() { span.style.opacity = '1'; }, 30);
  }
  // Show success note
  var noteBox = document.getElementById('s5-done-note-box');
  if (noteBox) noteBox.style.display = 'block';
  // Update status
  setS5Status('done');
  // Enable finish button
  var btn = document.getElementById('s5-start-btn');
  if (btn) {
    btn.disabled = false;
    btn.style.opacity = '1';
    btn.style.cursor = 'pointer';
  }
}
function doRestart() {
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'restart'});
}
function doFinish() {
  window.webkit && window.webkit.messageHandlers.xiabb.postMessage({action:'finish'});
}

function updateChecklist(hasKey, micOK, accOK) {
  setText('chk-key-icon', hasKey ? '✅' : '⚠️');
  setText('chk-key-status', hasKey ? t('chk_key_ok') : t('chk_key_no'));
  var ks = document.getElementById('chk-key-status');
  if (ks) ks.style.color = hasKey ? 'var(--green)' : 'var(--gray-400)';

  setText('chk-mic-icon', micOK ? '✅' : '⚠️');
  setText('chk-mic-status', micOK ? t('chk_mic_ok') : t('chk_mic_no'));
  var ms = document.getElementById('chk-mic-status');
  if (ms) ms.style.color = micOK ? 'var(--green)' : 'var(--gray-400)';

  setText('chk-acc-icon', accOK ? '✅' : '⚠️');
  setText('chk-acc-status', accOK ? t('chk_acc_ok') : t('chk_acc_no'));
  var as = document.getElementById('chk-acc-status');
  if (as) as.style.color = accOK ? 'var(--green)' : 'var(--gray-400)';
}

function init(cfg) {

  lang = cfg.lang || 'zh';
  applyLang();
  showStep(cfg.step || 0);
  if (cfg.existingKey) showExistingKey(cfg.existingKey);
  if (cfg.micGranted) onMicPermission(true);
  if (cfg.accGranted) onAccessibilityGranted();
  updateChecklist(cfg.existingKey, cfg.micGranted, cfg.accGranted);
}
</script>
</body>
</html>
"""

// MARK: - OnboardingWindow class

class OnboardingWindow: NSObject, WKScriptMessageHandler {
    private var window: NSWindow?
    var webView: WKWebView?

    // Mic test engine
    private var micEngine: AVAudioEngine?
    private var micTestActive = false

    // Globe key monitor (separate from main event tap)
    private var globeMonitor: Any?

    func show() {
        // Show in Dock + Cmd+Tab during onboarding
        NSApp.setActivationPolicy(.regular)
        // Ensure Globe key events route to onboarding
        if let app = XiaBBApp.shared { app.isOnboarding = true }

        if let w = window, w.isVisible {
            w.makeKeyAndOrderFront(nil)
            NSApp.activate(ignoringOtherApps: true)
            return
        }

        let savedStep = loadConfig()["onboarding_step"] as? Int ?? 0

        let wW: CGFloat = 600, wH: CGFloat = 550
        let win = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: wW, height: wH),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        win.title = currentLang == "zh" ? "虾BB — 设置向导" : "XiaBB — Setup Wizard"
        win.center()
        win.isReleasedWhenClosed = false
        win.styleMask.remove(.resizable)
        self.window = win

        // Build WKWebView
        let config = WKWebViewConfiguration()
        config.userContentController.add(self, name: "xiabb")

        let wv = WKWebView(frame: NSRect(x: 0, y: 0, width: wW, height: wH), configuration: config)
        wv.autoresizingMask = [.width, .height]
        wv.setValue(false, forKey: "drawsBackground")
        win.contentView = wv
        self.webView = wv

        wv.loadHTMLString(onboardingHTML, baseURL: nil)

        // Ensure Edit menu exists for Cmd+C/V/X/A to work in WKWebView
        if NSApp.mainMenu?.item(withTitle: "Edit") == nil {
            let editMenu = NSMenu(title: "Edit")
            editMenu.addItem(withTitle: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x")
            editMenu.addItem(withTitle: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
            editMenu.addItem(withTitle: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v")
            editMenu.addItem(withTitle: "Select All", action: #selector(NSText.selectAll(_:)), keyEquivalent: "a")
            let editItem = NSMenuItem(title: "Edit", action: nil, keyEquivalent: "")
            editItem.submenu = editMenu
            if NSApp.mainMenu == nil { NSApp.mainMenu = NSMenu() }
            NSApp.mainMenu?.addItem(editItem)
        }

        win.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)

        // After load, call init() in JS with current state
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.45) { [weak self] in
            self?.sendInitToJS(step: savedStep)
        }
    }

    // MARK: - JS to Swift bridge

    func userContentController(_ userContentController: WKUserContentController,
                                didReceive message: WKScriptMessage) {
        guard let body = message.body as? [String: Any],
              let action = body["action"] as? String else { return }

        switch action {
        case "validateKey":
            let key = body["key"] as? String ?? ""
            validateAPIKey(key)

        case "requestMic":
            let status = AVCaptureDevice.authorizationStatus(for: .audio)
            if status == .notDetermined {
                AVCaptureDevice.requestAccess(for: .audio) { [weak self] granted in
                    DispatchQueue.main.async {
                        let js = "updatePermissionStatus('mic', \(granted ? "true" : "false"))"
                        self?.webView?.evaluateJavaScript(js, completionHandler: nil)
                    }
                }
            } else {
                NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone")!)
            }

        case "requestAccessibility":
            let opts = [kAXTrustedCheckOptionPrompt.takeUnretainedValue(): true] as CFDictionary
            AXIsProcessTrustedWithOptions(opts)
            DistributedNotificationCenter.default().addObserver(
                forName: NSNotification.Name("com.apple.accessibility.api"),
                object: nil, queue: .main
            ) { [weak self] _ in
                if AXIsProcessTrusted() {
                    self?.webView?.evaluateJavaScript("onAccessibilityGranted()", completionHandler: nil)
                }
            }

        case "startMicTest":
            startMicTest()

        case "stopMicTest":
            stopMicTest()

        case "openURL":
            if let urlStr = body["url"] as? String, let url = URL(string: urlStr) {
                NSWorkspace.shared.open(url)
            }

        case "restart":
            let execPath = Bundle.main.executablePath ?? ProcessInfo.processInfo.arguments[0]
            let task = Process()
            task.executableURL = URL(fileURLWithPath: execPath)
            try? task.run()
            NSApp.terminate(nil)

        case "finish":
            finish()

        default:
            log("[onboarding] Unknown action: \(action)")
        }
    }

    // MARK: - Init JS

    private func sendInitToJS(step: Int) {
        // Re-read API key from file to ensure we have the latest
        apiKey = loadAPIKey()

        let micGranted = AVCaptureDevice.authorizationStatus(for: .audio) == .authorized
        let accGranted = AXIsProcessTrusted()
        let hasKey = !apiKey.isEmpty

        var maskedKeyStr = "null"
        if hasKey {
            let masked = maskKey(apiKey)
            // Escape for JS string — masked key only contains alphanumeric + * chars, safe
            maskedKeyStr = "\"\(masked)\""
        }

        let js = """
        init({lang:'\(currentLang)',step:\(step),existingKey:\(maskedKeyStr),micGranted:\(micGranted),accGranted:\(accGranted)});
        """
        webView?.evaluateJavaScript(js, completionHandler: nil)

        if accGranted { installGlobeMonitor() }
    }

    // MARK: - API Key Validation

    private func validateAPIKey(_ key: String) {
        guard !key.isEmpty else {
            let msg = currentLang == "zh" ? "请输入 Key" : "Please enter a key"
            webView?.callAsyncJavaScript("onKeyValidated(ok, msg)", arguments: ["ok": false, "msg": msg], in: nil, in: .page, completionHandler: nil)
            return
        }

        guard let url = URL(string: "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent") else { return }
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.setValue(key, forHTTPHeaderField: "x-goog-api-key")
        req.timeoutInterval = 15
        let bodyObj: [String: Any] = [
            "contents": [["parts": [["text": "Say OK"]]]],
            "generationConfig": ["maxOutputTokens": 5]
        ]
        req.httpBody = try? JSONSerialization.data(withJSONObject: bodyObj)

        URLSession.shared.dataTask(with: req) { [weak self] data, response, error in
            DispatchQueue.main.async {
                guard let self = self else { return }
                let httpCode = (response as? HTTPURLResponse)?.statusCode ?? 0
                if error == nil && httpCode == 200 {
                    let keyFile = dataDir.appendingPathComponent(".api-key")
                    try? key.write(to: keyFile, atomically: true, encoding: .utf8)
                    // Restrict file permissions to owner-only (600)
                    try? FileManager.default.setAttributes([.posixPermissions: 0o600], ofItemAtPath: keyFile.path)
                    apiKey = key
                    let msg = currentLang == "zh" ? "Key 有效" : "Key is valid"
                    self.webView?.callAsyncJavaScript("onKeyValidated(ok, msg)", arguments: ["ok": true, "msg": msg], in: nil, in: .page, completionHandler: nil)
                    log("🔑 API key validated and saved via onboarding")
                } else {
                    var msg = currentLang == "zh" ? "Key 无效，请检查后重试" : "Invalid key — check and try again"
                    if let data = data,
                       let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                       let err = json["error"] as? [String: Any],
                       let errMsg = err["message"] as? String {
                        msg = String(errMsg.prefix(80))
                    }
                    self.webView?.callAsyncJavaScript("onKeyValidated(ok, msg)", arguments: ["ok": false, "msg": msg], in: nil, in: .page, completionHandler: nil)
                }
            }
        }.resume()
    }

    // MARK: - Mic Test

    private func startMicTest() {
        guard !micTestActive else { return }
        guard AVCaptureDevice.authorizationStatus(for: .audio) == .authorized else { return }
        guard hasPhysicalAudioInput() else {
            log("[onboarding] No mic for mic test, skipping")
            return
        }
        stopMicTest()
        micTestActive = true

        let engine = AVAudioEngine()
        micEngine = engine
        let inputNode = engine.inputNode
        let hwFormat = inputNode.outputFormat(forBus: 0)
        guard hwFormat.sampleRate > 0 && hwFormat.channelCount > 0 else { return }

        inputNode.installTap(onBus: 0, bufferSize: 1024, format: hwFormat) { [weak self] buffer, _ in
            guard let self = self, self.micTestActive else { return }
            let channelData = buffer.floatChannelData?[0]
            let frameLength = Int(buffer.frameLength)
            guard let data = channelData, frameLength > 0 else { return }
            var rms: Float = 0
            for i in 0..<frameLength { rms += data[i] * data[i] }
            rms = sqrtf(rms / Float(frameLength))
            let dB = 20 * log10f(max(rms, 1e-7))
            let norm = max(0, min(1, (dB + 60) / 50))
            let levelStr = String(format: "%.3f", norm)
            DispatchQueue.main.async { [weak self] in
                self?.webView?.evaluateJavaScript("onMicLevel(\(levelStr))", completionHandler: nil)
            }
        }
        engine.prepare()
        try? engine.start()
        log("[onboarding] Mic test started")
    }

    private func stopMicTest() {
        micTestActive = false
        micEngine?.inputNode.removeTap(onBus: 0)
        micEngine?.stop()
        micEngine = nil
    }

    // MARK: - Globe Key Monitor

    private var globeWasDown = false

    private func installGlobeMonitor() {
        removeGlobeMonitor()
        guard AXIsProcessTrusted() else { return }
        globeMonitor = NSEvent.addGlobalMonitorForEvents(matching: [.flagsChanged]) { [weak self] event in
            guard let self = self else { return }
            let fnNow = event.modifierFlags.contains(.function)
            if fnNow && !self.globeWasDown {
                self.globeWasDown = true
                DispatchQueue.main.async {
                    self.webView?.evaluateJavaScript("onGlobeKeyDown()", completionHandler: nil)
                }
            } else if !fnNow && self.globeWasDown {
                self.globeWasDown = false
                DispatchQueue.main.async {
                    self.webView?.evaluateJavaScript("onGlobeKeyUp()", completionHandler: nil)
                }
            }
        }
    }

    // Called from XiaBBApp.handleFlagsChanged when isOnboarding=true
    func onGlobeEvent(pressed: Bool) {
        if pressed {
            webView?.evaluateJavaScript("onGlobeKeyDown()", completionHandler: nil)
        } else {
            webView?.evaluateJavaScript("onGlobeKeyUp()", completionHandler: nil)
        }
    }

    // Legacy entry point — kept for compatibility
    func onGlobeDetectedFromEventTap() {
        onGlobeEvent(pressed: true)
    }

    private func removeGlobeMonitor() {
        if let m = globeMonitor { NSEvent.removeMonitor(m); globeMonitor = nil }
    }

    // MARK: - Finish

    private func finish() {
        saveConfig(["onboarded": true, "onboarding_step": 0])
        stopMicTest()
        removeGlobeMonitor()
        window?.close()
        // Hide from Dock + Cmd+Tab, back to menu bar mode
        NSApp.setActivationPolicy(.accessory)
        // Re-enable recording after onboarding
        if let app = XiaBBApp.shared {
            app.isOnboarding = false
        }
        log("✅ Onboarding complete")
    }

    // MARK: - Helpers

    private func maskKey(_ key: String) -> String {
        if key.count > 16 { return String(key.prefix(8)) + "****" + String(key.suffix(4)) }
        else if key.count > 4 { return String(key.prefix(4)) + "****" }
        return "****"
    }

}

// MARK: - HUD Overlay

class HUDOverlay {
    private var window: NSWindow!
    private var label: NSTextField!
    private var dot: NSView!
    private var bg: NSView!
    private var bars: [NSView] = []  // 6 bars: [left0,left1,left2, right0,right1,right2]
    private var doneCheck: NSTextField!
    private var hudIcon: NSImageView!
    private var leftB: NSTextField!
    private var rightB: NSTextField!
    private var copyBtn: NSButton!
    private var modeBadge: NSTextField!  // persistent mode indicator
    var resultText = ""
    private var hideTimer: Timer?
    private var pulsePhase: Double = 0
    var isPulsing = false
    var isProcessing = false  // true when finalizing (after recording stops)

    init() {
        let cfg = loadConfig()
        let w: CGFloat = 280, h: CGFloat = 48
        let screen = NSScreen.main?.frame ?? NSRect(x: 0, y: 0, width: 1920, height: 1080)
        let x = (cfg["hud_x"] as? CGFloat) ?? ((screen.width - w) / 2)
        let y = (cfg["hud_y"] as? CGFloat) ?? (screen.height - h - 60)

        window = NSWindow(contentRect: NSRect(x: x, y: y, width: w, height: h),
                          styleMask: .borderless, backing: .buffered, defer: false)
        window.level = .floating
        window.isOpaque = false
        window.backgroundColor = .clear
        window.isMovableByWindowBackground = true
        window.collectionBehavior = [.canJoinAllSpaces, .stationary]
        window.hasShadow = true

        let cv = NSView(frame: NSRect(x: 0, y: 0, width: w, height: h))
        window.contentView = cv

        // Rounded background
        bg = HUDBackground(frame: NSRect(x: 0, y: 0, width: w, height: h))
        cv.addSubview(bg)

        // === Brand area: icon centered, wave bars on both sides, BB for success ===
        let iconH: CGFloat = 36
        let iconW: CGFloat = iconH * (14.0 / 36.0)
        let brandCenterX: CGFloat = 24 // center of the brand area
        let iconView = NSImageView(frame: NSRect(x: brandCenterX - iconW / 2, y: (h - iconH) / 2, width: iconW, height: iconH))
        let iconPaths = [
            Bundle.main.resourceURL?.appendingPathComponent("icon@2x.png"),
            dataDir.appendingPathComponent("icon@2x.png"),
            Bundle.main.resourceURL?.appendingPathComponent("icon.png"),
            dataDir.appendingPathComponent("icon.png"),
        ].compactMap { $0 }
        for path in iconPaths {
            if let img = NSImage(contentsOf: path) {
                img.isTemplate = true
                iconView.image = img
                break
            }
        }
        iconView.imageScaling = .scaleProportionallyDown
        iconView.contentTintColor = .systemRed
        cv.addSubview(iconView)
        hudIcon = iconView

        // Wave bars — 3 on each side, short→medium→long outward
        let barW: CGFloat = 2
        let barGap: CGFloat = 2.5
        let barHeights: [CGFloat] = [6, 10, 14]
        bars = []

        for i in 0..<3 {
            let x = brandCenterX - iconW / 2 - CGFloat(i + 1) * (barW + barGap)
            let bh = barHeights[i]
            let bar = NSView(frame: NSRect(x: x, y: (h - bh) / 2, width: barW, height: bh))
            bar.wantsLayer = true
            bar.layer?.cornerRadius = barW / 2
            bar.layer?.backgroundColor = NSColor.systemRed.cgColor
            cv.addSubview(bar)
            bars.append(bar)
        }
        for i in 0..<3 {
            let x = brandCenterX + iconW / 2 + CGFloat(i) * (barW + barGap) + barGap
            let bh = barHeights[i]
            let bar = NSView(frame: NSRect(x: x, y: (h - bh) / 2, width: barW, height: bh))
            bar.wantsLayer = true
            bar.layer?.cornerRadius = barW / 2
            bar.layer?.backgroundColor = NSColor.systemRed.cgColor
            cv.addSubview(bar)
            bars.append(bar)
        }

        // "BB!" — super tiny, top-right of mic icon, like a little speech bubble saying hi
        let bbFont = NSFont(name: "Futura-Bold", size: 7) ?? .systemFont(ofSize: 7, weight: .black)
        let iconRight = brandCenterX + iconW / 2
        let iconTop = (h + iconH) / 2

        rightB = NSTextField(labelWithString: "BB!")
        rightB.font = bbFont
        rightB.textColor = .systemGreen
        rightB.backgroundColor = .clear
        rightB.isBezeled = false
        rightB.isEditable = false
        rightB.frame = NSRect(x: iconRight - 3, y: iconTop - 5, width: 20, height: 9)
        rightB.wantsLayer = true
        rightB.layer?.setAffineTransform(CGAffineTransform(rotationAngle: -0.25))
        rightB.isHidden = true
        cv.addSubview(rightB)

        leftB = rightB // alias to avoid crash on old references

        dot = iconView

        // Mode badge — right-side emoji + text, no background color
        modeBadge = NSTextField(labelWithString: "")
        modeBadge.font = .systemFont(ofSize: 13)
        modeBadge.alignment = .center
        modeBadge.isBezeled = false
        modeBadge.isEditable = false
        modeBadge.isSelectable = false
        modeBadge.backgroundColor = .clear
        modeBadge.textColor = currentTheme.textColor
        modeBadge.frame = NSRect(x: w - 80, y: (h - 20) / 2, width: 72, height: 20)
        modeBadge.isHidden = true
        cv.addSubview(modeBadge)

        // Text label — always at same position, badge doesn't affect it
        label = NSTextField(labelWithString: "")
        label.frame = NSRect(x: 52, y: (h - 20) / 2, width: w - 86, height: 20)
        label.textColor = currentTheme.textColor
        label.font = .systemFont(ofSize: currentTheme.fontSize, weight: .medium)
        label.backgroundColor = .clear
        label.isBezeled = false
        label.isEditable = false
        label.isSelectable = false
        label.lineBreakMode = .byTruncatingHead
        cv.addSubview(label)

        // Copy button — right side of HUD, hidden until result
        copyBtn = NSButton(frame: NSRect(x: w - 36, y: (h - 20) / 2, width: 28, height: 20))
        copyBtn.title = "📋"
        copyBtn.bezelStyle = .inline
        copyBtn.isBordered = false
        copyBtn.font = .systemFont(ofSize: 14)
        copyBtn.target = self
        copyBtn.action = #selector(handleClick)
        copyBtn.toolTip = "复制 / Copy"
        copyBtn.isHidden = true
        cv.addSubview(copyBtn)

        // Also keep whole-HUD click to copy
        let clickGR = NSClickGestureRecognizer(target: self, action: #selector(handleClick))
        window.contentView?.addGestureRecognizer(clickGR)
    }

    @objc private func handleClick() {
        guard !resultText.isEmpty else { return }
        NSPasteboard.general.clearContents()
        NSPasteboard.general.setString(resultText, forType: .string)
        label.stringValue = "✅ " + L("copied")
        copyBtn.title = "✅"
        // Hide after brief confirmation
        hideTimer?.invalidate()
        hideTimer = Timer.scheduledTimer(withTimeInterval: 0.8, repeats: false) { [weak self] _ in
            self?.hide()
        }
    }

    private func resize(for text: String) {
        let badgeExtra: CGFloat = modeBadge.isHidden ? 0 : 80
        let minW: CGFloat = 200 + badgeExtra, maxW: CGFloat = 700, h: CGFloat = 48
        let w = min(maxW, max(minW, CGFloat(text.count) * 7.5 + 56 + badgeExtra))
        let f = window.frame
        let cx = f.origin.x + f.width / 2
        let newX = cx - w / 2
        window.setFrame(NSRect(x: newX, y: f.origin.y, width: w, height: h), display: true)
        bg.frame = NSRect(x: 0, y: 0, width: w, height: h)
        bg.needsDisplay = true
        let badgeSpace: CGFloat = modeBadge.isHidden ? 0 : 80
        label.frame = NSRect(x: 52, y: (h - 20) / 2, width: w - 86 - badgeSpace, height: 20)
        copyBtn.frame = NSRect(x: w - 36 - badgeSpace, y: (h - 20) / 2, width: 28, height: 20)
        if !modeBadge.isHidden {
            modeBadge.frame = NSRect(x: w - 80, y: (h - 20) / 2, width: 72, height: 20)
        }
    }

    /// Position HUD near the mouse cursor (above it) so it's always visible where you're working
    func moveToMouse() {
        let mouse = NSEvent.mouseLocation  // screen coords, origin bottom-left
        let hudW = window.frame.width
        let hudH = window.frame.height
        let screen = NSScreen.main?.frame ?? NSRect(x: 0, y: 0, width: 1920, height: 1080)

        // Place HUD centered above the mouse, 40px up
        var x = mouse.x - hudW / 2
        var y = mouse.y + 40

        // Keep on screen
        if x < screen.minX + 8 { x = screen.minX + 8 }
        if x + hudW > screen.maxX - 8 { x = screen.maxX - hudW - 8 }
        if y + hudH > screen.maxY - 8 { y = mouse.y - hudH - 20 }  // flip below if too high
        if y < screen.minY + 8 { y = screen.minY + 8 }

        window.setFrameOrigin(NSPoint(x: x, y: y))
    }

    func show(text: String) {
        DispatchQueue.main.async { [self] in
            resultText = ""
            hideTimer?.invalidate()
            hideTimer = nil
            // Reset mode badge
            modeBadge.isHidden = true
            resize(for: text)
            label.stringValue = text
            isProcessing = false
            let rc = currentTheme.recordingColor
            bars.forEach { $0.isHidden = false; $0.layer?.backgroundColor = rc.cgColor }
            rightB.isHidden = true
            copyBtn.isHidden = true
            hudIcon.contentTintColor = rc
            window.alphaValue = 1.0
            moveToMouse()
            window.orderFrontRegardless()
            isPulsing = true
            pulsePhase = 0
        }
    }

    func setMode(_ mode: SmartMode) {
        DispatchQueue.main.async { [self] in
            if mode == .dictation {
                modeBadge.isHidden = true
            } else {
                let isZH = currentLang == "zh"
                let text: String
                switch mode {
                case .translate: text = isZH ? "🔄 翻译" : "🔄 Trans"
                case .prompt: text = isZH ? "⚡ 提示词" : "⚡ Prompt"
                case .email: text = isZH ? "📧 邮件" : "📧 Email"
                case .dictation: text = ""
                }
                modeBadge.stringValue = text
                modeBadge.isHidden = false
                let w = window.frame.width
                let h = window.frame.height
                modeBadge.frame = NSRect(x: w - 80, y: (h - 20) / 2, width: 72, height: 20)
            }
        }
    }

    func updateText(_ text: String) {
        DispatchQueue.main.async { [self] in
            resize(for: text)
            label.stringValue = text
        }
    }

    func hide() {
        DispatchQueue.main.async { [self] in
            isPulsing = false
            window.orderOut(nil)
        }
    }

    func showResult(_ text: String, isError: Bool = false) {
        DispatchQueue.main.async { [self] in
            let display = isError ? "Error: \(text.prefix(50))" : String(text.prefix(60)) + (text.count > 60 ? "..." : "")
            if !isError { resultText = text }
            resize(for: display)
            label.stringValue = display
            isPulsing = false
            isProcessing = false
            modeBadge.isHidden = true
            // Hide wave bars, show B B! for success (or hide for error)
            bars.forEach { $0.isHidden = true }
            if isError {
                rightB.isHidden = true
            } else {
                // BB! pops out at upper-right of icon with spring bounce
                rightB.textColor = currentTheme.successColor
                rightB.isHidden = false
                rightB.alphaValue = 0
                rightB.layer?.setAffineTransform(
                    CGAffineTransform(scaleX: 0.1, y: 0.1).rotated(by: -0.2))

                // Pop in
                NSAnimationContext.runAnimationGroup { ctx in
                    ctx.duration = 0.25
                    ctx.timingFunction = CAMediaTimingFunction(name: .easeOut)
                    ctx.allowsImplicitAnimation = true
                    self.rightB.alphaValue = 1
                    self.rightB.layer?.setAffineTransform(
                        CGAffineTransform(scaleX: 1.3, y: 1.3).rotated(by: -0.2))
                }
                // Settle back
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
                    NSAnimationContext.runAnimationGroup { ctx in
                        ctx.duration = 0.2
                        ctx.allowsImplicitAnimation = true
                        self.rightB.layer?.setAffineTransform(
                            CGAffineTransform(scaleX: 1, y: 1).rotated(by: -0.2))
                    }
                }
            }
            hudIcon.contentTintColor = isError ? currentTheme.recordingColor : currentTheme.successColor
            copyBtn.isHidden = isError  // show copy button on success
            dot.alphaValue = 1.0
            window.alphaValue = 1.0
            window.orderFrontRegardless()

            hideTimer?.invalidate()
            hideTimer = Timer.scheduledTimer(withTimeInterval: 1.5, repeats: false) { [weak self] _ in
                self?.hide()
            }
        }
    }

    func tickPulse() {
        guard isPulsing else { return }
        pulsePhase += 0.15
        let h: CGFloat = 48
        let maxHeights: [CGFloat] = [6, 10, 14, 6, 10, 14]

        if isProcessing {
            for (i, bar) in bars.enumerated() {
                let idx = i % 3
                let delay = Double(2 - idx) * 3.0
                let t = pulsePhase * 2.5 - delay
                let spike = max(0, sin(t)) * exp(-0.3 * max(0, t.truncatingRemainder(dividingBy: .pi * 2)))
                let maxH: CGFloat = maxHeights[i]
                let barH = max(2, maxH * CGFloat(spike))
                bar.frame = NSRect(x: bar.frame.origin.x, y: (h - barH) / 2, width: bar.frame.width, height: barH)
            }
        } else {
            for (i, bar) in bars.enumerated() {
                let idx = i % 3
                let delay = Double(idx) * 3.0
                let t = pulsePhase * 2.0 - delay
                let spike = max(0, sin(t)) * exp(-0.2 * max(0, t.truncatingRemainder(dividingBy: .pi * 2)))
                let maxH: CGFloat = maxHeights[i]
                let barH = max(2, maxH * CGFloat(spike))
                bar.frame = NSRect(x: bar.frame.origin.x, y: (h - barH) / 2, width: bar.frame.width, height: barH)
            }
        }
    }
}

class HUDBackground: NSView {
    override func draw(_ dirtyRect: NSRect) {
        let t = currentTheme
        let path = NSBezierPath(roundedRect: bounds, xRadius: t.cornerRadius, yRadius: t.cornerRadius)
        NSColor(calibratedRed: t.bgRed, green: t.bgGreen, blue: t.bgBlue, alpha: t.bgAlpha).setFill()
        path.fill()
    }
}

// MARK: - App Controller

class XiaBBApp: NSObject {
    var statusItem: NSStatusItem!
    var statusMenuItem: NSMenuItem!
    var toggleItem: NSMenuItem!
    var iconIdle: NSImage?
    var iconRec: NSImage?
    var menuItems: [String: NSMenuItem] = [:]

    let recorder = AudioRecorder()
    let onboardingWindow = OnboardingWindow()
    var isOnboarding = false
    var lastTranscription = ""
    var liveSession: LiveSession?
    var hud: HUDOverlay!
    var latestDMGUrl: String?
    var liveSendTimer: Timer?
    var liveReconnectTimer: Timer?
    var liveAccumulatedText = "" // carries text across reconnections
    var lastSentChunk = 0
    var isTranscribing = false
    var tickCount = 0
    var idleTickCounter = 0

    var fnHeld = false
    var activeMode: SmartMode = .dictation
    var recordingStartTime: Date?
    var minRecordingDuration: TimeInterval = {
        // Configurable via .config.json "min_duration", default 2.0s
        return (loadConfig()["min_duration"] as? Double) ?? 2.0
    }()

    func setup() {
        let app = NSApplication.shared
        app.setActivationPolicy(.accessory)

        hud = HUDOverlay()

        // Load icons from bundle resources
        iconIdle = loadIcon(name: "icon", template: true)
        iconRec = loadIcon(name: "icon-red", template: false)
        if iconIdle == nil {
            iconIdle = NSImage(systemSymbolName: "mic.fill", accessibilityDescription: APP_NAME)
            iconIdle?.isTemplate = true
        }
        if iconRec == nil { iconRec = iconIdle }

        // Menu bar
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        statusItem.button?.image = iconIdle
        statusItem.button?.toolTip = APP_NAME

        let menu = NSMenu()

        let title = NSMenuItem(title: "XiaBB 🦞", action: nil, keyEquivalent: "")
        title.isEnabled = false
        menu.addItem(title)

        statusMenuItem = NSMenuItem(title: "\(L("idle")) — \(usage.statusLine())", action: nil, keyEquivalent: "")
        statusMenuItem.isEnabled = false
        menu.addItem(statusMenuItem)

        menu.addItem(.separator())

        let hotkey = NSMenuItem(title: L("hotkey"), action: nil, keyEquivalent: "")
        hotkey.isEnabled = false
        menu.addItem(hotkey)
        menuItems["hotkey"] = hotkey

        menu.addItem(.separator())

        toggleItem = NSMenuItem(title: L("start"), action: #selector(toggleRecording), keyEquivalent: "")
        toggleItem.target = self
        menu.addItem(toggleItem)
        menuItems["toggle"] = toggleItem

        menu.addItem(.separator())

        let apiItem = NSMenuItem(title: L("configure_api"), action: #selector(configureAPI), keyEquivalent: "")
        apiItem.target = self
        menu.addItem(apiItem)
        menuItems["api"] = apiItem

        let dictItem = NSMenuItem(title: currentLang == "zh" ? "自定义词汇表..." : "Custom Dictionary...", action: #selector(editDictionary), keyEquivalent: "d")
        dictItem.target = self
        menu.addItem(dictItem)

        let copyLastItem = NSMenuItem(title: currentLang == "zh" ? "复制上一句" : "Copy Last Result", action: #selector(copyLastResult), keyEquivalent: "c")
        copyLastItem.target = self
        menu.addItem(copyLastItem)

        let launchItem = NSMenuItem(title: L("launch_login"), action: #selector(toggleLaunchAtLogin), keyEquivalent: "")
        launchItem.target = self
        launchItem.state = isLaunchAtLogin() ? .on : .off
        menu.addItem(launchItem)
        menuItems["launch"] = launchItem

        menu.addItem(.separator())

        let langItem = NSMenuItem(title: L("language"), action: nil, keyEquivalent: "")
        let langMenu = NSMenu()

        let enItem = NSMenuItem(title: "English", action: #selector(setLangEN), keyEquivalent: "")
        enItem.target = self
        enItem.state = currentLang == "en" ? .on : .off
        langMenu.addItem(enItem)
        menuItems["en"] = enItem

        let zhItem = NSMenuItem(title: "中文", action: #selector(setLangZH), keyEquivalent: "")
        zhItem.target = self
        zhItem.state = currentLang == "zh" ? .on : .off
        langMenu.addItem(zhItem)
        menuItems["zh"] = zhItem

        langItem.submenu = langMenu
        menu.addItem(langItem)
        menuItems["lang"] = langItem

        // Theme selector
        let themeItem = NSMenuItem(title: currentLang == "zh" ? "皮肤 / Theme" : "Theme", action: nil, keyEquivalent: "")
        let themeMenu = NSMenu()
        for (id, theme) in themeList {
            let item = NSMenuItem(title: theme.name, action: #selector(switchTheme(_:)), keyEquivalent: "")
            item.target = self
            item.representedObject = id
            item.state = (loadConfig()["theme"] as? String ?? "lobster") == id ? .on : .off
            themeMenu.addItem(item)
        }
        themeItem.submenu = themeMenu
        menu.addItem(themeItem)

        // Permissions / Settings
        let permItem = NSMenuItem(title: OB("perm_menu"), action: #selector(showPermissions), keyEquivalent: ",")
        permItem.target = self
        menu.addItem(permItem)
        menuItems["perm"] = permItem

        menu.addItem(.separator())

        let feedbackItem = NSMenuItem(title: L("feedback"), action: #selector(sendFeedback), keyEquivalent: "")
        feedbackItem.target = self
        menu.addItem(feedbackItem)
        menuItems["feedback"] = feedbackItem

        let updateItem = NSMenuItem(title: L("check_update"), action: #selector(checkForUpdates), keyEquivalent: "")
        updateItem.target = self
        menu.addItem(updateItem)
        menuItems["update"] = updateItem

        menu.addItem(.separator())

        let quitItem = NSMenuItem(title: L("quit"), action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        menuItems["quit"] = quitItem

        statusItem.menu = menu

        // UI tick timer — fast when active, slow when idle
        Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            // Skip ticks when idle to save CPU (only tick every 20th cycle = 1/sec)
            if !self.recorder.isRecording && !self.isTranscribing {
                self.idleTickCounter += 1
                if self.idleTickCounter % 20 != 0 { return }
            } else {
                self.idleTickCounter = 0
            }
            self.tick()
        }

        // Setup event tap for Globe key
        setupEventTap()

        log("🦞 \(APP_NAME) — Native Swift Voice-to-Text")
        log("   Model:  \(MODEL_REST) + \(MODEL_LIVE)")
        log("   Quota:  \(usage.statusLine())")
        log("   API key: \(apiKey.isEmpty ? "❌ MISSING" : "✅ set")")
        log("   Hotkey: 🌐 Globe (fn) — hold to speak")
        log("   HUD:    drag to reposition")
        log("✅ Ready!")

        // Request microphone permission on first launch
        // The system dialog appears when user first tries to record (AVAudioEngine.start)
        // For now just use AVCaptureDevice to pre-request — the real dialog
        // will appear on first Globe key press if this doesn't trigger it
        if AVCaptureDevice.authorizationStatus(for: .audio) == .notDetermined {
            AVCaptureDevice.requestAccess(for: .audio) { granted in
                log("🎤 Microphone: \(granted ? "granted" : "denied")")
            }
        }

        // Auto-show onboarding on first launch or if any permission is missing
        let hasSeenOnboarding = loadConfig()["onboarded"] as? Bool ?? false
        let missingPerms = !AXIsProcessTrusted()
            || AVCaptureDevice.authorizationStatus(for: .audio) != .authorized
            || apiKey.isEmpty
        if !hasSeenOnboarding || missingPerms {
            isOnboarding = true
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) { [weak self] in
                self?.onboardingWindow.show()
            }
        }

        // Silent update check on launch (after 5s to not block startup)
        DispatchQueue.main.asyncAfter(deadline: .now() + 5) { [weak self] in
            self?.silentUpdateCheck()
        }
    }

    private func silentUpdateCheck() {
        let current = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "0.0.0"
        let url = URL(string: "https://api.github.com/repos/dyz2102/xiabb/releases/latest")!
        var req = URLRequest(url: url)
        req.timeoutInterval = 10
        URLSession.shared.dataTask(with: req) { [weak self] data, _, _ in
            guard let data = data,
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let tag = json["tag_name"] as? String else { return }
            let latest = tag.hasPrefix("v") ? String(tag.dropFirst()) : tag
            guard let self = self, self.isNewer(latest, than: current) else { return }

            // Check if user skipped this version
            let cfg = loadConfig()
            if let skipped = cfg["skipped_version"] as? String, skipped == latest { return }

            // Store DMG url
            if let assets = json["assets"] as? [[String: Any]],
               let dmg = assets.first(where: { ($0["name"] as? String)?.hasSuffix(".dmg") == true }),
               let dlUrl = dmg["browser_download_url"] as? String {
                self.latestDMGUrl = dlUrl
            } else if let htmlUrl = json["html_url"] as? String {
                self.latestDMGUrl = htmlUrl
            }

            // Parse release notes
            let notes = json["body"] as? String ?? ""

            DispatchQueue.main.async {
                self.menuItems["update"]?.title = "🔴 \(L("update_now")) (v\(latest))"
                self.menuItems["update"]?.action = #selector(self.openUpdate)
                log("🔔 Update available: v\(latest) (current: v\(current))")
                self.showUpdateAlert(current: current, latest: latest, notes: notes)
            }
        }.resume()
    }

    private func showUpdateAlert(current: String, latest: String, notes: String) {
        let zh = currentLang == "zh"
        let alert = NSAlert()
        alert.alertStyle = .informational
        alert.messageText = zh
            ? "🦞 虾BB 有新版本！"
            : "🦞 XiaBB Update Available!"
        alert.informativeText = zh
            ? "当前版本: v\(current)\n最新版本: v\(latest)\n\n\(formatNotes(notes))"
            : "Current: v\(current)\nLatest: v\(latest)\n\n\(formatNotes(notes))"

        // Buttons: rightmost is index 1000, then 1001, 1002...
        alert.addButton(withTitle: zh ? "下载更新" : "Download Update")
        alert.addButton(withTitle: zh ? "稍后提醒" : "Remind Me Later")
        alert.addButton(withTitle: zh ? "跳过此版本" : "Skip This Version")

        let response = alert.runModal()
        switch response {
        case .alertFirstButtonReturn:  // Download
            openUpdate()
        case .alertThirdButtonReturn:  // Skip
            var cfg = loadConfig()
            cfg["skipped_version"] = latest
            saveConfig(cfg)
            log("⏭️ Skipped version v\(latest)")
        default:  // Remind Later — do nothing, will check again next launch
            break
        }
    }

    private func formatNotes(_ notes: String) -> String {
        // Extract a clean summary from markdown release notes
        let lines = notes.components(separatedBy: .newlines)
            .map { $0.trimmingCharacters(in: .whitespaces) }
            .filter { !$0.isEmpty && !$0.hasPrefix("---") && !$0.hasPrefix("macOS") }
        let summary = lines.prefix(12).joined(separator: "\n")
        if summary.isEmpty { return "" }
        return summary
    }

    func loadIcon(name: String, template: Bool) -> NSImage? {
        // Try bundle resources first, then ~/Tools/xiabb/
        let paths = [
            Bundle.main.resourceURL?.appendingPathComponent("\(name)@2x.png"),
            Bundle.main.resourceURL?.appendingPathComponent("\(name).png"),
            dataDir.appendingPathComponent("\(name)@2x.png"),
            dataDir.appendingPathComponent("\(name).png"),
        ].compactMap { $0 }

        for path in paths {
            if let img = NSImage(contentsOf: path) {
                let sz = img.size
                if sz.height > 0 {
                    let scale = 18.0 / sz.height
                    img.size = NSSize(width: sz.width * scale, height: 18)
                }
                img.isTemplate = template
                return img
            }
        }
        return nil
    }

    // MARK: - Event Tap

    func setupEventTap() {
        log("Setting up event tap...")

        // Check accessibility permission first
        let trusted = AXIsProcessTrusted()
        log("AXIsProcessTrusted: \(trusted)")

        if !trusted {
            log("⚠️ Not trusted for accessibility — prompting user")

            // Trigger system accessibility permission prompt
            let opts = [kAXTrustedCheckOptionPrompt.takeUnretainedValue(): true] as CFDictionary
            AXIsProcessTrustedWithOptions(opts)

            // Listen for accessibility permission change via system notification (no polling)
            DistributedNotificationCenter.default().addObserver(
                forName: NSNotification.Name("com.apple.accessibility.api"),
                object: nil, queue: .main
            ) { [weak self] _ in
                if AXIsProcessTrusted() {
                    log("✅ Accessibility granted! Setting up event tap...")
                    self?.setupEventTapCore()
                    DistributedNotificationCenter.default().removeObserver(self as Any)
                }
            }

            log("   Listening for Accessibility permission change...")
            return
        }

        setupEventTapCore()
    }

    private var eventTap: CFMachPort?

    func setupEventTapCore() {
        let eventMask: CGEventMask = (1 << CGEventType.flagsChanged.rawValue) | (1 << CGEventType.keyDown.rawValue)

        XiaBBApp.shared = self

        guard let tap = CGEvent.tapCreate(
            tap: .cgSessionEventTap,
            place: .headInsertEventTap,
            options: .defaultTap,
            eventsOfInterest: eventMask,
            callback: { proxy, type, event, refcon in
                // tapDisabledByTimeout — re-enable IMMEDIATELY
                if type == .tapDisabledByTimeout || type.rawValue == 0xFFFFFFFF {
                    if let tap = XiaBBApp.shared?.eventTap {
                        CGEvent.tapEnable(tap: tap, enable: true)
                        DispatchQueue.global().async { log("⚠️ Event tap re-enabled (was disabled by timeout)") }
                    }
                    return Unmanaged.passUnretained(event)
                }
                if type == .flagsChanged {
                    XiaBBApp.shared?.handleFlagsChanged(event)
                } else if type == .keyDown {
                    // Swallow mode-switch keys (`, 1, 2) while Globe is held
                    if let app = XiaBBApp.shared, app.fnHeld {
                        let keyCode = event.getIntegerValueField(.keyboardEventKeycode)
                        if keyCode == 50 || keyCode == 18 || keyCode == 19 || keyCode == 53 { // `, 1, 2, Esc
                            app.handleKeyDown(event)
                            return nil  // suppress — don't pass to app
                        }
                    }
                    XiaBBApp.shared?.handleKeyDown(event)
                }
                return Unmanaged.passUnretained(event)
            },
            userInfo: nil
        ) else {
            log("❌ CGEvent.tapCreate returned nil (AXIsProcessTrusted=\(AXIsProcessTrusted()))")
            return
        }

        self.eventTap = tap
        let runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, tap, 0)
        CFRunLoopAddSource(CFRunLoopGetMain(), runLoopSource, .defaultMode)
        CGEvent.tapEnable(tap: tap, enable: true)
        log("✅ Event tap created and enabled")

        // Watchdog: re-enable event tap every 5 seconds in case it was silently disabled
        Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { [weak self] _ in
            guard let tap = self?.eventTap else { return }
            if !CGEvent.tapIsEnabled(tap: tap) {
                CGEvent.tapEnable(tap: tap, enable: true)
                log("⚠️ Watchdog re-enabled event tap")
            }
        }
    }

    static var shared: XiaBBApp?

    // Detect number keys (1/2) pressed while Globe is held — switch smart mode
    func handleKeyDown(_ event: CGEvent) {
        guard fnHeld else { return }
        let keyCode = event.getIntegerValueField(.keyboardEventKeycode)
        // keyCode 50 = "`" (grave/backtick, left of 1), 18 = "1", 19 = "2"
        switch keyCode {
        case 50: // "`" key — toggle translate
            let newMode: SmartMode = activeMode == .translate ? .dictation : .translate
            activeMode = newMode
            DispatchQueue.main.async { [weak self] in
                log(newMode == .dictation ? "🎤 Back to dictation" : "🔄 Smart mode: translate")
                self?.hud.setMode(newMode)
            }
        case 18: // "1" key — toggle prompt
            let newMode: SmartMode = activeMode == .prompt ? .dictation : .prompt
            activeMode = newMode
            DispatchQueue.main.async { [weak self] in
                log(newMode == .dictation ? "🎤 Back to dictation" : "⚡ Smart mode: prompt")
                self?.hud.setMode(newMode)
            }
        case 19: // "2" key — toggle email
            let newMode: SmartMode = activeMode == .email ? .dictation : .email
            activeMode = newMode
            DispatchQueue.main.async { [weak self] in
                log(newMode == .dictation ? "🎤 Back to dictation" : "📧 Smart mode: email")
                self?.hud.setMode(newMode)
            }
        case 53: // Esc key — cancel recording
            log("⛔ Recording cancelled by Esc")
            cancelRecording()
        default:
            break
        }
    }

    func cancelRecording() {
        guard recorder.isRecording else { return }
        recorder.audioQueue.async { [weak self] in
            _ = self?.recorder.stop()  // discard frames
            self?.liveSession?.stop()
            self?.liveSession = nil
            self?.liveAccumulatedText = ""
            DispatchQueue.main.async {
                self?.liveSendTimer?.invalidate()
                self?.liveSendTimer = nil
                self?.liveReconnectTimer?.invalidate()
                self?.liveReconnectTimer = nil
                self?.hud.hide()
            }
        }
        fnHeld = false  // reset so Globe UP doesn't trigger stopRecording
    }

    // MUST be extremely fast — macOS disables the tap if callback is slow
    func handleFlagsChanged(_ event: CGEvent) {
        let fnNow = (event.flags.rawValue & FN_FLAG) != 0
        if fnNow && !fnHeld {
            fnHeld = true
            activeMode = .dictation  // reset mode each press, number key changes it
            // Serialize on audio queue to prevent concurrent AVAudioEngine access
            recorder.audioQueue.async { [weak self] in
                log("🌐 Globe DOWN")
                self?.startRecording()
            }
            // Also notify onboarding if active
            if isOnboarding {
                DispatchQueue.main.async { [weak self] in
                    self?.onboardingWindow.onGlobeEvent(pressed: true)
                }
            }
        } else if !fnNow && fnHeld {
            fnHeld = false
            // Serialize on audio queue to prevent concurrent AVAudioEngine access
            recorder.audioQueue.async { [weak self] in
                log("🌐 Globe UP")
                self?.stopRecording()
            }
            // Also notify onboarding if active
            if isOnboarding {
                DispatchQueue.main.async { [weak self] in
                    self?.onboardingWindow.onGlobeEvent(pressed: false)
                }
            }
        }
    }

    // MARK: - Recording

    func startRecording() {
        guard !recorder.isRecording else { return }
        log("🎙 Starting recording...")
        recordingStartTime = Date()

        playSound(sfxStart())

        DispatchQueue.main.async { [weak self] in
            self?.hud.show(text: L("listening"))
        }

        recorder.start()

        // If start() failed (no mic), show error and bail
        guard recorder.isRecording else {
            log("⚠️ Recording did not start (no mic?)")
            DispatchQueue.main.async { [weak self] in
                self?.hud.show(text: "🎤 No microphone detected")
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) { [weak self] in
                self?.hud.hide()
            }
            return
        }

        lastSentChunk = 0

        // Start live session for real-time preview
        liveAccumulatedText = ""
        startNewLiveSession()

        // Timer to send audio chunks to live session
        DispatchQueue.main.async { [weak self] in
            self?.liveSendTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
                guard let self = self, self.recorder.isRecording else { return }
                let frames = self.recorder.getFramesSoFar()
                let newFrames = Array(frames.dropFirst(self.lastSentChunk))
                self.lastSentChunk = frames.count
                if !newFrames.isEmpty {
                    for frame in newFrames {
                        self.liveSession?.sendAudio(frame)
                    }
                }
            }

            // Reconnect live session every 15s to prevent degradation
            self?.liveReconnectTimer = Timer.scheduledTimer(withTimeInterval: 15.0, repeats: true) { [weak self] _ in
                guard let self = self, self.recorder.isRecording else { return }
                // Save text from current session before reconnecting
                if let currentSession = self.liveSession {
                    let sessionText = currentSession.currentText
                    if !sessionText.isEmpty && !self.liveAccumulatedText.isEmpty {
                        self.liveAccumulatedText += " "
                    }
                    self.liveAccumulatedText += sessionText
                    log("[live] 🔄 Reconnecting (15s). Accumulated: \(self.liveAccumulatedText.count) chars")
                    currentSession.stop()
                }
                self.startNewLiveSession()
            }
        }
        log("🎙 Recording started")
    }

    func startNewLiveSession() {
        liveSession = LiveSession()
        liveSession?.start { [weak self] sessionText in
            guard let self = self else { return }
            // Combine accumulated text from previous sessions + current session text
            let fullText = self.liveAccumulatedText + sessionText
            let display = fullText.count > 60 ? String(fullText.suffix(60)) : fullText
            self.hud.updateText(display)
        }
    }

    func stopRecording() {
        guard recorder.isRecording else { return }

        let duration = recordingStartTime.map { Date().timeIntervalSince($0) } ?? 0
        log("🎙 Stopping recording... (\(String(format: "%.2f", duration))s)")

        let frames = recorder.stop()

        DispatchQueue.main.async { [weak self] in
            self?.liveSendTimer?.invalidate()
            self?.liveSendTimer = nil
            self?.liveReconnectTimer?.invalidate()
            self?.liveReconnectTimer = nil
        }
        liveSession?.stop()
        liveSession = nil
        liveAccumulatedText = ""

        // Ignore accidental taps (< minRecordingDuration, default 2.0s)
        if duration < minRecordingDuration {
            log("  ⏭ Too short (\(String(format: "%.2f", duration))s < \(minRecordingDuration)s) — discarded")
            DispatchQueue.main.async { [weak self] in self?.hud.hide() }
            return
        }

        playSound(sfxStop())

        isTranscribing = true
        let finalizingLabel: String
        switch activeMode {
        case .dictation: finalizingLabel = L("finalizing")
        case .translate: finalizingLabel = currentLang == "zh" ? "翻译中..." : "Translating..."
        case .prompt: finalizingLabel = currentLang == "zh" ? "优化中..." : "Optimizing..."
        case .email: finalizingLabel = currentLang == "zh" ? "生成邮件..." : "Composing..."
        }
        DispatchQueue.main.async { [weak self] in
            self?.hud.isProcessing = true
            self?.hud.updateText(finalizingLabel)
        }

        guard !frames.isEmpty else {
            log("  No audio frames captured")
            isTranscribing = false
            DispatchQueue.main.async { [weak self] in self?.hud.hide() }
            return
        }

        guard usage.remaining > 0 else {
            isTranscribing = false
            playSound(sfxError())
            DispatchQueue.main.async { [weak self] in
                self?.hud.showResult("\(L("daily_limit")) (\(DAILY_FREE_LIMIT))", isError: true)
            }
            return
        }

        let (wavData, audioDuration) = encodeToWAV(frames: frames)
        log("  Audio: \(String(format: "%.1f", audioDuration))s, \(wavData.count) bytes, \(frames.count) chunks")

        let mode = activeMode
        if mode != .dictation {
            log("🧠 Smart mode: \(mode.rawValue)")
        }

        transcribeREST(wavData: wavData, mode: mode) { [weak self] result in
            guard let self = self else { return }
            self.isTranscribing = false
            switch result {
            case .success(let text):
                let count = usage.increment()
                log("✅ [\(count)/\(DAILY_FREE_LIMIT)] \(text)")
                playSound(sfxDone())
                DispatchQueue.main.async { [weak self] in
                    self?.hud.showResult(text)
                }
                self.lastTranscription = text
                if self.isOnboarding {
                    DispatchQueue.main.async { [weak self] in
                        self?.onboardingWindow.webView?.callAsyncJavaScript(
                            "onTranscriptionResult(text)",
                            arguments: ["text": text],
                            in: nil, in: .page, completionHandler: nil
                        )
                    }
                }
                // Always copy and paste, even during onboarding
                self.copyAndPaste(text)
            case .failure(let error):
                log("❌ Transcription error: \(error.localizedDescription)")
                playSound(sfxError())
                let msg = Self.friendlyError(error)
                DispatchQueue.main.async { [weak self] in
                    self?.hud.showResult(msg, isError: true)
                }
            }
        }
    }

    static func friendlyError(_ error: Error) -> String {
        let desc = error.localizedDescription.lowercased()
        let nsErr = error as NSError
        let zh = currentLang == "zh"

        // Network unreachable / no internet
        if nsErr.code == NSURLErrorNotConnectedToInternet
            || nsErr.code == NSURLErrorNetworkConnectionLost
            || desc.contains("network") && desc.contains("lost") {
            return zh ? "⚠️ 无网络连接" : "⚠️ No network"
        }
        // DNS / hostname not found
        if nsErr.code == NSURLErrorCannotFindHost
            || desc.contains("hostname could not be found") {
            return zh ? "⚠️ DNS解析失败" : "⚠️ DNS failed"
        }
        // Timeout
        if nsErr.code == NSURLErrorTimedOut || desc.contains("timed out") {
            return zh ? "⚠️ 请求超时" : "⚠️ Request timed out"
        }
        // SSL / certificate
        if nsErr.code == NSURLErrorSecureConnectionFailed
            || nsErr.code == NSURLErrorServerCertificateUntrusted
            || desc.contains("ssl") || desc.contains("certificate") {
            return zh ? "⚠️ SSL连接错误" : "⚠️ SSL error"
        }
        // API key invalid
        if desc.contains("api key") || desc.contains("permission") || desc.contains("403") {
            return zh ? "⚠️ API Key无效" : "⚠️ Invalid API Key"
        }
        // Rate limit
        if desc.contains("rate") || desc.contains("429") || desc.contains("quota") {
            return zh ? "⚠️ API限流，稍后重试" : "⚠️ Rate limited, retry later"
        }
        // Server error
        if desc.contains("500") || desc.contains("503") || desc.contains("internal server") {
            return zh ? "⚠️ Gemini服务故障" : "⚠️ Gemini server error"
        }
        // No speech
        if desc.contains("no speech") || nsErr.code == -2 {
            return zh ? "🤫 未检测到语音" : "🤫 No speech detected"
        }
        // Fallback — truncate to keep HUD readable
        let short = error.localizedDescription
        if short.count > 30 {
            return "⚠️ " + String(short.prefix(28)) + "…"
        }
        return "⚠️ " + short
    }

    func copyAndPaste(_ text: String) {
        // Copy to clipboard
        DispatchQueue.main.async {
            NSPasteboard.general.clearContents()
            let success = NSPasteboard.general.setString(text, forType: .string)
            log("📋 Clipboard: \(success ? "OK" : "FAILED")")

            // Simulate Cmd+V after a short delay
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                let src = CGEventSource(stateID: .hidSystemState)
                // V key = 0x09
                if let keyDown = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: true),
                   let keyUp = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: false) {
                    keyDown.flags = .maskCommand
                    keyDown.post(tap: .cghidEventTap)
                    keyUp.flags = .maskCommand
                    keyUp.post(tap: .cghidEventTap)
                    log("📋 Cmd+V posted")
                } else {
                    log("❌ Failed to create CGEvent for Cmd+V")
                    // Fallback: use osascript
                    DispatchQueue.global().async {
                        let proc = Process()
                        proc.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
                        proc.arguments = ["-e", "tell application \"System Events\" to keystroke \"v\" using command down"]
                        try? proc.run()
                        proc.waitUntilExit()
                        log("📋 osascript Cmd+V fallback: exit \(proc.terminationStatus)")
                    }
                }
            }
        }
    }

    // MARK: - Menu Actions

    @objc func toggleRecording() {
        if recorder.isRecording {
            recorder.audioQueue.async { [weak self] in
                self?.stopRecording()
            }
        } else {
            recorder.audioQueue.async { [weak self] in
                self?.startRecording()
            }
        }
    }

    @objc func copyLastResult() {
        guard !lastTranscription.isEmpty else { return }
        NSPasteboard.general.clearContents()
        NSPasteboard.general.setString(lastTranscription, forType: .string)
        log("📋 Copied last: \(lastTranscription.prefix(50))")
    }

    @objc func editDictionary() {
        DispatchQueue.global(qos: .userInitiated).async {
            let words = loadDictionary()
            // Escape for AppleScript string literal: backslashes then double-quotes
            let current = words.joined(separator: ", ")
                .replacingOccurrences(of: "\\", with: "\\\\")
                .replacingOccurrences(of: "\"", with: "\\\"")
            let prompt = currentLang == "zh"
                ? "编辑自定义词汇表（逗号分隔）\\n\\n这些词会被精确识别，不会被替换成发音相似的词。\\n例如：Claude 不会被识别成 cloud"
                : "Edit custom dictionary (comma-separated)\\n\\nThese words will be transcribed exactly as written.\\nExample: Claude won't be misheard as cloud"
            let script = """
            tell application "System Events"
              display dialog "\(prompt)" default answer "\(current)" with title "虾BB Dictionary" buttons {"Cancel", "Save"} default button "Save"
              set theWords to text returned of result
              return theWords
            end tell
            """
            let proc = Process()
            proc.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
            proc.arguments = ["-e", script]
            let pipe = Pipe()
            proc.standardOutput = pipe
            proc.standardError = Pipe()
            try? proc.run()
            proc.waitUntilExit()
            let output = String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
            if proc.terminationStatus == 0 && !output.isEmpty {
                let newWords = output.split(separator: ",").map { $0.trimmingCharacters(in: .whitespaces) }.filter { !$0.isEmpty }
                saveDictionary(newWords)
                log("📖 Dictionary updated: \(newWords.count) words")
                let p2 = Process()
                p2.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
                p2.arguments = ["-e", "tell application \"System Events\" to display notification \"词汇表已保存 ✅ (\(newWords.count) 个词)\" with title \"虾BB\""]
                try? p2.run()
            }
        }
    }

    @objc func configureAPI() {
        // Show current key masked (first 8 + *** + last 4)
        let currentDisplay: String
        if apiKey.isEmpty {
            currentDisplay = ""
        } else if apiKey.count > 16 {
            currentDisplay = String(apiKey.prefix(8)) + "****" + String(apiKey.suffix(4))
        } else {
            currentDisplay = String(apiKey.prefix(4)) + "****"
        }
        let prompt = currentLang == "zh"
            ? "输入 Gemini API Key\\n(免费获取: aistudio.google.com/apikey)\\n\\n留空点 Save 不会清除已有 Key"
            : "Enter Gemini API Key\\n(Free: aistudio.google.com/apikey)\\n\\nLeave empty + Save won't clear existing key"
        let script = """
        tell application "System Events"
          display dialog "\(prompt)" default answer "\(currentDisplay)" with title "XiaBB API Config" buttons {"Cancel", "Save"} default button "Save"
          set theKey to text returned of result
          return theKey
        end tell
        """
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
        proc.arguments = ["-e", script]
        let pipe = Pipe()
        proc.standardOutput = pipe
        proc.standardError = Pipe()
        try? proc.run()
        proc.waitUntilExit()
        let output = String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        // Only save if user entered a new key (not the masked display)
        if proc.terminationStatus == 0 && !output.isEmpty && output != currentDisplay {
            let keyFile = dataDir.appendingPathComponent(".api-key")
            try? output.write(to: keyFile, atomically: true, encoding: .utf8)
            try? FileManager.default.setAttributes([.posixPermissions: 0o600], ofItemAtPath: keyFile.path)
            apiKey = output
            log("🔑 API key saved")
            // Show confirmation
            let confirmScript = """
            tell application "System Events"
              display notification "API Key 已保存 ✅" with title "XiaBB"
            end tell
            """
            let p2 = Process()
            p2.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
            p2.arguments = ["-e", confirmScript]
            try? p2.run()
        }
    }

    @objc func toggleLaunchAtLogin() {
        let currently = isLaunchAtLogin()
        setLaunchAtLogin(!currently)
        menuItems["launch"]?.state = currently ? .off : .on
    }

    @objc func setLangEN() {
        currentLang = "en"
        saveConfig(["lang": "en"])
        refreshMenuTitles()
    }

    @objc func setLangZH() {
        currentLang = "zh"
        saveConfig(["lang": "zh"])
        refreshMenuTitles()
    }

    @objc func switchTheme(_ sender: NSMenuItem) {
        guard let themeId = sender.representedObject as? String,
              let theme = themes[themeId] else { return }
        currentTheme = theme
        saveConfig(["theme": themeId])
        // Update checkmarks
        if let themeMenu = sender.menu {
            for item in themeMenu.items { item.state = .off }
        }
        sender.state = .on
        // Rebuild HUD with new theme
        hud = HUDOverlay()
        log("🎨 Theme: \(theme.name)")
    }

    @objc func showPermissions() {
        onboardingWindow.show()
    }

    @objc func sendFeedback() {
        let ver = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"
        let subject = "XiaBB Feedback (v\(ver))"
            .addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? ""
        let body = (currentLang == "zh"
            ? "请在下方描述你的反馈:\n\n"
            : "Please describe your feedback below:\n\n")
            .addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? ""
        if let url = URL(string: "mailto:ZBOT6996@gmail.com?subject=\(subject)&body=\(body)") {
            NSWorkspace.shared.open(url)
        }
    }

    @objc func checkForUpdates() {
        let current = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "0.0.0"
        menuItems["update"]?.title = currentLang == "zh" ? "检查中..." : "Checking..."

        let url = URL(string: "https://api.github.com/repos/dyz2102/xiabb/releases/latest")!
        var req = URLRequest(url: url)
        req.timeoutInterval = 10
        URLSession.shared.dataTask(with: req) { [weak self] data, _, error in
            DispatchQueue.main.async {
                guard let self = self else { return }
                if error != nil || data == nil {
                    self.menuItems["update"]?.title = L("check_update")
                    let alert = NSAlert()
                    alert.alertStyle = .warning
                    alert.messageText = currentLang == "zh" ? "检查更新失败" : "Update Check Failed"
                    alert.informativeText = currentLang == "zh" ? "无法连接到服务器，请检查网络连接。" : "Could not connect to server. Check your network."
                    alert.addButton(withTitle: "OK")
                    alert.runModal()
                    return
                }
                guard let json = try? JSONSerialization.jsonObject(with: data!) as? [String: Any],
                      let tag = json["tag_name"] as? String else {
                    self.menuItems["update"]?.title = L("check_update")
                    return
                }
                let latest = tag.hasPrefix("v") ? String(tag.dropFirst()) : tag
                if self.isNewer(latest, than: current) {
                    // Store DMG url
                    if let assets = json["assets"] as? [[String: Any]],
                       let dmg = assets.first(where: { ($0["name"] as? String)?.hasSuffix(".dmg") == true }),
                       let dlUrl = dmg["browser_download_url"] as? String {
                        self.latestDMGUrl = dlUrl
                    } else if let htmlUrl = json["html_url"] as? String {
                        self.latestDMGUrl = htmlUrl
                    }
                    self.menuItems["update"]?.title = "🔴 \(L("update_now")) (v\(latest))"
                    self.menuItems["update"]?.action = #selector(self.openUpdate)
                    let notes = json["body"] as? String ?? ""
                    // Manual check always shows alert (ignores skipped_version)
                    self.showUpdateAlert(current: current, latest: latest, notes: notes)
                } else {
                    self.menuItems["update"]?.title = L("check_update")
                    let alert = NSAlert()
                    alert.alertStyle = .informational
                    alert.messageText = currentLang == "zh" ? "✅ 已是最新版本" : "✅ You're Up to Date"
                    alert.informativeText = currentLang == "zh"
                        ? "当前版本 v\(current) 已是最新。"
                        : "Version v\(current) is the latest."
                    alert.addButton(withTitle: "OK")
                    alert.runModal()
                }
            }
        }.resume()
    }

    private func isNewer(_ remote: String, than local: String) -> Bool {
        let r = remote.split(separator: ".").compactMap { Int($0) }
        let l = local.split(separator: ".").compactMap { Int($0) }
        for i in 0..<max(r.count, l.count) {
            let rv = i < r.count ? r[i] : 0
            let lv = i < l.count ? l[i] : 0
            if rv > lv { return true }
            if rv < lv { return false }
        }
        return false
    }

    @objc func openUpdate() {
        let urlStr = latestDMGUrl ?? "https://github.com/dyz2102/xiabb/releases/latest"
        if let url = URL(string: urlStr) {
            NSWorkspace.shared.open(url)
        }
    }

    @objc func quit() {
        NSApp.terminate(nil)
    }

    func refreshMenuTitles() {
        menuItems["hotkey"]?.title = L("hotkey")
        menuItems["toggle"]?.title = recorder.isRecording ? L("stop") : L("start")
        menuItems["api"]?.title = L("configure_api")
        menuItems["launch"]?.title = L("launch_login")
        menuItems["lang"]?.title = L("language")
        menuItems["quit"]?.title = L("quit")
        menuItems["feedback"]?.title = L("feedback")
        // Only reset update title if no update is pending
        if menuItems["update"]?.action == #selector(checkForUpdates) {
            menuItems["update"]?.title = L("check_update")
        }
        menuItems["en"]?.state = currentLang == "en" ? .on : .off
        menuItems["zh"]?.state = currentLang == "zh" ? .on : .off
    }

    // MARK: - Launch at Login

    let plistPath = URL(fileURLWithPath: NSHomeDirectory())
        .appendingPathComponent("Library/LaunchAgents/com.xiabb.plist")

    func isLaunchAtLogin() -> Bool {
        FileManager.default.fileExists(atPath: plistPath.path)
    }

    func setLaunchAtLogin(_ enabled: Bool) {
        if enabled {
            let appPath = Bundle.main.bundlePath
            let plist = """
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0"><dict>
              <key>Label</key><string>com.xiabb</string>
              <key>ProgramArguments</key><array>
                <string>/usr/bin/open</string>
                <string>-a</string>
                <string>\(appPath)</string>
              </array>
              <key>RunAtLoad</key><true/>
              <key>KeepAlive</key><false/>
            </dict></plist>
            """
            try? plist.write(to: plistPath, atomically: true, encoding: .utf8)
        } else {
            try? FileManager.default.removeItem(at: plistPath)
        }
    }

    // MARK: - Tick

    func tick() {
        tickCount += 1
        hud.tickPulse()

        if let btn = statusItem.button {
            if recorder.isRecording {
                btn.image = iconRec
                btn.alphaValue = 1.0
            } else if isTranscribing {
                btn.image = iconRec
                let phase = Double(tickCount) * 0.15
                btn.alphaValue = CGFloat(0.4 + 0.6 * abs(sin(phase)))
            } else {
                btn.image = iconIdle
                btn.alphaValue = 1.0
            }
        }

        if recorder.isRecording {
            statusMenuItem.title = "\(L("recording")) — \(usage.statusLine())"
            toggleItem.title = L("stop")
        } else if isTranscribing {
            statusMenuItem.title = "\(L("transcribing")) — \(usage.statusLine())"
        } else {
            statusMenuItem.title = "\(L("idle")) — \(usage.statusLine())"
            toggleItem.title = L("start")
        }
    }
}

// MARK: - Main

if apiKey.isEmpty {
    log("⚠️ No API key — set GEMINI_API_KEY env var or create ~/Tools/xiabb/.api-key")
    log("   Get a free key at https://aistudio.google.com/apikey")
}

let app = NSApplication.shared
let controller = XiaBBApp()
controller.setup()
app.run()
