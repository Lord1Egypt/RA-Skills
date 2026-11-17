# Extensions — Conflicts, Crashes, and What They Cost

Extensions share one process. One badly behaved extension slows, hangs or kills the host for all of them, and none of them will tell you which.

**Contents:** [The Extension Host](#the-extension-host) · [Bisect First](#bisect-first) · [Activation Cost](#activation-cost) · [Conflicts](#conflicts) · [Scoping And Disabling](#scoping-and-disabling) · [Recommending To A Team](#recommending-to-a-team) · [Versions And Pinning](#versions-and-pinning) · [Auditing What Is Installed](#auditing-what-is-installed) · [Extension Failure Signatures](#extension-failure-signatures)

**Before recommending or installing anything**, read `## Extensions` in `~/Clawic/data/vscode/memory.md` — or `extensions.md` if its `## Boxes` index points there — for what is already adopted, what was dropped and why. Never propose an id listed in `banned_extensions` in `config.yaml`; if one is already installed, say so.

## The Extension Host

- All extensions run in one separate process, not in the window. That is why an extension crash shows "Extension host terminated unexpectedly" and leaves the editor alive but inert: no completions, no linting, no git decorations.
- `Developer: Restart Extension Host` recovers without reloading the window and keeps unsaved editors. Reach for it before `Developer: Reload Window`.
- Remote windows have **two** hosts: a local one for `ui` extensions and a remote one for `workspace` extensions (`remote.md`). A crash in one leaves the other working, which makes the symptom partial and confusing.
- The crash reason is in `Developer: Show Logs… → Extension Host`. It usually names a file inside the guilty extension's directory in the stack trace — that name is the fastest identification available, faster than bisect when the log is readable.
- An extension can hang the host without crashing it: a synchronous file walk over a monorepo, or a language server started per file. The symptom is the whole UI freezing for seconds at a time (`performance.md`).

## Bisect First

`Help: Start Extension Bisect` disables half the extensions, asks whether the problem persists, and repeats. With N extensions it converges in ⌈log₂N⌉ rounds — 40 extensions is 6 reloads, versus up to 40 for disable-one-at-a-time. It ends by naming the extension and offering to disable or report it.

Rules that make bisect actually work:

- Have a **deterministic reproduction** before starting. Bisect asks a yes/no question each round; one wrong answer sends it into the wrong half and it will name an innocent extension with full confidence.
- Intermittent problems are the exception: for those, use a clean window (`--disable-extensions --user-data-dir <tmp>`) to establish that extensions are involved at all, then re-enable in halves manually and live with each half for a while.
- Bisect operates on the current profile. A problem that only appears in one profile is already half-localized (`settings.md`).

## Activation Cost

`Developer: Show Running Extensions` lists activation time and lets you profile the host's CPU. Read it *after* bisect, when you are optimizing rather than diagnosing.

- Activation events decide when an extension wakes up: on a language, on a command, on a file glob, on workspace contents, or `*` (always, at startup). The `*` extensions are the only ones with an unconditional startup cost, and there are usually two or three of them.
- Activation time is measured per extension but the host is shared: three extensions at 300 ms each are 900 ms of startup, serialized.
- An extension activating in *every* window regardless of language is either using `*` or matching a glob that is too broad. That is a legitimate reason to scope it to specific workspaces.
- Startup contribution and window-load time are different numbers. Use `Developer: Startup Performance` for the total, this view for the attribution (`performance.md`).

## Conflicts

The four kinds, each with its own signature:

| Kind | Signature | Resolution |
|---|---|---|
| **Two formatters for one language** | Save does nothing, or a prompt appears on manual format | Language-block `defaultFormatter`; ban the loser (`formatting.md`) |
| **Two language servers for one language** | Duplicate diagnostics with slightly different wording, or completions from two sources | Disable one for the workspace; keeping both is never right |
| **Keybinding collisions** | A shortcut does something unexpected, or nothing | Keyboard-shortcut troubleshooting names the winner (`keybindings.md`) |
| **Overlapping features** | Two git blame decorations, two bracket colorizers, two auto-import providers fighting on save | Pick one; the built-in feature usually won years ago and the extension is legacy |

The specific legacy trap: features that were once extensions are now built in — bracket pair colorization, sticky scroll, the merge editor, basic auto-import. An old extension providing one of them still registers, still costs activation, and now conflicts with the built-in. An extension list that has never been audited is mostly this.

## Scoping And Disabling

| Action | Effect |
|---|---|
| Disable | Off everywhere, kept installed |
| Disable (Workspace) | Off for this folder only — the surgical fix for a conflict that only matters in one repo |
| Enable (Workspace) only | The inverse: heavy extensions off by default, on where needed |
| Profile membership | The clean version of the above, at the cost of managing profiles (`settings.md`) |
| `--disable-extensions` | Launch flag; nothing loads. The baseline for "is this core or an extension" |
| `--extensions-dir <path>` | A completely separate extension set, for testing without touching the real one |

## Recommending To A Team

`.vscode/extensions.json` is the repo's onboarding document:

```json
{
  "recommendations": ["esbenp.prettier-vscode", "dbaeumer.vscode-eslint", "ms-python.python"],
  "unwantedRecommendations": ["hookyqr.beautify"]
}
```

- Recommendations prompt once per folder and appear under `@recommended` in the Extensions view. They are a suggestion, never an install.
- `unwantedRecommendations` is the underused half: it suppresses a recommendation another extension makes, which is how you stop a second formatter being suggested to every new contributor.
- Keep the list to what the repo genuinely needs to build, debug and format. A list of twenty is ignored; a list of four is followed.
- Recommendations are ids, and ids differ between marketplaces. A repo shared with fork users needs ids that exist on Open VSX or a note saying so (`forks.md`).

## Versions And Pinning

- Auto-update is on by default (`extensions.autoUpdate`, application-scoped). It is the right default and the reason a working setup breaks on a Tuesday with no local change.
- **Install Specific Version…** pins an extension after a bad release. The pin holds until you update manually — record why in the extension's `## Extensions` row in `memory.md`, or the pin becomes a mystery.
- **Pre-release versions** are a separate channel per extension, opted into individually. A pre-release channel silently enabled explains behavior that matches no documentation.
- An extension can require a minimum editor version; on an older editor the marketplace installs the last compatible release instead, silently. "The feature is missing" on an old install is usually this.

## Auditing What Is Installed

A quarterly pass, cheap and worth scheduling (`## Due` in `memory.md`):

1. List what is installed and, for each, whether it was used since the last audit. Anything you cannot name a use for goes.
2. Check for features now built in (the legacy trap above).
3. Check for duplicate roles: two formatters, two git tools, two REST clients.
4. Read `Developer: Show Running Extensions` and question anything activating on `*`.
5. Check publisher identity on anything doing network or shell work — extension supply chain is a real attack surface (`security.md`).
6. Record the verdict per extension in `## Extensions` of `memory.md`, with the reason, so the next audit is a diff rather than a rerun — a ban also goes to `banned_extensions` in `config.yaml`.

## Extension Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| "Extension host terminated unexpectedly" | One extension crashed the shared process | Log first, bisect second |
| Everything works except one extension's features | It failed to activate; its own output channel has the error | Output panel → the extension's channel |
| "Cannot find module" right after installing | The host has not reloaded with the new code | `Developer: Restart Extension Host` |
| Installed but invisible in a remote window | Installed on the wrong side | Install into the remote (`remote.md`) |
| Works in one folder, not another | Disabled for that workspace, or a different profile is active | Extensions view → filter by workspace |
| Appeared to install, not in the list | Marketplace mismatch on a fork | `forks.md` |
| Behavior changed with no local change | Auto-update shipped a new version | Install Specific Version to confirm, then pin or report |
| Editor freezes for seconds, no crash | An extension doing synchronous work on a large tree | Profile the host from Show Running Extensions |
| Anything else | Clean window with `--disable-extensions --user-data-dir <tmp>` | Survives = core, disappears = bisect |

**After any extension verdict** — adopted, dropped, banned, pinned, or blamed for a conflict — write the row in `## Extensions` of `~/Clawic/data/vscode/memory.md` with the id, the verdict and the one-clause reason (`memory-template.md`). A ban also goes to `banned_extensions` in `config.yaml`, because that is a declaration: the memory row carries the reason, the config key carries the enforcement. **After an audit**, record the date in `## Due` and any activation-cost measurement alongside its row — without the measurement the same extension gets re-suspected every year.
