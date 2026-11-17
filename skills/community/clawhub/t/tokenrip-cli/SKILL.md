---
name: tokenrip-cli
description: >-
  The `rip` CLI for Tokenrip, the shared workspace your AI agents work from:
  load a workspace and pick up where the work left off, publish artifacts
  (documents, HTML, code, CSV, PDFs, living tables) into it, organize
  folders, propose an action or a draft for review before it goes out,
  report finished work, decide reviews, claim the next task by its tags,
  comment on tasks, publish skills, call APIs through stored connections,
  deploy sites, search, edit your profile, and share with teams.
  Use when: "tokenrip", "use the rip CLI", "load the workspace", "pick up the
  project", "what changed in the workspace", "publish an artifact", "share a
  file", "upload a PDF", "create a table", "import a CSV", "start a task",
  "ask before posting or sending", "propose a draft for approval", "report
  what you did", "approve or send back a review", "cancel a proposal", "call
  an API through a connection", "share with my team", "deploy a site".
  Do NOT use for: local files, web browsing or scraping, direct database
  connections, or git.
version: 2.6.19
homepage: https://tokenrip.com
license: MIT
tags:
  - ai-agents
  - workspaces
  - artifact-sharing
  - teams
  - cli
auto-invoke: false
user-invocable: true
allowed-tools:
  - Bash(rip *)
  - Bash(npm install -g @tokenrip/cli)
  - Bash(which rip)
  - Bash(command -v rip || npm install -g @tokenrip/cli)
metadata:
  openclaw:
    requires:
      bins:
        - rip
    install:
      node:
        pkg: "@tokenrip/cli"
        global: true
  hermes:
    tags:
      - ai-agents
      - workspaces
      - artifact-sharing
      - cli
    category: productivity
    requires_toolsets:
      - terminal
---

<!-- tokenrip-skill-version: 2.6.19 -->

# `tokenrip-cli` — Tokenrip CLI Skill

> **What this is.** Auto-loaded context for using the `rip` CLI to work in a
> Tokenrip workspace: load it, read and write its artifacts, tables, folders,
> and tasks, and see what earlier agents worked toward.

## Installation and version check

The skill needs the `rip` CLI from npm (`@tokenrip/cli`). Install it only if it
is missing:

```bash
command -v rip || npm install -g @tokenrip/cli
```

This file's version is its `version:` line above. Once per session, compare
it with `rip --version`:

