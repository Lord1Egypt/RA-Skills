# Tasks & Activity

Return to [SKILL.md](../SKILL.md) for the command routing table.

A **task** is one piece of work in a workspace. It keeps the ask (its brief, and the files and links it uses), every review round (each draft proposed and how it was decided), its comments, the action and what came of it, so people and agents pass the work along on one record and anyone can read back what happened. The **activity** feed records what happened in a team or your own scope. After `rip workspace load`, read your instructions and what waits on you first.

---

## Tasks

### The protocol

1. **Load the workspace first; it opens with your instructions.** `rip workspace load` opens with what your person wrote for you here: which work is yours (often a `--type` and `--step` to claim), and the types that run on their own when you propose.
2. **Claim, work, then move it on.** `rip task start` (by id, or the next one by tags), do the work, then `rip task propose` (it needs review), `rip task done` (finished) or `rip task stop` (put it down). Renew a long hold by starting again; only the holder writes the task's draft files.
3. **Before acting outside the workspace** (post, send, publish, book), **propose** it: the exact draft (text, and the files it is made of), the approve verb, a type, a `--then` when someone else does the next step, and a reviewer if it is not your own person and the task names none.
4. The reply is **In review** (stop: a later run reads the decision), or **approved** at once when your instructions let that type run on its own.
5. **Read the decision on the latest round.** Approved: carry out exactly the approved round's final text and files, once, then complete with the result. Sent back: its comment says what to change; revise and propose again on the same task. Cancelled: the task was cancelled; do not carry it out. If carrying it out fails, propose again with what went wrong, or cancel with the reason.
6. **Report** work worth knowing that needed no review (nothing posted, sent or published outside the workspace); a later result goes on the same task.
7. **Comment** for questions, requested changes and answers, never for status: the task's state already says where the work stands.
8. Every run, **what's waiting on you comes first**: approved tasks to carry out, reviews addressed to you, tasks for you (one sent back to you among them).

Every task lives in exactly one workspace, with an **audience** inside it (`internal` or `shared`). There are no personal or team tasks: `task list`, `task add` and a new `task propose` or `task report` need `--workspace-id`, and the server answers a missing one with `WORKSPACE_REQUIRED`. A task carries a `title`, an optional markdown brief (`--body`), two optional tags, its links, a producer-defined payload, and optionally a **parent** in the same workspace (set when the task is created, never changed).

| Status | The dashboard says | Meaning |
|---|---|---|
| `todo` | To do | Nobody is on it (an approved proposal waits here to be carried out; a sent-back one waits here to be revised) |
| `doing` | Doing · *who* | One holder is working on it |
| `review` | In review | A proposal waits for its reviewer's decision; nobody works on it |
| `done` | Done | Finished, with what came of it |
| `cancelled` | Cancelled | Will not be done (a proposal its reviewer said no to lands here); reopenable |

```bash
rip task list --workspace-id <ws>                        # To do and Doing tasks you can see
rip task list --workspace-id <ws> --type article --step draft    # by tags
rip task list --workspace-id <ws> --reviewer me          # reviews In review addressed to you
rip task list --workspace-id <ws> --mine                 # for you (your person, or you as an agent) or held by you
rip task list --workspace-id <ws> --unassigned           # for no one, held or not
rip task list --workspace-id <ws> --status review        # every proposal In review you can see
rip task list --parent-id <id>                           # a task's children, in its workspace
rip task list --workspace-id <ws> --status done,cancelled --order finished   # most recently finished first
rip task show <id>                                       # everything: who, the rounds, what to carry out, links, children, the newest timeline entries
```

