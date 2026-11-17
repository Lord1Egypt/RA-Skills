# Settings — Scopes, Profiles, Sync, and Why Your Value Lost

A setting is never "broken". It is resolved, at a scope, against a chain that has seven links. Find the winner before changing anything.

**Contents:** [The Resolution Chain](#the-resolution-chain) · [Scope Metadata](#scope-metadata) · [Language-Specific Blocks](#language-specific-blocks) · [Variable Substitution](#variable-substitution) · [Where The Files Live](#where-the-files-live) · [Profiles](#profiles) · [Settings Sync](#settings-sync) · [Diagnosing A Setting](#diagnosing-a-setting) · [Settings Worth Setting Once](#settings-worth-setting-once)

**Before proposing any setting**, read `## Environment` and `## Projects` in `~/Clawic/data/vscode/memory.md`, and open any `artifacts/settings-*.md` its `## Boxes` index names for this repo — the scope that worked here was decided once already. `settings_scope_default` in `config.yaml` says where a new setting goes when the user does not say.

## The Resolution Chain

Later wins. This is the full order; there is no eighth link.

1. **Default** — shipped with the editor and with every installed extension. An extension can change a default, which is why a value you never set can change after an install.
2. **User** — your settings, on this machine and on every machine you sync to.
3. **Profile** — if a profile is active, its settings *replace* the user settings entirely rather than layering on them. This is the single most confusing part of profiles.
4. **Remote / WSL** — settings attached to the remote host or distro; apply only when the window is connected to it.
5. **Workspace** — `.vscode/settings.json` in a single-folder workspace, or the `settings` block of a `.code-workspace` file. If both exist for the same window, the `.code-workspace` block is the workspace scope and the folder's `.vscode/settings.json` becomes folder scope.
6. **Folder** — `.vscode/settings.json` inside each root of a multi-root workspace.
7. **Language block** — `"[python]": { … }` inside whichever of the above wins for that key.

Two consequences worth stating out loud: a workspace setting cannot be overridden by a user setting, ever; and a language block at a *lower* scope loses to a plain key at a *higher* scope, so a workspace `editor.tabSize` beats a user `"[python]": {"editor.tabSize": 4}`.

## Scope Metadata

Every setting carries a scope in its schema, and placing it lower than its scope allows makes it *ignored*, not overridden — usually with no error beyond a grey entry in the Settings UI.

| Scope in the schema | Settable in | Typical members |
|---|---|---|
| Application | User settings only | Update channel, telemetry level, title-bar style, extension auto-update, locale |
| Machine | User or remote settings; never a workspace file | Anything naming a local executable or a filesystem path outside the workspace |
| Machine-overridable | User, remote, and a *trusted* workspace | Default terminal profile, some tool paths — silently dropped in Restricted Mode |
| Window | User, remote, workspace; not per folder | Window title, zen mode, most `workbench.*` |
| Resource | Every scope including per folder | `editor.*`, `files.*`, formatter and linter keys |

The Settings UI is the fastest reader of this metadata: open the key there and the scope tabs that are disabled tell you where it cannot go.

## Language-Specific Blocks

```json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.tabSize": 4,
    "editor.codeActionsOnSave": ["source.organizeImports.ruff", "source.fixAll.ruff"]
  },
  "[markdown]": { "editor.formatOnSave": false, "editor.wordWrap": "on" }
}
```

- Only `editor.*` and a small set of resource-scoped keys are valid inside a language block. Putting `files.exclude` there does nothing.
- The language id is the one in the status bar, not the file extension: `javascriptreact`, not `jsx`; `shellscript`, not `bash`; `jsonc` for files with comments.
- A language block with a single key still overrides the plain key for *that key only* — the rest of the plain settings still apply. It is a merge, not a replacement.

## Variable Substitution

Valid in `settings.json` (a limited set), and everywhere in `tasks.json` and `launch.json`.

| Variable | Resolves to | Trap |
|---|---|---|
| `${workspaceFolder}` | Absolute path of the folder | Ambiguous in multi-root — use `${workspaceFolder:name}` |
| `${workspaceFolderBasename}` | Folder name only | — |
| `${file}` `${relativeFile}` `${fileBasenameNoExtension}` | The active editor | Nothing using these is runnable when no editor is focused |
| `${fileDirname}` `${fileWorkspaceFolder}` | Directory of the active file / its root | `${fileWorkspaceFolder}` is the multi-root-safe form |
| `${env:NAME}` | Process environment of the editor | Not the shell's environment (`terminal.md`) |
| `${config:some.setting}` | Another setting's value | Reads the *resolved* value, so it inherits this whole chain |
| `${command:extension.command}` | Whatever the command returns | Runs the command every time the variable resolves — slow ones cost a second per launch |
| `${input:id}` | A prompt defined in the `inputs` array | The only interactive one; `pickString`, `promptString`, `command` |
| `${pathSeparator}` | `/` or `\` | The portable way to build paths in a task |

## Where The Files Live

| Item | macOS | Linux | Windows |
|---|---|---|---|
| User settings | `~/Library/Application Support/Code/User/settings.json` | `~/.config/Code/User/settings.json` | `%APPDATA%\Code\User\settings.json` |
| Keybindings | same folder, `keybindings.json` | same | same |
| Snippets | same folder, `snippets/` | same | same |
| Profiles | same folder, `profiles/` | same | same |
| Extensions | `~/.vscode/extensions` | `~/.vscode/extensions` | `%USERPROFILE%\.vscode\extensions` |

Forks and channels use their own directory (`Code - Insiders`, `VSCodium`, the fork's own name), which is why "I already set that" can be true and invisible at the same time (`forks.md`). Portable mode moves all of it into a `data/` folder next to the binary.

## Profiles

A profile bundles settings, extensions, keybindings, snippets, tasks and UI state. It is the right tool when two contexts want *mutually exclusive extension sets*, and the wrong one when they merely want different themes.

- A profile **replaces** user settings; it does not layer on the default profile. Moving to a profile and finding half your settings gone is the expected behavior, not a bug.
- Profiles can be attached to a folder, so opening that folder switches automatically. This is what makes a heavy language stack cost nothing in unrelated repos.
- A **temporary profile** exists for exactly this: reproducing a bug in a clean environment without touching the real one, and disappearing on close.
- Export produces a single portable file (or a gist). An unexported profile is a machine-local artifact — schedule the export (`## Due` in `memory.md`).
- Contents can be *shared* rather than copied when creating a profile: share the keybindings, isolate the extensions. Sharing everything makes the profile pointless.

## Settings Sync

Syncs settings, keybindings, snippets, tasks, UI state, extensions and profiles, per account.

- Keybindings sync **per OS by default**, because modifier keys differ. Turning on cross-OS keybinding sync imports `cmd` bindings onto a machine with no `cmd` key.
- Machine-specific keys should never sync: add them to `settingsSync.ignoredSettings`, and troublesome extensions to `settingsSync.ignoredExtensions`. Interpreter paths and window sizes are the usual offenders.
- Conflicts open a merge view rather than picking a winner. A machine that has been offline for weeks and then syncs is the classic conflict; resolve it there, not by overwriting.
- Sync is per profile. Two machines "disagreeing" is often two different active profiles, not a sync failure.
- `Settings Sync: Show Synced Data` lists every machine and lets you turn one off — the fastest fix when an old laptop keeps re-pushing a stale value.

## Diagnosing A Setting

In order. Stop at the first step that explains it.

1. `Preferences: Open Default Settings (JSON)` — confirm the default and the exact key spelling. A key that does not exist is silently kept in the file.
2. Open user, remote, workspace and folder JSON in that order and search for the key. The last file that has it wins.
3. Search for a `"[language]"` block containing it in the winning file.
4. Check the scope metadata in the Settings UI — a greyed key is being ignored, not overridden.
5. Check the active profile. `Preferences: Open Settings (JSON)` opens the *active profile's* settings, which may not be the file you edited yesterday.
6. Check Restricted Mode. Machine-overridable settings are dropped in an untrusted folder (`security.md`).
7. Only then, check whether an extension is writing the value at runtime — some do, and `Developer: Show Logs…` names them.

## Settings Worth Setting Once

Defaults tuned for a first-run demo that most people eventually change, with the reason.

| Setting | Why |
|---|---|
| `files.insertFinalNewline`, `files.trimTrailingWhitespace` | Removes an entire class of diff noise that no formatter covers for non-code files |
| `editor.rulers` | A visible line width ends the "why did the formatter wrap that" argument |
| `files.autoSave` | Choose deliberately: `afterDelay` disables format-on-save (`formatting.md`), `onFocusChange` does not |
| `explorer.confirmDelete`, `explorer.confirmDragAndDrop` | Off by accident is how files move silently in a large tree |
| `editor.stickyScroll.enabled` | Keeps the enclosing signature visible; costs nothing |
| `workbench.editor.enablePreview` | Preview tabs replacing each other is the top complaint of people who think they lost a file |
| `search.useIgnoreFiles` | On by default and respects `.gitignore`; turning it off is how you search `node_modules` by accident |
| `telemetry.telemetryLevel` | Application-scoped, so it can only be set in user settings (`security.md`) |

**When a settings block finally resolves the problem**, write it to `~/Clawic/data/vscode/artifacts/settings-<what>.md` with the scope it lives at and what it fixed, and add its `## Boxes` line in the same turn (`memory-template.md`). Record scope-related surprises — a profile that shadowed a value, a machine-scoped key silently dropped, a sync conflict — as a line in `## Environment`. If the user states a preference while doing this (formatter, indentation, scope habit), it is a declaration: write it to `config.yaml`, not to memory.
