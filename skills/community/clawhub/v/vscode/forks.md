# Forks — Builds, Marketplaces, and the Extensions That Do Not Travel

"VS Code" is one codebase and several products. They share settings, keybindings and the extension API, and they differ in the one thing that decides whether your setup survives a switch: which marketplace they reach, and which extensions are licensed to them.

**Contents:** [The Builds](#the-builds) · [The Marketplace Boundary](#the-marketplace-boundary) · [Extensions That Do Not Travel](#extensions-that-do-not-travel) · [What Else Changes](#what-else-changes) · [Migrating Between Builds](#migrating-between-builds) · [Running Two Builds Side By Side](#running-two-builds-side-by-side) · [Choosing](#choosing) · [Fork Failure Signatures](#fork-failure-signatures)

**Before recommending an extension or a setting**, read `## Environment` in `~/Clawic/data/vscode/memory.md` for which build is in use and which extensions were already found unavailable, and open any `artifacts/decision-*.md` its `## Boxes` index names about the build choice. `vscode_build` and `extension_marketplace` in `config.yaml` are declarations — apply them without asking.

## The Builds

| Build | What it is | Marketplace | Config directory |
|---|---|---|---|
| **Stable** | The official product | Microsoft | `Code` |
| **Insiders** | Daily build of the same product, installs alongside stable | Microsoft | `Code - Insiders` |
| **VSCodium** | Community build of the open-source repository, telemetry-free | Open VSX | `VSCodium` |
| **Cursor** | Fork with its own agent and editing model, tracking upstream with a lag | Open VSX plus its own | its own |
| **Windsurf** | Fork with its own agent workflows | Open VSX plus its own | its own |
| **code-server** | The editor served in a browser from a machine you run | Open VSX | its own |
| **Codespaces / web** | Hosted, browser-based, official | Microsoft | server-side |

The open-source repository is the common base. The official builds add Microsoft's branding, telemetry, marketplace client and license; forks strip or replace those, and add their own features. Everything about settings, keybindings, tasks, launch configs and the extension API applies to all of them (`settings.md`).

## The Marketplace Boundary

- The Microsoft marketplace's terms restrict its use to Microsoft's own products. That is a licensing boundary, not a technical one, and it is why forks ship Open VSX instead.
- **Open VSX** is an open registry with the same extension format. Most popular open-source extensions are published to both; the gaps are Microsoft's own extensions and a long tail of publishers who never opted in.
- Extension **ids are the same across registries** (`publisher.name`), so `.vscode/extensions.json` is portable — a recommendation simply does not resolve where the extension is absent (`extensions.md`).
- A `.vsix` file can be installed from disk in any build. That is the escape hatch for an extension available in one registry only, at the cost of no auto-update and, for Microsoft-licensed extensions, a license you are not covered by.
- Patching `product.json` to point a fork at the Microsoft marketplace circumvents the terms and is overwritten by the next update. It is the wrong answer for a machine you rely on.

## Extensions That Do Not Travel

The categories, rather than a list that dates:

| Category | Why | What forks do |
|---|---|---|
| Microsoft's language servers for its own ecosystems | Licensed to official builds only | Ship an open-source alternative — often the open server the closed one was built on, with fewer features |
| The Remote Development pack (SSH, Containers, WSL) | Same licence restriction | Forks ship their own remote implementations, with their own gaps; code-server sidesteps it by being the server |
| Live collaboration | Requires Microsoft's service | Third-party alternatives, generally weaker |
| First-party AI assistants | Tied to the vendor's account and product | Each fork's own assistant is usually its whole reason to exist |
| Everything else | Nothing restricts it | Published to both registries, or installable as a `.vsix` |

The practical test before switching build: list the extensions you would notice losing within a week, and check each one's availability in the target registry by **id**. Usually the list is three or four, and one of them decides the question.

## What Else Changes

- **Config directory and CLI name.** Each build keeps its own settings, keybindings, snippets, profiles and extensions directory, and installs its own command (`code`, `code-insiders`, `codium`, the fork's name). "I already set that" can be true in the other build's file (`settings.md`).
- **Version lag.** A fork rebasing on upstream is weeks to months behind. A setting, API or feature from a recent release may simply not exist yet — check the fork's own version, not the upstream release notes.
- **Remote server compatibility.** The client and the server it installs must match. Two builds connecting to the same host install two separate servers, doubling disk use there (`remote.md`).
- **Settings Sync.** Official builds sync to a Microsoft account; forks either implement their own or offer none. Cross-build sync is not a thing — export and import a profile instead.
- **Telemetry.** Official builds collect it, subject to `telemetry.telemetryLevel`; VSCodium ships with it removed; forks vary and have their own policies (`security.md`).
- **Fork-specific settings.** A fork adds its own namespaces. Those keys are dead weight in another build, and a settings file shared between builds accumulates them harmlessly but confusingly.

## Migrating Between Builds

1. **Export a profile** from the source build — settings, keybindings, snippets, tasks, UI state, and the extension list in one file (`settings.md`).
2. **Check availability by id** in the target's registry for every extension in the list, before importing anything.
3. **Import the profile**; extensions that do not resolve are reported and skipped.
4. **Fill the gaps deliberately**: an open-source language server for a licensed one, the fork's remote implementation, a `.vsix` where the licence allows it.
5. **Re-do machine-side items** that do not travel: the CLI shim (`Shell Command: Install…`), `$EDITOR`/`$GIT_EDITOR` if they name the old command, any script or git config that hardcodes `code`.
6. **Record the decision and its cost** in `~/Clawic/data/vscode/artifacts/decision-build.md`, so the next time an extension turns out to be missing there is an artifact explaining why rather than a rediscovery.

## Running Two Builds Side By Side

Legitimate and common: stable for work, Insiders or a fork for a feature.

- They coexist by design — separate config directories, separate extension directories, separate CLI names.
- They do **not** share settings. Keeping them aligned means exporting a profile between them, or accepting drift.
- `--user-data-dir` and `--extensions-dir` give any build a throwaway environment, which is the cleanest way to trial a fork without touching your real setup.
- Two builds opening the same folder is fine; two builds with a git operation in flight on the same repository is not, for the same reason two terminals are not.
- On the same remote host, each installs its own server; watch the disk (`remote.md`).

## Choosing

| Situation | Build | Why |
|---|---|---|
| Default, and the ecosystem's extensions matter | Stable | Every extension resolves; nothing to work around |
| Telemetry-free is a requirement | VSCodium | Purpose-built for it; accept the licensed-extension gap |
| The fork's agent workflow is the reason you are here | Cursor or Windsurf | The feature is the product; verify your load-bearing extensions first |
| Editing on a server, from a browser | code-server or a tunnel | Tunnel keeps the official client; code-server keeps the machine self-contained |
| Trying an upcoming feature without risk | Insiders, with `--user-data-dir` | Installs alongside stable, no shared state |
| Anything else | Whatever `vscode_build` says, stable if unset | State the assumption before giving build-specific advice |

## Fork Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Extension not found by name in the Extensions view | Not published to this build's registry | Search by id; then `.vsix`, then an alternative |
| Extension installs but its language features are absent | The open-source stand-in has a narrower feature set | Compare features, not names |
| Remote-SSH missing or behaving differently | Licensed remote pack unavailable; the fork's own is in use | `remote.md` |
| A documented setting does not exist | Version lag against upstream | Check the build's own version |
| Settings "reverted" after switching builds | Different config directory | `settings.md` |
| `code` opens the wrong editor | Two CLI shims, or `$EDITOR` naming the old one | Reinstall the shim; fix the env var |
| Remote host filling up | Two builds, two server installations | Prune old server directories (`remote.md`) |
| Sync not working after a switch | Cross-build sync does not exist | Export and import a profile |
| Anything else | Reproduce in the official stable build; a difference localizes it to the fork | — |

**When a build decision is made or an extension turns out to be unavailable**, write it to `~/Clawic/data/vscode/artifacts/decision-build.md` — the build chosen, what was rejected, the extensions lost and their replacements, and the condition that would make you revisit — with its `## Boxes` line in the same turn (`memory-template.md`). Record the build and its config directory in `## Environment`, and each unavailable extension as a row in `## Extensions` with verdict `dropped` and the reason, so the same search is not repeated next quarter. `vscode_build` and `extension_marketplace` are declarations and belong in `config.yaml`, not in memory.
