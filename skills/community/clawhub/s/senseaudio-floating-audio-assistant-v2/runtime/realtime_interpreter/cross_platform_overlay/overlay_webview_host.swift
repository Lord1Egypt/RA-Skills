import AppKit
import Foundation
import WebKit

struct OverlayUIState {
    var hover = false
    var projectPanelOpen = false
    var hasCaption = true
}

final class OverlayHostWindow: NSWindow {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { true }

    override func mouseDown(with event: NSEvent) {
        performDrag(with: event)
    }
}

final class OverlayHitTestView: NSView {
    var uiState = OverlayUIState()

    override func hitTest(_ point: NSPoint) -> NSView? {
        guard interactivePath().contains(point) else { return nil }
        return super.hitTest(point)
    }

    private func interactivePath() -> NSBezierPath {
        let path = NSBezierPath()
        let size = bounds.size
        let shellPadding: CGFloat = 8
        let orbSystemSize = CGSize(width: 170, height: 170)
        let panelWidth: CGFloat = uiState.projectPanelOpen ? 198 : 0
        let gap: CGFloat = uiState.projectPanelOpen ? 6 : 0
        let orbOrigin = CGPoint(
            x: shellPadding + panelWidth + gap,
            y: size.height - shellPadding - orbSystemSize.height
        )
        let orbCenter = CGPoint(x: orbOrigin.x + orbSystemSize.width / 2, y: orbOrigin.y + orbSystemSize.height / 2)

        path.appendOval(in: NSRect(x: orbCenter.x - 41, y: orbCenter.y - 41, width: 82, height: 82))

        if uiState.hover || uiState.projectPanelOpen {
            let angles: [CGFloat] = [136, 162, 188, 214, 240]
            let radius: CGFloat = 98
            for angle in angles {
                let radians = angle * .pi / 180
                let cx = orbCenter.x + cos(radians) * radius
                let cy = orbCenter.y + sin(radians) * radius
                path.appendOval(in: NSRect(x: cx - 17, y: cy - 17, width: 34, height: 34))
            }
            path.appendRoundedRect(NSRect(x: orbCenter.x - 48, y: orbOrigin.y + 8, width: 110, height: 28), xRadius: 14, yRadius: 14)
        }

        if uiState.projectPanelOpen {
            path.appendRoundedRect(
                NSRect(
                    x: shellPadding,
                    y: size.height - shellPadding - 204,
                    width: 198,
                    height: 204
                ),
                xRadius: 18,
                yRadius: 18
            )
        }

        if uiState.hasCaption {
            path.appendRoundedRect(
                NSRect(
                    x: orbCenter.x - 104,
                    y: orbOrigin.y - 74,
                    width: 208,
                    height: 64
                ),
                xRadius: 16,
                yRadius: 16
            )
        }

        return path
    }
}

final class OverlayMessageHandler: NSObject, WKScriptMessageHandler {
    weak var controller: OverlayViewController?

    init(controller: OverlayViewController) {
        self.controller = controller
    }

    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        controller?.handleMessage(name: message.name, body: message.body)
    }
}

final class OverlayViewController: NSViewController {
    private let rootURL: URL
    private let stateURL: URL
    private weak var webView: WKWebView?
    private weak var fallbackLabel: NSTextField?
    private weak var hitTestView: OverlayHitTestView?
    private var messageHandler: OverlayMessageHandler?

    init(rootURL: URL, stateURL: URL) {
        self.rootURL = rootURL
        self.stateURL = stateURL
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        return nil
    }

