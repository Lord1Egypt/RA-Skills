#!/usr/bin/env swift

import AppKit
import ApplicationServices
import Foundation

typealias UIElement = AXUIElement

struct Options {
    let contact: String
    let message: String
    let dryRun: Bool
    let timeout: TimeInterval
}

struct UIContext {
    let window: UIElement
    let mainSplit: UIElement
    let searchField: UIElement
    let sessionTable: UIElement
    let rightPane: UIElement
}

enum ScriptError: LocalizedError {
    case usage(String)
    case missingAccessibilityPermission
    case weChatNotInstalled
    case weChatLaunchFailed
    case chatWindowNotFound
    case uiStructureChanged(String)
    case contactNotFound(String)
    case openedWrongChat(expected: String, actual: String)
    case messageNotSent(String)

    var errorDescription: String? {
        switch self {
        case .usage(let text):
            return text
        case .missingAccessibilityPermission:
            return "缺少辅助功能权限，请在“系统设置 -> 隐私与安全性 -> 辅助功能”里放行当前终端或 Codex。"
        case .weChatNotInstalled:
            return "未找到微信桌面版。"
        case .weChatLaunchFailed:
            return "微信启动失败。"
        case .chatWindowNotFound:
            return "未找到微信聊天主窗口。"
        case .uiStructureChanged(let message):
            return "微信界面结构与脚本预期不一致：\(message)"
        case .contactNotFound(let contact):
            return "未在微信搜索结果中找到精确匹配联系人：\(contact)"
        case .openedWrongChat(let expected, let actual):
            return "打开的会话不是目标联系人，期望“\(expected)”，实际“\(actual)”。"
        case .messageNotSent(let detail):
            return "消息未成功发送：\(detail)"
        }
    }
}

func printUsage() {
    let text = """
    用法:
      swift scripts/send_wechat_message.swift --contact "<联系人>" --message "<消息>" [--dry-run] [--timeout 10]

    参数:
      --contact   微信联系人显示名，必须精确匹配
      --message   要发送的文本内容
      --dry-run   只打开并校验会话，不发送消息
      --timeout   超时时间，默认 10 秒
    """
    print(text)
}

func parseArguments() throws -> Options {
    let args = Array(CommandLine.arguments.dropFirst())
    if args.isEmpty || args.contains("--help") || args.contains("-h") {
        throw ScriptError.usage("")
    }

    var contact: String?
    var message: String?
    var dryRun = false
    var timeout: TimeInterval = 10

    var index = 0
    while index < args.count {
        let arg = args[index]
        switch arg {
        case "--contact":
            index += 1
            guard index < args.count else {
                throw ScriptError.usage("缺少 --contact 的值")
            }
            contact = args[index]
        case "--message":
            index += 1
            guard index < args.count else {
                throw ScriptError.usage("缺少 --message 的值")
            }
            message = args[index]
        case "--timeout":
            index += 1
            guard index < args.count, let value = Double(args[index]), value > 0 else {
                throw ScriptError.usage("--timeout 必须是正数")
            }
            timeout = value
        case "--dry-run":
            dryRun = true
        default:
            throw ScriptError.usage("未知参数：\(arg)")
        }
        index += 1
    }

    guard let contact, !contact.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
        throw ScriptError.usage("contact 不能为空")
    }
    guard let message, !message.isEmpty else {
        throw ScriptError.usage("message 不能为空")
    }

    return Options(
        contact: contact.trimmingCharacters(in: .whitespacesAndNewlines),
        message: message,
        dryRun: dryRun,
        timeout: timeout
    )
}

func sleepBriefly(_ seconds: TimeInterval) {
    usleep(useconds_t(seconds * 1_000_000))
}

func waitUntil<T>(
    timeout: TimeInterval,
    interval: TimeInterval = 0.2,
    _ condition: () -> T?
) -> T? {
    let deadline = Date().addingTimeInterval(timeout)
    while Date() < deadline {
        if let result = condition() {
            return result
        }
        sleepBriefly(interval)
    }
    return nil
}

func shellOpenWeChat() throws {
    let task = Process()
    task.executableURL = URL(fileURLWithPath: "/usr/bin/open")
    task.arguments = ["-b", "com.tencent.xinWeChat"]
    try task.run()
    task.waitUntilExit()
    guard task.terminationStatus == 0 else {
        throw ScriptError.weChatLaunchFailed
    }
}

