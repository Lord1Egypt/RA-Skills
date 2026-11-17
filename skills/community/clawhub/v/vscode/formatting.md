# Formatting — The Save Pipeline, and Why Two Tools Fight Over Your File

Saving a file can run four things in sequence: auto-save timing, the formatter, code actions, and file trimming. Every "formatting is random" report is two of them running in an order nobody chose.

**Contents:** [The Order Of Operations](#the-order-of-operations) · [Choosing The Formatter](#choosing-the-formatter) · [codeActionsOnSave](#codeactionsonsave) · [Prettier Versus ESLint](#prettier-versus-eslint) · [EditorConfig](#editorconfig) · [Autosave Interactions](#autosave-interactions) · [Partial And Range Formatting](#partial-and-range-formatting) · [Formatting Failure Signatures](#formatting-failure-signatures)

**Before wiring a formatter**, read `## Projects` in `~/Clawic/data/vscode/memory.md` for this repo's existing formatter and any `artifacts/settings-*.md` its `## Boxes` index names — the formatter war in this repo may already have a winner. `formatter_stack` in `config.yaml` is the user's declared default stack.

## The Order Of Operations

On an explicit save (`Cmd/Ctrl+S`), in this order:

1. **`editor.formatOnSave`** runs the single formatter resolved for the language.
2. **`editor.codeActionsOnSave`** runs, in the order given if it is an array, otherwise in an unspecified order.
3. **`files.trimTrailingWhitespace`**, **`files.insertFinalNewline`**, **`files.trimFinalNewlines`** run last.
4. The file is written.

The consequence: a code action can undo the formatter, and the formatter never gets a second pass. If a lint fix reintroduces a style violation, the file is written violating the formatter — which is why "format on save does not work" is usually "a code action ran after it".

`editor.formatOnSaveMode` changes step 1's target: `file` (default), `modifications` (only lines changed relative to the source-control HEAD), `modificationsIfAvailable` (modifications when a provider can supply them, whole file otherwise). `modifications` requires a source-control provider that supports it; in a folder that is not a git repository it silently formats nothing.

## Choosing The Formatter

The resolution order for "which formatter runs":

1. `"[language]": {"editor.defaultFormatter": "<publisher>.<name>"}` in the winning settings scope.
2. `editor.defaultFormatter` (global) in the winning scope.
3. If exactly one extension registers a formatter for the language, it is used.
4. If more than one does, VS Code prompts on a manual format and does nothing on save.

Always write form 1. Form 2 is fragile: any language block anywhere overrides it, so it works until a workspace adds one line.

```json
{
  "editor.formatOnSave": true,
  "[typescript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[typescriptreact]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[json]": { "editor.defaultFormatter": "vscode.json-language-features" },
  "[python]": { "editor.defaultFormatter": "charliermarsh.ruff" },
  "[markdown]": { "editor.formatOnSave": false }
}
```

Built-in formatters have ids of the form `vscode.<feature>` — `vscode.json-language-features`, `vscode.html-language-features`, `vscode.typescript-language-features`. Naming them explicitly is what stops an installed extension from quietly taking over a language you were happy with.

## codeActionsOnSave

Boolean values are deprecated (`vscode >=1.85`). The current values are `"explicit"` (run when the user saves), `"always"` (also on auto-save and focus-change saves), `"never"`.

```json
"editor.codeActionsOnSave": {
  "source.organizeImports": "explicit",
  "source.fixAll.eslint": "explicit"
}
```

Object form does not guarantee order. When order matters, use the array form:

```json
"editor.codeActionsOnSave": ["source.organizeImports", "source.fixAll.eslint"]
```

Ordering rule with a worked example: organize-imports removes unused imports and sorts them; an ESLint autofix may rewrite import statements according to a plugin's rules. Run organize-imports **first** so ESLint sees the final import set; reversed, ESLint sorts imports that organize-imports then re-sorts differently, and the file changes on every alternate save.

- Prefer the **namespaced** action when a language has one: `source.organizeImports.ruff`, `source.fixAll.ts`, `source.fixAll.eslint`. The unnamespaced `source.fixAll` invites every extension that registers it, and two of them will disagree.
- `"always"` on a repo with `files.autoSave: afterDelay` runs the whole pipeline every second of idle typing. Use `"explicit"` unless there is a reason.
- Code actions that require the language server to be ready will silently skip during startup. A first-save-after-open that behaves differently is this, not a race in your config.

## Prettier Versus ESLint

Three configurations exist; pick one and say so.

| Setup | Wiring | Use when |
|---|---|---|
| **Prettier formats, ESLint lints** (default) | `defaultFormatter: prettier`, `eslint-config-prettier` disabling stylistic rules, `source.fixAll.eslint` in code actions | Almost always. Each tool does what it is good at |
| **ESLint formats too** | No Prettier extension; `source.fixAll.eslint` only; `editor.formatOnSave: false` for those languages | A repo that has already invested in stylistic ESLint rules and will not migrate |
| **Biome (or one unified tool)** | `defaultFormatter: biomejs.biome`, no Prettier, no ESLint formatting | Greenfield, and the tool covers every language in the repo |

The failure mode of mixing one and two: ESLint reports a stylistic error, Prettier fixes it its own way, ESLint reports it again on the next save. `eslint-config-prettier` exists to turn those rules off and is not optional in setup one.

ESLint flat config (`eslint.config.js`) is the default for ESLint 9+. The editor extension resolves it from the working directory; in a monorepo, set `eslint.workingDirectories` to `[{"mode": "auto"}]` or the extension lints package A with package B's config and reports rules that do not exist.

## EditorConfig

`.editorconfig` is read by the built-in support for a small set of keys: indent style and size, end of line, charset, trailing whitespace, final newline. It **wins over the equivalent VS Code settings** for those keys, at file level.

- It does not reach the formatter. Prettier reads `.editorconfig` itself only when configured to; other formatters may ignore it entirely. A repo where `.editorconfig` says 4 spaces and Prettier says 2 will produce 2 on format and 4 on manual indent.
- The frontier: `.editorconfig` for cross-editor basics, the formatter's own config file for everything the formatter owns. Duplicating a value in both is how they drift.

## Autosave Interactions

| `files.autoSave` | Format on save runs? | Notes |
|---|---|---|
| `off` | Yes, on explicit save | The predictable option |
| `afterDelay` | **No** | Delay saves do not trigger format-on-save; `files.autoSaveDelay` defaults to 1000 ms |
| `onFocusChange` | Yes | Formats when you click away — surprising in a split editor |
| `onWindowChange` | Yes | Formats when the window loses focus |

"Formatting stopped working after I turned on autosave" is this row, not a broken formatter. If autosave is required and formatting is required, use `onFocusChange`, or keep `afterDelay` and run formatting in a pre-commit hook instead.

## Partial And Range Formatting

- `editor.formatOnPaste` formats only the pasted range, and only if the formatter supports range formatting. Formatters that do not (most whole-file formatters) silently do nothing.
- `editor.formatOnType` fires on specific trigger characters the language provides — usually `;` and `}`. It is not a general formatter.
- Format Selection (`Cmd/Ctrl+K Cmd/Ctrl+F`) needs range support too; when it reformats the whole file instead, the formatter has no range provider.
- For a large legacy file nobody wants to reformat wholesale, `formatOnSaveMode: modifications` is the tool — it touches only lines the diff already touches, so the pull request stays reviewable.

## Formatting Failure Signatures

| Signature | Cause | Fix |
|---|---|---|
| Save does nothing at all | Two formatters registered, no `defaultFormatter` for the language | Language block naming one |
| Manual format prompts for a formatter every time | Same, and you dismissed the "remember" option | Language block; the prompt's choice writes it for you |
| Formats correctly, then reverts within the same save | A code action after the formatter (order of operations) | Array-form `codeActionsOnSave`, formatter-compatible lint config |
| Works for JS, not for JSX/TSX | The language ids are `javascriptreact`/`typescriptreact` and have no block | Add those blocks |
| Works locally, not for a colleague | Formatter extension not installed on their side, or not recommended in `.vscode/extensions.json` | Add to recommendations (`workspaces.md`) |
| Works in the file, not in the notebook cell | Notebooks route formatting separately | `notebook.formatOnSave.enabled` (`languages.md`) |
| Formatting stops after autosave was turned on | `afterDelay` does not trigger it | Table above |
| Different result in CI than in the editor | Extension bundles its own formatter version, repo pins another | Point the extension at the local install (`prettier.prettierPath`, or the tool's equivalent) |
| Anything else | Set `"<formatter>.trace"` or the extension's log level and read its output channel | — |

**When the save pipeline finally behaves**, write the exact block — formatter, language blocks, code-action array, autosave mode — to `~/Clawic/data/vscode/artifacts/settings-<repo>-format.md` with a line saying when to read it, plus its `## Boxes` line in the same turn (`memory-template.md`). Record the winning formatter per repo in `## Projects` of `memory.md`, and a formatter the user rules out in `## Extensions` with verdict `banned` — a second formatter for the same language is the most common silent breakage in this domain.
