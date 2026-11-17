# Keybindings — When Clauses, Chords, and the Key That Went Nowhere

A keystroke is dispatched to exactly one command: the last matching binding whose `when` clause is true. "Nothing happened" always means one of those two conditions failed, and the editor will tell you which.

**Contents:** [Troubleshooting First](#troubleshooting-first) · [The Resolution Rule](#the-resolution-rule) · [keybindings.json](#keybindingsjson) · [When Clauses](#when-clauses) · [Chords](#chords) · [The Terminal Steals Keys](#the-terminal-steals-keys) · [Layouts And Remaps](#layouts-and-remaps) · [Bindings Worth Adding](#bindings-worth-adding) · [Keybinding Failure Signatures](#keybinding-failure-signatures)

**Before changing a binding**, read `## Environment` in `~/Clawic/data/vscode/memory.md` — keyboard layout, OS-level remaps and any window-manager shortcut that swallows keys are recorded there, and they explain most "this binding does not work" reports before a single JSON edit. `os_family` in `config.yaml` decides whether to write `cmd` or `ctrl`; while it is unset, give both forms.

## Troubleshooting First

`Developer: Toggle Keyboard Shortcuts Troubleshooting` logs, for every keystroke: the raw key, the resolved keybinding, the command dispatched, and whether the `when` clause matched. Press the key that is failing and read the log. It distinguishes the three cases in one shot:

- **No entry at all** — the keystroke never reached the editor. The OS, the window manager, or the terminal took it.
- **Entry, no command** — the key is bound but every candidate's `when` clause was false.
- **Entry, unexpected command** — another binding wins the resolution.

`Developer: Inspect Context Keys` then tells you the value of every context key at the cursor, which is how you find out that `editorTextFocus` was false because focus was in the sidebar.

## The Resolution Rule

1. Collect every binding for the key combination — defaults plus user bindings.
2. Filter to those whose `when` clause evaluates true in the current context.
3. **The last one in the list wins**, and user bindings are appended after defaults. So a user binding always beats a default for the same key and context.
4. A binding whose command is prefixed with `-` **removes** a binding rather than adding one.

That last point is what people miss: to make a key do nothing, do not bind it to a no-op — remove the default.

```json
[
  { "key": "ctrl+shift+p", "command": "-workbench.action.showCommands" },
  { "key": "ctrl+shift+p", "command": "workbench.action.quickOpen" }
]
```

## keybindings.json

```json
[
  {
    "key": "cmd+k cmd+t",
    "command": "workbench.action.tasks.runTask",
    "args": "build",
    "when": "!inQuickOpen"
  },
  {
    "key": "cmd+i",
    "command": "editor.action.insertSnippet",
    "args": { "name": "React function component" },
    "when": "editorTextFocus && editorLangId == typescriptreact"
  }
]
```

- `args` passes a parameter to the command — running a *specific* task, inserting a *specific* snippet, opening a *specific* view. Most of the leverage in a custom keymap is here, not in remapping existing commands.
- Keybindings sync **per OS** by default, because `cmd` does not exist everywhere. Enabling cross-OS keybinding sync imports bindings that can never fire (`settings.md`).
- Keybindings belong to the active profile, like everything else.
- `keybindings.json` is user-scoped only. A repo cannot ship keybindings, which is deliberate: a repository that could rebind your keys would be an execution surface.

## When Clauses

The context keys that carry most of the weight:

| Key | True when |
|---|---|
| `editorTextFocus` | The caret is in a text editor — the correct guard for almost every editing command |
| `editorHasSelection`, `editorHasMultipleSelections` | Selection state |
| `editorLangId == python` | Language of the active editor — the way to make one key do different things per language |
| `resourceExtname == .md`, `resourceFilename`, `resourceDirname` | File-path predicates |
| `terminalFocus`, `inputFocus`, `listFocus`, `sideBarFocus`, `panelFocus` | Which surface has focus — the usual culprit for a key that works in the editor and not elsewhere |
| `inQuickOpen`, `suggestWidgetVisible`, `inlineSuggestionVisible`, `parameterHintsVisible` | Overlay states; guard against stealing Enter/Escape from a widget |
| `isMac`, `isLinux`, `isWindows`, `isWeb` | Platform, for a synced cross-platform keymap |
| `editorReadonly`, `inDebugMode`, `debuggersAvailable` | Mode predicates |
| `config.<setting>` | The value of any setting, so a binding can follow a preference |

Operators: `&&`, `||`, `!`, `==`, `!=`, `=~` (regex match), and `in` for set membership. Precedence is conventional; parenthesize anything with mixed `&&` and `||`.

The most common mistake is omitting the guard entirely. A binding with no `when` fires while you are typing in the find widget, the terminal, and the settings search box.

## Chords

`"key": "cmd+k cmd+s"` is a two-stroke chord. The first stroke shows a pending indicator in the status bar; the second resolves.

- Any key bound as a chord prefix cannot also be a single binding — `cmd+k` alone stops working the moment one `cmd+k <x>` chord exists.
- Chords are the answer to a keymap that has run out of combinations: one prefix gives you an entire namespace.
- A chord that never resolves usually has the second stroke consumed by the terminal or a widget; the troubleshooting log shows the prefix registering and the second stroke going elsewhere.

## The Terminal Steals Keys

When the integrated terminal has focus, most keystrokes go to the shell, not the editor — correct, because `Ctrl+C` must interrupt.

- `terminal.integrated.commandsToSkipShell` is the allowlist of editor commands that win even when the terminal has focus. It has a substantial default list; add to it with the command id, or exclude a default by prefixing with `-`.
- `terminal.integrated.sendKeybindingsToShell: true` inverts the policy: everything goes to the shell except a small core. Right for people living in a terminal multiplexer, wrong for most.
- `terminal.integrated.allowChords` (default true) — when false, chord prefixes go to the shell, which is what you want if your shell uses `Ctrl+K` or `Ctrl+B`.
- The practical rule: if a shortcut works everywhere except the terminal, it is this section, not a broken binding.

## Layouts And Remaps

- Bindings are stored by *key code*, and dispatched using the OS keyboard layout. On a non-US layout, a binding written as `ctrl+]` may require a different physical key or a dead key that cannot produce the combination at all.
- `keyboard.dispatch: "keyCode"` makes dispatch ignore the layout and use raw key codes. It is the fix for layouts where a needed combination is unreachable, at the cost of bindings no longer matching the printed legends.
- OS-level remaps (a swapped Alt, a Caps-to-Ctrl remap, a window-manager shortcut) are invisible to the editor and produce "no entry at all" in the troubleshooting log. Record them in `## Environment` — they invalidate default-binding advice everywhere else.
- On Linux, the desktop environment claims combinations (workspace switching, screenshots) before any application sees them. That is where a key with no log entry usually went.

## Bindings Worth Adding

Commands with real leverage that ship unbound or awkwardly bound:

| Command | Why bind it |
|---|---|
| `workbench.action.tasks.runTask` with an `args` label | One key for the build or test task, no picker |
| `workbench.action.terminal.focus` / `workbench.action.focusActiveEditorGroup` | Toggling between editor and terminal without the mouse |
| `editor.action.insertSnippet` with a named snippet | Skips the prefix and the widget entirely |
| `workbench.action.navigateBack` / `Go to Last Edit Location` | The return trip after chasing a definition |
| `editor.action.transformTo…` (upper/lower/title case) | Unbound by default, used constantly |
| `workbench.action.toggleSidebarVisibility` / `togglePanel` | Reclaiming screen width on a laptop |
| `workbench.action.quickOpenPreviousRecentlyUsedEditor` | The editor equivalent of Alt-Tab |
| `editor.action.smartSelect.expand` | Syntax-aware selection growth — replaces most manual selection |

Keep a custom keymap small. Every binding you add is one you have to remember on a machine that has not synced.

## Keybinding Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| No entry in the troubleshooting log | OS, window manager, or terminal consumed it | Layouts And Remaps; test in another application |
| Entry, no command dispatched | Every candidate's `when` was false | `Developer: Inspect Context Keys` |
| Entry, wrong command | A later binding wins | Search the Keyboard Shortcuts view for the key; user bindings are last |
| Works in the editor, not in the terminal | Terminal has focus and the command is not in the skip list | `commandsToSkipShell` |
| Chord prefix stopped working alone | A chord using that prefix exists | Expected; pick another prefix or drop the chord |
| Binding gone after switching machines | Per-OS sync, or a different profile | `settings.md` |
| The key cannot be produced on this layout | Layout-dependent dispatch | `keyboard.dispatch: "keyCode"`, or choose another key |
| A binding fires while typing in a widget | Missing `when` guard | Add `editorTextFocus` and the relevant `!…Visible` |
| Anything else | Open the Keyboard Shortcuts view and search by the key, not by the command name | — |

**When a keymap or a conflict resolution is worth keeping**, write the bindings to `~/Clawic/data/vscode/artifacts/keybindings-<what>.md` with the `when` clauses and the reason each exists, plus its `## Boxes` line in `memory.md` in the same turn (`memory-template.md`) — an unexported keymap is one machine failure from being rebuilt by memory. Keyboard layout, OS remaps and window-manager captures go to `## Environment`; a recurring conflict after editor updates earns a `## Due` row for a keybinding review.
