import AppKit
import AVFoundation
import CoreAudio
import Foundation
import UniformTypeIdentifiers

struct SubtitleRecord: Decodable {
    let source: String?
    let is_final: Bool?
    let segment_id: Int
    let original: String
    let translation: String
    let timestamp_end: Int?
    let emitted_at: String
}

struct LocalDraft {
    let segmentID: Int
    var text: String
    var isFinal: Bool
}

struct CommittedSegment {
    let text: String
    let translation: String
}

struct RecentProject {
    let runID: String
    let transcriptURL: URL
    let title: String
    let snippet: String
    let metaText: String
    let hasOrganizedNotes: Bool
    let runDirectory: URL
}

struct GeneratedMusicTrack {
    let id: String
    let title: String
    let metaText: String
    let audioURL: URL
    let sourceURL: URL?
    let metadataURL: URL
    let createdAt: Date
}

struct MusicStylePreset {
    let id: String
    let label: String
}

struct MusicGenerationMode {
    let id: String
    let label: String
    let shortLabel: String
}

struct OrganizationTemplate: Codable {
    let id: String
    var name: String
    var summary: String
    var prompt: String
    var isBuiltin: Bool
}

struct OrganizationTemplateStore: Codable {
    var selectedTemplateID: String
    var customTemplates: [OrganizationTemplate]
}

struct LocalFastOption {
    let id: String
    let label: String
    let modelDir: URL?

    var isDisabled: Bool { modelDir == nil }
}

struct TranslationTargetOption {
    let id: String
    let label: String
}

struct OutputVolumeControlState {
    let deviceID: AudioDeviceID
    let deviceName: String
    let channels: [UInt32]
    let percent: Int
    let isMuted: Bool
}

final class ProcessOutputCollector {
    let pipe = Pipe()
    private let lock = NSLock()
    private var bufferedData = Data()

    func attach(to process: Process) {
        process.standardOutput = pipe
        process.standardError = pipe
        pipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let chunk = handle.availableData
            guard !chunk.isEmpty else { return }
            self?.append(chunk)
        }
    }

    func finishText() -> String {
        pipe.fileHandleForReading.readabilityHandler = nil
        let remaining = pipe.fileHandleForReading.readDataToEndOfFile()
        if !remaining.isEmpty {
            append(remaining)
        }
        lock.lock()
        let data = bufferedData
        lock.unlock()
        return String(data: data, encoding: .utf8)?
            .trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    }

    private func append(_ data: Data) {
        lock.lock()
        bufferedData.append(data)
        lock.unlock()
    }
}

final class TemplatePickerAccessoryController: NSObject {
    let view: NSView
    private let templates: [OrganizationTemplate]
    private let selectedTemplateID: String
    private let inkColor: NSColor
    private let mutedInkColor: NSColor
    private let accentColor: NSColor
    private let surfaceColor: NSColor
    private let borderColor: NSColor
    private let popup: NSPopUpButton
    private let currentLabel: NSTextField
    private let kindLabel: NSTextField
    private let summaryLabel: NSTextField
    private let outputLabel: NSTextField

    init(
        templates: [OrganizationTemplate],
        selectedTemplateID: String,
        inkColor: NSColor,
        mutedInkColor: NSColor,
        accentColor: NSColor,
        surfaceColor: NSColor,
        borderColor: NSColor
    ) {
        self.templates = templates
        self.selectedTemplateID = selectedTemplateID
        self.inkColor = inkColor
        self.mutedInkColor = mutedInkColor
        self.accentColor = accentColor
        self.surfaceColor = surfaceColor
        self.borderColor = borderColor
        self.view = NSView(frame: NSRect(x: 0, y: 0, width: 430, height: 214))
        self.popup = NSPopUpButton(frame: NSRect(x: 16, y: 126, width: 398, height: 34), pullsDown: false)
        self.currentLabel = NSTextField(labelWithString: "")
        self.kindLabel = NSTextField(labelWithString: "")
        self.summaryLabel = NSTextField(wrappingLabelWithString: "")
        self.outputLabel = NSTextField(wrappingLabelWithString: "")
        super.init()
        build()
        updatePreview()
    }

    var selectedID: String {
        (popup.selectedItem?.representedObject as? String) ?? selectedTemplateID
    }

    private func build() {
        view.wantsLayer = true
        view.layer?.backgroundColor = NSColor.clear.cgColor

        let hero = NSView(frame: NSRect(x: 0, y: 164, width: 430, height: 44))
        hero.wantsLayer = true
        hero.layer?.cornerRadius = 18
        hero.layer?.backgroundColor = accentColor.withAlphaComponent(0.10).cgColor
        hero.layer?.borderWidth = 1
        hero.layer?.borderColor = accentColor.withAlphaComponent(0.18).cgColor
        view.addSubview(hero)

        let eyebrow = NSTextField(labelWithString: "整理模板")
        eyebrow.frame = NSRect(x: 16, y: 25, width: 120, height: 14)
        eyebrow.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .semibold)
        eyebrow.textColor = mutedInkColor
        hero.addSubview(eyebrow)

        currentLabel.frame = NSRect(x: 16, y: 7, width: 320, height: 20)
        currentLabel.font = NSFont(name: "SF Pro Display", size: 17) ?? .systemFont(ofSize: 17, weight: .semibold)
        currentLabel.textColor = inkColor
        hero.addSubview(currentLabel)

        kindLabel.frame = NSRect(x: 334, y: 11, width: 78, height: 22)
        kindLabel.alignment = .center
        kindLabel.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .semibold)
        kindLabel.textColor = accentColor
        kindLabel.wantsLayer = true
        kindLabel.layer?.cornerRadius = 11
        kindLabel.layer?.backgroundColor = NSColor.white.withAlphaComponent(0.66).cgColor
        kindLabel.layer?.borderWidth = 1
        kindLabel.layer?.borderColor = accentColor.withAlphaComponent(0.18).cgColor
        hero.addSubview(kindLabel)

        for template in templates {
            popup.addItem(withTitle: template.name)
            popup.lastItem?.representedObject = template.id
        }
        if let index = templates.firstIndex(where: { $0.id == selectedTemplateID }) {
            popup.selectItem(at: index)
        }
        popup.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13, weight: .medium)
        popup.target = self
        popup.action = #selector(selectionChanged)
        view.addSubview(popup)

        let preview = NSView(frame: NSRect(x: 0, y: 0, width: 430, height: 112))
        preview.wantsLayer = true
        preview.layer?.cornerRadius = 18
        preview.layer?.backgroundColor = surfaceColor.cgColor
        preview.layer?.borderWidth = 1
        preview.layer?.borderColor = borderColor.withAlphaComponent(0.76).cgColor
        view.addSubview(preview)

        let purposeTitle = NSTextField(labelWithString: "适合场景")
        purposeTitle.frame = NSRect(x: 16, y: 78, width: 90, height: 16)
        purposeTitle.font = NSFont(name: "SF Pro Text", size: 11) ?? .systemFont(ofSize: 11, weight: .semibold)
        purposeTitle.textColor = mutedInkColor
        preview.addSubview(purposeTitle)

        summaryLabel.frame = NSRect(x: 16, y: 51, width: 396, height: 30)
        summaryLabel.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        summaryLabel.textColor = inkColor
        summaryLabel.maximumNumberOfLines = 2
        preview.addSubview(summaryLabel)

        let divider = NSView(frame: NSRect(x: 16, y: 43, width: 398, height: 1))
        divider.wantsLayer = true
        divider.layer?.backgroundColor = borderColor.withAlphaComponent(0.55).cgColor
        preview.addSubview(divider)

        outputLabel.frame = NSRect(x: 16, y: 13, width: 396, height: 24)
        outputLabel.font = NSFont(name: "SF Pro Text", size: 11) ?? .systemFont(ofSize: 11)
        outputLabel.textColor = mutedInkColor
        outputLabel.maximumNumberOfLines = 2
        preview.addSubview(outputLabel)
    }

    @objc private func selectionChanged() {
        updatePreview()
    }

    private func updatePreview() {
        let template = templates.first(where: { $0.id == selectedID }) ?? templates.first
        guard let template else { return }
        currentLabel.stringValue = template.name
        kindLabel.stringValue = template.isBuiltin ? "预设" : "自定义"
        summaryLabel.stringValue = template.summary.isEmpty ? "按当前模板整理原始 ASR，并输出 Markdown 正文。" : template.summary
        let placeholderHint = template.prompt.contains("{asr}") || template.prompt.contains("{{asr}}")
            ? "已包含 ASR 占位符"
            : "会自动追加原始 ASR"
        outputLabel.stringValue = "\(placeholderHint) · 整理结果会保存到最近项目，并优先按当前模板打开。"
    }
}

private enum CompactActionButtonVariant {
    case primary
    case neutral
    case accentSoft
    case ghost
}

private enum CompactPreviewPanelMood {
    case project
    case music
}

final class OverlayWindow: NSWindow {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { true }
}

final class OverlayPanelWindow: NSWindow {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { false }
}

final class DraggableVisualEffectView: NSVisualEffectView {
    var onScroll: ((NSEvent) -> Void)?

    override func mouseDown(with event: NSEvent) {
        window?.performDrag(with: event)
    }

    override func scrollWheel(with event: NSEvent) {
        if let onScroll {
            onScroll(event)
            return
        }
        super.scrollWheel(with: event)
    }
}

class HoverTrackingButton: NSButton {
    var onHoverChanged: ((Bool) -> Void)?
    private var trackingAreaRef: NSTrackingArea?

    override func updateTrackingAreas() {
        super.updateTrackingAreas()
        if let trackingAreaRef {
            removeTrackingArea(trackingAreaRef)
        }
        let options: NSTrackingArea.Options = [.mouseEnteredAndExited, .activeInActiveApp, .inVisibleRect]
        let trackingArea = NSTrackingArea(rect: .zero, options: options, owner: self, userInfo: nil)
        addTrackingArea(trackingArea)
        trackingAreaRef = trackingArea
    }

    override func mouseEntered(with event: NSEvent) {
        super.mouseEntered(with: event)
        onHoverChanged?(true)
    }

    override func mouseExited(with event: NSEvent) {
        super.mouseExited(with: event)
        onHoverChanged?(false)
    }
}

class HoverTrackingView: NSView {
    var onHoverChanged: ((Bool) -> Void)?
    var onScroll: ((NSEvent) -> Void)?
    private var trackingAreaRef: NSTrackingArea?

    override func updateTrackingAreas() {
        super.updateTrackingAreas()
        if let trackingAreaRef {
            removeTrackingArea(trackingAreaRef)
        }
        let options: NSTrackingArea.Options = [.mouseEnteredAndExited, .activeInActiveApp, .inVisibleRect]
        let trackingArea = NSTrackingArea(rect: .zero, options: options, owner: self, userInfo: nil)
        addTrackingArea(trackingArea)
        trackingAreaRef = trackingArea
    }

    override func mouseEntered(with event: NSEvent) {
        super.mouseEntered(with: event)
        onHoverChanged?(true)
    }

    override func mouseExited(with event: NSEvent) {
        super.mouseExited(with: event)
        onHoverChanged?(false)
    }

    override func scrollWheel(with event: NSEvent) {
        if let onScroll {
            onScroll(event)
            return
        }
        super.scrollWheel(with: event)
    }
}

final class ClickableRowView: HoverTrackingView {
    var onClick: (() -> Void)?
    var onDoubleClick: (() -> Void)?

    override func mouseDown(with event: NSEvent) {
        super.mouseDown(with: event)
        if event.clickCount >= 2 {
            onDoubleClick?()
        } else {
            onClick?()
        }
    }
}

final class BubbleOrbButton: HoverTrackingView {
    var symbolImage: NSImage?

    init(title: String, target: AnyObject?, action: Selector?) {
        super.init(frame: .zero)
        wantsLayer = true
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        wantsLayer = true
    }

    override func mouseDown(with event: NSEvent) {
        window?.performDrag(with: event)
    }

    override func layout() {
        super.layout()
        wantsLayer = true
        layer?.cornerRadius = min(bounds.width, bounds.height) / 2
        layer?.masksToBounds = true
        needsDisplay = true
    }

    override func draw(_ dirtyRect: NSRect) {
        NSColor.clear.setFill()
        dirtyRect.fill()

        let orbRect = bounds.insetBy(dx: 2, dy: 2)
        let orbPath = NSBezierPath(ovalIn: orbRect)
        NSColor(calibratedRed: 0.98, green: 0.985, blue: 0.995, alpha: 0.99).setFill()
        orbPath.fill()

        NSColor(calibratedRed: 0.84, green: 0.87, blue: 0.92, alpha: 1.0).setStroke()
        orbPath.lineWidth = 1.2
        orbPath.stroke()

        if let symbolImage {
            let imageSize = NSSize(width: 34, height: 34)
            let imageRect = NSRect(
                x: bounds.midX - imageSize.width / 2,
                y: bounds.midY - imageSize.height / 2,
                width: imageSize.width,
                height: imageSize.height
            )
            symbolImage.draw(in: imageRect)
        }
    }
}

final class SatelliteOrbButton: HoverTrackingButton {
    var symbolImage: NSImage?

    override func layout() {
        super.layout()
        wantsLayer = true
        layer?.cornerRadius = min(bounds.width, bounds.height) / 2
        layer?.masksToBounds = true
        needsDisplay = true
    }

    override func draw(_ dirtyRect: NSRect) {
        NSColor.clear.setFill()
        dirtyRect.fill()

        let orbRect = bounds.insetBy(dx: 1.5, dy: 1.5)
        let orbPath = NSBezierPath(ovalIn: orbRect)
        NSColor(calibratedRed: 0.98, green: 0.985, blue: 0.995, alpha: 0.99).setFill()
        orbPath.fill()

        NSColor(calibratedRed: 0.84, green: 0.87, blue: 0.92, alpha: 1.0).setStroke()
        orbPath.lineWidth = 1.0
        orbPath.stroke()

        if let symbolImage {
            let imageSize = NSSize(width: 16, height: 16)
            let imageRect = NSRect(
                x: bounds.midX - imageSize.width / 2,
                y: bounds.midY - imageSize.height / 2,
                width: imageSize.width,
                height: imageSize.height
            )
            symbolImage.draw(in: imageRect)
        }
    }
}

private extension Array {
    subscript(safe index: Int) -> Element? {
        guard indices.contains(index) else { return nil }
        return self[index]
    }
}

final class RunnerController {
    let scriptDir: URL
    let workspaceDir: URL
    let repoDir: URL
    let configPath: URL
    let envPath: URL
    let logPath: URL
    let debugLogPath: URL

    var process: Process?
    var stdoutPipe: Pipe?
    var logOffset: UInt64 = 0
    var stdoutBuffer = Data()
    var isRunning = false

    var onStatus: ((String) -> Void)?
    var onSubtitle: ((SubtitleRecord) -> Void)?
    var onRunningChanged: ((Bool) -> Void)?
    var onTranslationDisabled: (() -> Void)?

    init(scriptDir: URL, workspaceDir: URL, repoDir: URL, configPath: URL, envPath: URL, logPath: URL, debugLogPath: URL) {
        self.scriptDir = scriptDir
        self.workspaceDir = workspaceDir
        self.repoDir = repoDir
        self.configPath = configPath
        self.envPath = envPath
        self.logPath = logPath
        self.debugLogPath = debugLogPath
    }

    func refreshRunningState() {
        if isRunning, let process, !process.isRunning {
            appendDebug("runner stale state detected, resetting local flags")
            stdoutPipe?.fileHandleForReading.readabilityHandler = nil
            stdoutPipe = nil
            self.process = nil
            isRunning = false
            onRunningChanged?(false)
        } else if isRunning, process == nil {
            appendDebug("runner stale state detected without process handle, resetting local flags")
            isRunning = false
            onRunningChanged?(false)
        }
    }

    func start(translationEnabled: Bool, runID: String, localFastOption: LocalFastOption, translationTarget: TranslationTargetOption) {
        refreshRunningState()
        guard !isRunning else { return }
        appendDebug("=== start run \(runID) ===")

        let venvPython = scriptDir.appendingPathComponent(".venv/bin/python")
        let runnerPath = scriptDir.appendingPathComponent("runner.py")

        let process = Process()
        if FileManager.default.isExecutableFile(atPath: venvPython.path) {
            process.executableURL = venvPython
            process.arguments = [
                "-u",
                runnerPath.path,
                "--config", configPath.path,
                "--env-file", envPath.path,
                "--run-id", runID,
                "--debug",
            ]
        } else {
            process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            process.arguments = [
                "python3",
                "-u",
                runnerPath.path,
                "--config", configPath.path,
                "--env-file", envPath.path,
                "--run-id", runID,
                "--debug",
            ]
        }

        if translationEnabled {
            process.arguments?.append("--translation-enabled")
            process.arguments?.append(contentsOf: ["--translation-target-language", translationTarget.id])
        } else {
            process.arguments?.append("--no-translation")
        }
        if localFastOption.isDisabled {
            process.arguments?.append("--local-fast-disabled")
        } else if let modelDir = localFastOption.modelDir {
            process.arguments?.append(contentsOf: ["--local-fast-model-dir", modelDir.path])
        }

        var env = ProcessInfo.processInfo.environment
        env["PYTHONUNBUFFERED"] = "1"
        process.environment = env
        process.currentDirectoryURL = repoDir

        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe

        stdoutBuffer = Data()
        logOffset = currentLogSize()

        pipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let chunk = handle.availableData
            guard !chunk.isEmpty else { return }
            self?.consumeStdout(chunk)
        }

        process.terminationHandler = { [weak self] task in
            DispatchQueue.main.async {
                self?.stdoutPipe?.fileHandleForReading.readabilityHandler = nil
                self?.stdoutPipe = nil
                self?.process = nil
                self?.isRunning = false
                self?.onRunningChanged?(false)
                self?.appendDebug("runner terminated status=\(task.terminationStatus)")
                if task.terminationStatus == 0 {
                    self?.onStatus?("已停止")
                } else {
                    self?.onStatus?("识别进程已退出，返回码 \(task.terminationStatus)")
                }
            }
        }

        do {
            try process.run()
            self.process = process
            self.stdoutPipe = pipe
            self.isRunning = true
            self.onRunningChanged?(true)
            self.onStatus?("正在连接 SenseAudio")
            appendDebug("runner started pid=\(process.processIdentifier)")
        } catch {
            appendDebug("runner start failed: \(error.localizedDescription)")
            self.onStatus?("启动失败: \(error.localizedDescription)")
        }
    }

    func stop() {
        refreshRunningState()
        guard let process else { return }
        onStatus?("正在停止识别")
        process.interrupt()
    }

    func pollLog() {
        guard FileManager.default.fileExists(atPath: logPath.path) else { return }
        guard let handle = try? FileHandle(forReadingFrom: logPath) else { return }
        defer { try? handle.close() }

        let size = currentLogSize()
        if size < logOffset {
            logOffset = 0
        }
        if size == logOffset {
            return
        }

        do {
            try handle.seek(toOffset: logOffset)
            let data = handle.readDataToEndOfFile()
            logOffset += UInt64(data.count)
            guard let text = String(data: data, encoding: .utf8) else { return }
            let decoder = JSONDecoder()
            for rawLine in text.split(separator: "\n") {
                guard let lineData = rawLine.data(using: .utf8) else { continue }
                guard let record = try? decoder.decode(SubtitleRecord.self, from: lineData) else { continue }
                onSubtitle?(record)
            }
        } catch {
            onStatus?("读取字幕日志失败: \(error.localizedDescription)")
        }
    }

    private func currentLogSize() -> UInt64 {
        let attributes = try? FileManager.default.attributesOfItem(atPath: logPath.path)
        return attributes?[.size] as? UInt64 ?? 0
    }

    private func consumeStdout(_ data: Data) {
        stdoutBuffer.append(data)
        while let newlineRange = stdoutBuffer.firstRange(of: Data([0x0A])) {
            let lineData = stdoutBuffer.subdata(in: 0..<newlineRange.lowerBound)
            stdoutBuffer.removeSubrange(0..<newlineRange.upperBound)
            guard let line = String(data: lineData, encoding: .utf8)?
                .trimmingCharacters(in: .whitespacesAndNewlines),
                  !line.isEmpty
            else { continue }
            DispatchQueue.main.async { [weak self] in
                self?.handleStdoutLine(line)
            }
        }
    }

    private func handleStdoutLine(_ line: String) {
        appendDebug(line)
        if line.contains("[400025]") {
            onStatus?("SenseAudio 实时并发配额不足，暂时无法继续识别")
        } else if line.contains("[translation] disabled after startup failure:") {
            onTranslationDisabled?()
            onStatus?("双语流启动失败，已自动降级为原文字幕")
        } else if line.contains("connected_success") {
            onStatus?("已连接，正在监听系统音频")
        } else if line.contains("task_started") {
            onStatus?("识别中")
        } else if line.contains("task_failed") {
            onStatus?(line)
        } else if line.contains("[local-fast] endpoint segment=") {
            onStatus?("本地快字幕识别中")
        } else if line.contains("[local_fast segment") || line.contains("[senseaudio segment") || line.contains("[segment") {
            onStatus?("收到新字幕")
        }
    }

    private func appendDebug(_ line: String) {
        let prefix = ISO8601DateFormatter().string(from: Date())
        let text = "[\(prefix)] \(line)\n"
        let dir = debugLogPath.deletingLastPathComponent()
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        if let data = text.data(using: .utf8) {
            if FileManager.default.fileExists(atPath: debugLogPath.path),
               let handle = try? FileHandle(forWritingTo: debugLogPath) {
                _ = try? handle.seekToEnd()
                try? handle.write(contentsOf: data)
                try? handle.close()
            } else {
                try? data.write(to: debugLogPath)
            }
        }
    }
}

final class OverlayViewController: NSViewController, NSWindowDelegate, AVAudioPlayerDelegate {
    private let compactWindowSize = NSSize(width: 220, height: 220)
    private let compactHoverWindowSize = NSSize(width: 236, height: 236)
    private let compactPanelWindowSize = NSSize(width: 226, height: 286)
    private let compactProjectWindowSize = NSSize(width: 296, height: 236)
    private let expandedWindowSize = NSSize(width: 860, height: 194)
    private let scriptDir: URL
    private let workspaceDir: URL
    private let statePath: URL
    private let debugLogPath: URL
    private let controller: RunnerController
    private var pollTimer: Timer?
    private var pendingRestart = false
    private var pendingCompactAfterStop = false
    private var isCompactMode = true
    private var isCompactHoverVisible = false
    private var compactHoverDismissDeadline: Date?
    private var translationEnabled = false
    private var currentRunID = ""
    private var latestSenseAudioFinal = ""
    private var latestSenseAudioTranslation = ""
    private var shutdownStarted = false
    private var uiBuilt = false
    private var pendingLocalDrafts: [LocalDraft] = []
    private var committedSegments: [CommittedSegment] = []
    private var committedLocalSegmentUpperBound = -1
    private var retainedLocalFastText = ""
    private var retainedLocalFastUpdatedAt: Date?
    private var lastSubtitleEventAt: Date?
    private var organizeProcess: Process?
    private var musicProcess: Process?
    private var speechProcess: Process?
    private var speechPlayer: AVAudioPlayer?
    private var speechPlayerData: Data?
    private var musicPlayer: AVAudioPlayer?
    private var musicPlayerData: Data?
    private var activeMusicTrackID: String?
    private var musicPlaybackLoadToken = 0
    private let audioRouteStateCacheTTL: TimeInterval = 5.0
    private let audioDeviceCacheTTL: TimeInterval = 8.0
    private let subtitleFadeDelay: TimeInterval = 2.8
    private let subtitleFadeDuration: TimeInterval = 1.45
    private let localFastTrailRetention: TimeInterval = 5.0
    private let compactHoverDismissDelay: TimeInterval = 0.95
    private let compactDataCacheTTL: TimeInterval = 3.0
    private let compactDataQueue = DispatchQueue(label: "audioclaw.compact-data", qos: .userInitiated)
    private let compactHintLabel = NSTextField(labelWithString: "悬停查看操作与最近项目")

    private weak var headerView: NSVisualEffectView?
    private weak var bodyView: NSVisualEffectView?
    private weak var compactRootView: NSView?
    private var compactPanelHostView: HoverTrackingView?
    private weak var compactPreviewPanel: NSVisualEffectView?
    private weak var compactPreviewScrollView: NSScrollView?
    private weak var compactPreviewStack: NSStackView?
    private weak var compactPreviewTitleLabel: NSTextField?
    private weak var compactPreviewSubtitleLabel: NSTextField?
    private weak var compactPreviewRefreshButton: NSButton?
    private weak var compactPreviewCloseButton: NSButton?
    private weak var compactPreviewSelectionLabel: NSTextField?
    private weak var compactPreviewMetaLabel: NSTextField?
    private var expandedChromeConstraints: [NSLayoutConstraint] = []
    private var compactBubbleCenterXConstraint: NSLayoutConstraint?
    private var compactBubbleTrailingConstraint: NSLayoutConstraint?
    private var compactPreviewLeadingConstraint: NSLayoutConstraint?
    private var compactPreviewWidthConstraint: NSLayoutConstraint?
    private var compactSatelliteHintCenterXConstraint: NSLayoutConstraint?
    private var compactSatelliteHintWidthConstraint: NSLayoutConstraint?
    private weak var compactSatelliteHintContainer: NSView?
    private weak var compactSatelliteHintLabel: NSTextField?
    private weak var compactSatelliteStartButton: NSButton?
    private weak var compactSatelliteProjectButton: NSButton?
    private weak var compactSatelliteReadButton: NSButton?
    private weak var compactSatelliteMusicButton: NSButton?
    private var compactSatelliteCenterXConstraints: [NSLayoutConstraint] = []
    private var compactSatelliteCenterYConstraints: [NSLayoutConstraint] = []
    private var compactPreviewRows: [ClickableRowView] = []
    private var compactPreviewLabels: [NSTextField] = []
    private var compactPreviewProjects: [RecentProject] = []
    private var compactMusicTracks: [GeneratedMusicTrack] = []
    private var cachedRecentProjects: [RecentProject] = []
    private var cachedRecentMusicTracks: [GeneratedMusicTrack] = []
    private var recentProjectsCacheLoadedAt: Date?
    private var recentMusicTracksCacheLoadedAt: Date?
    private var recentProjectsLoading = false
    private var recentMusicTracksLoading = false
    private var recentProjectsLoadToken = 0
    private var recentMusicTracksLoadToken = 0
    private var selectedCompactProjectIndex: Int?
    private var compactProjectPanelVisible = false
    private var compactMusicPanelVisible = false
    private var compactPanelWindow: OverlayPanelWindow?
    private var templatePanelWindow: OverlayPanelWindow?
    private var templatePanelSelectedID = ""
    private var templatePanelRows: [(id: String, row: ClickableRowView, name: NSTextField, meta: NSTextField)] = []
    private weak var templatePanelCurrentLabel: NSTextField?
    private weak var templatePanelKindLabel: NSTextField?
    private weak var templatePanelSummaryLabel: NSTextField?
    private weak var templatePanelPromptLabel: NSTextField?
    private weak var templatePanelOutputLabel: NSTextField?
    private weak var templatePanelUseButton: NSButton?
    private weak var templatePanelEditButton: NSButton?
    private weak var templatePanelImportButton: NSButton?
    private weak var templatePanelDeleteButton: NSButton?
    private weak var compactProjectActionStack: NSStackView?
    private weak var compactOrganizeSummaryButton: NSButton?
    private weak var compactExtractKeywordsButton: NSButton?
    private weak var compactEditTemplateButton: NSButton?
    private weak var compactOpenTranscriptButton: NSButton?
    private weak var compactMusicActionStack: NSStackView?
    private weak var compactMusicGenerateButton: NSButton?
    private weak var compactMusicPromptButton: NSButton?
    private weak var compactMusicStyleButton: NSButton?
    private weak var compactMusicModeButton: NSButton?
    private weak var compactMusicRenameButton: NSButton?
    private weak var compactMusicPlayPauseButton: NSButton?
    private weak var compactMusicOpenButton: NSButton?
    private var selectedCompactMusicIndex: Int?
    private weak var compactOpenNotesButton: NSButton?
    private weak var compactRenameProjectButton: NSButton?
    private weak var compactArchiveProjectButton: NSButton?
    private var organizingProjectRunID: String?
    private var historyTopHeightConstraint: NSLayoutConstraint?
    private var translationHeightConstraint: NSLayoutConstraint?
    private var pendingCompactBubbleAnchorScreenPoint: NSPoint?
    private var lastDisplayedHistoryText = ""
    private var lastDisplayedOriginalText = ""
    private var lastDisplayedTranslationText = ""
    private var suppressSubtitleAnimations = false
    private var skipCompactPreviewRefreshInButtonSync = false
    private var currentTranscriptHasContent = false
    private var currentTranscriptDiskProbeCompleted = false
    private var compactPreviewRefreshWorkItem: DispatchWorkItem?
    private var compactPreviewRefreshNeedsForceReload = false
    private var compactPanelSyncWorkItem: DispatchWorkItem?
    private var compactPanelSyncNeedsAnimation = false
    private var compactVolumeScrollAccumulator: CGFloat = 0
    private var volumeHintClearWorkItem: DispatchWorkItem?
    private var clipboardChangeCount = NSPasteboard.general.changeCount
    private var lastNonZeroOutputVolumePercent = 35
    private var cachedAudioRouteStateValues: [String: String] = [:]
    private var audioRouteStateLoadedAt: Date?
    private var cachedAudioDeviceIDs: [AudioDeviceID] = []
    private var cachedAudioDeviceNames: [AudioDeviceID: String] = [:]
    private var audioDeviceCacheLoadedAt: Date?
    private var latestClipboardText = ""
    private var latestClipboardCapturedAt: Date?
    private var customMusicPrompt = ""
    private let defaultOrganizationTemplateID = "summary_brief"
    private let builtinOrganizationTemplates: [OrganizationTemplate] = [
        OrganizationTemplate(
            id: "summary_brief",
            name: "通用纪要",
            summary: "摘要、重点、结论一页读完",
            prompt: """
请把下面这份 SenseAudio ASR 整理成一份简洁中文 Markdown。

输出结构：
1. 一句话摘要
2. 关键信息
3. 结构化整理稿
4. 待办/结论

{asr}
""",
            isBuiltin: true
        ),
        OrganizationTemplate(
            id: "study_notes",
            name: "学习笔记",
            summary: "适合课程、讲座、知识视频",
            prompt: """
请把下面这份 SenseAudio ASR 整理成学习笔记，语言清晰、适合复习。

输出结构：
1. 本段主题
2. 知识点整理
3. 关键概念/术语
4. 值得复习的问题

{asr}
""",
            isBuiltin: true
        ),
        OrganizationTemplate(
            id: "meeting_actions",
            name: "会议行动",
            summary: "提炼决策、行动项和风险",
            prompt: """
请把下面这份 SenseAudio ASR 整理成会议行动清单，不要编造责任人或日期。

输出结构：
1. 核心结论
2. 决策事项
3. 明确待办
4. 风险/阻塞
5. 仍需确认的问题

{asr}
""",
            isBuiltin: true
        ),
    ]
    private var organizationTemplateStoreCache: OrganizationTemplateStore?
    private let availableTTSVoices: [(id: String, label: String)] = [
        ("female_0006_a", "女声 A"),
        ("male_0004_a", "男声 A"),
        ("male_0018_a", "男声 B"),
        ("male_0027_a", "男声 C"),
        ("female_0033_a", "女声 B"),
    ]
    private var selectedTTSVoiceIndex = 0
    private let availableMusicStyles: [MusicStylePreset] = [
        MusicStylePreset(id: "cinematic", label: "电影感"),
        MusicStylePreset(id: "ambient", label: "氛围"),
        MusicStylePreset(id: "electronic", label: "轻电子"),
        MusicStylePreset(id: "piano", label: "钢琴"),
        MusicStylePreset(id: "uplifting", label: "明亮"),
    ]
    private var selectedMusicStyleIndex = 0
    private let availableMusicGenerationModes: [MusicGenerationMode] = [
        MusicGenerationMode(id: "instrumental", label: "纯音乐", shortLabel: "纯音"),
        MusicGenerationMode(id: "vocal_female", label: "女声演唱", shortLabel: "女声"),
        MusicGenerationMode(id: "vocal_male", label: "男声演唱", shortLabel: "男声"),
    ]
    private var selectedMusicGenerationModeIndex = 0
    private let availableLocalFastOptions: [LocalFastOption]
    private var selectedLocalFastOptionIndex = 0
    private let availableTranslationTargets: [TranslationTargetOption] = [
        TranslationTargetOption(id: "zh", label: "中文"),
        TranslationTargetOption(id: "en", label: "英文"),
        TranslationTargetOption(id: "ja", label: "日语"),
        TranslationTargetOption(id: "ko", label: "韩语"),
        TranslationTargetOption(id: "fr", label: "法语"),
        TranslationTargetOption(id: "de", label: "德语"),
        TranslationTargetOption(id: "es", label: "西语"),
    ]
    private var selectedTranslationTargetIndex = 0
    private let badgeLabel = NSTextField(labelWithString: "AUDIOCLAW LIVE")
    private let statusLabel = NSTextField(labelWithString: "准备就绪")
    private let historyTopLabel = NSTextField(wrappingLabelWithString: "")
    private let translationLabel = NSTextField(wrappingLabelWithString: "")
    private let originalLabel = NSTextField(wrappingLabelWithString: "系统字幕浮层已就绪")
    private let metaLabel = NSTextField(labelWithString: "模式: 原文 | 输入: 系统输出 (BlackHole)")
    private let startButton = NSButton(title: "Stop", target: nil, action: nil)
    private let organizeButton = NSButton(title: "整理本次", target: nil, action: nil)
    private let readClipboardButton = NSButton(title: "朗读复制", target: nil, action: nil)
    private let voiceButton = NSButton(title: "音色", target: nil, action: nil)
    private let fastSubtitleButton = NSButton(title: "快字", target: nil, action: nil)
    private let modeButton = NSButton(title: "双语 OFF", target: nil, action: nil)
    private let targetLanguageButton = NSButton(title: "译到中文", target: nil, action: nil)
    private let closeButton = NSButton(title: "收起", target: nil, action: nil)
    private let compactBubbleButton = BubbleOrbButton(title: "", target: nil, action: nil)

