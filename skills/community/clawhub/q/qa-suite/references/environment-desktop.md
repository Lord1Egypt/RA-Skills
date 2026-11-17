# Desktop Test Environment Setup

## Electron

```bash
npm install --save-dev vitest                      # Main + renderer process
npm install --save-dev @testing-library/react jsdom  # Renderer components
npm install --save-dev @playwright/test            # E2E (built-in Electron support)

# Playwright with Electron:
# const electronApp = await electron.launch({ args: ['.'] });
```

**Strategy**:
- Main process: Pure Node.js tests
- Renderer process: jsdom + Testing Library or Playwright
- IPC communication: Mock via `electron-mock-ipc`
- E2E: Playwright with Electron support

## Tauri

```bash
cargo test                          # Rust backend unit
cargo test --test integration_test  # Rust integration (tests/ directory)

npm install --save-dev vitest @testing-library/react jsdom  # Frontend

# E2E: Tauri test harness for real app testing
```

## macOS Native (Swift/AppKit)

```bash
xcodebuild test -scheme MyApp -destination 'platform=macOS'
# XCUITest also supports macOS
```

## Windows Native

- **C#/.NET**: MSTest or NUnit, run via `dotnet test`
- **C++**: Catch2 or Google Test, run via `ctest` (CMake + CTest)

## Headless Mode Limitations

- **Electron**: Playwright supports headless Electron
- **Tauri**: Frontend can be headless (jsdom), Rust backend needs no display
- **macOS native**: XCTest supports headless
- **Windows native**: Most frameworks support headless

## CI Requirements

- **Electron**: Ubuntu runner + `xvfb-run` (virtual display)
- **Tauri**: Rust + Node.js, Ubuntu runner usually sufficient
- **macOS**: Requires macOS runner (GitHub Actions has them)
- **Windows**: Requires Windows runner

## No Desktop Environment Fallback

If CI lacks desktop environment:
1. Backend/business logic tests run on standard CI
2. UI tests marked as manual
3. Mock IPC channels for frontend-backend communication logic
