# Tasks — Builds, Watchers, and Problem Matchers That Actually Match

A task is a command plus a parser. The command is the easy half; the parser is what turns compiler output into clickable Problems entries, and it is the part that gets abandoned.

**Contents:** [Anatomy Of A Task](#anatomy-of-a-task) · [shell Versus process](#shell-versus-process) · [Problem Matchers](#problem-matchers) · [Background And Watch Tasks](#background-and-watch-tasks) · [Composing Tasks](#composing-tasks) · [Inputs](#inputs) · [Presentation](#presentation) · [Auto-Run On Folder Open](#auto-run-on-folder-open) · [Task Failure Signatures](#task-failure-signatures)

**Before writing a task for a repo that already builds**, read `## Projects` in `~/Clawic/data/vscode/memory.md` and open any `artifacts/matcher-*.md` or `artifacts/tasks-*.md` its `## Boxes` index names — a problem matcher for a non-standard tool is the single most expensive artifact in this domain to re-derive.

## Anatomy Of A Task

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "pnpm",
      "args": ["build"],
      "options": { "cwd": "${workspaceFolder}/packages/api" },
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": "$tsc",
      "presentation": { "reveal": "silent", "panel": "dedicated", "clear": true }
    }
  ]
}
```

- `label` is the identity: `preLaunchTask`, `dependsOn` and `Tasks: Run Task` all reference it. Renaming a label silently breaks every reference.
- `group.isDefault` binds the task to `Run Build Task` (`Cmd/Ctrl+Shift+B`). Exactly one build task and one test task should have it.
- `options.cwd`, `options.env`, `options.shell` override per task. `cwd` defaults to `${workspaceFolder}`.
- Task-level `type` values that are always available: `shell` and `process`. Everything else (`npm`, `typescript`, `gulp`, `docker-build`) is contributed by an extension and vanishes when it is disabled — which is why a task file that works for you fails for a colleague with a different extension set.
- Auto-detected tasks (npm scripts, Make targets) appear in the picker without existing in `tasks.json`. They cannot be referenced by `dependsOn` until you materialize them with `Tasks: Configure Task`.

## shell Versus process

| | `shell` | `process` |
|---|---|---|
| What runs | The command string inside a shell | The executable directly |
| Quoting | The shell's rules apply — this is where arguments break | Args are passed verbatim, no quoting |
| Shell features | Pipes, globs, `&&`, env expansion | None |
| Use for | One-liners that genuinely need a shell | Anything invoking a binary with arguments |

Argument quoting in `shell` tasks is explicit when it matters:

```json
"args": [
  { "value": "src/**/*.ts", "quoting": "weak" },
  { "value": "a message with spaces", "quoting": "strong" },
  { "value": "$SOME_VAR", "quoting": "escape" }
]
```

`strong` prevents all interpretation, `weak` allows variable expansion, `escape` escapes only characters the shell would treat specially. A glob that "works in the terminal but not in the task" is almost always the shell expanding it in one case and the task quoting it in the other — switch to `process` and let the tool do its own globbing.

## Problem Matchers

A matcher turns lines of output into diagnostics. Named built-ins cover the common tools — `$tsc`, `$tsc-watch`, `$eslint-stylish`, `$eslint-compact`, `$msCompile`, `$jshint-stylish`, `$lessc`. Everything else needs one written.

```json
"problemMatcher": {
  "owner": "acme-cc",
  "source": "acme-cc",
  "fileLocation": ["relative", "${workspaceFolder}"],
  "pattern": {
    "regexp": "^(.+?):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
    "file": 1, "line": 2, "column": 3, "severity": 4, "message": 5
  }
}
```

Rules that decide whether it works at all:

- **`fileLocation` is the top cause of a silent matcher.** `"absolute"`, `"relative"` with a base, `"autoDetect"` with a base. A compiler printing paths relative to its own build directory needs that directory as the base, not the workspace root. A matcher that finds errors but produces no clickable entries is always this.
- Capture-group numbers are positions in the regex, counted by opening parenthesis. Adding a non-capturing group (`(?:…)`) does not shift them; adding a capturing one does, and every index below it is now wrong.
- Multi-line errors use `pattern` as an **array**, with `loop: true` on the last element for repeating detail lines. A message split across two lines with a single-pattern matcher matches only the first line and drops the message.
- `severity` may come from the output or be fixed with `"severity": "error"` at the matcher level for tools that do not print one.
- `owner` groups diagnostics; two tasks sharing an owner overwrite each other's Problems entries. Give each tool its own.
- Test a matcher by running the task and opening the Problems panel filtered to its source. If the count is zero and the terminal shows errors, the regex or `fileLocation` is wrong — nothing else produces that combination.

## Background And Watch Tasks

A watch task never exits. Without telling the editor how to recognize "a build cycle finished", `preLaunchTask` waits forever and F5 appears to hang.

```json
{
  "label": "watch",
  "type": "shell",
  "command": "tsc --watch --noEmit",
  "isBackground": true,
  "problemMatcher": {
    "base": "$tsc-watch",
    "background": {
      "activeOnStart": true,
      "beginsPattern": "Starting compilation|File change detected",
      "endsPattern": "Found \\d+ errors?\\. Watching for file changes"
    }
  }
}
```

- `isBackground: true` alone is not enough — the `background` block is what signals completion.
- `activeOnStart: true` treats the task as already building when it starts, so the first `endsPattern` match releases anything waiting. Without it, a watcher that prints nothing until the first change blocks the launch.
- `$tsc-watch` already carries these patterns. Write them by hand only for tools without a built-in.
- The patterns must match lines the tool actually prints in the mode you run it in. Quiet flags (`--silent`, `--logLevel error`) remove the very lines the matcher waits for.
- `runOptions.instanceLimit` and `"panel": "dedicated"` stop a watch task from being started five times by five F5 presses.

## Composing Tasks

```json
{ "label": "dev", "dependsOn": ["install", "codegen", "watch"], "dependsOrder": "sequence" }
```

- `dependsOrder` defaults to **parallel**. A build that "sometimes works" is usually a parallel dependency chain with an implicit ordering.
- `sequence` stops at the first failing dependency.
- A composite task with no `command` of its own is legitimate and is the clean way to name a workflow.
- `preLaunchTask` in `launch.json` accepts a task label; `postDebugTask` accepts one too and is the right place to tear down a container or free a port.
- Do not chain a watch task after a one-shot task with `sequence` — the sequence never advances past the watcher.

## Inputs

```json
"inputs": [
  { "id": "env", "type": "pickString", "description": "Target", "options": ["dev", "staging"], "default": "dev" },
  { "id": "msg", "type": "promptString", "description": "Message" },
  { "id": "ports", "type": "command", "command": "extension.someCommand" }
]
```

Referenced as `${input:env}`. `promptString` with `"password": true` masks the entry, but the value still ends up in the task's command line and in the terminal's scrollback — never use it for a real secret. Pass secrets through an env file the task reads, and keep that file out of version control.

## Presentation

| Key | Values | Use |
|---|---|---|
| `reveal` | `always` \| `silent` \| `never` | `silent` shows the terminal only on error — the right default for a build |
| `panel` | `shared` \| `dedicated` \| `new` | `dedicated` per watch task; `shared` for one-shot tasks |
| `clear` | bool | Clears before each run so the scrollback is this run only |
| `close` | bool | Closes the terminal on success — good for tasks whose output nobody reads |
| `group` | string | Puts several tasks in one terminal group, side by side |
| `echo` | bool | Prints the command line; useful once, noise afterwards |

## Auto-Run On Folder Open

```json
"runOptions": { "runOn": "folderOpen" }
```

This executes a shell command every time the folder opens, in a trusted workspace, with no prompt. It is a legitimate convenience for a watcher and an execution grant for anyone who can open a pull request against the repo (`security.md`, SKILL.md Rule 7). When generating one, say what it runs and why; when reading one from an unfamiliar repo, read it before trusting the folder. `trust_posture` in `config.yaml` decides whether these are emitted at all.

## Task Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Task runs, Problems panel stays empty | `fileLocation` wrong, or capture indices shifted | Compare one printed path against the base |
| "No problem matcher found" prompt every run | `problemMatcher` omitted | Set it, or `[]` explicitly for tasks with no diagnostics |
| F5 hangs, terminal shows a running watcher | Background patterns missing (above) | Add `background` with `activeOnStart` |
| Works in terminal, fails as a task | Shell quoting, or a different shell than the interactive one | Switch to `process`, or set `options.shell` |
| Command not found in the task only | The task inherits the editor's environment, not the login shell's | `terminal.md` |
| Task type unknown | The contributing extension is disabled, missing, or on the other side of a remote window | Install it where the task runs (`remote.md`) |
| Same task starts several times | No `instanceLimit`, `panel: shared` reused | `runOptions.instanceLimit: 1`, `panel: dedicated` |
| Task cannot find the package manager in a monorepo | `cwd` defaults to the workspace root, not the package | `options.cwd`, and `${workspaceFolder:name}` in multi-root |
| Anything else | Run the exact command in the integrated terminal; if it fails there too, it is not a task problem | — |

**When a task file finally builds and reports diagnostics correctly**, write it to `~/Clawic/data/vscode/artifacts/tasks-<repo>.md`, and write any hand-written problem matcher to its own `artifacts/matcher-<tool>.md` with the sample output it was derived from — that sample is what makes the regex maintainable — each with its `## Boxes` line in `memory.md` in the same turn (`memory-template.md`). If a task auto-runs on folder open, note that in `## Projects` so the grant is visible next time somebody audits the repo.
