# Testing: Rust Unit Tests, Frontend Mocks, WebDriver E2E

**Sources:**
- https://v2.tauri.app/develop/tests/
- https://v2.tauri.app/develop/tests/mocking/
- https://v2.tauri.app/develop/tests/webdriver/
- https://docs.rs/tauri/latest/tauri/test/index.html

Tauri v2 splits testing into three tiers. Use all three for a real app — they cover different failure classes and none of them substitutes for another.

| Tier | What it verifies | Speed | Tooling |
|---|---|---|---|
| Rust unit/integration tests | Command logic, state mutations, business logic — no webview at all | Fastest | `cargo test` + `tauri::test::mock_builder` |
| Frontend unit tests with `mockIPC` | Frontend code that calls `invoke`/listens to events, without a real backend | Fast | Vitest/Jest + `@tauri-apps/api/mocks` |
| WebDriver E2E | Real webview + real Rust backend + real IPC bridge, actual UI interaction | Slowest | `tauri-driver` + WebdriverIO (`@wdio/tauri-service`) or Selenium |

## Tier 1 — Rust-side testing with the mock runtime

`tauri::test` provides a `MockRuntime` so you can build a real `App`/`WebviewWindow` and dispatch IPC calls into it, entirely in `cargo test`, with no native webview libraries executed.

```rust
use tauri::test::{mock_builder, mock_context, noop_assets};

#[tauri::command]
fn ping() -> &'static str { "pong" }

fn create_app<R: tauri::Runtime>(builder: tauri::Builder<R>) -> tauri::App<R> {
    builder
        .invoke_handler(tauri::generate_handler![ping])
        .build(tauri::generate_context!())
        .expect("failed to build app")
}

#[test]
fn ping_returns_pong() {
    let app = create_app(mock_builder());
    let webview = tauri::WebviewWindowBuilder::new(&app, "main", Default::default())
        .build()
        .unwrap();

    let res = tauri::test::get_ipc_response(
        &webview,
        tauri::webview::InvokeRequest {
            cmd: "ping".into(),
            callback: tauri::ipc::CallbackFn(0),
            error: tauri::ipc::CallbackFn(1),
            url: "http://tauri.localhost".parse().unwrap(),
            body: tauri::ipc::InvokeBody::default(),
            headers: Default::default(),
            invoke_key: tauri::test::INVOKE_KEY.into(),
        },
    );
    assert!(res.is_ok());
}
```

Use this tier for: command logic that depends on `AppHandle`/`Window`/`State`, permission-adjacent behavior you want covered by an actual `App` instance rather than a bare function call, and anything where you want CI to catch "I forgot to register this command in `generate_handler!`" — a plain `#[test] fn` calling the Rust function directly won't catch that, but exercising it through `get_ipc_response` will.

For pure business logic with no Tauri-specific types involved, skip the mock runtime ceremony entirely and just unit-test the function directly — reserve `mock_builder`/`get_ipc_response` for testing the actual command-dispatch path.

## Tier 2 — Frontend unit tests with `mockIPC`

```ts
import { beforeAll, expect, test, vi } from "vitest";
import { randomFillSync } from "crypto";
import { mockIPC } from "@tauri-apps/api/mocks";
import { invoke } from "@tauri-apps/api/core";

// jsdom has no WebCrypto implementation by default — Tauri's mock layer needs it
beforeAll(() => {
  // @ts-ignore
  window.crypto = { getRandomValues: (buffer) => randomFillSync(buffer) };
});

test("invoke add", async () => {
  mockIPC((cmd, args) => {
    if (cmd === "add") return args.a + args.b;
  });
  const spy = vi.spyOn(window, "__TAURI_IPC__");
  await expect(invoke("add", { a: 12, b: 15 })).resolves.toBe(27);
  expect(spy).toHaveBeenCalled();
});
```

Runs in jsdom — no native webview, no Rust process, fast enough for a tight test-watch loop. This is what you reach for to test frontend logic (a hook, a store action, a component) that calls `invoke()`, without standing up the whole app.

### Mocking events

```ts
import { mockIPC } from "@tauri-apps/api/mocks";
// simulate the backend emitting an event your frontend listens for —
// use mockIPC's window.__TAURI_EVENT_PLUGIN_INTERNALS__ hooks or trigger your
// listen() callback directly in the test, depending on what you're isolating.
```

### Mocking sidecar/shell output

```ts
mockIPC(async (cmd, args) => {
  if (args.message.cmd === 'execute') {
    const eventCallbackId = `_${args.message.onEventFn}`;
    const eventEmitter = window[eventCallbackId];
    eventEmitter({ event: 'Stdout', payload: 'some data sent from the process' });
    eventEmitter({ event: 'Terminated', payload: { code: 0, signal: null } }); // must fire last to resolve the promise
  }
});
```

`mockIPC` fakes `invoke` under a mock runtime — it never touches a real webview or Rust backend. For an equivalent mock while running against a **real** app in an E2E context, use `@wdio/tauri-service`'s `browser.tauri.mock()` (Tier 3).

## Tier 3 — WebDriver E2E

The recommended v2 path is **WebdriverIO + `@wdio/tauri-service`**, which works across Windows, Linux, and macOS. By default it runs an embedded WebDriver server inside your app itself, so no external driver binary is required on any platform — including macOS, which has no standalone desktop WebDriver client (this is why plain `tauri-driver` + Selenium historically didn't support macOS, and why the service-based approach is the current recommendation over raw `tauri-driver`).

`@wdio/tauri-service` gives you:
- `browser.tauri.execute()` — run arbitrary Tauri API calls from the test.
- Command (IPC) mocking equivalent to `mockIPC`, but against the real running app.
- Frontend + backend log capture in one place.
- Multiremote support (drive more than one window/instance in one test).

### What E2E actually catches that mocks don't

Real IPC-permission failures (a capability misconfiguration that `mockIPC` would happily let through since it doesn't enforce capabilities at all), real window creation/deadlock issues (SKILL.md rule 7), real sidecar spawn/argument-validation behavior, and actual rendered-DOM correctness. If a bug report is "works in dev, breaks in the built app" or "works with mocks, breaks for real," it's very often a capability/permission mismatch or a platform-specific windowing quirk — exactly the class of bug Tier 1/2 tests cannot see.

### CI integration sketch

```yaml
jobs:
  e2e:
    strategy:
      matrix: { platform: [ubuntu-latest, windows-latest] }
    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/setup-node@v4
      - run: npm install
      - run: npm run tauri build -- --debug   # or the appropriate dev/test build
      - run: npx wdio run wdio.conf.ts
```

macOS is intentionally covered above too via the platform matrix pattern even though it needs no separate driver install, since `@wdio/tauri-service`'s embedded-server approach is what makes that possible — don't assume macOS needs to be excluded from the E2E matrix the way it historically did with raw `tauri-driver`.

## Testing strategy guidance

- Put the bulk of your test *count* in Tier 1 (cheap, fast, catches logic bugs) and Tier 2 (cheap, fast, catches frontend-integration bugs).
- Keep Tier 3 for a **smaller set of critical user flows** (first-run, the core "does the app do its main job" path, update-check flow) — it's slow and flakier by nature (real OS windowing), so it doesn't scale to exhaustive coverage the way the lower tiers do.
- Don't skip Tier 3 entirely on the theory that Tiers 1+2 "probably cover it" — capability misconfigurations (the most common real-world Tauri v2 bug class per `references/security-capabilities.md`) are specifically invisible to `mockIPC`, since mocks don't enforce the permission system at all.
