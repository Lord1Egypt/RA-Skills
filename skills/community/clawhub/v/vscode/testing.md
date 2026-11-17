# Testing — Discovery, Running One Test, and Coverage in the Gutter

The Test Explorer is a UI over a framework's own discovery. When it shows nothing, the framework refused to collect — and the reason is printed in an output channel almost nobody opens.

**Contents:** [The Discovery Chain](#the-discovery-chain) · [Reading The Failure](#reading-the-failure) · [Per-Framework Setup](#per-framework-setup) · [Debugging A Single Test](#debugging-a-single-test) · [Coverage](#coverage) · [Tests In A Container Or Remote](#tests-in-a-container-or-remote) · [Tasks Versus Test Explorer](#tasks-versus-test-explorer) · [Testing Failure Signatures](#testing-failure-signatures)

**Before wiring tests for a repo**, read `## Projects` in `~/Clawic/data/vscode/memory.md` for its test framework and interpreter, and open any `artifacts/` file its `## Boxes` index names for this repo's test setup. `language_stack` in `config.yaml` records the user's framework per language.

## The Discovery Chain

Every framework integration does the same four steps, and a failure is always at one of them:

1. **Resolve the runtime** — interpreter, node version, toolchain. Wrong runtime means imports fail before a test is seen (`languages.md`).
2. **Resolve the working directory** — usually the workspace folder, which is wrong in a monorepo where the framework config lives one level down.
3. **Run the framework's collection step** — `pytest --collect-only`, the runner's list mode, `go test -list`, `cargo test -- --list`.
4. **Parse the result into the tree.**

Steps 1-3 are the framework's problem and produce framework error messages. Only step 4 is the editor's, and it rarely fails. So: read the collection error, do not reconfigure the extension.

## Reading The Failure

- Open the extension's output channel (`Output` panel → the test extension's name, or `Python`, `Testing`, the runner's own channel). The collection command and its stderr are printed there verbatim.
- Copy that exact command into the integrated terminal and run it. If it fails there too, the editor is innocent and the fix is in the project.
- If it succeeds in the terminal and fails in the editor, the difference is the environment or the working directory — the two things the terminal inherits and the extension resolves for itself (`terminal.md`).

## Per-Framework Setup

| Stack | Enable with | The usual break |
|---|---|---|
| pytest | `python.testing.pytestEnabled: true`, `python.testing.pytestArgs: ["tests"]` | An import error in `conftest.py` fails collection for the whole tree, and the tree just looks empty |
| unittest | `python.testing.unittestEnabled: true` with pattern args | Only one of pytest and unittest may be enabled; both on means neither behaves |
| Jest | Framework extension, project root at the `jest.config` | Monorepo — the extension must be told each project root, or it runs the root config against every package |
| Vitest | Framework extension | A workspace-mode config (`vitest.workspace.ts`) that the extension needs pointed at explicitly |
| Mocha | Framework extension or a task | No standard discovery protocol; a task with a problem matcher is often simpler (`tasks.md`) |
| Go | Go extension, built in | Test caching returns instantly with stale results; `-count=1` in the test flags forces a real run |
| Rust | rust-analyzer, run/debug lenses above each `#[test]` | Integration tests in `tests/` need the crate built; the lens is missing until the first successful build |
| Java | Test runner in the language pack | A stale compiled class runs instead of the edited source |
| .NET | C# extension | Test project must be part of the loaded solution |

## Debugging A Single Test

This is the highest-leverage feature in the panel and the reason to wire discovery at all.

- Right-click a test in the explorer, or use the gutter icon, and choose Debug. The framework's own arguments are used — no `launch.json` needed, and no risk of the config drifting from how CI runs the suite.
- Breakpoints bind in test files and in the code under test. If they stay hollow, it is the same path problem as anywhere else (`debugging.md`).
- For pytest, `justMyCode: false` is needed to break inside a fixture provided by a plugin; the setting lives under the Python extension's debug configuration, not in the test config.
- `Test: Debug Test at Cursor` runs the innermost test containing the caret — the fastest loop when iterating on one failing case.
- A test that passes in the explorer and fails in CI is an environment difference; run the *collection command from the output channel* in a clean shell before suspecting the test.

## Coverage

- The Test Explorer renders coverage inline — line highlighting in the gutter and a coverage tree — when the test extension implements the editor's coverage API. Extensions that do not simply have no coverage action; there is no setting to enable it.
- For frameworks whose extension has no coverage support, generate an LCOV report from the test command and use a coverage-viewer extension. That path is a file watcher over `lcov.info`, so a stale file shows stale coverage — delete it as part of the test task.
- Branch coverage numbers differ between the framework's reporter and the editor's rendering when the reporter emits statement coverage only. Trust the reporter's summary for a number, the gutter for a location.

## Tests In A Container Or Remote

- Tests run wherever the workspace extension host runs. In a dev container, the test extension, the framework and the interpreter all live inside the container — installing the test extension locally does nothing (`remote.md`, SKILL.md Rule 8).
- A test suite that needs a database is a compose concern, not an editor one: the container the editor attaches to must be able to reach it by service name.
- Over SSH with a slow filesystem, discovery on every save is expensive. Most extensions expose a "discover on save" toggle; turning it off and discovering manually is the usual fix for an editor that stutters in a large remote repo (`performance.md`).

## Tasks Versus Test Explorer

Use the explorer when: you want per-test running, gutter status, and one-click debugging of a single case.

Use a task instead when: the suite is a single command with useful output, the framework has no integration, or you need the exact CI invocation. A test task with a problem matcher puts failures in the Problems panel and is often enough (`tasks.md`). Mark it `"group": {"kind": "test", "isDefault": true}` so `Tasks: Run Test Task` finds it.

Both at once is fine and common: the explorer for the inner loop, the task for the full run.

## Testing Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Explorer empty, no error shown | Collection failed; the error is in the output channel | Read the channel, run the printed command |
| Some tests found, one directory missing | Collection error in that directory's conftest/setup file | The framework prints it; the tree cannot |
| Tests found, all fail on import | Wrong interpreter or wrong working directory | Steps 1-2 of the discovery chain |
| Passes in explorer, fails in terminal | Different environment or cwd | Compare the two commands directly |
| Debug runs the whole suite | Debugging via a launch config rather than the explorer's per-test action | Use the gutter/explorer action |
| Breakpoint in a fixture never hits | `justMyCode` filtering library frames | Turn it off for that session |
| Results never refresh | Framework caching (Go `-count=1`), or a stale compiled artifact | Force a real run |
| Monorepo runs the wrong project's tests | One root config applied to every package | Configure per-project roots in the extension |
| Anything else | Run the framework's own list/collect command in the integrated terminal | — |

**When test discovery finally works for a repo**, record the framework, the interpreter and the working directory in `## Projects` of `~/Clawic/data/vscode/memory.md`, and if the setup needed a non-obvious configuration — per-project roots in a monorepo, a collection flag, a container-side install — write it to `~/Clawic/data/vscode/artifacts/tests-<repo>.md` with its `## Boxes` line in the same turn (`memory-template.md`). A discovery failure whose cause was not obvious earns a line in `## Pain Points`: the empty tree looks identical whatever caused it, so the note is the only thing that shortens the second occurrence.
