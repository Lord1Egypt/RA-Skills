# Workspaces — Multi-Root, Folder Scope, and the `.vscode/` Contract

A workspace is what defines the roots, and the roots define what `${workspaceFolder}` means, which settings apply, and where search and tasks operate. Most monorepo confusion is a single-folder workspace being asked to behave like several.

**Contents:** [Three Kinds Of Workspace](#three-kinds-of-workspace) · [The .code-workspace File](#the-code-workspace-file) · [What Applies At Folder Scope](#what-applies-at-folder-scope) · [Variables In Multi-Root](#variables-in-multi-root) · [Tasks And Launch In Multi-Root](#tasks-and-launch-in-multi-root) · [Monorepo: One Root Or Several](#monorepo-one-root-or-several) · [The .vscode Contract](#the-vscode-contract) · [Onboarding A Repository](#onboarding-a-repository) · [Workspace Failure Signatures](#workspace-failure-signatures)

**Before restructuring a workspace**, read `## Projects` in `~/Clawic/data/vscode/memory.md` for how this repo is currently opened and any `artifacts/` file its `## Boxes` index names for its workspace layout. `vscode_dir_policy` in `config.yaml` decides what generated configuration is written into a committed `.vscode/`.

## Three Kinds Of Workspace

| Kind | Opened by | `${workspaceFolder}` | Workspace settings live in |
|---|---|---|---|
| **Single folder** | Opening a folder | That folder | `.vscode/settings.json` |
| **Multi-root** | Opening a `.code-workspace` file | Ambiguous — must be qualified | The `settings` block of the `.code-workspace` |
| **Empty** | New window, no folder | Undefined | Nowhere — user settings only |

In a multi-root workspace, each root keeps its own `.vscode/settings.json`, which becomes **folder** scope and applies only to files under that root. The `.code-workspace` block is workspace scope and wins over none of them — folder scope is later in the chain (`settings.md`).

## The `.code-workspace` File

```jsonc
{
  "folders": [
    { "path": "packages/api", "name": "api" },
    { "path": "packages/web", "name": "web" },
    { "path": "../shared-lib", "name": "shared" }
  ],
  "settings": { "search.exclude": { "**/dist": true } },
  "extensions": { "recommendations": ["dbaeumer.vscode-eslint"] },
  "tasks": { "version": "2.0.0", "tasks": [] },
  "launch": { "version": "0.2.0", "configurations": [] }
}
```

- `folders` paths are relative to the file, and may point **outside** it — this is what lets you open a service and its shared library together without nesting them.
- `name` renames a root in the explorer and, more importantly, is what `${workspaceFolder:name}` refers to. Unnamed roots use the directory name, which breaks when two roots share one.
- `settings`, `extensions`, `tasks` and `launch` may all live in the file. Consolidating there is one legitimate style; the other is keeping them in each root's `.vscode/`. Mixing both means two places to look.
- The file may live anywhere; keeping it at the repository root is what makes it shareable, and keeping it outside the repository is what makes it personal. That choice is the whole "should we commit it" argument.

## What Applies At Folder Scope

Only **resource-scoped** settings apply per folder. Window-scoped and application-scoped ones are ignored there, silently.

| Applies per folder | Does not |
|---|---|
| `editor.*`, language blocks | `window.*`, most `workbench.*` |
| `files.exclude`, `files.associations`, `files.eol` | `terminal.integrated.defaultProfile.*` (machine-overridable, window level) |
| `search.exclude`, `files.watcherExclude` | Anything naming a local executable, unless trusted |
| Formatter, linter and language-server keys | Update, telemetry, sync, theme |

The practical consequence in a monorepo: per-package indentation and formatter choices work at folder scope; per-package terminal shells and window behavior do not.

## Variables In Multi-Root

- `${workspaceFolder}` in a multi-root workspace is **ambiguous**. It resolves to a folder the editor picks, which is stable enough to be misleading and wrong often enough to break.
- `${workspaceFolder:api}` names the root explicitly and is the only correct form once there is more than one.
- `${fileWorkspaceFolder}` resolves to the root containing the active file — the right variable for a task meant to act on whatever you are editing.
- Tasks and launch configs defined *inside a root's* `.vscode/` still resolve `${workspaceFolder}` to that root, which is why keeping them per-root sidesteps the ambiguity entirely.

## Tasks And Launch In Multi-Root

- The task picker groups tasks by the root that defines them, plus any defined in the `.code-workspace`. Two roots defining a task with the same label is legal and confusing; prefix labels with the root name.
- `dependsOn` can reference a task in another root by using the object form with a `"workspaceFolder"` — plain label references stay within one root's definitions.
- Debug configurations from every root appear in one dropdown. `presentation.group` is what keeps that list navigable once there are three services.
- A compound spanning roots must live in the `.code-workspace` file, because it references configurations from more than one root (`debugging.md`).

## Monorepo: One Root Or Several

| | Single root at the repo top | Multi-root, one per package |
|---|---|---|
| Search and go-to-definition | Across everything, including build output unless excluded | Scoped per root; cross-package navigation depends on the language server |
| Per-package settings | Only through language blocks and path-specific tooling config | Native, at folder scope |
| Language servers | One per language, indexing the whole tree | Potentially one per root — faster per root, more total memory |
| Tasks and launch | One file, labels must disambiguate | Per package, naturally scoped |
| Cost | Indexing everything, always | Managing a `.code-workspace`, and cross-root variables |

Decide by where the pain is. A repo whose language server handles the whole tree comfortably is simpler as one root. A repo where indexing everything costs minutes, or where packages genuinely need different formatter or interpreter settings, is a multi-root workspace. Some ecosystems have their own workspace concept (a Go workspace file, a Cargo workspace, a package-manager workspace) that must be configured regardless of how the editor is opened — the editor's roots do not replace it (`languages.md`).

## The `.vscode` Contract

What a repository may say to an editor, and who it says it to.

| File | Commit? | Why |
|---|---|---|
| `extensions.json` | **Always** | It is the onboarding list; costs nothing and prompts once |
| `launch.json` | **Always** | Debugging the project should not be tribal knowledge |
| `tasks.json` | **Always** | Same, plus problem matchers nobody wants to rewrite |
| `settings.json` | **Shared subset only** | Formatter, excludes, indentation, language blocks |
| `*.code-snippets` | Optional | Project conventions as snippets travel well |
| `.code-workspace` | Contested | Committing forces a layout; see Where Experts Disagree in SKILL.md |
| Anything with an absolute path or a token | **Never** | Breaks for everyone else; a token in a repo is an incident |

The line for `settings.json`: commit what makes the *repository* consistent, keep what makes *your machine* comfortable in user settings or a profile. Interpreter paths, font sizes, themes, personal keybindings, telemetry, and `terminal.integrated.env.*` are all machine-side. A useful test before committing a key: would a colleague on a different OS with a different toolchain manager be helped or broken by it?

`.gitignore` the rest of `.vscode/` rather than the whole directory — `/.vscode/*` with `!/.vscode/extensions.json` and friends un-ignored is the pattern that keeps the contract while excluding local noise.

## Onboarding A Repository

The minimum a repo needs so a new person is productive in one open, in the order they matter:

1. `extensions.json` with the four or five extensions the repo genuinely needs.
2. `settings.json` with the formatter per language and the excludes that keep search usable.
3. `tasks.json` with a default build task and a default test task, each with a problem matcher.
4. `launch.json` with one attach configuration for the main process and one for tests.
5. A `.devcontainer/` if the toolchain is hard to install locally (`remote.md`).
6. A line in the README saying which of these exist. Configuration nobody knows about is configuration nobody uses.

## Workspace Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| A folder setting is ignored | It is window- or application-scoped | The table above |
| Task runs in the wrong package | `${workspaceFolder}` ambiguous in multi-root | `${workspaceFolder:name}` or per-root task files |
| Two identical task labels in the picker | Two roots defining the same label | Prefix labels by root |
| Search returns results from build output | `search.exclude` not set at the right scope | `performance.md` |
| Colleague's editor behaves differently | Something machine-side got committed, or the shared subset did not | The `.vscode` contract table |
| Opening the folder ignores the workspace file | A folder was opened directly instead of the `.code-workspace` | Open the workspace file; the title bar says which |
| Language server only understands one package | Ecosystem-level workspace config missing | `languages.md` |
| Settings vanished after opening the workspace file | The `.code-workspace` `settings` block replaced what the folder's file was providing | Check both places |
| Anything else | Check the title bar and the Settings UI scope tabs — they name the workspace kind and the scopes available | `settings.md` |

**When a workspace layout is settled** — roots, per-root settings, the committed subset of `.vscode/` — record it in `## Projects` of `~/Clawic/data/vscode/memory.md`, and write the `.code-workspace` file itself to `~/Clawic/data/vscode/artifacts/workspace-<repo>.md` with a line saying when to read it and its `## Boxes` line in the same turn (`memory-template.md`). The repo as a *project* — its goal, status, and decisions — belongs in the shared `~/Clawic/data/projects/<project>.md` and is referenced from here by name only; never duplicate the project record inside a VS Code file.