func runningWeChatApp() -> NSRunningApplication? {
    NSRunningApplication.runningApplications(withBundleIdentifier: "com.tencent.xinWeChat").first
}

func ensureWeChatRunning(timeout: TimeInterval) throws -> NSRunningApplication {
    if let app = runningWeChatApp() {
        return app
    }

    guard NSWorkspace.shared.urlForApplication(withBundleIdentifier: "com.tencent.xinWeChat") != nil else {
        throw ScriptError.weChatNotInstalled
    }

    try shellOpenWeChat()

    guard let app = waitUntil(timeout: timeout, { runningWeChatApp() }) else {
        throw ScriptError.weChatLaunchFailed
    }
    return app
}

func axValue(_ element: UIElement, _ attribute: String) -> AnyObject? {
    var value: CFTypeRef?
    let result = AXUIElementCopyAttributeValue(element, attribute as CFString, &value)
    guard result == .success else {
        return nil
    }
    return value
}

func axChildren(_ element: UIElement) -> [UIElement] {
    axValue(element, kAXChildrenAttribute as String) as? [UIElement] ?? []
}

func axString(_ element: UIElement, _ attribute: String) -> String {
    guard let value = axValue(element, attribute) else {
        return ""
    }
    return String(describing: value)
}

func axRole(_ element: UIElement) -> String {
    axString(element, kAXRoleAttribute as String)
}

func axSubrole(_ element: UIElement) -> String {
    axString(element, kAXSubroleAttribute as String)
}

func axSet(_ element: UIElement, _ attribute: String, _ value: CFTypeRef) -> Bool {
    AXUIElementSetAttributeValue(element, attribute as CFString, value) == .success
}

func axAction(_ element: UIElement, _ action: String) -> Bool {
    AXUIElementPerformAction(element, action as CFString) == .success
}

func isEditableTextField(_ element: UIElement) -> Bool {
    axRole(element) == kAXTextFieldRole as String && axSettable(element, kAXValueAttribute as String)
}

func axSettable(_ element: UIElement, _ attribute: String) -> Bool {
    var flag = DarwinBoolean(false)
    return AXUIElementIsAttributeSettable(element, attribute as CFString, &flag) == .success && flag.boolValue
}

func firstDescendant(
    of root: UIElement,
    maxDepth: Int = 8,
    where matches: (UIElement) -> Bool
) -> UIElement? {
    var queue: [(UIElement, Int)] = [(root, 0)]
    while !queue.isEmpty {
        let (element, depth) = queue.removeFirst()
        if matches(element) {
            return element
        }
        guard depth < maxDepth else {
            continue
        }
        for child in axChildren(element) {
            queue.append((child, depth + 1))
        }
    }
    return nil
}

func descendantStrings(
    of root: UIElement,
    attributes: [String],
    maxDepth: Int = 5
) -> [String] {
    var values: [String] = []
    var queue: [(UIElement, Int)] = [(root, 0)]
    while !queue.isEmpty {
        let (element, depth) = queue.removeFirst()
        for attribute in attributes {
            let text = axString(element, attribute).trimmingCharacters(in: .whitespacesAndNewlines)
            if !text.isEmpty {
                values.append(text)
            }
        }
        guard depth < maxDepth else {
            continue
        }
        for child in axChildren(element) {
            queue.append((child, depth + 1))
        }
    }
    return values
}

func keyPress(_ keyCode: CGKeyCode, flags: CGEventFlags = []) {
    let source = CGEventSource(stateID: .hidSystemState)
    let keyDown = CGEvent(keyboardEventSource: source, virtualKey: keyCode, keyDown: true)
    keyDown?.flags = flags
    keyDown?.post(tap: .cghidEventTap)

    let keyUp = CGEvent(keyboardEventSource: source, virtualKey: keyCode, keyDown: false)
    keyUp?.flags = flags
    keyUp?.post(tap: .cghidEventTap)
}

func withTemporaryClipboard(_ text: String, body: () -> Void) {
    let pasteboard = NSPasteboard.general
    let originalText = pasteboard.string(forType: .string)

    pasteboard.clearContents()
    pasteboard.setString(text, forType: .string)
    body()
    sleepBriefly(0.1)

    pasteboard.clearContents()
    if let originalText {
        pasteboard.setString(originalText, forType: .string)
    }
}

