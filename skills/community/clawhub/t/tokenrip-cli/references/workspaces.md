# Workspaces

A workspace is the authoritative home for a project's artifacts, tables, flat folders, and tasks, with an internal/shared audience per item and guests you add or invite by email. Commands: `rip workspace …` (alias `rip ws`). Identifier: the workspace's **slug or id** (`rip workspace load tokenrip-social`), in any case, resolved by the server among the workspaces you reach. A slug none of them has is `WORKSPACE_NOT_FOUND`, as an unknown id is; a slug two of your workspaces share is refused with each candidate's id (`AMBIGUOUS_REFERENCE`, printed with its home and name): use the id. API: `/v0/workspaces`; MCP: the `workspace_*` tools (`workspace_list`, `workspace_load`, `workspace_changes`, …). Return to [SKILL.md](../SKILL.md) for the top-level decision trees.

## Membership and audience

Membership is resolved live:

- The personal owner, or the owning team's owner and admins, are internal **admins**.
- Other members of the owning team are internal **editors**.
- People added to the workspace are **guests** (`external`: shared items only), each as an **editor** or a **viewer**. Internal access (seeing everything) comes only from owning the workspace or being in its team: to give someone everything, add them to the owning team (`rip team add <team> <email>`; each team member is billed). Internal editors may invite; only admins change a guest's role or remove them. Team invites (`rip team add <team> <email>`) work the same way: your own person's other account is added at once; anyone else gets an emailed invite whose link is safe to share. Someone new to Tokenrip joins at sign-in with the emailed code; someone already on it presses Join on the invite page. `rip team show <team>` lists pending invites, and `rip team remove <team> <email-or-invite-id>` cancels one.

Every item has an `audience`: `internal` (the owner and the team) or `shared` (guests too). Internal members create `internal` items by default; guest editors create `shared` ones. `rip workspace list` prints each workspace's name, full id, slug, personal/team home, `membership/role`, permitted capabilities, and `needsYou=<n>`: how much waits on this agent key there (approved tasks for it to carry out, reviews addressed to it, the In review children of one parent counting once, and To do tasks naming it); `rip workspace show` (and `load`) add a `Can:` line (the operations your live capabilities allow), and `show` the `audiences`. With `--json` the full `capabilities` map is included. Trust the capabilities, not the role name.

## When to use

For work that belongs to a Tokenrip workspace:

- "work on project X from this harness" → `rip workspace load <workspace>`: follow its `Instructions`, handle `Waiting on you` first, then state `--why` on every write
- "post this", "send that email", "publish it" → propose it first (`rip task propose`, [references/tasks.md](tasks.md)) and act only on what comes back approved
- "take the next draft", "run the writer routine" → claim it by its tags (`rip task start --workspace-id <ws> --type <type> --step <step>`) as your instructions name them
- "hand this to Codex", "ask Maya's agent" → name the agent as `agent:<handle>` from load's `Agents` in `rip task add --assignee` or `--reviewer`
- "who worked on this, and toward what" → `rip workspace sessions <workspace>`
- "what changed since I last looked" → `rip workspace changes <workspace>`, then `rip workspace ack <workspace> --delivery-token <token>`
- "this document the operator is looking at" → `rip workspace view context <workspace>`, then write to the returned `savedArtifactId` with its `savedVersionId` / `savedRevision` as the precondition. Never guess from focus.
- "open that document in their browser" → `rip workspace view open …` and read the receipt (`queued` / `deferred` / `applied` / `disconnected`)
- "share this with the client" → `rip workspace adopt … --audience shared` for standalone content, `rip artifact patch <id> --audience shared` for a workspace artifact, `rip folder share-contents` for a folder and everything in it
- "send this to someone who has no account" → `rip artifact patch <id> --visibility link` (anyone with the URL can read it; `--visibility private` turns it off). Earlier versions become readable too; prune them first (`rip artifact prune-versions <id>`) if they shouldn't be
- "invite bob@example.com to this" → `rip workspace member add <workspace> bob@example.com --why "<the goal>"`, then read the row's `status`: `invited` (no account holds the address) → tell the person "invited" and give the `inviteUrl`; `member` (a verified address, alias or id) → they are in, and `inviteUrl` is null ([Members and invites](#members-and-invites))
- "give the client read access to what we share" → `rip workspace member add <workspace> <email> --role viewer --why "<the goal>"`
- "give a colleague access to everything" → `rip team add <team> <email>` (the workspace's owning team; a personal workspace's internal access is its owner's alone, so the work moves to a team)
- "bring an existing artifact or folder into the workspace" → `rip workspace adopt`
- "only one agent at a time", "send this once", several agents sharing a row → a plain append decides who goes first ([Coordinating agents on a row](#coordinating-agents-on-a-row))
- "I'm stopping here" → nothing to end: your session is recorded. Complete what you finished (`rip task done`), `rip task stop` what you hold but didn't finish, with its body saying how far it got (`rip task update`); a proposal stays In review ([When you stop](#when-you-stop))

## Lifecycle and members

```bash
rip workspace create <slug> [--name "Roadmap"] [--description <text>] [--team <team-slug-or-id>] --why "<the goal>"
rip workspace list                                   # names, ids, membership/role
rip workspace show <workspace>                       # adds Can: (capabilities) and audiences
rip workspace update <workspace> [--name <name>] [--description <text>]
rip workspace delete <workspace>                     # admins, only when your person names this workspace and approves; it and everything in it go to the trash for 30 days
rip trash restore <workspace-id> --why "<goal>"     # bring it back, as it was, until its purge date

rip workspace member list <workspace>                # members and pending invites; owner and team access are not listed
rip workspace member add <workspace> <email|alias|account-id> [--role viewer|editor] [--note <text>]
rip workspace member set-role <member> [--workspace-id <workspace>] --role viewer|editor
rip workspace member remove <member> [--workspace-id <workspace>]
```

`--name` defaults to the slug. `--team` takes the team's slug or id; only the team's owner and admins can create a team workspace. A team that still owns workspaces, including workspaces in the trash, cannot be deleted (`TEAM_OWNS_WORKSPACES`), nor can a team on a paid plan (`TEAM_HAS_PLAN`).

A team-owned workspace needs a paid plan, and every owner has a maximum number of live workspaces; workspaces in the trash do not count. `rip workspace create`, and `rip trash restore` of a workspace, when the owner has no room are refused `WORKSPACE_LIMIT_REACHED` with the owner, plan, limit and count. For a team without a plan, tell the person the limit; at the maximum, tell the person they can free a slot by deleting a workspace they choose. Never pick one yourself: delete a workspace only when the person names it and approves deleting it. Nothing was created or restored.

Every write here (create, update, delete, member add/set-role/remove, adopt) takes `--why`, like any workspace write ([Why](#why-every-write-says-what-it-is-for)).

Deleting a workspace needs `deleteWorkspace` (internal admins), and you delete one only when your person names that workspace and approves deleting it: it need not be empty. The workspace goes to the trash with everything in it (files, folders, tasks, pins), and restoring it brings all of it back. While it is in the trash, every call on it answers 410 `WORKSPACE_DELETED` with `deletedAt` and `purgeAt`; admins also get `restorable` and `deletedBy`. It leaves `rip workspace list`, and its slug stays held until it is purged. `rip trash restore <id>` brings it back until `purgeAt`; after that the daily purge removes it for good. `rip trash purge <id>` removes it for good now (permanent; only when your person asks), as Delete forever does in the dashboard.

## Members and invites

Bring someone in by their email address, whether or not they use Tokenrip. `member add` also takes an alias or account id. Everyone added is a guest, who sees shared items only, as `--role editor` (the default) or `--role viewer` (read-only). `--membership internal` is refused with `INTERNAL_NEEDS_TEAM`, whose message names the path: add them to the owning team, where each member is billed, or add them as a guest; on a personal workspace, internal access is the owner's alone, so work with others internally in a team. (`--membership external` is accepted and changes nothing; the flag is going away.) Internal admins and editors may add and invite; only admins change someone's role or remove them.

- **An address with no Tokenrip account** becomes an invite: the row comes back with `status: "invited"`, the address in `email`, and an `inviteUrl`. Tokenrip emails the person, naming the inviter (the verified address of the person who owns your account), the workspace and the access, quoting your `--note` (plain text, at most 280 characters), with a button to the invite page and a line they can paste into an AI assistant. Nothing in the email or the link signs anyone in, so the `inviteUrl` is safe to share in a chat as well.
- **The invite is claimed by signing in.** When the person signs in with the six-digit code Tokenrip emails to that address (in the browser, or through an agent following `https://tokenrip.com/setup`), every invite waiting on the address becomes their membership. There is no accept step. The row then reads `status: "member"` with their `accountId`.
- **Someone who already uses Tokenrip** (their verified address, alias or account id) is added at once: the row comes back with `status: "member"` and `inviteUrl: null`. An add by address emails them that they were added; an add by alias or id emails them only when their account has one verified person and yours has one to send from. Their agents see the workspace on their next `rip workspace list`.

Adding the same person again with the same access changes nothing, except that it resends a pending invite. Adding them with a different role needs an admin. `set-role` and `remove` take the member row's `id` from `member list`, which stands alone, or an account id, alias or email address with `--workspace-id`. `set-role` changes `--role`; the member stays a guest. An alias or account id that names no account is `ACCOUNT_NOT_FOUND`; removing someone with no row in the workspace changes nothing. An address finds the row of the person who holds it, on their primary account, or the row an add or invite by that address made; for a member on another of their accounts, use the row `id`. Removing an invite cancels it.

An add by email needs a verified person behind your account to send from: without one it is refused `NO_OPERATOR` (or `OPERATOR_AMBIGUOUS` when several people share the account). An add by alias or id then goes ahead with no email, and a `--note` is refused, since nothing carries it. Invite emails are limited per person: by default 20 an hour across all your accounts, one per invite an hour, and one per address an hour; past them the add is refused `RATE_LIMITED`, except that an add of an existing account by alias or id without a note goes ahead without the email.

Adding someone who is already internal (the owner or a member of the owning team) is refused (`WORKSPACE_MEMBER_INTERNAL`). When a guest later joins the owning team, their guest row is consumed, so leaving the team ends access. Removals and downgrades take effect on the next request and stop any task holds the new role does not allow (the tasks go back to To do).

## Adopt existing content

```bash
rip workspace adopt <workspace> <artifact-id>... [--audience internal|shared] [--destination-folder-id <uuid>]
rip workspace adopt <workspace> --folder <folder-id-or-slug> [--audience internal|shared]      # one of your personal folders, with its current artifacts
```

`--audience` defaults to `internal` (`shared` for an external editor). Adoption is atomic, makes no copy, and keeps identity and history. You must own the content; its team shares are removed. Refused before any effect: `MIXED_OWNERSHIP`, `ALREADY_IN_WORKSPACE`, `INELIGIBLE_STORAGE` (public assets, independently hosted content, public history), `WORKSPACE_BULK_LIMIT` (more than 500 items). Sharing an adopted artifact exposes every version it keeps. There is no move-out. A destination folder must belong to the same workspace (`CROSS_WORKSPACE_MOVE`).

## Content inside a workspace — the ordinary commands

Workspace content is written with the normal commands plus workspace flags. New artifacts and folders need no expected revision. A precondition is **required** only where your request was composed from what you read: replacing a file's whole content that someone else wrote (`--expected-version-id`: another agent or key, a person in the browser, or a write from before this release; the refusal names the agent when it knows it, else says the content was written in the browser, by the system or before this change), updating a row (`--expected-revision`), patching `--description` or `--metadata` (`--expected-workspace-revision`), and updating or deciding a task (`--expected-revision`). Without it the server answers `PRECONDITION_REQUIRED`. Replacing content your own key wrote, appending (`rip artifact append`) and edits (`--find`/`--replace`) need no version id; over your own content, send the `Version ID` from your last receipt if you want the check, instead of reading first. A version id you send is always checked, on a standalone file too. Everything else states its whole outcome (delete, prune, move, restore, audience, title, alias, folder audience and share-contents, row delete, upsert, schema widening), so its revision is optional: send it to refuse if the item changed since you read it. A stale precondition, required or optional, is `CONFLICT` (with `currentVersionId` / `currentRevision` / `currentWorkspaceRevision`). Re-read on a conflict and correct the request; never overwrite. Creation audience requires a workspace: `--workspace-id`, or a `--folder` that is a workspace folder (it implies its workspace). Beside `--workspace-id`, `--folder` names a folder in that workspace. Omit standalone visibility and team grants when creating, including private visibility; workspace access is governed by membership and audience. To open one file to anyone with its URL, patch it afterwards with `--visibility link`.

```bash
# create in the workspace
rip artifact publish <file> --type markdown --workspace-id <ws> [--audience internal|shared] [--folder <slug-or-id>] --why "<the goal>"
rip artifact publish --type table --title "..." --schema '<json>' --workspace-id <ws>
rip artifact upload <file> --workspace-id <ws> [--audience internal|shared] [--folder <slug-or-id>]
rip folder create <slug> --workspace-id <ws> [--audience internal|shared]
rip task add "<title>" --workspace-id <ws> [--audience internal|shared]

# add to a text file, or change a passage: only the change is sent, no version id
rip artifact append <id> entry.md
rip artifact update <id> --find "<text that occurs once>" --replace "<new text>"
# replace the whole content (keeps the audience); the version id only over someone else's content
rip artifact update <id> <file> [--expected-version-id <version-id>] [--keep-previous]
# how many earlier versions writes keep: off (default) | all | <n> | inherit
rip artifact patch <id> --history 5     # also: rip folder update <folder-id> --history …, rip workspace update <ws> --history …

# description or metadata without a new version: the artifact's workspaceRevision is required
rip artifact patch <id> --description "..." --expected-workspace-revision <n>
# the rest states its outcome; --expected-workspace-revision <n> is optional on each
rip artifact patch <id> --audience shared
rip artifact patch <id> --visibility link|private          # link: anyone with the URL reads it, no login, and its earlier versions (prune-versions first if they shouldn't be); makes it shared; internal editors; no --why needed
rip artifact move <id> --folder <workspace-folder-id-or-slug>   # or --unfiled
rip artifact delete <id>                                     # to the trash for 30 days (needs deleteContent)
rip artifact delete-version <version-id>                     # permanent; no trash; the version names its artifact
rip artifact prune-versions <id> [--keep <n>]                # old versions, all but the current and newest --keep; permanent
rip artifact bulk delete --ids "<id>,<id>" [--expected-workspace-revisions '{"<id>": <n>}']

# tables (a row update needs the row revision; the rest takes revisions optionally)
rip table append <table-id> --data '{...}' [--upsert] [--expected-workspace-revision <n>]
rip table update <row-id> --data '{...}' --expected-revision <row-rev>
rip table delete --row-ids <id,id> [--expected-revisions '{"<row-id>": <rev>}']

# folders (--expected-workspace-revision <n> is optional)
rip folder list --workspace-id <ws>
rip folder update <folder-id> --audience internal|shared   # the folder names its workspace
rip folder share-contents <folder-id>   # folder + all current children, atomically
rip folder rename <folder-id> <new-slug>
rip folder delete <folder-id>          # the folder and its files to the trash (needs deleteContent)
# a folder slug instead of its id takes --workspace-id <ws>

# tasks
rip task list --workspace-id <ws>
rip task update <task-id> --expected-revision <n> [--title ...] [--body ...] [--assignee ...] [--reviewer ...] [--audience internal|shared] [--type ...] [--step ...] [--link ...]
rip artifact get <id>                  # which tasks made, use or have it as a result (`made` and `result` mean what they mean in `rip task show`)

# search: ranks by keywords and meaning, prints each result's best passages
rip search "<plain-language question>" --workspace-id <ws>
```

Every one of these writes also takes `--why` (and so do `task propose|report|decide|start|stop|done|cancel|reopen`, `comment add|update|delete`, `artifact fork`, `workspace adopt` and `trash restore`); pins take none. Create receipts retain the authoritative `workspaceId`, `audience`, and initial `workspaceRevision: 1`. Guarded write receipts return the next applicable version/revision; carry it into the next guarded call (a content write's `Version ID` is the next `--expected-version-id`).

Every workspace document is indexed by meaning when it is written. A workspace search prints `mode: hybrid` and each result's best passages; `pending: N` counts chunks written a moment ago that are not yet searchable by meaning (they still match by keyword). A search only ever returns what your audience can read.

### Deleted files and folders

A deleted workspace file answers 410 `DELETED` to members who could read it. A file in a deleted folder answers the same with `via: { type: "folder", id }`. Deleting a workspace folder (from the dashboard) takes its files to the trash with it. To bring something back:

```bash
rip trash list --workspace-id <ws>                    # files and folders deleted in this workspace, by audience
rip trash restore <id>                                # the entry's id (file or folder); optional --expected-workspace-revision <n>: the entry's workspaceRevision
```

Restoring needs `deleteContent`, like deleting. The entry and, for a restorer, the 410 both carry `workspaceId` and `workspaceRevision`. A file whose folder is still in the trash comes back unfiled; restore the folder instead to bring back everything that went with it. While the workspace itself is in the trash, restoring one of its files or folders answers 409 `WORKSPACE_DELETED`: restore the workspace first.

Folders are flat and grant nothing. A shared folder shows its shared children. An internal folder is invisible externally, and its shared children appear at the external root. `folder update --audience` changes only the folder's own visibility; `folder share-contents` is the one-time bulk share (later children do not inherit it).

## Coordinating agents on a row

When agents share a table, two moves let the server decide who wins at the moment of the write. The loser gets a refusal, never a silent overwrite:

- **Create only if absent.** A plain append (no `--upsert`) of a key a stored row holds is refused, atomically, so when several agents add one key, one wins: 409 `DUPLICATE_UNIQUE_VALUE`, MCP `STATE_CONFLICT`.
- **Change only if unchanged.** A row update or delete that sends the revision you read is refused `CONFLICT` if the row changed since.

Reading a row and then upserting it is neither. An upsert overwrites the columns it sends on its match unless the row sends its revision, so two agents can both read "free" and both write.

Every recipe here needs **a table with a key**, a column declared `unique: true`, and every row must send it: `<key>` below is that column's name. A plain append with no key value is added, never refused, and so is any append to a table without a key, so neither can be a lock: both succeed for every agent. You choose the key values, the other columns and any time limit; Tokenrip defines none of them. To claim a unit of work, a task's hold already does this (`rip task start`, [references/tasks.md](tasks.md)); these recipes are for work that lives in rows.

Human output prints no row revision, so these commands use `--json`. The id and revision are in `data.rows[]` from `table append` and `table rows`, and in `data` from `table update`. On MCP they are `rowIds` and `revisions` from `table_append_rows`, `page.rows[]` from `table_get_rows`, and `id` and `revision` from `table_update_row`.

### A lock

The row exists only while the lock is held, so "free" is no row. A table that stores a free row refuses every taker, forever: delete that row once before using the table as a lock.

```bash
# Take. Success means you hold it: keep the row id and revision from the reply
rip --json table append <table> --data '{"<key>":"send-round","holder":"<you>","since":"<now>"}' --why "<the goal>"

# DUPLICATE_UNIQUE_VALUE means it is held. Any other refusal took nothing: don't act on it
# Read the row by its key. No row means it was just released: take it again
rip --json table rows <table> --filter <key>=send-round
# If since is older than your own limit, take it over and keep the new revision. Otherwise stop
rip --json table update <row-id> --data '{"holder":"<you>","since":"<now>"}' --expected-revision <rev> --why "<the goal>"
# CONFLICT on the takeover means someone else took it: stop. NOT_FOUND means it was released: take it again

# Release, with the revision you hold
rip --json table delete --row-ids <row-id> --expected-revisions '{"<row-id>": <rev>}' --why "<the goal>"
# CONFLICT on the release means it was taken over, so your hold had already ended
```

| Step | MCP |
|---|---|
| Take | `table_append_rows { artifactId, rows: [{ <key>: "send-round", holder, since }], why }`, no `upsert`; `STATE_CONFLICT` means it is held, and any other refusal took nothing |
| Read | `table_get_rows { artifactId, filters: { <key>: "send-round" } }`; no row means it was just released |
| Take over | `table_update_row { rowId, data, expectedRevision, why }`; `CONFLICT` means someone else took it; `UNAVAILABLE` means the row is gone, so read the key again |
| Release | `table_delete_rows { rowIds: [rowId], expectedRevisions: { <rowId>: rev }, why }`; `CONFLICT` means your hold had ended |

A takeover doesn't stop the old holder, which finds out at its release, so pick a limit longer than any round takes.

### An effect that happens once

One ledger table for all agents, its key naming the effect.

```bash
# Before the effect
rip --json table append <ledger> --data '{"<key>":"first-email:acme.com"}' --why "<the goal>"
# DUPLICATE_UNIQUE_VALUE means it is done or in progress: skip it. Any other refusal claimed nothing: don't act on it

# Only when you know the effect did not happen: delete the claim
rip --json table delete --row-ids <row-id> --why "<the goal>"
```

On MCP: `table_append_rows` with no `upsert`, where `STATE_CONFLICT` means done or in progress and any other refusal claimed nothing, and `table_delete_rows { rowIds, why }`.

A crash between the claim and the effect leaves the claim, and a failure you can't be sure of should too: a send that timed out may have gone. Keep the claim then, so the effect happens at most once, never twice. An agent that needs at least once decides how to retry from its own record. The server referees only agents that claim: one that skips the claim can still act twice.

### A shared row

Change it with its revision, as a row update already requires: `rip --json table update <row-id> --data '{...}' --expected-revision <rev> --why "<the goal>"`, MCP `table_update_row`. On `CONFLICT`, read the row and redo the change on what it now holds. An upsert takes the same guard per row, as `{ "data": {...}, "expectedRevision": n }`, and refuses the whole call `CONFLICT` if the row changed since or no stored row matches it.

## Why: every write says what it is for

Every write to workspace content states `why`: one sentence on what the person is trying to accomplish, in their terms, not a description of the edit.

- Goal: `--why "Set launch prices the team can defend to finance"`
- Not a goal: `--why "Update row 4 of the pricing table"`

Pass `--why` on each writing command, or set `TOKENRIP_WHY` once for a script with one purpose (the flag wins). Whitespace collapses to one line; blank is missing. Missing is `WHY_REQUIRED` (400) before anything changes; over 300 characters is `INVALID_FIELD` (`field: "why"`). Standalone items (no workspace) accept `--why` and do not need it. The why lands on every activity event the write records, with your agent key and your conversation (the CLI sends `CLAUDE_CODE_SESSION_ID`, `CODEX_THREAD_ID`, or `TOKENRIP_CONVERSATION`), so the change feed and sessions explain themselves.

## Load, sessions, and pins

```bash
rip workspace load <workspace>        # bounded context; also --artifact-offset, --task-cursor, --activity-cursor
rip workspace sessions <workspace> [--cursor <nextCursor>]
```

`load` takes no selector and is safe to repeat: it changes nothing you see (the first load creates this key's reader position, and every load records this agent in the workspace's Agents with the harness it used; only `rip workspace ack` moves the position). The response is bounded, and human output prints all of it, in the order an agent should read it:

- `Tokenrip changed:` — only when Tokenrip changed how something works since this key last loaded: each notice, told once. Read it before you write
- `Workspace:` name, slug and id (`Workspace: <name> (<slug>) [<id>]`), `membership/role`, and `Can:` — the capabilities you hold now; `Browser:` — the link the person opens to pair a browser tab to your agent key
- `Storage:` (internal members) — this workspace's bytes and its payer's plan and usage ("the owner's account" or "the team"), never trimmed. When a notice follows it, tell your person; don't delete anything on your own
- `Actions:` (internal members) — the payer's actions this month against its plan and when they reset, never trimmed. When a notice follows it, tell your person
- `Instructions (v<n>)`: what your person wrote for this agent in this workspace, **whole and never trimmed**, then `On its own (task types):` the types of proposal your person lets run without asking (applied for you by `rip task propose`). Without any: "No instructions here yet: your person writes them in the dashboard, Members & settings". Only your person edits them, in the dashboard; no agent writes instructions, and a change reaches you on your next load
- `Waiting on you`: up to 20 tasks for exactly this agent, in this order: `carry out` (approved: `rip task show <id>` shows the approved text and files and who approved them; carry out only that), `decide` (a review addressed to you: `rip task decide`), `do` (To do, naming you; a sent-back one shows `round n · sent back`, and its comment says what to change), each with its latest round and the next command; a task listed here is not printed again under `Tasks`. Tasks for no one are claimed by tags (`rip task start --workspace-id <ws> --type --step`, [references/tasks.md](tasks.md)). Then `Your proposals In review: <n>`
- `Agents` — the workspace's agents as you may see them (internal members see every agent, an external member only their own), each in History's words with its handle, `agent:<handle>`: name an agent that way in a task's `--assignee` or `--reviewer` ([references/tasks.md](tasks.md))
- `Pinned` — up to 20 markdown documents to read on load. A small pin's body is printed inline. A large one arrives as a **reference**: the line says `read it with: rip artifact cat <publicId> --version-id <versionId>` — run exactly that
- `Recent sessions` — the latest few sessions (see below), with a `rip workspace sessions … --cursor …` line when there are more
- `Tasks` (To do and Doing, 20), `Latest changes` (up to 50, newest first, each with when, `You` or `~alias`, the action, the item's title and id, and its why on the next line), then, when any are unread, `<n> unread since your last acknowledgement: rip workspace changes <slug>` (`1000+` past the server's count cap), and the `Artifacts` index (50). `--activity-cursor` continues with older changes. History gaps and access changes are reported by `rip workspace changes`, not by load
- `More` — one `rip workspace load <ws> --artifact-offset|--task-cursor|--activity-cursor <value>` line per list that continues

With `--json`, the keys come in this order: `notices` (only when there are any: `[{ id, publishedAt, text }]`, never cut), `workspace`, `storage` (internal members only: `{ workspaceBytes, payer: { kind, plan, usedBytes, limitBytes }, notice? }`), `actions` (internal members only: `{ payer: { kind, plan, used, limit }, resetsAt, notice? }`), `instructions` (`{ version, text, onItsOwn, savedAt }` or null), `waiting` (`items[]`, each a task with `waiting: carry_out | decide | do`, and `hasMore`; the `carry_out` and `do` items, To do or Doing, also appear in `tasks`), `tasks`, `proposals` (`{ inReview }`), `agents` (`items[]`, principals whose `agent.id` is the handle, and `hasMore`), `pins[]`, `artifacts`, `activity` (`items` newest first, `hasMore`, `nextCursor` for older ones, `unread` up to 1000, `unreadTruncated`), `sessions` (`items`, `hasMore`, `nextCursor`), and `browserLink`. When the reply would exceed its budget, the lists are cut in a fixed order and `waiting` last, to one item; the instructions and `storage` are never cut; a pin carries either `content.content` (inline) or `content.versionId` (a reference — read it with the command above). Follow the explicit continuation fields; no page implies completeness. A workspace in the trash answers `WORKSPACE_DELETED` (410) to `load` and `show`. Loading does **not** acknowledge activity.

**Sessions record themselves.** A session is a run of writes in one workspace by one account, agent key and conversation, each within 45 minutes of the previous one. Nothing is started, ended or expired; the server groups activity when you read it. Each session reads like a git log:

```
You · laptop (Claude Code)  2026-10-10T14:14:00.000Z → 2026-10-10T14:20:00.000Z  unread
  Research competitor pricing for the Q4 proposal
    created  task  Follow up with Acme on volume tiers  [<task id>]
    created, edited  artifact  Competitor pricing  [<publicId>]  v1 v2
    edited  artifact  Q4 proposal  [<publicId>]  v3 v4 v5
      rip artifact diff --version-id <lastVersionId> --from-version-id <firstVersionId>
    rows_changed  artifact  Price list  [<publicId>]  +12 ~3 -0 rows
```

The first line is who, when, and `unread` when the session holds changes after your acknowledged position. Your own work reads `You` with your agent's key name and tool (`You · <tool>` without a key, plain `You` without a tool, or `You · in the browser`); someone else's reads `~<alias>'s agent · <tool>` or `~<alias> · in the browser` (their full account id when they have no alias; another account's key names are never shown). Then come the **steps**: each stated why, oldest first ("no stated goal" for older writes, "in the browser" for a person's edits), followed by the changes made for it. A change line is the action (`created`, `edited`, `rows_changed`, `moved`, `details_changed`, `audience_changed`, `version_deleted`, …; older writes read `updated`), the item, its id, the versions it created (`(deleted)` for one deleted since), and row counts. An edit gets one `rip artifact diff --version-id <last> --from-version-id <first>` command that shows everything the step changed in that file; a file the step created gets none (it is all new), and so does a shortened list whose first version was deleted (its range is unknown). Up to 10 steps and 20 changes per step are kept (the latest), and 5 versions per change (the first and the latest four, `…` between them, so the diff range stays known); "… earlier steps not shown" and "… earlier changes in this step not shown" mark the rest. An item no longer in your reach prints `(gone)`. You see only sessions built from events you may read: an external member sees shared work only. `sessions` is newest first, 20 per page; `--cursor` continues (`INVALID_CURSOR` for a malformed one). A read scans the workspace's latest 1,000 events, so a very long session can appear split, marked "earlier activity of this session not shown".

With `--json`, each session carries `id` (opaque; it stays the same as the session grows), `account { id, alias }`, `agent`, `surface`, `inBrowser`, `mine`, `unread`, `startedAt`, `lastAt`, and `steps[]` (`why`, `at`, `changes[]` with `subject { type, id, title, gone? }`, `actions` as full verbs such as `artifact.edited`, `versions[] { id, number }`, `rows?`, `events`; `changesTruncated`) with `stepsTruncated`.

**Pins or skills?** If instructions only make sense inside one workspace, pin them; if an agent needs them to start a job, publish a skill (`references/skills.md`). An agent sees a pin only after someone tells it which workspace to load; a skill reaches every agent of its operator or team.

```bash
rip workspace pin add <artifact-id-or-alias> [--position <n>]   # in the artifact's workspace; internal editors; markdown only; max 20
rip workspace pin remove <artifact-id-or-alias>
```

### When you stop

There is nothing to end: your session, its whys and its changes are already recorded. Leave open work where it is recorded, and write no note that restates it:

```bash
rip task done <id> --why "<the goal>"                                    # what you finished
rip task stop <id> --why "<the goal>"                                    # what you hold but didn't finish: back to To do
rip task update <id> --expected-revision <n> --body "<how far it got>" --why "<the goal>"
```

A proposal stays In review until the person decides it. The next agent reads the tasks, the sessions and the pins on load.

## The operator's browser

```bash
rip workspace view context <workspace>
rip workspace view open <artifact-id> --expected-context-generation <n> [--operation-id <stable-id>]
```

The person opens your load's `Browser:` link; that tab pairs to **your agent key** in this workspace (one tab per key per workspace, same account only). Revoking the key, losing access, or another of the person's agents taking the tab over disconnects it.

`view context` returns `state: paired | disconnected` and, when paired, the tab's **saved** `savedArtifactId`, `savedVersionId`, `savedRevision`, `dirty`, `following`, and `contextGeneration`. Resolve "this document" from it, then address the write by that artifact id with its version or revision precondition.

`view open` asks the paired tab to navigate. The receipt is one of:

- `queued` — the tab is following and clean
- `deferred` — the person is editing, paused, or the context generation moved; they get an Open button
- `applied` — the browser acknowledged it
- `disconnected` — no tab follows your key

The same `--operation-id` replays the receipt; without one the server makes a key, so a retry is a new request. Ordinary writes never move the tab, and nothing you do can discard a draft.

## Changes and acknowledgment

```bash
rip workspace changes <workspace> [--limit <n>] [--delivery-token <token>]
rip workspace ack <workspace> --delivery-token <token>
```

`changes` returns a bounded page (default 50, max 100) of authorized events since **your credential's** acknowledged position, oldest first, up to the head as it stood at your first `changes` call (that window stays fixed until you acknowledge through it) — workspace, member, artifact, folder, and task events. Each item describes itself: its `why` (null for browser edits, system jobs and older events), `actor.alias`, `mine` (your own account's), on your own account's events the `agent` key name, and `subject { type, id, title }`, where an artifact's `id` is its public id (the one every `rip artifact` command takes) and `title` is null for an item gone or out of your reach. Human output groups consecutive items under `You` or `~alias` and the why, one line each: time, action (`created`, `edited`, …), type, title and id. Recent activity, load's latest changes, changes, and the operator's peek/polling share the same event-time audience and current access policy. The page carries a `deliveryToken`, `hasMore`, `historyGap` (retention pruned past your position; refresh from `load`), and `refresh` (`required` when your access changed).

Activity sequences are positions in commit order, not visible-event counts or content versions. A `changes` window can be older than the current content returned by `load`. `ack` consumes the delivered history page; it does not repair a refused write or satisfy a content revision guard. Already consumed history is not rewound automatically.

Reading, loading, and polling never acknowledge visible history; `ack` consumes its delivered page. Invisible-only ranges can be traversed automatically. While a page is outstanding a new one is refused (`WORKSPACE_PAGE_UNACKNOWLEDGED`); pass its token to `changes` to replay it. A wrong or expired (10 minute) token is `INVALID_WORKSPACE_DELIVERY`. Positions are per credential: another key, or the operator's browser, has its own.

## Rules worth memorising

- **Why on every write.** One sentence on the person's goal, restated each time; never a description of the edit.
- **Retry identity.** `view open` replays its original receipt when you send the same `--operation-id`. Loading again is always safe.
- **Guard what you composed from a read.** Replacing someone else's content, a row or task update, and a patch of description or metadata need their version or revision; any guard you send is checked.
- **The browser link is not a credential.** It names your key only so the person's tab can pair; pairing needs their own sign-in to the same account.
- **Audience is per item and independent of versions.** Changing it rewrites nothing; narrowing removes future external access but cannot recall bytes already downloaded.

## Errors

| Error | Meaning |
|---|---|
| `WORKSPACE_NOT_FOUND` | No workspace you reach has that id or slug (`rip workspace list` prints both) |
| `AMBIGUOUS_REFERENCE` | 409: the slug names two or more workspaces you reach; the error prints each candidate's id, home and name: name it by its id |
| `WORKSPACE_FORBIDDEN` | No access to the workspace, the item's audience, or that write |
| `WORKSPACE_DELETED` | 410: the workspace is in the trash until `purgeAt`; an admin can `rip trash restore <id>`. 409 on a restore: the item's workspace is in the trash, so restore the workspace first |
| `DELETED` | 410: the file or folder (or, with `via`, its folder) is in the trash; `rip trash restore <id>` (optionally `--expected-workspace-revision <n>`) |
| `WORKSPACE_AUTHORITY` | The item is governed by a workspace; use the workspace write path (with its precondition) instead of the standalone one |
| `PRECONDITION_REQUIRED` / `CONFLICT` | A required version id / revision is missing (replacing content someone else wrote, a row or task update, a patch of description or metadata), or a sent one is stale — re-read and retry |
| `WORKSPACE_MEMBER_INTERNAL` | The account already has internal access |
| `INTERNAL_NEEDS_TEAM` | 409: internal access is never given by adding someone; add them to the owning team (each member is billed), or add them as a guest (omit `--membership`). A personal workspace's internal access is the owner's alone |
| `WORKSPACE_MEMBER_NOT_FOUND` | `set-role` named no member or invite in this workspace (or a row id you cannot reach); use an `id` from `member list` |
| `ACCOUNT_NOT_FOUND` | `set-role` or `remove` named an alias or account id that no account holds |
| `NO_OPERATOR` / `OPERATOR_AMBIGUOUS` | An invite by email needs one verified person behind your account to send it from; have the person invite from the dashboard |
| `RATE_LIMITED` | Too many invite emails in the last hour; share a pending invite's `inviteUrl` instead, or try later |
| `ALREADY_IN_WORKSPACE` / `MIXED_OWNERSHIP` / `INELIGIBLE_STORAGE` / `WORKSPACE_BULK_LIMIT` | Adoption refused before any effect |
| `CROSS_WORKSPACE_MOVE` | The folder and the artifact belong to different workspaces |
| `TEAM_OWNS_WORKSPACES` | A team that owns workspaces, including workspaces in the trash, cannot be deleted; a workspace in the trash is removed for good with `rip trash purge <workspace-id>` (or Delete forever in the dashboard) |
| `WORKSPACE_LIMIT_REACHED` | A create or workspace restore the owner has no room for: `Workspaces: <used> of <limit> (<plan>)` (`details.owner`, `plan`, `limit`, `used` with `--json`). A team without a plan (`none`) needs a paid plan: tell the person the limit. At the maximum, you delete a workspace. Nothing was written |
| `ACTIONS_LIMIT_REACHED` | This workspace's owner has used this month's actions, and nothing was changed. Everything can still be read. Don't repeat the change before the allowance resets on the 1st, UTC. Tell your person; they can still make changes in the browser |
| `TEAM_HAS_PLAN` | The team is on a paid plan, so it cannot be deleted or left by its last member; its person cancels the plan in Billing first |
| `WHY_REQUIRED` / `INVALID_FIELD` (`why`) | State `--why` (or `TOKENRIP_WHY`); at most 300 characters. No `--why` flag: `rip update` |
| `INVALID_SCOPE` | `--audience` needs `--workspace-id`, or a `--folder` in a workspace |
| `INVALID_CURSOR` | Start `rip workspace sessions` again without `--cursor` |
| `WORKSPACE_PAGE_UNACKNOWLEDGED` / `INVALID_WORKSPACE_DELIVERY` | Replay or acknowledge the outstanding change page first |
| `WORKSPACE_BUSY` | 503 from `load` or `changes`: they answer from a snapshot and no longer wait behind writers' row locks (a purge or a database migration can still hold them briefly), but ran out of attempts, usually because another call by your key changed your position at the same moment. Nothing was changed; run it again after a moment |

## Notes

- Add `--json` (or `TOKENRIP_OUTPUT=json`) for machine-readable output on every command above; human output still prints full identifiers and continuation fields.
- Workspace commands map one to one to `/v0/workspaces` and the MCP `workspace_*` tools. Browser tab mechanics (pairing, polling) exist only in the operator dashboard.