    private let accentColor = NSColor(calibratedRed: 0.19, green: 0.49, blue: 0.93, alpha: 0.98)
    private let accentSoftColor = NSColor(calibratedRed: 0.91, green: 0.95, blue: 1.0, alpha: 0.98)
    private let musicAccentColor = NSColor(calibratedRed: 0.78, green: 0.38, blue: 0.18, alpha: 0.98)
    private let musicAccentSoftColor = NSColor(calibratedRed: 1.0, green: 0.93, blue: 0.84, alpha: 0.98)
    private let musicInkColor = NSColor(calibratedRed: 0.13, green: 0.11, blue: 0.09, alpha: 0.98)
    private let musicPanelColor = NSColor(calibratedRed: 1.0, green: 0.985, blue: 0.95, alpha: 0.99)
    private let musicBorderColor = NSColor(calibratedRed: 0.88, green: 0.78, blue: 0.64, alpha: 0.72)
    private let paperColor = NSColor(calibratedRed: 0.965, green: 0.97, blue: 0.98, alpha: 0.985)
    private let surfaceColor = NSColor(calibratedRed: 0.985, green: 0.988, blue: 0.995, alpha: 0.99)
    private let borderColor = NSColor(calibratedRed: 0.84, green: 0.87, blue: 0.91, alpha: 0.92)
    private let inkColor = NSColor(calibratedRed: 0.13, green: 0.15, blue: 0.18, alpha: 0.97)
    private let mutedInkColor = NSColor(calibratedRed: 0.42, green: 0.47, blue: 0.54, alpha: 0.82)
    private let committedTextColor = NSColor(calibratedRed: 0.18, green: 0.39, blue: 0.73, alpha: 0.95)
    private let localFastTextColor = NSColor(calibratedRed: 0.60, green: 0.43, blue: 0.16, alpha: 0.92)
    private let senseAudioTextColor = NSColor(calibratedRed: 0.12, green: 0.29, blue: 0.58, alpha: 0.96)
    private let translationTextColor = NSColor(calibratedRed: 0.10, green: 0.43, blue: 0.34, alpha: 0.96)
    private let subtitleStatusColor = NSColor(calibratedRed: 0.34, green: 0.39, blue: 0.46, alpha: 0.88)
    private let debugCompactBackground = false

    var compactLaunchWindowSize: NSSize { compactWindowSize }
    private var compactAnyPanelVisible: Bool { compactProjectPanelVisible || compactMusicPanelVisible }