func matchingRow(_ row: UIElement, contact: String) -> Bool {
    let candidates = descendantStrings(
        of: row,
        attributes: [kAXTitleAttribute as String, kAXValueAttribute as String],
        maxDepth: 4
    )
    return candidates.contains { text in
        text == contact || text.hasPrefix(contact + ",") || text.hasPrefix(contact + "，")
    }
}

func resolveContext(app: NSRunningApplication) -> UIContext? {
    let axApp = AXUIElementCreateApplication(app.processIdentifier)
    let windows = axValue(axApp, kAXWindowsAttribute as String) as? [UIElement] ?? []

    let chatWindow = windows.first(where: { axString($0, kAXTitleAttribute as String).contains("(聊天)") })
        ?? windows.first(where: { axChildren($0).count >= 10 })
    guard let chatWindow else {
        return nil
    }

    let mainSplit = axChildren(chatWindow).first {
        axRole($0) == kAXSplitGroupRole as String
            && firstDescendant(of: $0, maxDepth: 2) {
                axRole($0) == kAXTextFieldRole as String && axSubrole($0) == kAXSearchFieldSubrole as String
            } != nil
    }
    guard let mainSplit else {
        return nil
    }

    let searchField = axChildren(mainSplit).first {
        axRole($0) == kAXTextFieldRole as String && axSubrole($0) == kAXSearchFieldSubrole as String
    }
    let sessionTable = axChildren(mainSplit)
        .first(where: { axRole($0) == kAXScrollAreaRole as String })
        .flatMap { firstDescendant(of: $0, maxDepth: 2) { axRole($0) == kAXTableRole as String } }
    let rightPane = axChildren(mainSplit).first {
        axRole($0) == kAXSplitGroupRole as String
            && firstDescendant(of: $0, maxDepth: 3) { axRole($0) == kAXTextAreaRole as String } != nil
    }

    guard let searchField, let sessionTable, let rightPane else {
        return nil
    }

    return UIContext(
        window: chatWindow,
        mainSplit: mainSplit,
        searchField: searchField,
        sessionTable: sessionTable,
        rightPane: rightPane
    )
}

func currentChatTitle(app: NSRunningApplication) -> String? {
    guard let context = resolveContext(app: app) else {
        return nil
    }

    for child in axChildren(context.rightPane) where axRole(child) == kAXStaticTextRole as String {
        let value = axString(child, kAXValueAttribute as String).trimmingCharacters(in: .whitespacesAndNewlines)
        if value.isEmpty || value == "Field" {
            continue
        }
        if value.hasPrefix("(") && value.hasSuffix(")") {
            continue
        }
        return value
    }

    return firstDescendant(of: context.rightPane, maxDepth: 4) {
        axRole($0) == kAXStaticTextRole as String
            && !axString($0, kAXValueAttribute as String).trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }.map {
        axString($0, kAXValueAttribute as String).trimmingCharacters(in: .whitespacesAndNewlines)
    }
}

func messageInput(app: NSRunningApplication) -> UIElement? {
    guard let context = resolveContext(app: app) else {
        return nil
    }

    var matches: [UIElement] = []
    var queue: [UIElement] = [context.rightPane]
    while !queue.isEmpty {
        let element = queue.removeFirst()
        if axRole(element) == kAXTextAreaRole as String {
            matches.append(element)
        }
        queue.append(contentsOf: axChildren(element))
    }
    return matches.last
}

