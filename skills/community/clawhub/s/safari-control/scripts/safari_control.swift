#!/usr/bin/env swift

import AppKit
import ApplicationServices
import CoreGraphics
import Foundation
import UniformTypeIdentifiers

// MARK: - Constants

let jsPermissionHint =
    "Safari JavaScript access is disabled. Enable Safari Settings > Advanced > Developer, then turn on 'Allow JavaScript from Apple Events'."

let axPermissionHint =
    "Safari native UI automation requires macOS Accessibility access for this process."

let toolVersion = "0.4.1"

// MARK: - Errors

struct SafariControlError: Error, CustomStringConvertible {
    let message: String
    var description: String { message }
}

// MARK: - Process Helpers

struct ProcessResult {
    let status: Int32
    let stdout: String
    let stderr: String
}

func runProcess(_ executable: String, _ arguments: [String]) throws -> ProcessResult {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: executable)
    process.arguments = arguments

    let stdoutPipe = Pipe()
    let stderrPipe = Pipe()
    process.standardOutput = stdoutPipe
    process.standardError = stderrPipe

    try process.run()
    process.waitUntilExit()

    let stdoutData = stdoutPipe.fileHandleForReading.readDataToEndOfFile()
    let stderrData = stderrPipe.fileHandleForReading.readDataToEndOfFile()

    return ProcessResult(
        status: process.terminationStatus,
        stdout: String(data: stdoutData, encoding: .utf8) ?? "",
        stderr: String(data: stderrData, encoding: .utf8) ?? ""
    )
}

func runTemporaryScript(language: String?, script: String) throws -> ProcessResult {
    let scriptsDir = URL(fileURLWithPath: NSTemporaryDirectory(), isDirectory: true)
        .appendingPathComponent("safari-control-scripts", isDirectory: true)
    try FileManager.default.createDirectory(at: scriptsDir, withIntermediateDirectories: true)

    let fileExtension = language == "JavaScript" ? "js" : "applescript"
    let scriptURL = scriptsDir.appendingPathComponent(UUID().uuidString).appendingPathExtension(fileExtension)
    try script.write(to: scriptURL, atomically: true, encoding: .utf8)
    defer { try? FileManager.default.removeItem(at: scriptURL) }

    var arguments: [String] = []
    if let language {
        arguments += ["-l", language]
    }
    arguments.append(scriptURL.path)
    return try runProcess("/usr/bin/osascript", arguments)
}

func runOsaScript(_ script: String) throws -> String {
    let result = try runTemporaryScript(language: nil, script: script)
    if result.status != 0 {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        if stderr.contains("Allow JavaScript from Apple Events") {
            throw SafariControlError(message: jsPermissionHint)
        }
        throw SafariControlError(message: stderr.isEmpty ? "osascript failed" : stderr)
    }
    return result.stdout.trimmingCharacters(in: CharacterSet(charactersIn: "\n"))
}

func runJXAScript(_ script: String) throws -> String {
    let result = try runTemporaryScript(language: "JavaScript", script: script)
    if result.status != 0 {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        if stderr.contains("Allow JavaScript from Apple Events") {
            throw SafariControlError(message: jsPermissionHint)
        }
        throw SafariControlError(message: stderr.isEmpty ? "osascript JavaScript failed" : stderr)
    }
    return result.stdout.trimmingCharacters(in: CharacterSet(charactersIn: "\n"))
}

func sourceScriptDir() -> URL {
    URL(fileURLWithPath: #filePath).deletingLastPathComponent()
}

func resolveAXTool() -> (String, [String]) {
    if let entrypoint = CommandLine.arguments.first, !entrypoint.isEmpty {
        let normalized = URL(fileURLWithPath: entrypoint).standardizedFileURL.path
        if normalized.hasSuffix(".swift") {
            return ("/usr/bin/swift", [normalized, "__ax-helper"])
        }
        return (normalized, ["__ax-helper"])
    }
    return ("/usr/bin/swift", [sourceScriptDir().appendingPathComponent("safari_control.swift").path, "__ax-helper"])
}

func runAXTool(_ arguments: [String]) throws -> String {
    let tool = resolveAXTool()
    let result = try runProcess(tool.0, tool.1 + arguments)
    if result.status != 0 {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        if stderr.contains("Accessibility access is not enabled") {
            throw SafariControlError(message: axPermissionHint)
        }
        throw SafariControlError(message: stderr.isEmpty ? "Safari AX helper failed" : stderr)
    }
    return result.stdout.trimmingCharacters(in: CharacterSet(charactersIn: "\n"))
}

// MARK: - Serialization Helpers

func printJSON(_ value: Any) throws {
    let data = try JSONSerialization.data(withJSONObject: value, options: [.prettyPrinted, .fragmentsAllowed])
    if let text = String(data: data, encoding: .utf8) {
        print(text)
    }
}

func parseJSON(_ text: String, default fallback: Any) -> Any {
    guard let data = text.data(using: .utf8), !data.isEmpty else {
        return fallback
    }
    do {
        return try JSONSerialization.jsonObject(with: data)
    } catch {
        return fallback
    }
}

func jsonStringLiteral(_ value: String) throws -> String {
    let data = try JSONEncoder().encode(value)
    guard let text = String(data: data, encoding: .utf8) else {
        throw SafariControlError(message: "Failed to encode JSON string literal.")
    }
    return text
}

// MARK: - Filesystem Helpers

func expandPath(_ path: String) -> String {
    NSString(string: path).expandingTildeInPath
}

@discardableResult
func writeOutput(path: String, content: String) throws -> URL {
    let expanded = expandPath(path)
    let url = URL(fileURLWithPath: expanded)
    try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
    try content.write(to: url, atomically: true, encoding: .utf8)
    return url
}

@discardableResult
func writeJSONOutput(path: String, value: Any) throws -> URL {
    let data = try JSONSerialization.data(withJSONObject: value, options: [.prettyPrinted, .fragmentsAllowed])
    guard let text = String(data: data, encoding: .utf8) else {
        throw SafariControlError(message: "Failed to serialize JSON output.")
    }
    return try writeOutput(path: path, content: text)
}

func iso8601Timestamp(_ date: Date = Date()) -> String {
    let formatter = ISO8601DateFormatter()
    formatter.formatOptions = [.withInternetDateTime]
    return formatter.string(from: date)
}

func compactTimestamp(_ date: Date = Date()) -> String {
    let formatter = DateFormatter()
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.timeZone = TimeZone(secondsFromGMT: 0)
    formatter.dateFormat = "yyyyMMdd'T'HHmmss'Z'"
    return formatter.string(from: date)
}

// MARK: - Generic Helpers

func escapeAppleScript(_ value: String) -> String {
    value.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\"")
}

func retryMissingValue<T>(
    attempts: Int = 5,
    delay: TimeInterval = 0.1,
    _ block: () throws -> T
) throws -> T {
    var lastError: Error?
    for _ in 0..<attempts {
        do {
            return try block()
        } catch {
            let text = String(describing: error)
            if !text.contains("missing value") {
                throw error
            }
            lastError = error
            Thread.sleep(forTimeInterval: delay)
        }
    }
    throw lastError ?? SafariControlError(message: "Unexpected retry state.")
}

func waitUntil(
    timeoutMs: Int,
    intervalMs: Int,
    description: String,
    _ check: () throws -> Bool
) throws {
    let deadline = Date().timeIntervalSince1970 + Double(timeoutMs) / 1000.0
    while true {
        if try check() {
            return
        }
        if Date().timeIntervalSince1970 >= deadline {
            throw SafariControlError(message: "Timed out waiting for \(description).")
        }
        Thread.sleep(forTimeInterval: Double(intervalMs) / 1000.0)
    }
}

func fileSize(_ url: URL) -> Int64 {
    (try? url.resourceValues(forKeys: [.fileSizeKey]).fileSize).map(Int64.init) ?? 0
}

func sha256(_ url: URL) throws -> String {
    let result = try runProcess("/usr/bin/shasum", ["-a", "256", url.path])
    guard result.status == 0 else {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        throw SafariControlError(message: stderr.isEmpty ? "Failed to compute SHA-256 for \(url.lastPathComponent)." : stderr)
    }
    let line = result.stdout.trimmingCharacters(in: .whitespacesAndNewlines)
    guard let digest = line.split(separator: " ").first, !digest.isEmpty else {
        throw SafariControlError(message: "Failed to parse SHA-256 output for \(url.lastPathComponent).")
    }
    return String(digest)
}

func gitMetadata(startingAt directory: URL = sourceScriptDir()) -> [String: Any]? {
    func git(_ arguments: [String]) -> ProcessResult? {
        try? runProcess("/usr/bin/git", ["-C", directory.path] + arguments)
    }

    guard let rootResult = git(["rev-parse", "--show-toplevel"]), rootResult.status == 0 else {
        return nil
    }
    let repoRoot = rootResult.stdout.trimmingCharacters(in: .whitespacesAndNewlines)
    guard !repoRoot.isEmpty else { return nil }

    let branch = git(["branch", "--show-current"])?.stdout.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    let revision = git(["rev-parse", "HEAD"])?.stdout.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    let shortRevision = git(["rev-parse", "--short=12", "HEAD"])?.stdout.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    let commitTime = git(["log", "-1", "--format=%cI"])?.stdout.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    let statusText = git(["status", "--porcelain", "--untracked-files=normal"])?.stdout ?? ""
    let dirtyEntries = statusText
        .split(whereSeparator: \.isNewline)
        .map(String.init)
        .filter { !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty }

    return [
        "repo_root": repoRoot,
        "branch": branch,
        "revision": revision,
        "revision_short": shortRevision,
        "commit_time": commitTime,
        "dirty": !dirtyEntries.isEmpty,
        "dirty_entries": dirtyEntries.count,
    ]
}

