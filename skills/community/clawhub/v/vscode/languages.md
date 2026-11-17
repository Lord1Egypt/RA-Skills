# Languages — Servers, Interpreters, and Why the Editor Disagrees With the Compiler

A squiggle is one program's opinion. When the editor and the command line disagree, they are reading different project roots, different toolchains, or different versions — and the fix is to make them read the same thing.

**Contents:** [The Universal First Three](#the-universal-first-three) · [TypeScript And JavaScript](#typescript-and-javascript) · [Python](#python) · [Go](#go) · [Rust](#rust) · [C And C++](#c-and-c) · [Java](#java) · [Web, JSON, YAML, Markdown](#web-json-yaml-markdown) · [Notebooks](#notebooks) · [Language Failure Signatures](#language-failure-signatures)

**Before diagnosing a language server**, read `## Projects` and `## Environment` in `~/Clawic/data/vscode/memory.md` — the interpreter, the toolchain manager and the monorepo root for this repo were established once already, and `## Environment` holds the machine-level facts (version manager, PATH resolution) that break every language at once. `language_stack` in `config.yaml` names the user's linter and test framework per language.

## The Universal First Three

Before anything language-specific, in this order:

1. **Restart the server.** Most stale-state problems die here. Every ecosystem has the command: `TypeScript: Restart TS Server`, `Python: Restart Language Server`, `Go: Restart Language Server`, `rust-analyzer: Restart server`, `Java: Clean Java Language Server Workspace`.
2. **Confirm which project root it resolved.** Editors resolve config upward from the file; a monorepo has several candidates and the server picked one. Every server can print it — the TS server log, `Python: Show Output`, rust-analyzer's status.
3. **Confirm which toolchain it is using.** The status bar shows the interpreter, the toolchain, the SDK. A version manager (nvm, fnm, pyenv, asdf, rustup, sdkman) that works in the terminal may be invisible to the editor, because the editor's environment is not the shell's (`terminal.md`).

If all three agree with the command line and the disagreement persists, then it is a real difference: a plugin the CLI loads and the editor does not, or a strictness flag that only one path applies.

## TypeScript And JavaScript

- **Workspace version vs bundled version.** The editor ships a TypeScript version; the repo has another in `node_modules`. Use the workspace one: `"typescript.tsdk": "node_modules/typescript/lib"`, then `TypeScript: Select TypeScript Version → Use Workspace Version`. Mismatched versions is the top cause of an error the CLI does not report.
- `TypeScript: Open TS Server Log` (after setting `typescript.tsserver.log` to `verbose`) shows the resolved `tsconfig.json`, the file list and the module resolutions. It is the only place the resolution is visible.
- **Project references and monorepos**: with `composite` projects the server needs the referenced projects built (`tsc --build`) or it reports missing declarations for sibling packages. `"typescript.tsserver.experimental.enableProjectDiagnostics"` changes how whole-project errors are reported, at a memory cost.
- Memory: the server defaults to roughly 3 GB and dies silently past it on a very large repo. `typescript.tsserver.maxTsServerMemory` raises it; the real fix is usually excluding build output from the program (`performance.md`).
- `// @ts-check` in a JS file, or `"checkJs": true`, turns on type errors in JavaScript. Errors appearing in `.js` files after a config change is this, not the extension.
- Auto-imports pick the wrong path when several barrels export the same name: `"typescript.preferences.importModuleSpecifier": "non-relative"` plus correct `paths` in tsconfig settles it.
- Deep type errors and their remedies are the language's problem, not the editor's (`typescript`).

## Python

- **Interpreter selection is workspace state, not a setting.** `Python: Select Interpreter` stores the choice per workspace. `python.defaultInterpreterPath` is *only* a fallback used when nothing has been selected — editing it after a selection exists changes nothing, and this is the single most common Python-in-editor confusion.
- The selected interpreter drives everything downstream: the language server's search paths, test discovery, the debugger and the terminal's auto-activation. One wrong selection makes all four look broken independently.
- **Terminal activation**: the integrated terminal activates the selected environment on open. A terminal opened before the selection keeps the old one — open a new terminal rather than debugging the activation.
- Language server choice: `python.languageServer` selects between the bundled options. A closed-source server is unavailable in non-Microsoft builds and falls back silently (`forks.md`).
- `python.analysis.extraPaths` for imports the server cannot find in a src-layout or namespace-package repo. Prefer fixing the project's own path configuration; use the setting when you do not own the layout.
- `python.analysis.typeCheckingMode` (`off` / `basic` / `standard` / `strict`) is the reason a repo suddenly has hundreds of squiggles the CLI does not report — it is the editor applying a strictness the project never asked for.
- Linter and formatter are separate extensions now, not part of the language extension. Two of them for the same job is the classic conflict (`formatting.md`).

## Go

- The extension needs its tools installed once per environment (`Go: Install/Update Tools`). In a container or over SSH they must be installed *there*.
- `gopls` resolves the module from the nearest `go.mod`. A repo with several modules needs a workspace file (`go.work`) or the server will only understand one of them.
- Build tags: code behind a tag is not analyzed unless `"go.buildFlags": ["-tags=integration"]` is set — the symptom is real code that shows as unused and unreachable.
- `GOFLAGS`, `GOPRIVATE` and proxy settings come from the environment the editor started with; a private module that resolves in the terminal and not in the editor is an environment problem (`terminal.md`).

## Rust

- rust-analyzer builds a real crate graph; the first index on a large workspace is slow and CPU-heavy, and this is expected rather than a misconfiguration.
- `rust-analyzer.cargo.features` and `cargo.allFeatures` decide which cfg-gated code is analyzed. Code that looks dead is usually behind a feature the server does not have on.
- `rust-analyzer.check.command` set to `clippy` moves lints into the editor at the cost of a slower check cycle.
- Proc-macro and build-script support must be enabled for macro-heavy crates, or every derived item reads as unresolved.
- Analysis and `cargo build` compete for the same target directory and block each other. A separate target dir for the server removes the stall at the cost of disk.

## C And C++

- IntelliSense needs a compilation database: `compile_commands.json` generated by the build system, pointed at with `"compileCommands"`. Without it the extension guesses include paths and is wrong in any non-trivial project.
- The alternative is the clangd extension, which reads the same database. Running both C/C++ IntelliSense and clangd produces duplicate diagnostics — disable one (`extensions.md`).
- Cross-compilation: the database records the cross compiler's flags, which the editor's parser may not understand. Setting the right `intelliSenseMode` and compiler path is what stops thousands of phantom errors.
- Debugging is a separate concern from IntelliSense; a binary built with `-g` is what the debugger needs (`debugging.md`).

## Java

- The language server maintains its own workspace index. Corruption is common after a large branch switch; `Java: Clean Java Language Server Workspace` is the reset, and it costs a full re-index.
- Multiple JDKs: the runtime the server *runs on* and the runtime a project *targets* are configured separately. A project targeting an older release still needs a supported JDK to run the server.
- Build-tool import (Maven, Gradle) happens on open and can fail quietly on a proxy or a missing wrapper distribution. The import log is its own output channel.

## Web, JSON, YAML, Markdown

- **JSON schemas**: `json.schemas` maps a glob to a schema; `$schema` in the file wins over it. Validation errors in a config file with no visible cause are usually a schema the editor auto-associated by filename.
- **JSONC**: files with comments must be recognized as `jsonc` or every comment is an error. `.vscode/*.json` is jsonc by default; a custom config file with comments needs `"files.associations": {"*.myrc": "jsonc"}`.
- **YAML**: schema association and indentation come from an extension, not the core. Anchors and multi-document files are where the editors and the consumers most often disagree.
- **Emmet** works in HTML and CSS by default; in JSX, Vue templates and others it needs `"emmet.includeLanguages": {"javascriptreact": "html"}` (`editing.md`).
- **Markdown**: link validation is built in and can be strict about relative paths; the setting to relax it exists, and turning it off wholesale loses the one check that catches renamed files.

## Notebooks

- The kernel is chosen per notebook and stored with the workspace, not in settings — the same model as the Python interpreter, with the same confusion.
- A kernel from a virtual environment must have the kernel package installed *in that environment*; selecting it otherwise fails at connect time with an unhelpful message.
- Formatting a notebook is separate: `notebook.formatOnSave.enabled`, and `notebook.codeActionsOnSave` for save actions. The editor keys do not apply to cells.
- Outputs are stored in the file. A repo that diffs notebooks needs output stripping in a pre-commit hook, not an editor setting.
- Long outputs are truncated in the rendered view; the full text is in the output item's own scrollback, and very large outputs slow the whole window (`performance.md`).

## Language Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Editor errors, clean CLI build | Different version, different project root, or a stricter editor-only setting | The universal first three |
| No completions at all, no errors either | Server failed to start; its output channel says why | Output panel → the server's channel |
| Completions from two sources, duplicated diagnostics | Two language servers for one language | Disable one (`extensions.md`) |
| Imports unresolved for one directory only | Path config the server does not know about (src layout, `paths`, `go.work`, multi-root) | Fix the project config, not the editor |
| Correct until a branch switch, then nonsense | Stale index | The ecosystem's clean/restart command |
| Works in terminal, not in editor, for a version-managed toolchain | Editor environment ≠ shell environment | `terminal.md` |
| Server dies repeatedly on a big repo | Memory ceiling, or indexing build output | Raise the ceiling, then exclude output (`performance.md`) |
| Feature missing entirely in a fork | Licensed extension unavailable | `forks.md` |
| Anything else | Turn the server's trace to verbose and read the resolution it printed | — |

**When a language setup finally resolves correctly**, record the interpreter or toolchain, the project root and any extra path in `## Projects` of `~/Clawic/data/vscode/memory.md`; if the fix was a settings block worth reusing, it goes to `~/Clawic/data/vscode/artifacts/settings-<repo>-<language>.md` with its `## Boxes` line in the same turn (`memory-template.md`). A machine-level cause — a version manager the editor cannot see, a proxy, a corporate CA — belongs in `## Environment` instead, because it will break the next language too.