    init(scriptDir: URL, workspaceDir: URL, repoDir: URL) {
        self.scriptDir = scriptDir
        self.workspaceDir = workspaceDir
        self.statePath = workspaceDir.appendingPathComponent("state/realtime_interpreter/overlay_state.json")
        let configPath = scriptDir.appendingPathComponent("config.example.json")
        let envPath = workspaceDir.appendingPathComponent(".env")
        let logPath = workspaceDir.appendingPathComponent("state/realtime_interpreter/session.log")
        let debugLogPath = workspaceDir.appendingPathComponent("state/realtime_interpreter/overlay_runner_debug.log")
        self.debugLogPath = debugLogPath
        self.availableLocalFastOptions = Self.discoverLocalFastOptions(modelsRoot: scriptDir.appendingPathComponent("models"))
        self.controller = RunnerController(
            scriptDir: scriptDir,
            workspaceDir: workspaceDir,
            repoDir: repoDir,
            configPath: configPath,
            envPath: envPath,
            logPath: logPath,
            debugLogPath: debugLogPath
        )
        super.init(nibName: nil, bundle: nil)
        translationEnabled = CommandLine.arguments.contains("--bilingual")
        if let firstEnabled = availableLocalFastOptions.firstIndex(where: { !$0.isDisabled }) {
            selectedLocalFastOptionIndex = firstEnabled
        }
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func loadView() {
        view = NSView()
        view.wantsLayer = true
        view.layer?.backgroundColor = NSColor.clear.cgColor
        view.layer?.cornerRadius = 0
        view.layer?.borderColor = NSColor.clear.cgColor
        view.layer?.borderWidth = 0
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        appendOverlayDebug("viewDidLoad")
        ensureUIBuilt()
        debugCompactRenderState("after viewDidLoad")
    }

    override func viewDidAppear() {
        super.viewDidAppear()
        appendOverlayDebug("viewDidAppear")
        applyPresentationMode(animated: false)
        warmCompactCachesIfNeeded()
        debugCompactRenderState("after viewDidAppear")
    }

    override func viewDidLayout() {
        super.viewDidLayout()
        compactBubbleButton.layer?.cornerRadius = compactBubbleButton.bounds.width / 2
        compactSatelliteStartButton?.layer?.cornerRadius = (compactSatelliteStartButton?.bounds.width ?? 0) / 2
        compactSatelliteProjectButton?.layer?.cornerRadius = (compactSatelliteProjectButton?.bounds.width ?? 0) / 2
        compactSatelliteReadButton?.layer?.cornerRadius = (compactSatelliteReadButton?.bounds.width ?? 0) / 2
        compactSatelliteMusicButton?.layer?.cornerRadius = (compactSatelliteMusicButton?.bounds.width ?? 0) / 2
    }

    private func buildUI() {
        appendOverlayDebug("buildUI begin")
        let compactRoot = HoverTrackingView()
        compactRoot.wantsLayer = true
        compactRoot.layer?.backgroundColor = debugCompactBackground
            ? NSColor.systemYellow.withAlphaComponent(0.25).cgColor
            : NSColor.clear.cgColor
        compactRoot.translatesAutoresizingMaskIntoConstraints = false
        compactRoot.onHoverChanged = { [weak self] hovering in
            if hovering {
                self?.beginCompactHover()
            } else {
                self?.scheduleCompactHoverDismiss()
            }
        }
        compactRoot.onScroll = { [weak self] event in
            self?.handleVolumeScroll(event)
        }
        view.addSubview(compactRoot)
        self.compactRootView = compactRoot

        let previewHost = HoverTrackingView()
        previewHost.wantsLayer = true
        previewHost.layer?.backgroundColor = NSColor.clear.cgColor
        previewHost.translatesAutoresizingMaskIntoConstraints = false
        previewHost.onHoverChanged = { [weak self] hovering in
            if hovering {
                self?.beginCompactHover()
            } else {
                self?.scheduleCompactHoverDismiss()
            }
        }
        self.compactPanelHostView = previewHost

        let previewPanel = NSVisualEffectView()
        previewPanel.material = .menu
        previewPanel.blendingMode = .withinWindow
        previewPanel.state = .active
        previewPanel.wantsLayer = true
        previewPanel.layer?.cornerRadius = 20
        previewPanel.layer?.backgroundColor = surfaceColor.cgColor
        previewPanel.layer?.borderColor = borderColor.cgColor
        previewPanel.layer?.borderWidth = 1
        previewPanel.layer?.shadowColor = NSColor(calibratedRed: 0.14, green: 0.18, blue: 0.28, alpha: 0.10).cgColor
        previewPanel.layer?.shadowOpacity = 1
        previewPanel.layer?.shadowRadius = 10
        previewPanel.layer?.shadowOffset = NSSize(width: 0, height: -3)
        previewPanel.alphaValue = 0
        previewPanel.translatesAutoresizingMaskIntoConstraints = false
        previewHost.addSubview(previewPanel)
        self.compactPreviewPanel = previewPanel

        compactBubbleButton.wantsLayer = true
        compactBubbleButton.layer?.cornerRadius = 33
        compactBubbleButton.layer?.masksToBounds = true
        if #available(macOS 11.0, *) {
            compactBubbleButton.symbolImage = NSImage(systemSymbolName: "waveform.circle.fill", accessibilityDescription: "AudioClaw")
        }
        compactBubbleButton.translatesAutoresizingMaskIntoConstraints = false
        compactBubbleButton.onScroll = { [weak self] event in
            self?.handleVolumeScroll(event)
        }
        compactRoot.addSubview(compactBubbleButton)

        let satelliteStart = makeCompactSatellite(symbol: "play.fill", tooltip: "开始实时 ASR", action: #selector(startFromCompactPanel))
        let satelliteProject = makeCompactSatellite(symbol: "clock.arrow.circlepath", tooltip: "最近项目", action: #selector(toggleCompactProjectPanel))
        let satelliteRead = makeCompactSatellite(symbol: "speaker.wave.2.fill", tooltip: "朗读复制文本", action: #selector(readClipboardCapture))
        let satelliteMusic = makeCompactSatellite(symbol: "music.note", tooltip: "音乐", action: #selector(toggleCompactMusicPanel))
        [satelliteStart, satelliteProject, satelliteRead, satelliteMusic].forEach {
            compactRoot.addSubview($0)
        }
        self.compactSatelliteStartButton = satelliteStart
        self.compactSatelliteProjectButton = satelliteProject
        self.compactSatelliteReadButton = satelliteRead
        self.compactSatelliteMusicButton = satelliteMusic
        appendOverlayDebug("buildUI compact satellites done")

        let satelliteHintContainer = NSView()
        satelliteHintContainer.wantsLayer = true
        satelliteHintContainer.layer?.cornerRadius = 8
        satelliteHintContainer.layer?.masksToBounds = true
        satelliteHintContainer.layer?.backgroundColor = paperColor.withAlphaComponent(0.98).cgColor
        satelliteHintContainer.layer?.borderColor = borderColor.withAlphaComponent(0.95).cgColor
        satelliteHintContainer.layer?.borderWidth = 1
        satelliteHintContainer.alphaValue = 0.0
        satelliteHintContainer.isHidden = true
        satelliteHintContainer.translatesAutoresizingMaskIntoConstraints = false
        compactRoot.addSubview(satelliteHintContainer)
        self.compactSatelliteHintContainer = satelliteHintContainer

        let satelliteHintLabel = NSTextField(labelWithString: "")
        satelliteHintLabel.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .medium)
        satelliteHintLabel.textColor = inkColor
        satelliteHintLabel.alignment = .center
        satelliteHintLabel.maximumNumberOfLines = 1
        satelliteHintLabel.lineBreakMode = .byTruncatingTail
        satelliteHintLabel.drawsBackground = false
        satelliteHintLabel.isBezeled = false
        satelliteHintLabel.isEditable = false
        satelliteHintLabel.isSelectable = false
        satelliteHintLabel.translatesAutoresizingMaskIntoConstraints = false
        satelliteHintContainer.addSubview(satelliteHintLabel)
        self.compactSatelliteHintLabel = satelliteHintLabel
        appendOverlayDebug("buildUI compact hint done")

        let previewTitle = NSTextField(labelWithString: "项目")
        previewTitle.font = NSFont(name: "SF Pro Text", size: 12) ?? .systemFont(ofSize: 12, weight: .semibold)
        previewTitle.textColor = inkColor
        previewTitle.translatesAutoresizingMaskIntoConstraints = false
        previewPanel.addSubview(previewTitle)
        self.compactPreviewTitleLabel = previewTitle

        let previewSubtitle = NSTextField(labelWithString: "点选后继续处理")
        previewSubtitle.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: .regular)
        previewSubtitle.textColor = mutedInkColor
        previewSubtitle.translatesAutoresizingMaskIntoConstraints = false
        previewPanel.addSubview(previewSubtitle)
        self.compactPreviewSubtitleLabel = previewSubtitle

        let previewCloseButton = NSButton(title: "", target: self, action: #selector(closeCompactPreviewPanel))
        previewCloseButton.isBordered = false
        previewCloseButton.bezelStyle = .regularSquare
        previewCloseButton.contentTintColor = mutedInkColor
        previewCloseButton.wantsLayer = true
        previewCloseButton.layer?.cornerRadius = 8
        previewCloseButton.layer?.backgroundColor = paperColor.withAlphaComponent(0.7).cgColor
        previewCloseButton.translatesAutoresizingMaskIntoConstraints = false
        if #available(macOS 11.0, *) {
            previewCloseButton.image = NSImage(systemSymbolName: "xmark", accessibilityDescription: "关闭")
            previewCloseButton.imagePosition = .imageOnly
        } else {
            previewCloseButton.title = "×"
        }
        previewPanel.addSubview(previewCloseButton)
        self.compactPreviewCloseButton = previewCloseButton

        let previewRefreshButton = NSButton(title: "", target: self, action: #selector(refreshCompactPreviewPanelManually))
        previewRefreshButton.isBordered = false
        previewRefreshButton.bezelStyle = .regularSquare
        previewRefreshButton.contentTintColor = mutedInkColor
        previewRefreshButton.wantsLayer = true
        previewRefreshButton.layer?.cornerRadius = 8
        previewRefreshButton.layer?.backgroundColor = paperColor.withAlphaComponent(0.7).cgColor
        previewRefreshButton.translatesAutoresizingMaskIntoConstraints = false
        if #available(macOS 11.0, *) {
            previewRefreshButton.image = NSImage(systemSymbolName: "arrow.clockwise", accessibilityDescription: "刷新")
            previewRefreshButton.imagePosition = .imageOnly
        } else {
            previewRefreshButton.title = "↻"
        }
        previewPanel.addSubview(previewRefreshButton)
        self.compactPreviewRefreshButton = previewRefreshButton

        let previewSelectionLabel = NSTextField(labelWithString: "暂无项目")
        previewSelectionLabel.font = NSFont(name: "SF Pro Text", size: 11) ?? .systemFont(ofSize: 11, weight: .semibold)
        previewSelectionLabel.textColor = inkColor
        previewSelectionLabel.maximumNumberOfLines = 3
        previewSelectionLabel.lineBreakMode = .byWordWrapping
        previewSelectionLabel.translatesAutoresizingMaskIntoConstraints = false
        previewPanel.addSubview(previewSelectionLabel)
        self.compactPreviewSelectionLabel = previewSelectionLabel

        let previewMetaLabel = NSTextField(labelWithString: "等待识别结果")
        previewMetaLabel.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: .medium)
        previewMetaLabel.textColor = mutedInkColor
        previewMetaLabel.maximumNumberOfLines = 1
        previewMetaLabel.lineBreakMode = .byTruncatingTail
        previewMetaLabel.translatesAutoresizingMaskIntoConstraints = false
        previewPanel.addSubview(previewMetaLabel)
        self.compactPreviewMetaLabel = previewMetaLabel

        let previewScrollView = NSScrollView()
        previewScrollView.drawsBackground = false
        previewScrollView.borderType = .noBorder
        previewScrollView.hasVerticalScroller = true
        previewScrollView.hasHorizontalScroller = false
        previewScrollView.autohidesScrollers = true
        previewScrollView.scrollerStyle = .overlay
        previewScrollView.translatesAutoresizingMaskIntoConstraints = false
        previewPanel.addSubview(previewScrollView)
        self.compactPreviewScrollView = previewScrollView

        let previewListContainer = NSView()
        previewListContainer.translatesAutoresizingMaskIntoConstraints = false
        previewScrollView.documentView = previewListContainer

        let previewStack = NSStackView()
        previewStack.orientation = .vertical
        previewStack.spacing = 8
        previewStack.alignment = .leading
        previewStack.translatesAutoresizingMaskIntoConstraints = false
        previewListContainer.addSubview(previewStack)
        self.compactPreviewStack = previewStack

        compactPreviewRows = (0..<8).map { index in
            let row = ClickableRowView()
            row.translatesAutoresizingMaskIntoConstraints = false
            row.wantsLayer = true
            row.layer?.cornerRadius = 8
            row.layer?.masksToBounds = true
            row.isHidden = true
            row.onClick = { [weak self] in
                if self?.compactMusicPanelVisible == true {
                    self?.selectMusicTrack(at: index)
                } else {
                    self?.selectRecentProject(at: index)
                }
            }
            row.onDoubleClick = { [weak self] in
                guard let self else { return }
                if self.compactMusicPanelVisible {
                    self.selectMusicTrack(at: index)
                    self.playPauseSelectedMusic()
                }
            }
            row.heightAnchor.constraint(equalToConstant: 24).isActive = true

            let label = NSTextField(labelWithString: "")
            label.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: .medium)
            label.textColor = mutedInkColor
            label.maximumNumberOfLines = 1
            label.lineBreakMode = .byTruncatingTail
            label.translatesAutoresizingMaskIntoConstraints = false
            row.addSubview(label)

            NSLayoutConstraint.activate([
                label.leadingAnchor.constraint(equalTo: row.leadingAnchor, constant: 10),
                label.trailingAnchor.constraint(equalTo: row.trailingAnchor, constant: -10),
                label.centerYAnchor.constraint(equalTo: row.centerYAnchor),
            ])

            previewStack.addArrangedSubview(row)
            row.widthAnchor.constraint(equalTo: previewListContainer.widthAnchor).isActive = true
            compactPreviewLabels.append(label)
            return row
        }
        appendOverlayDebug("buildUI compact preview cards done")

        let actionStack = NSStackView()
        actionStack.orientation = .vertical
        actionStack.alignment = .leading
        actionStack.distribution = .fillEqually
        actionStack.spacing = 8
        actionStack.translatesAutoresizingMaskIntoConstraints = false
        actionStack.isHidden = true
        actionStack.alphaValue = 0.0
        previewPanel.addSubview(actionStack)
        self.compactProjectActionStack = actionStack

        let compactOpenNotesButton = makeCompactActionButton(title: "查看", action: #selector(openSelectedProjectNotes))
        let compactOrganizeSummaryButton = makeCompactActionButton(title: "整理", action: #selector(organizeSelectedRecentProject))
        let compactRenameProjectButton = makeCompactActionButton(title: "改名", action: #selector(renameSelectedRecentProject))
        let compactEditTemplateButton = makeCompactActionButton(title: "模板", action: #selector(editOrganizationTemplate))
        let compactOpenTranscriptButton = makeCompactActionButton(title: "原文", action: #selector(openSelectedProjectTranscript))
        let actionRowTop = NSStackView(views: [compactOpenNotesButton, compactOrganizeSummaryButton, compactRenameProjectButton])
        actionRowTop.orientation = .horizontal
        actionRowTop.alignment = .centerY
        actionRowTop.distribution = .fillEqually
        actionRowTop.spacing = 6
        let actionRowBottom = NSStackView(views: [compactEditTemplateButton, compactOpenTranscriptButton])
        actionRowBottom.orientation = .horizontal
        actionRowBottom.alignment = .centerY
        actionRowBottom.distribution = .fillEqually
        actionRowBottom.spacing = 6
        actionStack.addArrangedSubview(actionRowTop)
        actionStack.addArrangedSubview(actionRowBottom)
        self.compactOrganizeSummaryButton = compactOrganizeSummaryButton
        self.compactExtractKeywordsButton = nil
        self.compactEditTemplateButton = compactEditTemplateButton
        self.compactOpenTranscriptButton = compactOpenTranscriptButton
        self.compactOpenNotesButton = compactOpenNotesButton
        self.compactRenameProjectButton = compactRenameProjectButton
        self.compactArchiveProjectButton = nil
        appendOverlayDebug("buildUI compact actions done")

        let musicActionStack = NSStackView()
        musicActionStack.orientation = .vertical
        musicActionStack.alignment = .leading
        musicActionStack.distribution = .fillEqually
        musicActionStack.spacing = 6
        musicActionStack.translatesAutoresizingMaskIntoConstraints = false
        musicActionStack.isHidden = true
        musicActionStack.alphaValue = 0.0
        previewPanel.addSubview(musicActionStack)
        self.compactMusicActionStack = musicActionStack

        let compactMusicGenerateButton = makeCompactActionButton(title: "生成", action: #selector(generateMusicFromCurrentContext))
        let compactMusicPromptButton = makeCompactActionButton(title: "提示词", action: #selector(editMusicPrompt))
        let compactMusicStyleButton = makeCompactActionButton(title: "风格", action: #selector(cycleMusicStylePreset))
        let compactMusicModeButton = makeCompactActionButton(title: "模式", action: #selector(cycleMusicGenerationMode))
        let compactMusicRenameButton = makeCompactActionButton(title: "改名", action: #selector(renameSelectedMusicTrack))
        let compactMusicPlayPauseButton = makeCompactActionButton(title: "播放", action: #selector(playPauseSelectedMusic))
        let compactMusicOpenButton = makeCompactActionButton(title: "打开", action: #selector(openSelectedMusicFile))
        compactMusicPromptButton.setContentHuggingPriority(.required, for: .horizontal)
        compactMusicPromptButton.setContentCompressionResistancePriority(.required, for: .horizontal)
        compactMusicPromptButton.toolTip = "写自定义音乐提示词"
        compactMusicPromptButton.widthAnchor.constraint(equalToConstant: 48).isActive = true
        compactMusicRenameButton.toolTip = "重命名选中的音乐"
        compactMusicRenameButton.widthAnchor.constraint(equalToConstant: 44).isActive = true
        compactMusicGenerateButton.setContentHuggingPriority(.defaultLow, for: .horizontal)
        let musicRowTop = NSStackView(views: [compactMusicGenerateButton, compactMusicPromptButton, compactMusicRenameButton])
        musicRowTop.orientation = .horizontal
        musicRowTop.alignment = .centerY
        musicRowTop.distribution = .fill
        musicRowTop.spacing = 6
        let musicRowBottom = NSStackView(views: [compactMusicStyleButton, compactMusicModeButton, compactMusicPlayPauseButton, compactMusicOpenButton])
        musicRowBottom.orientation = .horizontal
        musicRowBottom.alignment = .centerY
        musicRowBottom.distribution = .fillEqually
        musicRowBottom.spacing = 5
        musicActionStack.addArrangedSubview(musicRowTop)
        musicActionStack.addArrangedSubview(musicRowBottom)
        self.compactMusicGenerateButton = compactMusicGenerateButton
        self.compactMusicPromptButton = compactMusicPromptButton
        self.compactMusicStyleButton = compactMusicStyleButton
        self.compactMusicModeButton = compactMusicModeButton
        self.compactMusicRenameButton = compactMusicRenameButton
        self.compactMusicPlayPauseButton = compactMusicPlayPauseButton
        self.compactMusicOpenButton = compactMusicOpenButton
        appendOverlayDebug("buildUI compact music actions done")

        let bubbleCenterX = compactBubbleButton.centerXAnchor.constraint(equalTo: compactRoot.centerXAnchor)
        let bubbleTrailing = compactBubbleButton.trailingAnchor.constraint(equalTo: compactRoot.trailingAnchor, constant: -12)
        self.compactBubbleCenterXConstraint = bubbleCenterX
        self.compactBubbleTrailingConstraint = bubbleTrailing
        bubbleCenterX.isActive = true

        self.compactPreviewLeadingConstraint = nil
        self.compactPreviewWidthConstraint = nil

        let satelliteRadius: CGFloat = 54
        let satelliteAngles: [CGFloat] = [246, 194, 142, 90]
        func orbitalOffset(_ angle: CGFloat) -> (x: CGFloat, y: CGFloat) {
            let radians = angle * .pi / 180
            return (
                x: cos(radians) * satelliteRadius,
                y: -sin(radians) * satelliteRadius
            )
        }
        let startOffset = orbitalOffset(satelliteAngles[0])
        let projectOffset = orbitalOffset(satelliteAngles[1])
        let readOffset = orbitalOffset(satelliteAngles[2])
        let musicOffset = orbitalOffset(satelliteAngles[3])

        let satelliteStartCenterX = satelliteStart.centerXAnchor.constraint(equalTo: compactBubbleButton.centerXAnchor, constant: startOffset.x)
        let satelliteStartCenterY = satelliteStart.centerYAnchor.constraint(equalTo: compactBubbleButton.centerYAnchor, constant: startOffset.y)
        let satelliteProjectCenterX = satelliteProject.centerXAnchor.constraint(equalTo: compactBubbleButton.centerXAnchor, constant: projectOffset.x)
        let satelliteProjectCenterY = satelliteProject.centerYAnchor.constraint(equalTo: compactBubbleButton.centerYAnchor, constant: projectOffset.y)
        let satelliteReadCenterX = satelliteRead.centerXAnchor.constraint(equalTo: compactBubbleButton.centerXAnchor, constant: readOffset.x)
        let satelliteReadCenterY = satelliteRead.centerYAnchor.constraint(equalTo: compactBubbleButton.centerYAnchor, constant: readOffset.y)
        let satelliteMusicCenterX = satelliteMusic.centerXAnchor.constraint(equalTo: compactBubbleButton.centerXAnchor, constant: musicOffset.x)
        let satelliteMusicCenterY = satelliteMusic.centerYAnchor.constraint(equalTo: compactBubbleButton.centerYAnchor, constant: musicOffset.y)
        self.compactSatelliteCenterXConstraints = [
            satelliteStartCenterX,
            satelliteProjectCenterX,
            satelliteReadCenterX,
            satelliteMusicCenterX,
        ]
        self.compactSatelliteCenterYConstraints = [
            satelliteStartCenterY,
            satelliteProjectCenterY,
            satelliteReadCenterY,
            satelliteMusicCenterY,
        ]

        let satelliteHintCenterX = satelliteHintContainer.centerXAnchor.constraint(equalTo: compactRoot.centerXAnchor)
        self.compactSatelliteHintCenterXConstraint = satelliteHintCenterX
        let satelliteHintWidth = satelliteHintContainer.widthAnchor.constraint(equalToConstant: 110)
        self.compactSatelliteHintWidthConstraint = satelliteHintWidth

        NSLayoutConstraint.activate([
            compactRoot.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            compactRoot.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            compactRoot.topAnchor.constraint(equalTo: view.topAnchor),
            compactRoot.bottomAnchor.constraint(equalTo: view.bottomAnchor),

            compactBubbleButton.centerYAnchor.constraint(equalTo: compactRoot.centerYAnchor),
            compactBubbleButton.widthAnchor.constraint(equalToConstant: 66),
            compactBubbleButton.heightAnchor.constraint(equalToConstant: 66),

            satelliteStartCenterX,
            satelliteStartCenterY,
            satelliteStart.widthAnchor.constraint(equalToConstant: 30),
            satelliteStart.heightAnchor.constraint(equalToConstant: 30),

            satelliteProjectCenterX,
            satelliteProjectCenterY,
            satelliteProject.widthAnchor.constraint(equalToConstant: 30),
            satelliteProject.heightAnchor.constraint(equalToConstant: 30),

            satelliteReadCenterX,
            satelliteReadCenterY,
            satelliteRead.widthAnchor.constraint(equalToConstant: 30),
            satelliteRead.heightAnchor.constraint(equalToConstant: 30),

            satelliteMusicCenterX,
            satelliteMusicCenterY,
            satelliteMusic.widthAnchor.constraint(equalToConstant: 30),
            satelliteMusic.heightAnchor.constraint(equalToConstant: 30),

            satelliteHintCenterX,
            satelliteHintContainer.topAnchor.constraint(equalTo: compactBubbleButton.bottomAnchor, constant: 12),
            satelliteHintWidth,
            satelliteHintContainer.heightAnchor.constraint(equalToConstant: 20),

            satelliteHintLabel.leadingAnchor.constraint(equalTo: satelliteHintContainer.leadingAnchor, constant: 8),
            satelliteHintLabel.trailingAnchor.constraint(equalTo: satelliteHintContainer.trailingAnchor, constant: -8),
            satelliteHintLabel.centerYAnchor.constraint(equalTo: satelliteHintContainer.centerYAnchor),

            previewPanel.leadingAnchor.constraint(equalTo: previewHost.leadingAnchor, constant: 10),
            previewPanel.trailingAnchor.constraint(equalTo: previewHost.trailingAnchor, constant: -10),
            previewPanel.topAnchor.constraint(equalTo: previewHost.topAnchor, constant: 10),
            previewPanel.bottomAnchor.constraint(equalTo: previewHost.bottomAnchor, constant: -10),

            previewTitle.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            previewTitle.trailingAnchor.constraint(lessThanOrEqualTo: previewRefreshButton.leadingAnchor, constant: -10),
            previewTitle.topAnchor.constraint(equalTo: previewPanel.topAnchor, constant: 14),

            previewCloseButton.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -12),
            previewCloseButton.centerYAnchor.constraint(equalTo: previewTitle.centerYAnchor),
            previewCloseButton.widthAnchor.constraint(equalToConstant: 18),
            previewCloseButton.heightAnchor.constraint(equalToConstant: 18),

            previewRefreshButton.trailingAnchor.constraint(equalTo: previewCloseButton.leadingAnchor, constant: -6),
            previewRefreshButton.centerYAnchor.constraint(equalTo: previewTitle.centerYAnchor),
            previewRefreshButton.widthAnchor.constraint(equalToConstant: 18),
            previewRefreshButton.heightAnchor.constraint(equalToConstant: 18),

            previewSubtitle.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            previewSubtitle.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -68),
            previewSubtitle.topAnchor.constraint(equalTo: previewTitle.bottomAnchor, constant: 4),

            previewSelectionLabel.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            previewSelectionLabel.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -16),
            previewSelectionLabel.topAnchor.constraint(equalTo: previewSubtitle.bottomAnchor, constant: 10),

            previewMetaLabel.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            previewMetaLabel.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -16),
            previewMetaLabel.topAnchor.constraint(equalTo: previewSelectionLabel.bottomAnchor, constant: 6),

            previewScrollView.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            previewScrollView.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -16),
            previewScrollView.topAnchor.constraint(equalTo: previewMetaLabel.bottomAnchor, constant: 12),
            previewScrollView.heightAnchor.constraint(equalToConstant: 92),

            previewListContainer.leadingAnchor.constraint(equalTo: previewScrollView.contentView.leadingAnchor),
            previewListContainer.trailingAnchor.constraint(equalTo: previewScrollView.contentView.trailingAnchor),
            previewListContainer.topAnchor.constraint(equalTo: previewScrollView.contentView.topAnchor),
            previewListContainer.bottomAnchor.constraint(equalTo: previewScrollView.contentView.bottomAnchor),
            previewListContainer.widthAnchor.constraint(equalTo: previewScrollView.contentView.widthAnchor),

            previewStack.leadingAnchor.constraint(equalTo: previewListContainer.leadingAnchor),
            previewStack.trailingAnchor.constraint(equalTo: previewListContainer.trailingAnchor),
            previewStack.topAnchor.constraint(equalTo: previewListContainer.topAnchor),
            previewStack.bottomAnchor.constraint(equalTo: previewListContainer.bottomAnchor),

            actionStack.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            actionStack.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -16),
            actionStack.topAnchor.constraint(equalTo: previewScrollView.bottomAnchor, constant: 14),
            actionStack.heightAnchor.constraint(equalToConstant: 68),
            actionStack.bottomAnchor.constraint(lessThanOrEqualTo: previewPanel.bottomAnchor, constant: -16),

            musicActionStack.leadingAnchor.constraint(equalTo: previewPanel.leadingAnchor, constant: 16),
            musicActionStack.trailingAnchor.constraint(equalTo: previewPanel.trailingAnchor, constant: -16),
            musicActionStack.topAnchor.constraint(equalTo: previewScrollView.bottomAnchor, constant: 14),
            musicActionStack.heightAnchor.constraint(equalToConstant: 68),
            musicActionStack.bottomAnchor.constraint(lessThanOrEqualTo: previewPanel.bottomAnchor, constant: -16),
        ])
        appendOverlayDebug("buildUI compact section done")
        [satelliteStart, satelliteProject, satelliteRead, satelliteMusic].forEach {
            $0.isHidden = true
            $0.alphaValue = 0.0
        }

        let header = DraggableVisualEffectView()
        header.material = .hudWindow
        header.blendingMode = .withinWindow
        header.state = .active
        header.wantsLayer = true
        header.layer?.cornerRadius = 22
        header.layer?.backgroundColor = NSColor(calibratedRed: 0.955, green: 0.965, blue: 0.98, alpha: 0.98).cgColor
        header.translatesAutoresizingMaskIntoConstraints = false
        header.onScroll = { [weak self] event in
            self?.handleVolumeScroll(event)
        }
        view.addSubview(header)
        self.headerView = header

        let body = DraggableVisualEffectView()
        body.material = .underWindowBackground
        body.blendingMode = .withinWindow
        body.state = .active
        body.wantsLayer = true
        body.layer?.backgroundColor = surfaceColor.cgColor
        body.translatesAutoresizingMaskIntoConstraints = false
        body.onScroll = { [weak self] event in
            self?.handleVolumeScroll(event)
        }
        view.addSubview(body)
        self.bodyView = body

        let expandedChromeConstraints = [
            header.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            header.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            header.topAnchor.constraint(equalTo: view.topAnchor),
            header.heightAnchor.constraint(equalToConstant: 42),

            body.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            body.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            body.topAnchor.constraint(equalTo: header.bottomAnchor),
            body.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ]
        self.expandedChromeConstraints = expandedChromeConstraints
        NSLayoutConstraint.activate(expandedChromeConstraints)

        badgeLabel.font = NSFont(name: "SF Pro Display", size: 9) ?? .boldSystemFont(ofSize: 9)
        badgeLabel.textColor = NSColor(calibratedRed: 0.18, green: 0.38, blue: 0.72, alpha: 1.0)
        badgeLabel.alignment = .center
        badgeLabel.drawsBackground = true
        badgeLabel.backgroundColor = accentSoftColor
        badgeLabel.wantsLayer = true
        badgeLabel.layer?.cornerRadius = 10
        badgeLabel.layer?.masksToBounds = true
        badgeLabel.translatesAutoresizingMaskIntoConstraints = false

        statusLabel.font = NSFont(name: "SF Pro Text", size: 11) ?? .systemFont(ofSize: 11, weight: .medium)
        statusLabel.textColor = inkColor
        statusLabel.translatesAutoresizingMaskIntoConstraints = false

        compactHintLabel.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .medium)
        compactHintLabel.textColor = mutedInkColor
        compactHintLabel.translatesAutoresizingMaskIntoConstraints = false

        styleButton(startButton, background: accentColor)
        styleButton(organizeButton, background: paperColor)
        styleButton(readClipboardButton, background: accentColor)
        styleButton(voiceButton, background: paperColor)
        styleButton(fastSubtitleButton, background: paperColor)
        styleButton(modeButton, background: paperColor)
        styleButton(targetLanguageButton, background: paperColor)
        styleButton(closeButton, background: paperColor)
        startButton.contentTintColor = .white
        organizeButton.contentTintColor = inkColor
        readClipboardButton.contentTintColor = .white
        voiceButton.contentTintColor = inkColor
        fastSubtitleButton.contentTintColor = inkColor
        modeButton.contentTintColor = inkColor
        targetLanguageButton.contentTintColor = inkColor
        closeButton.contentTintColor = inkColor

        startButton.target = self
        startButton.action = #selector(toggleRunner)
        organizeButton.target = self
        organizeButton.action = #selector(organizeTranscript)
        readClipboardButton.target = self
        readClipboardButton.action = #selector(readClipboardCapture)
        voiceButton.target = self
        voiceButton.action = #selector(cycleTTSVoice)
        voiceButton.toolTip = "切换朗读复制文本的音色"
        fastSubtitleButton.target = self
        fastSubtitleButton.action = #selector(cycleLocalFastOption)
        fastSubtitleButton.toolTip = "切换本地快速字幕语言，运行中会自动重启识别"
        modeButton.target = self
        modeButton.action = #selector(toggleMode)
        modeButton.toolTip = "开启或关闭 SenseAudio 双语字幕"
        targetLanguageButton.target = self
        targetLanguageButton.action = #selector(cycleTranslationTarget)
        targetLanguageButton.toolTip = "切换 SenseAudio 翻译目标语言，运行中会自动重启识别"
        closeButton.title = "收起"
        closeButton.target = self
        closeButton.action = #selector(closeWindow)

        let headerStack = NSStackView(views: [
            badgeLabel,
            statusLabel,
            compactHintLabel,
            NSView(),
            startButton,
            organizeButton,
            readClipboardButton,
            voiceButton,
            fastSubtitleButton,
            modeButton,
            targetLanguageButton,
            closeButton,
        ])
        headerStack.orientation = .horizontal
        headerStack.alignment = .centerY
        headerStack.spacing = 10
        headerStack.translatesAutoresizingMaskIntoConstraints = false
        header.addSubview(headerStack)

        let spacer = headerStack.views[3]
        spacer.setContentHuggingPriority(.defaultLow, for: .horizontal)
        spacer.setContentCompressionResistancePriority(.defaultLow, for: .horizontal)

        NSLayoutConstraint.activate([
            headerStack.leadingAnchor.constraint(equalTo: header.leadingAnchor, constant: 14),
            headerStack.trailingAnchor.constraint(equalTo: header.trailingAnchor, constant: -14),
            headerStack.topAnchor.constraint(equalTo: header.topAnchor, constant: 8),
            headerStack.bottomAnchor.constraint(equalTo: header.bottomAnchor, constant: -8),
            badgeLabel.widthAnchor.constraint(equalToConstant: 108),
        ])
        appendOverlayDebug("buildUI header section done")
        organizeButton.isEnabled = false
        organizeButton.alphaValue = 0.45
        readClipboardButton.isEnabled = false
        readClipboardButton.alphaValue = 0.45
        voiceButton.isEnabled = true
        fastSubtitleButton.isEnabled = true
        targetLanguageButton.isEnabled = true

        historyTopLabel.font = NSFont(name: "SF Pro Text", size: 11.5) ?? .systemFont(ofSize: 11.5, weight: .medium)
        historyTopLabel.textColor = localFastTextColor
        historyTopLabel.maximumNumberOfLines = 1
        historyTopLabel.lineBreakMode = .byTruncatingTail
        historyTopLabel.allowsEditingTextAttributes = true
        historyTopLabel.translatesAutoresizingMaskIntoConstraints = false
        historyTopLabel.wantsLayer = true
        historyTopLabel.isHidden = true

        translationLabel.font = NSFont(name: "SF Pro Text", size: 14) ?? .systemFont(ofSize: 14, weight: .medium)
        translationLabel.textColor = translationTextColor
        translationLabel.maximumNumberOfLines = 1
        translationLabel.lineBreakMode = .byTruncatingTail
        translationLabel.allowsEditingTextAttributes = true
        translationLabel.translatesAutoresizingMaskIntoConstraints = false
        translationLabel.wantsLayer = true
        translationLabel.isHidden = true

        originalLabel.font = NSFont(name: "SF Pro Display", size: 16.5) ?? .systemFont(ofSize: 16.5, weight: .semibold)
        originalLabel.textColor = senseAudioTextColor
        originalLabel.maximumNumberOfLines = 1
        originalLabel.lineBreakMode = .byTruncatingTail
        originalLabel.allowsEditingTextAttributes = true
        originalLabel.translatesAutoresizingMaskIntoConstraints = false
        originalLabel.wantsLayer = true

        metaLabel.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: .regular)
        metaLabel.textColor = mutedInkColor
        metaLabel.translatesAutoresizingMaskIntoConstraints = false

        body.addSubview(historyTopLabel)
        body.addSubview(translationLabel)
        body.addSubview(originalLabel)
        body.addSubview(metaLabel)

        let historyTopHeight = historyTopLabel.heightAnchor.constraint(equalToConstant: 0)
        let translationHeight = translationLabel.heightAnchor.constraint(equalToConstant: 0)
        self.historyTopHeightConstraint = historyTopHeight
        self.translationHeightConstraint = translationHeight

        NSLayoutConstraint.activate([
            historyTopLabel.leadingAnchor.constraint(equalTo: body.leadingAnchor, constant: 24),
            historyTopLabel.trailingAnchor.constraint(equalTo: body.trailingAnchor, constant: -24),
            historyTopLabel.topAnchor.constraint(equalTo: body.topAnchor, constant: 14),
            historyTopHeight,

            originalLabel.leadingAnchor.constraint(equalTo: body.leadingAnchor, constant: 24),
            originalLabel.trailingAnchor.constraint(equalTo: body.trailingAnchor, constant: -24),
            originalLabel.topAnchor.constraint(equalTo: historyTopLabel.bottomAnchor, constant: 5),

            translationLabel.leadingAnchor.constraint(equalTo: body.leadingAnchor, constant: 24),
            translationLabel.trailingAnchor.constraint(equalTo: body.trailingAnchor, constant: -24),
            translationLabel.topAnchor.constraint(equalTo: originalLabel.bottomAnchor, constant: 6),
            translationHeight,

            metaLabel.leadingAnchor.constraint(equalTo: body.leadingAnchor, constant: 24),
            metaLabel.trailingAnchor.constraint(equalTo: body.trailingAnchor, constant: -24),
            metaLabel.topAnchor.constraint(equalTo: translationLabel.bottomAnchor, constant: 10),
            metaLabel.bottomAnchor.constraint(lessThanOrEqualTo: body.bottomAnchor, constant: -16),
        ])
        appendOverlayDebug("buildUI body section done")
        appendOverlayDebug("buildUI end")
    }

    func ensureUIBuilt() {
        guard !uiBuilt else { return }
        uiBuilt = true
        buildUI()
        bindController()
        syncModeLabels()
        syncButtons(running: false)
        startPolling()
        appendOverlayDebug("ensureUIBuilt finished")
    }

    private func debugCompactRenderState(_ prefix: String) {
        let compactHidden = compactRootView?.isHidden ?? true
        let compactFrame = compactRootView?.frame ?? .zero
        let bubbleHidden = compactBubbleButton.isHidden
        let bubbleFrame = compactBubbleButton.frame
        appendOverlayDebug("\(prefix) compactMode=\(isCompactMode) compactHidden=\(compactHidden) compactFrame=\(NSStringFromRect(compactFrame)) bubbleHidden=\(bubbleHidden) bubbleFrame=\(NSStringFromRect(bubbleFrame))")
    }

    private func bindController() {
        controller.onStatus = { [weak self] status in
            self?.appendOverlayDebug("status -> \(status)")
            self?.handleRunnerStatus(status)
        }
        controller.onRunningChanged = { [weak self] running in
            self?.appendOverlayDebug("runningChanged -> \(running)")
            self?.syncButtons(running: running)
            if !running, self?.pendingRestart == true {
                self?.pendingRestart = false
                self?.startNewRun()
            } else if !running, self?.pendingCompactAfterStop == true {
                self?.pendingCompactAfterStop = false
                self?.setCompactMode(true, animated: true)
            } else if !running {
                self?.handleRecognitionStopped()
            }
            self?.refreshOrganizeButton()
        }
        controller.onTranslationDisabled = { [weak self] in
            self?.translationEnabled = false
            self?.syncModeLabels()
        }
        controller.onSubtitle = { [weak self] record in
            self?.appendOverlayDebug("subtitle -> source=\(record.source ?? "unknown") segment=\(record.segment_id) final=\(record.is_final ?? false) text=\(record.original.prefix(24))")
            self?.apply(record: record)
        }
    }

    private func startPolling() {
        pollTimer = Timer.scheduledTimer(withTimeInterval: 0.25, repeats: true) { [weak self] _ in
            self?.controller.pollLog()
            self?.pollClipboard()
            self?.tickSubtitleFade()
            self?.tickCompactHoverDismiss()
        }
    }

    private func handleRunnerStatus(_ status: String) {
        let displayStatus = friendlyRunnerStatus(status)
        statusLabel.stringValue = displayStatus

        guard !isCompactMode, controller.isRunning, !hasSubtitleContentThisRun() else {
            return
        }

        let subtitleHint: String?
        if status.contains("正在连接 SenseAudio") {
            subtitleHint = "正在连接 SenseAudio..."
        } else if status.contains("已连接") || status.contains("正在监听系统音频") {
            subtitleHint = "已接入电脑音频，播放音视频即可显示字幕"
        } else if status == "识别中" {
            subtitleHint = "正在监听系统音频"
        } else if status.contains("配额不足") || status.contains("[400025]") {
            subtitleHint = "SenseAudio 实时配额不足，已暂停云端识别"
        } else if status.contains("启动失败") || status.contains("task_failed") || status.contains("返回码") {
            subtitleHint = "识别连接异常，请稍后重试"
        } else {
            subtitleHint = nil
        }

        if let subtitleHint {
            clearLine(historyTopLabel)
            clearLine(translationLabel)
            applyLineDisplay(to: originalLabel, text: subtitleHint, committed: false)
            metaLabel.stringValue = runningModeSummary()
        }
    }

    private func friendlyRunnerStatus(_ status: String) -> String {
        if status.contains("正在连接 SenseAudio") {
            return "正在连接 SenseAudio"
        }
        if status.contains("已连接") || status.contains("正在监听系统音频") {
            return "已接入电脑音频"
        }
        if status == "识别中" {
            return "识别中"
        }
        if status.contains("本地快字幕") {
            return status
        }
        if status.contains("[400025]") || status.contains("配额不足") {
            return "SenseAudio 并发配额不足"
        }
        return status
    }

    private func handleRecognitionStopped() {
        guard !isCompactMode else { return }
        if transcriptHasContent() {
            statusLabel.stringValue = "已停止，可整理本次 ASR"
            metaLabel.stringValue = runningModeSummary()
        } else {
            statusLabel.stringValue = "已停止，暂无可整理字幕"
            clearLine(historyTopLabel)
            clearLine(translationLabel)
            applyLineDisplay(to: originalLabel, text: "已停止，未捕获到可整理字幕", committed: false)
            lastSubtitleEventAt = Date()
        }
    }

    private func syncButtons(running: Bool) {
        startButton.title = running ? "停止识别" : "开始识别"
        if let layer = startButton.layer {
            layer.backgroundColor = (running
                ? NSColor(calibratedRed: 0.70, green: 0.47, blue: 0.39, alpha: 0.96)
                : accentColor).cgColor
        }
        modeButton.toolTip = running ? "切换后会自动重启识别" : "开启或关闭 SenseAudio 双语字幕"
        fastSubtitleButton.toolTip = running ? "切换后会自动重启识别" : "切换本地快速字幕语言"
        targetLanguageButton.toolTip = running ? "切换后会自动重启识别" : "切换 SenseAudio 翻译目标语言"
    }

    private func applyPresentationMode(animated: Bool) {
        expandedChromeConstraints.forEach { $0.isActive = !isCompactMode }
        compactRootView?.isHidden = !isCompactMode
        headerView?.isHidden = isCompactMode
        bodyView?.isHidden = isCompactMode
        view.layer?.backgroundColor = isCompactMode
            ? (debugCompactBackground ? paperColor.withAlphaComponent(0.92).cgColor : NSColor.clear.cgColor)
            : paperColor.cgColor
        view.layer?.borderColor = isCompactMode
            ? (debugCompactBackground ? borderColor.cgColor : NSColor.clear.cgColor)
            : borderColor.cgColor
        view.layer?.cornerRadius = isCompactMode
            ? (compactWindowSize.width / 2)
            : 20
        view.layer?.borderWidth = (isCompactMode && debugCompactBackground) ? 1 : (isCompactMode ? 0 : 1)
        statusLabel.stringValue = isCompactMode ? "迷你浮窗待命中" : "准备就绪"
        compactHintLabel.isHidden = !isCompactMode
        organizeButton.isHidden = isCompactMode
        modeButton.isHidden = isCompactMode
        closeButton.isHidden = isCompactMode
        badgeLabel.stringValue = "LIVE CAPTION"
        badgeLabel.backgroundColor = accentSoftColor
        refreshCompactPreview()
        applyCompactProjectLayout(animated: false)
        view.layoutSubtreeIfNeeded()
        let targetSize = isCompactMode
            ? compactWindowSize
            : expandedWindowSize
        if let window = view.window {
            if isCompactMode {
                window.minSize = targetSize
                window.maxSize = targetSize
            } else {
                window.minSize = NSSize(width: 640, height: 160)
                window.maxSize = NSSize(width: 4000, height: 2400)
            }
        }
        resizeWindow(to: targetSize, animated: animated)
        syncCompactPanelWindow(animated: animated)
        refreshOrganizeButton()
    }

    private func applyCompactProjectLayout(animated: Bool) {
        guard isCompactMode else { return }
        let showingProject = compactProjectPanelVisible
        let showingMusic = compactMusicPanelVisible
        compactBubbleCenterXConstraint?.isActive = true
        compactBubbleTrailingConstraint?.isActive = false

        compactHintLabel.stringValue = showingProject
            ? "查看最近项目"
            : (showingMusic ? "查看音乐历史" : "悬停查看操作与最近项目")
        compactProjectActionStack?.alphaValue = showingProject ? (compactProjectActionStack?.alphaValue ?? 1.0) : 0.0
        compactProjectActionStack?.isHidden = !showingProject
        compactMusicActionStack?.alphaValue = showingMusic ? (compactMusicActionStack?.alphaValue ?? 1.0) : 0.0
        compactMusicActionStack?.isHidden = !showingMusic

        compactSatelliteProjectButton?.toolTip = showingProject ? "收起最近项目" : "最近项目"
        compactSatelliteMusicButton?.toolTip = showingMusic ? "收起音乐" : "音乐"

        syncCompactPanelWindow(animated: animated)

        guard animated else {
            view.layoutSubtreeIfNeeded()
            return
        }
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.18
            context.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
            view.layoutSubtreeIfNeeded()
        }
    }

    private func setCompactMode(_ compact: Bool, animated: Bool) {
        isCompactMode = compact
        if !compact {
            isCompactHoverVisible = false
            compactHoverDismissDeadline = nil
            compactProjectPanelVisible = false
            compactMusicPanelVisible = false
        }
        applyPresentationMode(animated: animated)
    }

    private func animateCompactNode(_ view: NSView?, visible: Bool, offsetX: CGFloat, offsetY: CGFloat, scale: CGFloat = 0.92, duration: CFTimeInterval = 0.24) {
        guard let view, let layer = view.layer else { return }
        view.isHidden = false
        layer.removeAnimation(forKey: "hover-x")
        layer.removeAnimation(forKey: "hover-y")
        layer.removeAnimation(forKey: "hover-scale")
        layer.removeAnimation(forKey: "hover-opacity")

        let fromX = visible ? offsetX : 0
        let toX: CGFloat = visible ? 0 : offsetX
        let fromY = visible ? offsetY : 0
        let toY: CGFloat = visible ? 0 : offsetY
        let fromScale: CGFloat = visible ? scale : 1.0
        let toScale: CGFloat = visible ? 1.0 : scale
        let fromOpacity: Float = visible ? 0.0 : Float(view.alphaValue)
        let toOpacity: Float = visible ? 1.0 : 0.0

        let moveX = CABasicAnimation(keyPath: "transform.translation.x")
        moveX.fromValue = fromX
        moveX.toValue = toX
        moveX.duration = duration
        moveX.timingFunction = CAMediaTimingFunction(name: .easeOut)

        let moveY = CABasicAnimation(keyPath: "transform.translation.y")
        moveY.fromValue = fromY
        moveY.toValue = toY
        moveY.duration = duration
        moveY.timingFunction = CAMediaTimingFunction(name: .easeOut)

        let zoom = CABasicAnimation(keyPath: "transform.scale")
        zoom.fromValue = fromScale
        zoom.toValue = toScale
        zoom.duration = duration
        zoom.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)

        let fade = CABasicAnimation(keyPath: "opacity")
        fade.fromValue = fromOpacity
        fade.toValue = toOpacity
        fade.duration = duration * 0.92
        fade.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)

        layer.opacity = toOpacity
        layer.transform = visible ? CATransform3DIdentity : CATransform3DMakeScale(scale, scale, 1)
        view.alphaValue = CGFloat(toOpacity)
        layer.add(moveX, forKey: "hover-x")
        layer.add(moveY, forKey: "hover-y")
        layer.add(zoom, forKey: "hover-scale")
        layer.add(fade, forKey: "hover-opacity")
        if !visible {
            DispatchQueue.main.asyncAfter(deadline: .now() + duration + 0.02) { [weak view] in
                view?.isHidden = true
            }
        }
    }

    private func setCompactHoverVisible(_ visible: Bool, animated: Bool) {
        guard isCompactMode else { return }
        compactHoverDismissDeadline = nil
        let previousHoverVisible = isCompactHoverVisible
        isCompactHoverVisible = visible
        if compactAnyPanelVisible {
            compactSatelliteStartButton?.isHidden = true
            compactSatelliteReadButton?.isHidden = true
            compactSatelliteProjectButton?.isHidden = compactMusicPanelVisible
            compactSatelliteMusicButton?.isHidden = compactProjectPanelVisible
            compactSatelliteStartButton?.alphaValue = 0.0
            compactSatelliteReadButton?.alphaValue = 0.0
            compactSatelliteProjectButton?.alphaValue = compactMusicPanelVisible ? 0.0 : 1.0
            compactSatelliteMusicButton?.alphaValue = compactProjectPanelVisible ? 0.0 : 1.0
            syncCompactPanelWindow(animated: animated)
            return
        }
        if animated {
            if previousHoverVisible != visible {
                animateCompactNode(compactSatelliteStartButton, visible: visible, offsetX: 18, offsetY: 12, scale: 0.9, duration: 0.18)
                animateCompactNode(compactSatelliteProjectButton, visible: visible, offsetX: 20, offsetY: 2, scale: 0.9, duration: 0.20)
                animateCompactNode(compactSatelliteReadButton, visible: visible, offsetX: 12, offsetY: -10, scale: 0.9, duration: 0.22)
                animateCompactNode(compactSatelliteMusicButton, visible: visible, offsetX: 4, offsetY: -16, scale: 0.9, duration: 0.24)
            }
        } else {
            compactSatelliteStartButton?.isHidden = !visible
            compactSatelliteProjectButton?.isHidden = !visible
            compactSatelliteReadButton?.isHidden = !visible
            compactSatelliteMusicButton?.isHidden = !visible
            compactSatelliteStartButton?.alphaValue = visible ? 1.0 : 0.0
            compactSatelliteProjectButton?.alphaValue = visible ? 1.0 : 0.0
            compactSatelliteReadButton?.alphaValue = visible ? 1.0 : 0.0
            compactSatelliteMusicButton?.alphaValue = visible ? 1.0 : 0.0
        }
    }

    private func tickCompactHoverDismiss() {
        guard isCompactMode, isCompactHoverVisible, let window = view.window else { return }
        guard let deadline = compactHoverDismissDeadline else { return }
        let mouseLocation = NSEvent.mouseLocation
        let hitFrame = compactInteractiveScreenFrame(in: window).insetBy(dx: -10, dy: -10)
        if hitFrame.contains(mouseLocation) {
            compactHoverDismissDeadline = nil
            return
        }
        if Date() >= deadline {
            compactProjectPanelVisible = false
            compactMusicPanelVisible = false
            setCompactSatelliteHint(nil)
            syncCompactPanelWindow(animated: true)
            setCompactHoverVisible(false, animated: true)
        }
    }

    private func beginCompactHover() {
        compactHoverDismissDeadline = nil
        setCompactHoverVisible(true, animated: true)
    }

    private func scheduleCompactHoverDismiss() {
        compactHoverDismissDeadline = Date().addingTimeInterval(compactHoverDismissDelay)
    }

    private func compactInteractiveScreenFrame(in window: NSWindow) -> NSRect {
        guard let compactRoot = compactRootView else { return window.frame }
        let interactiveViews: [NSView?] = [
            compactBubbleButton,
            compactSatelliteStartButton,
            compactSatelliteProjectButton,
            compactSatelliteReadButton,
            compactSatelliteMusicButton,
            compactSatelliteHintContainer,
        ]
        let visibleViews = interactiveViews.compactMap { $0 }.filter { !$0.isHidden && $0.alphaValue > 0.01 }
        guard let firstView = visibleViews.first else { return window.frame }

        var unionRect = compactRoot.convert(firstView.bounds, from: firstView)
        for view in visibleViews.dropFirst() {
            unionRect = unionRect.union(compactRoot.convert(view.bounds, from: view))
        }
        let windowRect = compactRoot.convert(unionRect, to: nil)
        var screenRect = window.convertToScreen(windowRect)
        if let panelWindow = compactPanelWindow, panelWindow.isVisible {
            screenRect = screenRect.union(panelWindow.frame)
        }
        return screenRect
    }

    private func currentBubbleCenterInScreen() -> NSPoint? {
        guard let window = compactBubbleButton.window else { return nil }
        let localCenter = NSPoint(x: compactBubbleButton.bounds.midX, y: compactBubbleButton.bounds.midY)
        let centerInWindow = compactBubbleButton.convert(localCenter, to: nil)
        return window.convertToScreen(NSRect(origin: centerInWindow, size: .zero)).origin
    }

    private func ensureCompactPanelWindow() {
        guard compactPanelWindow == nil, let panelHost = compactPanelHostView else { return }
        panelHost.frame = NSRect(origin: .zero, size: compactPanelWindowSize)
        panelHost.autoresizingMask = [.width, .height]

        let panelWindow = OverlayPanelWindow(
            contentRect: NSRect(origin: .zero, size: compactPanelWindowSize),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        panelWindow.level = .floating
        panelWindow.isOpaque = false
        panelWindow.backgroundColor = .clear
        panelWindow.alphaValue = 1.0
        panelWindow.hasShadow = false
        panelWindow.isMovableByWindowBackground = true
        panelWindow.collectionBehavior = [.moveToActiveSpace]
        panelWindow.contentView = panelHost
        compactPanelWindow = panelWindow
    }

    private func compactPanelFrame(anchoringTo bubbleWindow: NSWindow) -> NSRect {
        let visible = bubbleWindow.screen?.visibleFrame ?? NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let bubbleFrame = bubbleWindow.frame
        let size = compactPanelWindowSize
        let gap: CGFloat = 10
        let proposedX = bubbleFrame.minX - size.width - gap
        let proposedY = bubbleFrame.midY - size.height / 2
        let x = min(max(proposedX, visible.minX), visible.maxX - size.width)
        let y = min(max(proposedY, visible.minY), visible.maxY - size.height)
        return NSRect(x: x, y: y, width: size.width, height: size.height)
    }

    private func syncCompactPanelWindow(animated: Bool) {
        compactPanelSyncNeedsAnimation = compactPanelSyncNeedsAnimation || animated
        if compactPanelSyncWorkItem != nil {
            return
        }
        let workItem = DispatchWorkItem { [weak self] in
            guard let self else { return }
            let shouldAnimate = self.compactPanelSyncNeedsAnimation
            self.compactPanelSyncNeedsAnimation = false
            self.compactPanelSyncWorkItem = nil
            self.performCompactPanelWindowSync(animated: shouldAnimate)
        }
        compactPanelSyncWorkItem = workItem
        DispatchQueue.main.async(execute: workItem)
    }

    private func performCompactPanelWindowSync(animated: Bool) {
        guard let bubbleWindow = view.window else { return }
        guard isCompactMode, compactAnyPanelVisible else {
            if let panelWindow = compactPanelWindow, panelWindow.isVisible {
                if animated {
                    NSAnimationContext.runAnimationGroup { context in
                        context.duration = 0.18
                        panelWindow.animator().alphaValue = 0.0
                    } completionHandler: {
                        panelWindow.orderOut(nil)
                        panelWindow.alphaValue = 1.0
                    }
                } else {
                    panelWindow.orderOut(nil)
                    panelWindow.alphaValue = 1.0
                }
            }
            return
        }

        ensureCompactPanelWindow()
        guard let panelWindow = compactPanelWindow else { return }
        let targetFrame = compactPanelFrame(anchoringTo: bubbleWindow)
        if !panelWindow.isVisible {
            panelWindow.setFrame(targetFrame, display: true)
            if animated {
                panelWindow.alphaValue = 0.0
                panelWindow.orderFrontRegardless()
                NSAnimationContext.runAnimationGroup { context in
                    context.duration = 0.18
                    panelWindow.animator().alphaValue = 1.0
                }
            } else {
                panelWindow.alphaValue = 1.0
                panelWindow.orderFrontRegardless()
            }
        } else {
            let current = panelWindow.frame
            let frameAlmostEqual =
                abs(current.origin.x - targetFrame.origin.x) < 0.5 &&
                abs(current.origin.y - targetFrame.origin.y) < 0.5 &&
                abs(current.size.width - targetFrame.size.width) < 0.5 &&
                abs(current.size.height - targetFrame.size.height) < 0.5
            if frameAlmostEqual {
                return
            }
            panelWindow.setFrame(targetFrame, display: true)
            panelWindow.orderFrontRegardless()
        }
    }

    private func resizeWindow(to size: NSSize, animated: Bool) {
        guard let window = view.window else { return }
        let oldFrame = window.frame
        let visible = window.screen?.visibleFrame ?? NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let center = NSPoint(x: oldFrame.midX, y: oldFrame.midY)
        let bubbleCenterInScreen = pendingCompactBubbleAnchorScreenPoint ?? currentBubbleCenterInScreen() ?? center
        let minX = visible.minX
        let maxX = visible.maxX - size.width
        let minY = visible.minY
        let maxY = visible.maxY - size.height
        let compactBubbleHalfWidth = compactBubbleButton.bounds.width > 0 ? compactBubbleButton.bounds.width / 2 : 33
        let compactBubbleTrailingInset = CGFloat(abs(compactBubbleTrailingConstraint?.constant ?? -12)) + compactBubbleHalfWidth
        let proposedX: CGFloat
        if isCompactMode && compactAnyPanelVisible {
            proposedX = bubbleCenterInScreen.x - (size.width - compactBubbleTrailingInset)
        } else if isCompactMode {
            proposedX = bubbleCenterInScreen.x - size.width / 2
        } else {
            proposedX = center.x - size.width / 2
        }
        let proposedY = isCompactMode
            ? bubbleCenterInScreen.y - size.height / 2
            : center.y - size.height / 2
        let clampedX = min(max(proposedX, minX), maxX)
        let clampedY = min(max(proposedY, minY), maxY)
        let newOrigin = NSPoint(x: clampedX, y: clampedY)
        let newFrame = NSRect(origin: newOrigin, size: size)
        window.setFrame(newFrame, display: true, animate: animated)
        pendingCompactBubbleAnchorScreenPoint = nil
        saveWindowState()
    }

    private func refreshCompactPreview(forceReload: Bool = false) {
        compactPreviewRefreshNeedsForceReload = compactPreviewRefreshNeedsForceReload || forceReload
        if compactPreviewRefreshWorkItem != nil {
            return
        }
        let workItem = DispatchWorkItem { [weak self] in
            guard let self else { return }
            let shouldForceReload = self.compactPreviewRefreshNeedsForceReload
            self.compactPreviewRefreshNeedsForceReload = false
            self.compactPreviewRefreshWorkItem = nil
            self.performCompactPreviewRefresh(forceReload: shouldForceReload)
        }
        compactPreviewRefreshWorkItem = workItem
        DispatchQueue.main.async(execute: workItem)
    }

    private func performCompactPreviewRefresh(forceReload: Bool = false) {
        if compactMusicPanelVisible {
            refreshCompactMusicPanel(forceReload: forceReload)
            return
        }

        applyCompactPreviewPanelStyle(isMusic: false)
        compactPreviewScrollView?.isHidden = false
        compactPreviewProjects = recentProjects(limit: compactPreviewLabels.count, forceReload: forceReload)
        compactPreviewPanel?.isHidden = !compactProjectPanelVisible
        compactPreviewPanel?.alphaValue = compactProjectPanelVisible ? 1.0 : 0.0
        compactPreviewTitleLabel?.stringValue = "项目"
        compactPreviewSubtitleLabel?.stringValue = "点选项目 · 当前模板：\(selectedOrganizationTemplate().name)"
        compactPreviewRefreshButton?.isHidden = true
        if selectedCompactProjectIndex == nil, !compactPreviewProjects.isEmpty {
            selectedCompactProjectIndex = 0
        }
        if let selectedCompactProjectIndex, !compactPreviewProjects.indices.contains(selectedCompactProjectIndex) {
            self.selectedCompactProjectIndex = nil
        }
        for (index, label) in compactPreviewLabels.enumerated() {
            let row = compactPreviewRows[index]
            guard index < compactPreviewProjects.count else {
                label.stringValue = ""
                row.isHidden = true
                continue
            }
            let project = compactPreviewProjects[index]
            let selected = selectedCompactProjectIndex == index
            let isOrganizing = organizingProjectRunID == project.runID
            let baseTitle = project.title == project.snippet
                ? "\(prettyRunTimestamp(project.runID)) · \(project.title)"
                : project.title
            label.stringValue = isOrganizing ? "正在整理 · \(baseTitle)" : baseTitle
            label.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: selected ? .semibold : .medium)
            row.isHidden = false
            label.textColor = isOrganizing ? accentColor : (selected ? inkColor : mutedInkColor)
            row.alphaValue = (selected || isOrganizing) ? 1.0 : 0.76
            styleCompactPreviewRow(row, selected: selected || isOrganizing)
            if isOrganizing {
                row.layer?.borderColor = accentColor.withAlphaComponent(0.34).cgColor
                row.layer?.backgroundColor = accentSoftColor.withAlphaComponent(0.92).cgColor
            }
        }

        if let compactProjectActionStack {
            let hasSelection = selectedCompactProjectIndex != nil
            compactProjectActionStack.isHidden = !compactProjectPanelVisible
            compactProjectActionStack.alphaValue = compactProjectPanelVisible ? (hasSelection ? 1.0 : 0.35) : 0.0
            compactMusicActionStack?.isHidden = true
            compactMusicActionStack?.alphaValue = 0.0
            updateCompactProjectActionButtons(hasSelection: hasSelection)
        }

        if let selectedCompactProjectIndex, compactPreviewProjects.indices.contains(selectedCompactProjectIndex) {
            let project = compactPreviewProjects[selectedCompactProjectIndex]
            let isOrganizing = organizingProjectRunID == project.runID
            compactPreviewSelectionLabel?.stringValue = project.title
            compactPreviewSelectionLabel?.textColor = isOrganizing ? accentColor : inkColor
            compactPreviewMetaLabel?.stringValue = isOrganizing
                ? "AudioClaw 正在生成整理稿..."
                : (project.hasOrganizedNotes
                ? "\(project.metaText) · 可直接查看"
                : "\(project.metaText) · 可按\(selectedOrganizationTemplate().name)整理")
            compactPreviewMetaLabel?.textColor = mutedInkColor
        } else {
            compactPreviewSelectionLabel?.stringValue = compactPreviewProjects.isEmpty
                ? (recentProjectsLoading ? "正在载入项目" : "暂无项目")
                : "未选中项目"
            compactPreviewSelectionLabel?.textColor = mutedInkColor
            compactPreviewMetaLabel?.stringValue = compactPreviewProjects.isEmpty
                ? (recentProjectsLoading ? "正在后台扫描最近识别结果" : "等待新的识别结果")
                : "请选择一个项目"
            compactPreviewMetaLabel?.textColor = mutedInkColor
        }
    }

    private func refreshCompactMusicPanel(forceReload: Bool = false) {
        applyCompactPreviewPanelStyle(isMusic: true)
        compactPreviewScrollView?.isHidden = false
        compactMusicTracks = recentMusicTracks(limit: compactPreviewLabels.count, forceReload: forceReload)
        compactPreviewPanel?.isHidden = !compactMusicPanelVisible
        compactPreviewPanel?.alphaValue = compactMusicPanelVisible ? 1.0 : 0.0
        updateCompactMusicPanelHeader()
        compactPreviewRefreshButton?.isHidden = false

        if selectedCompactMusicIndex == nil, !compactMusicTracks.isEmpty {
            selectedCompactMusicIndex = 0
        }
        if let selectedCompactMusicIndex, !compactMusicTracks.indices.contains(selectedCompactMusicIndex) {
            self.selectedCompactMusicIndex = nil
        }

        for (index, label) in compactPreviewLabels.enumerated() {
            let row = compactPreviewRows[index]
            guard index < compactMusicTracks.count else {
                label.stringValue = ""
                row.isHidden = true
                continue
            }
            let track = compactMusicTracks[index]
            let selected = selectedCompactMusicIndex == index
            let isActive = activeMusicTrackID == track.id && musicPlayer != nil
            let isPlaying = isActive && (musicPlayer?.isPlaying == true)
            let prefix = isPlaying ? "播放中 · " : (isActive ? "已暂停 · " : "")
            label.stringValue = prefix + "♪ " + track.title
            label.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: selected ? .semibold : .medium)
            row.isHidden = false
            label.textColor = isActive ? musicAccentColor : (selected ? musicInkColor : mutedInkColor)
            row.alphaValue = selected ? 1.0 : 0.76
            styleCompactPreviewRow(row, selected: selected, mood: .music)
        }

        let hasSelection = selectedCompactMusicIndex != nil
        compactProjectActionStack?.isHidden = true
        compactProjectActionStack?.alphaValue = 0.0
        compactMusicActionStack?.isHidden = !compactMusicPanelVisible
        compactMusicActionStack?.alphaValue = compactMusicPanelVisible ? 1.0 : 0.0
        updateCompactMusicActionButtons(hasSelection: hasSelection)

        if let selectedCompactMusicIndex, compactMusicTracks.indices.contains(selectedCompactMusicIndex) {
            let track = compactMusicTracks[selectedCompactMusicIndex]
            let isActive = activeMusicTrackID == track.id && musicPlayer != nil
            let isPlaying = isActive && (musicPlayer?.isPlaying == true)
            compactPreviewSelectionLabel?.stringValue = track.title
            compactPreviewSelectionLabel?.textColor = musicInkColor
            let playbackText = isPlaying ? "正在播放" : (isActive ? "已暂停" : "未播放")
            compactPreviewMetaLabel?.stringValue = "\(playbackText) · \(track.metaText)"
            compactPreviewMetaLabel?.textColor = isActive ? musicAccentColor : mutedInkColor
            compactMusicPlayPauseButton?.title = isPlaying ? "暂停" : (isActive ? "继续" : "播放")
        } else {
            if musicProcess != nil {
                compactPreviewSelectionLabel?.stringValue = "正在为\(currentMusicSourceSummary())生成\(musicResultNoun())"
                compactPreviewSelectionLabel?.textColor = musicInkColor
                compactPreviewMetaLabel?.stringValue = "\(musicGenerationSummary()) · \(musicPromptStateSummary())"
                compactPreviewMetaLabel?.textColor = musicAccentColor
            } else {
                compactPreviewSelectionLabel?.stringValue = compactMusicTracks.isEmpty
                    ? (recentMusicTracksLoading ? "正在载入作品" : "还没有生成过作品")
                    : "选择一首作品"
                compactPreviewSelectionLabel?.textColor = compactMusicTracks.isEmpty ? musicInkColor : mutedInkColor
                compactPreviewMetaLabel?.stringValue = compactMusicTracks.isEmpty
                    ? (recentMusicTracksLoading
                        ? "正在后台读取音乐记录"
                        : "\(currentMusicSourceSummary()) · \(musicGenerationSummary()) · \(musicPromptStateSummary())")
                    : "单击选中，双击试听"
                compactPreviewMetaLabel?.textColor = mutedInkColor
            }
            compactMusicPlayPauseButton?.title = "播放"
        }
    }