func environmentMetadata() -> [String: Any] {
    func commandOutput(_ executable: String, _ arguments: [String]) -> String {
        let result = try? runProcess(executable, arguments)
        guard let result, result.status == 0 else { return "" }
        return result.stdout.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    let processInfo = ProcessInfo.processInfo
    let osVersion = processInfo.operatingSystemVersion
    let swProductName = commandOutput("/usr/bin/sw_vers", ["-productName"])
    let swProductVersion = commandOutput("/usr/bin/sw_vers", ["-productVersion"])
    let swBuildVersion = commandOutput("/usr/bin/sw_vers", ["-buildVersion"])
    let machine = commandOutput("/usr/bin/uname", ["-m"])

    return [
        "hostname": processInfo.hostName,
        "architecture": machine.isEmpty ? "unknown" : machine,
        "os": [
            "product_name": swProductName,
            "product_version": swProductVersion,
            "build_version": swBuildVersion,
            "version_string": "\(osVersion.majorVersion).\(osVersion.minorVersion).\(osVersion.patchVersion)",
        ],
        "process": [
            "processors": processInfo.processorCount,
            "active_processors": processInfo.activeProcessorCount,
            "physical_memory": Int64(processInfo.physicalMemory),
        ],
    ]
}

func mimeType(for url: URL) -> String {
    if let type = UTType(filenameExtension: url.pathExtension), let mime = type.preferredMIMEType {
        return mime
    }
    return "application/octet-stream"
}

func globMatches(_ name: String, pattern: String) -> Bool {
    let escaped = NSRegularExpression.escapedPattern(for: pattern)
        .replacingOccurrences(of: "\\*", with: ".*")
        .replacingOccurrences(of: "\\?", with: ".")
    let regex = "^\(escaped)$"
    return name.range(of: regex, options: .regularExpression) != nil
}

func safariInstallPath() -> String? {
    let candidates = [
        "/Applications/Safari.app",
        "/System/Applications/Safari.app",
    ]
    return candidates.first { FileManager.default.fileExists(atPath: $0) }
}

func doctorItem(name: String, ok: Bool, detail: String, hint: String? = nil) -> [String: Any] {
    var item: [String: Any] = [
        "name": name,
        "ok": ok,
        "detail": detail,
    ]
    if let hint {
        item["hint"] = hint
    }
    return item
}

func compileSwiftBinary(source: URL, output: URL) throws -> [String: Any] {
    let result = try runProcess("/usr/bin/xcrun", ["swiftc", "-O", source.path, "-o", output.path])
    if result.status != 0 {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        throw SafariControlError(message: stderr.isEmpty ? "swiftc failed for \(source.lastPathComponent)" : stderr)
    }
    return [
        "source": source.path,
        "output": output.path,
        "bytes": fileSize(output),
        "sha256": try sha256(output),
    ]
}

struct AXControlRecord {
    let index: Int
    let role: String
    let subrole: String
    let title: String
    let description: String
    let identifier: String
    let value: String
    let actions: [String]
    let pressable: Bool
    let focusable: Bool
    let settable: Bool
    let menuable: Bool
    let path: String

    var json: [String: Any] {
        [
            "index": index,
            "role": role,
            "subrole": subrole,
            "title": title,
            "description": description,
            "identifier": identifier,
            "value": value,
            "actions": actions,
            "pressable": pressable,
            "focusable": focusable,
            "settable": settable,
            "menuable": menuable,
            "path": path,
        ]
    }
}

struct AXMatchOptions {
    let exact: Bool
    let field: String
    let index: Int
    let includeWeb: Bool
}

struct AXMenuItemRecord {
    let role: String
    let title: String
    let description: String
    let identifier: String
    let enabled: Bool?
    let actions: [String]
    let path: [String]
    let children: [AXMenuItemRecord]

    var json: [String: Any] {
        [
            "role": role,
            "title": title,
            "description": description,
            "identifier": identifier,
            "enabled": enabled as Any,
            "actions": actions,
            "path": path,
            "children": children.map(\.json),
        ]
    }
}

func axCopyAttr(_ element: AXUIElement, _ name: String) -> AnyObject? {
    var value: CFTypeRef?
    let error = AXUIElementCopyAttributeValue(element, name as CFString, &value)
    guard error == .success else { return nil }
    return value
}

func axStrAttr(_ element: AXUIElement, _ name: String) -> String {
    if let value = axCopyAttr(element, name) as? String { return value }
    return ""
}

func axChildren(of element: AXUIElement) -> [AXUIElement] {
    if let value = axCopyAttr(element, kAXChildrenAttribute) as? [AXUIElement] { return value }
    return []
}

func axActionNames(of element: AXUIElement) -> [String] {
    var value: CFArray?
    let error = AXUIElementCopyActionNames(element, &value)
    guard error == .success, let names = value as? [String] else { return [] }
    return names
}

func axActionSummary(_ actions: [String]) -> String {
    actions.isEmpty ? "none" : actions.joined(separator: ", ")
}

func axBoolAttr(_ element: AXUIElement, _ name: String) -> Bool? {
    if let value = axCopyAttr(element, name) as? Bool { return value }
    return nil
}

func axIsValueSettable(_ element: AXUIElement) -> Bool {
    var isSettable = DarwinBoolean(false)
    let error = AXUIElementIsAttributeSettable(element, kAXValueAttribute as CFString, &isSettable)
    return error == .success && isSettable.boolValue
}

func axSetBoolAttr(_ element: AXUIElement, _ name: String, _ value: Bool) -> Bool {
    AXUIElementSetAttributeValue(element, name as CFString, value as CFTypeRef) == .success
}

func axLabelForPath(title: String, description: String, identifier: String) -> String {
    for candidate in [title, description, identifier] {
        if !candidate.isEmpty { return candidate }
    }
    return "(unnamed)"
}

func postKeyCode(_ keyCode: CGKeyCode) {
    guard let source = CGEventSource(stateID: .hidSystemState) else { return }
    let down = CGEvent(keyboardEventSource: source, virtualKey: keyCode, keyDown: true)
    let up = CGEvent(keyboardEventSource: source, virtualKey: keyCode, keyDown: false)
    down?.post(tap: .cghidEventTap)
    up?.post(tap: .cghidEventTap)
}

func axFocusedWindow() throws -> AXUIElement {
    guard AXIsProcessTrusted() else {
        throw SafariControlError(message: "Accessibility access is not enabled for this process.")
    }
    guard let app = NSRunningApplication.runningApplications(withBundleIdentifier: "com.apple.Safari").first else {
        throw SafariControlError(message: "Safari is not running.")
    }
    let axApp = AXUIElementCreateApplication(app.processIdentifier)
    guard let value = axCopyAttr(axApp, kAXFocusedWindowAttribute) else {
        throw SafariControlError(message: "Safari has no focused window.")
    }
    guard CFGetTypeID(value) == AXUIElementGetTypeID() else {
        throw SafariControlError(message: "Safari focused window is not an accessibility element.")
    }
    return unsafeBitCast(value, to: AXUIElement.self)
}

func axIsActionable(role: String, actions: [String]) -> Bool {
    let interestingRoles = Set([
        "AXButton",
        "AXMenuButton",
        "AXPopUpButton",
        "AXCheckBox",
        "AXRadioButton",
        "AXTextField",
        "AXComboBox",
        "AXTabGroup",
    ])
    if interestingRoles.contains(role) { return true }
    if actions.contains(kAXPressAction as String) { return true }
    return false
}

func axCollectControls(root: AXUIElement, includeWeb: Bool, includeAll: Bool) -> [(AXUIElement, AXControlRecord)] {
    var results: [(AXUIElement, AXControlRecord)] = []

    func walk(_ element: AXUIElement, path: [Int]) {
        let role = axStrAttr(element, kAXRoleAttribute)
        if !includeWeb && role == "AXWebArea" { return }
        let subrole = axStrAttr(element, kAXSubroleAttribute)
        let title = axStrAttr(element, kAXTitleAttribute)
        let description = axStrAttr(element, kAXDescriptionAttribute)
        let identifier = axStrAttr(element, kAXIdentifierAttribute)
        let value = axCopyAttr(element, kAXValueAttribute).map(String.init(describing:)) ?? ""
        let actions = axActionNames(of: element)
        let pressable = actions.contains(kAXPressAction as String)
        let focusable = axCopyAttr(element, kAXFocusedAttribute) != nil || pressable
        let settable = axIsValueSettable(element)
        let menuable = actions.contains(kAXShowMenuAction as String)
        if includeAll || axIsActionable(role: role, actions: actions) {
            let record = AXControlRecord(
                index: results.count + 1,
                role: role,
                subrole: subrole,
                title: title,
                description: description,
                identifier: identifier,
                value: value,
                actions: actions,
                pressable: pressable,
                focusable: focusable,
                settable: settable,
                menuable: menuable,
                path: path.map(String.init).joined(separator: ".")
            )
            results.append((element, record))
        }
        for (idx, child) in axChildren(of: element).enumerated() {
            walk(child, path: path + [idx + 1])
        }
    }

    walk(root, path: [1])
    return results
}

func axMatchControl(_ controls: [AXControlRecord], query: String, exact: Bool, field: String, index: Int) throws -> AXControlRecord {
    let needle = query.lowercased()
    let matches = controls.filter { record in
        let haystacks: [String]
        switch field {
        case "title":
            haystacks = [record.title]
        case "description":
            haystacks = [record.description]
        case "identifier":
            haystacks = [record.identifier]
        case "value":
            haystacks = [record.value]
        default:
            haystacks = [record.title, record.description, record.identifier, record.value]
        }
        return haystacks.contains { hay in
            let text = hay.lowercased()
            return exact ? text == needle : text.contains(needle)
        }
    }
    guard !matches.isEmpty else {
        throw SafariControlError(message: "No native Safari control matched: \(query)")
    }
    guard index > 0, index <= matches.count else {
        throw SafariControlError(message: "Only found \(matches.count) native Safari control matches, index \(index) is out of range.")
    }
    return matches[index - 1]
}

func axPress(element: AXUIElement, record: AXControlRecord) throws {
    if axActionNames(of: element).contains(kAXPressAction as String) {
        let error = AXUIElementPerformAction(element, kAXPressAction as CFString)
        guard error == .success else {
            throw SafariControlError(message: "AXPress failed for \(record.identifier.isEmpty ? record.title : record.identifier).")
        }
        return
    }
    if record.role == "AXTextField", axSetBoolAttr(element, kAXFocusedAttribute, true) {
        return
    }
    let label = record.identifier.isEmpty ? (record.title.isEmpty ? record.description : record.title) : record.identifier
    throw SafariControlError(message: "Safari control is not pressable: \(label). Available actions: \(axActionSummary(record.actions)).")
}

func axPerformAction(element: AXUIElement, record: AXControlRecord, actionName: String) throws {
    let available = axActionNames(of: element)
    guard available.contains(actionName) else {
        throw SafariControlError(message: "Safari control does not expose action \(actionName). Available actions: \(axActionSummary(available)).")
    }
    let error = AXUIElementPerformAction(element, actionName as CFString)
    guard error == .success else {
        throw SafariControlError(message: "AX action \(actionName) failed for \(record.identifier.isEmpty ? record.title : record.identifier).")
    }
}

func axSetValue(element: AXUIElement, record: AXControlRecord, value: String) throws {
    let result = AXUIElementSetAttributeValue(element, kAXValueAttribute as CFString, value as CFTypeRef)
    guard result == .success else {
        let label = record.identifier.isEmpty ? (record.title.isEmpty ? record.description : record.title) : record.identifier
        throw SafariControlError(message: "Failed to set value for \(label). Available actions: \(axActionSummary(record.actions)).")
    }
    _ = axSetBoolAttr(element, kAXFocusedAttribute, true)
}

func axFocusControl(element: AXUIElement, record: AXControlRecord) throws {
    if axSetBoolAttr(element, kAXFocusedAttribute, true) {
        return
    }
    if axActionNames(of: element).contains(kAXPressAction as String) {
        let error = AXUIElementPerformAction(element, kAXPressAction as CFString)
        guard error == .success else {
            let label = record.identifier.isEmpty ? (record.title.isEmpty ? record.description : record.title) : record.identifier
            throw SafariControlError(message: "Failed to focus \(label). Available actions: \(axActionSummary(record.actions)).")
        }
        return
    }
    let label = record.identifier.isEmpty ? (record.title.isEmpty ? record.description : record.title) : record.identifier
    throw SafariControlError(message: "Safari control is not focusable: \(label). Available actions: \(axActionSummary(record.actions)).")
}

func axReadMatchOptions(_ argv: [String]) -> AXMatchOptions {
    let exact = argv.contains("--exact")
    let includeWeb = argv.contains("--include-web")
    let field: String
    if let idx = argv.firstIndex(of: "--field"), idx + 1 < argv.count {
        field = argv[idx + 1]
    } else {
        field = "any"
    }
    let matchIndex: Int
    if let idx = argv.firstIndex(of: "--index"), idx + 1 < argv.count {
        matchIndex = Int(argv[idx + 1]) ?? 1
    } else {
        matchIndex = 1
    }
    return AXMatchOptions(exact: exact, field: field, index: matchIndex, includeWeb: includeWeb)
}

func axMatchedControl(root: AXUIElement, query: String, options: AXMatchOptions) throws -> (AXUIElement, AXControlRecord) {
    let controls = axCollectControls(root: root, includeWeb: options.includeWeb, includeAll: true)
    let record = try axMatchControl(
        controls.map(\.1),
        query: query,
        exact: options.exact,
        field: options.field,
        index: options.index
    )
    guard let tuple = controls.first(where: { $0.1.index == record.index }) else {
        throw SafariControlError(message: "Matched control disappeared before action.")
    }
    return tuple
}

func axCollectMenus(root: AXUIElement) -> [(AXUIElement, [Int], String)] {
    var results: [(AXUIElement, [Int], String)] = []

    func walk(_ element: AXUIElement, path: [Int]) {
        let role = axStrAttr(element, kAXRoleAttribute)
        if role == "AXMenu" {
            let itemLabels = axChildren(of: element)
                .filter { axStrAttr($0, kAXRoleAttribute) == "AXMenuItem" }
                .map {
                    axLabelForPath(
                        title: axStrAttr($0, kAXTitleAttribute),
                        description: axStrAttr($0, kAXDescriptionAttribute),
                        identifier: axStrAttr($0, kAXIdentifierAttribute)
                    )
                }
                .joined(separator: "|")
            let signature = path.map(String.init).joined(separator: ".") + "::" + itemLabels
            results.append((element, path, signature))
        }
        for (idx, child) in axChildren(of: element).enumerated() {
            walk(child, path: path + [idx + 1])
        }
    }

    walk(root, path: [1])
    return results
}

func axChildMenu(of item: AXUIElement) -> AXUIElement? {
    axChildren(of: item).first { axStrAttr($0, kAXRoleAttribute) == "AXMenu" }
}

func axBuildMenuItems(_ menu: AXUIElement, path: [String]) -> [AXMenuItemRecord] {
    axChildren(of: menu)
        .filter { axStrAttr($0, kAXRoleAttribute) == "AXMenuItem" }
        .map { item in
            let title = axStrAttr(item, kAXTitleAttribute)
            let description = axStrAttr(item, kAXDescriptionAttribute)
            let identifier = axStrAttr(item, kAXIdentifierAttribute)
            let label = axLabelForPath(title: title, description: description, identifier: identifier)
            let nextPath = path + [label]
            let submenuChildren = axChildMenu(of: item).map { axBuildMenuItems($0, path: nextPath) } ?? []
            return AXMenuItemRecord(
                role: axStrAttr(item, kAXRoleAttribute),
                title: title,
                description: description,
                identifier: identifier,
                enabled: axBoolAttr(item, kAXEnabledAttribute),
                actions: axActionNames(of: item),
                path: nextPath,
                children: submenuChildren
            )
        }
}

func axFilterTopLevelMenus(_ menus: [(AXUIElement, [Int], String)]) -> [(AXUIElement, [Int], String)] {
    menus.filter { candidate in
        !menus.contains { other in
            guard other.1.count < candidate.1.count else { return false }
            return Array(candidate.1.prefix(other.1.count)) == other.1
        }
    }
}

func axNewMenus(afterShowingOn root: AXUIElement, baseline: Set<String>) -> [(AXUIElement, [Int], String)] {
    let current = axCollectMenus(root: root)
    let delta = current.filter { !baseline.contains($0.2) }
    if !delta.isEmpty { return axFilterTopLevelMenus(delta) }
    return axFilterTopLevelMenus(current)
}

func axCancelMenus(root: AXUIElement, _ menus: [AXUIElement]) {
    for menu in menus {
        let available = axActionNames(of: menu)
        if available.contains("AXCancel") {
            _ = AXUIElementPerformAction(menu, "AXCancel" as CFString)
        }
    }
    usleep(100_000)
    if !axCollectMenus(root: root).isEmpty {
        postKeyCode(53)
        usleep(100_000)
    }
}

func axShowMenuForControl(root: AXUIElement, query: String, options: AXMatchOptions, timeoutMs: Int) throws -> (AXControlRecord, [(AXUIElement, [Int], String)]) {
    let existingMenus = axCollectMenus(root: root)
    if !existingMenus.isEmpty {
        axCancelMenus(root: root, existingMenus.map(\.0))
    }
    let baseline = Set(axCollectMenus(root: root).map(\.2))
    let tuple = try axMatchedControl(root: root, query: query, options: options)
    _ = axSetBoolAttr(tuple.0, kAXFocusedAttribute, true)
    usleep(50_000)
    try axPerformAction(element: tuple.0, record: tuple.1, actionName: "AXShowMenu")

    let deadline = Date().addingTimeInterval(Double(timeoutMs) / 1000.0)
    while Date() < deadline {
        let menus = axNewMenus(afterShowingOn: root, baseline: baseline)
        if !menus.isEmpty {
            return (tuple.1, menus)
        }
        usleep(100_000)
    }
    throw SafariControlError(message: "Timed out waiting for a Safari native menu after AXShowMenu.")
}

func axItemMatches(_ item: AXUIElement, query: String, field: String, exact: Bool) -> Bool {
    let needle = query.lowercased()
    let haystacks: [String]
    switch field {
    case "title":
        haystacks = [axStrAttr(item, kAXTitleAttribute)]
    case "description":
        haystacks = [axStrAttr(item, kAXDescriptionAttribute)]
    case "identifier":
        haystacks = [axStrAttr(item, kAXIdentifierAttribute)]
    default:
        haystacks = [
            axStrAttr(item, kAXTitleAttribute),
            axStrAttr(item, kAXDescriptionAttribute),
            axStrAttr(item, kAXIdentifierAttribute),
        ]
    }
    return haystacks.contains { hay in
        let text = hay.lowercased()
        return exact ? text == needle : text.contains(needle)
    }
}

func axSelectMenuPath(menu: AXUIElement, segments: [String], field: String, exact: Bool, trail: [String]) throws -> (AXUIElement, [String])? {
    guard let segment = segments.first else { return nil }
    let items = axChildren(of: menu).filter { axStrAttr($0, kAXRoleAttribute) == "AXMenuItem" }
    let matches = items.filter { axItemMatches($0, query: segment, field: field, exact: exact) }
    if matches.isEmpty { return nil }
    if segments.count == 1 {
        if matches.count > 1 {
            throw SafariControlError(message: "Native menu path is ambiguous at segment '\(segment)'.")
        }
        let item = matches[0]
        let label = axLabelForPath(
            title: axStrAttr(item, kAXTitleAttribute),
            description: axStrAttr(item, kAXDescriptionAttribute),
            identifier: axStrAttr(item, kAXIdentifierAttribute)
        )
        return (item, trail + [label])
    }

    var resolved: [(AXUIElement, [String])] = []
    for item in matches {
        let label = axLabelForPath(
            title: axStrAttr(item, kAXTitleAttribute),
            description: axStrAttr(item, kAXDescriptionAttribute),
            identifier: axStrAttr(item, kAXIdentifierAttribute)
        )
        var submenu = axChildMenu(of: item)
        if submenu == nil && axActionNames(of: item).contains(kAXPressAction as String) {
            _ = AXUIElementPerformAction(item, kAXPressAction as CFString)
            usleep(150_000)
            submenu = axChildMenu(of: item)
        }
        if let submenu,
           let next = try axSelectMenuPath(
                menu: submenu,
                segments: Array(segments.dropFirst()),
                field: field,
                exact: exact,
                trail: trail + [label]
           ) {
            resolved.append(next)
        }
    }
    if resolved.count > 1 {
        throw SafariControlError(message: "Native menu path is ambiguous under segment '\(segment)'.")
    }
    return resolved.first
}

func handleEmbeddedAXHelper(arguments argv: [String]) throws {
    guard let command = argv.first else {
        throw SafariControlError(message: "usage: safari_control __ax-helper <list-controls|press-control|perform-action|set-value|focus-control|list-menu-items|pick-menu-item> ...")
    }
    let root = try axFocusedWindow()
    switch command {
    case "list-controls":
        let includeWeb = argv.contains("--include-web")
        let includeAll = argv.contains("--all")
        try printJSON(axCollectControls(root: root, includeWeb: includeWeb, includeAll: includeAll).map { $0.1.json })
    case "press-control":
        guard argv.count >= 2 else { throw SafariControlError(message: "press-control requires a query.") }
        let query = argv[1]
        let options = axReadMatchOptions(argv)
        let tuple = try axMatchedControl(root: root, query: query, options: options)
        try axPress(element: tuple.0, record: tuple.1)
        try printJSON(["ok": true, "control": tuple.1.json])
    case "perform-action":
        guard argv.count >= 3 else { throw SafariControlError(message: "perform-action requires a query and action name.") }
        let query = argv[1]
        let actionName = argv[2]
        let options = axReadMatchOptions(argv)
        let tuple = try axMatchedControl(root: root, query: query, options: options)
        try axPerformAction(element: tuple.0, record: tuple.1, actionName: actionName)
        try printJSON(["ok": true, "action": actionName, "control": tuple.1.json])
    case "set-value":
        guard argv.count >= 3 else { throw SafariControlError(message: "set-value requires a query and text value.") }
        let query = argv[1]
        let value = argv[2]
        let options = axReadMatchOptions(argv)
        let tuple = try axMatchedControl(root: root, query: query, options: options)
        try axSetValue(element: tuple.0, record: tuple.1, value: value)
        try printJSON(["ok": true, "value": value, "control": tuple.1.json])
    case "focus-control":
        guard argv.count >= 2 else { throw SafariControlError(message: "focus-control requires a query.") }
        let query = argv[1]
        let options = axReadMatchOptions(argv)
        let tuple = try axMatchedControl(root: root, query: query, options: options)
        try axFocusControl(element: tuple.0, record: tuple.1)
        try printJSON(["ok": true, "control": tuple.1.json])
    case "list-menu-items":
        guard argv.count >= 2 else { throw SafariControlError(message: "list-menu-items requires a control query.") }
        let query = argv[1]
        let options = axReadMatchOptions(argv)
        let timeoutMs = argv.firstIndex(of: "--timeout-ms").flatMap { idx in
            idx + 1 < argv.count ? Int(argv[idx + 1]) : nil
        } ?? 1500
        let result = try axShowMenuForControl(root: root, query: query, options: options, timeoutMs: timeoutMs)
        let menuElements = result.1.map(\.0)
        defer { axCancelMenus(root: root, menuElements) }
        let menus = menuElements.flatMap { axBuildMenuItems($0, path: []).map(\.json) }
        try printJSON(["ok": true, "control": result.0.json, "items": menus])
    case "pick-menu-item":
        guard argv.count >= 3 else { throw SafariControlError(message: "pick-menu-item requires a control query and at least one menu path segment.") }
        let query = argv[1]
        let options = axReadMatchOptions(argv)
        let timeoutMs = argv.firstIndex(of: "--timeout-ms").flatMap { idx in
            idx + 1 < argv.count ? Int(argv[idx + 1]) : nil
        } ?? 1500
        let itemField = argv.firstIndex(of: "--item-field").flatMap { idx in
            idx + 1 < argv.count ? argv[idx + 1] : nil
        } ?? "any"
        let itemExact = !argv.contains("--item-contains")
        let optionFlags = Set(["--exact", "--field", "--index", "--include-web", "--timeout-ms", "--item-field", "--item-contains"])
        var skipNext = false
        var itemSegments: [String] = []
        for token in argv.dropFirst(2) {
            if skipNext {
                skipNext = false
                continue
            }
            if ["--field", "--index", "--timeout-ms", "--item-field"].contains(token) {
                skipNext = true
                continue
            }
            if optionFlags.contains(token) { continue }
            itemSegments.append(token)
        }
        if itemSegments.isEmpty {
            throw SafariControlError(message: "pick-menu-item requires at least one native menu path segment.")
        }
        let result = try axShowMenuForControl(root: root, query: query, options: options, timeoutMs: timeoutMs)
        let menuElements = result.1.map(\.0)
        defer { axCancelMenus(root: root, menuElements) }
        var matches: [(AXUIElement, [String])] = []
        for menu in menuElements {
            if let matched = try axSelectMenuPath(menu: menu, segments: itemSegments, field: itemField, exact: itemExact, trail: []) {
                matches.append(matched)
            }
        }
        if matches.isEmpty {
            throw SafariControlError(message: "No native menu item matched path: \(itemSegments.joined(separator: " > "))")
        }
        if matches.count > 1 {
            throw SafariControlError(message: "Native menu item path is ambiguous: \(itemSegments.joined(separator: " > "))")
        }
        let item = matches[0].0
        let itemActions = axActionNames(of: item)
        let actionName = itemActions.contains("AXPick") ? "AXPick" : (itemActions.contains(kAXPressAction as String) ? (kAXPressAction as String) : "")
        if actionName.isEmpty {
            throw SafariControlError(message: "Matched native menu item is not selectable.")
        }
        let error = AXUIElementPerformAction(item, actionName as CFString)
        guard error == .success else {
            throw SafariControlError(message: "Failed to select native menu item: \(matches[0].1.joined(separator: " > "))")
        }
        try printJSON(["ok": true, "control": result.0.json, "action": actionName, "path": matches[0].1])
    default:
        throw SafariControlError(message: "Unknown AX helper command: \(command)")
    }
}

// Use ditto so the produced archive is a normal Finder/macOS-friendly zip.
func createZipArchive(item: URL, output: URL) throws -> [String: Any] {
    if FileManager.default.fileExists(atPath: output.path) {
        throw SafariControlError(message: "Refusing to overwrite existing zip archive: \(output.path)")
    }
    try FileManager.default.createDirectory(at: output.deletingLastPathComponent(), withIntermediateDirectories: true)
    let result = try runProcess("/usr/bin/ditto", ["-c", "-k", "--sequesterRsrc", "--keepParent", item.path, output.path])
    if result.status != 0 || fileSize(output) <= 0 {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        throw SafariControlError(message: stderr.isEmpty ? "Failed to create zip archive for \(item.lastPathComponent)." : stderr)
    }
    return [
        "path": output.path,
        "bytes": fileSize(output),
        "sha256": try sha256(output),
    ]
}

struct SafariWindowTarget {
    let windowID: Int
    let bounds: CGRect
    let title: String
}

func safariRunningApplication() -> NSRunningApplication? {
    NSRunningApplication.runningApplications(withBundleIdentifier: "com.apple.Safari").first
}

func safariOwnerNames() -> Set<String> {
    var names: Set<String> = ["Safari", "Safari浏览器"]
    if let app = safariRunningApplication() {
        if let localized = app.localizedName, !localized.isEmpty {
            names.insert(localized)
        }
    }
    return names
}

func safariWindowTarget() throws -> SafariWindowTarget {
    let options: CGWindowListOption = [.optionOnScreenOnly, .excludeDesktopElements]
    guard let rawList = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
        throw SafariControlError(message: "Failed to read macOS window list.")
    }
    let ownerNames = safariOwnerNames()

    let candidates = rawList.compactMap { window -> SafariWindowTarget? in
        guard let owner = window[kCGWindowOwnerName as String] as? String, ownerNames.contains(owner) else { return nil }
        guard let layer = window[kCGWindowLayer as String] as? Int, layer == 0 else { return nil }
        guard let number = window[kCGWindowNumber as String] as? Int else { return nil }
        guard let boundsValue = window[kCGWindowBounds as String] as? [String: Any],
              let rect = CGRect(dictionaryRepresentation: boundsValue as CFDictionary) else { return nil }
        let title = (window[kCGWindowName as String] as? String) ?? ""
        if rect.width < 80 || rect.height < 80 { return nil }
        return SafariWindowTarget(windowID: number, bounds: rect, title: title)
    }

    guard let target = candidates.max(by: { ($0.bounds.width * $0.bounds.height) < ($1.bounds.width * $1.bounds.height) }) else {
        throw SafariControlError(message: "No visible Safari window was found for screenshot.")
    }
    return target
}

func screenshotBackground(path: URL) throws -> [String: Any] {
    let target = try safariWindowTarget()
    let result = try runProcess("/usr/sbin/screencapture", ["-l", String(target.windowID), "-o", "-x", path.path])
    guard result.status == 0, fileSize(path) > 0 else {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        throw SafariControlError(message: stderr.isEmpty ? "Background Safari screenshot failed." : stderr)
    }
    return [
        "ok": true,
        "mode": "background",
        "path": path.path,
        "bytes": fileSize(path),
        "window_id": target.windowID,
        "title": target.title,
        "bounds": [
            "x": Int(target.bounds.origin.x.rounded()),
            "y": Int(target.bounds.origin.y.rounded()),
            "width": Int(target.bounds.size.width.rounded()),
            "height": Int(target.bounds.size.height.rounded()),
        ],
    ]
}

