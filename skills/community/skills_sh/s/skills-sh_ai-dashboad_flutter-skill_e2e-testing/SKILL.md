---
name: e2e-testing
description: "AI-powered E2E testing for any app — Flutter, React Native, iOS, Android, Electron, Tauri, KMP, .NET MAUI. Connects via MCP to running apps so the agent can take screenshots, tap elements, enter text, scroll, inspect UI trees, and verify state with natural language. Use when the user wants to test an app's UI end-to-end, automate cross-platform testing, run smoke tests, validate form flows, or verify navigation without writing test code."
---

# AI E2E Testing — 8 Platforms, Zero Test Code

flutter-skill is an MCP server that connects AI agents to running apps across 8 platforms. The agent takes screenshots, taps elements, enters text, scrolls, navigates, inspects UI trees, and verifies state — all through natural language.

## Supported Platforms

| Platform | Setup |
|----------|-------|
| Flutter (iOS/Android/Web) | `flutter pub add flutter_skill` |
| React Native | `npm install flutter-skill-react-native` |
| Electron | `npm install flutter-skill-electron` |
| iOS (Swift/UIKit) | SPM: `FlutterSkillSDK` |
| Android (Kotlin) | Gradle: `flutter-skill-android` |
| Tauri (Rust) | `cargo add flutter-skill-tauri` |
| KMP Desktop | Gradle dependency |
| .NET MAUI | NuGet package |

## Install

```bash
# npm (recommended)
npm install -g flutter-skill

# Homebrew
brew install ai-dashboad/flutter-skill/flutter-skill

# Or download binary from GitHub Releases
```

## MCP Configuration

Add to your AI agent's MCP config (Claude Desktop, Cursor, Windsurf, OpenClaw, etc.):

```json
{
  "mcpServers": {
    "flutter-skill": {
      "command": "flutter-skill",
      "args": ["server"]
    }
  }
}
```

## Quick Start

### 1. Initialize your app (one-time)

```bash
flutter-skill init
```

Auto-detects project type and patches your app with the testing bridge.

**Verify:** Output should confirm the project type was detected and main entry point was patched. If it fails, check that you are in the project root and the framework is supported.

### 2. Launch and connect

```bash
flutter-skill launch .
```

**Verify:** A VM Service URI appears in the output (e.g. `ws://127.0.0.1:50000/ws`). If no URI appears, check that Flutter/the target framework is installed and the app compiles.

### 3. Test with natural language

The agent follows this core loop:

1. `screenshot()` — see the current screen
2. `inspect_interactive()` — discover all tappable/typeable elements with semantic refs
3. `tap(ref: "button:Login")` — tap using stable semantic reference
4. `enter_text(ref: "input:Email", text: "admin@test.com")` — type into field
5. `wait_for_element(key: "Dashboard")` — verify navigation succeeded
6. `screenshot()` — confirm final state

**If `inspect_interactive()` returns no elements:** Take a screenshot to confirm the screen loaded, then check `get_logs()` for errors. The app may still be loading — retry after a short wait.

## Available MCP Tools

### Core Actions
| Tool | Description |
|------|-------------|
| `screenshot` | Capture current screen as image |
| `tap` | Tap element by key, text, ref, or coordinates |
| `enter_text` | Type text into a field |
| `scroll` | Scroll up/down/left/right |
| `swipe` | Swipe gesture between points |
| `long_press` | Long press an element |
| `drag` | Drag from point A to B |
| `go_back` | Navigate back |
| `press_key` | Send keyboard key events |

### Inspection
| Tool | Description |
|------|-------------|
| `inspect_interactive` | Get all interactive elements with semantic ref IDs |
| `get_elements` | List all elements on screen |
| `find_element` | Find element by key or text |
| `wait_for_element` | Wait for element to appear (with timeout) |
| `get_element_properties` | Get detailed properties of an element |

### Text Manipulation
| Tool | Description |
|------|-------------|
| `set_text` | Replace text in a field |
| `clear_text` | Clear a text field |
| `get_text` | Read text content |

### App Control
| Tool | Description |
|------|-------------|
| `get_logs` | Read app logs |
| `clear_logs` | Clear log buffer |

## Semantic Refs

`inspect_interactive` returns elements with stable semantic reference IDs:

```
button:Login          → Login button
input:Email           → Email text field
toggle:Dark Mode      → Dark mode switch
button:Submit[1]      → Second Submit button (disambiguated)
```

Format: `{role}:{content}[{index}]`

7 roles: `button`, `input`, `toggle`, `slider`, `select`, `link`, `item`

Use refs for reliable element targeting that survives UI changes:
```
tap(ref: "button:Login")
enter_text(ref: "input:Email", text: "test@example.com")
```

## Testing Workflow

### Core Loop
```
screenshot() → inspect_interactive() → tap/enter_text → screenshot() → verify
```

Always call `screenshot()` before and after actions. Use `wait_for_element()` after navigation — apps need time to transition.

### Validation Checkpoints

- **After `screenshot()`**: Confirm the expected screen is visible before acting.
- **After `tap()` or `enter_text()`**: Call `screenshot()` to verify the UI responded.
- **After navigation**: Use `wait_for_element(key: "target_screen")` with a timeout. If it times out, call `screenshot()` and `get_logs()` to diagnose.
- **On unexpected state**: Call `get_logs()` and `inspect_interactive()` to understand what elements are present.

### Element Targeting Priority

1. **`ref:`** (most reliable) — semantic ref from `inspect_interactive()`
2. **`key:`** — widget key set by the developer
3. **`text:`** — visible text content (fragile if text changes)
4. **Coordinates** — last resort, breaks on different screen sizes

## Links

- [GitHub](https://github.com/ai-dashboad/flutter-skill)
- [npm](https://www.npmjs.com/package/flutter-skill)
- [Documentation](https://github.com/ai-dashboad/flutter-skill/blob/main/docs/USAGE_GUIDE.md)
- [pub.dev](https://pub.dev/packages/flutter_skill)
- [VSCode Extension](https://marketplace.visualstudio.com/items?itemName=AIDashboard.flutter-skill)