    private func updateCompactMusicPanelHeader() {
        compactPreviewTitleLabel?.stringValue = "音乐工坊"
        if musicProcess != nil {
            compactPreviewSubtitleLabel?.stringValue = "生成中 · \(selectedMusicStyle().label) · \(selectedMusicGenerationMode().shortLabel)"
        } else {
            compactPreviewSubtitleLabel?.stringValue = "\(currentMusicSourceSummary()) · \(selectedMusicStyle().label) · \(selectedMusicGenerationMode().shortLabel) · \(musicPromptStateSummary())"
        }
    }

    private func updateCompactMusicActionButtons(hasSelection: Bool? = nil) {
        let resolvedHasSelection = hasSelection ?? (selectedCompactMusicIndex != nil)
        let canGenerate = musicProcess == nil && musicGenerationInputAvailable()
        let promptConfigured = hasCustomMusicPrompt()
        let isActiveSelection: Bool
        let isPlaying: Bool
        if let selectedCompactMusicIndex, compactMusicTracks.indices.contains(selectedCompactMusicIndex) {
            let track = compactMusicTracks[selectedCompactMusicIndex]
            isActiveSelection = activeMusicTrackID == track.id && musicPlayer != nil
            isPlaying = isActiveSelection && (musicPlayer?.isPlaying == true)
        } else {
            isActiveSelection = false
            isPlaying = false
        }

        compactMusicGenerateButton?.title = musicProcess == nil ? "生成音乐" : "生成中"
        compactMusicPromptButton?.title = promptConfigured ? "已写" : "灵感"
        compactMusicStyleButton?.title = selectedMusicStyle().label
        compactMusicModeButton?.title = selectedMusicGenerationMode().shortLabel
        compactMusicRenameButton?.title = "改名"
        compactMusicPlayPauseButton?.title = isPlaying ? "暂停" : (isActiveSelection ? "继续" : "播放")
        compactMusicOpenButton?.title = "文件"
        compactMusicGenerateButton?.isEnabled = canGenerate
        compactMusicPromptButton?.isEnabled = musicProcess == nil
        compactMusicStyleButton?.isEnabled = musicProcess == nil
        compactMusicModeButton?.isEnabled = musicProcess == nil
        compactMusicRenameButton?.isEnabled = resolvedHasSelection && musicProcess == nil
        compactMusicPlayPauseButton?.isEnabled = resolvedHasSelection
        compactMusicOpenButton?.isEnabled = resolvedHasSelection
        applyCompactActionButtonStyle(compactMusicGenerateButton, variant: .primary)
        applyCompactActionButtonStyle(compactMusicPromptButton, variant: promptConfigured ? .accentSoft : .neutral)
        applyCompactActionButtonStyle(compactMusicStyleButton, variant: .neutral)
        applyCompactActionButtonStyle(compactMusicModeButton, variant: .neutral)
        applyCompactActionButtonStyle(compactMusicRenameButton, variant: .neutral)
        applyCompactActionButtonStyle(compactMusicPlayPauseButton, variant: isActiveSelection || isPlaying ? .accentSoft : .ghost)
        applyCompactActionButtonStyle(compactMusicOpenButton, variant: .ghost)
    }

    private func updateCompactProjectActionButtons(hasSelection: Bool? = nil) {
        let resolvedHasSelection = hasSelection ?? (selectedCompactProject() != nil)
        let selectedProject = selectedCompactProject()
        let isOrganizingSelection = selectedProject.map { organizingProjectRunID == $0.runID } ?? false
        let canStartOrganization = resolvedHasSelection && organizeProcess == nil

        compactOpenNotesButton?.title = "查看"
        compactOrganizeSummaryButton?.title = isOrganizingSelection
            ? "整理中"
            : (selectedProject?.hasOrganizedNotes == true ? "重整" : "整理")
        compactEditTemplateButton?.title = selectedOrganizationTemplate().name
        compactRenameProjectButton?.title = "改名"
        compactOpenTranscriptButton?.title = "原文"

        compactOpenNotesButton?.isEnabled = resolvedHasSelection && selectedProjectNotesURL() != nil && !isOrganizingSelection
        compactOrganizeSummaryButton?.isEnabled = canStartOrganization
        compactExtractKeywordsButton?.isEnabled = canStartOrganization
        compactEditTemplateButton?.isEnabled = organizeProcess == nil
        compactRenameProjectButton?.isEnabled = resolvedHasSelection && organizeProcess == nil
        compactOpenTranscriptButton?.isEnabled = resolvedHasSelection
        compactArchiveProjectButton?.isEnabled = resolvedHasSelection && organizeProcess == nil && musicProcess == nil

        applyCompactActionButtonStyle(compactOpenNotesButton, variant: selectedProject?.hasOrganizedNotes == true ? .accentSoft : .ghost)
        applyCompactActionButtonStyle(compactOrganizeSummaryButton, variant: isOrganizingSelection ? .accentSoft : .primary)
        applyCompactActionButtonStyle(compactEditTemplateButton, variant: .neutral)
        applyCompactActionButtonStyle(compactRenameProjectButton, variant: .neutral)
        applyCompactActionButtonStyle(compactOpenTranscriptButton, variant: .ghost)
        if isOrganizingSelection {
            compactOrganizeSummaryButton?.alphaValue = 1.0
        }
    }

    private func selectedMusicStyle() -> MusicStylePreset {
        availableMusicStyles[selectedMusicStyleIndex % availableMusicStyles.count]
    }

    private func selectedMusicGenerationMode() -> MusicGenerationMode {
        availableMusicGenerationModes[selectedMusicGenerationModeIndex % availableMusicGenerationModes.count]
    }

    private func musicGenerationInputAvailable() -> Bool {
        !customMusicPrompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            || selectedCompactProject() != nil
            || transcriptHasContent()
    }

    private func musicGenerationLabel(for id: String) -> String {
        availableMusicGenerationModes.first(where: { $0.id == id })?.label ?? "纯音乐"
    }

    private func musicGenerationSummary() -> String {
        "\(selectedMusicStyle().label) · \(selectedMusicGenerationMode().label)"
    }

    private func hasCustomMusicPrompt() -> Bool {
        !customMusicPrompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }

    private func musicPromptStateSummary() -> String {
        hasCustomMusicPrompt() ? "自定义提示" : "默认提示"
    }