func screenshotForeground(path: URL, restorePreviousApp: Bool) throws -> [String: Any] {
    let previousApp = NSWorkspace.shared.frontmostApplication
    guard let safari = safariRunningApplication() else {
        throw SafariControlError(message: "Safari is not running.")
    }
    _ = try runOsaScript(#"tell application "Safari" to activate"#)
    Thread.sleep(forTimeInterval: 0.35)
    let target = try safariWindowTarget()
    let x = Int(target.bounds.origin.x.rounded())
    let y = Int(target.bounds.origin.y.rounded())
    let width = Int(target.bounds.size.width.rounded())
    let height = Int(target.bounds.size.height.rounded())
    let rect = "\(x),\(y),\(width),\(height)"
    let result = try runProcess("/usr/sbin/screencapture", ["-x", "-R", rect, path.path])
    if restorePreviousApp,
       let previousApp,
       previousApp.processIdentifier != safari.processIdentifier,
       let bundleID = previousApp.bundleIdentifier {
        _ = try? runOsaScript(#"tell application id "\#(escapeAppleScript(bundleID))" to activate"#)
    }
    guard result.status == 0, fileSize(path) > 0 else {
        let stderr = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        throw SafariControlError(message: stderr.isEmpty ? "Foreground Safari screenshot failed." : stderr)
    }
    return [
        "ok": true,
        "mode": "foreground",
        "path": path.path,
        "bytes": fileSize(path),
        "window_id": target.windowID,
        "title": target.title,
        "bounds": [
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        ],
    ]
}

func captureScreenshot(path: URL, mode: String, restorePreviousApp: Bool) throws -> [String: Any] {
    switch mode {
    case "background":
        return try screenshotBackground(path: path)
    case "foreground":
        return try screenshotForeground(path: path, restorePreviousApp: restorePreviousApp)
    case "auto":
        do {
            return try screenshotBackground(path: path)
        } catch {
            return try screenshotForeground(path: path, restorePreviousApp: restorePreviousApp)
        }
    default:
        throw SafariControlError(message: "Unsupported screenshot mode: \(mode). Use auto, background, or foreground.")
    }
}

// MARK: - Argument Parsing

struct CommandOptions {
    let positionals: [String]
    let flags: Set<String>
    let values: [String: String]

    init(_ arguments: [String]) {
        var positionals: [String] = []
        var flags: Set<String> = []
        var values: [String: String] = [:]
        var index = 0

        while index < arguments.count {
            let arg = arguments[index]
            if arg.hasPrefix("--") {
                if index + 1 < arguments.count, !arguments[index + 1].hasPrefix("--") {
                    values[arg] = arguments[index + 1]
                    index += 2
                } else {
                    flags.insert(arg)
                    index += 1
                }
            } else {
                positionals.append(arg)
                index += 1
            }
        }

        self.positionals = positionals
        self.flags = flags
        self.values = values
    }

    func flag(_ name: String) -> Bool {
        flags.contains(name)
    }

    func string(_ name: String) -> String? {
        values[name]
    }

    func int(_ name: String) throws -> Int? {
        guard let raw = values[name] else { return nil }
        guard let value = Int(raw) else {
            throw SafariControlError(message: "Invalid integer for \(name): \(raw)")
        }
        return value
    }

    func tabTarget() throws -> SafariTabTarget? {
        let window = try int("--window")
        let tab = try int("--tab")
        if window == nil && tab == nil {
            return nil
        }
        if let window, window <= 0 {
            throw SafariControlError(message: "--window must be greater than 0.")
        }
        if let tab, tab <= 0 {
            throw SafariControlError(message: "--tab must be greater than 0.")
        }
        return SafariTabTarget(window: window, tab: tab)
    }
}

struct SafariTabTarget {
    let window: Int?
    let tab: Int?
}

func safariTargetSetup(_ target: SafariTabTarget?) -> String {
    let windowLine: String
    if let window = target?.window {
        windowLine = "set theWindow to window \(window)"
    } else {
        windowLine = "set theWindow to front window"
    }

    let tabLine: String
    if let tab = target?.tab {
        tabLine = "set theTab to tab \(tab) of theWindow"
    } else {
        tabLine = "set theTab to current tab of theWindow"
    }

    return windowLine + "\n            " + tabLine
}

func safariTargetStateJSON(target: SafariTabTarget? = nil) throws -> [String: Any] {
    let windowExpr = (target?.window).map(String.init) ?? "null"
    let tabExpr = (target?.tab).map(String.init) ?? "null"
    let script = #"""
    (() => {
      const safari = Application("Safari");
      const windows = safari.windows();
      const windowIndex = \#(windowExpr);
      const tabIndex = \#(tabExpr);
      if (!windows.length) {
        return JSON.stringify({ current: null, windows: [], tabs: [] });
      }

      const resolveWindow = (index) => {
        if (index === null) return windows[0];
        if (index <= 0 || index > windows.length) {
          throw new Error(`Safari window ${index} does not exist.`);
        }
        return windows[index - 1];
      };

      const resolveTab = (window, index) => {
        const tabs = window.tabs();
        if (!tabs.length) return null;
        if (index === null) return window.currentTab();
        if (index <= 0 || index > tabs.length) {
          throw new Error(`Safari tab ${index} does not exist in the selected window.`);
        }
        return tabs[index - 1];
      };

      const windowsJSON = windows.map((window, windowOffset) => {
        const tabs = window.tabs();
        const current = tabs.length ? window.currentTab() : null;
        const currentIndex = current ? (current.index() || 0) : 0;
        const currentTitle = current ? (current.name() || "") : "";
        const currentURL = current ? (current.url() || "") : "";
        return {
          window: windowOffset + 1,
          front: windowOffset === 0,
          tab_count: tabs.length,
          current_tab: currentIndex,
          title: currentTitle,
          url: currentURL
        };
      });

      const tabsJSON = windows.flatMap((window, windowOffset) => {
        const tabs = window.tabs();
        const current = tabs.length ? window.currentTab() : null;
        const currentIndex = current ? (current.index() || 0) : 0;
        return tabs.map((tab, tabOffset) => ({
          window: windowOffset + 1,
          tab: tabOffset + 1,
          current: current ? (tab.index() || 0) === currentIndex : false,
          title: tab.name() || "",
          url: tab.url() || ""
        }));
      });

      const selectedWindow = resolveWindow(windowIndex);
      const selectedTab = resolveTab(selectedWindow, tabIndex);

      return JSON.stringify({
        current: selectedTab ? {
          title: selectedTab.name() || "",
          url: selectedTab.url() || ""
        } : null,
        windows: windowsJSON,
        tabs: tabsJSON
      });
    })()
    """#
    return parseJSON(try runJXAScript(script), default: [:]) as? [String: Any] ?? [:]
}

// MARK: - Core Safari State

func currentTab(target: SafariTabTarget? = nil) throws -> [String: Any] {
    let payload = try safariTargetStateJSON(target: target)
    return payload["current"] as? [String: Any] ?? [:]
}

func allWindows() throws -> [[String: Any]] {
    let payload = try safariTargetStateJSON()
    return payload["windows"] as? [[String: Any]] ?? []
}

func currentTabSource(target: SafariTabTarget? = nil) throws -> String {
    let targetSetup = safariTargetSetup(target)
    return try runOsaScript(
        #"""
        tell application "Safari"
            if (count of windows) = 0 then
                return ""
            end if
            \#(targetSetup)
            return source of theTab
        end tell
        """#
    )
}

func allTabs() throws -> [[String: Any]] {
    let payload = try safariTargetStateJSON()
    return payload["tabs"] as? [[String: Any]] ?? []
}

func buildSessionSnapshot(frontOnly: Bool, window: Int?) throws -> [String: Any] {
    var windows = try allWindows()
    var tabs = try allTabs()

    if frontOnly {
        windows = windows.filter { ($0["front"] as? Bool) == true }
    } else if let window {
        windows = windows.filter { ($0["window"] as? Int) == window }
    }

    let wanted = Set(windows.compactMap { $0["window"] as? Int })
    tabs = tabs.filter { tab in
        guard let window = tab["window"] as? Int else { return false }
        return wanted.contains(window)
    }

    var grouped: [Int: [[String: Any]]] = [:]
    for tab in tabs {
        guard let window = tab["window"] as? Int else { continue }
        grouped[window, default: []].append(tab)
    }

    let snapshotWindows = windows.map { window -> [String: Any] in
        let index = window["window"] as? Int ?? 0
        return [
            "window": index,
            "front": window["front"] as? Bool ?? false,
            "current_tab": window["current_tab"] as? Int ?? 1,
            "tabs": grouped[index] ?? [],
        ]
    }

    return [
        "created_at": Int(Date().timeIntervalSince1970),
        "window_count": snapshotWindows.count,
        "windows": snapshotWindows,
    ]
}

// MARK: - Safari JavaScript Helpers

func jsResult(_ code: String, target: SafariTabTarget? = nil) throws -> String {
    let escaped = escapeAppleScript(code)
    let targetSetup = safariTargetSetup(target)
    return try runOsaScript(
        #"""
        tell application "Safari"
            if (count of windows) = 0 then
                error "Safari has no open windows."
            end if
            \#(targetSetup)
            return do JavaScript "\#(escaped)" in theTab
        end tell
        """#
    )
}

func getTextForMode(_ mode: String, target: SafariTabTarget? = nil) throws -> String {
    let snippets: [String: String] = [
        "body": #"""(() => document.body ? document.body.innerText : "")()"""#,
        "selection": #"""(() => window.getSelection ? window.getSelection().toString() : "")()"""#,
        "article": #"""
        (() => {
          const selectors = ["article", "main", "[role='main']"];
          for (const selector of selectors) {
            const node = document.querySelector(selector);
            if (node && node.innerText && node.innerText.trim()) return node.innerText;
          }
          return document.body ? document.body.innerText : "";
        })()
        """#,
    ]
    return try jsResult(snippets[mode] ?? snippets["article"]!, target: target)
}

func interactiveItems(limit: Int, target: SafariTabTarget? = nil) throws -> [[String: Any]] {
    let code = #"""
    (() => {
      const selector = 'a, button, input, textarea, select, summary, [role="button"], [onclick]';
      const nodes = Array.from(document.querySelectorAll(selector)).slice(0, \#(limit));
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const attrSelector = (tag, attr, value) => `${tag}[${attr}="${String(value).replace(/"/g, '\\"')}"]`;
      const selectorFor = (el) => {
        const tag = el.tagName.toLowerCase();
        const dataAttrs = ['data-testid', 'data-test', 'data-qa', 'data-cy'];
        for (const attr of dataAttrs) {
          const value = el.getAttribute(attr);
          if (value) return attrSelector(tag, attr, value);
        }
        const aria = el.getAttribute('aria-label');
        if (aria) return attrSelector(tag, 'aria-label', aria);
        if (el.name) return attrSelector(tag, 'name', el.name);
        if (el.id) return `#${cssEscape(el.id)}`;
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return attrSelector(tag, 'placeholder', placeholder);
        const role = el.getAttribute('role');
        if (role) return attrSelector(tag, 'role', role);
        if (tag === 'a') {
          const href = el.getAttribute('href');
          if (href) return attrSelector(tag, 'href', href);
        }
        const type = el.getAttribute('type');
        if (type) return attrSelector(tag, 'type', type);
        return tag;
      };
      return JSON.stringify(nodes.map((el, index) => ({
        index: index + 1,
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type') || '',
        text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200),
        id: el.id || '',
        name: el.getAttribute('name') || '',
        href: el.href || '',
        suggested_selector: selectorFor(el),
        selector_source: (() => {
          const s = selectorFor(el);
          if (s.startsWith('#')) return 'id';
          if (s.includes('[data-testid=')) return 'data-testid';
          if (s.includes('[data-test=')) return 'data-test';
          if (s.includes('[data-qa=')) return 'data-qa';
          if (s.includes('[data-cy=')) return 'data-cy';
          if (s.includes('[aria-label=')) return 'aria-label';
          if (s.includes('[name=')) return 'name';
          if (s.includes('[placeholder=')) return 'placeholder';
          if (s.includes('[role=')) return 'role';
          if (s.includes('[href=')) return 'href';
          if (s.includes('[type=')) return 'type';
          return 'tag';
        })()
      })));
    })()
    """#
    return parseJSON(try jsResult(code, target: target), default: []) as? [[String: Any]] ?? []
}

func querySelector(selector: String, limit: Int, target: SafariTabTarget? = nil) throws -> [[String: Any]] {
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const nodes = Array.from(document.querySelectorAll(\#(selectorLiteral))).slice(0, \#(limit));
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const attrSelector = (tag, attr, value) => `${tag}[${attr}="${String(value).replace(/"/g, '\\"')}"]`;
      const selectorFor = (el) => {
        const tag = el.tagName.toLowerCase();
        const dataAttrs = ['data-testid', 'data-test', 'data-qa', 'data-cy'];
        for (const attr of dataAttrs) {
          const value = el.getAttribute(attr);
          if (value) return attrSelector(tag, attr, value);
        }
        const aria = el.getAttribute('aria-label');
        if (aria) return attrSelector(tag, 'aria-label', aria);
        if (el.name) return attrSelector(tag, 'name', el.name);
        if (el.id) return `#${cssEscape(el.id)}`;
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return attrSelector(tag, 'placeholder', placeholder);
        const role = el.getAttribute('role');
        if (role) return attrSelector(tag, 'role', role);
        if (tag === 'a') {
          const href = el.getAttribute('href');
          if (href) return attrSelector(tag, 'href', href);
        }
        const type = el.getAttribute('type');
        if (type) return attrSelector(tag, 'type', type);
        return tag;
      };
      return JSON.stringify(nodes.map((el, index) => ({
        index: index + 1,
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        classes: typeof el.className === 'string' ? el.className : '',
        name: el.getAttribute('name') || '',
        type: el.getAttribute('type') || '',
        text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200),
        href: el.href || '',
        value: 'value' in el ? String(el.value).slice(0, 200) : '',
        suggested_selector: selectorFor(el),
        selector_source: (() => {
          const s = selectorFor(el);
          if (s.startsWith('#')) return 'id';
          if (s.includes('[data-testid=')) return 'data-testid';
          if (s.includes('[data-test=')) return 'data-test';
          if (s.includes('[data-qa=')) return 'data-qa';
          if (s.includes('[data-cy=')) return 'data-cy';
          if (s.includes('[aria-label=')) return 'aria-label';
          if (s.includes('[name=')) return 'name';
          if (s.includes('[placeholder=')) return 'placeholder';
          if (s.includes('[role=')) return 'role';
          if (s.includes('[href=')) return 'href';
          if (s.includes('[type=')) return 'type';
          return 'tag';
        })()
      })));
    })()
    """#
    return parseJSON(try jsResult(code, target: target), default: []) as? [[String: Any]] ?? []
}

func pageStructure(
    interactiveLimit: Int,
    headingLimit: Int,
    formLimit: Int,
    fieldLimit: Int,
    target: SafariTabTarget? = nil
) throws -> [String: Any] {
    let code = #"""
    (() => {
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const attrSelector = (tag, attr, value) => `${tag}[${attr}="${String(value).replace(/"/g, '\\"')}"]`;
      const selectorFor = (el) => {
        const tag = el.tagName.toLowerCase();
        const dataAttrs = ['data-testid', 'data-test', 'data-qa', 'data-cy'];
        for (const attr of dataAttrs) {
          const value = el.getAttribute(attr);
          if (value) return attrSelector(tag, attr, value);
        }
        const aria = el.getAttribute('aria-label');
        if (aria) return attrSelector(tag, 'aria-label', aria);
        if (el.name) return attrSelector(tag, 'name', el.name);
        if (el.id) return `#${cssEscape(el.id)}`;
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return attrSelector(tag, 'placeholder', placeholder);
        const role = el.getAttribute('role');
        if (role) return attrSelector(tag, 'role', role);
        if (tag === 'a') {
          const href = el.getAttribute('href');
          if (href) return attrSelector(tag, 'href', href);
        }
        const type = el.getAttribute('type');
        if (type) return attrSelector(tag, 'type', type);
        return tag;
      };
      const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
        .slice(0, \#(headingLimit))
        .map((el) => ({
          level: el.tagName.toLowerCase(),
          text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 200)
        }));
      const interactive = Array.from(document.querySelectorAll('a, button, input, textarea, select, summary, [role="button"], [onclick]'))
        .slice(0, \#(interactiveLimit))
        .map((el, index) => ({
          index: index + 1,
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute('type') || '',
          text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200),
          id: el.id || '',
          name: el.getAttribute('name') || '',
          href: el.href || '',
          suggested_selector: selectorFor(el),
          selector_source: (() => {
            const s = selectorFor(el);
            if (s.startsWith('#')) return 'id';
            if (s.includes('[data-testid=')) return 'data-testid';
            if (s.includes('[data-test=')) return 'data-test';
            if (s.includes('[data-qa=')) return 'data-qa';
            if (s.includes('[data-cy=')) return 'data-cy';
            if (s.includes('[aria-label=')) return 'aria-label';
            if (s.includes('[name=')) return 'name';
            if (s.includes('[placeholder=')) return 'placeholder';
            if (s.includes('[role=')) return 'role';
            if (s.includes('[href=')) return 'href';
            if (s.includes('[type=')) return 'type';
            return 'tag';
          })()
        }));
      const forms = Array.from(document.forms)
        .slice(0, \#(formLimit))
        .map((form, formIndex) => ({
          index: formIndex + 1,
          id: form.id || '',
          name: form.getAttribute('name') || '',
          method: (form.getAttribute('method') || 'get').toLowerCase(),
          action: form.getAttribute('action') || '',
          fields: Array.from(form.querySelectorAll('input, textarea, select, button'))
            .slice(0, \#(fieldLimit))
            .map((el, fieldIndex) => ({
              index: fieldIndex + 1,
              tag: el.tagName.toLowerCase(),
              type: el.getAttribute('type') || '',
              name: el.getAttribute('name') || '',
              id: el.id || '',
              placeholder: el.getAttribute('placeholder') || '',
              text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 120),
              suggested_selector: selectorFor(el),
              selector_source: (() => {
                const s = selectorFor(el);
                if (s.startsWith('#')) return 'id';
                if (s.includes('[data-testid=')) return 'data-testid';
                if (s.includes('[data-test=')) return 'data-test';
                if (s.includes('[data-qa=')) return 'data-qa';
                if (s.includes('[data-cy=')) return 'data-cy';
                if (s.includes('[aria-label=')) return 'aria-label';
                if (s.includes('[name=')) return 'name';
                if (s.includes('[placeholder=')) return 'placeholder';
                if (s.includes('[role=')) return 'role';
                if (s.includes('[href=')) return 'href';
                if (s.includes('[type=')) return 'type';
                return 'tag';
              })()
            }))
        }));
      return JSON.stringify({
        meta: {
          title: document.title,
          url: location.href,
          ready_state: document.readyState,
          form_count: document.forms.length,
          link_count: document.links.length,
          interactive_count: document.querySelectorAll('a, button, input, textarea, select, summary, [role="button"], [onclick]').length,
          selected_text: window.getSelection ? window.getSelection().toString().slice(0, 200) : ''
        },
        headings,
        forms,
        interactive
      });
    })()
    """#
    return parseJSON(try jsResult(code, target: target), default: [:]) as? [String: Any] ?? [:]
}

func buildSnapshotPayload(
    limit: Int,
    mode: String,
    textChars: Int,
    headingLimit: Int,
    formLimit: Int,
    fieldLimit: Int,
    interactiveOnly: Bool,
    target: SafariTabTarget? = nil
) throws -> [String: Any] {
    let structure = try pageStructure(
        interactiveLimit: limit,
        headingLimit: headingLimit,
        formLimit: formLimit,
        fieldLimit: fieldLimit,
        target: target
    )
    var payload: [String: Any] = [
        "current": try currentTab(target: target),
        "meta": structure["meta"] ?? [:],
        "interactive": structure["interactive"] ?? [],
    ]
    if !interactiveOnly {
        payload["headings"] = structure["headings"] ?? []
        payload["forms"] = structure["forms"] ?? []
        let text = try getTextForMode(mode, target: target)
        payload["text"] = String(text.prefix(textChars))
    }
    return payload
}

// MARK: - Native Menu / Input Helpers

func menuItemSpec(_ path: [String]) throws -> String {
    guard !path.isEmpty else {
        throw SafariControlError(message: "Menu path cannot be empty.")
    }
    if path.count == 1 {
        return #"menu bar item "\#(escapeAppleScript(path[0]))" of menu bar 1"#
    }
    var spec = #"menu 1 of menu bar item "\#(escapeAppleScript(path[0]))" of menu bar 1"#
    for segment in path.dropFirst().dropLast() {
        spec = #"menu 1 of menu item "\#(escapeAppleScript(segment))" of \#(spec)"#
    }
    return #"menu item "\#(escapeAppleScript(path.last!))" of \#(spec)"#
}

func nativeSearchFieldIdentifier() -> String {
    "WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD"
}

func sendSystemKey(_ keyCode: Int) throws {
    _ = try runOsaScript(
        #"""
        tell application "System Events"
            key code \#(keyCode)
        end tell
        """#
    )
}

func parseShortcut(_ combo: String) throws -> (String, [String]) {
    let parts = combo.split(separator: "+").map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter { !$0.isEmpty }
    guard let key = parts.last else {
        throw SafariControlError(message: "Shortcut cannot be empty.")
    }
    let aliases: [String: String] = [
        "cmd": "command down",
        "command": "command down",
        "meta": "command down",
        "ctrl": "control down",
        "control": "control down",
        "alt": "option down",
        "option": "option down",
        "shift": "shift down",
    ]
    let modifiers = try parts.dropLast().map { part -> String in
        guard let modifier = aliases[part.lowercased()] else {
            throw SafariControlError(message: "Unsupported shortcut modifier: \(part)")
        }
        return modifier
    }
    return (String(key), modifiers)
}

func nativeConfirmSearchField(mode: String) throws -> [String: Any] {
    switch mode {
    case "ax":
        var payload = parseJSON(
            try runAXTool([
                "perform-action",
                nativeSearchFieldIdentifier(),
                "AXConfirm",
                "--field",
                "identifier",
                "--exact",
            ]),
            default: [:]
        ) as? [String: Any] ?? [:]
        payload["confirm_mode"] = "ax"
        return payload
    case "enter":
        try sendSystemKey(36)
        return ["ok": true, "confirm_mode": "enter"]
    case "both":
        var payload = try nativeConfirmSearchField(mode: "ax")
        try sendSystemKey(36)
        payload["confirm_mode"] = "both"
        return payload
    default:
        throw SafariControlError(message: "Unsupported confirm mode: \(mode). Use ax, enter, or both.")
    }
}

func tabMatch(_ tabs: [[String: Any]], key: String, needle: String, exact: Bool, index: Int) throws -> [String: Any] {
    let lowered = needle.lowercased()
    let matches = tabs.filter { tab in
        let value = ((tab[key] as? String) ?? "").lowercased()
        return exact ? value == lowered : value.contains(lowered)
    }
    guard !matches.isEmpty else {
        throw SafariControlError(message: "No Safari tab \(key) matched: \(needle)")
    }
    guard index > 0, index <= matches.count else {
        throw SafariControlError(message: "Only found \(matches.count) \(key) matches, index \(index) is out of range.")
    }
    return matches[index - 1]
}

func waitForCurrentTabChange(from baseline: [String: Any], timeoutMs: Int, intervalMs: Int = 150) throws -> [String: Any] {
    if timeoutMs <= 0 {
        return try currentTab()
    }
    let deadline = Date().timeIntervalSince1970 + Double(timeoutMs) / 1000.0
    var latest = try currentTab()
    while Date().timeIntervalSince1970 < deadline {
        latest = try currentTab()
        if NSDictionary(dictionary: latest).isEqual(to: baseline) == false {
            return latest
        }
        Thread.sleep(forTimeInterval: Double(intervalMs) / 1000.0)
    }
    return latest
}

// MARK: - Session / Native Command Handlers

func cmdActivate() throws {
    _ = try runOsaScript(#"tell application "Safari" to activate"#)
    print("activated")
}

func cmdOpen(_ options: CommandOptions) throws {
    guard let url = options.positionals.first else {
        throw SafariControlError(message: "open requires a URL.")
    }
    _ = try runOsaScript(#"tell application "Safari" to open location "\#(escapeAppleScript(url))""#)
    _ = try runOsaScript(#"tell application "Safari" to activate"#)
    print("opened\t\(url)")
}

func cmdNewTab(_ options: CommandOptions) throws {
    let script: String
    if let url = options.positionals.first {
        script = #"""
        tell application "Safari"
            activate
            if (count of windows) = 0 then
                make new document with properties {URL:"\#(escapeAppleScript(url))"}
            else
                tell front window
                    set current tab to (make new tab with properties {URL:"\#(escapeAppleScript(url))"})
                end tell
            end if
        end tell
        """#
    } else {
        script = #"""
        tell application "Safari"
            activate
            if (count of windows) = 0 then
                make new document
            else
                tell front window
                    set current tab to (make new tab)
                end tell
            end if
        end tell
        """#
    }
    _ = try runOsaScript(script)
    print("new-tab")
}

func cmdDuplicateTab() throws {
    let tab = try currentTab()
    guard let url = tab["url"] as? String, !url.isEmpty else {
        throw SafariControlError(message: "Safari has no current tab URL to duplicate.")
    }
    _ = try runOsaScript(
        #"""
        tell application "Safari"
            activate
            if (count of windows) = 0 then
                make new document with properties {URL:"\#(escapeAppleScript(url))"}
            else
                tell front window
                    set current tab to (make new tab with properties {URL:"\#(escapeAppleScript(url))"})
                end tell
            end if
        end tell
        """#
    )
    try printJSON(["ok": true, "source": tab, "current": try currentTab()])
}

func cmdCurrent(_ options: CommandOptions) throws {
    let data = try currentTab(target: try options.tabTarget())
    if options.flag("--json") {
        try printJSON(data)
    } else if !data.isEmpty {
        print("\((data["title"] as? String) ?? "")\t\((data["url"] as? String) ?? "")")
    }
}

func cmdListMenuBar(_ options: CommandOptions) throws {
    let output = try runOsaScript(
        #"""
        tell application "Safari" to activate
        delay 0.2
        tell application "System Events"
            tell process "Safari"
                return name of every menu bar item of menu bar 1
            end tell
        end tell
        """#
    )
    let items = output.split(separator: ",").map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter { !$0.isEmpty }
    if options.flag("--json") {
        try printJSON(items)
    } else {
        items.forEach { print($0) }
    }
}

func cmdListMenuItems(_ options: CommandOptions) throws {
    guard !options.positionals.isEmpty else {
        throw SafariControlError(message: "list-menu-items requires at least one menu path segment.")
    }
    let spec = try menuItemSpec(options.positionals)
    let output = try runOsaScript(
        #"""
        tell application "Safari" to activate
        delay 0.2
        tell application "System Events"
            tell process "Safari"
                return name of every menu item of menu 1 of \#(spec)
            end tell
        end tell
        """#
    )
    let items = output.split(separator: ",").map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter {
        !$0.isEmpty && $0 != "missing value"
    }
    if options.flag("--json") {
        try printJSON(items)
    } else {
        items.forEach { print($0) }
    }
}

func cmdClickMenu(_ options: CommandOptions) throws {
    let spec = try menuItemSpec(options.positionals)
    _ = try runOsaScript(
        #"""
        tell application "Safari" to activate
        delay 0.2
        tell application "System Events"
            tell process "Safari"
                click \#(spec)
            end tell
        end tell
        """#
    )
    try printJSON(["ok": true, "path": options.positionals])
}

func cmdListNativeControls(_ options: CommandOptions) throws {
    var args = ["list-controls"]
    if options.flag("--include-web") { args.append("--include-web") }
    if options.flag("--all") { args.append("--all") }
    let controls = parseJSON(try runAXTool(args), default: []) as? [[String: Any]] ?? []
    if options.flag("--json") {
        try printJSON(controls)
    } else {
        for item in controls {
            let identifier = item["identifier"] as? String ?? ""
            let title = item["title"] as? String ?? ""
            let description = item["description"] as? String ?? ""
            let value = item["value"] as? String ?? ""
            let label: String
            if !identifier.isEmpty {
                label = identifier
            } else if !title.isEmpty {
                label = title
            } else if !description.isEmpty {
                label = description
            } else {
                label = value
            }
            print("\((item["index"] as? Int) ?? 0)\t\((item["role"] as? String) ?? "")\t\(label)")
        }
    }
}

func nativeControlArgs(baseCommand: String, options: CommandOptions, extra: [String] = []) throws -> [String] {
    guard let query = options.positionals.first else {
        throw SafariControlError(message: "\(baseCommand) requires a query.")
    }
    var args = [baseCommand, query]
    args.append(contentsOf: extra)
    if options.flag("--exact") { args.append("--exact") }
    args.append("--field")
    args.append(options.string("--field") ?? "any")
    args.append("--index")
    args.append(String(try options.int("--index") ?? 1))
    if options.flag("--include-web") { args.append("--include-web") }
    return args
}

func cmdPressNativeControl(_ options: CommandOptions) throws {
    let payload = parseJSON(try runAXTool(try nativeControlArgs(baseCommand: "press-control", options: options)), default: [:])
    try printJSON(payload)
}

func cmdFocusNativeControl(_ options: CommandOptions) throws {
    let payload = parseJSON(try runAXTool(try nativeControlArgs(baseCommand: "focus-control", options: options)), default: [:])
    try printJSON(payload)
}

func cmdPerformNativeAction(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "perform-native-action requires a query and action.")
    }
    let query = options.positionals[0]
    let action = options.positionals[1]
    var args = ["perform-action", query, action]
    if options.flag("--exact") { args.append("--exact") }
    args += ["--field", options.string("--field") ?? "any", "--index", String(try options.int("--index") ?? 1)]
    if options.flag("--include-web") { args.append("--include-web") }
    let payload = parseJSON(try runAXTool(args), default: [:])
    try printJSON(payload)
}

func cmdSetNativeValue(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "set-native-value requires a query and value.")
    }
    let query = options.positionals[0]
    let value = options.positionals[1]
    var args = ["set-value", query, value]
    if options.flag("--exact") { args.append("--exact") }
    args += ["--field", options.string("--field") ?? "any", "--index", String(try options.int("--index") ?? 1)]
    if options.flag("--include-web") { args.append("--include-web") }
    let payload = parseJSON(try runAXTool(args), default: [:])
    try printJSON(payload)
}

func cmdListNativeMenuItems(_ options: CommandOptions) throws {
    var args = try nativeControlArgs(baseCommand: "list-menu-items", options: options)
    args += ["--timeout-ms", String(try options.int("--timeout-ms") ?? 1500)]
    let payload = parseJSON(try runAXTool(args), default: [:]) as? [String: Any] ?? [:]
    if options.flag("--json") {
        try printJSON(payload)
    } else {
        let items = payload["items"] as? [[String: Any]] ?? []
        for item in items {
            let path = item["path"] as? [String] ?? []
            print(path.joined(separator: " > "))
        }
    }
}

func cmdClickNativeMenuItem(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "click-native-menu-item requires a query and at least one menu path segment.")
    }
    let query = options.positionals[0]
    let path = Array(options.positionals.dropFirst())
    var args = ["pick-menu-item", query] + path
    if options.flag("--exact") { args.append("--exact") }
    args += [
        "--field", options.string("--field") ?? "any",
        "--index", String(try options.int("--index") ?? 1),
        "--timeout-ms", String(try options.int("--timeout-ms") ?? 1500),
        "--item-field", options.string("--item-field") ?? "any",
    ]
    if options.flag("--item-contains") { args.append("--item-contains") }
    if options.flag("--include-web") { args.append("--include-web") }
    let payload = parseJSON(try runAXTool(args), default: [:])
    try printJSON(payload)
}

func cmdPressSystemKey(_ options: CommandOptions) throws {
    guard let key = options.positionals.first else {
        throw SafariControlError(message: "press-system-key requires a key.")
    }
    var keyCode: Int? = nil
    if key.count == 1 {
        _ = try runOsaScript(
            #"""
            tell application "System Events"
                keystroke "\#(escapeAppleScript(key))"
            end tell
            """#
        )
    } else {
        let aliases: [String: Int] = [
            "enter": 36,
            "return": 36,
            "tab": 48,
            "space": 49,
            "escape": 53,
            "esc": 53,
            "left": 123,
            "right": 124,
            "down": 125,
            "up": 126,
            "delete": 51,
            "forwarddelete": 117,
        ]
        guard let resolved = aliases[key.lowercased()] else {
            throw SafariControlError(message: "Unsupported system key: \(key)")
        }
        keyCode = resolved
        try sendSystemKey(resolved)
    }
    try printJSON(["ok": true, "key": key, "key_code": keyCode as Any])
}

func cmdPressSystemShortcut(_ options: CommandOptions) throws {
    guard let combo = options.positionals.first else {
        throw SafariControlError(message: "press-system-shortcut requires a combo.")
    }
    let (key, modifiers) = try parseShortcut(combo)
    let mods = modifiers.joined(separator: ", ")
    _ = try runOsaScript(
        #"""
        tell application "System Events"
            keystroke "\#(escapeAppleScript(key))" using {\#(mods)}
        end tell
        """#
    )
    try printJSON(["ok": true, "combo": combo])
}

func cmdNativeOpenURL(_ options: CommandOptions) throws {
    guard var value = options.positionals.first else {
        throw SafariControlError(message: "native-open-url requires a URL.")
    }
    let before = try currentTab()
    if !value.contains("://") && !value.hasPrefix("about:") && !value.hasPrefix("file:") && !value.hasPrefix("data:") {
        value = "https://\(value)"
    }
    let confirmMode = (options.string("--confirm-mode") ?? "ax").lowercased()
    _ = try runAXTool([
        "set-value",
        nativeSearchFieldIdentifier(),
        value,
        "--field",
        "identifier",
        "--exact",
    ])
    var result = try nativeConfirmSearchField(mode: confirmMode)
    result["submitted_value"] = value
    result["current"] = try waitForCurrentTabChange(
        from: before,
        timeoutMs: try options.int("--wait-ms") ?? 1500
    )
    try printJSON(result)
}

func cmdNativeSearch(_ options: CommandOptions) throws {
    guard let query = options.positionals.first else {
        throw SafariControlError(message: "native-search requires a query.")
    }
    let before = try currentTab()
    let confirmMode = (options.string("--confirm-mode") ?? "ax").lowercased()
    _ = try runAXTool([
        "set-value",
        nativeSearchFieldIdentifier(),
        query,
        "--field",
        "identifier",
        "--exact",
    ])
    var payload = try nativeConfirmSearchField(mode: confirmMode)
    payload["submitted_value"] = query
    payload["current"] = try waitForCurrentTabChange(
        from: before,
        timeoutMs: try options.int("--wait-ms") ?? 1500
    )
    try printJSON(payload)
}

func cmdNewWindow(_ options: CommandOptions) throws {
    let script: String
    if let url = options.positionals.first {
        script = #"""
        tell application "Safari"
            activate
            make new document with properties {URL:"\#(escapeAppleScript(url))"}
        end tell
        """#
    } else {
        script = #"""
        tell application "Safari"
            activate
            make new document
        end tell
        """#
    }
    _ = try runOsaScript(script)
    let windows = try allWindows()
    try printJSON(windows.first ?? [:])
}

func cmdListWindows(_ options: CommandOptions) throws {
    let windows = try allWindows()
    if options.flag("--json") {
        try printJSON(windows)
    } else {
        for window in windows {
            let marker = (window["front"] as? Bool) == true ? "*" : "-"
            print("\(marker)\twindow=\((window["window"] as? Int) ?? 0)\ttabs=\((window["tab_count"] as? Int) ?? 0)\tcurrent_tab=\((window["current_tab"] as? Int) ?? 0)\t\((window["title"] as? String) ?? "")\t\((window["url"] as? String) ?? "")")
        }
    }
}

func cmdSwitchWindow(_ options: CommandOptions) throws {
    guard let window = Int(options.positionals.first ?? "") else {
        throw SafariControlError(message: "switch-window requires a numeric window.")
    }
    _ = try runOsaScript(
        #"""
        tell application "Safari"
            if (count of windows) < \#(window) then
                error "Safari window \#(window) does not exist."
            end if
            set index of window \#(window) to 1
            activate
        end tell
        """#
    )
    let windows = try allWindows()
    try printJSON(windows.first ?? [:])
}

func cmdCloseWindow(_ options: CommandOptions) throws {
    let window = try options.int("--window") ?? 1
    _ = try runOsaScript(
        #"""
        tell application "Safari"
            if (count of windows) < \#(window) then
                error "Safari window \#(window) does not exist."
            end if
            close window \#(window)
        end tell
        """#
    )
    print("closed-window")
}

func cmdSaveSession(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "save-session requires a path.")
    }
    let snapshot = try buildSessionSnapshot(frontOnly: options.flag("--front-only"), window: try options.int("--window"))
    let url = try writeJSONOutput(path: path, value: snapshot)
    try printJSON([
        "ok": true,
        "path": url.path,
        "bytes": fileSize(url),
        "window_count": snapshot["window_count"] as? Int ?? 0,
    ])
}

func cmdRestoreSession(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "restore-session requires a path.")
    }
    let url = URL(fileURLWithPath: expandPath(path))
    let data = try Data(contentsOf: url)
    let snapshot = try JSONSerialization.jsonObject(with: data) as? [String: Any] ?? [:]
    guard let windows = snapshot["windows"] as? [[String: Any]], !windows.isEmpty else {
        throw SafariControlError(message: "Session snapshot does not contain any windows.")
    }

    // Recreate windows back-to-front so the saved front window ends up in front again.
    for windowSnapshot in windows.reversed() {
        let tabs = windowSnapshot["tabs"] as? [[String: Any]] ?? []
        let firstURL = (tabs.first?["url"] as? String) ?? ""
        let script: String
        if !firstURL.isEmpty {
            script = #"""
            tell application "Safari"
                activate
                make new document with properties {URL:"\#(escapeAppleScript(firstURL))"}
            end tell
            """#
        } else {
            script = #"""
            tell application "Safari"
                activate
                make new document
            end tell
            """#
        }
        _ = try runOsaScript(script)
        for tab in tabs.dropFirst() {
            let url = (tab["url"] as? String) ?? ""
            if url.isEmpty { continue }
            _ = try runOsaScript(
                #"""
                tell application "Safari"
                    tell front window
                        set current tab to (make new tab with properties {URL:"\#(escapeAppleScript(url))"})
                    end tell
                end tell
                """#
            )
        }
        let currentTabIndex = windowSnapshot["current_tab"] as? Int ?? 1
        _ = try runOsaScript(
            #"""
            tell application "Safari"
                tell front window
                    if (count of tabs) >= \#(currentTabIndex) then
                        set current tab to tab \#(currentTabIndex)
                    end if
                end tell
            end tell
            """#
        )
    }

    try printJSON([
        "ok": true,
        "path": url.path,
        "window_count": windows.count,
        "created_windows": windows.count,
    ])
}

func cmdSwitchTab(_ options: CommandOptions) throws {
    guard let tab = Int(options.positionals.first ?? "") else {
        throw SafariControlError(message: "switch-tab requires a numeric tab.")
    }
    let window = try options.int("--window") ?? 1
    _ = try runOsaScript(
        #"""
        tell application "Safari"
            if (count of windows) < \#(window) then
                error "Safari window \#(window) does not exist."
            end if
            tell window \#(window)
                if (count of tabs) < \#(tab) then
                    error "Safari tab \#(tab) does not exist in window \#(window)."
                end if
                set current tab to tab \#(tab)
            end tell
            activate
        end tell
        """#
    )
    try printJSON(try currentTab())
}

func cmdCloseTab(_ options: CommandOptions) throws {
    let window = try options.int("--window") ?? 1
    let script: String
    if let tab = try options.int("--tab") {
        script = #"""
        tell application "Safari"
            if (count of windows) < \#(window) then
                error "Safari window \#(window) does not exist."
            end if
            tell window \#(window)
                if (count of tabs) < \#(tab) then
                    error "Safari tab \#(tab) does not exist in window \#(window)."
                end if
                close tab \#(tab)
            end tell
        end tell
        """#
    } else {
        script = #"""
        tell application "Safari"
            if (count of windows) < \#(window) then
                error "Safari window \#(window) does not exist."
            end if
            tell window \#(window)
                close current tab
            end tell
        end tell
        """#
    }
    _ = try runOsaScript(script)
    print("closed")
}

func cmdListTabs(_ options: CommandOptions) throws {
    let tabs = try allTabs()
    if options.flag("--json") {
        try printJSON(tabs)
    } else {
        for tab in tabs {
            let marker = (tab["current"] as? Bool) == true ? "*" : "-"
            print("\(marker)\twindow=\((tab["window"] as? Int) ?? 0)\ttab=\((tab["tab"] as? Int) ?? 0)\t\((tab["title"] as? String) ?? "")\t\((tab["url"] as? String) ?? "")")
        }
    }
}

func cmdSwitchTabTitle(_ options: CommandOptions) throws {
    guard let title = options.positionals.first else {
        throw SafariControlError(message: "switch-tab-title requires a title.")
    }
    let target = try tabMatch(try allTabs(), key: "title", needle: title, exact: options.flag("--exact"), index: try options.int("--index") ?? 1)
    let window = target["window"] as? Int ?? 1
    let tab = target["tab"] as? Int ?? 1
    _ = try runOsaScript(
        #"""
        tell application "Safari"
            tell window \#(window)
                set current tab to tab \#(tab)
            end tell
            activate
        end tell
        """#
    )
    try printJSON(try currentTab())
}

func cmdSwitchTabURL(_ options: CommandOptions) throws {
    guard let url = options.positionals.first else {
        throw SafariControlError(message: "switch-tab-url requires a URL fragment.")
    }
    let target = try tabMatch(try allTabs(), key: "url", needle: url, exact: options.flag("--exact"), index: try options.int("--index") ?? 1)
    let window = target["window"] as? Int ?? 1
    let tab = target["tab"] as? Int ?? 1
    _ = try runOsaScript(
        #"""
        tell application "Safari"
            tell window \#(window)
                set current tab to tab \#(tab)
            end tell
            activate
        end tell
        """#
    )
    try printJSON(try currentTab())
}

// MARK: - Page / DOM Command Handlers

func cmdCheckJS() throws {
    do {
        _ = try jsResult("document.title")
        print("enabled")
    } catch let error as SafariControlError where error.message == jsPermissionHint {
        print("disabled")
        fputs("\(jsPermissionHint)\n", stderr)
        Foundation.exit(2)
    }
}

func cmdRunJS(_ options: CommandOptions) throws {
    guard let code = options.positionals.first else {
        throw SafariControlError(message: "run-js requires code.")
    }
    print(try jsResult(code, target: try options.tabTarget()))
}

func cmdEvalJS(_ options: CommandOptions) throws {
    guard let expression = options.positionals.first else {
        throw SafariControlError(message: "eval-js requires an expression.")
    }
    let limit = try options.int("--limit") ?? 20
    let keyLimit = try options.int("--key-limit") ?? 50
    let expressionLiteral = try jsonStringLiteral(expression)
    let code = #"""
    (() => {
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const attrSelector = (tag, attr, value) => `${tag}[${attr}="${String(value).replace(/"/g, '\\"')}"]`;
      const selectorFor = (el) => {
        const tag = el.tagName.toLowerCase();
        const dataAttrs = ['data-testid', 'data-test', 'data-qa', 'data-cy'];
        for (const attr of dataAttrs) {
          const value = el.getAttribute(attr);
          if (value) return attrSelector(tag, attr, value);
        }
        const aria = el.getAttribute('aria-label');
        if (aria) return attrSelector(tag, 'aria-label', aria);
        if (el.name) return attrSelector(tag, 'name', el.name);
        if (el.id) return `#${cssEscape(el.id)}`;
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return attrSelector(tag, 'placeholder', placeholder);
        const role = el.getAttribute('role');
        if (role) return attrSelector(tag, 'role', role);
        if (tag === 'a') {
          const href = el.getAttribute('href');
          if (href) return attrSelector(tag, 'href', href);
        }
        const type = el.getAttribute('type');
        if (type) return attrSelector(tag, 'type', type);
        return tag;
      };
      const normalize = (value, depth = 0) => {
        if (depth > 3) return '[max-depth]';
        if (value === undefined) return null;
        if (value === null) return null;
        const valueType = typeof value;
        if (valueType === 'string' || valueType === 'number' || valueType === 'boolean') return value;
        if (value instanceof Element) {
          return {
            tag: value.tagName.toLowerCase(),
            id: value.id || '',
            name: value.getAttribute('name') || '',
            text: (value.innerText || value.textContent || value.value || '').replace(/\s+/g, ' ').trim().slice(0, 200),
            value: 'value' in value ? String(value.value).slice(0, 200) : '',
            href: value.href || '',
            suggested_selector: selectorFor(value)
          };
        }
        if (value instanceof DOMRect) {
          return {
            x: value.x,
            y: value.y,
            width: value.width,
            height: value.height,
            top: value.top,
            left: value.left,
            right: value.right,
            bottom: value.bottom
          };
        }
        if (Array.isArray(value) || value instanceof NodeList || value instanceof HTMLCollection) {
          return Array.from(value).slice(0, \#(limit)).map((item) => normalize(item, depth + 1));
        }
        if (valueType === 'object') {
          const out = {};
          for (const [key, item] of Object.entries(value).slice(0, \#(keyLimit))) {
            out[key] = normalize(item, depth + 1);
          }
          return out;
        }
        return String(value);
      };
      try {
        const value = eval(\#(expressionLiteral));
        return JSON.stringify({ ok: true, value: normalize(value) });
      } catch (error) {
        return JSON.stringify({ ok: false, error: String(error) });
      }
    })()
    """#
    let target = try options.tabTarget()
    let result = parseJSON(try jsResult(code, target: target), default: [:]) as? [String: Any] ?? [:]
    if (result["ok"] as? Bool) != true {
        throw SafariControlError(message: result["error"] as? String ?? "JavaScript evaluation failed.")
    }
    let value = result["value"] ?? NSNull()
    if let path = options.string("--path") {
        let url = try writeJSONOutput(path: path, value: value)
        try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url)])
    } else {
        try printJSON(value)
    }
}

func cmdGetText(_ options: CommandOptions) throws {
    let mode = options.string("--mode") ?? "article"
    print(try getTextForMode(mode, target: try options.tabTarget()))
}

func cmdSaveHTML(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "save-html requires a path.")
    }
    let url = try writeOutput(path: path, content: try currentTabSource(target: try options.tabTarget()))
    try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url)])
}

func cmdSaveText(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "save-text requires a path.")
    }
    let mode = options.string("--mode") ?? "article"
    let url = try writeOutput(path: path, content: try getTextForMode(mode, target: try options.tabTarget()))
    try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url), "mode": mode])
}

func cmdInteractive(_ options: CommandOptions) throws {
    let limit = try options.int("--limit") ?? 40
    let result = try interactiveItems(limit: limit, target: try options.tabTarget())
    if options.flag("--json") {
        try printJSON(result)
    } else {
        for item in result {
            print("\((item["index"] as? Int) ?? 0)\t\((item["tag"] as? String) ?? "")\t\((item["suggested_selector"] as? String) ?? "")\t\(((item["text"] as? String)?.isEmpty == false ? (item["text"] as? String)! : (item["href"] as? String) ?? ""))")
        }
    }
}

func cmdQuery(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "query requires a selector.")
    }
    let limit = try options.int("--limit") ?? 20
    let result = try querySelector(selector: selector, limit: limit, target: try options.tabTarget())
    if options.flag("--json") {
        try printJSON(result)
    } else {
        for item in result {
            let text = (item["text"] as? String).flatMap { !$0.isEmpty ? $0 : nil }
                ?? (item["value"] as? String).flatMap { !$0.isEmpty ? $0 : nil }
                ?? (item["href"] as? String) ?? ""
            print("\((item["index"] as? Int) ?? 0)\t\((item["tag"] as? String) ?? "")\t\((item["id"] as? String) ?? "")\t\(text)")
        }
    }
}

func cmdExists(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "exists requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({exists: false, visible: false});
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      const visible = !!(rect.width || rect.height || el.getClientRects().length) &&
        style.visibility !== 'hidden' &&
        style.display !== 'none';
      return JSON.stringify({exists: true, visible});
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdCount(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "count requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"(() => document.querySelectorAll(\#(selectorLiteral)).length)()"#
    print(Int((Double(try jsResult(code, target: try options.tabTarget())) ?? 0.0)))
}

func cmdSnapshot(_ options: CommandOptions) throws {
    let payload = try buildSnapshotPayload(
        limit: try options.int("--limit") ?? 20,
        mode: options.string("--mode") ?? "article",
        textChars: try options.int("--text-chars") ?? 2000,
        headingLimit: try options.int("--heading-limit") ?? 10,
        formLimit: try options.int("--form-limit") ?? 5,
        fieldLimit: try options.int("--field-limit") ?? 12,
        interactiveOnly: options.flag("--interactive-only"),
        target: try options.tabTarget()
    )
    try printJSON(payload)
}

func cmdSaveSnapshot(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "save-snapshot requires a path.")
    }
    let payload = try buildSnapshotPayload(
        limit: try options.int("--limit") ?? 20,
        mode: options.string("--mode") ?? "article",
        textChars: try options.int("--text-chars") ?? 2000,
        headingLimit: try options.int("--heading-limit") ?? 10,
        formLimit: try options.int("--form-limit") ?? 5,
        fieldLimit: try options.int("--field-limit") ?? 12,
        interactiveOnly: options.flag("--interactive-only"),
        target: try options.tabTarget()
    )
    let url = try writeJSONOutput(path: path, value: payload)
    try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url)])
}

func cmdSnapshotWithScreenshot(_ options: CommandOptions) throws {
    guard let screenshotPathArg = options.positionals.first else {
        throw SafariControlError(message: "snapshot-with-screenshot requires a screenshot path.")
    }
    let payload = try buildSnapshotPayload(
        limit: try options.int("--limit") ?? 20,
        mode: options.string("--mode") ?? "article",
        textChars: try options.int("--text-chars") ?? 2000,
        headingLimit: try options.int("--heading-limit") ?? 10,
        formLimit: try options.int("--form-limit") ?? 5,
        fieldLimit: try options.int("--field-limit") ?? 12,
        interactiveOnly: options.flag("--interactive-only"),
        target: try options.tabTarget()
    )
    let screenshotPath = URL(fileURLWithPath: expandPath(screenshotPathArg))
    try FileManager.default.createDirectory(at: screenshotPath.deletingLastPathComponent(), withIntermediateDirectories: true)
    let screenshot = try captureScreenshot(
        path: screenshotPath,
        mode: (options.string("--screenshot-mode") ?? "auto").lowercased(),
        restorePreviousApp: !options.flag("--no-restore")
    )

    var combined = payload
    combined["screenshot"] = screenshot

    if let jsonPath = options.string("--path") {
        let url = try writeJSONOutput(path: jsonPath, value: combined)
        try printJSON([
            "ok": true,
            "path": url.path,
            "bytes": fileSize(url),
            "screenshot_path": screenshot["path"] ?? screenshotPath.path,
        ])
    } else {
        try printJSON(combined)
    }
}

func cmdSavePageBundle(_ options: CommandOptions) throws {
    guard let dirArg = options.positionals.first else {
        throw SafariControlError(message: "save-page-bundle requires a target directory.")
    }
    let dir = URL(fileURLWithPath: expandPath(dirArg), isDirectory: true)
    try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)

    let mode = options.string("--mode") ?? "article"
    let target = try options.tabTarget()
    let snapshot = try buildSnapshotPayload(
        limit: try options.int("--limit") ?? 20,
        mode: mode,
        textChars: try options.int("--text-chars") ?? 2000,
        headingLimit: try options.int("--heading-limit") ?? 10,
        formLimit: try options.int("--form-limit") ?? 5,
        fieldLimit: try options.int("--field-limit") ?? 12,
        interactiveOnly: options.flag("--interactive-only"),
        target: target
    )
    let html = try currentTabSource(target: target)
    let text = try getTextForMode(mode, target: target)
    let links = try extractLinksData(
        selector: options.string("--links-selector") ?? "a",
        limit: try options.int("--links-limit") ?? 100,
        target: target
    )
    let tables = try extractTablesData(
        selector: options.string("--tables-selector") ?? "table",
        limit: try options.int("--tables-limit") ?? 20,
        rowLimit: try options.int("--row-limit") ?? 20,
        target: target
    )
    let screenshot = try captureScreenshot(
        path: dir.appendingPathComponent("screenshot.png"),
        mode: (options.string("--screenshot-mode") ?? "auto").lowercased(),
        restorePreviousApp: !options.flag("--no-restore")
    )

    let htmlURL = try writeOutput(path: dir.appendingPathComponent("page.html").path, content: html)
    let textURL = try writeOutput(path: dir.appendingPathComponent("page.txt").path, content: text)
    let linksURL = try writeJSONOutput(path: dir.appendingPathComponent("links.json").path, value: links)
    let tablesURL = try writeJSONOutput(path: dir.appendingPathComponent("tables.json").path, value: tables)
    let snapshotURL = try writeJSONOutput(path: dir.appendingPathComponent("snapshot.json").path, value: snapshot)

    let manifest: [String: Any] = [
        "ok": true,
        "tool": "safari-control",
        "version": toolVersion,
        "implementation": "swift",
        "created_at": Int(Date().timeIntervalSince1970),
        "current": snapshot["current"] ?? [:],
        "meta": snapshot["meta"] ?? [:],
        "files": [
            "html": ["path": htmlURL.path, "bytes": fileSize(htmlURL)],
            "text": ["path": textURL.path, "bytes": fileSize(textURL), "mode": mode],
            "links": ["path": linksURL.path, "bytes": fileSize(linksURL), "count": links.count],
            "tables": ["path": tablesURL.path, "bytes": fileSize(tablesURL), "count": tables.count],
            "snapshot": ["path": snapshotURL.path, "bytes": fileSize(snapshotURL)],
            "screenshot": screenshot,
        ],
    ]
    let manifestURL = try writeJSONOutput(path: dir.appendingPathComponent("manifest.json").path, value: manifest)
    var payload: [String: Any] = [
        "ok": true,
        "dir": dir.path,
        "manifest": manifestURL.path,
        "files": manifest["files"] ?? [:],
    ]
    if options.flag("--zip") || options.string("--zip-path") != nil {
        let zipPath = options.string("--zip-path")
            .map { URL(fileURLWithPath: expandPath($0)) }
            ?? dir.deletingLastPathComponent().appendingPathComponent("\(dir.lastPathComponent).zip")
        payload["zip"] = try createZipArchive(item: dir, output: zipPath)
    }
    try printJSON(payload)
}

func cmdVersion() throws {
    let helper = resolveAXTool()
    var payload: [String: Any] = [
        "tool": "safari-control",
        "version": toolVersion,
        "implementation": "swift",
        "entrypoint": CommandLine.arguments.first ?? "",
        "runtime_mode": CommandLine.arguments.first?.hasSuffix(".swift") == true ? "script" : "binary",
        "ax_helper_executable": helper.0,
        "ax_helper_arguments": helper.1,
        "environment": environmentMetadata(),
    ]
    if let git = gitMetadata() {
        payload["git"] = git
    }
    try printJSON(payload)
}

func cmdClick(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "click requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      el.click();
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdFocus(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "focus requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      if (el.scrollIntoView) el.scrollIntoView({ block: 'center', inline: 'nearest' });
      if (typeof el.focus === 'function') el.focus();
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        active: document.activeElement === el,
        selector: \#(selectorLiteral)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdFill(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "fill requires a selector and value.")
    }
    let selectorLiteral = try jsonStringLiteral(options.positionals[0])
    let valueLiteral = try jsonStringLiteral(options.positionals[1])
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      el.focus();
      if (!('value' in el)) return JSON.stringify({ok: false, error: 'element has no value property'});
      const proto = Object.getPrototypeOf(el);
      const descriptor = proto ? Object.getOwnPropertyDescriptor(proto, 'value') : null;
      if (descriptor && typeof descriptor.set === 'function') descriptor.set.call(el, \#(valueLiteral));
      else el.value = \#(valueLiteral);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        value: String(el.value).slice(0, 200)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdWaitJS(_ options: CommandOptions) throws {
    guard let expression = options.positionals.first else {
        throw SafariControlError(message: "wait-js requires an expression.")
    }
    let expressionLiteral = try jsonStringLiteral(expression)
    let target = try options.tabTarget()
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "js \(expression)"
    ) {
        let code = #"""
        (() => {
          try {
            return !!eval(\#(expressionLiteral));
          } catch (error) {
            return false;
          }
        })()
        """#
        return try jsResult(code, target: target).trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == "true"
    }
    print("ready")
}

func cmdWaitText(_ options: CommandOptions) throws {
    guard let text = options.positionals.first else {
        throw SafariControlError(message: "wait-text requires text.")
    }
    let textLiteral = try jsonStringLiteral(text)
    let target = try options.tabTarget()
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "text \(text)"
    ) {
        let code = #"""
        (() => {
          const bodyText = document.body ? document.body.innerText : '';
          return bodyText.includes(\#(textLiteral));
        })()
        """#
        return try jsResult(code, target: target).trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == "true"
    }
    print("ready")
}

func cmdWaitCount(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "wait-count requires a selector and count.")
    }
    let selector = options.positionals[0]
    guard let targetCount = Int(options.positionals[1]) else {
        throw SafariControlError(message: "wait-count requires a numeric count.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let op = options.string("--op") ?? "ge"
    let target = try options.tabTarget()
    func currentCount() throws -> Int {
        let code = #"(() => document.querySelectorAll(\#(selectorLiteral)).length)()"#
        return Int((Double(try jsResult(code, target: target)) ?? 0.0))
    }
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "count(\(selector)) \(op) \(targetCount)"
    ) {
        let count = try currentCount()
        switch op {
        case "eq": return count == targetCount
        case "le": return count <= targetCount
        default: return count >= targetCount
        }
    }
    print(try currentCount())
}

func cmdWaitTitle(_ options: CommandOptions) throws {
    guard let title = options.positionals.first else {
        throw SafariControlError(message: "wait-title requires a title.")
    }
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "title \(title)"
    ) {
        let current = try currentTab(target: try options.tabTarget())["title"] as? String ?? ""
        return options.flag("--exact") ? current == title : current.contains(title)
    }
    try printJSON(try currentTab(target: try options.tabTarget()))
}

func cmdWaitURL(_ options: CommandOptions) throws {
    guard let url = options.positionals.first else {
        throw SafariControlError(message: "wait-url requires a URL fragment.")
    }
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "url \(url)"
    ) {
        let current = try currentTab(target: try options.tabTarget())["url"] as? String ?? ""
        return options.flag("--exact") ? current == url : current.contains(url)
    }
    try printJSON(try currentTab(target: try options.tabTarget()))
}

func runNavigation(_ script: String, waitMs: Int, action: String) throws {
    let before = try currentTab()
    _ = try jsResult(script)
    let deadline = Date().timeIntervalSince1970 + Double(max(0, waitMs)) / 1000.0
    var after = try currentTab()
    while Date().timeIntervalSince1970 < deadline {
        let candidate = try currentTab()
        if NSDictionary(dictionary: candidate).isEqual(to: before) == false {
            after = candidate
            break
        }
        after = candidate
        Thread.sleep(forTimeInterval: 0.1)
    }
    try printJSON([
        "ok": true,
        "action": action,
        "changed": NSDictionary(dictionary: after).isEqual(to: before) == false,
        "before": before,
        "after": after,
    ])
}

func cmdBack(_ options: CommandOptions) throws {
    try runNavigation("history.back(); true;", waitMs: try options.int("--wait-ms") ?? 500, action: "back")
}

func cmdForward(_ options: CommandOptions) throws {
    try runNavigation("history.forward(); true;", waitMs: try options.int("--wait-ms") ?? 500, action: "forward")
}

func cmdReload(_ options: CommandOptions) throws {
    try runNavigation("location.reload(); true;", waitMs: try options.int("--wait-ms") ?? 500, action: "reload")
}

func cmdFindText(_ options: CommandOptions) throws {
    guard let text = options.positionals.first else {
        throw SafariControlError(message: "find-text requires text.")
    }
    let selectorLiteral = try jsonStringLiteral(options.string("--selector") ?? "*")
    let textLiteral = try jsonStringLiteral(text)
    let exact = options.flag("--exact")
    let limit = try options.int("--limit") ?? 10
    let code = #"""
    (() => {
      const selector = \#(selectorLiteral);
      const wanted = \#(textLiteral);
      const exact = \#(exact ? "true" : "false");
      const limit = \#(limit);
      const nodes = Array.from(document.querySelectorAll(selector));
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const attrSelector = (tag, attr, value) => `${tag}[${attr}="${String(value).replace(/"/g, '\\"')}"]`;
      const selectorFor = (el) => {
        const tag = el.tagName.toLowerCase();
        const dataAttrs = ['data-testid', 'data-test', 'data-qa', 'data-cy'];
        for (const attr of dataAttrs) {
          const value = el.getAttribute(attr);
          if (value) return attrSelector(tag, attr, value);
        }
        const aria = el.getAttribute('aria-label');
        if (aria) return attrSelector(tag, 'aria-label', aria);
        if (el.name) return attrSelector(tag, 'name', el.name);
        if (el.id) return `#${cssEscape(el.id)}`;
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return attrSelector(tag, 'placeholder', placeholder);
        const role = el.getAttribute('role');
        if (role) return attrSelector(tag, 'role', role);
        if (tag === 'a') {
          const href = el.getAttribute('href');
          if (href) return attrSelector(tag, 'href', href);
        }
        const type = el.getAttribute('type');
        if (type) return attrSelector(tag, 'type', type);
        return tag;
      };
      const selectorSource = (s) => {
        if (s.startsWith('#')) return 'id';
        if (s.includes('[data-testid=')) return 'data-testid';
        if (s.includes('[data-test=')) return 'data-test';
        if (s.includes('[data-qa=')) return 'data-qa';
        if (s.includes('[data-cy=')) return 'data-cy';
        if (s.includes('[aria-label=')) return 'aria-label';
        if (s.includes('[name=')) return 'name';
        if (s.includes('[placeholder=')) return 'placeholder';
        if (s.includes('[role=')) return 'role';
        if (s.includes('[href=')) return 'href';
        if (s.includes('[type=')) return 'type';
        return 'tag';
      };
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const wantedCmp = normalize(wanted).toLowerCase();
      const results = [];
      for (const el of nodes) {
        const textValue = normalize(el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '');
        if (!textValue) continue;
        const hay = textValue.toLowerCase();
        const matches = exact ? hay === wantedCmp : hay.includes(wantedCmp);
        if (!matches) continue;
        const suggested = selectorFor(el);
        results.push({
          tag: el.tagName.toLowerCase(),
          text: textValue.slice(0, 200),
          id: el.id || '',
          name: el.getAttribute('name') || '',
          href: el.href || '',
          suggested_selector: suggested,
          selector_source: selectorSource(suggested)
        });
        if (results.length >= limit) break;
      }
      return JSON.stringify(results);
    })()
    """#
    let results = parseJSON(try jsResult(code, target: try options.tabTarget()), default: []) as? [[String: Any]] ?? []
    if options.flag("--json") {
        try printJSON(results)
    } else {
        for (index, item) in results.enumerated() {
            print("\(index + 1)\t\((item["tag"] as? String) ?? "")\t\((item["suggested_selector"] as? String) ?? "")\t\((item["text"] as? String) ?? "")")
        }
    }
}

func extractLinksData(selector: String, limit: Int, target: SafariTabTarget? = nil) throws -> [[String: Any]] {
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const nodes = Array.from(document.querySelectorAll(\#(selectorLiteral))).slice(0, \#(limit));
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      return JSON.stringify(nodes.map((el, index) => ({
        index: index + 1,
        text: normalize(el.innerText || el.textContent || '').slice(0, 200),
        href: el.href || el.getAttribute('href') || '',
        title: el.getAttribute('title') || '',
        rel: el.getAttribute('rel') || '',
        target: el.getAttribute('target') || ''
      })));
    })()
    """#
    return parseJSON(try jsResult(code, target: target), default: []) as? [[String: Any]] ?? []
}

func cmdExtractLinks(_ options: CommandOptions) throws {
    let selector = options.string("--selector") ?? "a"
    let limit = try options.int("--limit") ?? 100
    let result = try extractLinksData(selector: selector, limit: limit, target: try options.tabTarget())
    if options.flag("--json") {
        try printJSON(result)
    } else {
        for item in result {
            print("\((item["index"] as? Int) ?? 0)\t\((item["href"] as? String) ?? "")\t\((item["text"] as? String) ?? "")")
        }
    }
}

func extractTablesData(selector: String, limit: Int, rowLimit: Int, target: SafariTabTarget? = nil) throws -> [[String: Any]] {
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const tables = Array.from(document.querySelectorAll(\#(selectorLiteral))).slice(0, \#(limit));
      return JSON.stringify(tables.map((table, tableIndex) => {
        const rows = Array.from(table.querySelectorAll('tr')).slice(0, \#(rowLimit));
        const parsedRows = rows.map((row) =>
          Array.from(row.querySelectorAll('th, td')).map((cell) => normalize(cell.innerText || cell.textContent || '').slice(0, 200))
        );
        let headers = [];
        const ths = Array.from(table.querySelectorAll('thead th'));
        if (ths.length) {
          headers = ths.map((cell) => normalize(cell.innerText || cell.textContent || '').slice(0, 200));
        } else if (parsedRows.length) {
          headers = parsedRows[0];
        }
        return {
          index: tableIndex + 1,
          id: table.id || '',
          class_name: typeof table.className === 'string' ? table.className : '',
          headers,
          rows: parsedRows
        };
      }));
    })()
    """#
    return parseJSON(try jsResult(code, target: target), default: []) as? [[String: Any]] ?? []
}

func cmdExtractTables(_ options: CommandOptions) throws {
    let selector = options.string("--selector") ?? "table"
    let limit = try options.int("--limit") ?? 20
    let rowLimit = try options.int("--row-limit") ?? 20
    let result = try extractTablesData(selector: selector, limit: limit, rowLimit: rowLimit, target: try options.tabTarget())
    if options.flag("--json") {
        try printJSON(result)
    } else {
        for table in result {
            let headers = (table["headers"] as? [Any])?.count ?? 0
            let rows = (table["rows"] as? [Any])?.count ?? 0
            print("table=\((table["index"] as? Int) ?? 0)\theaders=\(headers)\trows=\(rows)")
        }
    }
}

func cmdExportCookies(_ options: CommandOptions) throws {
    let code = #"""
    (() => {
      const cookies = document.cookie
        .split(';')
        .map((item) => item.trim())
        .filter(Boolean)
        .map((item) => {
          const idx = item.indexOf('=');
          if (idx === -1) return { name: item, value: '' };
          return { name: item.slice(0, idx), value: item.slice(idx + 1) };
        });
      return JSON.stringify(cookies);
    })()
    """#
    let cookies = parseJSON(try jsResult(code, target: try options.tabTarget()), default: []) as? [[String: Any]] ?? []
    if let path = options.string("--path") {
        let url = try writeJSONOutput(path: path, value: cookies)
        try printJSON(["ok": true, "path": url.path, "count": cookies.count, "kind": "cookies"])
    } else {
        try printJSON(cookies)
    }
}

func cmdExportStorage(_ options: CommandOptions) throws {
    guard let kind = options.positionals.first else {
        throw SafariControlError(message: "export-storage requires local or session.")
    }
    let storageExpr = kind == "local" ? "localStorage" : "sessionStorage"
    let code = #"""
    (() => {
      const out = {};
      for (let i = 0; i < \#(storageExpr).length; i++) {
        const key = \#(storageExpr).key(i);
        out[key] = \#(storageExpr).getItem(key);
      }
      return JSON.stringify(out);
    })()
    """#
    let storage = parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]) as? [String: Any] ?? [:]
    if let path = options.string("--path") {
        let url = try writeJSONOutput(path: path, value: storage)
        try printJSON(["ok": true, "path": url.path, "count": storage.count, "kind": kind])
    } else {
        try printJSON(storage)
    }
}

func cmdSetStorage(_ options: CommandOptions) throws {
    guard options.positionals.count >= 3 else {
        throw SafariControlError(message: "set-storage requires kind, key, and value.")
    }
    let kind = options.positionals[0]
    let keyLiteral = try jsonStringLiteral(options.positionals[1])
    let valueLiteral = try jsonStringLiteral(options.positionals[2])
    let kindLiteral = try jsonStringLiteral(kind)
    let storageExpr = kind == "local" ? "localStorage" : "sessionStorage"
    let code = #"""
    (() => {
      \#(storageExpr).setItem(\#(keyLiteral), \#(valueLiteral));
      return JSON.stringify({
        ok: true,
        kind: \#(kindLiteral),
        key: \#(keyLiteral),
        value: \#(storageExpr).getItem(\#(keyLiteral))
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdRemoveStorage(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "remove-storage requires kind and key.")
    }
    let kind = options.positionals[0]
    let keyLiteral = try jsonStringLiteral(options.positionals[1])
    let kindLiteral = try jsonStringLiteral(kind)
    let storageExpr = kind == "local" ? "localStorage" : "sessionStorage"
    let code = #"""
    (() => {
      const existed = \#(storageExpr).getItem(\#(keyLiteral)) !== null;
      \#(storageExpr).removeItem(\#(keyLiteral));
      return JSON.stringify({
        ok: true,
        kind: \#(kindLiteral),
        key: \#(keyLiteral),
        existed
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdSetCookie(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "set-cookie requires a name and value.")
    }
    let nameLiteral = try jsonStringLiteral(options.positionals[0])
    let valueLiteral = try jsonStringLiteral(options.positionals[1])
    let pathLiteral = try jsonStringLiteral(options.string("--path") ?? "/")
    let hasMaxAge = (try options.int("--max-age")) != nil
    let maxAge = try options.int("--max-age") ?? 0
    let code = #"""
    (() => {
      const name = \#(nameLiteral);
      const value = \#(valueLiteral);
      const pathValue = \#(pathLiteral);
      let cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; path=${pathValue}`;
      if (\#(hasMaxAge ? "true" : "false")) cookie += `; max-age=\#(maxAge)`;
      document.cookie = cookie;
      return JSON.stringify({
        ok: true,
        cookie,
        current: document.cookie
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdElementInfo(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "element-info requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let limit = try options.int("--limit") ?? 1
    let attrLimit = try options.int("--attr-limit") ?? 30
    let code = #"""
    (() => {
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const attrSelector = (tag, attr, value) => `${tag}[${attr}="${String(value).replace(/"/g, '\\"')}"]`;
      const selectorFor = (el) => {
        const tag = el.tagName.toLowerCase();
        const dataAttrs = ['data-testid', 'data-test', 'data-qa', 'data-cy'];
        for (const attr of dataAttrs) {
          const value = el.getAttribute(attr);
          if (value) return attrSelector(tag, attr, value);
        }
        const aria = el.getAttribute('aria-label');
        if (aria) return attrSelector(tag, 'aria-label', aria);
        if (el.name) return attrSelector(tag, 'name', el.name);
        if (el.id) return `#${cssEscape(el.id)}`;
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return attrSelector(tag, 'placeholder', placeholder);
        const role = el.getAttribute('role');
        if (role) return attrSelector(tag, 'role', role);
        if (tag === 'a') {
          const href = el.getAttribute('href');
          if (href) return attrSelector(tag, 'href', href);
        }
        const type = el.getAttribute('type');
        if (type) return attrSelector(tag, 'type', type);
        return tag;
      };
      const describe = (el, index) => {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        const attrs = {};
        for (const attr of Array.from(el.attributes).slice(0, \#(attrLimit))) {
          attrs[attr.name] = attr.value;
        }
        return {
          index,
          tag: el.tagName.toLowerCase(),
          id: el.id || '',
          name: el.getAttribute('name') || '',
          type: el.getAttribute('type') || '',
          role: el.getAttribute('role') || '',
          text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200),
          value: 'value' in el ? String(el.value).slice(0, 200) : '',
          href: el.href || '',
          checked: 'checked' in el ? !!el.checked : null,
          disabled: 'disabled' in el ? !!el.disabled : null,
          visible: !!(rect.width || rect.height || el.getClientRects().length) && style.visibility !== 'hidden' && style.display !== 'none',
          dataset: Object.assign({}, el.dataset || {}),
          attributes: attrs,
          rect: {
            x: rect.x, y: rect.y, width: rect.width, height: rect.height,
            top: rect.top, left: rect.left, right: rect.right, bottom: rect.bottom
          },
          suggested_selector: selectorFor(el)
        };
      };
      const matches = Array.from(document.querySelectorAll(\#(selectorLiteral))).slice(0, \#(limit));
      return JSON.stringify(matches.map((el, index) => describe(el, index + 1)));
    })()
    """#
    let results = parseJSON(try jsResult(code, target: try options.tabTarget()), default: []) as? [[String: Any]] ?? []
    if let path = options.string("--path") {
        let url = try writeJSONOutput(path: path, value: results)
        try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url), "count": results.count])
    } else if options.flag("--json") || limit != 1 {
        try printJSON(results)
    } else {
        try printJSON(results.first ?? [:])
    }
}

func cmdDispatchEvent(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "dispatch-event requires a selector and event name.")
    }
    let selectorLiteral = try jsonStringLiteral(options.positionals[0])
    let eventNameLiteral = try jsonStringLiteral(options.positionals[1])
    let eventClassLiteral = try jsonStringLiteral(options.string("--event-class") ?? "Event")
    let keyLiteral = try jsonStringLiteral(options.string("--key") ?? "")
    let codeLiteral = try jsonStringLiteral(options.string("--code") ?? "")
    let cancelable = options.flag("--cancelable")
    let composed = options.flag("--composed")
    let ctrl = options.flag("--ctrl")
    let meta = options.flag("--meta")
    let alt = options.flag("--alt")
    let shift = options.flag("--shift")
    let clientX = try options.int("--client-x") ?? 0
    let clientY = try options.int("--client-y") ?? 0
    let button = try options.int("--button") ?? 0
    let buttons = try options.int("--buttons") ?? 1
    let detailLiteral: String
    if let detail = options.string("--detail") {
        let detailData = try JSONSerialization.jsonObject(with: Data(detail.utf8))
        let data = try JSONSerialization.data(withJSONObject: detailData)
        detailLiteral = String(data: data, encoding: .utf8) ?? "null"
    } else {
        detailLiteral = "null"
    }
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      const eventName = \#(eventNameLiteral);
      const eventClass = \#(eventClassLiteral);
      const ctor = {
        Event,
        CustomEvent,
        MouseEvent,
        KeyboardEvent,
        InputEvent,
        FocusEvent
      }[eventClass] || Event;
      const init = {
        bubbles: true,
        cancelable: \#(cancelable ? "true" : "false"),
        composed: \#(composed ? "true" : "false")
      };
      if (eventClass === 'CustomEvent') init.detail = \#(detailLiteral);
      if (eventClass === 'KeyboardEvent') {
        init.key = \#(keyLiteral);
        init.code = \#(codeLiteral);
        init.ctrlKey = \#(ctrl ? "true" : "false");
        init.metaKey = \#(meta ? "true" : "false");
        init.altKey = \#(alt ? "true" : "false");
        init.shiftKey = \#(shift ? "true" : "false");
      }
      if (eventClass === 'MouseEvent') {
        init.clientX = \#(clientX);
        init.clientY = \#(clientY);
        init.button = \#(button);
        init.buttons = \#(buttons);
        init.ctrlKey = \#(ctrl ? "true" : "false");
        init.metaKey = \#(meta ? "true" : "false");
        init.altKey = \#(alt ? "true" : "false");
        init.shiftKey = \#(shift ? "true" : "false");
      }
      const event = new ctor(eventName, init);
      const dispatched = el.dispatchEvent(event);
      return JSON.stringify({
        ok: true,
        dispatched,
        tag: el.tagName.toLowerCase(),
        type: ctor.name,
        event_name: eventName,
        default_prevented: event.defaultPrevented
      });
    })()
    """#
    let result = parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]) as? [String: Any] ?? [:]
    if (result["ok"] as? Bool) != true {
        throw SafariControlError(message: result["error"] as? String ?? "dispatch-event failed")
    }
    try printJSON(result)
}

func cmdWaitMutation(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "wait-mutation requires a selector.")
    }
    let mode = options.string("--mode") ?? "text"
    let selectorLiteral = try jsonStringLiteral(selector)
    let modeLiteral = try jsonStringLiteral(mode)
    let attrLiteral = try jsonStringLiteral(options.string("--attr") ?? "")
    func capture() throws -> Any? {
        let code = #"""
        (() => {
          const selector = \#(selectorLiteral);
          const mode = \#(modeLiteral);
          if (mode === 'count') {
            return JSON.stringify({value: document.querySelectorAll(selector).length});
          }
          const el = document.querySelector(selector);
          if (!el) return JSON.stringify({value: '__missing__'});
          if (mode === 'text') return JSON.stringify({value: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim()});
          if (mode === 'html') return JSON.stringify({value: el.innerHTML});
          if (mode === 'value') return JSON.stringify({value: 'value' in el ? String(el.value) : ''});
          if (mode === 'attr') return JSON.stringify({value: el.getAttribute(\#(attrLiteral))});
          return JSON.stringify({value: ''});
        })()
        """#
        let result = parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]) as? [String: Any]
        return result?["value"]
    }
    let before = try capture()
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "mutation \(selector)"
    ) {
        let after = try capture()
        return String(describing: before) != String(describing: after)
    }
    let after = try capture()
    try printJSON([
        "ok": true,
        "selector": selector,
        "mode": mode,
        "attr": options.string("--attr").map { $0 as Any } ?? NSNull(),
        "before": before ?? NSNull(),
        "after": after ?? NSNull(),
    ])
}

func cmdGetFormState(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "get-form-state requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let limit = try options.int("--limit") ?? 50
    let code = #"""
    (() => {
      const form = document.querySelector(\#(selectorLiteral));
      if (!form) return JSON.stringify({ok: false, error: 'form not found'});
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const selectorFor = (el) => {
        if (el.name) return `${el.tagName.toLowerCase()}[name="${String(el.name).replace(/"/g, '\\"')}"]`;
        if (el.id) return `#${cssEscape(el.id)}`;
        return el.tagName.toLowerCase();
      };
      const fields = Array.from(form.querySelectorAll('input, textarea, select, button')).slice(0, \#(limit)).map((el, index) => {
        const tag = el.tagName.toLowerCase();
        const type = (el.getAttribute('type') || '').toLowerCase();
        let value = '';
        if (tag === 'select' && el.multiple) {
          value = Array.from(el.selectedOptions).map((opt) => opt.value);
        } else if (type === 'checkbox' || type === 'radio') {
          value = !!el.checked;
        } else if ('value' in el) {
          value = String(el.value);
        }
        return {
          index: index + 1,
          tag,
          type,
          name: el.getAttribute('name') || '',
          id: el.id || '',
          disabled: !!el.disabled,
          checked: 'checked' in el ? !!el.checked : null,
          value,
          selector: selectorFor(el)
        };
      });
      return JSON.stringify({ok: true, selector: \#(selectorLiteral), fields});
    })()
    """#
    let result = parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]) as? [String: Any] ?? [:]
    if (result["ok"] as? Bool) != true {
        throw SafariControlError(message: result["error"] as? String ?? "get-form-state failed")
    }
    if let path = options.string("--path") {
        let url = try writeJSONOutput(path: path, value: result)
        let count = (result["fields"] as? [Any])?.count ?? 0
        try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url), "count": count])
    } else {
        try printJSON(result)
    }
}

func cmdSetFormState(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "set-form-state requires a selector.")
    }
    let source: String
    if let file = options.string("--file") {
        source = try String(contentsOfFile: expandPath(file), encoding: .utf8)
    } else if let data = options.string("--data") {
        source = data
    } else {
        throw SafariControlError(message: "set-form-state requires --data or --file.")
    }
    let jsonObject = try JSONSerialization.jsonObject(with: Data(source.utf8))
    guard let payload = jsonObject as? [String: Any] else {
        throw SafariControlError(message: "Form state input must be a JSON object.")
    }
    let payloadData = try JSONSerialization.data(withJSONObject: payload)
    guard let payloadLiteral = String(data: payloadData, encoding: .utf8) else {
        throw SafariControlError(message: "Failed to encode form state payload.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const form = document.querySelector(\#(selectorLiteral));
      if (!form) return JSON.stringify({ok: false, error: 'form not found'});
      const updates = \#(payloadLiteral);
      const cssEscape = (value) => {
        if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
        return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
      };
      const resolveField = (key) => {
        if (key.startsWith('css:')) return form.querySelector(key.slice(4));
        return form.querySelector(`[name="${String(key).replace(/"/g, '\\"')}"]`) ||
          form.querySelector(`#${cssEscape(key)}`);
      };
      const out = [];
      for (const [key, rawValue] of Object.entries(updates)) {
        const el = resolveField(key);
        if (!el) {
          out.push({key, ok: false, error: 'field not found'});
          continue;
        }
        const tag = el.tagName.toLowerCase();
        const type = (el.getAttribute('type') || '').toLowerCase();
        if (type === 'radio') {
          const name = el.getAttribute('name') || key;
          const radio = form.querySelector(`input[type="radio"][name="${String(name).replace(/"/g, '\\"')}"][value="${String(rawValue).replace(/"/g, '\\"')}"]`);
          if (!radio) {
            out.push({key, ok: false, error: 'radio option not found'});
            continue;
          }
          radio.checked = true;
          radio.dispatchEvent(new Event('input', { bubbles: true }));
          radio.dispatchEvent(new Event('change', { bubbles: true }));
          out.push({key, ok: true, type, value: radio.value});
          continue;
        }
        if (type === 'checkbox') {
          el.checked = !!rawValue;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          out.push({key, ok: true, type, value: !!el.checked});
          continue;
        }
        if (tag === 'select') {
          const values = Array.isArray(rawValue) ? rawValue.map(String) : [String(rawValue)];
          for (const option of Array.from(el.options)) {
            option.selected = values.includes(option.value) || values.includes(option.text);
          }
          if (!el.multiple && values.length) el.value = values[0];
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          out.push({
            key,
            ok: true,
            type: el.multiple ? 'select-multiple' : 'select',
            value: el.multiple ? Array.from(el.selectedOptions).map((opt) => opt.value) : el.value
          });
          continue;
        }
        if ('value' in el) {
          const nextValue = rawValue == null ? '' : String(rawValue);
          const proto = Object.getPrototypeOf(el);
          const descriptor = proto ? Object.getOwnPropertyDescriptor(proto, 'value') : null;
          if (descriptor && typeof descriptor.set === 'function') descriptor.set.call(el, nextValue);
          else el.value = nextValue;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          out.push({key, ok: true, type, value: String(el.value)});
          continue;
        }
        out.push({key, ok: false, error: 'field is not settable'});
      }
      return JSON.stringify({ok: true, selector: \#(selectorLiteral), updates: out});
    })()
    """#
    let result = parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]) as? [String: Any] ?? [:]
    if (result["ok"] as? Bool) != true {
        throw SafariControlError(message: result["error"] as? String ?? "set-form-state failed")
    }
    try printJSON(result)
}

func cmdSaveLinks(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "save-links requires a path.")
    }
    let data = try extractLinksData(
        selector: options.string("--selector") ?? "a",
        limit: try options.int("--limit") ?? 100,
        target: try options.tabTarget()
    )
    let url = try writeJSONOutput(path: path, value: data)
    try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url), "count": data.count])
}

func cmdSaveTables(_ options: CommandOptions) throws {
    guard let path = options.positionals.first else {
        throw SafariControlError(message: "save-tables requires a path.")
    }
    let data = try extractTablesData(
        selector: options.string("--selector") ?? "table",
        limit: try options.int("--limit") ?? 20,
        rowLimit: try options.int("--row-limit") ?? 20,
        target: try options.tabTarget()
    )
    let url = try writeJSONOutput(path: path, value: data)
    try printJSON(["ok": true, "path": url.path, "bytes": fileSize(url), "count": data.count])
}

func cmdHover(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "hover requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      if (el.scrollIntoView) el.scrollIntoView({ block: 'center', inline: 'nearest' });
      const rect = el.getBoundingClientRect();
      const point = {
        clientX: rect.left + Math.max(1, rect.width / 2),
        clientY: rect.top + Math.max(1, rect.height / 2)
      };
      for (const type of ['pointerover', 'mouseover', 'pointerenter', 'mouseenter', 'pointermove', 'mousemove']) {
        el.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, ...point }));
      }
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdScrollToSelector(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "scroll-to-selector requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let blockLiteral = try jsonStringLiteral(options.string("--block") ?? "center")
    let inlineLiteral = try jsonStringLiteral(options.string("--inline") ?? "nearest")
    let behaviorLiteral = try jsonStringLiteral(options.string("--behavior") ?? "auto")
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      if (typeof el.scrollIntoView === 'function') {
        el.scrollIntoView({ block: \#(blockLiteral), inline: \#(inlineLiteral), behavior: \#(behaviorLiteral) });
      }
      const rect = el.getBoundingClientRect();
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        top: Math.round(rect.top),
        left: Math.round(rect.left),
        text: (el.innerText || el.textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 200)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdDrag(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "drag requires source and target selectors.")
    }
    let sourceLiteral = try jsonStringLiteral(options.positionals[0])
    let targetLiteral = try jsonStringLiteral(options.positionals[1])
    let code = #"""
    (() => {
      const source = document.querySelector(\#(sourceLiteral));
      const target = document.querySelector(\#(targetLiteral));
      if (!source) return JSON.stringify({ok: false, error: 'source not found'});
      if (!target) return JSON.stringify({ok: false, error: 'target not found'});
      if (source.scrollIntoView) source.scrollIntoView({ block: 'center', inline: 'nearest' });
      if (target.scrollIntoView) target.scrollIntoView({ block: 'center', inline: 'nearest' });
      const dataTransfer = typeof DataTransfer === 'undefined' ? null : new DataTransfer();
      const center = (el) => {
        const rect = el.getBoundingClientRect();
        return {
          clientX: rect.left + Math.max(1, rect.width / 2),
          clientY: rect.top + Math.max(1, rect.height / 2)
        };
      };
      const srcPoint = center(source);
      const dstPoint = center(target);
      const mouse = (el, type, point) => el.dispatchEvent(new MouseEvent(type, {
        bubbles: true,
        cancelable: true,
        ...point
      }));
      const drag = (el, type, point) => {
        const event = new DragEvent(type, {
          bubbles: true,
          cancelable: true,
          ...point,
          dataTransfer
        });
        return el.dispatchEvent(event);
      };
      mouse(source, 'pointerdown', srcPoint);
      mouse(source, 'mousedown', srcPoint);
      if (typeof DragEvent !== 'undefined') {
        drag(source, 'dragstart', srcPoint);
        drag(target, 'dragenter', dstPoint);
        drag(target, 'dragover', dstPoint);
        drag(target, 'drop', dstPoint);
        drag(source, 'dragend', dstPoint);
      }
      mouse(target, 'pointerup', dstPoint);
      mouse(target, 'mouseup', dstPoint);
      return JSON.stringify({
        ok: true,
        source_tag: source.tagName.toLowerCase(),
        target_tag: target.tagName.toLowerCase()
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdCheck(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "check requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      const tag = el.tagName ? el.tagName.toLowerCase() : '';
      const type = (el.getAttribute('type') || '').toLowerCase();
      if (!(tag === 'input' && (type === 'checkbox' || type === 'radio'))) {
        return JSON.stringify({ok: false, error: 'element is not checkbox or radio'});
      }
      if (!el.checked) {
        el.checked = true;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
      return JSON.stringify({ok: true, checked: !!el.checked, type});
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdUncheck(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "uncheck requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      const tag = el.tagName ? el.tagName.toLowerCase() : '';
      const type = (el.getAttribute('type') || '').toLowerCase();
      if (!(tag === 'input' && type === 'checkbox')) {
        return JSON.stringify({ok: false, error: 'element is not checkbox'});
      }
      if (el.checked) {
        el.checked = false;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
      return JSON.stringify({ok: true, checked: !!el.checked, type});
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdClickText(_ options: CommandOptions) throws {
    guard let text = options.positionals.first else {
        throw SafariControlError(message: "click-text requires text.")
    }
    let selectorLiteral = try jsonStringLiteral(options.string("--selector") ?? "*")
    let textLiteral = try jsonStringLiteral(text)
    let exact = options.flag("--exact")
    let index = try options.int("--index") ?? 1
    let code = #"""
    (() => {
      const selector = \#(selectorLiteral);
      const wanted = \#(textLiteral);
      const exact = \#(exact ? "true" : "false");
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const wantedCmp = normalize(wanted).toLowerCase();
      const nodes = Array.from(document.querySelectorAll(selector));
      const matches = nodes.filter((el) => {
        const textValue = normalize(el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '');
        if (!textValue) return false;
        const hay = textValue.toLowerCase();
        return exact ? hay === wantedCmp : hay.includes(wantedCmp);
      });
      const el = matches[\#(index - 1)] || null;
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      el.click();
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        text: normalize(el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '').slice(0, 200),
        match_index: \#(index)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdFocusText(_ options: CommandOptions) throws {
    guard let text = options.positionals.first else {
        throw SafariControlError(message: "focus-text requires text.")
    }
    let selectorLiteral = try jsonStringLiteral(options.string("--selector") ?? "*")
    let textLiteral = try jsonStringLiteral(text)
    let exact = options.flag("--exact")
    let index = try options.int("--index") ?? 1
    let code = #"""
    (() => {
      const selector = \#(selectorLiteral);
      const wanted = \#(textLiteral);
      const exact = \#(exact ? "true" : "false");
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const wantedCmp = normalize(wanted).toLowerCase();
      const nodes = Array.from(document.querySelectorAll(selector));
      const matches = nodes.filter((el) => {
        const textValue = normalize(el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '');
        if (!textValue) return false;
        const hay = textValue.toLowerCase();
        return exact ? hay === wantedCmp : hay.includes(wantedCmp);
      });
      const el = matches[\#(index - 1)] || null;
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      if (el.scrollIntoView) el.scrollIntoView({ block: 'center', inline: 'nearest' });
      if (typeof el.focus === 'function') el.focus();
      return JSON.stringify({
        ok: true,
        tag: el.tagName.toLowerCase(),
        active: document.activeElement === el,
        text: normalize(el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '').slice(0, 200),
        match_index: \#(index)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdSubmit(_ options: CommandOptions) throws {
    let target: String
    if let selector = options.positionals.first {
        target = try "document.querySelector(\(jsonStringLiteral(selector)))"
    } else {
        target = "document.activeElement"
    }
    let code = #"""
    (() => {
      const el = \#(target);
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      const form = el.tagName && el.tagName.toLowerCase() === 'form' ? el : el.form;
      if (!form) return JSON.stringify({ok: false, error: 'no form found'});
      if (typeof form.requestSubmit === 'function') form.requestSubmit();
      else form.submit();
      return JSON.stringify({ok: true, action: 'submitted'});
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdPressKey(_ options: CommandOptions) throws {
    guard let key = options.positionals.first else {
        throw SafariControlError(message: "press-key requires a key.")
    }
    let keyLiteral = try jsonStringLiteral(key)
    let shift = options.flag("--shift")
    let code = #"""
    (() => {
      const key = \#(keyLiteral);
      const shift = \#(shift ? "true" : "false");
      const aliases = {
        return: 'Enter',
        enter: 'Enter',
        esc: 'Escape',
        escape: 'Escape',
        tab: 'Tab',
        space: ' ',
        spacebar: ' ',
        backspace: 'Backspace',
        delete: 'Delete',
        arrowup: 'ArrowUp',
        arrowdown: 'ArrowDown',
        arrowleft: 'ArrowLeft',
        arrowright: 'ArrowRight'
      };
      const normalized = aliases[String(key).toLowerCase()] || key;
      const active = document.activeElement || document.body;
      const dispatchAll = (target, eventKey, extra = {}) => {
        for (const type of ['keydown', 'keypress', 'keyup']) {
          target.dispatchEvent(new KeyboardEvent(type, {
            key: eventKey,
            bubbles: true,
            cancelable: true,
            ...extra
          }));
        }
      };
      if (normalized === 'Tab') {
        const focusables = Array.from(document.querySelectorAll(
          'a[href], button, input, textarea, select, summary, [tabindex]:not([tabindex="-1"])'
        )).filter((el) => {
          const style = window.getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          return !el.disabled &&
            style.visibility !== 'hidden' &&
            style.display !== 'none' &&
            !!(rect.width || rect.height || el.getClientRects().length);
        });
        if (!focusables.length) return JSON.stringify({ok: false, error: 'no focusable elements'});
        const currentIndex = Math.max(0, focusables.indexOf(active));
        const nextIndex = shift ? (currentIndex - 1 + focusables.length) % focusables.length : (currentIndex + 1) % focusables.length;
        const next = focusables[nextIndex];
        if (next.scrollIntoView) next.scrollIntoView({ block: 'center', inline: 'nearest' });
        if (typeof next.focus === 'function') next.focus();
        return JSON.stringify({
          ok: true,
          key: normalized,
          active_tag: document.activeElement ? document.activeElement.tagName.toLowerCase() : '',
          active_text: ((document.activeElement && (document.activeElement.innerText || document.activeElement.textContent || document.activeElement.value || document.activeElement.getAttribute('aria-label'))) || '').replace(/\s+/g, ' ').trim().slice(0, 200)
        });
      }
      dispatchAll(active, normalized, { shiftKey: shift });
      if (normalized === 'Enter' && active) {
        const tag = active.tagName ? active.tagName.toLowerCase() : '';
        if (tag === 'textarea') {
        } else if (tag === 'button' || tag === 'a') {
          active.click();
        } else if (active.form) {
          if (typeof active.form.requestSubmit === 'function') active.form.requestSubmit();
          else active.form.submit();
        }
      }
      return JSON.stringify({
        ok: true,
        key: normalized,
        active_tag: active && active.tagName ? active.tagName.toLowerCase() : '',
        active_text: ((active && (active.innerText || active.textContent || active.value || active.getAttribute('aria-label'))) || '').replace(/\s+/g, ' ').trim().slice(0, 200)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdPressShortcut(_ options: CommandOptions) throws {
    guard let combo = options.positionals.first else {
        throw SafariControlError(message: "press-shortcut requires a combo.")
    }
    let comboLiteral = try jsonStringLiteral(combo)
    let code = #"""
    (() => {
      const combo = \#(comboLiteral);
      const parts = String(combo).split('+').map((part) => part.trim()).filter(Boolean);
      if (!parts.length) return JSON.stringify({ok: false, error: 'empty shortcut'});
      const keyRaw = parts[parts.length - 1];
      const modifiers = new Set(parts.slice(0, -1).map((part) => part.toLowerCase()));
      const aliases = {
        return: 'Enter',
        enter: 'Enter',
        esc: 'Escape',
        escape: 'Escape',
        tab: 'Tab',
        space: ' ',
        spacebar: ' ',
        backspace: 'Backspace',
        delete: 'Delete',
        command: 'Meta',
        cmd: 'Meta',
        option: 'Alt',
        alt: 'Alt',
        control: 'Control',
        ctrl: 'Control',
        shift: 'Shift'
      };
      const key = aliases[String(keyRaw).toLowerCase()] || keyRaw;
      const target = document.activeElement || document.body;
      const eventInit = {
        key,
        metaKey: modifiers.has('command') || modifiers.has('cmd') || modifiers.has('meta'),
        ctrlKey: modifiers.has('control') || modifiers.has('ctrl'),
        altKey: modifiers.has('option') || modifiers.has('alt'),
        shiftKey: modifiers.has('shift'),
        bubbles: true,
        cancelable: true
      };
      for (const type of ['keydown', 'keypress', 'keyup']) {
        target.dispatchEvent(new KeyboardEvent(type, eventInit));
      }
      return JSON.stringify({
        ok: true,
        combo,
        active_tag: target && target.tagName ? target.tagName.toLowerCase() : ''
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdSelectOption(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "select-option requires a selector and target.")
    }
    let selectorLiteral = try jsonStringLiteral(options.positionals[0])
    let targetLiteral = try jsonStringLiteral(options.positionals[1])
    let modeLiteral = try jsonStringLiteral(options.string("--by") ?? "text")
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      if (!el.tagName || el.tagName.toLowerCase() !== 'select') return JSON.stringify({ok: false, error: 'element is not select'});
      const target = \#(targetLiteral);
      const mode = \#(modeLiteral);
      const options = Array.from(el.options);
      let index = -1;
      if (mode === 'index') {
        index = Number(target);
      } else if (mode === 'value') {
        index = options.findIndex((option) => option.value === target);
      } else {
        const wanted = String(target).replace(/\s+/g, ' ').trim().toLowerCase();
        index = options.findIndex((option) =>
          String(option.text).replace(/\s+/g, ' ').trim().toLowerCase() === wanted
        );
      }
      if (!(index >= 0 && index < options.length)) return JSON.stringify({ok: false, error: 'option not found'});
      el.selectedIndex = index;
      el.value = options[index].value;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
      return JSON.stringify({
        ok: true,
        index,
        value: options[index].value,
        text: String(options[index].text).replace(/\s+/g, ' ').trim().slice(0, 200)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdWaitSelector(_ options: CommandOptions) throws {
    guard let selector = options.positionals.first else {
        throw SafariControlError(message: "wait-selector requires a selector.")
    }
    let selectorLiteral = try jsonStringLiteral(selector)
    let visible = options.flag("--visible")
    let target = try options.tabTarget()
    try waitUntil(
        timeoutMs: try options.int("--timeout-ms") ?? 5000,
        intervalMs: try options.int("--interval-ms") ?? 250,
        description: "selector \(selector)"
    ) {
        let code = #"""
        (() => {
          const el = document.querySelector(\#(selectorLiteral));
          if (!el) return false;
          if (!\#(visible ? "true" : "false")) return true;
          const style = window.getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          const rendered = !!(rect.width || rect.height || el.getClientRects().length);
          return rendered && style.visibility !== 'hidden' && style.display !== 'none';
        })()
        """#
        return try jsResult(code, target: target).trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == "true"
    }
    print("ready")
}

func cmdUpload(_ options: CommandOptions) throws {
    guard options.positionals.count >= 2 else {
        throw SafariControlError(message: "upload requires a selector and at least one file path.")
    }
    let selectorLiteral = try jsonStringLiteral(options.positionals[0])
    let fileURLs = options.positionals.dropFirst().map { URL(fileURLWithPath: expandPath($0)) }
    if let missing = fileURLs.first(where: { !FileManager.default.fileExists(atPath: $0.path) || (try? $0.resourceValues(forKeys: [.isRegularFileKey]).isRegularFile) != true }) {
        throw SafariControlError(message: "Upload file not found: \(missing.path)")
    }
    let totalBytes = fileURLs.reduce(Int64(0)) { $0 + fileSize($1) }
    if totalBytes > 700_000 {
        throw SafariControlError(message: "Upload payload is too large for Safari DOM injection. Use smaller files or fall back to desktop-control.")
    }
    let payload: [[String: Any]] = try fileURLs.map { url in
        let data = try Data(contentsOf: url)
        return [
            "name": url.lastPathComponent,
            "mime": mimeType(for: url),
            "base64": data.base64EncodedString(),
        ]
    }
    let payloadData = try JSONSerialization.data(withJSONObject: payload)
    guard let filesLiteral = String(data: payloadData, encoding: .utf8) else {
        throw SafariControlError(message: "Failed to encode upload payload.")
    }
    let code = #"""
    (() => {
      const el = document.querySelector(\#(selectorLiteral));
      if (!el) return JSON.stringify({ok: false, error: 'not found'});
      if (!el.tagName || el.tagName.toLowerCase() !== 'input' || (el.getAttribute('type') || '').toLowerCase() !== 'file') {
        return JSON.stringify({ok: false, error: 'element is not file input'});
      }
      const source = \#(filesLiteral);
      if (typeof DataTransfer === 'undefined') {
        return JSON.stringify({ok: false, error: 'DataTransfer unavailable in this page context'});
      }
      if (!el.multiple && source.length > 1) {
        return JSON.stringify({ok: false, error: 'input does not allow multiple files'});
      }
      const toBytes = (base64Value) => Uint8Array.from(atob(base64Value), (char) => char.charCodeAt(0));
      const dt = new DataTransfer();
      for (const item of source) {
        const file = new File([toBytes(item.base64)], item.name, {
          type: item.mime,
          lastModified: Date.now()
        });
        dt.items.add(file);
      }
      el.files = dt.files;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
      return JSON.stringify({
        ok: true,
        count: el.files.length,
        names: Array.from(el.files).map((file) => file.name)
      });
    })()
    """#
    try printJSON(parseJSON(try jsResult(code, target: try options.tabTarget()), default: [:]))
}

func cmdWaitDownload(_ options: CommandOptions) throws {
    guard let pattern = options.positionals.first else {
        throw SafariControlError(message: "wait-download requires a filename pattern.")
    }
    let directory = URL(fileURLWithPath: expandPath(options.string("--dir") ?? "~/Downloads"), isDirectory: true)
    var isDirectory: ObjCBool = false
    guard FileManager.default.fileExists(atPath: directory.path, isDirectory: &isDirectory) else {
        throw SafariControlError(message: "Download directory does not exist: \(directory.path)")
    }
    guard isDirectory.boolValue else {
        throw SafariControlError(message: "Download path is not a directory: \(directory.path)")
    }
    let timeoutMs = try options.int("--timeout-ms") ?? 5000
    let intervalMs = try options.int("--interval-ms") ?? 250
    let deadline = Date().timeIntervalSince1970 + Double(timeoutMs) / 1000.0
    let newOnly = options.flag("--new-only")

    func fileIdentity(_ url: URL) -> String {
        let values = try? url.resourceValues(forKeys: [.contentModificationDateKey, .fileSizeKey])
        let mtime = values?.contentModificationDate?.timeIntervalSince1970 ?? 0
        let size = values?.fileSize ?? 0
        return "\(url.path)|\(mtime)|\(size)"
    }

    func candidates(ignoring ignoredEntries: Set<String>) throws -> [URL] {
        let urls = try FileManager.default.contentsOfDirectory(
            at: directory,
            includingPropertiesForKeys: [.isRegularFileKey, .contentModificationDateKey, .fileSizeKey],
            options: [.skipsHiddenFiles]
        )
        return urls.filter { url in
            guard globMatches(url.lastPathComponent, pattern: pattern) else { return false }
            guard !ignoredEntries.contains(fileIdentity(url)) else { return false }
            guard !url.lastPathComponent.hasSuffix(".download"),
                  !url.lastPathComponent.hasSuffix(".part"),
                  !url.lastPathComponent.hasSuffix(".crdownload") else { return false }
            let values = try? url.resourceValues(forKeys: [.isRegularFileKey, .contentModificationDateKey])
            guard values?.isRegularFile == true else { return false }
            return true
        }.sorted {
            let lhs = (try? $0.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate?.timeIntervalSince1970) ?? 0
            let rhs = (try? $1.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate?.timeIntervalSince1970) ?? 0
            return lhs > rhs
        }
    }
    let ignoredEntries = newOnly ? Set(try candidates(ignoring: Set<String>()).map(fileIdentity)) : Set<String>()

    while true {
        let found = try candidates(ignoring: ignoredEntries)
        if let path = found.first {
            let values = try path.resourceValues(forKeys: [.fileSizeKey, .contentModificationDateKey])
            let size = values.fileSize ?? 0
            let mtime = values.contentModificationDate?.timeIntervalSince1970 ?? 0
            try printJSON([
                "ok": true,
                "path": path.path,
                "name": path.lastPathComponent,
                "size": size,
                "mtime": mtime,
            ])
            return
        }
        if Date().timeIntervalSince1970 >= deadline {
            throw SafariControlError(message: "Timed out waiting for download matching \(pattern) in \(directory.path).")
        }
        Thread.sleep(forTimeInterval: Double(intervalMs) / 1000.0)
    }
}

func cmdDoctor(_ options: CommandOptions) throws {
    var checks: [[String: Any]] = []

    if let installPath = safariInstallPath() {
        checks.append(doctorItem(name: "safari_app", ok: true, detail: installPath))
    } else {
        checks.append(doctorItem(name: "safari_app", ok: false, detail: "Safari.app not found.", hint: "Install Safari or use macOS with Safari available."))
    }

    let runningResult = try runProcess("/usr/bin/pgrep", ["-x", "Safari"])
    let safariRunning = runningResult.status == 0
    checks.append(doctorItem(
        name: "safari_running",
        ok: safariRunning,
        detail: safariRunning ? "Safari is running." : "Safari is not running.",
        hint: safariRunning ? nil : "Launch Safari before using native window or page commands."
    ))

    do {
        _ = try runOsaScript(#"tell application "Safari" to name"#)
        checks.append(doctorItem(name: "apple_events", ok: true, detail: "Apple Events access to Safari is working."))
    } catch {
        checks.append(doctorItem(
            name: "apple_events",
            ok: false,
            detail: String(describing: error),
            hint: "Allow this process to control Safari in macOS Privacy & Security > Automation."
        ))
    }

    if safariRunning {
        do {
            _ = try jsResult("document.title")
            checks.append(doctorItem(name: "safari_js", ok: true, detail: "JavaScript from Apple Events is enabled for the current Safari session."))
        } catch {
            let detail = String(describing: error)
            let hint = detail == jsPermissionHint ? jsPermissionHint : "Open a Safari tab and enable JavaScript from Apple Events if you need DOM commands."
            checks.append(doctorItem(name: "safari_js", ok: false, detail: detail, hint: hint))
        }

        do {
            _ = try runAXTool(["list-controls"])
            checks.append(doctorItem(name: "accessibility", ok: true, detail: "Accessibility automation for Safari native UI is working."))
        } catch {
            checks.append(doctorItem(
                name: "accessibility",
                ok: false,
                detail: String(describing: error),
                hint: "Grant Accessibility access to the process running Safari Control."
            ))
        }

        let probePath = URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("safari-control-doctor-shot.png")
        do {
            let result = try screenshotBackground(path: probePath)
            checks.append(doctorItem(
                name: "screenshot_background",
                ok: true,
                detail: "Background screenshot is working for window \(result["window_id"] ?? "")."
            ))
            try? FileManager.default.removeItem(at: probePath)
        } catch {
            let detail = String(describing: error)
            let hint: String
            if detail.contains("No visible Safari window was found for screenshot.") {
                hint = "Make sure Safari has a visible on-screen window, or use foreground screenshot mode as a fallback."
            } else {
                hint = "Background screenshot may require Screen Recording permission. Foreground screenshot can still work as a fallback."
            }
            checks.append(doctorItem(
                name: "screenshot_background",
                ok: false,
                detail: detail,
                hint: hint
            ))
        }
    } else {
        checks.append(doctorItem(
            name: "safari_js",
            ok: false,
            detail: "Skipped because Safari is not running.",
            hint: "Launch Safari, then re-run doctor to test JavaScript injection."
        ))
        checks.append(doctorItem(
            name: "accessibility",
            ok: false,
            detail: "Skipped because Safari is not running.",
            hint: "Launch Safari, then re-run doctor to test native UI accessibility."
        ))
        checks.append(doctorItem(
            name: "screenshot_background",
            ok: false,
            detail: "Skipped because Safari is not running.",
            hint: "Launch Safari, then re-run doctor to test screenshot capture."
        ))
    }

    let summaryOK = checks.allSatisfy { ($0["ok"] as? Bool) == true }
    let payload: [String: Any] = [
        "ok": summaryOK,
        "checks": checks,
    ]
    try printJSON(payload)
}

func performBuild(outputDir: URL, zipPath: URL?) throws -> [String: Any] {
    try FileManager.default.createDirectory(at: outputDir, withIntermediateDirectories: true)

    let sourceDir = sourceScriptDir()
    let controlSource = sourceDir.appendingPathComponent("safari_control.swift")
    let git = gitMetadata(startingAt: sourceDir)
    let environment = environmentMetadata()

    let controlBinary = try compileSwiftBinary(source: controlSource, output: outputDir.appendingPathComponent("safari_control"))
    let builtAt = iso8601Timestamp()
    var payload: [String: Any] = [
        "ok": true,
        "output_dir": outputDir.path,
        "artifacts": [controlBinary],
    ]
    if let zipPath {
        payload["zip"] = try createZipArchive(item: outputDir, output: zipPath)
    }
    var manifest: [String: Any] = [
        "tool": "safari-control",
        "version": toolVersion,
        "implementation": "swift",
        "built_at": builtAt,
        "entrypoint_source": controlSource.path,
        "output_dir": outputDir.path,
        "artifacts": payload["artifacts"] ?? [],
        "zip": payload["zip"] ?? NSNull(),
        "environment": environment,
    ]
    if let git {
        manifest["git"] = git
    }
    let manifestURL = try writeJSONOutput(
        path: outputDir.appendingPathComponent("build-manifest.json").path,
        value: manifest
    )
    payload["manifest"] = [
        "path": manifestURL.path,
        "bytes": fileSize(manifestURL),
        "sha256": try sha256(manifestURL),
    ]
    return payload
}

func cmdBuild(_ options: CommandOptions) throws {
    let outputDir: URL
    if let path = options.positionals.first ?? options.string("--output-dir") {
        outputDir = URL(fileURLWithPath: expandPath(path), isDirectory: true)
    } else {
        outputDir = sourceScriptDir().appendingPathComponent("bin", isDirectory: true)
    }
    let zipPath: URL?
    if options.flag("--zip") || options.string("--zip-path") != nil {
        zipPath = options.string("--zip-path")
            .map { URL(fileURLWithPath: expandPath($0)) }
            ?? outputDir.deletingLastPathComponent().appendingPathComponent("\(outputDir.lastPathComponent).zip")
    } else {
        zipPath = nil
    }
    let payload = try performBuild(outputDir: outputDir, zipPath: zipPath)
    try printJSON(payload)
}

func cmdRelease(_ options: CommandOptions) throws {
    let createdAt = Date()
    let defaultName = "safari-control-v\(toolVersion)-\(compactTimestamp(createdAt))"
    let git = gitMetadata()
    let environment = environmentMetadata()
    let releaseName = options.string("--name") ?? defaultName
    let releaseNotes: String?
    if let notesFile = options.string("--notes-file") {
        let path = expandPath(notesFile)
        releaseNotes = try String(contentsOfFile: path, encoding: .utf8)
    } else {
        releaseNotes = options.string("--notes")
    }
    let releaseDir: URL
    if let path = options.positionals.first ?? options.string("--output-dir") {
        releaseDir = URL(fileURLWithPath: expandPath(path), isDirectory: true)
    } else {
        let releasesRoot = sourceScriptDir().deletingLastPathComponent().appendingPathComponent("releases", isDirectory: true)
        releaseDir = releasesRoot.appendingPathComponent(releaseName, isDirectory: true)
    }
    try FileManager.default.createDirectory(at: releaseDir, withIntermediateDirectories: true)
    let distDir = releaseDir.appendingPathComponent("dist", isDirectory: true)
    let zipPath = releaseDir.appendingPathComponent("\(releaseName).zip")
    let buildPayload = try performBuild(outputDir: distDir, zipPath: zipPath)

    var releaseManifest: [String: Any] = [
        "tool": "safari-control",
        "version": toolVersion,
        "implementation": "swift",
        "created_at": iso8601Timestamp(createdAt),
        "name": releaseName,
        "release_dir": releaseDir.path,
        "dist_dir": distDir.path,
        "environment": environment,
        "build": buildPayload,
    ]
    if let git {
        releaseManifest["git"] = git
    }
    if let releaseNotes, !releaseNotes.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
        releaseManifest["notes"] = releaseNotes
    }
    let releaseManifestURL = try writeJSONOutput(
        path: releaseDir.appendingPathComponent("release-manifest.json").path,
        value: releaseManifest
    )
    try printJSON([
        "ok": true,
        "release_dir": releaseDir.path,
        "dist_dir": distDir.path,
        "zip": buildPayload["zip"] ?? NSNull(),
        "build_manifest": buildPayload["manifest"] ?? NSNull(),
        "release_manifest": [
            "path": releaseManifestURL.path,
            "bytes": fileSize(releaseManifestURL),
            "sha256": try sha256(releaseManifestURL),
        ],
    ])
}

func cmdScreenshot(_ options: CommandOptions) throws {
    let pathArg = options.positionals.first ?? options.string("--path") ?? "./safari-screenshot.png"
    let path = URL(fileURLWithPath: expandPath(pathArg))
    try FileManager.default.createDirectory(at: path.deletingLastPathComponent(), withIntermediateDirectories: true)
    let mode = (options.string("--mode") ?? "auto").lowercased()
    let restore = !options.flag("--no-restore")
    let payload = try captureScreenshot(path: path, mode: mode, restorePreviousApp: restore)
    try printJSON(payload)
}

// MARK: - Usage

let commandDescriptions: [String: String] = [
    "activate": "Bring Safari to the front.",
    "back": "Navigate back in history.",
    "build": "Compile safari_control into a standalone binary with embedded AX support.",
    "release": "Create a release directory with dist, zip, manifests, and optional release notes.",
    "click": "Click the first DOM element matching a CSS selector.",
    "click-text": "Click the first DOM element whose visible text matches.",
    "count": "Count elements matching a CSS selector.",
    "check": "Check a checkbox or radio input.",
    "dispatch-event": "Dispatch a DOM event to the first element matching a CSS selector.",
    "doctor": "Check Safari installation, runtime, Apple Events, JavaScript, and Accessibility access.",
    "drag": "Trigger best-effort DOM drag and drop between two selectors.",
    "element-info": "Describe the first few DOM elements matching a selector.",
    "export-cookies": "Export document.cookie for the current origin.",
    "export-storage": "Export localStorage or sessionStorage for the current origin.",
    "exists": "Check whether a CSS selector matches an element.",
    "extract-links": "Extract links from the current page.",
    "extract-tables": "Extract tables from the current page.",
    "fill": "Set the value of the first DOM element matching a CSS selector.",
    "find-text": "Find DOM elements by visible text.",
    "focus": "Focus the first DOM element matching a CSS selector.",
    "focus-text": "Focus the first DOM element whose visible text matches.",
    "forward": "Navigate forward in history.",
    "get-form-state": "Read form field state from a form selector.",
    "open": "Open a URL in Safari.",
    "hover": "Dispatch hover-like pointer and mouse events to an element.",
    "new-tab": "Open a new Safari tab.",
    "new-window": "Open a new Safari window.",
    "duplicate-tab": "Open the current tab URL in a new Safari tab.",
    "version": "Show safari-control version and runtime packaging details.",
    "current": "Show the current tab.",
    "list-menu-bar": "List top-level Safari menu bar items.",
    "list-menu-items": "List menu items under a Safari menu path.",
    "click-menu": "Click a Safari menu bar item or nested menu item path.",
    "list-windows": "List Safari windows.",
    "switch-window": "Bring a Safari window to the front.",
    "close-window": "Close a Safari window.",
    "save-session": "Save Safari window and tab layout to a local JSON file.",
    "restore-session": "Restore Safari windows and tabs from a saved session JSON file.",
    "switch-tab": "Switch to a Safari tab.",
    "close-tab": "Close a Safari tab.",
    "list-tabs": "List Safari tabs.",
    "switch-tab-title": "Switch to a Safari tab by title.",
    "switch-tab-url": "Switch to a Safari tab by URL.",
    "check-js": "Check whether Safari JavaScript access is enabled.",
    "run-js": "Run JavaScript in the current tab.",
    "eval-js": "Evaluate a JavaScript expression and normalize the result as JSON.",
    "get-text": "Extract text from the current page.",
    "interactive": "List likely interactive DOM elements.",
    "query": "Query DOM elements by CSS selector.",
    "reload": "Reload the current tab.",
    "save-html": "Save the current page HTML to a local file.",
    "save-links": "Save extracted links to a local JSON file.",
    "save-page-bundle": "Save HTML, text, links, tables, snapshot, screenshot, and a manifest into one directory.",
    "snapshot": "Get current tab info, interactives, and text excerpt.",
    "snapshot-with-screenshot": "Capture a structured page snapshot and a Safari screenshot in one command.",
    "save-tables": "Save extracted tables to a local JSON file.",
    "save-text": "Save extracted page text to a local file.",
    "save-snapshot": "Save a structured page snapshot to a local JSON file.",
    "screenshot": "Capture the visible Safari window to a PNG file using background or foreground mode.",
    "scroll-to-selector": "Scroll a matched element into view.",
    "select-option": "Select an option in a native HTML select element.",
    "set-cookie": "Write a cookie through document.cookie.",
    "set-form-state": "Apply multiple form field values from a JSON object.",
    "set-storage": "Write localStorage or sessionStorage for the current origin.",
    "upload": "Inject one or more local files into a file input.",
    "list-native-controls": "List Safari native chrome controls outside the web page.",
    "press-native-control": "Press a Safari native chrome control by title, description, or identifier.",
    "focus-native-control": "Focus a Safari native chrome control by title, description, or identifier.",
    "list-native-menu-items": "Show the popup menu items exposed by a Safari native control with AXShowMenu.",
    "click-native-menu-item": "Open a Safari native popup menu and choose a menu item path.",
    "perform-native-action": "Perform a specific AX action exposed by a Safari native control.",
    "set-native-value": "Set the value of a Safari native text field or similar accessibility control.",
    "native-open-url": "Open a URL by writing Safari's native smart search field and confirming it.",
    "native-search": "Run a search query through Safari's native smart search field.",
    "press-key": "Dispatch a page-level keyboard event.",
    "press-shortcut": "Dispatch a page-level keyboard shortcut.",
    "press-system-key": "Send a system-level key event through macOS accessibility.",
    "press-system-shortcut": "Send a system-level keyboard shortcut like Cmd+L.",
    "remove-storage": "Remove a localStorage or sessionStorage key.",
    "wait-count": "Wait for the number of matching elements to reach a condition.",
    "wait-download": "Wait for a downloaded file matching a glob pattern to appear.",
    "wait-js": "Wait for a JavaScript expression to become truthy.",
    "wait-mutation": "Wait for text, HTML, value, attribute, or count to change.",
    "wait-selector": "Wait for a selector to appear, optionally visible.",
    "wait-text": "Wait for text to appear in the page body.",
    "wait-title": "Wait for the current tab title to match or contain text.",
    "wait-url": "Wait for the current tab URL to match or contain text.",
    "submit": "Submit the nearest form from a selector or the active element.",
    "uncheck": "Uncheck a checkbox input.",
]

func printUsage() {
    print("usage: safari_control.swift <command> [options]")
    print("")
    print("Control Safari from Swift.")
    print("")
    for key in commandDescriptions.keys.sorted() {
        print("  \(key)\t\(commandDescriptions[key]!)")
    }
}

// MARK: - Main

func main() -> Int32 {
    var args = Array(CommandLine.arguments.dropFirst())
    guard let command = args.first else {
        printUsage()
        return 0
    }
    if command == "__ax-helper" {
        do {
            try handleEmbeddedAXHelper(arguments: Array(args.dropFirst()))
            return 0
        } catch {
            fputs("\(error)\n", stderr)
            return 1
        }
    }
    if command == "-h" || command == "--help" || command == "help" {
        printUsage()
        return 0
    }
    args.removeFirst()
    let options = CommandOptions(args)

    do {
        switch command {
        case "activate": try cmdActivate()
        case "build": try cmdBuild(options)
        case "release": try cmdRelease(options)
        case "version": try cmdVersion()
        case "open": try cmdOpen(options)
        case "new-tab": try cmdNewTab(options)
        case "new-window": try cmdNewWindow(options)
        case "duplicate-tab": try cmdDuplicateTab()
        case "current": try cmdCurrent(options)
        case "doctor": try cmdDoctor(options)
        case "list-menu-bar": try cmdListMenuBar(options)
        case "list-menu-items": try cmdListMenuItems(options)
        case "click-menu": try cmdClickMenu(options)
        case "list-windows": try cmdListWindows(options)
        case "switch-window": try cmdSwitchWindow(options)
        case "close-window": try cmdCloseWindow(options)
        case "save-session": try cmdSaveSession(options)
        case "restore-session": try cmdRestoreSession(options)
        case "screenshot": try cmdScreenshot(options)
        case "switch-tab": try cmdSwitchTab(options)
        case "close-tab": try cmdCloseTab(options)
        case "list-tabs": try cmdListTabs(options)
        case "switch-tab-title": try cmdSwitchTabTitle(options)
        case "switch-tab-url": try cmdSwitchTabURL(options)
        case "check-js": try cmdCheckJS()
        case "run-js": try cmdRunJS(options)
        case "eval-js": try cmdEvalJS(options)
        case "get-text": try cmdGetText(options)
        case "save-html": try cmdSaveHTML(options)
        case "save-text": try cmdSaveText(options)
        case "save-page-bundle": try cmdSavePageBundle(options)
        case "interactive": try cmdInteractive(options)
        case "query": try cmdQuery(options)
        case "exists": try cmdExists(options)
        case "count": try cmdCount(options)
        case "find-text": try cmdFindText(options)
        case "extract-links": try cmdExtractLinks(options)
        case "extract-tables": try cmdExtractTables(options)
        case "export-cookies": try cmdExportCookies(options)
        case "export-storage": try cmdExportStorage(options)
        case "set-storage": try cmdSetStorage(options)
        case "remove-storage": try cmdRemoveStorage(options)
        case "set-cookie": try cmdSetCookie(options)
        case "element-info": try cmdElementInfo(options)
        case "snapshot": try cmdSnapshot(options)
        case "snapshot-with-screenshot": try cmdSnapshotWithScreenshot(options)
        case "save-snapshot": try cmdSaveSnapshot(options)
        case "save-links": try cmdSaveLinks(options)
        case "save-tables": try cmdSaveTables(options)
        case "click": try cmdClick(options)
        case "hover": try cmdHover(options)
        case "scroll-to-selector": try cmdScrollToSelector(options)
        case "drag": try cmdDrag(options)
        case "check": try cmdCheck(options)
        case "uncheck": try cmdUncheck(options)
        case "click-text": try cmdClickText(options)
        case "focus": try cmdFocus(options)
        case "focus-text": try cmdFocusText(options)
        case "submit": try cmdSubmit(options)
        case "fill": try cmdFill(options)
        case "press-key": try cmdPressKey(options)
        case "press-shortcut": try cmdPressShortcut(options)
        case "select-option": try cmdSelectOption(options)
        case "upload": try cmdUpload(options)
        case "wait-js": try cmdWaitJS(options)
        case "dispatch-event": try cmdDispatchEvent(options)
        case "wait-mutation": try cmdWaitMutation(options)
        case "get-form-state": try cmdGetFormState(options)
        case "set-form-state": try cmdSetFormState(options)
        case "wait-selector": try cmdWaitSelector(options)
        case "wait-text": try cmdWaitText(options)
        case "wait-count": try cmdWaitCount(options)
        case "wait-download": try cmdWaitDownload(options)
        case "wait-title": try cmdWaitTitle(options)
        case "wait-url": try cmdWaitURL(options)
        case "back": try cmdBack(options)
        case "forward": try cmdForward(options)
        case "reload": try cmdReload(options)
        case "list-native-controls": try cmdListNativeControls(options)
        case "press-native-control": try cmdPressNativeControl(options)
        case "focus-native-control": try cmdFocusNativeControl(options)
        case "list-native-menu-items": try cmdListNativeMenuItems(options)
        case "click-native-menu-item": try cmdClickNativeMenuItem(options)
        case "perform-native-action": try cmdPerformNativeAction(options)
        case "set-native-value": try cmdSetNativeValue(options)
        case "native-open-url": try cmdNativeOpenURL(options)
        case "native-search": try cmdNativeSearch(options)
        case "press-system-key": try cmdPressSystemKey(options)
        case "press-system-shortcut": try cmdPressSystemShortcut(options)
        default:
            throw SafariControlError(message: "Unknown command: \(command)")
        }
        return 0
    } catch {
        fputs("\(error)\n", stderr)
        return 1
    }
}

Foundation.exit(main())
