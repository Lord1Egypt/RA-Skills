# Performance — Startup, Watchers, Search, and Memory

Slowness has four sources and they need different fixes: startup cost (extensions), event volume (watchers), scan cost (search and indexing), and memory (language servers). Measure which one before excluding anything.

**Contents:** [Measure First](#measure-first) · [Startup](#startup) · [The Three Exclude Lists](#the-three-exclude-lists) · [File Watching](#file-watching) · [Search](#search) · [Language Server Memory](#language-server-memory) · [Large Files And Long Lines](#large-files-and-long-lines) · [Rendering And The GPU](#rendering-and-the-gpu) · [A Monorepo Baseline](#a-monorepo-baseline) · [Performance Failure Signatures](#performance-failure-signatures)

**Before excluding anything**, read `## Environment` and `## Projects` in `~/Clawic/data/vscode/memory.md` — the watcher limit already raised on this machine, the exclude set already derived for this repo, and the measurement that justified them are recorded there. `startup_budget_ms` in `config.yaml` is the threshold above which startup counts as a problem worth profiling.

## Measure First

| Question | Tool | What it tells you |
|---|---|---|
| How long does a window take to load, and where does it go? | `Developer: Startup Performance` | A breakdown by phase, plus per-extension activation |
| Which extension costs what? | `Developer: Show Running Extensions` | Activation event, activation time, and a CPU profile of the host |
| Is this extensions at all? | Launch with `--disable-extensions --user-data-dir <tmp>` | A clean baseline; if it is still slow, it is core or the repo |
| Where is the CPU going right now? | `Developer: Show Running Extensions` → profile, or the process explorer | Which process — window, host, server, language server |
| How many files is this? | The repo's own count, before and after your excludes | The number that predicts everything else |

Rule: never apply an exclude list you have not justified with one of these. Excludes hide problems as often as they fix them, and a hidden folder that a language server needs produces "cannot find module" a month later.

## Startup

- Window load above `startup_budget_ms` is worth profiling; below it, effort is better spent elsewhere.
- Extensions with a `*` activation event pay their cost on every window, in every language, forever. Two or three is normal; ten is a problem you can measure (`extensions.md`).
- Restoring a previous session reopens every editor, which reactivates every language server for those files. A window that is slow only when reopening a workspace is this, not a startup regression.
- `window.restoreWindows` and the number of restored editors are the cheapest knobs; closing tabs you are not using is faster than any setting.
- A remote window's startup includes installing or verifying the server on the target, which dominates the first connection and disappears on later ones (`remote.md`).

## The Three Exclude Lists

Three settings that look interchangeable and are not. Using the wrong one is the most common self-inflicted performance fix.

| Setting | Hides from | Side effect |
|---|---|---|
| `files.exclude` | The explorer, **and every extension that walks the workspace** | Go-to-definition, imports and refactoring can stop finding those files. Use sparingly |
| `search.exclude` | Full-text search and quick open | None beyond search — this is the safe one, and it inherits `files.exclude` |
| `files.watcherExclude` | The file watcher | Changes in those paths are not detected — correct for build output, wrong for source |

Guidance: exclude build output and dependency directories from **search** and **watching**; exclude from `files.exclude` only what you genuinely never want any tool to see. `search.useIgnoreFiles` (default on) already respects `.gitignore`, so a well-ignored repo needs less than people assume.

```json
{
  "files.watcherExclude": {
    "**/node_modules/**": true, "**/.git/objects/**": true,
    "**/dist/**": true, "**/target/**": true, "**/.venv/**": true
  },
  "search.exclude": { "**/node_modules": true, "**/dist": true, "**/*.lock": true }
}
```

## File Watching

- On Linux, watching uses inotify, which has per-user limits on watches and instances. Exhausting them produces `ENOSPC` on open, or — worse — silent failure to detect changes.
- The fix is both halves: raise `fs.inotify.max_user_watches` at the OS level (524288 is the commonly used value on developer machines) **and** exclude directories that do not need watching. Raising the limit alone leaves the editor watching a dependency tree for no benefit.
- macOS and Windows use different mechanisms without the same hard limit, but a large watched tree still costs CPU on every build.
- A watcher covering a network mount or a virtualized bind mount is disproportionately expensive; this is the main reason a container-based setup feels slow (`remote.md`).
- Symptom of watching failure rather than watcher cost: the editor not noticing changes made by a build or a `git checkout` until you focus a file. That is exhausted watches, not a slow machine.

## Search

- Search uses a fast text-search backend and respects `.gitignore` by default. A search that takes minutes is almost always searching something ignored — build output, a vendored dependency tree, or a lockfile of a million lines.
- Quick open (`Cmd/Ctrl+P`) indexes file names, not contents, and honors the same excludes. A slow quick open means the file count itself is enormous.
- Search in binary or minified files wastes the whole budget: exclude `*.min.js`, source maps, and generated bundles explicitly.
- `search.followSymlinks` (default on) can walk out of the repository entirely through a symlinked dependency directory. Turning it off is the fix for a search that finds files that are not in the project.
- For a genuinely huge repo, scoping the search to a folder from the search box beats any setting.

## Language Server Memory

- Each language server is its own process with its own ceiling. The window can be idle while a server uses several gigabytes.
- TypeScript defaults to roughly a 3 GB ceiling and dies quietly past it; `typescript.tsserver.maxTsServerMemory` raises it. Raising it treats the symptom — the cause is usually the program including build output or a dependency tree that `tsconfig.json` should exclude (`languages.md`).
- Rust and C++ analysis are CPU- and memory-heavy by design on first index. Repeated re-indexing, not the first one, is the signal something is wrong.
- Two language servers for one language doubles the cost and produces duplicate diagnostics — check for that before tuning either (`extensions.md`).
- The process explorer attributes memory per process: window, extension host, each server, the remote server. A number without an owner is not actionable.

## Large Files And Long Lines

- Above a size threshold the editor disables tokenization, folding and some features (`editor.largeFileOptimizations`, on by default). Syntax highlighting silently disappearing in a big file is this working as intended.
- `editor.maxTokenizationLineLength` (default 20,000 characters) stops highlighting very long lines — the reason a minified file is plain text.
- Word wrap on a very long line is expensive to lay out; turning it off for that file is faster than any other change.
- For a multi-hundred-megabyte log, the editor is the wrong tool. Stream it, or slice the region of interest into a smaller file.
- Notebook outputs count as file content: a notebook with megabytes of stored output is slow to open, slow to diff and slow to search (`languages.md`).

## Rendering And The GPU

- Rendering happens on the GPU by default. On a machine with a driver problem the symptom is visual — flickering, blank panes, artifacts on scroll — not slowness.
- Launching with `--disable-gpu` is the diagnostic; if the artifacts disappear, it is the driver, and the persistent form of the workaround is a startup argument rather than a setting.
- Distinguish from an extension-host freeze: rendering problems affect drawing while the editor still responds; a host freeze stops completions and decorations while the UI still scrolls.
- High-refresh or scaled displays can make smooth scrolling and cursor animation expensive; those are settings, and turning them off is a real gain on a weak GPU.

## A Monorepo Baseline

Applied in this order, each justified by a measurement:

1. Exclude build output and dependency directories from `search.exclude` and `files.watcherExclude`.
2. Make sure the language server's own config excludes the same paths — the editor's excludes do not reach it (`tsconfig.json` `exclude`, the Python analysis paths, `go.work`).
3. Raise the OS watcher limit if the platform has one.
4. Turn off git decorations and autorefresh if the change volume is large (`git.md`).
5. Decide single-root vs multi-root deliberately; a per-package root is a smaller program for the language server (`workspaces.md`).
6. Close editors you are not using — restored editors reactivate servers.
7. Only then consider raising memory ceilings.

## Performance Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Slow startup in every workspace | Extensions activating on `*` | `Developer: Startup Performance` |
| Slow startup in one workspace only | Restored editors, or a server indexing that repo | Close tabs; check the server |
| UI freezes for seconds, periodically | An extension doing synchronous work | Profile the extension host |
| Changes not detected until focus | Watcher limit exhausted | Raise the limit and exclude |
| `ENOSPC` on open | Same, at the hard limit | Same |
| Search takes minutes | Searching ignored or generated content | `search.exclude`, check `followSymlinks` |
| Editor fine, completions absent after a while | Language server crashed on memory | Its output channel; then exclude, then raise |
| Highlighting gone in one file | Large-file optimizations or line-length limit | Expected; slice the file |
| Flicker, blank panes, scroll artifacts | GPU rendering | `--disable-gpu` as a test |
| Slow only in a container or over a network mount | Filesystem crossing a boundary | `remote.md` |
| Anything else | Clean window baseline, then add back | `extensions.md` |

**When a performance fix is measured and applied**, write the numbers, not just the change: the measured before and after, the exclude set, and the OS-level limit raised go in `## Environment` of `~/Clawic/data/vscode/memory.md` if they are machine-wide, or in `## Projects` if they are one repo's (`memory-template.md`). An exclude list worth reusing across machines is an `artifacts/settings-<repo>-performance.md` with its `## Boxes` line in the same turn. Record any extension-activation measurement next to its row in `## Extensions` — without the number, the same extension gets re-suspected and re-measured every year, and the audit cadence belongs in `## Due`.
