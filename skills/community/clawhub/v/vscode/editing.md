# Editing — Suggestions, Snippets, Multi-Cursor, and Refactorings

The authoring layer is where a small number of settings produce most of the daily friction. Each one below has a default tuned for discoverability, not for someone who types all day.

**Contents:** [The Suggest Widget](#the-suggest-widget) · [Inline Suggestions](#inline-suggestions) · [Snippets](#snippets) · [Multi-Cursor And Selection](#multi-cursor-and-selection) · [Refactorings And Code Actions](#refactorings-and-code-actions) · [Emmet](#emmet) · [Navigation](#navigation) · [Editing Failure Signatures](#editing-failure-signatures)

**Before changing authoring behavior**, read `## Environment` in `~/Clawic/data/vscode/memory.md` — a remapped modifier key or a non-US keyboard layout changes which of these settings are even reachable, and it was recorded the first time it cost time.

## The Suggest Widget

| Setting | Default behavior | Why change it |
|---|---|---|
| `editor.acceptSuggestionOnEnter` | `on` | `off` or `smart` stops Enter from accepting a suggestion when you meant a newline — the single most common source of accidental completions |
| `editor.suggestOnTriggerCharacters` | on | Off stops the widget appearing on every `.`; pair with an explicit trigger keybinding |
| `editor.quickSuggestions` | on in code, off in comments and strings | Turn it on in strings for template-heavy code, off in code for a quieter editor |
| `editor.suggest.insertMode` | `insert` | `replace` overwrites the rest of the word — correct when editing an existing identifier, wrong when prefixing |
| `editor.suggestSelection` | `first` | `recentlyUsedByPrefix` makes the widget learn your habits per prefix |
| `editor.wordBasedSuggestions` | on | Off removes noise once a real language server is running; on it is the only source in plain text |
| `editor.snippetSuggestions` | `inline` | `top`/`bottom` separates snippets from language completions when they collide |
| `editor.acceptSuggestionOnCommitCharacter` | on | Off stops `(` or `.` from accepting the highlighted item mid-word |

The two that resolve most complaints: `acceptSuggestionOnEnter: "off"` for people who type faster than they read, and `snippetSuggestions: "bottom"` when a snippet keeps winning over the symbol you wanted.

## Inline Suggestions

- `editor.inlineSuggest.enabled` governs ghost-text suggestions from whichever provider is installed. Tab accepts, which collides with indentation at the start of a line — `editor.tabCompletion` and the provider's own accept binding are the two knobs.
- Word-by-word acceptance exists as a separate command; binding it is what makes ghost text usable when the suggestion is 80% right.
- Two providers registering inline suggestions produce alternating ghost text. Only one should be enabled per language (`extensions.md`).

## Snippets

Three scopes, three locations:

| Scope | Location | Applies to |
|---|---|---|
| Language | user snippets dir, `<language>.json` | That language, everywhere |
| Global | user snippets dir, `<name>.code-snippets` with a `scope` field | The languages listed in `scope`, or all if omitted |
| Project | `.vscode/<name>.code-snippets` in the repo | That workspace only — the one that travels with the team |

```json
{
  "React function component": {
    "prefix": "rfc",
    "scope": "typescriptreact",
    "body": [
      "export function ${1:${TM_FILENAME_BASE}}({ ${2:props} }: ${1}Props) {",
      "\treturn <div>$0</div>;",
      "}"
    ],
    "description": "Typed function component"
  }
}
```

- `$1`, `$2`, `$0` are tab stops; `$0` is the final cursor position and there is exactly one. Repeating `${1}` mirrors the value as you type it.
- `${1|a,b,c|}` is a choice list. `${1:default}` is a placeholder.
- Variables worth knowing: `TM_FILENAME_BASE`, `TM_SELECTED_TEXT` (the selection when the snippet is triggered from a selection), `CLIPBOARD`, `WORKSPACE_NAME`, `CURRENT_YEAR`, `RANDOM_HEX`.
- Transformations apply a regex to a variable: `${TM_FILENAME_BASE/(.*)/${1:/pascalcase}/}` turns `user-card` into `UserCard`. This is what makes a component snippet actually usable.
- Snippets can be bound to a key directly in `keybindings.json` with `"command": "editor.action.insertSnippet"` and a `snippet` argument — no prefix, no widget (`keybindings.md`).
- A project snippet file is the underused one: it puts the repo's conventions (a test skeleton, a migration header, a license block) one prefix away for everyone who clones it.

## Multi-Cursor And Selection

| Action | Binding | Note |
|---|---|---|
| Add cursor at next occurrence | `Cmd/Ctrl+D` | Repeated; `Cmd/Ctrl+K Cmd/Ctrl+D` skips the current one |
| Select all occurrences | `Cmd+Shift+L` / `Ctrl+Shift+L` | Whole file — dangerous in a large one, safe after a selection |
| Add cursor above/below | `Cmd+Opt+Up/Down` / `Ctrl+Alt+Up/Down` | Column editing without column selection |
| Add cursor at click | `Alt+Click` (default) | Governed by `editor.multiCursorModifier` |
| Column (box) selection | `Shift+Alt+drag`, or the toggle command | The right tool for fixed-width data |
| Expand/shrink selection | `Shift+Alt+Right/Left` | Syntax-aware; the fastest way to select an expression exactly |

`editor.multiCursorModifier` has a side effect people miss: it is either `alt` (multi-cursor on Alt+click, go-to-definition on Cmd/Ctrl+click) or `ctrlCmd` (the reverse). Changing it to work around an OS-level Alt remap also moves go-to-definition, which then feels broken for a week. Record the remap and the reason (`## Environment`).

Two habits that beat multi-cursor when the change is structural: **Rename Symbol** (`F2`), which is semantic and crosses files, and search-and-replace with a regex in the Search view, which previews every match before committing.

## Refactorings And Code Actions

- The lightbulb offers quick fixes and refactorings from the language server. `Cmd/Ctrl+.` opens it without the mouse; `editor.lightbulb.enabled` hides the icon while keeping the shortcut.
- **Rename Symbol** (`F2`) is semantic: it updates imports and usages across the project, which text replace does not. It fails on dynamically constructed names, and the server says so rather than silently missing them.
- Refactor Preview (`Refactor: Preview` in the code-action menu, or the preview toggle) shows a diff of every file a refactoring will touch. Use it for anything crossing more than one file.
- Extract to function/variable/constant is language-server-provided and varies in quality by ecosystem — TypeScript and Java are strong, others less so.
- **Move to file** (where supported) is the refactoring that keeps imports correct when splitting a large module, and is far safer than cut-paste.
- Organize Imports is a code action, which is why it participates in the save pipeline and its ordering matters (`formatting.md`).

## Emmet

- Built in for HTML and CSS. `emmet.includeLanguages` extends it: `{"javascriptreact": "html", "vue-html": "html", "php": "html"}`.
- `emmet.triggerExpansionOnTab` makes Tab expand abbreviations, which conflicts with snippet tab stops and indentation. Off by default for a reason; turning it on is a deliberate trade.
- `emmet.showExpandedAbbreviation: "never"` removes Emmet entries from the suggest widget while keeping the expand command — the setting for people who find Emmet suggestions noisy but want the feature.

## Navigation

The commands worth binding, because they replace scrolling:

| Need | Command |
|---|---|
| Symbol in this file | `Cmd/Ctrl+Shift+O`, or `@` in quick open |
| Symbol in the workspace | `Cmd/Ctrl+T`, or `#` in quick open |
| Back and forward through jumps | `Ctrl+-` / `Ctrl+Shift+-` (macOS), `Alt+Left/Right` elsewhere |
| Last edit location | `Ctrl+Q`-style "Go to Last Edit Location" — the fastest return after chasing a definition |
| Peek definition/references | `Opt/Alt+F12`, `Shift+F12` — inline, keeps context |
| Breadcrumb navigation | `breadcrumbs.enabled`, then the focus command — keyboard-driven structural navigation |
| Sticky scroll | `editor.stickyScroll.enabled` — keeps the enclosing signature visible in long functions |

`workbench.editor.enablePreview` controls preview tabs (italic, replaced by the next thing you open). Turning it off makes every open a real tab; leaving it on and double-clicking to pin is the middle ground. Most reports of "I lost the file I had open" are preview tabs.

## Editing Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Enter accepts a completion instead of a newline | `acceptSuggestionOnEnter: on` | Set `off` or `smart` |
| Tab indents instead of expanding a snippet | Snippet prefix not matched, or tab completion off | `editor.tabCompletion: "on"` and check the prefix's scope |
| A snippet appears in the wrong languages | Global `.code-snippets` with no `scope` | Add `scope`, or move it to a language file |
| Alt+Click does nothing | OS or window manager consumed Alt, or `multiCursorModifier` changed | Table above; record the remap in `## Environment` |
| Rename Symbol only changes one file | Language server not resolving the project, or the symbol is dynamic | `languages.md` |
| Ghost text alternates between two suggestions | Two inline-suggestion providers | Disable one (`extensions.md`) |
| Emmet does nothing in JSX | Language not in `emmet.includeLanguages` | Add it |
| Files keep disappearing from the tab bar | Preview tabs | `workbench.editor.enablePreview: false`, or pin |
| Anything else | Reproduce in a clean window; an authoring behavior that survives is core and has a setting | `extensions.md` |

**When a snippet set or an authoring configuration is worth keeping**, write it to `~/Clawic/data/vscode/artifacts/snippets-<what>.md` or `artifacts/settings-editing.md` with a line saying when to read it, plus its `## Boxes` line in `memory.md` in the same turn (`memory-template.md`) — a project snippet file belongs in the repo, and the artifact records why it exists. Keyboard-layout facts and modifier remaps go to `## Environment`, because they invalidate the default binding advice in every other file.
