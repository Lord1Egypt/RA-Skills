# Git — The SCM Panel, Diffs, Merges, and Repos That Are Too Big for It

The Git integration is a front end over the `git` binary. When it behaves strangely the question is always which binary, which repository, and which working tree it decided it was looking at.

**Contents:** [Repository Detection](#repository-detection) · [Which Git Binary](#which-git-binary) · [Staging And Partial Commits](#staging-and-partial-commits) · [Diffs](#diffs) · [The Merge Editor](#the-merge-editor) · [Credentials And Remotes](#credentials-and-remotes) · [Big Repositories](#big-repositories) · [Submodules And Worktrees](#submodules-and-worktrees) · [Git Failure Signatures](#git-failure-signatures)

**Before changing Git behavior for a repo**, read `## Environment` and `## Projects` in `~/Clawic/data/vscode/memory.md` — the credential mechanism, the merge-tool decision and any autofetch exception for a large repo were settled once already.

## Repository Detection

- The editor scans the open folders for `.git`. A workspace opened *inside* a subdirectory of a repository still detects the repo above it, but only up to a bounded depth; a repo several levels up may not be found.
- `git.autoRepositoryDetection` controls whether it also picks up repositories in subfolders and in open editors. In a monorepo of many repos, `"subFolders"` populates the Source Control view; `false` keeps it to what you opened.
- `git.repositoryScanMaxDepth` bounds the search. A repo not appearing in a deeply nested workspace is this, not a broken integration.
- Multi-root workspaces show one repository section per root. A commit is per repository — there is no cross-repo commit, and the button acts on whichever section you pressed.
- A folder that is a repository but shows nothing usually has an `.git` file (a worktree or submodule pointer) rather than a directory; see below.

## Which Git Binary

- `git.path` (machine-scoped) selects the binary. Unset, the editor finds the first `git` in the environment it has — which is the *process* environment, not your shell's (`terminal.md`).
- The consequence: a Git installed by a version manager or a package manager that only exists on your interactive PATH is invisible, and the panel reports Git as missing while the terminal is fine.
- On Windows the choice between the Git for Windows binary and a WSL one changes line-ending and path behavior. Pick deliberately.
- `git.enabled: false` disables the whole integration for a workspace — the correct move for a folder inside a repository so large that every scan is a stall.

## Staging And Partial Commits

- Staging a **hunk** or a **selection** is available from the diff view's gutter and the context menu. This is the feature that makes small, reviewable commits practical, and most people never find it.
- The staged view and the working-tree view are separate editors. Editing the *staged* version directly is possible and is occasionally the cleanest way to fix a partially staged file.
- `git.enableSmartCommit` commits all changes when nothing is staged. It saves a click and it is exactly how an unintended file ends up in a commit — leave it off unless you always review the change list.
- `git.postCommitCommand` can push or sync automatically after a commit. Convenient and irreversible in the same gesture; a deliberate choice, not a default worth adopting silently.
- Amend, undo last commit, and unstage are all in the Source Control menu. "Undo Last Commit" is a soft reset — it keeps the changes, and the wording confuses people who expect the commit's content to be gone.

## Diffs

- Side-by-side vs inline is a toggle per diff editor; `diffEditor.renderSideBySide` sets the default, and `diffEditor.useInlineViewWhenSpaceIsLimited` switches automatically on narrow layouts.
- `diffEditor.ignoreTrimWhitespace` defaults to on, which hides whitespace-only changes. That is usually what you want and is occasionally why a diff looks empty.
- `diffEditor.hideUnchangedRegions.enabled` collapses untouched code — the setting that makes a large file's diff readable.
- Comparing arbitrary things: `--diff a b` from the command line, "Select for Compare" / "Compare with Selected" in the explorer, and Open Changes against any commit from the Timeline view.
- The **Timeline view** shows a file's commit history inline in the explorer and is the fastest path to "when did this line change" without leaving the editor.

## The Merge Editor

`git.mergeEditor` enables the three-way view: incoming, current, and the result you are building, with per-conflict accept buttons and a base view.

- The base pane is the part that matters. Two conflicting edits look arbitrary until you see what they both started from; without it, merge decisions are guesses.
- Conflicts that the editor marks as resolvable automatically still need review — "accept both" produces syntactically valid nonsense often enough to matter.
- The classic text-marker view (`<<<<<<<`) is still there for people who prefer it; the merge editor is a view over the same file, not a different mechanism.
- For a merge with many conflicting files, resolve in the merge editor and commit from the panel; the editor tracks which files still have unresolved conflicts, which a text search does not.

## Credentials And Remotes

- The editor delegates authentication to `git` itself, which uses the platform credential helper. Credentials are never stored by the editor, and never belong in a setting.
- A push that hangs with no prompt is almost always a credential helper waiting for input on a terminal you cannot see. Run the same push in the integrated terminal to get the prompt.
- SSH remotes need an agent with the key loaded in the environment the editor has — the same process-environment problem as everything else (`terminal.md`).
- Over Remote-SSH, git runs **on the remote host** with the remote's credentials and agent. Local credential helpers do not apply, and agent forwarding is what makes a private remote work (`remote.md`).
- HTTPS remotes with a token embedded in the URL leak the token into every log, every screenshot and any artifact you write. Use a credential helper; if a URL with a token appears in something being saved, replace it with a pointer (`memory-template.md`).

## Big Repositories

The settings that turn an unusable panel into a usable one, in order of impact:

| Setting | Effect |
|---|---|
| `git.autorefresh: false` | Stops the status refresh on every filesystem event — the biggest single win on a huge tree |
| `git.autofetch: false` | Stops periodic network calls; `git.autofetchPeriod` tunes it if you want it slower rather than off |
| `scm.diffDecorations: "none"` | Removes gutter decorations, which require a diff per open file |
| `git.untrackedChanges: "separate"` or `"hidden"` | A repository with thousands of untracked build artifacts spends its time listing them |
| `git.repositoryScanMaxDepth` | Bounds detection in a monorepo of repos |
| `git.ignoreLimitWarning` | Suppresses the "too many changes" warning — suppress the warning only after you know why there are that many |

The complementary half of this is excluding build output from search and watching, which reduces the event volume that triggers refreshes in the first place (`performance.md`).

## Submodules And Worktrees

- Submodules appear as separate repositories in the panel when `git.detectSubmodules` is on. Each has its own commit and push; a commit in the parent records the submodule's SHA and nothing else.
- `git.ignoreSubmodules` hides them from the parent's status, which is the fix for a parent repo that always shows a dirty submodule you are not working on.
- A **worktree** has a `.git` *file* pointing at the main repository's directory. The panel handles it, but tools that assume `.git` is a directory do not; an extension misbehaving only in a worktree is this.
- Opening two worktrees of the same repository in one multi-root workspace works and is a legitimate way to compare branches side by side, with two independent repository sections.

## Git Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Source Control panel empty in a real repo | Repo not detected (depth, subfolder policy), or `git.enabled: false` | Repository Detection |
| "Git not found" while the terminal has git | `git.path` unset and git only on the interactive PATH | Set `git.path`, or launch from a shell |
| Push or pull hangs forever | Credential helper prompting invisibly | Run the same command in the integrated terminal |
| Changes not appearing until a manual refresh | `git.autorefresh` off, or watcher limits exhausted | `performance.md` |
| Diff looks empty for a change you made | Whitespace-only change and `ignoreTrimWhitespace` | Toggle the setting for that diff |
| Commit included files you did not stage | Smart commit with nothing staged | Turn it off |
| Submodule always dirty | Submodule status surfacing in the parent | `git.ignoreSubmodules` |
| Everything slow only in this repo | Volume of changes and events | Big Repositories table |
| Git works locally, fails over SSH | Remote host's credentials and agent, not yours | `remote.md` |
| Anything else | Run the same operation in the integrated terminal; the panel is a front end, and the CLI error is the real one | — |

**When a Git configuration decision is made** — the credential mechanism for a host, the large-repo setting set and why, a merge-tool choice, a submodule policy — record it in `## Environment` of `~/Clawic/data/vscode/memory.md` if it is machine-wide, or in `## Projects` if it is one repo's (`memory-template.md`). Never write a remote URL that embeds a token: strip it and store the pointer. If a repo needed a whole block of large-repo settings, that block is an `artifacts/settings-<repo>-git.md` with its `## Boxes` line, because it will be needed again on the next machine.