func openChat(contact: String, app: NSRunningApplication, timeout: TimeInterval) throws {
    guard let initialContext = waitUntil(timeout: timeout, { resolveContext(app: app) }) else {
        throw ScriptError.chatWindowNotFound
    }

    guard axAction(initialContext.searchField, kAXPressAction as String) else {
        throw ScriptError.uiStructureChanged("无法聚焦左侧搜索框")
    }

    guard let searchInput = waitUntil(timeout: timeout, {
        resolveContext(app: app).flatMap { context in
            firstDescendant(of: context.searchField, maxDepth: 1) { isEditableTextField($0) }
        }
    }) else {
        throw ScriptError.uiStructureChanged("搜索框未展开成可编辑输入框")
    }

    guard axSet(searchInput, kAXFocusedAttribute as String, kCFBooleanTrue) else {
        throw ScriptError.uiStructureChanged("无法聚焦搜索输入框")
    }

    withTemporaryClipboard(contact) {
        keyPress(0, flags: .maskCommand)
        sleepBriefly(0.08)
        keyPress(51)
        sleepBriefly(0.08)
        keyPress(9, flags: .maskCommand)
    }

    _ = waitUntil(timeout: timeout) {
        let value = axString(searchInput, kAXValueAttribute as String)
        return value == contact ? true : nil
    }

    guard let row = waitUntil(timeout: timeout, {
        resolveContext(app: app).flatMap { context in
            let rows = axChildren(context.sessionTable).filter {
                axRole($0) == kAXRowRole as String && axSubrole($0) == kAXTableRowSubrole as String
            }
            return rows.first { matchingRow($0, contact: contact) }
        }
    }) else {
        throw ScriptError.contactNotFound(contact)
    }

    guard let latestContext = resolveContext(app: app) else {
        throw ScriptError.chatWindowNotFound
    }

    let selectedRows = [row] as CFArray
    guard axSet(latestContext.sessionTable, kAXSelectedRowsAttribute as String, selectedRows) else {
        throw ScriptError.uiStructureChanged("无法选中搜索结果行")
    }
    _ = axSet(latestContext.sessionTable, kAXFocusedAttribute as String, kCFBooleanTrue)
    sleepBriefly(0.15)
    keyPress(36)

    guard let openedTitle = waitUntil(timeout: timeout, { currentChatTitle(app: app) == contact ? contact : nil }) else {
        let actual = currentChatTitle(app: app) ?? "未知"
        throw ScriptError.openedWrongChat(expected: contact, actual: actual)
    }

    guard openedTitle == contact else {
        throw ScriptError.openedWrongChat(expected: contact, actual: openedTitle)
    }
}

func sendMessage(_ message: String, app: NSRunningApplication, timeout: TimeInterval) throws {
    guard let input = waitUntil(timeout: timeout, { messageInput(app: app) }) else {
        throw ScriptError.uiStructureChanged("未找到消息输入框")
    }

    guard axSet(input, kAXFocusedAttribute as String, kCFBooleanTrue) else {
        throw ScriptError.uiStructureChanged("无法聚焦消息输入框")
    }
    guard axSet(input, kAXValueAttribute as String, "" as CFString) else {
        throw ScriptError.uiStructureChanged("无法清空消息输入框")
    }
    guard axSet(input, kAXValueAttribute as String, message as CFString) else {
        throw ScriptError.uiStructureChanged("无法写入消息输入框")
    }

    guard waitUntil(timeout: timeout, {
        axString(input, kAXValueAttribute as String) == message ? true : nil
    }) != nil else {
        throw ScriptError.messageNotSent("消息内容未成功写入输入框")
    }

    let attempts: [(String, CGEventFlags)] = [
        ("return", []),
        ("command+return", .maskCommand),
        ("control+return", .maskControl),
    ]

    for (_, flags) in attempts {
        keyPress(36, flags: flags)
        sleepBriefly(0.35)
        if axString(input, kAXValueAttribute as String).isEmpty {
            return
        }
        _ = axSet(input, kAXValueAttribute as String, message as CFString)
        sleepBriefly(0.12)
    }

    throw ScriptError.messageNotSent("发送快捷键执行后，输入框仍有残留内容")
}

func run() throws {
    let options = try parseArguments()

    if !AXIsProcessTrusted() {
        throw ScriptError.missingAccessibilityPermission
    }

    let app = try ensureWeChatRunning(timeout: options.timeout)
    _ = app.activate(options: [.activateAllWindows])

    guard waitUntil(timeout: options.timeout, { resolveContext(app: app) }) != nil else {
        throw ScriptError.chatWindowNotFound
    }

    try openChat(contact: options.contact, app: app, timeout: options.timeout)

    if options.dryRun {
        print("dry-run ok: \(options.contact)")
        return
    }

    try sendMessage(options.message, app: app, timeout: options.timeout)
    print("sent: \(options.contact)")
}

do {
    try run()
} catch let error as ScriptError {
    if case .usage(let detail) = error, detail.isEmpty {
        printUsage()
        exit(0)
    }
    fputs("ERROR: \(error.localizedDescription)\n", stderr)
    if case .usage = error {
        printUsage()
    }
    exit(1)
} catch {
    fputs("ERROR: \(error.localizedDescription)\n", stderr)
    exit(1)
}