Filters: `--status` (comma list of `todo,doing,review,done,cancelled`, or `all`; default `todo,doing`, or `review` with `--reviewer me` alone), `--order` (omitted: [queue order](#queue-order) when every status is open, else newest first; `created`, newest first; or `finished`, which needs `--status` of only `done` and/or `cancelled`), `--type`, `--step`, `--mine` or `--unassigned` (not both), `--reviewer me`, `--since`, `--limit` (max 200), `--cursor` (replay it with the same filters and order). Each row shows the task's type and step and its latest round (`round 2 · sent back`).

### Type and step

Two free tags carry your workspace's own workflow. **`type`** is what the work is (`article`, `x-reply`, `first-email`); **`step`** is where it is (`draft`, `post`, `send`). Each is lowercase letters, digits, `-` and `_`, starting with a letter or digit, at most 64 characters. Tokenrip never interprets them: your person's instructions say which steps exist and who does each, and agents coordinate by claiming and filtering on them.

- Set both with `rip task add --type --step` and `rip task update --type --step` (`--no-type` / `--no-step` clear one); setting the type records you as who gave it.
- `rip task propose` and `rip task report` take `--type`: on an existing task it fills a missing type, and another type is `INVALID_FIELD`.
- A proposal's **`--then <step>`** is the step an approval moves the task to. Approved with a then, the task is To do at that step and assigned to no one, for whoever does that step to claim. Without one it comes back to you to carry out. The reviewer may change or clear it when approving.

### Start: claim your next piece of work

```bash
rip task start <id>                                                  # one task by its id
rip task start <id> --lease-hours 4                                  # again on long work: renews your lease
rip task start --workspace-id <ws> --type article --step draft       # the first To do task in queue order matching the tags
rip task start --workspace-id <ws>                                   # no tags: the first To do task in queue order for this agent
```

- **By id**: a free task (To do, or an agent hold whose lease lapsed) becomes yours under a lease (default 2 hours, 0.25 to 72). Starting your own hold again renews it, never shorter. Someone else's live hold is `TASK_TAKEN`.
- **By tags** (`--workspace-id` instead of an id): one call finds the first To do task in queue order ([Queue order](#queue-order)) in your audiences that matches `--type` and `--step` and starts it for you; two agents starting at once never get the same task. With **no tag** it takes only a task for you as this agent (what load lists as waiting on you). With **a tag** it also takes one for no one, or for your person with no agent named. It never takes another agent's or another person's task, and never one In review, Doing, Done or Cancelled. It prints **No task** (exit 0) when none matches, or when a match is busy for a moment: nothing was taken; try again on your next run.
- **Give the step, or no tags; never a type alone.** A type alone also matches approved tasks waiting at the next step (`--type article` would take an article waiting at `post` as readily as one at `draft`).
- The answer is the task whole: its brief, its files and links, its latest round (a sent-back round's comment says what to change) and its approved round (what to carry out).

### Queue order

A workspace's tasks wait in a queue. A new task joins the back, so until anyone moves one the queue is creation order; a task keeps its place through start, stop, a send back and the rest.

- **What follows it:** `rip task list` when every status asked for is open (the default `todo,doing`, or `--status todo`), front of the queue first; the open tasks in `rip workspace load`; and starting by tags, which takes from the front. `--order created` lists newest first instead; a list with Done or Cancelled is newest first by default.
- **Moving a task:** `rip task update <id> --position top` (or `bottom`) puts it at the front (or back); `--before <id>` or `--after <id>` puts it beside another task in the workspace you can read. One of the three per call (two are `INVALID_ARGUMENT` before any request); naming the task itself, or one elsewhere, is `INVALID_FIELD`.
- **A move needs no revision.** Sent with only `--why`, it needs no `--expected-revision`, changes no revision and records no change. Sent beside other fields, `--expected-revision` covers those fields as usual.

```bash
rip task update <id> --position top --why "Ship the pricing post first"     # started next by tags
rip task update <id> --after <other-id> --why "Write it after the outline"
```

**Two rules go with a hold:**

- **Renew during long work.** Start the task again before its lease runs out. Once it lapses, another agent can take the task; your propose is then refused `TASK_TAKEN`, but you may already have overwritten a draft file.
- **Only the holder writes the task's draft files.** The hold covers the task, not its files: this is a convention, not enforced. Earlier versions survive only where history keeps them, and every version a review round uses is always kept.

### Who a task names

Every task names people and agents in four roles, as **principals**: `assignee` (who it is for; empty: anyone), `reviewer` (who decides its proposals; empty: any person who can edit tasks), `createdBy` and `completedBy`. A principal is a person (`{ account, agent: null }`) or one agent (`agent: { id, name, harness }`), with `mine` (on your account) and `isCaller` (exactly you). Human output uses History's words:

| Principal | Printed as |
|---|---|
| Your person | `You` |
| One of your person's agents | `You · Grok (Claude Code)` (its key name and harness) |
| You, the calling agent | `You · Grok (Claude Code) · this agent` |
| Another person | `~alek` (their account id when they have no alias) |
| Another person's agent | `~alek's agent · Codex` (their key names are never shown) |

To name a principal in `--assignee` or `--reviewer`, give a person's account id or alias (`alek`, `@alek`), or an agent as **`agent:<handle>`**. The handle is `agent.id`, which `rip workspace load` prints beside each agent under Agents and `rip task show` prints beside each agent principal. A bare uuid is never read as a handle. Key ids never appear.

- **Assignee.** A person: the task is for them, and any of their agents may pick it up. An agent: the task is that agent's. It is advisory, not a lock: anyone who can edit tasks may still start it by id. `--mine` (`assignee=me`) lists tasks for your account with no agent named, tasks assigned to you exactly, and tasks you hold; not a sibling agent's. `--unassigned` (`assignee=none`) lists tasks for no one, held or not.
- **Reviewer.** A person, an agent, or empty. It must be a current member who can edit tasks in the task's audience. It may be the assignee (your person reviewing what their own agent did for them), but never the one who proposed (`INVALID_REVIEWER`).
- **While In review** both can change: a new reviewer re-addresses the open review (never to its proposer), and a new assignee is whom a send back returns the task to.

```bash
rip task add "Write the launch article" --workspace-id <ws> --type article --step draft --reviewer alek --link artifact:<style-guide-id>
rip task add "Reply to each launch mention" --parent-id <id>     # under a task: its workspace is the parent's
rip task update <id> --expected-revision <n> --reviewer agent:<handle>     # title/body/assignee/reviewer/audience/type/step/links
rip task update <id> --position top                                         # move it in the queue: no revision ([Queue order](#queue-order))
```

### Propose: ask before it goes out

```bash
rip task propose --workspace-id <ws> --title "Reply to @jen" --draft-file reply.txt --verb Post --type x-reply
rip task propose --workspace-id <ws> --title "Email the investors" --draft-file email.md --verb Send --reviewer alek --link artifact:<publicId>
rip task propose <id> --draft-file article.md --draft-artifact <x-post-id> --draft-artifact <linkedin-id>@3 --then post
rip task propose <id> --draft "Thanks Jen, we ship Thursday!" --comment "Shorter, as you asked"     # a new draft for your own proposal
```

- **Each proposal is a review round.** It records the task's step, you as proposer, the verb, `--then`, an optional `--comment` for the reviewer (posted in the same write) and the draft. Rounds are kept: the task's timeline shows every one.
- **The draft is what the reviewer approves and you carry out**: text (`--draft` inline, or `--draft-file`, read verbatim; at most 64,000 characters) and up to 10 files (`--draft-artifact <publicId>[@version]`, repeatable, in order, each once; a version number or id, else the file's current version). Each draft file is linked to the task, and the round keeps the versions it names for as long as the task exists. `--verb` is the approve button's word (at most 24 characters; "Approve" without it). `--link artifact:<publicId>[@version]` or `url:<https://…>` adds a file or page the work uses (repeatable, up to 50). A new proposal also takes `--body` (context for the reviewer) and `--audience`; under a task, name it with `--parent-id` instead of `--workspace-id` (never both).
- **On an existing task** it works from To do or Doing when the task is free or held by you, and on your own proposal In review, whose round it replaces (that round closes `replaced`). Your hold is cleared; the assignment never changes, so a task you claimed by tags stays for no one. The title, parent and audience never change. Someone else's proposal is `TASK_IN_REVIEW`.
- **Who reviews it.** The task's reviewer when one is set (naming a different one is `INVALID_REVIEWER`), else your `--reviewer`, else your own person. Never you.
- **The reply.** Usually `status: review` (In review): stop. Do not act, and do not ask in the chat; the reviewer decides (a person in the dashboard). A re-proposal bumps the revision, so a decision made on the old draft is refused `CONFLICT`.
- **On its own.** When the proposal goes to your own person and its type is on your instructions' on-its-own list, it comes back approved at once (the round names the instructions version): without `--then`, `status: doing`, held by you, to carry out now; with `--then`, To do at that step for whoever does it. That holds only when your own account gave the task its type: your own new proposals, tasks your person (or another of their agents) wrote or tagged with that type, and types you set on a task that had none. A type someone else gave a task never approves it on its own.
- **Limits.** At most 50 rounds per task (`TOO_MANY_ROUNDS`), 200 of your proposals In review per workspace (`TOO_MANY_PROPOSALS`), 10 draft files per round; a task holds at most 100 children.
- **Withdraw** your own proposal with `rip task stop <id>`: the round closes `withdrawn` and the task goes back to To do, still for whoever it was for. `rip task cancel <id> --reason "…"` ends it instead: the round closes `cancelled` and the task is Cancelled. Its proposer, the proposer's person or whoever decides it may cancel it; anyone else gets `REVIEW_NOT_YOURS`.

### Read the decision

`rip task show <id>` prints the **Latest round** (its step, who proposed it, the draft, the outcome, who decided and the comment) and, once approved, what to carry out. The outcomes:

| Latest round | The task is | Next |
|---|---|---|
| in review | In review | Nothing: wait for the decision |
| `approved` | To do (or Doing, approved on its own), for you to carry out; with a then, To do at that step for whoever claims it | Carry out exactly the approved round's final material, then `rip task done` |
| `sent_back` | To do, still for whoever it was for, at the same step | Read the comment, revise, `rip task propose <id>` again (keep `--then`) |
| `cancelled` | Cancelled, with the canceller's reason | Nothing; do not carry it out |
| `withdrawn` | To do (stopped) | Its proposer withdrew it with `rip task stop`, or lost access to the task |
| `replaced` | (a later round followed) | Read the latest round |

A sent-back task waits on you under `do` when it is yours; one you claimed by tags (for no one) comes back to whoever next starts by those tags, with its latest round and the comment.

### Carry out what was approved

An approved task carries `approvedRound: { number, final: { text, artifacts } }`: its final material, part by part the reviewer's edit, else the draft. `rip task show <id>` prints the text under **Approved text (round n, carry out exactly this)** and the files under **Approved files (round n, these versions)** (on a Done task the label reads "carried out").

```bash
rip task show <id> --json        # data.approvedRound.final.text, and final.artifacts[].version.id
rip artifact cat <publicId> --version-id <versionId>      # a file exactly as approved
rip task done <id> --result-text "4 likes" --link url:https://x.com/acme/status/1
```

- What was approved is the final text, character for character (not your draft when the reviewer edited it, and not a rewording), and each file at the version named, not the file's latest. Take the text from `--json`: the human output indents each line and does not show trailing whitespace. Before acting, check you have not already done it (a retry after a timeout must not post twice).
- If it fails, propose again on the same task with what went wrong (`rip task propose <id> --draft …`), or cancel it with the reason.
- An approval is spent once used: reopening a Done task clears the approved round.

### Report: work that needed no review

```bash
rip task report --workspace-id <ws> --title "Sent the weekly digest" --result-text "38% opened" --link url:https://…
rip task report <id> --result-text "12 likes" --link url:https://…      # a later result on a Done task
```

A new report is a task born Done, created and completed by you, with no round. `--result-text` is what came of it (at most 280 characters); it also takes `--link` (result links), `--type`, `--body` and `--audience`, and `--parent-id` in place of `--workspace-id` for a report under a task. A later result goes only on a Done task (`TASK_NOT_DONE` otherwise), by any agent that can edit tasks there: `--result-text` replaces the text and `--link` adds links.

### Decide: reviews addressed to you

```bash
rip task list --workspace-id <ws> --reviewer me
rip task show <id>                                                   # the draft, the verb, then, the revision
rip task decide <id> --approve --expected-revision <n>
rip task decide <id> --approve --expected-revision <n> --edited-draft-file edited.txt --edit-artifact <publicId>@4
rip task decide <id> --approve --expected-revision <n> --then publish        # or --no-then: back to its proposer
rip task decide <id> --send-back --expected-revision <n> --comment "Name the day, not the date"
rip task cancel <id> --reason "Not this week"                       # to say no: cancel the task
```

- An agent decides only a review whose reviewer is exactly its key. A person's review, an unaddressed one (any other person decides those), another agent's, and your own proposal are `REVIEW_NOT_YOURS`, with `Reviewer:` saying whose it is; nothing is written. A person decides theirs in the dashboard, from their own sign-in.
- A review has two answers: exactly one of `--approve` and `--send-back`. `--comment` may go with either (posted in the same write) and is required with `--send-back`: it says what to change. `--approve` takes `--then <step>` (overrides the proposal's) or `--no-then` (clears it), `--edited-draft-file` (the text then carried out; kept only when it differs) and `--edit-artifact <publicId>@<version>` (a later version of a draft file, the one you saw and approve).
- `--send-back` makes the task To do with its assignment and step unchanged, so it goes back to whoever had it.
- To say no, cancel the task: `rip task cancel <id> --reason "…" --expected-revision <n>`. The reviewer may cancel a task In review; the round closes `cancelled`. `--expected-revision` (optional) is the revision you read: a draft replaced, decided or started since is `CONFLICT` and nothing is cancelled. `--decline` and `--reason` on decide are refused with a hint naming `rip task cancel`.
- An approval is refused `DELETED` while a draft file is in the trash or after it was purged, and `INVALID_LINKS` when a shared task's draft file is no longer shared: send it back or cancel it instead.
- `--expected-revision` is the revision you read. A draft replaced since is `CONFLICT` with `currentRevision`: read it again. A task already decided is `TASK_NOT_IN_REVIEW`, with `Latest round:` saying how it ended.
- Deciding a whole batch at once is dashboard-only; decide each child.

### Instructions and what waits on you

Your person writes **instructions** for you in each workspace, in the dashboard (Members & settings). No agent writes instructions, its own or another's, and there is no CLI command for them. `rip workspace load` prints them first, whole, as `Instructions (v<n>):` with their **On its own** task types, or "No instructions here yet: your person writes them in the dashboard, Members & settings". A change reaches you on your next load.

Then `Waiting on you (<n>):` lists, in this order, up to 20 tasks for exactly this agent, each with its reason and latest round:

| Reason | Means | Next |
|---|---|---|
| `carry out` | approved, for you (To do, or Doing in your hold) | `rip task show <id>` (the approved text and files, and who approved them), carry out only that, `rip task done <id> --result-text "…"` |
| `decide` | a review addressed to you | `rip task decide <id> --approve\|--send-back --expected-revision <n>`, or `rip task cancel <id>` to say no |
| `do` | To do, naming you (a sent-back one too: `round n · sent back`) | read it, then start it, or revise and propose it when its round was sent back |

Tasks for no one, or for your person with no agent named, never wait on you here: claim them by tags. With `--json` they are under `instructions` (`{ version, text, onItsOwn, savedAt }` or null), `waiting.items[]` (each task with `waiting: carry_out | decide | do`; the `carry_out` and `do` items, To do or Doing, also appear in `tasks`), `proposals.inReview` (your proposals In review) and `agents.items[]` (principals, each `agent.id` a handle). `task list --mine` and `--reviewer me` read the rest.

### The lifecycle

```
                 propose (new)
                     │
todo ──propose──> review ──approve──> todo (to carry out; or at its then step, for no one) ──start──> doing ──done──> done
 │  <──send back── review                                                                            │
 │  <──stop (withdraw)── review ──cancel──> cancelled                                                │
 │ <──stop / lease lapses── doing                                                                    │
 └──done (straight from To do) ───────────────────────────────────────────────────────────────────────┘
report (new) ──> done          todo / doing / review ──cancel──> cancelled
reopen: done and cancelled go back to todo; a proposal cancelled In review and still for its proposer goes back to review on a new round
```

```bash
rip task start <id> --lease-hours 4
rip task start <id>                              # again on long work: renews your lease
rip task stop <id>                               # back to To do (on your own proposal: withdraws it)
rip task done <id> --result-text "…" --link artifact:q3-memo@2 --link url:https://…
rip task cancel <id> --reason "duplicate"
rip task reopen <id>
```

Every write states `--why "<the person's goal>"` (or `TOKENRIP_WHY`), like any workspace write; without it the server refuses `WHY_REQUIRED`. An In review task refuses start and complete with `TASK_IN_REVIEW`. Reopening clears the approved round and any cancel reason; every round, the result text and the links stay.

**Old words are gone.** `rip task claim`, `touch`, `release` and `dismiss` are unknown commands, `--kind`, `--skip` and `--decline` are unknown options (use `--type`, and `rip task cancel` to say no; the server refuses `kind`, `skip` and `decline` the same way), and the old status words (`open`, `claimed`, `dismissed`) are refused: use `start` (it also renews your own hold), `stop` and `cancel`, and `todo`, `doing` and `cancelled`.

### Who holds a task

- **One holder per task, per key.** When an agent starts a task, the hold belongs to that agent's key, not just the account. Two agents of the same person cannot both hold one task: the second gets `TASK_TAKEN`.
- **An agent's hold has a lease**: 0.25 to 72 hours, default 2. A sweep runs every minute and returns a lapsed hold to To do, so work is never parked by a harness that vanished. Starting your own task again renews the lease, never shorter; advertise the `holder.leaseExpiresAt` that comes back, not the value you asked for.
- **The person's hold has no lease.** When the person starts a task in the dashboard, it stays theirs until they move it. Leave it alone unless they ask.
- **Races resolve at the database.** Two agents starting one task by id at once: one wins, the other gets `TASK_TAKEN` with `holder` saying who. Two starting by tags at once get two different tasks, or one gets none. Never check-then-start: call `start` and branch on the answer.
- A task whose agent lease has lapsed is **free**: anyone may start it (a takeover) or complete it.

### Who can do what

- **Visibility** follows the workspace: internal members see both audiences, external members only `shared`. No access: `WORKSPACE_FORBIDDEN`.
- **Writing** (add, propose, report, start, stop, done, cancel, reopen, update) needs task-write access for the task's audience. A workspace in the trash answers 410 `WORKSPACE_DELETED` to every task call until an admin restores it.
- **Commenting** needs only read access: anyone who can read the task, viewers included (an external member on shared tasks only).
- **Stop** is for the holder. The person may stop any of their own agents' holds, and a workspace admin may stop anyone's; everyone else gets `TASK_TAKEN`.
- Losing access (removed from the workspace or its owning team, downgraded, narrowed out of the audience) stops your holds, withdraws your open proposals, and clears the assignee and reviewer roles you can no longer fill.

### Files and links

A task has one list of **links**, each with a role: **context** (what the work uses: the brief's files, the draft files, a post to reply to) or **result** (what came of it). Each points at an artifact in the task's workspace (optionally at a version) or at a URL. `rip task show` prints the files under **Files** (see [A task's files](#a-tasks-files)) and the URLs under **Links**, each result marked `(result)`. A write's output (start, done, propose and the rest) prints the links under **Files & links** and **Result links**.

- Context links: `--link artifact:<publicId>[@version]` or `--link url:<https://…>` on `add`, `update` and `propose` (repeatable, up to 50 a call); `rip task update <id> --remove-link artifact:<publicId>` (or `url:…`) removes one. A proposal's draft files are linked as context too.
- Result links: `--link` on `done` and `report`; they are never removed.
- An artifact must live in the task's workspace, and on a shared task it must be shared (`INVALID_LINKS`); each target once per role, at most 100 per role per task. One in the trash is refused (410 `DELETED`) and left out of reads until restored; purging it removes its links.
- A version on a link is a pointer, not a keep: if that version is removed later, the link reads the file's current version. Only the versions a review round uses are kept.

### A task's files

`rip task show` (and `--json`'s `files`) lists every file the task links or names in a round, once, with how the task relates to it:

- **`made`**: a round of this task proposed the file as new (version 1, written by the round's proposer). A draft the task wrote.
- **`result`**: a result link of this task names it.
- **`otherTasks`**: how many other tasks you can read link it or name it in a round.
- **`onlyThisTask`**: no other task uses it, including tasks you cannot see.

A file is **made for this task** when it is `made` and `onlyThisTask`. Files in the trash are not listed.

**Tidying up.** When a task is cancelled, the files made for this task may be moved to the trash. After a task is completed, move them to the folder the workspace's instructions name for finished work; trash them only when the person or the instructions ask:

```bash
rip artifact bulk delete --ids "<id>,<id>"                     # to the trash, restorable for 30 days
rip artifact bulk move --ids "<id>,<id>" --folder <slug>       # into the workspace's folder for finished work
```

Never a file another task uses (`onlyThisTask` false), and never a result, even one the task made (`rip task show` reads `made for this task · result`).

### Completing

- `rip task done` completes a task that is **free** (To do, or a lapsed agent hold) or **yours**; you do not need to start it first. Someone else's live hold: `TASK_TAKEN`, and **nothing is saved**: keep your work locally and pick another task, or wait.
- `--result-text "<what came of it>"` (at most 280 characters; given again, it replaces the old text) and `--link artifact:<publicId>[@version]` or `--link url:<https://…>`, repeatable, up to 50: result links.
- Reopening keeps the result links. Status is the truth, not the links.

### Comments

```bash
rip comment add --task <id> "Should the post name the day or the date?"
rip comment add --task <id> --file answer.md
rip comment update <comment-id> "Should the post name the day?"     # your own comment; it reads as edited
rip comment delete <comment-id>                                     # your own; a deleted marker stays
```

A comment is markdown on a task (at most 8,000 characters): a question, a requested change or an answer. It is **never a status report**: the task's state, its rounds and the workspace's changes already say where the work stands and what you did. Anyone who can read the task may comment (viewers too; an external member only on shared tasks). Only the author changes or deletes a comment (the same agent; a person also over their own agents'), else `COMMENT_NOT_YOURS`. Propose and decide take `--comment` too, posted in the same write. Nobody is emailed about a comment; it lands in the task's timeline and the workspace's changes (`comment.created`, `comment.updated`, `comment.deleted`, which never carry the text). `rip task show` and `rip task timeline` print each comment with its id.

### A task's timeline

`rip task show <id>` prints the newest 30 timeline entries; `rip task timeline <id>` pages through all of them, newest first. Each entry is one of:

- a **round**: its number and step, the proposal (text cut to 512 bytes; `rip task show <id> --round <n>` prints a round whole) and how it was decided, by whom, with the comment;
- a **comment**, with edited and deleted markers;
- a **step** from the activity log: created, started, stopped, lease lapsed, completed, cancelled, reopened, result added, links changed, title, brief, tags or roles changed; each with who, when, from which harness, and the why.

`rip task show <id> --round <n>` prints each draft file with its version, whether the file changed since, and the command that diffs it against the same file in the previous round at the same step: `rip artifact diff --version-id <v> --base <baseVersionId>`.

Task events are also **workspace activity**: `task.created`, `task.updated`, `task.audience_changed`, `task.links_changed`, `task.proposed`, `task.approved`, `task.sent_back`, `task.withdrawn`, `task.started`, `task.stopped`, `task.lease_expired`, `task.completed`, `task.reported`, `task.result_added`, `task.cancelled`, `task.reopened` and the comment verbs arrive through `rip workspace changes <workspace>` (MCP `workspace_changes`) alongside the workspace's other changes. Older rows may still say `task.skipped` (an old skip, which cancelled the task), `task.claimed`, `task.released` or `task.dismissed`. No event carries a draft, a comment or a result's text. The account/team feed below never carries task events.

### Worked example: an article through draft, send back and post

Your person's instructions make one agent the writer (it takes `article` tasks at step `draft` and proposes them with `then: post`) and another the publisher (it takes them at step `post`).

```bash
export TOKENRIP_WHY="Get the launch article out on X and LinkedIn this week"

# Writer run: claim the next article draft
rip task start --workspace-id content --type article --step draft
# → Doing, held by you: its brief and Files & links (the style guide, the two post files)

# Write the posts into the task's files (you hold the task), then propose the article's text and both files
rip artifact update 3c9e7f10-... x-post.md
rip artifact update 8d2a4b61-... linkedin-post.md
rip task propose 7a1c2d1e-... --draft-file article.md --draft-artifact 3c9e7f10-... --draft-artifact 8d2a4b61-... --then post
# → In review: stop.

# A later writer run: the sent-back task comes back when it is the first matching To do task in
# queue order the writer may take (one ahead of it comes first; the sent-back task keeps its place)
rip task start --workspace-id content --type article --step draft
# → Latest round (1): sent back, with the comment "Cut the pricing paragraph; end with the waitlist link"
rip artifact update 8d2a4b61-... linkedin-post.md      # revised as the comment asks (and article.md)
rip task propose 7a1c2d1e-... --draft-file article.md --draft-artifact 3c9e7f10-... --draft-artifact 8d2a4b61-... --then post
# → round 2, In review. Approved, the task moves to step post, for no one in particular.

# Publisher run: claim what was approved, post exactly those versions, complete with the links
rip task start --workspace-id content --type article --step post
rip task show 7a1c2d1e-... --json        # approvedRound.final: the text, and each file at its approved version
rip artifact cat 3c9e7f10-... --version-id <versionId>
rip task done 7a1c2d1e-... --link url:https://x.com/acme/status/1 --link url:https://linkedin.com/posts/acme-1
```

---

## Activity

An append-only feed of what happened in a team or your own scope: team shares, connection changes, and member removals. Non-consuming — poll it freely.

```bash
rip activity --team quintel
rip activity --team quintel --type connection.created,team.member_removed --since 7
rip activity --actor alek
rip activity --subject <connection-id>
```

Every row carries a sentence rendered server-side, so `--json` and human output tell the same story:

```
alek created connection minimax 12m ago (claude-code)
sam removed alek from the team 2h ago
```

Verbs: `artifact.shared_to_team`, `connection.created`, `connection.disabled`, `credential.created`, `credential.rotated`, `team.member_removed` (older rows may read `connection.rotated`). `--subject <id>` narrows the feed to one subject: the id a row ends with (a connection's, a credential's), or an artifact's id or alias, with no type prefix. An artifact deleted forever has no id; its row keeps its title. Task history is not here; read it with `rip workspace changes <workspace>`.

---

## Attribution — which harness you are

Every task hold and activity row records the **harness** it came from, not just the account, and the agent key that acted. The CLI resolves the harness automatically: an explicit `TOKENRIP_SURFACE` wins, otherwise Claude Code names itself (`claude-code`), then Codex (`codex`), otherwise plain `cli`. It also sends the harness conversation id (`TOKENRIP_CONVERSATION`, else `CLAUDE_CODE_SESSION_ID`, else `CODEX_THREAD_ID`; stored only as a hash), so two conversations on one key form two sessions.

```bash
TOKENRIP_SURFACE=nightly-batch rip task start <id>
```

That value lands on the task's `holder.surface` and every activity row — so a feed can tell a task started in the dashboard from one started by a cron shell. Attribution is metadata and can never fail a call; only a missing `--why` on a write refuses.

---

## Error recovery

| Error | Fix |
|---|---|
| `WORKSPACE_REQUIRED` | `task list` / `task add` / a new `task propose` or `task report` need `--workspace-id`: every task lives in a workspace |
| `WORKSPACE_FORBIDDEN` | You have no access to the workspace or the task's audience, or no task-write access |
| `WORKSPACE_DELETED` | The workspace is in the trash; a workspace admin can `rip trash restore <id>` |
| `TASK_TAKEN` | Someone else is working on it. `holder` (printed as `Held by: …`) says who and until when: pick another task or wait. Nothing was saved. On a propose after your lease lapsed: the task is someone else's now |
| `TASK_IN_REVIEW` | The task waits for a decision: start and complete are refused. Your own proposal: stop; once decided, a later load shows it under Waiting on you (or withdraw it with `rip task stop <id>`). Someone else's (proposing on another's proposal is refused the same way): leave it to its reviewer |
| `TASK_NOT_IN_REVIEW` | Nothing to decide: `Latest round:` (`details.latestRound`) says how its latest round ended, `Status:` where the task is now. `rip task show <id>` |
| `REVIEW_NOT_YOURS` | Not addressed to you, or your own proposal: `Reviewer:` (`details.reviewer`; null is any person who can edit tasks) says who decides it. Decide only what `--reviewer me` lists; nothing was written |
| `INVALID_REVIEWER` | The reviewer must be a member who can edit tasks in the audience, never the one who proposed. When the task already names one (`details.reviewer`), omit `--reviewer` or name that one; if it names you, ask whoever set it to change it |
| `TOO_MANY_ROUNDS` | The task has had 50 review rounds, its most. Finish it as it stands, or add a new task for the rest |
| `TOO_MANY_PROPOSALS` | 200 of your proposals are In review in this workspace: wait for decisions, or withdraw some with `rip task stop`, before proposing more |
| `TASK_NOT_DONE` | A later result (`rip task report <id>`) goes on a Done task; finish this one with `rip task done <id> --result-text "…"` |
| `INVALID_LINKS` | A `--link` or `--draft-artifact` names a file outside the task's workspace, one its readers cannot see (internal on a shared task), a version of another file, or `--link` names the same target twice, or a task already has 100 links of that role (a `--draft-artifact` given twice is `INVALID_FIELD`). Nothing was written |
| `DELETED` | A file you link or propose is in the trash (restore it first), or, on an approval, a draft file is: send the proposal back or cancel it |
| `VERSION_IN_USE` | (`rip artifact delete-version`) A review round uses that version, so it is kept while the task exists; `In use by:` names the task and round |
| `COMMENT_NOT_YOURS` / `COMMENT_NOT_FOUND` | Only a comment's author changes or deletes it: add your own instead / the comment is deleted, or on a task you cannot read |
| `CONFLICT` | On `decide`: the draft changed since you read it (`currentRevision`). Read it again before deciding. On `update`: re-read and retry |
| `PRECONDITION_REQUIRED` | `decide` and `update` need `--expected-revision` (a move alone, `--position`/`--before`/`--after` with only `--why`, needs none) |
| `TASK_NOT_STARTED` | `stop` on a task that is not Doing (or your lease already lapsed). `rip task show <id>` |
| `TASK_CLOSED` | The task is cancelled (or, for `start`, done). Reopen it first if the work is still wanted |
| `TASK_ALREADY_DONE` / `TASK_NOT_CLOSED` | Already done (reopen first) / only done or cancelled tasks reopen. `rip task show <id>` |
| `INVALID_ASSIGNEE` | The `--assignee` is not a member who can edit tasks in the task's audience, or an `agent:<handle>` that is unknown here or revoked |
| `INVALID_FIELD` | A draft over 64,000 characters, a verb over 24, a result over 280, a type or step not matching the grammar, a type other than the task's, a draft file given twice or an 11th, an edit of a file not in the draft or not later than it, a round number the task does not have, or a parent outside the workspace (or with 100 children). `field` says which |
| `INVALID_CURSOR` | Cursors are opaque: re-run the query rather than editing the value |
| `INVALID_FIELD` on `--since` | `--since 0`, a negative, and a unix timestamp are all rejected. Use a positive number of days or an ISO-8601 timestamp |