    private func currentMusicPromptSummary() -> String {
        let trimmed = customMusicPrompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return "未自定义" }
        let normalized = trimmed.replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
        guard normalized.count > 14 else { return normalized }
        let end = normalized.index(normalized.startIndex, offsetBy: 14)
        return String(normalized[..<end]) + "…"
    }

    private func musicResultNoun() -> String {
        selectedMusicGenerationMode().id == "instrumental" ? "配乐" : "歌曲"
    }

    private func musicDurationLabel(_ rawValue: Any?) -> String? {
        let seconds: Int?
        if let value = rawValue as? Int {
            seconds = value
        } else if let value = rawValue as? Double {
            seconds = Int(value.rounded())
        } else if let value = rawValue as? NSNumber {
            seconds = value.intValue
        } else {
            seconds = nil
        }
        guard let totalSeconds = seconds, totalSeconds > 0 else { return nil }
        return totalSeconds >= 60
            ? String(format: "%d:%02d", totalSeconds / 60, totalSeconds % 60)
            : "\(totalSeconds)秒"
    }

    private func currentMusicSourceSummary() -> String {
        if !customMusicPrompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
           selectedCompactProject() == nil,
           !transcriptHasContent() {
            return "自定义提示"
        }
        if let project = selectedCompactProject() {
            return "项目 \(project.runID)"
        }
        if transcriptHasContent() {
            return "本次 ASR"
        }
        return "暂无"
    }

    private func recentProjects(limit: Int, forceReload: Bool = false) -> [RecentProject] {
        if !forceReload,
           let loadedAt = recentProjectsCacheLoadedAt,
           Date().timeIntervalSince(loadedAt) < compactDataCacheTTL {
            return Array(cachedRecentProjects.prefix(limit))
        }
        requestRecentProjectsReload(limit: max(limit, 12), forceReload: forceReload)
        return Array(cachedRecentProjects.prefix(limit))
    }

    private func recentProjectsIndexURL() -> URL {
        workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("recent_projects_index.json")
    }

    private func recentMusicIndexURL() -> URL {
        workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("music_index.json")
    }

    private func loadRecentProjects(limit: Int, forceReload: Bool = false) -> [RecentProject] {
        let runsDir = workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("runs", isDirectory: true)
        let indexURL = recentProjectsIndexURL()
        let indexModified = (try? indexURL.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
        let runsModified = (try? runsDir.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
        if !forceReload,
           FileManager.default.fileExists(atPath: indexURL.path),
           runsModified <= indexModified,
           let indexed = readRecentProjectsIndex(limit: limit),
           !indexed.isEmpty {
            return indexed
        }
        let projects = scanRecentProjects(limit: max(limit, 80), runsDir: runsDir)
        writeRecentProjectsIndex(projects)
        return Array(projects.prefix(limit))
    }

    private func scanRecentProjects(limit: Int, runsDir: URL) -> [RecentProject] {
        guard let items = try? FileManager.default.contentsOfDirectory(
            at: runsDir,
            includingPropertiesForKeys: [.contentModificationDateKey],
            options: [.skipsHiddenFiles]
        ) else {
            return []
        }

        let sorted = items.sorted { lhs, rhs in
            let l = (try? lhs.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
            let r = (try? rhs.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
            return l > r
        }

        var projects: [RecentProject] = []
        for runDir in sorted {
            let transcriptURL = runDir.appendingPathComponent("senseaudio_asr.json")
            guard FileManager.default.fileExists(atPath: transcriptURL.path),
                  let data = try? Data(contentsOf: transcriptURL),
                  let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any]
            else { continue }

            let segmentCount = payload["segment_count"] as? Int ?? 0
            let transcriptText = (payload["transcript_text"] as? String ?? "")
                .replacingOccurrences(of: "\n", with: " ")
                .trimmingCharacters(in: .whitespacesAndNewlines)
            guard segmentCount > 0, !transcriptText.isEmpty else { continue }

            let timeText = prettyRunTimestamp(runDir.lastPathComponent)
            let snippet = compactPreviewSnippet(transcriptText)
            let hasNotes = projectHasOrganizedNotes(in: runDir)
            let metaText = "\(timeText) · \(segmentCount)段" + (hasNotes ? " · 已整理" : " · 未整理")
            let title = projectDisplayName(in: runDir) ?? snippet
            projects.append(
                RecentProject(
                    runID: runDir.lastPathComponent,
                    transcriptURL: transcriptURL,
                    title: title,
                    snippet: snippet,
                    metaText: metaText,
                    hasOrganizedNotes: hasNotes,
                    runDirectory: runDir
                )
            )
            if projects.count >= limit {
                break
            }
        }
        return projects
    }

    private func readRecentProjectsIndex(limit: Int) -> [RecentProject]? {
        let url = recentProjectsIndexURL()
        guard let data = try? Data(contentsOf: url),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let entries = payload["projects"] as? [[String: Any]]
        else {
            return nil
        }
        var projects: [RecentProject] = []
        for entry in entries {
            guard let runID = entry["run_id"] as? String,
                  let transcriptPath = entry["transcript_path"] as? String,
                  let runPath = entry["run_directory"] as? String
            else { continue }
            let transcriptURL = URL(fileURLWithPath: transcriptPath)
            let runDirectory = URL(fileURLWithPath: runPath)
            guard FileManager.default.fileExists(atPath: transcriptURL.path),
                  FileManager.default.fileExists(atPath: runDirectory.path)
            else { continue }
            let hasNotes = projectHasOrganizedNotes(in: runDirectory)
            let segmentCount = entry["segment_count"] as? Int ?? 0
            let timeText = prettyRunTimestamp(runID)
            let metaText = "\(timeText) · \(segmentCount)段" + (hasNotes ? " · 已整理" : " · 未整理")
            let snippet = (entry["snippet"] as? String ?? "").trimmingCharacters(in: .whitespacesAndNewlines)
            let title = (projectDisplayName(in: runDirectory) ?? entry["title"] as? String ?? snippet)
                .trimmingCharacters(in: .whitespacesAndNewlines)
            projects.append(
                RecentProject(
                    runID: runID,
                    transcriptURL: transcriptURL,
                    title: title.isEmpty ? snippet : title,
                    snippet: snippet,
                    metaText: metaText,
                    hasOrganizedNotes: hasNotes,
                    runDirectory: runDirectory
                )
            )
            if projects.count >= limit {
                break
            }
        }
        return projects
    }

    private func writeRecentProjectsIndex(_ projects: [RecentProject]) {
        let url = recentProjectsIndexURL()
        try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        let entries: [[String: Any]] = projects.map { project in
            [
                "run_id": project.runID,
                "transcript_path": project.transcriptURL.path,
                "run_directory": project.runDirectory.path,
                "title": project.title,
                "snippet": project.snippet,
                "segment_count": projectSegmentCount(project),
                "has_organized_notes": project.hasOrganizedNotes,
            ]
        }
        let payload: [String: Any] = [
            "version": 1,
            "updated_at": ISO8601DateFormatter().string(from: Date()),
            "projects": entries,
        ]
        if let data = try? JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted, .sortedKeys]) {
            try? data.write(to: url, options: .atomic)
        }
    }

    private func projectSegmentCount(_ project: RecentProject) -> Int {
        guard let data = try? Data(contentsOf: project.transcriptURL),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any]
        else { return 0 }
        return payload["segment_count"] as? Int ?? 0
    }

    private func projectHasOrganizedNotes(in runDir: URL) -> Bool {
        if [
            "organized_notes.md",
            "keywords_notes.md",
            "meeting_notes.md",
            "study_notes.md",
            "todo_notes.md",
        ].contains(where: { FileManager.default.fileExists(atPath: runDir.appendingPathComponent($0).path) }) {
            return true
        }
        let generated = (try? FileManager.default.contentsOfDirectory(
            at: runDir,
            includingPropertiesForKeys: nil,
            options: [.skipsHiddenFiles]
        )) ?? []
        return generated.contains {
            $0.lastPathComponent.hasPrefix("organized_") && $0.lastPathComponent.hasSuffix("_notes.md")
        }
    }

    private func projectMetadataURL(in runDirectory: URL) -> URL {
        runDirectory.appendingPathComponent("project_meta.json")
    }

    private func projectDisplayName(in runDirectory: URL) -> String? {
        let url = projectMetadataURL(in: runDirectory)
        guard let data = try? Data(contentsOf: url),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let title = payload["title"] as? String
        else {
            return nil
        }
        let trimmed = title.trimmingCharacters(in: .whitespacesAndNewlines)
        return trimmed.isEmpty ? nil : trimmed
    }

    private func saveProjectDisplayName(_ title: String, for project: RecentProject) throws {
        var payload: [String: Any] = [:]
        let url = projectMetadataURL(in: project.runDirectory)
        if let data = try? Data(contentsOf: url),
           let existing = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
            payload = existing
        }
        payload["title"] = title
        payload["updated_at"] = ISO8601DateFormatter().string(from: Date())
        let output = try JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted, .sortedKeys])
        try output.write(to: url, options: .atomic)
    }

    private func recentMusicTracks(limit: Int, forceReload: Bool = false) -> [GeneratedMusicTrack] {
        if !forceReload,
           let loadedAt = recentMusicTracksCacheLoadedAt,
           Date().timeIntervalSince(loadedAt) < compactDataCacheTTL {
            return Array(cachedRecentMusicTracks.prefix(limit))
        }
        requestRecentMusicTracksReload(limit: max(limit, 12), forceReload: forceReload)
        return Array(cachedRecentMusicTracks.prefix(limit))
    }

    private func loadRecentMusicTracks(limit: Int, forceReload: Bool = false) -> [GeneratedMusicTrack] {
        if !forceReload,
           let indexed = readRecentMusicIndex(limit: limit),
           !indexed.isEmpty {
            return indexed
        }
        let tracks = scanRecentMusicTracks(limit: max(limit, 80))
        writeRecentMusicIndex(tracks)
        return Array(tracks.prefix(limit))
    }

    private func scanRecentMusicTracks(limit: Int) -> [GeneratedMusicTrack] {
        let searchRoots = [
            workspaceDir
                .appendingPathComponent("state", isDirectory: true)
                .appendingPathComponent("realtime_interpreter", isDirectory: true),
            workspaceDir
                .appendingPathComponent("output", isDirectory: true),
        ].filter { FileManager.default.fileExists(atPath: $0.path) }
        guard !searchRoots.isEmpty else {
            return []
        }

        var tracks: [GeneratedMusicTrack] = []
        var seenAudioPaths = Set<String>()
        for root in searchRoots {
            guard let enumerator = FileManager.default.enumerator(at: root, includingPropertiesForKeys: [.contentModificationDateKey]) else {
                continue
            }
            for case let fileURL as URL in enumerator {
                guard fileURL.lastPathComponent == "generated_music.meta.json",
                      let data = try? Data(contentsOf: fileURL),
                      let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any]
                else { continue }

                guard let outputAudio = payload["output_audio"] as? String else { continue }
                let audioURL = URL(fileURLWithPath: outputAudio)
                guard FileManager.default.fileExists(atPath: audioURL.path) else { continue }
                let audioKey = audioURL.standardizedFileURL.path
                guard !seenAudioPaths.contains(audioKey) else { continue }
                seenAudioPaths.insert(audioKey)

                let trimmedTitle = (payload["title"] as? String)?
                    .trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
                let title = trimmedTitle.isEmpty ? audioURL.deletingPathExtension().lastPathComponent : trimmedTitle
                let createdText = (payload["created_at"] as? String) ?? ""
                let sourcePath = (payload["source_path"] as? String).flatMap { $0.isEmpty ? nil : URL(fileURLWithPath: $0) }
                let styleID = (payload["style_preset"] as? String) ?? "cinematic"
                let generationModeID = (payload["generation_mode"] as? String) ?? "instrumental"
                let createdDate = ISO8601DateFormatter().date(from: createdText) ?? ((try? fileURL.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast)
                let createdLabel = prettyMusicTimestamp(createdDate)
                let sourceLabel = sourcePath?.deletingPathExtension().lastPathComponent ?? fileURL.deletingLastPathComponent().lastPathComponent
                let durationLabel = musicDurationLabel(payload["duration"]).map { " · \($0)" } ?? ""
                tracks.append(
                    GeneratedMusicTrack(
                        id: (payload["task_id"] as? String) ?? fileURL.deletingLastPathComponent().lastPathComponent,
                        title: title,
                        metaText: "\(createdLabel) · \(musicStyleLabel(for: styleID)) · \(musicGenerationLabel(for: generationModeID))\(durationLabel) · \(sourceLabel)",
                        audioURL: audioURL,
                        sourceURL: sourcePath,
                        metadataURL: fileURL,
                        createdAt: createdDate
                    )
                )
            }
        }
        return Array(tracks.sorted { $0.createdAt > $1.createdAt }.prefix(limit))
    }

    private func readRecentMusicIndex(limit: Int) -> [GeneratedMusicTrack]? {
        let url = recentMusicIndexURL()
        guard let data = try? Data(contentsOf: url),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let entries = payload["tracks"] as? [[String: Any]]
        else {
            return nil
        }
        var tracks: [GeneratedMusicTrack] = []
        for entry in entries {
            guard let id = entry["id"] as? String,
                  let audioPath = entry["audio_path"] as? String,
                  let metadataPath = entry["metadata_path"] as? String,
                  let createdAtRaw = entry["created_at"] as? String
            else { continue }
            let audioURL = URL(fileURLWithPath: audioPath)
            let metadataURL = URL(fileURLWithPath: metadataPath)
            guard FileManager.default.fileExists(atPath: audioURL.path),
                  FileManager.default.fileExists(atPath: metadataURL.path)
            else { continue }
            let createdAt = ISO8601DateFormatter().date(from: createdAtRaw) ?? .distantPast
            let sourceURL = (entry["source_path"] as? String).flatMap { $0.isEmpty ? nil : URL(fileURLWithPath: $0) }
            tracks.append(
                GeneratedMusicTrack(
                    id: id,
                    title: (entry["title"] as? String ?? audioURL.deletingPathExtension().lastPathComponent),
                    metaText: (entry["meta_text"] as? String ?? ""),
                    audioURL: audioURL,
                    sourceURL: sourceURL,
                    metadataURL: metadataURL,
                    createdAt: createdAt
                )
            )
            if tracks.count >= limit {
                break
            }
        }
        return tracks
    }

    private func writeRecentMusicIndex(_ tracks: [GeneratedMusicTrack]) {
        let url = recentMusicIndexURL()
        try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        let formatter = ISO8601DateFormatter()
        let entries: [[String: Any]] = tracks.map { track in
            [
                "id": track.id,
                "title": track.title,
                "meta_text": track.metaText,
                "audio_path": track.audioURL.path,
                "source_path": track.sourceURL?.path ?? "",
                "metadata_path": track.metadataURL.path,
                "created_at": formatter.string(from: track.createdAt),
            ]
        }
        let payload: [String: Any] = [
            "version": 1,
            "updated_at": formatter.string(from: Date()),
            "tracks": entries,
        ]
        if let data = try? JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted, .sortedKeys]) {
            try? data.write(to: url, options: .atomic)
        }
    }

    private func requestRecentProjectsReload(limit: Int, forceReload: Bool) {
        if !forceReload,
           recentProjectsLoading {
            return
        }

        recentProjectsLoading = true
        recentProjectsLoadToken += 1
        let token = recentProjectsLoadToken
        compactDataQueue.async { [weak self] in
            guard let self else { return }
            let projects = self.loadRecentProjects(limit: limit, forceReload: forceReload)
            DispatchQueue.main.async { [weak self] in
                guard let self, token == self.recentProjectsLoadToken else { return }
                self.recentProjectsLoading = false
                self.cachedRecentProjects = projects
                self.recentProjectsCacheLoadedAt = Date()
                if self.compactProjectPanelVisible && !self.compactMusicPanelVisible {
                    self.refreshCompactPreview()
                }
                self.refreshOrganizeButton()
            }
        }
    }

    private func requestRecentMusicTracksReload(limit: Int, forceReload: Bool) {
        if !forceReload,
           recentMusicTracksLoading {
            return
        }

        recentMusicTracksLoading = true
        recentMusicTracksLoadToken += 1
        let token = recentMusicTracksLoadToken
        compactDataQueue.async { [weak self] in
            guard let self else { return }
            let tracks = self.loadRecentMusicTracks(limit: limit, forceReload: forceReload)
            DispatchQueue.main.async { [weak self] in
                guard let self, token == self.recentMusicTracksLoadToken else { return }
                self.recentMusicTracksLoading = false
                self.cachedRecentMusicTracks = tracks
                self.recentMusicTracksCacheLoadedAt = Date()
                if self.compactMusicPanelVisible {
                    self.refreshCompactPreview()
                }
                self.refreshOrganizeButton()
            }
        }
    }

    private func invalidateRecentProjectsCache() {
        recentProjectsCacheLoadedAt = nil
    }

    private func invalidateRecentMusicTracksCache() {
        recentMusicTracksCacheLoadedAt = nil
    }

    private func warmCompactCachesIfNeeded() {
        if recentProjectsCacheLoadedAt == nil {
            requestRecentProjectsReload(limit: 12, forceReload: false)
        }
        if recentMusicTracksCacheLoadedAt == nil {
            requestRecentMusicTracksReload(limit: 12, forceReload: false)
        }
    }

    private func prettyMusicTimestamp(_ date: Date) -> String {
        let output = DateFormatter()
        output.locale = Locale(identifier: "zh_CN")
        output.dateFormat = "M月d日 HH:mm"
        return output.string(from: date)
    }

    private func musicStyleLabel(for id: String) -> String {
        availableMusicStyles.first(where: { $0.id == id })?.label ?? "电影感"
    }

    private func compactPreviewSnippet(_ text: String) -> String {
        let normalized = text.replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        guard normalized.count > 18 else { return normalized }
        let end = normalized.index(normalized.startIndex, offsetBy: 18)
        return String(normalized[..<end]) + "…"
    }

    private func prettyRunTimestamp(_ runID: String) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyyMMdd-HHmmss"
        if let date = formatter.date(from: runID) {
            let output = DateFormatter()
            output.locale = Locale(identifier: "zh_CN")
            output.dateFormat = "M月d日 HH:mm"
            return output.string(from: date)
        }
        return runID
    }

    private func refreshOrganizeButton() {
        let enabled = !controller.isRunning && organizeProcess == nil && transcriptHasContent()
        organizeButton.isEnabled = enabled
        organizeButton.alphaValue = enabled ? 1.0 : 0.45
        let hasClipboard = !latestClipboardText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
        let speechActive = speechProcess != nil || (speechPlayer?.isPlaying == true)
        readClipboardButton.isEnabled = hasClipboard || speechActive
        readClipboardButton.alphaValue = readClipboardButton.isEnabled ? 1.0 : 0.45
        readClipboardButton.title = speechActive ? "停止朗读" : "朗读复制"
        voiceButton.title = "音色 \(selectedTTSVoice().label)"
        updateCompactMusicActionButtons()
        compactSatelliteStartButton?.isEnabled = !controller.isRunning
        compactSatelliteStartButton?.toolTip = nil
        compactSatelliteReadButton?.isEnabled = hasClipboard || speechActive
        compactSatelliteReadButton?.toolTip = nil
        compactSatelliteMusicButton?.isEnabled = musicProcess == nil
        compactSatelliteMusicButton?.toolTip = nil
        compactSatelliteProjectButton?.isEnabled = !compactPreviewProjects.isEmpty
        compactSatelliteProjectButton?.toolTip = nil
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.16
            compactSatelliteReadButton?.animator().alphaValue = (hasClipboard || speechActive) && isCompactHoverVisible ? 1.0 : 0.0
            compactSatelliteMusicButton?.animator().alphaValue = isCompactHoverVisible ? 1.0 : 0.0
        }
        compactSatelliteReadButton?.isHidden = !((hasClipboard || speechActive) && isCompactHoverVisible)
        compactSatelliteMusicButton?.isHidden = !isCompactHoverVisible
        compactSatelliteProjectButton?.isEnabled = !cachedRecentProjects.isEmpty
        if compactMusicPanelVisible && !skipCompactPreviewRefreshInButtonSync {
            updateCompactMusicPanelHeader()
        }
    }

    private func currentOutputVolumeState() -> OutputVolumeControlState? {
        if let preferredName = preferredControllableOutputDeviceName(),
           let deviceID = audioDeviceID(named: preferredName),
           let state = makeOutputVolumeControlState(for: deviceID) {
            return state
        }
        if let defaultOutputDeviceID = defaultOutputDeviceID(),
           let state = makeOutputVolumeControlState(for: defaultOutputDeviceID),
           !isAggregateRouteDevice(state.deviceName) {
            return state
        }
        for deviceID in allAudioDeviceIDs() {
            guard let state = makeOutputVolumeControlState(for: deviceID),
                  !isAggregateRouteDevice(state.deviceName) else {
                continue
            }
            return state
        }
        return nil
    }

    private func preferredControllableOutputDeviceName() -> String? {
        let state = audioRouteStateValues()
        if let saved = Int(state["PREV_OUTPUT_VOLUME"] ?? ""), saved > 0 {
            lastNonZeroOutputVolumePercent = saved
        }
        let candidates = [
            state["PREV_OUTPUT_DEVICE"],
            state["CURRENT_OUTPUT_DEVICE"],
            state["ROUTE_DEVICE"],
        ]
        for candidate in candidates {
            guard let candidate,
                  !candidate.isEmpty,
                  !isAggregateRouteDevice(candidate) else {
                continue
            }
            return candidate
        }
        return nil
    }

    private func audioRouteStateValues() -> [String: String] {
        if let loadedAt = audioRouteStateLoadedAt,
           Date().timeIntervalSince(loadedAt) < audioRouteStateCacheTTL {
            return cachedAudioRouteStateValues
        }
        let stateURL = workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("audio_route_state.sh")
        guard let text = try? String(contentsOf: stateURL, encoding: .utf8) else {
            cachedAudioRouteStateValues = [:]
            audioRouteStateLoadedAt = Date()
            return [:]
        }

        var values: [String: String] = [:]
        for rawLine in text.components(separatedBy: .newlines) {
            let line = rawLine.trimmingCharacters(in: .whitespacesAndNewlines)
            guard !line.isEmpty,
                  !line.hasPrefix("#"),
                  let separator = line.firstIndex(of: "=") else {
                continue
            }
            let key = String(line[..<separator])
            var value = String(line[line.index(after: separator)...]).trimmingCharacters(in: .whitespaces)
            if value.hasPrefix("'"), value.hasSuffix("'"), value.count >= 2 {
                value.removeFirst()
                value.removeLast()
                value = value.replacingOccurrences(of: "'\\''", with: "'")
            }
            values[key] = value
        }
        cachedAudioRouteStateValues = values
        audioRouteStateLoadedAt = Date()
        return values
    }

    private func isAggregateRouteDevice(_ name: String) -> Bool {
        let lowered = name.lowercased()
        return lowered.contains("multi-output")
            || name.contains("多输出设备")
            || lowered.contains("blackhole")
    }

    private func allAudioDeviceIDs() -> [AudioDeviceID] {
        if let loadedAt = audioDeviceCacheLoadedAt,
           Date().timeIntervalSince(loadedAt) < audioDeviceCacheTTL,
           !cachedAudioDeviceIDs.isEmpty {
            return cachedAudioDeviceIDs
        }
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioHardwarePropertyDevices,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var size: UInt32 = 0
        guard AudioObjectGetPropertyDataSize(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size) == noErr else {
            return []
        }
        let count = Int(size) / MemoryLayout<AudioDeviceID>.size
        var ids = Array(repeating: AudioDeviceID(0), count: count)
        guard AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &ids) == noErr else {
            return []
        }
        cachedAudioDeviceIDs = ids
        cachedAudioDeviceNames.removeAll()
        audioDeviceCacheLoadedAt = Date()
        return ids
    }

    private func audioDeviceID(named deviceName: String) -> AudioDeviceID? {
        let exactMatch = allAudioDeviceIDs().first { audioDeviceName(for: $0) == deviceName }
        if let exactMatch {
            return exactMatch
        }
        return allAudioDeviceIDs().first {
            (audioDeviceName(for: $0) ?? "").localizedCaseInsensitiveContains(deviceName)
        }
    }

    private func defaultOutputDeviceID() -> AudioDeviceID? {
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioHardwarePropertyDefaultOutputDevice,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var deviceID = AudioDeviceID(0)
        var size = UInt32(MemoryLayout<AudioDeviceID>.size)
        let status = AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &address, 0, nil, &size, &deviceID)
        return status == noErr ? deviceID : nil
    }

    private func audioDeviceName(for deviceID: AudioDeviceID) -> String? {
        if let cached = cachedAudioDeviceNames[deviceID] {
            return cached
        }
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioObjectPropertyName,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain
        )
        var name: Unmanaged<CFString>?
        var size = UInt32(MemoryLayout<Unmanaged<CFString>?>.size)
        let status = withUnsafeMutablePointer(to: &name) {
            AudioObjectGetPropertyData(deviceID, &address, 0, nil, &size, $0)
        }
        guard status == noErr else {
            return nil
        }
        let value = name?.takeRetainedValue() as String?
        if let value {
            cachedAudioDeviceNames[deviceID] = value
        }
        return value
    }

    private func makeOutputVolumeControlState(for deviceID: AudioDeviceID) -> OutputVolumeControlState? {
        let channels = outputVolumeChannels(for: deviceID)
        guard !channels.isEmpty else {
            return nil
        }
        let values = channels.compactMap { outputVolumeScalar(for: deviceID, channel: $0) }
        guard !values.isEmpty else {
            return nil
        }
        let average = values.reduce(0, +) / Float(values.count)
        let percent = max(0, min(100, Int((average * 100).rounded())))
        let deviceName = audioDeviceName(for: deviceID) ?? "当前输出"
        return OutputVolumeControlState(
            deviceID: deviceID,
            deviceName: deviceName,
            channels: channels,
            percent: percent,
            isMuted: percent == 0
        )
    }

    private func outputVolumeChannels(for deviceID: AudioDeviceID) -> [UInt32] {
        if audioDeviceHasVolume(deviceID, channel: kAudioObjectPropertyElementMain) {
            return [kAudioObjectPropertyElementMain]
        }
        let stereoChannels = preferredStereoChannels(for: deviceID)
        let supportedStereoChannels = stereoChannels.filter { audioDeviceHasVolume(deviceID, channel: $0) }
        if !supportedStereoChannels.isEmpty {
            return Array(Set(supportedStereoChannels)).sorted()
        }
        var fallbackChannels: [UInt32] = []
        for channel in 1...8 where audioDeviceHasVolume(deviceID, channel: UInt32(channel)) {
            fallbackChannels.append(UInt32(channel))
        }
        return fallbackChannels
    }

    private func preferredStereoChannels(for deviceID: AudioDeviceID) -> [UInt32] {
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyPreferredChannelsForStereo,
            mScope: kAudioDevicePropertyScopeOutput,
            mElement: kAudioObjectPropertyElementMain
        )
        guard AudioObjectHasProperty(deviceID, &address) else {
            return []
        }
        var channels = [UInt32](repeating: 0, count: 2)
        var size = UInt32(MemoryLayout<UInt32>.size * channels.count)
        let status = AudioObjectGetPropertyData(deviceID, &address, 0, nil, &size, &channels)
        guard status == noErr else {
            return []
        }
        return channels.filter { $0 > 0 }
    }

    private func audioDeviceHasVolume(_ deviceID: AudioDeviceID, channel: UInt32) -> Bool {
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyVolumeScalar,
            mScope: kAudioDevicePropertyScopeOutput,
            mElement: channel
        )
        return AudioObjectHasProperty(deviceID, &address)
    }

    private func outputVolumeScalar(for deviceID: AudioDeviceID, channel: UInt32) -> Float? {
        var address = AudioObjectPropertyAddress(
            mSelector: kAudioDevicePropertyVolumeScalar,
            mScope: kAudioDevicePropertyScopeOutput,
            mElement: channel
        )
        guard AudioObjectHasProperty(deviceID, &address) else {
            return nil
        }
        var value: Float32 = 0
        var size = UInt32(MemoryLayout<Float32>.size)
        let status = AudioObjectGetPropertyData(deviceID, &address, 0, nil, &size, &value)
        return status == noErr ? Float(value) : nil
    }

    private func setOutputVolumePercent(_ percent: Int, using state: OutputVolumeControlState? = nil) -> Bool {
        guard let currentState = state ?? currentOutputVolumeState() else {
            return false
        }
        let scalar = Float32(max(0, min(100, percent))) / 100
        var didSet = false
        for channel in currentState.channels {
            var address = AudioObjectPropertyAddress(
                mSelector: kAudioDevicePropertyVolumeScalar,
                mScope: kAudioDevicePropertyScopeOutput,
                mElement: channel
            )
            guard AudioObjectHasProperty(currentState.deviceID, &address) else {
                continue
            }
            var value = scalar
            let status = AudioObjectSetPropertyData(
                currentState.deviceID,
                &address,
                0,
                nil,
                UInt32(MemoryLayout<Float32>.size),
                &value
            )
            if status == noErr {
                didSet = true
            }
        }
        if didSet, percent > 0 {
            lastNonZeroOutputVolumePercent = percent
        }
        return didSet
    }

    private func adjustOutputVolume(by delta: Int) {
        guard let state = currentOutputVolumeState() else {
            statusLabel.stringValue = "当前输出链路没有可调的音量设备"
            return
        }
        let baseline = state.isMuted ? lastNonZeroOutputVolumePercent : state.percent
        let target = max(0, min(100, baseline + delta))
        guard setOutputVolumePercent(target, using: state) else {
            statusLabel.stringValue = "\(state.deviceName) 音量调整失败"
            return
        }
        statusLabel.stringValue = "\(state.deviceName) 音量 \(target)%"
    }

    private func handleVolumeScroll(_ event: NSEvent) {
        let delta = event.scrollingDeltaY == 0 ? -event.scrollingDeltaX : event.scrollingDeltaY
        guard abs(delta) >= 0.35 else {
            return
        }

        compactVolumeScrollAccumulator -= delta
        let threshold: CGFloat = event.hasPreciseScrollingDeltas ? 4.0 : 0.7
        guard abs(compactVolumeScrollAccumulator) >= threshold else {
            return
        }

        let steps = Int(compactVolumeScrollAccumulator / threshold)
        compactVolumeScrollAccumulator -= CGFloat(steps) * threshold
        let adjustment = max(-18, min(18, steps * 4))
        guard adjustment != 0 else {
            return
        }
        adjustOutputVolume(by: adjustment)
        showTransientVolumeHint()
    }

    private func showTransientVolumeHint() {
        guard let state = currentOutputVolumeState() else {
            showVolumeStatusText("音量不可调")
            return
        }
        let label = state.isMuted ? "已静音" : "音量 \(state.percent)%"
        showVolumeStatusText(label)
        volumeHintClearWorkItem?.cancel()
        let workItem = DispatchWorkItem { [weak self] in
            guard let self else { return }
            if self.isCompactMode {
                self.setCompactSatelliteHint(nil)
            }
        }
        volumeHintClearWorkItem = workItem
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.9, execute: workItem)
    }

    private func showVolumeStatusText(_ text: String) {
        if isCompactMode {
            setCompactSatelliteHint(text, anchorView: compactBubbleButton)
        } else {
            statusLabel.stringValue = text
        }
    }

    private func ensureAudibleOutputVolumeForMusic() {
        guard let state = currentOutputVolumeState() else {
            return
        }
        if state.percent == 0 {
            let target = max(20, lastNonZeroOutputVolumePercent)
            _ = setOutputVolumePercent(target, using: state)
        }
    }

    private func selectedTTSVoice() -> (id: String, label: String) {
        availableTTSVoices[selectedTTSVoiceIndex % availableTTSVoices.count]
    }

    private func selectedLocalFastOption() -> LocalFastOption {
        availableLocalFastOptions[selectedLocalFastOptionIndex % availableLocalFastOptions.count]
    }

    private func selectedTranslationTarget() -> TranslationTargetOption {
        availableTranslationTargets[selectedTranslationTargetIndex % availableTranslationTargets.count]
    }

    private func pollClipboard() {
        let pasteboard = NSPasteboard.general
        guard pasteboard.changeCount != clipboardChangeCount else { return }
        clipboardChangeCount = pasteboard.changeCount
        guard let copied = pasteboard.string(forType: .string)?
            .trimmingCharacters(in: .whitespacesAndNewlines),
            !copied.isEmpty,
            copied != latestClipboardText
        else {
            return
        }
        latestClipboardText = copied
        latestClipboardCapturedAt = Date()
        appendOverlayDebug("clipboard captured chars=\(copied.count)")
        statusLabel.stringValue = "已捕获复制文本，可点击“朗读复制”"
        refreshOrganizeButton()
        refreshCompactPreview()
    }

    private func selectedCompactProject() -> RecentProject? {
        guard let selectedCompactProjectIndex, compactPreviewProjects.indices.contains(selectedCompactProjectIndex) else {
            return nil
        }
        return compactPreviewProjects[selectedCompactProjectIndex]
    }

    private func selectedProjectNotesURL() -> URL? {
        guard let project = selectedCompactProject() else { return nil }
        let activeTemplateNotes = project.runDirectory.appendingPathComponent(
            organizationOutputFilename(for: selectedOrganizationTemplateID())
        )
        if FileManager.default.fileExists(atPath: activeTemplateNotes.path) {
            return activeTemplateNotes
        }
        let candidates = [
            project.runDirectory.appendingPathComponent("organized_notes.md"),
            project.runDirectory.appendingPathComponent("keywords_notes.md"),
            project.runDirectory.appendingPathComponent("meeting_notes.md"),
            project.runDirectory.appendingPathComponent("study_notes.md"),
            project.runDirectory.appendingPathComponent("todo_notes.md"),
        ]
        if let first = candidates.first(where: { FileManager.default.fileExists(atPath: $0.path) }) {
            return first
        }
        let generated = (try? FileManager.default.contentsOfDirectory(
            at: project.runDirectory,
            includingPropertiesForKeys: [.contentModificationDateKey],
            options: [.skipsHiddenFiles]
        )) ?? []
        return generated
            .filter { $0.lastPathComponent.hasPrefix("organized_") && $0.lastPathComponent.hasSuffix("_notes.md") }
            .sorted {
                let lhs = (try? $0.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
                let rhs = (try? $1.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
                return lhs > rhs
            }
            .first
    }

    private func resetCurrentTranscriptContentState() {
        currentTranscriptHasContent = false
        currentTranscriptDiskProbeCompleted = false
    }

    private func markCurrentTranscriptHasContent() {
        currentTranscriptHasContent = true
        currentTranscriptDiskProbeCompleted = true
    }

    private func syncModeLabels() {
        modeButton.title = translationEnabled ? "双语 ON" : "双语 OFF"
        fastSubtitleButton.title = "快字 \(selectedLocalFastOption().label)"
        targetLanguageButton.title = "译到\(selectedTranslationTarget().label)"
        targetLanguageButton.alphaValue = translationEnabled ? 1.0 : 0.72
        targetLanguageButton.contentTintColor = translationEnabled ? inkColor : mutedInkColor
        metaLabel.stringValue = runningModeSummary()
    }

    private func runningModeSummary(source: String? = nil, updatedAt: String? = nil) -> String {
        var parts = [
            "模式: \(translationEnabled ? "双语→\(selectedTranslationTarget().label)" : "原文")",
            "快字: \(selectedLocalFastOption().label)",
            "输入: 系统输出 (BlackHole)",
        ]
        if let source, !source.isEmpty {
            parts.append("来源: \(source)")
        }
        if let updatedAt, !updatedAt.isEmpty {
            parts.append("更新: \(updatedAt)")
        }
        return parts.joined(separator: " | ")
    }

    private func hasSubtitleContentThisRun() -> Bool {
        currentTranscriptHasContent
            || !pendingLocalDrafts.isEmpty
            || !committedSegments.isEmpty
            || !latestSenseAudioFinal.isEmpty
    }

    private func startNewRun() {
        currentRunID = Self.makeRunID()
        resetCurrentTranscriptContentState()
        appendOverlayDebug("startNewRun runID=\(currentRunID) translation=\(translationEnabled) target=\(selectedTranslationTarget().id) localFast=\(selectedLocalFastOption().label)")
        refreshOrganizeButton()
        controller.start(
            translationEnabled: translationEnabled,
            runID: currentRunID,
            localFastOption: selectedLocalFastOption(),
            translationTarget: selectedTranslationTarget()
        )
    }

    private func currentRunDirectory() -> URL {
        workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("runs", isDirectory: true)
            .appendingPathComponent(currentRunID, isDirectory: true)
    }

    private func transcriptJSONURL() -> URL {
        currentRunDirectory().appendingPathComponent("senseaudio_asr.json")
    }

    private func transcriptHasContent() -> Bool {
        if currentTranscriptHasContent {
            return true
        }
        guard !currentRunID.isEmpty, !currentTranscriptDiskProbeCompleted else {
            return false
        }
        currentTranscriptDiskProbeCompleted = true
        let url = transcriptJSONURL()
        guard let data = try? Data(contentsOf: url),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any]
        else {
            return false
        }
        if let segmentCount = payload["segment_count"] as? Int, segmentCount > 0 {
            currentTranscriptHasContent = true
            return true
        }
        if let segments = payload["segments"] as? [[String: Any]], !segments.isEmpty {
            currentTranscriptHasContent = true
            return true
        }
        return false
    }

    private func extractOutputMarkdownPath(from text: String) -> URL? {
        guard let data = text.data(using: .utf8),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let rawPath = payload["output_markdown"] as? String
        else {
            return nil
        }
        return URL(fileURLWithPath: rawPath)
    }

    private func extractOutputAudioPath(from text: String) -> URL? {
        guard let data = text.data(using: .utf8),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let rawPath = payload["output_audio"] as? String
        else {
            return nil
        }
        return URL(fileURLWithPath: rawPath)
    }

    private static func makeRunID() -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyyMMdd-HHmmss"
        return formatter.string(from: Date())
    }

    private func apply(record: SubtitleRecord) {
        lastSubtitleEventAt = Date()
        setSubtitleOpacity(1.0)
        if !record.original.isEmpty {
            markCurrentTranscriptHasContent()
        }
        let source = record.source ?? "senseaudio"
        if source == "local_fast" {
            applyLocalDraft(record: record)
        } else {
            applySenseAudioFinal(record: record)
        }
        metaLabel.stringValue = runningModeSummary(source: source, updatedAt: record.emitted_at)
    }

    private func applyLocalDraft(record: SubtitleRecord) {
        guard !record.original.isEmpty else { return }
        if record.segment_id <= committedLocalSegmentUpperBound {
            return
        }
        if let index = pendingLocalDrafts.firstIndex(where: { $0.segmentID == record.segment_id }) {
            pendingLocalDrafts[index].text = record.original
            pendingLocalDrafts[index].isFinal = record.is_final ?? false
        } else {
            pendingLocalDrafts.append(LocalDraft(segmentID: record.segment_id, text: record.original, isFinal: record.is_final ?? false))
            pendingLocalDrafts.sort { $0.segmentID < $1.segmentID }
        }
        updateRetainedLocalFastText()
        suppressSubtitleAnimations = true
        renderCurrentSubtitleState()
        suppressSubtitleAnimations = false
        statusLabel.stringValue = (record.is_final ?? false) ? "本地快字幕完成一段" : "本地快字幕更新"
    }

    private func applySenseAudioFinal(record: SubtitleRecord) {
        guard !record.original.isEmpty else { return }
        latestSenseAudioFinal = record.original
        latestSenseAudioTranslation = record.translation.trimmingCharacters(in: .whitespacesAndNewlines)
        let previousLiveText = pendingLocalDrafts
            .map(\.text)
            .joined()
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let matched = commitSenseAudioFinal(record.original)
        appendCommittedSegment(
            text: record.original,
            translation: latestSenseAudioTranslation,
            comparedTo: matched ? previousLiveText : nil
        )
        renderCurrentSubtitleState()
        statusLabel.stringValue = latestSenseAudioTranslation.isEmpty ? "SenseAudio 终稿已更新" : "SenseAudio 双语终稿已更新"
    }

    private func renderCurrentSubtitleState(forceCommitted: String? = nil, highlightComparedTo: String? = nil) {
        _ = highlightComparedTo
        let liveDrafts = pendingLocalDrafts
            .map { draft in
                draft.text.trimmingCharacters(in: .whitespacesAndNewlines)
            }
            .filter { !$0.isEmpty }

        renderLayeredSubtitleBlock(liveDrafts: liveDrafts, forceCommitted: forceCommitted)
    }

    private func renderLayeredSubtitleBlock(liveDrafts: [String], forceCommitted: String?) {
        let liveText = liveDrafts.suffix(4).joined(separator: " ").trimmingCharacters(in: .whitespacesAndNewlines)
        let localFastText = liveText.isEmpty ? retainedLocalFastDisplayText() : liveText
        if localFastText.isEmpty {
            clearLine(historyTopLabel)
        } else {
            applyLineDisplay(to: historyTopLabel, text: clippedSubtitleTail(localFastText, limit: 72), committed: false)
        }

        let latestCommitted = committedSegments.last
        let senseText = [
            forceCommitted ?? "",
            latestCommitted?.text ?? "",
            latestSenseAudioFinal,
        ].first(where: { !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty })?
            .trimmingCharacters(in: .whitespacesAndNewlines)

        if let senseText, !senseText.isEmpty {
            applyLineDisplay(to: originalLabel, text: clippedSubtitleTail(senseText, limit: 64), committed: true)
        } else if !localFastText.isEmpty {
            applyLineDisplay(to: originalLabel, text: "等待 SenseAudio 校准...", committed: false)
        } else {
            applyLineDisplay(to: originalLabel, text: latestSenseAudioFinal.isEmpty ? "已捕获音频，但本句未识别出文本" : latestSenseAudioFinal, committed: !latestSenseAudioFinal.isEmpty)
        }

        let translationText = [
            latestCommitted?.translation ?? "",
            latestSenseAudioTranslation,
        ].first(where: { !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty })?
            .trimmingCharacters(in: .whitespacesAndNewlines)

        if let translationText, !translationText.isEmpty {
            applyLineDisplay(to: translationLabel, text: clippedSubtitleTail(translationText, limit: 58), committed: true)
        } else if translationEnabled, senseText != nil || !localFastText.isEmpty {
            applyLineDisplay(to: translationLabel, text: "等待 SenseAudio 翻译...", committed: false)
        } else {
            clearLine(translationLabel)
        }
    }

    private func clippedSubtitleTail(_ text: String, limit: Int) -> String {
        let normalized = text.replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        guard normalized.count > limit else { return normalized }
        return String(normalized.suffix(limit))
    }

    private func updateRetainedLocalFastText() {
        let text = pendingLocalDrafts
            .suffix(4)
            .map { $0.text.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
            .joined(separator: " ")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty else { return }
        retainedLocalFastText = text
        retainedLocalFastUpdatedAt = Date()
    }

    private func retainedLocalFastDisplayText() -> String {
        guard !retainedLocalFastText.isEmpty,
              let retainedLocalFastUpdatedAt,
              Date().timeIntervalSince(retainedLocalFastUpdatedAt) <= localFastTrailRetention
        else {
            return ""
        }
        return retainedLocalFastText
    }

    private func renderBilingualSubtitleBlock(liveDrafts: [String], forceCommitted: String?) {
        let latestCommitted = committedSegments.last
        let currentOriginal = [
            liveDrafts.suffix(2).joined(separator: " ").trimmingCharacters(in: .whitespacesAndNewlines),
            latestCommitted?.text ?? "",
            forceCommitted ?? "",
            latestSenseAudioFinal,
        ].first(where: { !$0.isEmpty }) ?? "已捕获音频，但本句未识别出文本"
        let currentTranslation = [
            latestCommitted?.translation ?? "",
            latestSenseAudioTranslation,
        ].first(where: { !$0.isEmpty })

        clearLine(historyTopLabel)
        if let currentTranslation, !currentTranslation.isEmpty {
            applyLineDisplay(to: translationLabel, text: currentTranslation, committed: true)
        } else {
            showTranslationPlaceholder()
        }
        applyLineDisplay(to: originalLabel, text: currentOriginal, committed: liveDrafts.isEmpty)
    }

    private func renderTwoLineBlock(liveDrafts: [String]) {
        let committedText = committedSegments
            .suffix(4)
            .map(\.text)
            .joined(separator: " ")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let liveText = liveDrafts.suffix(2).joined(separator: " ").trimmingCharacters(in: .whitespacesAndNewlines)
        let fullText = [committedText, liveText]
            .filter { !$0.isEmpty }
            .joined(separator: " ")
            .trimmingCharacters(in: .whitespacesAndNewlines)

        let visible = rollingLineWindow(for: fullText.isEmpty ? "已捕获音频，但本句未识别出文本" : fullText)
        clearLine(translationLabel)

        if visible.count == 1 {
            clearLine(historyTopLabel)
            applyLineDisplay(to: originalLabel, text: visible[0], committed: !committedText.isEmpty && liveText.isEmpty)
            return
        }

        let historyCommitted = liveText.isEmpty
        applyLineDisplay(to: historyTopLabel, text: visible[0], committed: historyCommitted)
        applyLineDisplay(to: originalLabel, text: visible[1], committed: false)
    }

    private func rollingLineWindow(for text: String) -> [String] {
        let normalized = text.replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        guard !normalized.isEmpty else { return [] }

        let charLimit = 28
        let characters = Array(normalized)
        let tailCount = min(characters.count, charLimit * 2)
        let tail = Array(characters.suffix(tailCount))
        if tail.count <= charLimit {
            return [String(tail)]
        }

        let splitIndex = max(charLimit, tail.count - charLimit)
        let first = String(tail.prefix(splitIndex)).trimmingCharacters(in: .whitespacesAndNewlines)
        let second = String(tail.suffix(tail.count - splitIndex)).trimmingCharacters(in: .whitespacesAndNewlines)
        return [first, second].filter { !$0.isEmpty }
    }

    private func animateLineChange(_ label: NSTextField, targetAlpha: CGFloat, rise: CGFloat) {
        guard let layer = label.layer else {
            label.alphaValue = targetAlpha
            return
        }
        layer.removeAnimation(forKey: "subtitle-rise")
        layer.removeAnimation(forKey: "subtitle-fade")

        let move = CABasicAnimation(keyPath: "transform.translation.y")
        move.fromValue = rise
        move.toValue = 0
        move.duration = label === translationLabel ? 0.30 : 0.24
        move.timingFunction = CAMediaTimingFunction(name: .easeOut)

        let fade = CABasicAnimation(keyPath: "opacity")
        let currentOpacity = layer.presentation()?.opacity ?? layer.opacity
        fade.fromValue = min(Float(targetAlpha), max(0.0, currentOpacity * 0.65))
        fade.toValue = targetAlpha
        fade.duration = label === translationLabel ? 0.28 : 0.22
        fade.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)

        layer.opacity = Float(targetAlpha)
        layer.add(move, forKey: "subtitle-rise")
        layer.add(fade, forKey: "subtitle-fade")
        label.alphaValue = targetAlpha
    }

    private func applyLineDisplay(to label: NSTextField, text: String, committed: Bool) {
        let previousText = storedSubtitleBodyText(for: label)
        let paragraph = NSMutableParagraphStyle()
        paragraph.lineSpacing = 3
        paragraph.lineBreakMode = label.lineBreakMode
        paragraph.tabStops = [NSTextTab(textAlignment: .left, location: 104, options: [:])]
        paragraph.defaultTabInterval = 104
        let attributed = attributedSubtitleLine(for: label, text: text, committed: committed, paragraph: paragraph)
        label.attributedStringValue = attributed
        label.isHidden = false
        let targetAlpha: CGFloat
        if label === historyTopLabel {
            targetAlpha = 0.72
        } else if label === translationLabel {
            targetAlpha = text.contains("等待 SenseAudio") ? 0.58 : 0.88
        } else {
            targetAlpha = 1.0
        }
        if previousText != text {
            if shouldAnimateLineChange(label: label, previousText: previousText, newText: text, committed: committed) {
                let rise: CGFloat
                if label === historyTopLabel {
                    rise = 5
                } else if label === originalLabel {
                    rise = 8
                } else {
                    rise = 7
                }
                animateLineChange(label, targetAlpha: targetAlpha, rise: rise)
            } else {
                label.alphaValue = targetAlpha
                label.layer?.opacity = Float(targetAlpha)
            }
        } else {
            label.alphaValue = targetAlpha
        }
        if label === historyTopLabel {
            historyTopHeightConstraint?.constant = 16
            lastDisplayedHistoryText = text
        } else if label === translationLabel {
            translationHeightConstraint?.constant = 18
            lastDisplayedTranslationText = text
        } else if label === originalLabel {
            lastDisplayedOriginalText = text
        }
    }

    private func storedSubtitleBodyText(for label: NSTextField) -> String {
        if label === historyTopLabel {
            return lastDisplayedHistoryText
        }
        if label === translationLabel {
            return lastDisplayedTranslationText
        }
        if label === originalLabel {
            return lastDisplayedOriginalText
        }
        return label.stringValue
    }

    private func attributedSubtitleLine(for label: NSTextField, text: String, committed: Bool, paragraph: NSParagraphStyle) -> NSAttributedString {
        let role = subtitleRole(for: label, text: text, committed: committed)
        let prefixFont = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .bold)
        let bodyFont = label.font ?? .systemFont(ofSize: 16)
        let full = NSMutableAttributedString(
            string: "\(role.prefix)\t",
            attributes: [
                .foregroundColor: role.prefixColor,
                .font: prefixFont,
                .kern: 0.45,
                .paragraphStyle: paragraph,
            ]
        )
        full.append(NSAttributedString(
            string: text,
            attributes: [
                .foregroundColor: role.bodyColor,
                .font: bodyFont,
                .kern: 0.05,
                .paragraphStyle: paragraph,
            ]
        ))
        return full
    }

    private func subtitleRole(for label: NSTextField, text: String, committed: Bool) -> (prefix: String, prefixColor: NSColor, bodyColor: NSColor) {
        if label === historyTopLabel {
            return ("快字 ASR", localFastTextColor, localFastTextColor)
        }
        if label === translationLabel {
            let color = text.contains("等待 SenseAudio") ? mutedInkColor : translationTextColor
            return ("翻译", translationTextColor, color)
        }
        if label === originalLabel {
            let statusLike = !committed && !hasSubtitleContentThisRun() && (
                text.contains("正在")
                    || text.contains("已接入")
                    || text.contains("已停止")
                    || text.contains("异常")
                    || text.contains("配额")
            )
            if statusLike {
                return ("状态", subtitleStatusColor, subtitleStatusColor)
            }
            let bodyColor = committed ? senseAudioTextColor : mutedInkColor
            return ("SenseAudio ASR", senseAudioTextColor, bodyColor)
        }
        return ("字幕", committed ? committedTextColor : mutedInkColor, committed ? committedTextColor : inkColor)
    }

    private func shouldAnimateLineChange(label: NSTextField, previousText: String, newText: String, committed: Bool) -> Bool {
        if suppressSubtitleAnimations {
            return false
        }
        if isStreamingAppend(from: previousText, to: newText) {
            return false
        }
        if label === originalLabel, !committed {
            return false
        }
        return true
    }

    private func isStreamingAppend(from previousText: String, to newText: String) -> Bool {
        let previous = previousText.replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let next = newText.replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        guard !previous.isEmpty, next.count > previous.count else { return false }
        return next.hasPrefix(previous)
    }

    private func showTranslationPlaceholder() {
        translationLabel.attributedStringValue = NSAttributedString(string: "")
        translationLabel.isHidden = false
        translationLabel.alphaValue = 0
        translationLabel.layer?.opacity = 0
        translationHeightConstraint?.constant = 18
    }

    private func clearLine(_ label: NSTextField) {
        label.attributedStringValue = NSAttributedString(string: "")
        label.isHidden = true
        if label === historyTopLabel {
            historyTopHeightConstraint?.constant = 0
            lastDisplayedHistoryText = ""
        } else if label === translationLabel {
            translationHeightConstraint?.constant = 0
            lastDisplayedTranslationText = ""
        } else if label === originalLabel {
            lastDisplayedOriginalText = ""
        }
    }

    private func tickSubtitleFade() {
        guard originalLabel.attributedStringValue.length > 0 else { return }
        guard let lastSubtitleEventAt else { return }

        let idle = Date().timeIntervalSince(lastSubtitleEventAt)
        if idle <= subtitleFadeDelay {
            setSubtitleOpacity(1.0)
            return
        }

        let progress = min(1.0, (idle - subtitleFadeDelay) / subtitleFadeDuration)
        let easedProgress = 1.0 - pow(1.0 - progress, 2.0)
        setSubtitleOpacity(max(0.0, 1.0 - easedProgress))

        if progress >= 1.0 {
            clearSubtitleDisplayState()
        }
    }

    private func setSubtitleOpacity(_ alpha: CGFloat) {
        originalLabel.alphaValue = alpha
        historyTopLabel.alphaValue = alpha
        translationLabel.alphaValue = alpha
        originalLabel.layer?.opacity = Float(alpha)
        historyTopLabel.layer?.opacity = Float(alpha)
        translationLabel.layer?.opacity = Float(alpha)
    }

    private func clearSubtitleDisplayState() {
        pendingLocalDrafts.removeAll()
        committedSegments.removeAll()
        committedLocalSegmentUpperBound = -1
        retainedLocalFastText = ""
        retainedLocalFastUpdatedAt = nil
        latestSenseAudioFinal = ""
        latestSenseAudioTranslation = ""
        lastSubtitleEventAt = nil
        clearLine(historyTopLabel)
        clearLine(translationLabel)
        clearLine(originalLabel)
        setSubtitleOpacity(1.0)
        if compactMusicPanelVisible {
            updateCompactMusicPanelHeader()
        }
    }

    @discardableResult
    private func commitSenseAudioFinal(_ finalText: String) -> Bool {
        guard !pendingLocalDrafts.isEmpty else { return false }
        let normalizedFinal = normalizeForMatch(finalText)
        guard !normalizedFinal.isEmpty else { return false }

        var bestScore = 0.0
        var bestLength = 0
        let maxWindow = min(5, pendingLocalDrafts.count)
        for length in 1...maxWindow {
            let combined = pendingLocalDrafts.prefix(length).map(\.text).joined()
            let score = similarity(normalizeForMatch(combined), normalizedFinal)
            if score > bestScore {
                bestScore = score
                bestLength = length
            }
        }

        if bestScore >= 0.42, bestLength > 0 {
            let removed = Array(pendingLocalDrafts.prefix(bestLength))
            if let lastCommitted = removed.last?.segmentID {
                committedLocalSegmentUpperBound = max(committedLocalSegmentUpperBound, lastCommitted)
            }
            pendingLocalDrafts.removeFirst(bestLength)
            return true
        }
        return false
    }

    private func appendCommittedSegment(text: String, translation: String, comparedTo baseline: String?) {
        _ = baseline
        committedSegments.append(CommittedSegment(text: text, translation: translation))
        if committedSegments.count > 6 {
            committedSegments.removeFirst(committedSegments.count - 6)
        }
        if compactMusicPanelVisible {
            updateCompactMusicPanelHeader()
        }
    }

    private func normalizeForMatch(_ text: String) -> String {
        let lowered = text.lowercased()
        return lowered.replacingOccurrences(
            of: #"[[:space:][:punct:]，。！？；：“”‘’、]+"#,
            with: "",
            options: .regularExpression
        )
    }

    private func similarity(_ lhs: String, _ rhs: String) -> Double {
        if lhs.isEmpty || rhs.isEmpty { return 0.0 }
        let distance = levenshtein(lhs, rhs)
        let maxLength = max(lhs.count, rhs.count)
        return max(0.0, 1.0 - (Double(distance) / Double(maxLength)))
    }

    private func levenshtein(_ lhs: String, _ rhs: String) -> Int {
        let a = Array(lhs)
        let b = Array(rhs)
        if a.isEmpty { return b.count }
        if b.isEmpty { return a.count }

        var previous = Array(0...b.count)
        for (i, ca) in a.enumerated() {
            var current = [i + 1] + Array(repeating: 0, count: b.count)
            for (j, cb) in b.enumerated() {
                let cost = ca == cb ? 0 : 1
                current[j + 1] = min(
                    previous[j + 1] + 1,
                    current[j] + 1,
                    previous[j] + cost
                )
            }
            previous = current
        }
        return previous[b.count]
    }

    private func styleButton(_ button: NSButton, background: NSColor, minWidth: CGFloat = 62) {
        button.wantsLayer = true
        button.isBordered = false
        button.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .semibold)
        button.contentTintColor = .white
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 30).isActive = true
        button.widthAnchor.constraint(greaterThanOrEqualToConstant: minWidth).isActive = true
        if let layer = button.layer {
            layer.cornerRadius = 8
            layer.backgroundColor = background.cgColor
            layer.borderWidth = background == paperColor ? 1 : 0
            layer.borderColor = background == paperColor ? borderColor.cgColor : NSColor.clear.cgColor
        }
    }

    private func applyCompactPreviewPanelStyle(isMusic: Bool) {
        compactPreviewPanel?.layer?.backgroundColor = (isMusic ? musicPanelColor : surfaceColor).cgColor
        compactPreviewPanel?.layer?.borderColor = (isMusic ? musicBorderColor : borderColor).cgColor
        compactPreviewPanel?.layer?.shadowColor = (isMusic
            ? NSColor(calibratedRed: 0.36, green: 0.22, blue: 0.10, alpha: 0.12)
            : NSColor(calibratedRed: 0.14, green: 0.18, blue: 0.28, alpha: 0.10)).cgColor
        compactPreviewTitleLabel?.textColor = isMusic ? musicInkColor : inkColor
        compactPreviewSubtitleLabel?.textColor = isMusic
            ? NSColor(calibratedRed: 0.44, green: 0.34, blue: 0.24, alpha: 0.76)
            : mutedInkColor
    }

    private func applyCompactActionButtonStyle(_ button: NSButton?, variant: CompactActionButtonVariant) {
        guard let button, let layer = button.layer else { return }
        button.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: .semibold)

        let textColor: NSColor
        let backgroundColor: NSColor
        let borderWidth: CGFloat
        let outlineColor: NSColor
        let cornerRadius: CGFloat
        let shadowColor: NSColor
        let shadowRadius: CGFloat
        let shadowOffset = NSSize(width: 0, height: -1)

        switch variant {
        case .primary:
            textColor = .white
            backgroundColor = musicInkColor
            borderWidth = 0
            outlineColor = .clear
            cornerRadius = 12
            shadowColor = musicAccentColor.withAlphaComponent(0.24)
            shadowRadius = 7
        case .neutral:
            textColor = musicInkColor
            backgroundColor = NSColor.white.withAlphaComponent(0.5)
            borderWidth = 1
            outlineColor = musicBorderColor.withAlphaComponent(0.58)
            cornerRadius = 11
            shadowColor = .clear
            shadowRadius = 0
        case .accentSoft:
            textColor = musicAccentColor
            backgroundColor = musicAccentSoftColor
            borderWidth = 1
            outlineColor = musicAccentColor.withAlphaComponent(0.24)
            cornerRadius = 12
            shadowColor = .clear
            shadowRadius = 0
        case .ghost:
            textColor = NSColor(calibratedRed: 0.27, green: 0.22, blue: 0.17, alpha: 0.88)
            backgroundColor = NSColor.white.withAlphaComponent(0.36)
            borderWidth = 1
            outlineColor = musicBorderColor.withAlphaComponent(0.42)
            cornerRadius = 11
            shadowColor = .clear
            shadowRadius = 0
        }

        button.contentTintColor = textColor
        button.alphaValue = button.isEnabled ? 1.0 : 0.46
        layer.cornerRadius = cornerRadius
        layer.backgroundColor = backgroundColor.cgColor
        layer.borderWidth = borderWidth
        layer.borderColor = outlineColor.cgColor
        layer.shadowColor = shadowColor.cgColor
        layer.shadowOpacity = shadowRadius > 0 ? 1.0 : 0.0
        layer.shadowRadius = shadowRadius
        layer.shadowOffset = shadowOffset
    }

    private func styleCompactPreviewRow(_ row: NSView, selected: Bool, mood: CompactPreviewPanelMood = .project) {
        let selectedAccent = mood == .music ? musicAccentColor : accentColor
        let selectedFill = mood == .music ? musicAccentSoftColor : accentSoftColor
        let normalFill = mood == .music
            ? NSColor(calibratedRed: 1.0, green: 0.975, blue: 0.93, alpha: 0.52)
            : NSColor.white.withAlphaComponent(0.38)
        row.layer?.backgroundColor = (selected
            ? selectedFill.withAlphaComponent(0.86)
            : normalFill).cgColor
        row.layer?.borderWidth = selected ? 1.25 : 1
        row.layer?.borderColor = (selected
            ? selectedAccent.withAlphaComponent(0.2)
            : (mood == .music ? musicBorderColor : borderColor).withAlphaComponent(0.42)).cgColor
        row.layer?.shadowColor = selected ? selectedAccent.withAlphaComponent(0.14).cgColor : NSColor.clear.cgColor
        row.layer?.shadowOpacity = selected ? 1.0 : 0.0
        row.layer?.shadowRadius = selected ? 5 : 0
        row.layer?.shadowOffset = NSSize(width: 0, height: -1)
    }

    private func makeCompactActionButton(title: String, action: Selector) -> NSButton {
        let button = NSButton(title: title, target: self, action: action)
        button.wantsLayer = true
        button.isBordered = false
        button.bezelStyle = .regularSquare
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 30).isActive = true
        button.widthAnchor.constraint(greaterThanOrEqualToConstant: 38).isActive = true
        button.font = NSFont(name: "SF Pro Text", size: 9) ?? .systemFont(ofSize: 9, weight: .semibold)
        button.contentTintColor = inkColor
        if let layer = button.layer {
            layer.cornerRadius = 9
            layer.backgroundColor = paperColor.cgColor
            layer.borderWidth = 1
            layer.borderColor = borderColor.cgColor
        }
        return button
    }

    private func makeCompactSatellite(symbol: String, tooltip: String, action: Selector) -> NSButton {
        let button = SatelliteOrbButton(title: "", target: self, action: action)
        button.isBordered = false
        button.bezelStyle = .regularSquare
        button.wantsLayer = true
        button.translatesAutoresizingMaskIntoConstraints = false
        button.alphaValue = 0.0
        button.layer?.cornerRadius = 18
        button.layer?.shadowColor = NSColor(calibratedRed: 0.15, green: 0.18, blue: 0.26, alpha: 0.10).cgColor
        button.layer?.shadowOpacity = 1
        button.layer?.shadowRadius = 8
        button.layer?.shadowOffset = NSSize(width: 0, height: -2)
        button.contentTintColor = inkColor
        button.toolTip = nil
        button.imagePosition = .imageOnly
        if #available(macOS 11.0, *) {
            button.image = NSImage(systemSymbolName: symbol, accessibilityDescription: tooltip)
            button.symbolImage = button.image
        }
        button.onHoverChanged = { [weak self, weak button] hovering in
            if hovering {
                self?.beginCompactHover()
            } else {
                self?.scheduleCompactHoverDismiss()
            }
            self?.setCompactSatelliteHint(hovering ? tooltip : nil, anchorView: hovering ? button : nil)
        }
        return button
    }

    private func setCompactSatelliteHint(_ text: String?, anchorView: NSView? = nil) {
        guard let label = compactSatelliteHintLabel,
              let container = compactSatelliteHintContainer,
              let compactRoot = compactRootView else { return }
        let value = text?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        guard !value.isEmpty else {
            NSAnimationContext.runAnimationGroup { context in
                context.duration = 0.16
                container.animator().alphaValue = 0.0
            } completionHandler: {
                container.isHidden = true
                label.isHidden = true
                label.stringValue = ""
            }
            return
        }
        label.stringValue = value
        let desiredWidth = min(156, max(64, ceil(label.intrinsicContentSize.width) + 16))
        compactSatelliteHintWidthConstraint?.constant = desiredWidth
        if let anchorView {
            let anchorPoint = anchorView.convert(
                NSPoint(x: anchorView.bounds.midX, y: anchorView.bounds.maxY),
                to: compactRoot
            )
            compactSatelliteHintCenterXConstraint?.constant = anchorPoint.x - compactRoot.bounds.midX
            compactRoot.layoutSubtreeIfNeeded()
        } else {
            compactSatelliteHintCenterXConstraint?.constant = 0
        }
        container.isHidden = false
        label.isHidden = false
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.16
            container.animator().alphaValue = 1.0
        }
    }

    @objc private func startFromCompactPanel() {
        controller.refreshRunningState()
        appendOverlayDebug("compact start tapped running=\(controller.isRunning)")
        guard !controller.isRunning else { return }
        beginListeningRun()
    }

    @objc private func toggleCompactProjectPanel() {
        compactMusicPanelVisible = false
        compactProjectPanelVisible.toggle()
        if compactProjectPanelVisible {
            if selectedCompactProjectIndex == nil, !compactPreviewProjects.isEmpty {
                selectedCompactProjectIndex = 0
            }
            statusLabel.stringValue = "最近项目已展开"
            compactHoverDismissDeadline = nil
            isCompactHoverVisible = true
            refreshCompactPreview()
            applyCompactProjectLayout(animated: true)
            setCompactHoverVisible(true, animated: true)
        } else {
            statusLabel.stringValue = "最近项目已收起"
            selectedCompactProjectIndex = nil
            refreshCompactPreview()
            syncCompactPanelWindow(animated: true)
            if isMouseInsideCompactRoot() {
                setCompactHoverVisible(true, animated: true)
            } else {
                setCompactHoverVisible(false, animated: true)
            }
        }
    }

    @objc private func toggleCompactMusicPanel() {
        compactProjectPanelVisible = false
        compactMusicPanelVisible.toggle()
        if compactMusicPanelVisible {
            if selectedCompactMusicIndex == nil, !compactMusicTracks.isEmpty {
                selectedCompactMusicIndex = 0
            }
            statusLabel.stringValue = "音乐面板已展开"
            compactHoverDismissDeadline = nil
            isCompactHoverVisible = true
            refreshCompactPreview()
            applyCompactProjectLayout(animated: true)
            setCompactHoverVisible(true, animated: true)
        } else {
            statusLabel.stringValue = "音乐面板已收起"
            refreshCompactPreview()
            syncCompactPanelWindow(animated: true)
            if isMouseInsideCompactRoot() {
                setCompactHoverVisible(true, animated: true)
            } else {
                setCompactHoverVisible(false, animated: true)
            }
        }
    }

    private func beginListeningRun() {
        appendOverlayDebug("beginListeningRun")
        setCompactHoverVisible(false, animated: false)
        setCompactMode(false, animated: true)
        latestSenseAudioFinal = ""
        pendingLocalDrafts.removeAll()
        committedSegments.removeAll()
        committedLocalSegmentUpperBound = -1
        retainedLocalFastText = ""
        retainedLocalFastUpdatedAt = nil
        lastSubtitleEventAt = nil
        setSubtitleOpacity(1.0)
        clearLine(historyTopLabel)
        clearLine(translationLabel)
        applyLineDisplay(to: originalLabel, text: "正在接入电脑音频...", committed: false)
        metaLabel.stringValue = runningModeSummary()
        statusLabel.stringValue = "正在启动实时 ASR"
        startNewRun()
    }

    @objc private func toggleRunner() {
        controller.refreshRunningState()
        appendOverlayDebug("toggleRunner running=\(controller.isRunning)")
        if controller.isRunning {
            statusLabel.stringValue = "正在停止识别"
            controller.stop()
        } else {
            beginListeningRun()
        }
    }

    @objc private func organizeTranscript() {
        guard !controller.isRunning else {
            statusLabel.stringValue = "请先停止识别，再整理本次 ASR"
            return
        }
        runTranscriptOrganization(at: transcriptJSONURL(), statusName: "本次 ASR", metaOverride: nil, mode: "summary")
    }

    @objc private func cycleTTSVoice() {
        selectedTTSVoiceIndex = (selectedTTSVoiceIndex + 1) % availableTTSVoices.count
        let voice = selectedTTSVoice()
        statusLabel.stringValue = "已切换朗读音色：\(voice.label)"
        refreshOrganizeButton()
    }

    @objc private func cycleLocalFastOption() {
        guard !availableLocalFastOptions.isEmpty else { return }
        selectedLocalFastOptionIndex = (selectedLocalFastOptionIndex + 1) % availableLocalFastOptions.count
        syncModeLabels()
        let label = selectedLocalFastOption().label
        if controller.isRunning {
            pendingRestart = true
            controller.stop()
            statusLabel.stringValue = "正在切换快速字幕：\(label)"
        } else {
            statusLabel.stringValue = "快速字幕已切换为：\(label)"
        }
    }

    @objc private func cycleTranslationTarget() {
        let wasEnabled = translationEnabled
        if !translationEnabled {
            translationEnabled = true
        } else {
            selectedTranslationTargetIndex = (selectedTranslationTargetIndex + 1) % availableTranslationTargets.count
        }
        syncModeLabels()
        let target = selectedTranslationTarget().label
        if controller.isRunning {
            pendingRestart = true
            controller.stop()
            statusLabel.stringValue = wasEnabled ? "正在切换翻译目标：\(target)" : "正在启用双语翻译：\(target)"
        } else {
            statusLabel.stringValue = wasEnabled ? "翻译目标已切换为：\(target)" : "双语翻译已开启：\(target)"
        }
    }

    @objc private func cycleMusicStylePreset() {
        selectedMusicStyleIndex = (selectedMusicStyleIndex + 1) % availableMusicStyles.count
        statusLabel.stringValue = "已切换配乐风格：\(selectedMusicStyle().label)"
        skipCompactPreviewRefreshInButtonSync = true
        refreshOrganizeButton()
        skipCompactPreviewRefreshInButtonSync = false
        if compactMusicPanelVisible {
            updateCompactMusicPanelHeader()
        }
    }

    @objc private func cycleMusicGenerationMode() {
        selectedMusicGenerationModeIndex = (selectedMusicGenerationModeIndex + 1) % availableMusicGenerationModes.count
        statusLabel.stringValue = "已切换生成模式：\(selectedMusicGenerationMode().label)"
        skipCompactPreviewRefreshInButtonSync = true
        refreshOrganizeButton()
        skipCompactPreviewRefreshInButtonSync = false
        if compactMusicPanelVisible {
            updateCompactMusicPanelHeader()
        }
    }

    @objc private func editMusicPrompt() {
        let alert = NSAlert()
        alert.messageText = "写一点音乐灵感"
        alert.informativeText = "一句话就够了，例如氛围、节奏、乐器或想要的情绪。"
        alert.addButton(withTitle: "保存灵感")
        alert.addButton(withTitle: "清空")
        alert.addButton(withTitle: "取消")

        let accessory = NSView(frame: NSRect(x: 0, y: 0, width: 318, height: 142))
        accessory.wantsLayer = true
        accessory.layer?.backgroundColor = NSColor.clear.cgColor

        let hint = NSTextField(labelWithString: "会和当前项目、剪贴板或本次 ASR 一起作为生成参考")
        hint.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .medium)
        hint.textColor = NSColor(calibratedRed: 0.46, green: 0.36, blue: 0.25, alpha: 0.78)
        hint.frame = NSRect(x: 4, y: 120, width: 310, height: 16)
        accessory.addSubview(hint)

        let textView = NSTextView(frame: NSRect(x: 0, y: 0, width: 302, height: 96))
        textView.isRichText = false
        textView.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        textView.textColor = musicInkColor
        textView.backgroundColor = musicPanelColor
        textView.textContainerInset = NSSize(width: 10, height: 8)
        textView.string = customMusicPrompt

        let scrollView = NSScrollView(frame: NSRect(x: 4, y: 10, width: 310, height: 104))
        scrollView.borderType = .noBorder
        scrollView.drawsBackground = false
        scrollView.hasVerticalScroller = true
        scrollView.autohidesScrollers = true
        scrollView.wantsLayer = true
        scrollView.layer?.cornerRadius = 13
        scrollView.layer?.masksToBounds = true
        scrollView.layer?.backgroundColor = musicPanelColor.cgColor
        scrollView.layer?.borderWidth = 1
        scrollView.layer?.borderColor = musicBorderColor.cgColor
        scrollView.documentView = textView
        accessory.addSubview(scrollView)
        alert.accessoryView = accessory

        let response = alert.runModal()
        switch response {
        case .alertFirstButtonReturn:
            customMusicPrompt = textView.string.trimmingCharacters(in: .whitespacesAndNewlines)
            statusLabel.stringValue = customMusicPrompt.isEmpty ? "灵感为空，将按上下文生成" : "音乐灵感已更新"
        case .alertSecondButtonReturn:
            customMusicPrompt = ""
            statusLabel.stringValue = "已清空音乐灵感"
        default:
            return
        }

        skipCompactPreviewRefreshInButtonSync = true
        refreshOrganizeButton()
        skipCompactPreviewRefreshInButtonSync = false
        if compactMusicPanelVisible {
            updateCompactMusicPanelHeader()
        }
    }

    @objc private func renameSelectedMusicTrack() {
        guard let selectedCompactMusicIndex, compactMusicTracks.indices.contains(selectedCompactMusicIndex) else {
            statusLabel.stringValue = "请先选一首歌曲"
            return
        }

        let track = compactMusicTracks[selectedCompactMusicIndex]
        let alert = NSAlert()
        alert.messageText = "给这首音乐起个名字"
        alert.informativeText = "只修改音乐工坊里的显示名称，不移动音频文件。"
        alert.addButton(withTitle: "保存")
        alert.addButton(withTitle: "取消")

        let textField = NSTextField(frame: NSRect(x: 0, y: 0, width: 300, height: 28))
        textField.stringValue = track.title
        textField.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        alert.accessoryView = textField

        guard alert.runModal() == .alertFirstButtonReturn else { return }
        let newTitle = textField.stringValue.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !newTitle.isEmpty else {
            statusLabel.stringValue = "音乐名称不能为空"
            return
        }

        do {
            let data = try Data(contentsOf: track.metadataURL)
            var payload = (try JSONSerialization.jsonObject(with: data) as? [String: Any]) ?? [:]
            payload["title"] = newTitle
            let output = try JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted, .sortedKeys])
            try output.write(to: track.metadataURL, options: .atomic)
            invalidateRecentMusicTracksCache()
            self.selectedCompactMusicIndex = selectedCompactMusicIndex
            statusLabel.stringValue = "已重命名为 \(newTitle)"
            refreshCompactPreview(forceReload: true)
        } catch {
            statusLabel.stringValue = "改名失败: \(error.localizedDescription)"
        }
    }

    private func shortProcessOutput(_ text: String, fallback: String) -> String {
        let compact = text
            .split(whereSeparator: \.isNewline)
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
            .joined(separator: " ")
        guard !compact.isEmpty else { return fallback }
        return compact.count > 86 ? String(compact.prefix(86)) + "..." : compact
    }

    @objc private func readClipboardCapture() {
        if let speechProcess, speechProcess.isRunning {
            speechProcess.terminate()
            self.speechProcess = nil
            speechPlayer?.stop()
            speechPlayer = nil
            speechPlayerData = nil
            statusLabel.stringValue = "已停止朗读"
            refreshOrganizeButton()
            return
        }
        if speechPlayer?.isPlaying == true {
            speechPlayer?.stop()
            speechPlayer = nil
            speechPlayerData = nil
            statusLabel.stringValue = "已停止朗读"
            refreshOrganizeButton()
            return
        }

        let copied = latestClipboardText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !copied.isEmpty else {
            statusLabel.stringValue = "还没有捕获到复制文本"
            return
        }

        let clipboardDir = workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("clipboard", isDirectory: true)
        try? FileManager.default.createDirectory(at: clipboardDir, withIntermediateDirectories: true)
        let timestamp = Int((latestClipboardCapturedAt ?? Date()).timeIntervalSince1970)
        let textFile = clipboardDir.appendingPathComponent("clipboard_\(timestamp)_speak.txt")
        try? copied.write(to: textFile, atomically: true, encoding: .utf8)

        let outputAudio = clipboardDir.appendingPathComponent("clipboard_\(timestamp)_\(selectedTTSVoice().id).mp3")
        let script = scriptDir.appendingPathComponent("senseaudio_tts_clipboard.py")
        let envFile = workspaceDir.appendingPathComponent(".env")
        let pythonURL = FileManager.default.isExecutableFile(atPath: scriptDir.appendingPathComponent(".venv/bin/python").path)
            ? scriptDir.appendingPathComponent(".venv/bin/python")
            : URL(fileURLWithPath: "/usr/bin/env")

        let process = Process()
        process.executableURL = pythonURL
        let voice = selectedTTSVoice()
        if pythonURL.lastPathComponent == "env" {
            process.arguments = ["python3", script.path, "--text-file", textFile.path, "--env-file", envFile.path, "--voice-id", voice.id, "--output-audio", outputAudio.path]
        } else {
            process.arguments = [script.path, "--text-file", textFile.path, "--env-file", envFile.path, "--voice-id", voice.id, "--output-audio", outputAudio.path]
        }
        process.currentDirectoryURL = repoDirURL()
        let outputCollector = ProcessOutputCollector()
        outputCollector.attach(to: process)
        process.terminationHandler = { [weak self] task in
            let processOutput = outputCollector.finishText()
            DispatchQueue.main.async {
                guard let self else { return }
                self.speechProcess = nil
                guard task.terminationStatus == 0 else {
                    self.statusLabel.stringValue = self.shortProcessOutput(processOutput, fallback: "朗读失败")
                    self.refreshOrganizeButton()
                    return
                }
                guard FileManager.default.fileExists(atPath: outputAudio.path) else {
                    self.statusLabel.stringValue = self.shortProcessOutput(processOutput, fallback: "朗读失败：没有生成音频")
                    self.refreshOrganizeButton()
                    return
                }
                do {
                    let audioData = try Data(contentsOf: outputAudio)
                    let player = try AVAudioPlayer(data: audioData)
                    player.delegate = self
                    player.prepareToPlay()
                    player.volume = 1.0
                    self.speechPlayerData = audioData
                    self.speechPlayer = player
                    self.ensureAudibleOutputVolumeForMusic()
                    if player.play() {
                        self.statusLabel.stringValue = "正在朗读：\(voice.label)"
                    } else {
                        self.statusLabel.stringValue = "朗读启动失败"
                    }
                } catch {
                    self.speechPlayer = nil
                    self.speechPlayerData = nil
                    self.statusLabel.stringValue = "朗读播放失败: \(error.localizedDescription)"
                }
                self.refreshOrganizeButton()
            }
        }

        do {
            try process.run()
            speechProcess = process
            statusLabel.stringValue = "正在用 SenseAudio 朗读：\(voice.label)"
            refreshOrganizeButton()
        } catch {
            speechProcess = nil
            refreshOrganizeButton()
            statusLabel.stringValue = "朗读启动失败: \(error.localizedDescription)"
        }
    }

    private func selectRecentProject(at index: Int) {
        guard compactPreviewProjects.indices.contains(index) else { return }
        selectedCompactProjectIndex = index
        refreshCompactPreview()
        let project = compactPreviewProjects[index]
        statusLabel.stringValue = project.hasOrganizedNotes
            ? "已选中项目，可直接查看整理稿"
            : "已选中项目，可按需整理"
    }

    @objc private func renameSelectedRecentProject() {
        guard let project = selectedCompactProject() else {
            statusLabel.stringValue = "请先点一个历史项目"
            return
        }

        let alert = NSAlert()
        alert.messageText = "给这个项目起个名字"
        alert.informativeText = "只修改最近项目里的显示名称，不会改动原始 ASR 或整理稿。"
        alert.addButton(withTitle: "保存")
        alert.addButton(withTitle: "取消")

        let textField = NSTextField(frame: NSRect(x: 0, y: 0, width: 300, height: 28))
        textField.stringValue = project.title
        textField.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        alert.accessoryView = textField

        guard alert.runModal() == .alertFirstButtonReturn else { return }
        let newTitle = textField.stringValue.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !newTitle.isEmpty else {
            statusLabel.stringValue = "项目名称不能为空"
            return
        }

        do {
            try saveProjectDisplayName(newTitle, for: project)
            let selectedRunID = project.runID
            let refreshed = loadRecentProjects(limit: max(compactPreviewLabels.count, 12))
            cachedRecentProjects = refreshed
            recentProjectsCacheLoadedAt = Date()
            if let newIndex = refreshed.firstIndex(where: { $0.runID == selectedRunID }) {
                selectedCompactProjectIndex = newIndex
            }
            refreshCompactPreview()
            statusLabel.stringValue = "已重命名为 \(newTitle)"
        } catch {
            statusLabel.stringValue = "项目改名失败: \(error.localizedDescription)"
        }
    }

    private func selectMusicTrack(at index: Int) {
        guard compactMusicTracks.indices.contains(index) else { return }
        selectedCompactMusicIndex = index
        refreshCompactPreview()
        statusLabel.stringValue = "已选中歌曲 \(compactMusicTracks[index].title)"
    }

    @objc private func generateMusicFromCurrentContext() {
        let promptExtra = customMusicPrompt.trimmingCharacters(in: .whitespacesAndNewlines)
        if let selectedCompactProjectIndex, compactPreviewProjects.indices.contains(selectedCompactProjectIndex) {
            let project = compactPreviewProjects[selectedCompactProjectIndex]
            let outputDir = project.runDirectory.appendingPathComponent("music_generation", isDirectory: true)
            runMusicGeneration(
                textFile: nil,
                transcriptURL: project.transcriptURL,
                outputDir: outputDir,
                statusName: "项目 \(project.runID)",
                metaOverride: "历史项目: \(project.runID)",
                titleOverride: "\(project.runID)·\(musicGenerationSummary())\(musicResultNoun())",
                promptExtra: promptExtra
            )
            return
        }
        if transcriptHasContent() {
            let outputDir = currentRunDirectory().appendingPathComponent("music_generation", isDirectory: true)
            runMusicGeneration(
                textFile: nil,
                transcriptURL: transcriptJSONURL(),
                outputDir: outputDir,
                statusName: "本次 ASR",
                metaOverride: "来源: 本次识别",
                titleOverride: "本次识别·\(musicGenerationSummary())\(musicResultNoun())",
                promptExtra: promptExtra
            )
            return
        }
        if !promptExtra.isEmpty {
            let promptDir = workspaceDir
                .appendingPathComponent("state", isDirectory: true)
                .appendingPathComponent("realtime_interpreter", isDirectory: true)
                .appendingPathComponent("music_prompts", isDirectory: true)
            try? FileManager.default.createDirectory(at: promptDir, withIntermediateDirectories: true)
            let timestamp = Int(Date().timeIntervalSince1970)
            let textFile = promptDir.appendingPathComponent("prompt_\(timestamp).txt")
            try? promptExtra.write(to: textFile, atomically: true, encoding: .utf8)
            let outputDir = promptDir.appendingPathComponent("prompt_\(timestamp)_music", isDirectory: true)
            runMusicGeneration(
                textFile: textFile,
                transcriptURL: nil,
                outputDir: outputDir,
                statusName: "自定义提示",
                metaOverride: "来源: 自定义提示词",
                titleOverride: "自定义提示·\(musicGenerationSummary())\(musicResultNoun())"
            )
            return
        }
        statusLabel.stringValue = "还没有可用于生成音乐的项目或文本"
    }

    @objc private func playPauseSelectedMusic() {
        guard let selectedCompactMusicIndex, compactMusicTracks.indices.contains(selectedCompactMusicIndex) else {
            statusLabel.stringValue = "请先选一首歌曲"
            return
        }
        let track = compactMusicTracks[selectedCompactMusicIndex]
        if activeMusicTrackID == track.id, let player = musicPlayer {
            if player.isPlaying {
                player.pause()
                statusLabel.stringValue = "已暂停 \(track.title)"
            } else {
                player.play()
                statusLabel.stringValue = "正在播放 \(track.title)"
            }
            refreshCompactPreview()
            return
        }

        musicPlayer?.stop()
        musicPlayer = nil
        musicPlayerData = nil
        activeMusicTrackID = track.id
        musicPlaybackLoadToken += 1
        let token = musicPlaybackLoadToken
        statusLabel.stringValue = "正在载入 \(track.title)"
        refreshCompactPreview()

        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            do {
                let data = try Data(contentsOf: track.audioURL)
                let player = try AVAudioPlayer(data: data)
                player.prepareToPlay()
                DispatchQueue.main.async {
                    guard let self, token == self.musicPlaybackLoadToken else { return }
                    player.delegate = self
                    player.volume = 1.0
                    self.musicPlayerData = data
                    self.musicPlayer = player
                    self.ensureAudibleOutputVolumeForMusic()
                    if player.play() {
                        self.statusLabel.stringValue = "正在播放 \(track.title)"
                    } else {
                        self.statusLabel.stringValue = "播放启动失败"
                    }
                    self.refreshCompactPreview()
                }
            } catch {
                DispatchQueue.main.async {
                    guard let self, token == self.musicPlaybackLoadToken else { return }
                    self.musicPlayer = nil
                    self.musicPlayerData = nil
                    self.activeMusicTrackID = nil
                    self.statusLabel.stringValue = "播放失败: \(error.localizedDescription)"
                    self.refreshCompactPreview()
                }
            }
        }
    }

    @objc private func stopMusicPlayback() {
        musicPlaybackLoadToken += 1
        musicPlayer?.stop()
        musicPlayer = nil
        musicPlayerData = nil
        activeMusicTrackID = nil
        statusLabel.stringValue = "已停止播放"
        refreshCompactPreview()
    }

    @objc private func openSelectedMusicFile() {
        guard let selectedCompactMusicIndex, compactMusicTracks.indices.contains(selectedCompactMusicIndex) else {
            statusLabel.stringValue = "请先选一首歌曲"
            return
        }
        let track = compactMusicTracks[selectedCompactMusicIndex]
        NSWorkspace.shared.open(track.audioURL)
        statusLabel.stringValue = "已打开 \(track.title)"
    }

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        if player === speechPlayer {
            speechPlayer = nil
            speechPlayerData = nil
            statusLabel.stringValue = flag ? "朗读完成" : "朗读已结束"
            refreshOrganizeButton()
            return
        }
        if player === musicPlayer {
            musicPlayer = nil
            activeMusicTrackID = nil
            statusLabel.stringValue = flag ? "播放完成" : "播放已结束"
            refreshCompactPreview()
        }
    }

    @objc private func organizeSelectedRecentProject() {
        guard let selectedCompactProjectIndex, compactPreviewProjects.indices.contains(selectedCompactProjectIndex) else {
            statusLabel.stringValue = "请先点一个历史项目"
            return
        }
        let project = compactPreviewProjects[selectedCompactProjectIndex]
        runTranscriptOrganization(
            at: project.transcriptURL,
            statusName: "项目 \(project.runID)",
            metaOverride: "历史项目: \(project.runID)",
            mode: "summary",
            projectRunID: project.runID
        )
    }

    private func legacyOrganizationTemplateURL() -> URL {
        workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("organize_template.txt")
    }

    private func organizationTemplateStoreURL() -> URL {
        workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("organization_templates.json")
    }

    private func activeOrganizationTemplateRuntimeURL() -> URL {
        workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("active_organization_template.txt")
    }

    private func defaultOrganizationTemplateStore() -> OrganizationTemplateStore {
        var customTemplates: [OrganizationTemplate] = []
        let legacy = (try? String(contentsOf: legacyOrganizationTemplateURL(), encoding: .utf8))?
            .trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        if !legacy.isEmpty {
            customTemplates.append(
                OrganizationTemplate(
                    id: "custom_legacy",
                    name: "旧模板",
                    summary: "从旧版自定义模板迁移",
                    prompt: legacy,
                    isBuiltin: false
                )
            )
        }
        return OrganizationTemplateStore(
            selectedTemplateID: customTemplates.first?.id ?? defaultOrganizationTemplateID,
            customTemplates: customTemplates
        )
    }

    private func loadOrganizationTemplateStore() -> OrganizationTemplateStore {
        if let organizationTemplateStoreCache {
            return organizationTemplateStoreCache
        }
        let url = organizationTemplateStoreURL()
        let store: OrganizationTemplateStore
        if let data = try? Data(contentsOf: url),
           let decoded = try? JSONDecoder().decode(OrganizationTemplateStore.self, from: data) {
            store = decoded
        } else {
            store = defaultOrganizationTemplateStore()
        }
        let normalized = normalizedOrganizationTemplateStore(store)
        organizationTemplateStoreCache = normalized
        if normalized.selectedTemplateID != store.selectedTemplateID || normalized.customTemplates.count != store.customTemplates.count {
            saveOrganizationTemplateStore(normalized)
        }
        return normalized
    }

    private func normalizedOrganizationTemplateStore(_ store: OrganizationTemplateStore) -> OrganizationTemplateStore {
        let builtinIDs = Set(builtinOrganizationTemplates.map(\.id))
        var seen = Set<String>()
        let customTemplates = store.customTemplates.compactMap { template -> OrganizationTemplate? in
            let name = template.name.trimmingCharacters(in: .whitespacesAndNewlines)
            let prompt = template.prompt.trimmingCharacters(in: .whitespacesAndNewlines)
            let id = template.id.trimmingCharacters(in: .whitespacesAndNewlines)
            guard !id.isEmpty, !name.isEmpty, !prompt.isEmpty, !builtinIDs.contains(id), !seen.contains(id) else {
                return nil
            }
            seen.insert(id)
            return OrganizationTemplate(
                id: id,
                name: name,
                summary: template.summary.trimmingCharacters(in: .whitespacesAndNewlines),
                prompt: prompt,
                isBuiltin: false
            )
        }
        let allIDs = Set(builtinOrganizationTemplates.map(\.id) + customTemplates.map(\.id))
        let selectedID = allIDs.contains(store.selectedTemplateID) ? store.selectedTemplateID : defaultOrganizationTemplateID
        return OrganizationTemplateStore(selectedTemplateID: selectedID, customTemplates: customTemplates)
    }

    private func saveOrganizationTemplateStore(_ store: OrganizationTemplateStore) {
        let normalized = normalizedOrganizationTemplateStore(store)
        organizationTemplateStoreCache = normalized
        let url = organizationTemplateStoreURL()
        try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        if let data = try? JSONEncoder().encode(normalized) {
            try? data.write(to: url, options: .atomic)
        }
    }

    private func organizationTemplates() -> [OrganizationTemplate] {
        builtinOrganizationTemplates + loadOrganizationTemplateStore().customTemplates
    }

    private func selectedOrganizationTemplate() -> OrganizationTemplate {
        let store = loadOrganizationTemplateStore()
        return organizationTemplates().first(where: { $0.id == store.selectedTemplateID })
            ?? builtinOrganizationTemplates.first!
    }

    private func selectedOrganizationTemplateID() -> String {
        selectedOrganizationTemplate().id
    }

    private func setSelectedOrganizationTemplateID(_ id: String) {
        var store = loadOrganizationTemplateStore()
        guard organizationTemplates().contains(where: { $0.id == id }) else { return }
        store.selectedTemplateID = id
        saveOrganizationTemplateStore(store)
    }

    private func upsertCustomOrganizationTemplate(_ template: OrganizationTemplate, select: Bool) {
        var store = loadOrganizationTemplateStore()
        let custom = OrganizationTemplate(
            id: template.id,
            name: template.name.trimmingCharacters(in: .whitespacesAndNewlines),
            summary: template.summary.trimmingCharacters(in: .whitespacesAndNewlines),
            prompt: template.prompt.trimmingCharacters(in: .whitespacesAndNewlines),
            isBuiltin: false
        )
        if let index = store.customTemplates.firstIndex(where: { $0.id == custom.id }) {
            store.customTemplates[index] = custom
        } else {
            store.customTemplates.insert(custom, at: 0)
        }
        if select {
            store.selectedTemplateID = custom.id
        }
        saveOrganizationTemplateStore(store)
    }

    private func deleteCustomOrganizationTemplate(id: String) -> Bool {
        var store = loadOrganizationTemplateStore()
        guard let index = store.customTemplates.firstIndex(where: { $0.id == id }) else {
            return false
        }
        store.customTemplates.remove(at: index)
        if store.selectedTemplateID == id {
            store.selectedTemplateID = defaultOrganizationTemplateID
        }
        saveOrganizationTemplateStore(store)
        return true
    }

    private func activeOrganizationTemplateURL() -> URL? {
        let prompt = selectedOrganizationTemplate().prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !prompt.isEmpty else { return nil }
        let url = activeOrganizationTemplateRuntimeURL()
        try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        do {
            try prompt.write(to: url, atomically: true, encoding: .utf8)
            return url
        } catch {
            statusLabel.stringValue = "模板写入失败: \(error.localizedDescription)"
            return nil
        }
    }

    private func organizationOutputFilename(for templateID: String) -> String {
        if templateID == defaultOrganizationTemplateID {
            return "organized_notes.md"
        }
        let safeCharacters = templateID.map { character -> Character in
            character.isLetter || character.isNumber || character == "_" || character == "-" ? character : "_"
        }
        let stem = String(safeCharacters).trimmingCharacters(in: CharacterSet(charactersIn: "_-"))
        return "organized_\(stem.isEmpty ? "custom" : stem)_notes.md"
    }

    @objc private func editOrganizationTemplate() {
        showOrganizationTemplatePanel()
    }

    private func showOrganizationTemplatePanel() {
        let templates = organizationTemplates()
        guard !templates.isEmpty else { return }

        templatePanelWindow?.orderOut(nil)
        templatePanelRows.removeAll()
        templatePanelSelectedID = selectedOrganizationTemplateID()

        let size = NSSize(width: 540, height: 368)
        let root = NSVisualEffectView(frame: NSRect(origin: .zero, size: size))
        root.material = .popover
        root.blendingMode = .withinWindow
        root.state = .active
        root.wantsLayer = true
        root.layer?.cornerRadius = 28
        root.layer?.masksToBounds = true
        root.layer?.backgroundColor = NSColor(calibratedRed: 0.985, green: 0.982, blue: 0.965, alpha: 0.96).cgColor
        root.layer?.borderWidth = 1
        root.layer?.borderColor = NSColor.white.withAlphaComponent(0.72).cgColor

        let accentWash = NSView(frame: NSRect(x: 0, y: 262, width: size.width, height: 106))
        accentWash.wantsLayer = true
        accentWash.layer?.backgroundColor = accentSoftColor.withAlphaComponent(0.72).cgColor
        root.addSubview(accentWash)

        let title = NSTextField(labelWithString: "整理方式")
        title.frame = NSRect(x: 24, y: 318, width: 220, height: 28)
        title.font = NSFont(name: "SF Pro Display", size: 24) ?? .systemFont(ofSize: 24, weight: .bold)
        title.textColor = inkColor
        root.addSubview(title)

        let subtitle = NSTextField(labelWithString: "选择 AudioClaw 如何处理最近项目，不同模板会保留各自整理稿。")
        subtitle.frame = NSRect(x: 25, y: 294, width: 386, height: 18)
        subtitle.font = NSFont(name: "SF Pro Text", size: 12) ?? .systemFont(ofSize: 12)
        subtitle.textColor = mutedInkColor
        root.addSubview(subtitle)

        let closeButton = makeTemplatePanelButton(title: "关闭", action: #selector(closeOrganizationTemplatePanel), variant: .ghost)
        closeButton.frame = NSRect(x: 452, y: 314, width: 64, height: 30)
        root.addSubview(closeButton)

        let listPanel = NSView(frame: NSRect(x: 20, y: 76, width: 194, height: 202))
        listPanel.wantsLayer = true
        listPanel.layer?.cornerRadius = 20
        listPanel.layer?.backgroundColor = NSColor.white.withAlphaComponent(0.54).cgColor
        listPanel.layer?.borderWidth = 1
        listPanel.layer?.borderColor = borderColor.withAlphaComponent(0.54).cgColor
        root.addSubview(listPanel)

        let scrollView = NSScrollView(frame: NSRect(x: 10, y: 10, width: 174, height: 182))
        scrollView.drawsBackground = false
        scrollView.borderType = .noBorder
        scrollView.hasVerticalScroller = templates.count > 3
        scrollView.autohidesScrollers = true
        listPanel.addSubview(scrollView)

        let rowHeight: CGFloat = 56
        let documentHeight = max(CGFloat(templates.count) * (rowHeight + 8), 182)
        let documentView = NSView(frame: NSRect(x: 0, y: 0, width: 174, height: documentHeight))
        scrollView.documentView = documentView

        for (index, template) in templates.enumerated() {
            let y = documentHeight - CGFloat(index + 1) * (rowHeight + 8) + 8
            let row = ClickableRowView(frame: NSRect(x: 0, y: y, width: 174, height: rowHeight))
            row.wantsLayer = true
            row.layer?.cornerRadius = 15
            row.layer?.masksToBounds = true
            row.onClick = { [weak self] in
                self?.selectOrganizationTemplateInPanel(template.id)
            }

            let name = NSTextField(labelWithString: template.name)
            name.frame = NSRect(x: 13, y: 29, width: 120, height: 17)
            name.font = NSFont(name: "SF Pro Text", size: 12) ?? .systemFont(ofSize: 12, weight: .semibold)
            row.addSubview(name)

            let meta = NSTextField(labelWithString: template.isBuiltin ? "预设" : "自定义")
            meta.frame = NSRect(x: 13, y: 10, width: 130, height: 14)
            meta.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10)
            row.addSubview(meta)

            let dot = NSView(frame: NSRect(x: 149, y: 24, width: 8, height: 8))
            dot.wantsLayer = true
            dot.layer?.cornerRadius = 4
            dot.layer?.backgroundColor = (template.isBuiltin ? accentColor : musicAccentColor).withAlphaComponent(0.75).cgColor
            row.addSubview(dot)

            documentView.addSubview(row)
            templatePanelRows.append((template.id, row, name, meta))
        }
        scrollView.contentView.scroll(to: NSPoint(x: 0, y: max(0, documentHeight - scrollView.contentView.bounds.height)))
        scrollView.reflectScrolledClipView(scrollView.contentView)

        let previewPanel = NSView(frame: NSRect(x: 226, y: 76, width: 294, height: 202))
        previewPanel.wantsLayer = true
        previewPanel.layer?.cornerRadius = 24
        previewPanel.layer?.backgroundColor = surfaceColor.withAlphaComponent(0.94).cgColor
        previewPanel.layer?.borderWidth = 1
        previewPanel.layer?.borderColor = borderColor.withAlphaComponent(0.58).cgColor
        previewPanel.layer?.shadowColor = NSColor(calibratedRed: 0.22, green: 0.20, blue: 0.15, alpha: 0.10).cgColor
        previewPanel.layer?.shadowOpacity = 1
        previewPanel.layer?.shadowRadius = 18
        previewPanel.layer?.shadowOffset = NSSize(width: 0, height: -8)
        root.addSubview(previewPanel)

        let currentLabel = NSTextField(labelWithString: "")
        currentLabel.frame = NSRect(x: 20, y: 157, width: 184, height: 25)
        currentLabel.font = NSFont(name: "SF Pro Display", size: 20) ?? .systemFont(ofSize: 20, weight: .bold)
        currentLabel.textColor = inkColor
        previewPanel.addSubview(currentLabel)
        templatePanelCurrentLabel = currentLabel

        let kindLabel = NSTextField(labelWithString: "")
        kindLabel.frame = NSRect(x: 214, y: 160, width: 56, height: 21)
        kindLabel.alignment = .center
        kindLabel.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10, weight: .bold)
        kindLabel.textColor = accentColor
        kindLabel.wantsLayer = true
        kindLabel.layer?.cornerRadius = 10.5
        kindLabel.layer?.backgroundColor = accentSoftColor.withAlphaComponent(0.92).cgColor
        previewPanel.addSubview(kindLabel)
        templatePanelKindLabel = kindLabel

        let summaryLabel = NSTextField(wrappingLabelWithString: "")
        summaryLabel.frame = NSRect(x: 20, y: 119, width: 254, height: 34)
        summaryLabel.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        summaryLabel.textColor = inkColor
        summaryLabel.maximumNumberOfLines = 2
        previewPanel.addSubview(summaryLabel)
        templatePanelSummaryLabel = summaryLabel

        let divider = NSView(frame: NSRect(x: 20, y: 106, width: 254, height: 1))
        divider.wantsLayer = true
        divider.layer?.backgroundColor = borderColor.withAlphaComponent(0.52).cgColor
        previewPanel.addSubview(divider)

        let promptLabel = NSTextField(wrappingLabelWithString: "")
        promptLabel.frame = NSRect(x: 20, y: 54, width: 254, height: 42)
        promptLabel.font = NSFont(name: "SF Pro Text", size: 11) ?? .systemFont(ofSize: 11)
        promptLabel.textColor = mutedInkColor
        promptLabel.maximumNumberOfLines = 3
        previewPanel.addSubview(promptLabel)
        templatePanelPromptLabel = promptLabel

        let outputLabel = NSTextField(wrappingLabelWithString: "")
        outputLabel.frame = NSRect(x: 20, y: 18, width: 254, height: 26)
        outputLabel.font = NSFont(name: "SF Pro Text", size: 10) ?? .systemFont(ofSize: 10)
        outputLabel.textColor = accentColor
        outputLabel.maximumNumberOfLines = 2
        previewPanel.addSubview(outputLabel)
        templatePanelOutputLabel = outputLabel

        let useButton = makeTemplatePanelButton(title: "设为当前", action: #selector(useSelectedOrganizationTemplateFromPanel), variant: .primary)
        useButton.frame = NSRect(x: 24, y: 24, width: 112, height: 34)
        root.addSubview(useButton)
        templatePanelUseButton = useButton

        let editButton = makeTemplatePanelButton(title: "编辑副本", action: #selector(editSelectedOrganizationTemplateFromPanel), variant: .neutral)
        editButton.frame = NSRect(x: 146, y: 24, width: 92, height: 34)
        root.addSubview(editButton)
        templatePanelEditButton = editButton

        let importButton = makeTemplatePanelButton(title: "导入", action: #selector(importOrganizationTemplateFromPanel), variant: .neutral)
        importButton.frame = NSRect(x: 248, y: 24, width: 76, height: 34)
        root.addSubview(importButton)
        templatePanelImportButton = importButton

        let deleteButton = makeTemplatePanelButton(title: "删除", action: #selector(deleteSelectedOrganizationTemplateFromPanel), variant: .ghost)
        deleteButton.frame = NSRect(x: 426, y: 24, width: 82, height: 34)
        root.addSubview(deleteButton)
        templatePanelDeleteButton = deleteButton

        let window = OverlayPanelWindow(
            contentRect: NSRect(origin: .zero, size: size),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        window.level = .floating
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = true
        window.isMovableByWindowBackground = true
        window.collectionBehavior = [.moveToActiveSpace]
        window.contentView = root
        templatePanelWindow = window

        if let anchorWindow = view.window {
            let anchor = anchorWindow.frame
            let visible = anchorWindow.screen?.visibleFrame ?? NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
            let x = min(max(anchor.midX - size.width / 2, visible.minX + 12), visible.maxX - size.width - 12)
            let y = min(max(anchor.midY - size.height / 2, visible.minY + 12), visible.maxY - size.height - 12)
            window.setFrameOrigin(NSPoint(x: x, y: y))
        } else {
            window.center()
        }

        selectOrganizationTemplateInPanel(templatePanelSelectedID)
        window.alphaValue = 0
        window.orderFrontRegardless()
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.18
            context.timingFunction = CAMediaTimingFunction(name: .easeOut)
            window.animator().alphaValue = 1
        }
    }

    private func makeTemplatePanelButton(title: String, action: Selector, variant: CompactActionButtonVariant) -> NSButton {
        let button = NSButton(title: title, target: self, action: action)
        button.isBordered = false
        button.bezelStyle = .regularSquare
        button.wantsLayer = true
        button.font = NSFont(name: "SF Pro Text", size: 11) ?? .systemFont(ofSize: 11, weight: .semibold)
        button.contentTintColor = variant == .primary ? .white : inkColor
        let background: NSColor
        let border: NSColor
        switch variant {
        case .primary:
            background = accentColor
            border = accentColor
        case .neutral:
            background = NSColor.white.withAlphaComponent(0.64)
            border = borderColor.withAlphaComponent(0.70)
        case .accentSoft:
            background = accentSoftColor
            border = accentColor.withAlphaComponent(0.24)
        case .ghost:
            background = NSColor.white.withAlphaComponent(0.30)
            border = borderColor.withAlphaComponent(0.42)
        }
        button.layer?.cornerRadius = 13
        button.layer?.backgroundColor = background.cgColor
        button.layer?.borderWidth = 1
        button.layer?.borderColor = border.cgColor
        return button
    }

    private func selectOrganizationTemplateInPanel(_ id: String) {
        let templates = organizationTemplates()
        guard let template = templates.first(where: { $0.id == id }) ?? templates.first else { return }
        templatePanelSelectedID = template.id
        for item in templatePanelRows {
            let selected = item.id == template.id
            item.row.layer?.backgroundColor = selected
                ? accentColor.withAlphaComponent(0.13).cgColor
                : NSColor.white.withAlphaComponent(0.30).cgColor
            item.row.layer?.borderWidth = selected ? 1 : 0
            item.row.layer?.borderColor = accentColor.withAlphaComponent(0.22).cgColor
            item.name.textColor = selected ? inkColor : mutedInkColor
            item.meta.textColor = selected ? accentColor : mutedInkColor
            item.row.alphaValue = selected ? 1.0 : 0.78
        }
        templatePanelCurrentLabel?.stringValue = template.name
        templatePanelKindLabel?.stringValue = template.isBuiltin ? "预设" : "自定义"
        templatePanelSummaryLabel?.stringValue = template.summary.isEmpty ? "按当前模板整理原始 ASR，并输出 Markdown 正文。" : template.summary
        let promptPreview = template.prompt
            .replacingOccurrences(of: "\n", with: " ")
            .replacingOccurrences(of: #"\s+"#, with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        templatePanelPromptLabel?.stringValue = promptPreview.isEmpty ? "暂无模板内容" : promptPreview
        let placeholderHint = template.prompt.contains("{asr}") || template.prompt.contains("{{asr}}")
            ? "已包含 ASR 占位符"
            : "会自动追加原始 ASR"
        templatePanelOutputLabel?.stringValue = "\(placeholderHint) · 结果保存在最近项目"
        templatePanelDeleteButton?.alphaValue = template.isBuiltin ? 0.36 : 1.0
    }

    @objc private func closeOrganizationTemplatePanel() {
        guard let window = templatePanelWindow else { return }
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.14
            window.animator().alphaValue = 0
        } completionHandler: { [weak self] in
            window.orderOut(nil)
            self?.templatePanelWindow = nil
            self?.templatePanelRows.removeAll()
        }
    }

    @objc private func useSelectedOrganizationTemplateFromPanel() {
        setSelectedOrganizationTemplateID(templatePanelSelectedID)
        statusLabel.stringValue = "已选择整理模板：\(selectedOrganizationTemplate().name)"
        refreshCompactPreview()
        closeOrganizationTemplatePanel()
    }

    @objc private func editSelectedOrganizationTemplateFromPanel() {
        let selectedID = templatePanelSelectedID
        let selected = organizationTemplates().first(where: { $0.id == selectedID }) ?? selectedOrganizationTemplate()
        closeOrganizationTemplatePanel()
        editOrganizationTemplateDetail(selected)
    }

    @objc private func importOrganizationTemplateFromPanel() {
        closeOrganizationTemplatePanel()
        importOrganizationTemplate()
    }

    @objc private func deleteSelectedOrganizationTemplateFromPanel() {
        let selectedID = templatePanelSelectedID
        if deleteCustomOrganizationTemplate(id: selectedID) {
            statusLabel.stringValue = "已删除自定义模板"
            refreshCompactPreview()
            closeOrganizationTemplatePanel()
        } else {
            statusLabel.stringValue = "预设模板不能删除"
            selectOrganizationTemplateInPanel(selectedID)
        }
    }

    private func editOrganizationTemplateDetail(_ source: OrganizationTemplate) {
        let alert = NSAlert()
        alert.messageText = source.isBuiltin ? "基于预设新建模板" : "编辑整理模板"
        alert.informativeText = "写你希望 AudioClaw 如何整理 ASR。可用 {asr} 作为原文占位符。"
        alert.addButton(withTitle: "保存并使用")
        alert.addButton(withTitle: "取消")

        let accessory = NSView(frame: NSRect(x: 0, y: 0, width: 390, height: 230))
        let nameField = NSTextField(frame: NSRect(x: 0, y: 196, width: 390, height: 26))
        nameField.stringValue = source.isBuiltin ? "\(source.name)副本" : source.name
        nameField.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        nameField.placeholderString = "模板名称"
        accessory.addSubview(nameField)

        let textView = NSTextView(frame: NSRect(x: 0, y: 0, width: 374, height: 176))
        textView.isRichText = false
        textView.font = NSFont(name: "SF Pro Text", size: 13) ?? .systemFont(ofSize: 13)
        textView.textColor = inkColor
        textView.backgroundColor = surfaceColor
        textView.textContainerInset = NSSize(width: 10, height: 8)
        textView.string = source.prompt

        let scrollView = NSScrollView(frame: NSRect(x: 0, y: 8, width: 390, height: 178))
        scrollView.borderType = .noBorder
        scrollView.drawsBackground = false
        scrollView.hasVerticalScroller = true
        scrollView.autohidesScrollers = true
        scrollView.wantsLayer = true
        scrollView.layer?.cornerRadius = 13
        scrollView.layer?.masksToBounds = true
        scrollView.layer?.backgroundColor = surfaceColor.cgColor
        scrollView.layer?.borderWidth = 1
        scrollView.layer?.borderColor = borderColor.cgColor
        scrollView.documentView = textView
        accessory.addSubview(scrollView)
        alert.accessoryView = accessory

        let response = alert.runModal()
        guard response == .alertFirstButtonReturn else {
            return
        }
        let name = nameField.stringValue.trimmingCharacters(in: .whitespacesAndNewlines)
        let prompt = textView.string.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !name.isEmpty, !prompt.isEmpty else {
            statusLabel.stringValue = "模板名称和内容不能为空"
            return
        }
        let id = source.isBuiltin ? "custom_\(Int(Date().timeIntervalSince1970))" : source.id
        let template = OrganizationTemplate(
            id: id,
            name: name,
            summary: source.isBuiltin ? "由\(source.name)调整" : source.summary,
            prompt: prompt,
            isBuiltin: false
        )
        upsertCustomOrganizationTemplate(template, select: true)
        statusLabel.stringValue = "已保存并选择模板：\(name)"
        refreshCompactPreview()
    }

    private func importOrganizationTemplate() {
        let panel = NSOpenPanel()
        panel.title = "导入整理模板"
        panel.prompt = "导入"
        panel.canChooseDirectories = false
        panel.canChooseFiles = true
        panel.allowsMultipleSelection = false
        panel.allowedContentTypes = [
            .plainText,
            UTType(filenameExtension: "md"),
            UTType(filenameExtension: "markdown"),
        ].compactMap { $0 }
        let response = panel.runModal()
        guard response == .OK, let url = panel.url else {
            return
        }
        do {
            let prompt = try String(contentsOf: url, encoding: .utf8)
                .trimmingCharacters(in: .whitespacesAndNewlines)
            guard !prompt.isEmpty else {
                statusLabel.stringValue = "导入失败：模板文件为空"
                return
            }
            let baseName = url.deletingPathExtension().lastPathComponent
                .trimmingCharacters(in: .whitespacesAndNewlines)
            let template = OrganizationTemplate(
                id: "custom_import_\(Int(Date().timeIntervalSince1970))",
                name: baseName.isEmpty ? "导入模板" : baseName,
                summary: "从文件导入",
                prompt: prompt,
                isBuiltin: false
            )
            upsertCustomOrganizationTemplate(template, select: true)
            statusLabel.stringValue = "已导入并选择模板：\(template.name)"
            refreshCompactPreview()
        } catch {
            statusLabel.stringValue = "导入模板失败: \(error.localizedDescription)"
        }
    }

    @objc private func extractKeywordsForSelectedProject() {
        guard let project = selectedCompactProject() else {
            statusLabel.stringValue = "请先点一个历史项目"
            return
        }
        runTranscriptOrganization(
            at: project.transcriptURL,
            statusName: "项目 \(project.runID) 关键词提取",
            metaOverride: "历史项目: \(project.runID)",
            mode: "keywords",
            projectRunID: project.runID
        )
    }

    @objc private func openSelectedProjectTranscript() {
        guard let project = selectedCompactProject() else {
            statusLabel.stringValue = "请先点一个历史项目"
            return
        }
        NSWorkspace.shared.open(project.transcriptURL)
        statusLabel.stringValue = "已打开项目原文"
    }

    @objc private func openSelectedProjectNotes() {
        guard let notesURL = selectedProjectNotesURL() else {
            statusLabel.stringValue = "这个项目还没有整理稿"
            return
        }
        NSWorkspace.shared.open(notesURL)
        statusLabel.stringValue = "已打开整理稿"
    }

    @objc private func archiveSelectedProject() {
        guard let project = selectedCompactProject() else {
            statusLabel.stringValue = "请先点一个历史项目"
            return
        }
        let archiveDir = workspaceDir
            .appendingPathComponent("state", isDirectory: true)
            .appendingPathComponent("realtime_interpreter", isDirectory: true)
            .appendingPathComponent("runs_archived", isDirectory: true)
        try? FileManager.default.createDirectory(at: archiveDir, withIntermediateDirectories: true)
        let destination = archiveDir.appendingPathComponent(project.runID, isDirectory: true)
        do {
            if FileManager.default.fileExists(atPath: destination.path) {
                try FileManager.default.removeItem(at: destination)
            }
            try FileManager.default.moveItem(at: project.runDirectory, to: destination)
            invalidateRecentProjectsCache()
            selectedCompactProjectIndex = nil
            refreshCompactPreview(forceReload: true)
            statusLabel.stringValue = "已归档项目 \(project.runID)"
        } catch {
            statusLabel.stringValue = "归档失败: \(error.localizedDescription)"
        }
    }

    private func runTranscriptOrganization(
        at transcriptURL: URL,
        statusName: String,
        metaOverride: String?,
        mode: String,
        projectRunID: String? = nil
    ) {
        guard organizeProcess == nil else {
            statusLabel.stringValue = "正在整理，请稍候"
            return
        }
        guard FileManager.default.fileExists(atPath: transcriptURL.path) else {
            statusLabel.stringValue = "\(statusName) 还没有可整理的 SenseAudio 终稿"
            refreshOrganizeButton()
            return
        }

        let organizer = scriptDir.appendingPathComponent("organize_senseaudio_transcript.py")
        let pythonURL = FileManager.default.isExecutableFile(atPath: scriptDir.appendingPathComponent(".venv/bin/python").path)
            ? scriptDir.appendingPathComponent(".venv/bin/python")
            : URL(fileURLWithPath: "/usr/bin/env")

        let process = Process()
        process.executableURL = pythonURL
        let selectedTemplate = selectedOrganizationTemplate()
        let templateURL = activeOrganizationTemplateURL()
        var organizerArgs = [organizer.path, "--transcript-json", transcriptURL.path, "--mode", mode]
        if let templateURL {
            organizerArgs += ["--template-file", templateURL.path]
        }
        if mode == "summary" {
            let outputURL = transcriptURL
                .deletingLastPathComponent()
                .appendingPathComponent(organizationOutputFilename(for: selectedTemplate.id))
            organizerArgs += ["--output-markdown", outputURL.path]
        }
        if pythonURL.lastPathComponent == "env" {
            process.arguments = ["python3"] + organizerArgs
        } else {
            process.arguments = organizerArgs
        }
        process.currentDirectoryURL = repoDirURL()
        let outputCollector = ProcessOutputCollector()
        outputCollector.attach(to: process)

        organizeProcess = process
        organizingProjectRunID = projectRunID
        refreshOrganizeButton()
        refreshCompactPreview()
        statusLabel.stringValue = templateURL == nil
            ? "正在调用 audioclaw 处理 \(statusName)"
            : "正在按\(selectedTemplate.name)整理 \(statusName)"

        process.terminationHandler = { [weak self] task in
            let text = outputCollector.finishText()
            DispatchQueue.main.async {
                self?.organizeProcess = nil
                if self?.organizingProjectRunID == projectRunID {
                    self?.organizingProjectRunID = nil
                }
                self?.refreshOrganizeButton()
                guard task.terminationStatus == 0 else {
                    self?.statusLabel.stringValue = text.isEmpty ? "整理失败" : text
                    self?.refreshCompactPreview()
                    return
                }
                self?.invalidateRecentProjectsCache()
                self?.refreshCompactPreview(forceReload: true)
                self?.statusLabel.stringValue = "\(statusName) 整理完成"
                if let path = self?.extractOutputMarkdownPath(from: text) {
                    NSWorkspace.shared.open(path)
                    let metaPrefix = metaOverride ?? "模式: \(self?.translationEnabled == true ? "双语" : "原文")"
                    self?.metaLabel.stringValue = "\(metaPrefix) | 整理稿: \(path.lastPathComponent)"
                }
            }
        }

        do {
            try process.run()
        } catch {
            organizeProcess = nil
            if organizingProjectRunID == projectRunID {
                organizingProjectRunID = nil
            }
            refreshOrganizeButton()
            refreshCompactPreview()
            statusLabel.stringValue = "整理启动失败: \(error.localizedDescription)"
        }
    }

    private func runMusicGeneration(
        textFile: URL?,
        transcriptURL: URL?,
        outputDir: URL,
        statusName: String,
        metaOverride: String?,
        titleOverride: String? = nil,
        promptExtra: String = ""
    ) {
        guard musicProcess == nil else {
            statusLabel.stringValue = "正在生成音乐，请稍候"
            return
        }

        let generator = scriptDir.appendingPathComponent("generate_senseaudio_music.py")
        let envFile = workspaceDir.appendingPathComponent(".env")
        let pythonURL = FileManager.default.isExecutableFile(atPath: scriptDir.appendingPathComponent(".venv/bin/python").path)
            ? scriptDir.appendingPathComponent(".venv/bin/python")
            : URL(fileURLWithPath: "/usr/bin/env")

        let process = Process()
        process.executableURL = pythonURL
        var args = [generator.path, "--env-file", envFile.path, "--output-dir", outputDir.path]
        args += ["--style-preset", selectedMusicStyle().id]
        args += ["--generation-mode", selectedMusicGenerationMode().id]
        if !promptExtra.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            args += ["--prompt-extra", promptExtra]
        }
        if let titleOverride, !titleOverride.isEmpty {
            args += ["--title", titleOverride]
        }
        if let textFile {
            args += ["--text-file", textFile.path]
        }
        if let transcriptURL {
            args += ["--transcript-json", transcriptURL.path]
        }
        if pythonURL.lastPathComponent == "env" {
            process.arguments = ["python3"] + args
        } else {
            process.arguments = args
        }
        process.currentDirectoryURL = repoDirURL()
        let outputCollector = ProcessOutputCollector()
        outputCollector.attach(to: process)

        musicProcess = process
        refreshOrganizeButton()
        statusLabel.stringValue = "正在用 SenseAudio 为\(statusName)生成\(musicGenerationSummary())\(musicResultNoun())"

        process.terminationHandler = { [weak self] task in
            let text = outputCollector.finishText()
            DispatchQueue.main.async {
                self?.musicProcess = nil
                self?.refreshOrganizeButton()
                guard task.terminationStatus == 0 else {
                    self?.statusLabel.stringValue = text.isEmpty ? "音乐生成失败" : text
                    return
                }
                self?.invalidateRecentMusicTracksCache()
                self?.compactMusicPanelVisible = true
                self?.selectedCompactMusicIndex = 0
                self?.statusLabel.stringValue = "\(statusName) \(self?.musicResultNoun() ?? "作品")完成"
                if let path = self?.extractOutputAudioPath(from: text) {
                    NSWorkspace.shared.open(path)
                    let metaPrefix = metaOverride ?? "模式: \(self?.translationEnabled == true ? "双语" : "原文")"
                    self?.metaLabel.stringValue = "\(metaPrefix) | 生成: \(self?.musicGenerationSummary() ?? "纯音乐") | 文件: \(path.lastPathComponent)"
                    self?.refreshCompactPreview(forceReload: true)
                }
            }
        }

        do {
            try process.run()
        } catch {
            musicProcess = nil
            refreshOrganizeButton()
            statusLabel.stringValue = "音乐生成启动失败: \(error.localizedDescription)"
        }
    }

    @objc private func toggleMode() {
        translationEnabled.toggle()
        syncModeLabels()
        if controller.isRunning {
            pendingRestart = true
            controller.stop()
            statusLabel.stringValue = "正在切换模式"
        }
    }

    @objc private func closeWindow() {
        if controller.isRunning {
            pendingCompactAfterStop = true
            controller.stop()
            statusLabel.stringValue = "正在收起浮窗"
            return
        }
        clearSubtitleDisplayState()
        setCompactMode(true, animated: true)
        statusLabel.stringValue = "迷你浮窗待命中"
    }

    @objc private func closeCompactPreviewPanel() {
        compactProjectPanelVisible = false
        compactMusicPanelVisible = false
        selectedCompactProjectIndex = nil
        selectedCompactMusicIndex = nil
        compactHoverDismissDeadline = nil
        setCompactSatelliteHint(nil)
        refreshCompactPreview()
        syncCompactPanelWindow(animated: true)
        DispatchQueue.main.async { [weak self] in
            guard let self else { return }
            if self.isMouseInsideCompactRoot() {
                self.setCompactHoverVisible(true, animated: true)
            } else {
                self.setCompactHoverVisible(false, animated: true)
            }
        }
        statusLabel.stringValue = "面板已收起"
    }

    @objc private func refreshCompactPreviewPanelManually() {
        if compactMusicPanelVisible {
            invalidateRecentMusicTracksCache()
        } else {
            invalidateRecentProjectsCache()
        }
        refreshCompactPreview(forceReload: true)
        statusLabel.stringValue = compactMusicPanelVisible ? "音乐历史已刷新" : "最近项目已刷新"
    }

    private func isMouseInsideCompactRoot() -> Bool {
        guard let window = view.window, let compactRoot = compactRootView else { return false }
        let mouseLocation = NSEvent.mouseLocation
        let rootRect = window.convertToScreen(compactRoot.convert(compactRoot.bounds, to: nil))
        return rootRect.insetBy(dx: -12, dy: -12).contains(mouseLocation)
    }

    func forceCompactLaunchState(on window: NSWindow) {
        isCompactMode = true
        isCompactHoverVisible = false
        compactProjectPanelVisible = false
        compactMusicPanelVisible = false
        compactHoverDismissDeadline = nil
        applyPresentationMode(animated: false)
        syncCompactPanelWindow(animated: false)
        view.layoutSubtreeIfNeeded()
        placeWindowInVisibleArea(window)
    }

    func restoreWindowState(_ window: NSWindow) {
        placeWindowInVisibleArea(window)
    }

    func saveWindowState() {
        guard let window = view.window else { return }
        let frame = window.frame
        let payload: [String: CGFloat] = [
            "x": frame.origin.x,
            "y": frame.origin.y,
            "width": frame.size.width,
            "height": frame.size.height,
        ]
        let stateDir = statePath.deletingLastPathComponent()
        try? FileManager.default.createDirectory(at: stateDir, withIntermediateDirectories: true)
        if let data = try? JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted]) {
            try? data.write(to: statePath)
        }
    }

    func windowDidMove(_ notification: Notification) {
        syncCompactPanelWindow(animated: false)
        saveWindowState()
    }

    func windowDidEndLiveResize(_ notification: Notification) {
        syncCompactPanelWindow(animated: false)
        saveWindowState()
    }

    func windowWillClose(_ notification: Notification) {
        beginShutdown()
    }

    func placeWindowInVisibleArea(_ window: NSWindow) {
        let screenFrame = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let size = isCompactMode ? compactWindowSize : expandedWindowSize
        let origin = NSPoint(
            x: screenFrame.midX - size.width / 2,
            y: screenFrame.midY - size.height / 2
        )
        window.setFrame(NSRect(origin: origin, size: size), display: true)
        saveWindowState()
    }

    private func beginShutdown() {
        if shutdownStarted {
            return
        }
        shutdownStarted = true
        saveWindowState()

        let exitScript = scriptDir.appendingPathComponent("exit_subtitle_mode.sh")
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/bin/bash")
        process.arguments = [exitScript.path, "--skip-overlay-kill"]
        process.currentDirectoryURL = repoDirURL()
        try? process.run()

        controller.stop()
        compactPanelWindow?.orderOut(nil)
        view.window?.orderOut(nil)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            NSApp.terminate(nil)
        }
    }

    private func repoDirURL() -> URL {
        workspaceDir.deletingLastPathComponent()
    }

    private static func discoverLocalFastOptions(modelsRoot: URL) -> [LocalFastOption] {
        var options: [LocalFastOption] = [
            LocalFastOption(id: "disabled", label: "关闭", modelDir: nil)
        ]
        let fm = FileManager.default
        guard let enumerator = fm.enumerator(at: modelsRoot, includingPropertiesForKeys: [.isDirectoryKey], options: [.skipsHiddenFiles]) else {
            return options
        }

        for case let url as URL in enumerator {
            guard (try? url.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) == true else { continue }
            let modelFile = url.appendingPathComponent("model.int8.onnx")
            let transducerEncoder = url.appendingPathComponent("encoder-epoch-99-avg-1.int8.onnx")
            let averagedTransducerEncoder = url.appendingPathComponent("encoder-epoch-29-avg-9-with-averaged-model.int8.onnx")
            let tokensFile = url.appendingPathComponent("tokens.txt")
            guard fm.fileExists(atPath: tokensFile.path),
                  fm.fileExists(atPath: modelFile.path)
                    || fm.fileExists(atPath: transducerEncoder.path)
                    || fm.fileExists(atPath: averagedTransducerEncoder.path)
            else { continue }

            let folder = url.lastPathComponent.lowercased()
            let label: String
            if folder.contains("zh-en") || folder.contains("bilingual") {
                label = "中英"
            } else if folder.contains("korean") || folder.contains("ko-") {
                label = "韩语"
            } else if folder.contains("french") || folder.contains("fr-") {
                label = "法语"
            } else if folder.contains("german") || folder.contains("de-") {
                label = "德语"
            } else if folder.contains("spanish") || folder.contains("es-") {
                label = "西语"
            } else if folder.contains("-en-") || folder.contains("english") {
                label = "英文"
            } else if folder.contains("-zh-") || folder.contains("mandarin") || folder.contains("ctc-zh") {
                label = "中文"
            } else {
                label = url.lastPathComponent
            }

            let id = url.lastPathComponent
            if !options.contains(where: { $0.id == id }) {
                options.append(LocalFastOption(id: id, label: label, modelDir: url))
            }
        }
        let preferredOrder: [String: Int] = [
            "关闭": 0,
            "中文": 1,
            "英文": 2,
            "中英": 3,
            "韩语": 4,
            "法语": 5,
            "德语": 6,
            "西语": 7,
        ]
        return options.sorted {
            let lhs = preferredOrder[$0.label, default: 999]
            let rhs = preferredOrder[$1.label, default: 999]
            if lhs == rhs {
                return $0.label < $1.label
            }
            return lhs < rhs
        }
    }

    private func appendOverlayDebug(_ line: String) {
        let prefix = ISO8601DateFormatter().string(from: Date())
        let text = "[\(prefix)] [overlay] \(line)\n"
        let dir = debugLogPath.deletingLastPathComponent()
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        if let data = text.data(using: .utf8) {
            if FileManager.default.fileExists(atPath: debugLogPath.path),
               let handle = try? FileHandle(forWritingTo: debugLogPath) {
                _ = try? handle.seekToEnd()
                try? handle.write(contentsOf: data)
                try? handle.close()
            } else {
                try? data.write(to: debugLogPath)
            }
        }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var window: OverlayWindow?
    private var controller: OverlayViewController?

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        NSApp.unhide(nil)

        let executableURL = URL(fileURLWithPath: CommandLine.arguments[0]).resolvingSymlinksInPath()
        let bundleURL = Bundle.main.bundleURL.resolvingSymlinksInPath()
        let scriptDir: URL
        if bundleURL.pathExtension == "app" {
            scriptDir = bundleURL.deletingLastPathComponent()
        } else {
            scriptDir = executableURL.deletingLastPathComponent()
        }
        let workspaceDir = scriptDir.deletingLastPathComponent().deletingLastPathComponent()
        let repoDir = workspaceDir.deletingLastPathComponent()

        let viewController = OverlayViewController(scriptDir: scriptDir, workspaceDir: workspaceDir, repoDir: repoDir)
        self.controller = viewController
        _ = viewController.view
        viewController.ensureUIBuilt()

        let screenFrame = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let defaultFrame = NSRect(
            x: screenFrame.midX - viewController.compactLaunchWindowSize.width / 2,
            y: screenFrame.midY - viewController.compactLaunchWindowSize.height / 2,
            width: viewController.compactLaunchWindowSize.width,
            height: viewController.compactLaunchWindowSize.height
        )
        let window = OverlayWindow(
            contentRect: defaultFrame,
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        window.level = .floating
        window.isOpaque = false
        window.backgroundColor = .clear
        window.alphaValue = 1.0
        window.hasShadow = false
        window.isMovableByWindowBackground = true
        window.collectionBehavior = [.moveToActiveSpace]
        window.contentView = viewController.view
        window.delegate = viewController
        viewController.restoreWindowState(window)
        viewController.forceCompactLaunchState(on: window)
        NSApp.activate(ignoringOtherApps: true)
        window.setIsVisible(true)
        if let screen = NSScreen.main?.visibleFrame, !screen.intersects(window.frame) {
            viewController.placeWindowInVisibleArea(window)
        }
        window.orderFrontRegardless()
        window.makeKeyAndOrderFront(nil)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
            NSApp.unhide(nil)
            NSApp.activate(ignoringOtherApps: true)
            viewController.forceCompactLaunchState(on: window)
            window.setIsVisible(true)
            window.orderFrontRegardless()
            window.makeKeyAndOrderFront(nil)
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
            NSApp.unhide(nil)
            NSApp.activate(ignoringOtherApps: true)
            viewController.forceCompactLaunchState(on: window)
            window.setIsVisible(true)
            window.orderFrontRegardless()
            window.makeKeyAndOrderFront(nil)
        }

        self.window = window
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        true
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.setActivationPolicy(.regular)
app.delegate = delegate
app.run()
