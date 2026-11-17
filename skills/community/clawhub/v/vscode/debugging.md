# Debugging — launch.json, Attach, and the Hollow Breakpoint

The debug adapter knows nothing about your folder. It knows the paths recorded inside the code it loaded. Every hard debugging problem in this editor is the gap between those two.

**Contents:** [Launch Versus Attach](#launch-versus-attach) · [Anatomy Of A Config](#anatomy-of-a-config) · [The Hollow Breakpoint](#the-hollow-breakpoint) · [Node And The Browser](#node-and-the-browser) · [Python](#python) · [Go, Rust, C And C++, Java](#go-rust-c-and-c-and-java) · [Compounds And Multi-Process](#compounds-and-multi-process) · [Breakpoint Types](#breakpoint-types) · [Debugging Over SSH And In Containers](#debugging-over-ssh-and-in-containers) · [Debug Failure Signatures](#debug-failure-signatures)

**Before writing a debug config for a repo that already has one**, read `## Projects` in `~/Clawic/data/vscode/memory.md` and open any `artifacts/launch-*.md` its `## Boxes` index names — the path mapping and the port for this repo were solved once already. `remote_mode` in `config.yaml` decides whether the target is local, in a container, or over SSH.

## Launch Versus Attach

| | Launch | Attach |
|---|---|---|
| Who starts the process | The debugger | You, or a supervisor, a compose file, a watcher |
| Restart semantics | Full restart on every F5 | The process outlives the debug session |
| Right for | Scripts, tests, single-shot CLI runs | Servers, containers, anything with a slow boot, anything a framework's own reloader manages |
| Failure mode | The debugger's environment differs from your shell's | The port is not open, or the process was not started with the inspector flag |

Default to **attach** for anything long-running. A launch config for a dev server duplicates the framework's own reloading and produces two processes fighting over a port. The pattern that works: the framework starts the app with its inspector flag; the editor attaches; the framework's reloader keeps working.

## Anatomy Of A Config

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to API",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true,
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app",
      "skipFiles": ["<node_internals>/**", "**/node_modules/**"]
    }
  ]
}
```

- `type` names the debug extension, not the language. A missing extension makes F5 report "configured debug type is not supported" — install the debugger, not the language extension.
- `cwd` defaults to `${workspaceFolder}`, never the folder holding `launch.json`. Relative paths in `args` resolve from `cwd`.
- `restart: true` on an attach config reconnects after the process restarts — the difference between a usable and an unusable watch loop.
- `skipFiles` is what makes step-into land in your code instead of a framework's stack. Without it, stepping through an async call is unusable.
- `env` and `envFile` add to, not replace, the inherited environment. Secrets belong in `envFile` pointing at a gitignored file, never inline in a committed `launch.json`.
- `presentation: {"hidden": true, "group": "…", "order": n}` keeps helper configs out of the dropdown. A dropdown with fifteen entries is a config file nobody maintains.
- `"type": "node"` with `"request": "launch"` and `"runtimeExecutable"` is how you debug through a package manager script or a runner (`tsx`, `ts-node`, `nodemon`) rather than reimplementing it.

## The Hollow Breakpoint

A grey or hollow breakpoint means: the adapter has no loaded script whose source path matches this file. It is a mapping failure, and the diagnosis is always the same three questions.

1. **Did the code load at all?** A breakpoint in a module that is never imported stays hollow forever and is not a bug.
2. **What path did the runtime record?** Print it from the debug console — `__filename` in Node, `__file__` in Python, the module's `__spec__.origin`. Compare it character by character with the on-disk path.
3. **Is a sourcemap in play?** Transpiled code carries a `sourceMappingURL`. If the map's `sources` entries are relative to a build directory that no longer matches the layout, the mapping resolves to a file that does not exist.

The fixes, by runtime:

| Runtime | Knob | What it maps |
|---|---|---|
| Node | `localRoot` / `remoteRoot` | Disk path ↔ path inside the container or remote host |
| Node | `sourceMapPathOverrides` | Sourcemap `sources` entries ↔ disk paths, glob-based |
| Node | `outFiles` | Where the adapter looks for compiled output; a wrong glob means no maps are read at all |
| Python | `pathMappings: [{"localRoot": "${workspaceFolder}", "remoteRoot": "/app"}]` | Disk path ↔ path inside the container |
| Browser | `webRoot` | URL path ↔ disk path for served assets |
| Any | `"sourceMaps": true` plus a build that emits them | Turning maps off in the build for speed is the cause more often than the config |

Two extra causes worth checking before reaching for mappings: the file on disk has been edited since the process started (the adapter maps by content in some runtimes and refuses to bind), and case sensitivity on macOS — a case-insensitive filesystem happily opens `Src/app.ts` while the map says `src/app.ts`, and the paths do not match as strings.

## Node And The Browser

- **Auto Attach** (`debug.javascript.autoAttachFilter`): `smart` attaches to scripts outside `node_modules` run from the integrated terminal, `always` to everything, `onlyWithFlag` only when `--inspect` is present, `disabled` never. `smart` is the right default; `always` makes every `npm install` a debug session.
- The **JavaScript Debug Terminal** attaches to whatever you run in it with no config at all. It is the fastest path to a one-off debug session and requires no `launch.json`.
- Inspector ports: `--inspect` waits for nothing, `--inspect-brk` pauses on the first line. Use `-brk` when the bug is in startup; otherwise the process is past the interesting part before you connect.
- In a container, the inspector must bind `0.0.0.0`: `--inspect=0.0.0.0:9229`. Bound to localhost inside the container, it is unreachable from the host no matter what the port mapping says.
- **Browser debugging**: `"type": "chrome"` or `"msedge"`, `request: launch` opens a fresh profile (no extensions, no logged-in session) while `request: attach` needs the browser started with a remote-debugging port. `webRoot` maps the served URL back to disk; a dev server serving from memory needs the bundler's sourcemap setting, not a different `webRoot`.
- `"serverReadyAction"` opens the browser automatically when a pattern appears in the output — the tidiest full-stack setup, paired with a compound.

## Python

- Interpreter selection is not a setting: it is stored per workspace by the Python extension and is what the debugger uses. Changing `python.defaultInterpreterPath` after a selection exists changes nothing (`languages.md`).
- `justMyCode: true` is the default and skips library frames. Turn it off to break inside a dependency, and remember to turn it back on — with it off, an exception in a framework stops there instead of in your handler.
- `"module": "uvicorn"` with `args` beats `"program": ".../uvicorn"`: it uses the selected interpreter's module resolution and survives a virtualenv move.
- Remote attach uses `debugpy.listen()` in the process plus a `connect` block in the config; `pathMappings` is mandatory whenever the code lives at a different path in the target.
- Django and Flask: use the framework's own template of `"django": true` / `"jinja": true` so template exceptions map back to template files, and disable the framework's auto-reloader (`--noreload`, `use_reloader=False`) or the reloaded child process is not the one being debugged.
- Pytest: debug a single test from the Test Explorer rather than a launch config; discovery already knows the arguments (`testing.md`).

## Go, Rust, C And C++, Java

- **Go**: Delve is the adapter. `"mode": "debug"` builds and runs, `"mode": "test"` debugs the package's tests, `"mode": "remote"` attaches to a `dlv --headless` process. Optimizations must be off (`-gcflags="all=-N -l"`, which the extension passes by default) or variables read as optimized out.
- **Rust**: use CodeLLDB rather than the MS C++ adapter on macOS and Linux — better Rust type formatting. Build with a debug profile; a release binary has no usable line table. `sourceMap` maps the crate registry path if you need to step into a dependency.
- **C/C++**: the adapter needs `compile_commands.json` for IntelliSense but not for debugging; what it needs for debugging is a binary built with `-g`, and `miDebuggerPath` pointing at a real gdb/lldb. On macOS, unsigned debuggers cannot attach to arbitrary processes.
- **Java**: launch configs are generated from the project model; the common failure is a stale build — the extension debugs the compiled class, so a config that "runs old code" needs a clean build, not a config change.

## Compounds And Multi-Process

```json
"compounds": [
  { "name": "Full stack", "configurations": ["Attach to API", "Chrome"], "stopAll": true, "preLaunchTask": "dev" }
]
```

- `stopAll: true` — without it, stopping one session leaves the others running and the next launch hits a port already in use.
- Order in `configurations` is start order, but there is no wait between them. Use `serverReadyAction` or a background task with an `endsPattern` (`tasks.md`) when the client must not start first.
- Child processes: Node's adapter follows forks and workers automatically; other adapters do not. For a process that spawns workers, attach to each by port, or debug the worker in isolation.

## Breakpoint Types

| Type | What it does | Use it for |
|---|---|---|
| Conditional | Breaks when an expression is true | A loop that only misbehaves on one iteration — cheaper than a hundred continues |
| Hit count | Breaks on the Nth hit | Recursion, retries, "it fails the third time" |
| Logpoint | Prints a message and does **not** stop | Adding tracing to a running server without editing, rebuilding or redeploying it |
| Function breakpoint | Breaks on a name, not a line | Code you do not have open, or a minified target |
| Exception breakpoint | Breaks on thrown or uncaught exceptions | Finding where an error originates instead of where it is reported |
| Data / watchpoint | Breaks when a value changes | Supported by some adapters (LLDB, Delve, C++); not universal |

Logpoints are the most under-used of these: they turn "add a print, rebuild, redeploy" into a two-second edit against a live process, and they leave no trace in the source to forget about.

## Debugging Over SSH And In Containers

- The debug session runs where the *workspace* extension runs: on the remote host or inside the container, never split (`remote.md`). The adapter therefore sees the remote filesystem, which is why `pathMappings` disappears as a concern when the window is genuinely attached to the container rather than debugging into it from outside.
- Debugging **into** a container from a local window is the case that needs mappings: `localRoot` = your folder, `remoteRoot` = the path the code is mounted at.
- The inspector port must be published, and bound to `0.0.0.0` inside the container.
- Compose: attach to the service by port, and set `restart: true` so a container restart reconnects instead of ending the session.
- Over SSH with the port not published, the editor's own port forwarding usually already made it available on localhost — check the Ports panel before adding an SSH tunnel by hand.

## Debug Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| "Configured debug type is not supported" | Debug extension not installed, or not installed on the remote side | `remote.md`, Rule 8 |
| F5 opens a config picker every time | No `launch.json`, so the editor is guessing from the open file | Create the file; `Run: Add Configuration…` scaffolds it |
| F5 hangs before anything starts | `preLaunchTask` is a watch task with no `endsPattern` | `tasks.md` |
| Breakpoint hollow, program runs through | Path or sourcemap mismatch | The three questions above |
| Breakpoints work on the first run, not after a rebuild | `outFiles` glob no longer matches the output, or maps disabled in the incremental build | Check the build's sourcemap flag first |
| Steps into framework code constantly | No `skipFiles` | Add `<node_internals>/**` and the dependency directory |
| Variables show as `<optimized out>` | Release/optimized build | Debug profile |
| "Cannot connect to runtime process, timeout" | Inspector bound to localhost inside a container, wrong port, or the process already exited | Confirm the port is listening on the target's `0.0.0.0` |
| The debugger attaches to the wrong process | Auto Attach `always` plus a package-manager script | Set the filter to `smart` |
| Env vars present in the terminal, missing in the debug session | The debug session inherits the editor's process environment, not the shell's | `envFile`, or fix the editor's environment (`terminal.md`) |
| Anything else | Set `"trace": true` on the config and read the adapter log | — |

**When a debug config finally attaches and binds breakpoints**, write it to `~/Clawic/data/vscode/artifacts/launch-<repo>.md` — the JSON, the path mapping and the one-paragraph reason it is shaped that way, with every secret replaced by its pointer — and add its `## Boxes` line in `memory.md` in the same turn (`memory-template.md`). Record the repo's debug entry point and port in `## Projects`, and any mapping surprise (mount path, case sensitivity, a build that dropped sourcemaps) in `## Pain Points`. A hollow breakpoint that took an afternoon and was not written down costs the same afternoon again.