    override func loadView() {
        let root = OverlayHitTestView(frame: NSRect(x: 0, y: 0, width: 360, height: 300))
        root.wantsLayer = true
        root.layer?.backgroundColor = NSColor(calibratedWhite: 1.0, alpha: 0.001).cgColor
        view = root
        hitTestView = root
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        let contentController = WKUserContentController()
        let bootstrap = """
        window.__AUDIOCLAW_OVERLAY_BRIDGE__ = {
          getInitialState: async () => window.webkit.messageHandlers.overlayGetState.postMessage({}),
          triggerSatellite: async (action) => window.webkit.messageHandlers.overlaySatellite.postMessage({ action }),
          triggerProjectAction: async (payload) => window.webkit.messageHandlers.overlayProject.postMessage(payload),
          setVoice: async (voiceId) => window.webkit.messageHandlers.overlayVoice.postMessage({ voiceId })
        };
        """
        let script = WKUserScript(source: bootstrap, injectionTime: .atDocumentStart, forMainFrameOnly: true)
        contentController.addUserScript(script)

        let configuration = WKWebViewConfiguration()
        configuration.userContentController = contentController
        configuration.preferences.setValue(true, forKey: "developerExtrasEnabled")

        let handler = OverlayMessageHandler(controller: self)
        messageHandler = handler
        contentController.add(handler, name: "overlayGetState")
        contentController.add(handler, name: "overlaySatellite")
        contentController.add(handler, name: "overlayProject")
        contentController.add(handler, name: "overlayVoice")
        contentController.add(handler, name: "overlayUIState")

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.setValue(false, forKey: "drawsBackground")
        webView.wantsLayer = true
        webView.layer?.backgroundColor = NSColor.clear.cgColor
        view.addSubview(webView)
        NSLayoutConstraint.activate([
            webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            webView.topAnchor.constraint(equalTo: view.topAnchor),
            webView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
        self.webView = webView

        let fallback = NSTextField(labelWithString: "正在加载 React 浮窗…")
        fallback.font = .systemFont(ofSize: 16, weight: .medium)
        fallback.textColor = NSColor(calibratedWhite: 0.25, alpha: 1.0)
        fallback.alignment = .center
        fallback.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(fallback)
        NSLayoutConstraint.activate([
            fallback.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            fallback.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
        fallbackLabel = fallback

        loadFrontend()
    }

    private func loadFrontend() {
        let indexURL = rootURL.appendingPathComponent("index.html")
        guard var html = try? String(contentsOf: indexURL, encoding: .utf8) else {
            fallbackLabel?.stringValue = "React 构建产物读取失败"
            return
        }

        let cssPattern = #"href="\.\/(assets\/[^"]+\.css)""#
        let jsPattern = #"src="\.\/(assets\/[^"]+\.js)""#
        let cssPath = matchFirst(in: html, pattern: cssPattern)
        let jsPath = matchFirst(in: html, pattern: jsPattern)

        if let cssPath {
            let cssURL = rootURL.appendingPathComponent(cssPath)
            if let css = try? String(contentsOf: cssURL, encoding: .utf8) {
                html = html.replacingOccurrences(
                    of: #"<link rel="stylesheet" crossorigin href="./\#(cssPath)"></link>"#,
                    with: "<style>\(css)</style>"
                )
                html = html.replacingOccurrences(
                    of: #"<link rel="stylesheet" crossorigin href="./\#(cssPath)">"#,
                    with: "<style>\(css)</style>"
                )
            }
        }

        if let jsPath {
            let jsURL = rootURL.appendingPathComponent(jsPath)
            if let js = try? String(contentsOf: jsURL, encoding: .utf8) {
                html = html.replacingOccurrences(
                    of: #"<script type="module" crossorigin src="./\#(jsPath)"></script>"#,
                    with: "<script type=\"module\">\(js)</script>"
                )
            }
        }

        webView?.loadHTMLString(html, baseURL: rootURL)

        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) { [weak self] in
            self?.webView?.evaluateJavaScript("document.body.innerText.length") { result, _ in
                DispatchQueue.main.async {
                    if let length = result as? Int, length > 0 {
                        self?.fallbackLabel?.isHidden = true
                    } else {
                        self?.fallbackLabel?.stringValue = "React 页面未成功渲染"
                    }
                }
            }
        }
    }

    private func matchFirst(in text: String, pattern: String) -> String? {
        guard let regex = try? NSRegularExpression(pattern: pattern) else {
            return nil
        }
        let range = NSRange(text.startIndex..., in: text)
        guard let match = regex.firstMatch(in: text, range: range),
              match.numberOfRanges > 1,
              let captureRange = Range(match.range(at: 1), in: text)
        else {
            return nil
        }
        return String(text[captureRange])
    }

    func handleMessage(name: String, body: Any) {
        switch name {
        case "overlayGetState":
            dispatchState()
        case "overlaySatellite":
            print("[overlay:satellite] \(body)")
        case "overlayProject":
            print("[overlay:project] \(body)")
        case "overlayVoice":
            print("[overlay:voice] \(body)")
        case "overlayUIState":
            if let dict = body as? [String: Any] {
                var state = OverlayUIState()
                state.hover = dict["hover"] as? Bool ?? false
                state.projectPanelOpen = dict["projectPanelOpen"] as? Bool ?? false
                state.hasCaption = dict["hasCaption"] as? Bool ?? true
                hitTestView?.uiState = state
            }
        default:
            break
        }
    }

    func dispatchState() {
        let payload = initialStateJSON()
        let script = """
        window.dispatchEvent(new CustomEvent('audioclaw:overlay-state', { detail: \(payload) }));
        """
        webView?.evaluateJavaScript(script)
    }

    func initialStateJSON() -> String {
        let payload: [String: Any] = [
            "status": "待命中",
            "hover": false,
            "projectPanelOpen": false,
            "selectedProjectId": "run-1",
            "voiceId": "female_0006_a",
            "voices": [
                ["id": "female_0006_a", "label": "女声 A"],
                ["id": "male_0004_a", "label": "男声 A"],
                ["id": "male_0018_a", "label": "男声 B"]
            ],
            "previousLine": "SenseAudio 已确认上一句字幕",
            "currentLine": "React + AppKit/WKWebView 原生壳预览已启动",
            "projects": [
                ["id": "run-1", "title": "4月7日 产品评审会议", "updatedAt": "10:42", "state": "organized"],
                ["id": "run-2", "title": "双语字幕视频测试", "updatedAt": "09:18", "state": "draft"]
            ]
        ]
        let data = try? JSONSerialization.data(withJSONObject: payload, options: [])
        return String(data: data ?? Data("{}".utf8), encoding: .utf8) ?? "{}"
    }

    func restoreWindowState(_ window: NSWindow) {
        guard let data = try? Data(contentsOf: stateURL),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let x = payload["x"] as? CGFloat,
              let y = payload["y"] as? CGFloat,
              let width = payload["width"] as? CGFloat,
              let height = payload["height"] as? CGFloat
        else {
            centerWindow(window)
            return
        }
        let requested = NSRect(x: x, y: y, width: width, height: height)
        if let visible = NSScreen.main?.visibleFrame, visible.intersects(requested) {
            window.setFrame(requested, display: true)
        } else {
            centerWindow(window)
        }
    }

    func saveWindowState() {
        guard let window = view.window else { return }
        let frame = window.frame
        let payload: [String: CGFloat] = [
            "x": frame.origin.x,
            "y": frame.origin.y,
            "width": frame.width,
            "height": frame.height
        ]
        if let data = try? JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted]) {
            try? data.write(to: stateURL)
        }
    }

    func centerWindow(_ window: NSWindow) {
        let visible = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let size = NSSize(width: 382, height: 250)
        let origin = NSPoint(x: visible.midX - size.width / 2, y: visible.midY - size.height / 2)
        window.setFrame(NSRect(origin: origin, size: size), display: true)
        saveWindowState()
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate, NSWindowDelegate {
    var window: OverlayHostWindow?
    var controller: OverlayViewController?

    func applicationDidFinishLaunching(_ notification: Notification) {
        let root = URL(fileURLWithPath: CommandLine.arguments.dropFirst().first ?? "")
        guard root.isFileURL else {
            NSApp.terminate(nil)
            return
        }
        let stateURL = root.appendingPathComponent(".overlay_webview_state.json")
        let controller = OverlayViewController(rootURL: root, stateURL: stateURL)
        self.controller = controller

        let window = OverlayHostWindow(
            contentRect: NSRect(x: 240, y: 180, width: 382, height: 250),
            styleMask: [.borderless, .resizable],
            backing: .buffered,
            defer: false
        )
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = false
        window.level = .floating
        window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        window.isMovableByWindowBackground = true
        window.contentViewController = controller
        window.delegate = self
        controller.restoreWindowState(window)
        window.orderFrontRegardless()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        self.window = window
    }

    func windowDidMove(_ notification: Notification) {
        controller?.saveWindowState()
    }

    func windowDidEndLiveResize(_ notification: Notification) {
        controller?.saveWindowState()
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