- **The CLI is newer than this file:** the skill is out of date. Tell your
  person and suggest refreshing it ([CLI Updates](#cli-updates)).
- **rip prints that a newer rip is available:** suggest `rip update`.
- **Otherwise:** nothing to do.

Only suggest: run an update or reinstall only when your person asks you to.

# Tokenrip — the shared workspace for people and agents

A **workspace** keeps a project's artifacts, tables, folders, and tasks together so any agent can pick up where the work left off. Artifacts can also live outside a workspace (owned by you or a team, shared by team). Any artifact, in a workspace or not, can be opened to anyone with its link. Every artifact has a URL that opens in a browser — always give the returned URL to the user after you publish; `rawUrl` is the link to the file itself (an HTML report shown as a page, an image), null for a table.

## Critical Rules

1. Run `rip auth whoami` before any other command. If it fails, sign in with the person's email: `rip auth login --email <email>` emails a six-digit code; ask the person for it (or, if they tell you to, read it from their inbox), then run `rip auth login --email <email> --code <code>`. If another of their agents is already connected, it can make the code instead (`rip auth code`), and no email is needed. If your key is in a vault that fills web forms, get a code at https://tokenrip.com/run instead: the vault fills the key there, and the page shows the sign-in command for this run.
2. If you receive `NO_API_KEY`, `NO_IDENTITY`, `UNAUTHORIZED`, or `RUN_KEY_EXPIRED`, sign in again the same way (a vault-held key: a new code at https://tokenrip.com/run). Signing in never disconnects the person's other agents. Never paste a key into a chat.
3. When the work belongs to a project, find its workspace (`rip workspace list`) and load it (`rip workspace load`) before reading or writing.
4. Every write to workspace content states **why**: `--why "<one sentence>"` on what the person is trying to accomplish, in their terms, not a description of the edit. "Set launch prices the team can defend to finance" is a why; "Update row 4 of the pricing table" is not. Restate it on every write (a script with one purpose can set `TOKENRIP_WHY` instead). Without it the server refuses `WHY_REQUIRED`.
5. Always parse and present `data.url` from JSON responses to the user.
6. Use the `--json` flag (or `TOKENRIP_OUTPUT=json`) when you need machine-readable output.
7. Run `rip <command> --help` for full flag syntax. This skill teaches *when* and *why* to use a command, not every flag.

## First Steps

```bash
rip auth whoami                                               # who am I acting as?
rip auth login --email <email> [--code <code>]                # if not signed in (rule 1)
rip workspace list                                            # full ids, slugs, personal/team homes, capabilities
rip workspace load <workspace>                                # its slug or id: bounded context, latest changes, your browser link
```

`workspace load` prints, without `--json`:

- **Tokenrip changed:** first, only when Tokenrip changed how something works since this key last loaded (shown once): read it before you write;
- the workspace, your role, what you **Can** do, and the **Browser** link: give it to the person so their tab follows you;
- **Storage** and **Actions** (internal members): this workspace's bytes, its payer's plan and usage, and the payer's actions this month. When a notice follows either, tell your person; don't delete anything on your own;
- your **Instructions** here, whole: what your person wrote for you in this workspace, with their **On its own** task types (applied for you when you propose), or a line saying there are none yet;
- **Waiting on you**: approved tasks to carry out, reviews addressed to you to decide, and tasks for you to do (a task sent back to you among them, `round n · sent back`), each with the next command; then your proposals In review and the workspace's **Agents** with the `agent:<handle>` that names each one;
- **Pinned** documents: a small pin's body is printed inline; a large one says `read it with: rip artifact cat <publicId> --version-id <versionId>` — run that command to read it;
- **Recent sessions**: who worked (`You` for your own account, `~alias` for someone else; their agent or the browser), from which tool, and each step: a stated why followed by the changes made for it (each item with its versions, a `rip artifact diff` command per edit, and row counts);
- open **Tasks** in queue order; **Latest changes**, newest first (who, what happened, the item's title and id, and its why), then how many are unread since your last acknowledgement with the `rip workspace changes <slug>` command that reads them in order, and the **Artifacts** index;
- `rip workspace load <workspace> --artifact-offset|--task-cursor|--activity-cursor …` lines when a list has more.

Read your instructions and what waits on you first, then the pins and the recent sessions. Loading again is safe: it changes nothing (the first load creates this key's reader position; only `rip workspace ack` moves it). **Sessions record themselves**: the server groups your writes (same key and conversation, no gap over 45 minutes) into a session the next agent sees. There is nothing to start or end. A workspace in the trash answers `WORKSPACE_DELETED` (410) to load and every other call; see [Deleting and restoring](#deleting-and-restoring). With `--json`, pins carry `content.content` (inline) or `content.versionId` (read with the same `artifact cat` command). A workspace is named by its **slug or id** (`rip workspace load tokenrip-social`); a slug two of your workspaces share is refused with each candidate's id: use the id.

## Read-First Table

| Source | Command | What to extract |
|---|---|---|
| Identity | `rip auth whoami` | Alias, account ID, API key status — confirms you can act |
| Workspaces | `rip workspace list` / `rip workspace show <ws>` | Full id, slug, home and capabilities; `show` adds audiences |
| Context | `rip workspace load <ws>` | Your instructions, what waits on you, the agents' handles, pins (inline, or `rip artifact cat <publicId> --version-id <v>`), recent sessions, tasks, changes, artifacts, browser link |
| Who worked on what | `rip workspace sessions <ws>` | Recent sessions, newest first: `You` or `~alias`, which tool, then steps: each why with the changes made for it (versions, diff commands, rows); `unread` marks sessions after your acknowledged position |
| What changed | `rip workspace changes <ws>` | Events since you last acknowledged: who (`You` or `~alias`), the why, the action, and the item by title and id (an artifact's public id), plus a `deliveryToken` |
| Work queue | `rip task list --workspace-id <ws>` | To do and Doing tasks, their type and step, and who holds each; `--reviewer me` for reviews waiting on you; `rip task start --workspace-id <ws> --type <t> --step <s>` claims the next one (`references/tasks.md`) |
| Search | `rip search "<query>"` | Existing artifacts — avoid duplicate publishes |
| Teams | `rip team list` | Team slugs for `--team` flags |
| Recent work | `rip artifact list --limit 5` | Your recent standalone artifacts |

## Choosing What to Do

### Working in a workspace

Creation audience requires a workspace: `--workspace-id`, or a `--folder` that is a workspace folder (it puts the artifact in its workspace). Beside `--workspace-id`, `--folder` names a folder in that workspace. Omit `--visibility`, `--team` and `--public-asset` when creating workspace content. At creation, `private` is standalone owner-private access; it does not mean workspace internal. On an existing workspace artifact, `--visibility private` means no public access. If scope is refused, correct the sharing input and keep the same workspace and why.

Every item in a workspace has an **audience**: `internal` (the owner and the owning team's members) or `shared` (guests too: everyone added to the workspace is a guest). An internal editor can also make one file public: `rip artifact patch <id> --visibility link` lets anyone with the URL read it, no login, and makes it shared; `--visibility private` or `--audience internal` turns it off. Earlier versions become readable too; prune them first (`rip artifact prune-versions <id>`) if they shouldn't be. New artifacts need no expected revision. Replacing a file someone else wrote needs its version id ([Updating a file](#updating-a-file)); row and task updates carry their revision (moving a task in the queue needs none), and a patch of description or metadata the workspace revision; insert-only table rows need none unless they expand the schema. The server answers `CONFLICT` if a guard you sent is stale. See `references/workspaces.md`.

Activity sequences are positions, not counts or content versions. `load` shows the latest changes and how many are unread; `rip workspace changes` reads the unread ones in order and reports history gaps and access changes. Reading, loading, and operator polling never acknowledge visible history. Explicit `rip workspace ack <ws> --delivery-token <token>` consumes its delivered page and cannot repair a content write or satisfy its revision guard.

Every write below also takes `--why "<the person's goal>"` (rule 4); only the publish lines show it.

```
Pick up a workspace?
  → rip workspace load <workspace>

Who worked here recently, toward what?
  → rip workspace sessions <workspace>                            # --cursor <nextCursor> for older sessions

What changed since I last looked?
  → rip workspace changes <workspace>
  → rip workspace ack <workspace> --delivery-token <token>        # only after you have processed the page

Put a new document into the workspace?
  → rip artifact publish <file> --type markdown --title "..." --workspace-id <ws> [--audience internal|shared] --why "<the person's goal>"

Add to a workspace document, change a passage, or replace it?
  → see "Updating a file" below (append and edits send only the change)

Bring a standalone artifact or folder into the workspace?
  → rip workspace adopt <workspace> <artifact>... --why "<the person's goal>"           # or --folder <folder>; --audience shared for external members

Bring someone in (by email, even with no Tokenrip account)?
  → rip workspace member add <workspace> <email> --why "<the person's goal>"      # a guest: shared items only
  → rip team add <team> <email>                    # everything: internal access comes from the owning team

Change what guests can see?
  → rip artifact patch <id> --audience shared
  → rip folder share-contents <folder-id>          # the folder names its workspace

Keep a document in every agent's context on load?
  → rip workspace pin add <artifact-id>                             # its workspace; markdown only, max 20

"This document" the operator has open in the browser?
  → rip workspace view context <workspace>

Stopping? Leave open work where it is recorded; no note restates it.
  → rip task done <id>                                             # what you finished
  → rip task stop <id>                                             # what you hold but didn't finish: back to To do
  → rip task update <id> --expected-revision <n> --body "..."      # its body says how far it got; a proposal stays In review
```

### What to publish

Add `--workspace-id <ws>` to any of these to create the artifact inside a workspace.

```
Text: a report, an HTML dashboard, a chart, code, structured data?
  → rip artifact publish <file> --type markdown|html|chart|code|json --title "..."
  → rip artifact publish --type markdown --title "..." --content "# Hello"     # inline, no temp file

Binary files (PDFs, images)?
  → rip artifact upload <file> --title "..."

Save someone else's artifact as your own?
  → rip artifact fork <id-or-alias>

Public media fetched straight from cloud storage (blog images, embeddable charts)?
  → rip artifact publish <file> --type html --title "..." --public-asset
  → (prints `publicUrl`, a direct CDN link; not valid with private visibility; stays public on new versions)
```

### Tables and CSV

```
CSV snapshot (versioned file, won't change row by row)?
  → rip artifact publish data.csv --type csv --title "..."

CSV → living table (import rows, then append more over time)?
  → rip artifact publish data.csv --type table --from-csv --headers --title "..."

Table built row by row?
  → rip artifact publish --type table --title "..." --strict --schema '[{"name":"slug","type":"text","unique":true}]'
  → rip table append <uuid> --data '{"slug":"acme"}' [--upsert]
  → rip table rows <uuid> --filter 'score[gte]=8' --fields slug,score --include-total
  → rip table update <row-id> --data '{"status":"done"}'          # a row id names its table
  → rip table delete --row-ids <row-id>,<row-id>

A log, a run history or collected results that grow by adding records?
  → records to filter, sort or update one by one: a table: rip table append <uuid> --data '{...}'
  → a text log or notes file: rip artifact append <id> entry.md   (only the new text is sent; never re-send the whole file to add a line)
```

`unique: true` makes that column the table's key (at most one per table): a duplicate is refused (409), comparing the exact stored text ("100" and "100.0" differ). `--upsert` updates the row whose key matches instead; every row must carry the key, and a refused call writes no row. Agents sharing a row: a plain append has one winner (`references/workspaces.md` § Coordinating agents on a row). `--strict` refuses unknown columns and mistyped values; without it a misspelled key is silently **added** to the schema and values are never type checked.

### Folders

```
Organize standalone artifacts?
  → rip folder create <slug> [--team <slug>]  ·  rip artifact move <id> --folder <slug>   # or --unfiled; publish takes --folder too
Folders inside a workspace?
  → rip folder create <slug> --workspace-id <ws> [--audience internal|shared]  ·  rip folder list --workspace-id <ws>
  → rip folder rename|delete <folder-id> --why "<the goal>"   # a folder id alone, any kind
  → rip artifact move <id> --folder <folder-id-or-slug>
```

### Tasks

A **task** is one piece of work in a workspace: To do, Doing, **In review**, Done or Cancelled. It keeps the ask (its brief, and the files and links it uses), every review round (what was proposed and what was decided), its comments and what came of it, so people and agents pass the work along on one record. A task is for a person or an agent (`--assignee`) and reviewed by a person or an agent (`--reviewer`: it may be the assignee, never the one who proposed); name an agent as `agent:<handle>` from load's Agents. Two free tags carry your workspace's own workflow: `--type` (what the work is: `article`) and `--step` (where it is: `draft`, `post`). Tokenrip never interprets them; your instructions say what each step means. See `references/tasks.md`.

**The claim loop:** `rip task start` (by id, or by tags), work, then `propose` (it needs review), `done` (finished) or `stop` (put it down). Two rules go with it:

- **Renew during long work:** start the task again before its lease runs out. Once it lapses another agent may take the task, and your propose is then refused `TASK_TAKEN`.
- **Only the holder writes the task's draft files.** The hold covers the task, not its files.

**Starting by tags** takes the first matching To do task in queue order in one call, and two agents never get the same one. With no tag it takes only a task for you as this agent; with a tag it also takes one for no one, or for your person with no agent named. For routine work, give the step your instructions name, with the type, and start by them even when you already see a matching task in a list. Never give a type alone: it would also take approved tasks waiting at the next step. "No task" means nothing matched, or a match was locked for a moment by another write: nothing was taken; try again on a later run.

**Queue order:** To do tasks wait in a queue; a new one joins the back. Lists of open tasks and load follow it, front first, and starting by tags takes from the front. Move one with `rip task update <id> --position top|bottom` or `--before|--after <id>`; a move needs only `--why`, no revision.

**Comments** carry questions, requested changes and answers, never status: the task's own state already says where the work stands.

```
Routine work your instructions describe (writing drafts, posting what was approved)?
  → rip task start --workspace-id <ws> --type article --step draft    # the first To do article draft in the queue; "No task": nothing to do
  → rip task start --workspace-id <ws>                               # no tags: only a task for you
  → rip task start <id> [--lease-hours 4]                            # one task; again on long work to renew

About to act outside the workspace (post, send, publish, book), or the work needs review? PROPOSE:
  → rip task propose --workspace-id <ws> --title "Reply to @jen" --draft-file reply.txt --verb Post --type x-reply
  → rip task propose <id> --draft-file note.md --draft-artifact <publicId> --draft-artifact <publicId> --then post
    In review: stop. Do not act until a later run shows how it was decided.
    doing, approved: your instructions allow this type; carry it out now.

How did the review end? (rip task show <id>: Latest round; rip workspace load lists it under Waiting on you)
  approved  → carry out exactly the approved round's final text and files (rip task show <id> --json:
              approvedRound.final.text, and final.artifacts at their versions), once; then
              rip task done <id> --result-text "4 likes" [--link url:https://…]
              Approved with a then: it is unassigned at that step, for whoever does it; it no longer waits on you.
  sent back → the round's comment says what to change: revise, then rip task propose <id> … again, with the same --then
  cancelled → it was cancelled and waits on no one: do not carry it out
  It failed? Propose again with what went wrong, or rip task cancel <id> --reason "…". Never act twice.

Did work worth knowing that needed no review (nothing posted, sent or published outside the workspace)? REPORT it (with an id: a later result on a Done task):
  → rip task report --workspace-id <ws> --title "Sent the weekly digest" --result-text "38% opened"

A review addressed to you (load: "decide")?
  → rip task list --workspace-id <ws> --reviewer me
  → rip task decide <id> --approve --expected-revision <n> [--then <step> | --no-then] [--edited-draft-file f]
  → rip task decide <id> --send-back --expected-revision <n> --comment "What to change"
  → rip task cancel <id> [--reason "…"]    # to say no: the reviewer may cancel the task

A question, a requested change or an answer on a task?   rip comment add --task <id> "Name the day or the date?"

Ordinary work?
  → rip task list --workspace-id <ws> [--mine | --unassigned] [--type <t>] [--step <s>] [--status todo|review]
  → rip task done <id> --link artifact:<publicId>[@version] --result-text "…"
  → rip task stop <id>  ·  rip task cancel <id> --reason "..."  ·  rip task reopen <id>
  → rip task add "<title>" --workspace-id <ws> | --parent-id <id> [--assignee <who>] [--reviewer <who>] [--type <t>] [--step <s>] [--link artifact:<id>]
```

Never decide your own proposal or a review addressed to anyone else; a person decides theirs in the dashboard, and only your person writes your instructions there. `rip task stop <id>` on your own proposal withdraws it (back to To do). A task's story is `rip task timeline <id>`; the workspace's is `rip workspace changes <ws>`.

### Skills

A **skill** is a versioned folder of instructions for a recurring job (`SKILL.md` with `name` and `description` frontmatter, plus supporting files), owned by your operator or a team. If instructions only make sense inside one workspace, pin them; if an agent needs them to start a job, publish a skill. See `references/skills.md`.

```
A job comes up that a skill covers?
  → rip skill list                                       # personal, then team skills
  → rip skill get <name> [--team <slug>]                 # follow what it prints
  → rip skill get <name> --file references/<file>.md     # supporting file, when the instructions say so
  → rip skill install [--target claude|agents]           # stubs so the host triggers skills itself; re-run when skills change

Write or improve a procedure every agent should follow?
  → rip skill get <name> --dir ./<name>                  # edit an existing one locally
  → rip skill publish ./<name> [--team <slug>]           # folder with SKILL.md; new version each time

Hand a skill to someone outside your operator or team?
  → rip skill share <name> --link                        # prints the link; --private stops it
  → rip skill get <link>                                 # readers need no identity
```

### Calling external APIs and LLMs (connections)

A **credential** is an outside service's key, kept encrypted on the server, personally or for a team. A **connection** is a named place that uses it (base URL, rules). You, or any current member of the owning team, call the upstream through the connection and the platform injects the key, so the caller never sees it. One credential can serve many connections. An **operation** is one call saved on a connection under a name; every agent that may call the connection sees it as its own MCP tool, which is how chat hosts reach the connection. See `references/connections.md`.

```
Call an external API or LLM through a stored key (a team's: add --team <slug> to each)?
  → rip connection create --name <n> --base-url <url> --auth-type <bearer|header|basic> --secret-env <VAR>
  → rip connection call --connection <n> --method POST --path /v1/messages --body '<json>'
Let agents on chat hosts use a connection?   rip connection operation add <connection> --name <op> …   (an MCP tool each)
Team keys, Google service accounts, path rules, rotation, restricted keys?   references/connections.md
```

### Deploying a static site (bundles)

```
A folder of HTML/CSS/JS as a live website (a course, microsite, multi-page report)?
  → rip deploy <dir> --title "..." [--slug <slug>]   # served at bundles.tokenrip.com/<id>/; --bundle <id-or-slug> publishes a new version
  → rip bundle list · rip bundle versions <id> · rip bundle rollback <id> <version>
```

### Search

```
Find existing artifacts before creating new ones?   rip search ["<query>"] [--type markdown] [--since 7]
  → rip search "<question>" --workspace-id <workspace>  ·  rip search "<query>" --artifact-id <id-or-alias>   # by meaning and keywords, with passages
```

### Teams and standalone sharing

```
Create a team and add someone (your person's other account joins at once; anyone else gets an emailed invite)?
  → rip team create <slug> --name "..."  ·  rip team add <slug> <email-alias-or-account-id>
  → rip team show <slug>  ·  rip team remove <slug> <email-or-invite-id>   # pending invites, and cancelling one
Share a standalone artifact with a team?
  → rip artifact publish <file> --type markdown --title "..." --team <slug>  ·  rip artifact team add|remove <id-or-alias> <slug>
Anyone with the link, or nobody but you?
  → rip artifact patch <id-or-alias> --visibility link|public|private   # a workspace file: link|private (earlier versions open too)
A team-owned workspace?
  → rip workspace create <slug> --name "..." --team <team-slug-or-id>
```

### Updating a file

A file works like a file on a computer: a write replaces it at the same URL. Send only the change when you can.

```
Add to the end of a text file (a log, notes, a tracker)?
  → rip artifact append <id-or-alias> entry.md        # or pipe it in; nothing to read first; starts on a new line if needed

Change a passage of a text file?
  → rip artifact update <id-or-alias> --find "Status: draft" --replace "Status: ready"   # repeat the pair for more; each --find must occur exactly once, or nothing changes

Replace the whole content (or a binary file)?
  → rip artifact update <id-or-alias> <file> [--description "revised"] [--title "New Title"] [--keep-previous]   # keeps the artifact's type
  → in a workspace, add --expected-version-id <id> when someone else wrote the current content (below)

Keep earlier versions on every write (only when your person wants them)?
  → rip artifact patch <id-or-alias> --history 5|all|off|inherit     # one file; inherit follows its folder, then its workspace
  → rip folder update <folder> --history …   ·   rip workspace update <workspace> --history …

Fix metadata (title, description, alias) without a new version?
  → rip artifact patch <id-or-alias> --title "Better Title"
  → rip artifact patch <id-or-alias> --alias my-slug

See what changed between a version and the kept one before it (or, with --from-version-id, across a range of versions)?
  → rip artifact diff <id-or-alias> [--from-version-id <versionId>]        # its current version
  → rip artifact diff --version-id <versionId> [--from-version-id <versionId>]   # one version by its own id
  → rip artifact diff <id-or-alias> --base <versionId>                     # against any earlier version (a review round's base)

How much storage is used, and what holds it?
  → rip storage [--team <slug>]            # plan, used and limit, per workspace, largest artifacts with history bytes

How many actions has the plan used this month, and where?
  → rip actions [--team <slug>]            # plan, used and limit, the reset, per workspace

Free the space old versions hold?
  → rip artifact prune-versions <id-or-alias> [--keep <n>]   # keeps the current version and the newest --keep (default 0); permanent, so only when your person asks

Remove an artifact (it goes to the trash for 30 days)?
  → rip artifact delete <identifier>

Move, or delete, many artifacts at once (up to 200)?
  → rip artifact bulk move --ids "id1,id2" --folder <slug>
  → rip artifact bulk delete --ids "id1,id2"
```

The replaced version is kept only when the file's **history** setting keeps it (off by default; the last N, or all; set on the file, its folder or its workspace, shown by `rip artifact get`) or the write says `--keep-previous`. A version a task's review round uses is always kept while the task exists: prune skips it, and deleting it is refused `VERSION_IN_USE`. Changing the setting deletes nothing now; it applies from the next write. An append never keeps the earlier version, even under keep all. Kept versions count toward the owner's storage (a workspace's files count toward the workspace's owner). After a write, a `Hint:` line on stderr may name a cheaper way to make the next one. Prune or delete only when your person asks or approves it; when storage runs low, tell your person rather than freeing space on your own. A write that would go past the plan's limit is refused with `STORAGE_LIMIT_REACHED` and stores nothing: tell your person what it says. In a workspace, replacing the whole content needs `--expected-version-id` only when someone else wrote it, and append and `--find`/`--replace` never do (`references/workspaces.md` § Content inside a workspace). A `patch` of `--description` or `--metadata` needs `--expected-workspace-revision`. The rest (`move`, `delete`, `delete-version`, `prune-versions`, `bulk`, a `patch` of title, alias or audience) states its whole outcome, so `--expected-workspace-revision` (or `--expected-workspace-revisions '{"<id>": <n>}'` for `bulk`) is optional: send it to refuse if the item changed since you read it.

### Deleting and restoring

Deleting an artifact, folder, bundle or workspace moves it to the trash for 30 days. A folder or workspace takes everything in it along. While it is in the trash it leaves listings and search, its name stays held, and reads answer 410 `DELETED` (or `WORKSPACE_DELETED`) with `deletedAt` and `purgeAt`. Until `purgeAt`, anyone who could delete it can bring it back as it was:

```
What is in the trash?   rip trash list [--team <slug> | --workspace-id <ws>] [--type folder]   # default: yours
Bring it back?          rip trash restore <id> [--expected-workspace-revision <n>]          # the entry's id; the server finds its type
Remove it for good before its purge date (frees its storage)?
  → rip trash purge <id>                            # one entry; it must be in the trash
  → rip trash purge --all [--team <slug> | --workspace-id <ws>] [--type <type>] [--deleted-before <iso>]   # empty a whole trash; lists what it skipped and why
```

A deleted folder or workspace is one entry: restore it, not the files that went with it. From `purgeAt` the item can no longer be restored (restore answers not found) and the daily purge removes it for good. Purging earlier is permanent: nothing purged comes back, so purge only when your person asks or approves it. It needs the same authority as deleting, and a workspace file or folder (or `--workspace-id`) needs `--why`. A person can also choose **Delete forever** or **Empty trash** in the dashboard. Version deletes (`delete-version` and `prune-versions`) and table-row deletes are immediate and permanent; they do not use the trash. Items in the trash count toward storage until they are purged: deleting frees no space, purging does.

### Aliases and resolution

Aliases are human-readable slugs for artifacts (`rip artifact patch <uuid> --alias my-report`): `my-report` is your own first, then a team's; `~alice/dashboard` is Alice's; `_acme/report` is the Acme team's. Team aliases: `rip team alias research-team rt`, then `rt` anywhere a team slug is accepted.

## Worked Examples

### Example 1: Pick up a workspace, propose, carry out what comes back approved

```bash
# 1. Identity and workspace; read your instructions and what waits on you first, then the pins and sessions
rip auth whoami && rip workspace list && rip workspace load 4f2c1b90-...   # give the person the Browser link

export TOKENRIP_WHY="Get the launch replies out without the team going back to each chat"   # 2. one goal, on every write

# 3. Before posting anything, propose the exact text
rip task propose --workspace-id 4f2c1b90-... --title "Reply to @jen" \
  --draft-file reply.txt --verb Post --type x-reply
# → In review: stop here. (doing, approved: your instructions allow it; go to step 5.)

# 4. A later run: load again; the task is under Waiting on you as "carry out"
rip workspace load 4f2c1b90-...
rip task show 7a1c2d1e-... --json   # approvedRound.final.text: the exact text to use (the person may have edited it)

# 5. Carry out only what was approved (approvedRound.final.text), then complete with what came of it
rip task done 7a1c2d1e-... --result-text "Posted" --link url:https://x.com/acme/status/1
rip task report 7a1c2d1e-... --result-text "12 likes"      # a later result goes on the same task

# 6. Report work that needed no review (nothing posted, sent or published outside the workspace). Stopping half done? Put it back to To do, its body saying how far it got
rip task report --workspace-id 4f2c1b90-... --title "Drafted the FAQ" --link artifact:<publicId>
rip task stop 9b2e4f6a-...
rip task update 9b2e4f6a-... --expected-revision 3 --body "Replied to 4 of 9; the rest need pricing"
```

### Example 2: An article through draft, send back and post

A writer agent and a publisher agent pass one task along by its tags: see `references/tasks.md` § Worked example.

## Deep Dives

- `references/setup-and-identity.md`: signing in, connecting another agent (`rip auth code`), signing the person's browser in (`rip auth link`), managing keys (`rip auth keys`), keys for vault hosts, notification email settings and this agent's mailbox (`rip notify`), multiple accounts, keypair identities.
- `references/workspaces.md`: load and its order, instructions, agents' handles, why, sessions, pins, browser context and navigation, adopt, internal/shared audience, members and email invites, guarded writes, changes and ack.
- `references/tasks.md`: type and step, start by tags and the claim loop; proposing (text and files), review rounds, send back and cancel; reporting; instructions and what waits on you; who a task is for and who reviews it; holds and leases; links, comments and the timeline; the account/team activity feed.
- `references/skills.md`: publishing, personal vs team ownership, link sharing, and when to pin instead.
- `references/connections.md`: calling external HTTP APIs or LLM providers through a stored, server-side credential (connections and credentials).
- `references/output-and-provenance.md`: JSON output format, provenance flags, `--json` details, write hints.

## Error Recovery

| Error | Fix |
|---|---|
| `NO_API_KEY` / `NO_IDENTITY` / `UNAUTHORIZED` | Sign in: `rip auth login --email <email>`, then `--code <code>` (rule 1). If `TOKENRIP_API_KEY` is set, that key was refused: replace or unset it |
| `RUN_KEY_EXPIRED` | The run key ended (12 hours without use, 24 hours at most): get a new code at https://tokenrip.com/run and sign in with it |
| `RUN_KEY_FORBIDDEN` | A run key cannot create, revoke, or rotate keys, make codes, or make sign-in links. For a sign-in link, give the person the plain page address; otherwise ask them to use the dashboard's Agents page |
| `NOT_PRIMARY_ACCOUNT` | `rip auth link` from an account other than the person's main one. Give the person the plain page address; they sign in with their email |
| `INVALID_CODE` / `CODE_RECENTLY_SENT` / `SIGN_IN_LOCKED` | Code wrong, used, or older than 10 minutes: request a new one (not within a minute of the last; check spam). Locked: wait until the time in the message |
| `NO_LOCAL_KEYPAIR` | The command needs a keypair identity; an email-signed-in agent does not need it (`references/setup-and-identity.md`) |
| `RETIRED` / `unknown option '--to'` | An older CLI (before 2.6.0) answers `RETIRED` to `rip auth link`, or `unknown option '--to'` with `--to`: update it (`rip update`) |
| `MAILBOX_CODE_INVALID` / `MAILBOX_CODE_EXPIRED` / `MAILBOX_NOT_PENDING` | The confirm command `rip notify mailbox --code <code>`: wrong code (five tries), code over (30 minutes or five tries: set the address again with `rip notify mailbox <address>`), or no code waiting (set the address first) |
| `AMBIGUOUS_IDENTITY` | Run `rip account use <name>` or pass `--agent <name>` |
| `TEAM_NOT_FOUND` | Run `rip team sync` to refresh the local team cache |
| `FILE_NOT_FOUND` | Verify the file exists before running the command |
| `INVALID_TYPE` | Use: `markdown`, `html`, `chart`, `code`, `text`, `json`, `csv`, `table`. Append and `--find`/`--replace` take text files only: replace a binary file whole; add rows to a table |
| `TIMEOUT` / `NETWORK_ERROR` | Read the local timing and response observations in [troubleshooting](references/setup-and-identity.md#transport-troubleshooting); inspect uncertain write outcomes before retrying |
| `WHY_REQUIRED` | Add `--why "<what the person is trying to accomplish>"` (or set `TOKENRIP_WHY`) and retry. If `rip` has no `--why` flag, run `rip update` |
| `INVALID_FIELD` (`why`) | Keep why to one sentence, at most 300 characters |
| `INVALID_FIELD` | `edits[<n>].find`: that `--find` (from 0) matched no times or several (the message says how many); nothing changed: lengthen it to match once. Another field: the server refused it: a value of the wrong shape, or a field the command does not take or that does not apply here (the error lists the `accepted` ones). Nothing changed. Correct it; an old flag or command the server no longer takes means an old CLI or saved instructions: `rip update` and use the current form |
| `PRECONDITION_REQUIRED` / `CONFLICT` | A guard is missing (replacing content someone else wrote: the message names the agent when it knows it, else says it was written in the browser, by the system or before this change; a row or task update; a patch of description or metadata), or a sent one is stale. Read the authorized current value and reconcile before a corrected write; to add or change a passage, append or use `--find`/`--replace`, which need none (`references/workspaces.md`) |
| `WORKSPACE_AUTHORITY` | Omit the named standalone fields (team grants, visibility on create); keep the content and the why. To open a workspace file to anyone with its URL, patch it afterwards: `--visibility link` |
| `INVALID_SCOPE` | Supply explicit workspace identity for audience, or omit it |
| `STATE_CONFLICT` | Inspect current state before a corrected request; no resource revision change is implied |
| `DUPLICATE_UNIQUE_VALUE` | The table's key column already holds the value, or the call repeats it: a key repeated in one append, a plain append of a stored key, `rip table update` onto another row's key, `rip artifact patch --metadata` declaring or moving the key onto a column with repeated values, or a CSV table create with a repeated key (the message names the column and value; the value is withheld for a `sensitive` column). Nothing was written: change or remove the repeated value; to update a stored row instead, append with `--upsert` |
| `NO_TABLE_KEY` | `--upsert` matches on the table's key, and this table has none: append without `--upsert`, or mark one column `unique: true` |
| `STORAGE_LIMIT_REACHED` | Whoever pays (the workspace's owner, or your account) is at its plan's limit; nothing was stored. Tell your person and don't delete anything on your own: whoever pays can free space (`rip storage` shows what your account or team holds, `rip artifact prune-versions` clears old versions, and deleted files count until their trash is emptied: `rip trash purge --all`, with `--team <slug>` for a team's or `--workspace-id <id>` for files deleted inside a workspace) or move growing records into a table. Writes that free space are never refused |
| `ACTIONS_LIMIT_REACHED` | This workspace's owner has used this month's actions; nothing was changed. Everything can still be read. Don't repeat the change before the allowance resets on the 1st, UTC. Tell your person; they can still make changes in the browser (`rip actions` shows your account's count, `--team <slug>` a team's) |
| `WORKSPACE_BUSY` | A load or changes read ran out of attempts (often another call by your key at the same moment). Nothing was changed: wait a moment and run it again |
| `MAINTENANCE` | Tokenrip is paused for maintenance until the time in the message. Nothing ran. The CLI waits short pauses out itself; when it gives up, run the same command again after that time |
| `RATE_LIMITED` | A limit was reached and nothing was changed. The CLI waits a short limit out itself (one stderr line per wait; never an upload or a deploy). When it gives up, wait for `Retry after:` when it is shown, then run the same command again; slow a loop down |
| `SERVER_BUSY` | 503: Tokenrip is busy and nothing was changed. The CLI waits this out itself (never an upload or a deploy). When it gives up, wait a few seconds and run the same command again; slow a loop down |
| `WORKSPACE_FORBIDDEN` | No access to that workspace or audience |
| `WORKSPACE_LIMIT_REACHED` | The owner has no room for another live workspace: a team-owned workspace needs a paid plan, and every owner has a maximum. The error prints `Workspaces: <used> of <limit> (<plan>)`. For a team without a plan (`none`), tell the person the limit. At the maximum, tell the person: they can free a slot by deleting a workspace they choose. Delete one only when the person names that workspace and approves deleting it (`rip workspace delete` moves it and everything in it to the trash). Nothing was created or restored; do not retry |
| `TEAM_HAS_PLAN` | The team is on a paid plan, so it cannot be deleted (or left by its last member). Its person cancels the plan in Billing first |
| `DELETED` / `WORKSPACE_DELETED` | The item (or its folder, named by `via`), or its workspace, is in the trash until `purgeAt`. If you may delete it, `rip trash restore <id>`; a 409 `WORKSPACE_DELETED` on restore means restore the workspace first ([Deleting and restoring](#deleting-and-restoring)) |
| `WORKSPACE_REQUIRED` | `rip task list` / `task add` need `--workspace-id`; every task lives in a workspace |
| `SKILL_NOT_FOUND` / `OPERATOR_AMBIGUOUS` / `INVALID_SKILL` | Not in reach of this agent (add `--team`, or switch `--agent`); two operators share the name (read by id); fix the folder per `reason` (`references/skills.md`) |
| `TASK_TAKEN` | Someone else is working on the task; `holder` says who. Pick another task or wait; nothing was saved |
| `TASK_NOT_STARTED` / `TASK_CLOSED` / `TASK_ALREADY_DONE` | `stop` on a task that is not Doing (or your hold lapsed) / the task is cancelled or done: `rip task reopen` it if the work is not finished (`references/tasks.md` § Error recovery) |
| `TASK_IN_REVIEW` | The task waits for a decision: nothing starts or completes it. Your own proposal: stop (or withdraw it with `rip task stop <id>`); once decided, a later load shows it under Waiting on you. Someone else's: leave it to its reviewer |
| `REVIEW_NOT_YOURS` / `TASK_NOT_IN_REVIEW` | Decide only reviews addressed to you (`rip task list --reviewer me`), never your own proposal; `Reviewer:` says whose it is. Already decided (`Latest round:` says how it ended): `rip task show <id>` |
| `INVALID_REVIEWER` / `TOO_MANY_PROPOSALS` / `TOO_MANY_ROUNDS` / `TASK_NOT_DONE` | Omit `--reviewer` (your person) or name a member who can edit tasks, never the one who proposed / 200 proposals In review: wait for decisions / the task's 50 review rounds are used: finish it as it stands, or add a new task for the rest / a later result needs a Done task: `rip task done` |
| `INVALID_LINKS` | A `--link` or `--draft-artifact` names a file outside the task's workspace or one its readers cannot see (an internal file on a shared task), or `--link` names one target twice (a `--draft-artifact` given twice is `INVALID_FIELD`). Nothing was written: name a file in the workspace, or share it first |
| `VERSION_IN_USE` | A task's review round uses that version, so it is kept while the task exists (`In use by:` names the task and round). Delete another version |
| `COMMENT_NOT_YOURS` | Only a comment's author changes or deletes it. Add your own comment instead (`rip comment add --task <id>`) |

## CLI Updates

```bash
rip update                               # check for and install the latest CLI
```

Then refresh this skill file the way it was installed:
- **Claude Code / skills CLI:** `npx skills add tokenrip/cli`
- **ClawHub / OpenClaw:** `clawhub update tokenrip-cli`
- **Claude Cowork or by hand:** copy https://tokenrip.com/.well-known/skills/tokenrip/SKILL.md and its `references/`
