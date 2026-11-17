# memo — Projects: context, status, evidence, chat links and annotations

**Start work on a project with `memo projects context <key>`.** Its client is `memo organizations context
<organization>`, a deal on it `memo deals context deal:<id> --brief`. Its key documents come first:
read them before anything else. Mark one with
`memo projects key-documents add <key> <reference> --reason '<why>'`.
Then ask where it stands with `memo projects status <key>`, and read only the chats its `next` names.

To see where a project stands, use `memo projects status <project>` (over MCP, `memo_read` runs `projects status`).
It reads the stored messages of every chat linked to the project, in every account those links name, and lists the
accounts in `meta.accounts`. Per chat it says who wrote last, whose move it is, the open questions both ways,
promises, and amounts asked in messages with their direction (`asked` is a request found by words, not a debt:
it may be a price the owner quoted). Money owed comes from confirmed invoices and payments (`finance`); when a
project has them, amounts found by words are left out. Add `--context-query <words>` to see how long a topic has been quiet on
their side. An amount or promise marked `pattern` is a word match: read the cited message before you trust it. Read
with `--compact`, one line per row, to keep your context small. Then read only the chats in `next`, from the date it
gives, with the command it names (that command has `--compact` too). Do not read every chat, and do not copy
messages out with your own script. Never write message text to a file: quote it in your answer with its reference.
memo picks no messenger profile: when several are signed in to a chat's account, the command says `<profile>` and
`missing` names them; ask the owner which, and pass `--sync-profile max=<profile>`.

To collect what the store holds about a project, use `memo projects evidence <project> --source <accounts|all>`
(MCP `project_evidence`). The name, the key, each alias, `--alias`, `--context-query` and `--contact` is its own
search: every word of it must appear in one text, in any order, as whole words; hits are joined. Every message of a
chat confirmed as the project's is read too when `--source` holds its account: a `linked-chat` item names nothing, it
is there because the chat is the project's. One run takes only a share from each linked chat; a capped one is
named in the output, and `--cursor` reads the rest. A linked chat outside `--source` is listed as not read. Confirmed `person` members of the project are read by sender too, without `--contact` (no aliases; a suggested member is not read; a person also given with `--contact` is read once). Members beyond the 16 lane limit are listed as not read (`member, member-limit`), never dropped silently. Link a chat with
`memo relationships add chat:<provider>/<account>/<chat> project:<id>`; yours waits for the owner to confirm it. When `next` names `relationships scan`, `memo relationships scan <project> --source <accounts|all>` lists the chats and people that look like the project's and writes nothing; with `--yes` it writes them as proposals by `memo-scan` for the owner's `memo review`, never as links. Its `groups` name each chat two or more proposed people write in, with `memo review list via:<chat>` to show that group's senders together; the confirm stays the owner's. `--contact person:<id>` (find the id with `memo search people <name>`) reads every message and mail that person's stored identities wrote in `--source` (a `sender` item, matched by who wrote it, may name nothing) and searches the aliases the owner gave them, not their messenger display name; an unknown id is `not_found`. New mail and documents are indexed first unless `--no-catch-up`. A `person-only` item mentions a person, not the project. To answer who is involved, read `people`: who wrote the run's messages and mail, person by person from stored contacts (linked identities across messengers count as one; the owner is left out; at most 20, `people_omitted` for the rest; add the counts up across `--cursor` runs). It never matches names in the text, so do not add people from names you read in excerpts. Unread or failed sources are coverage, not
absence. A chat held only in part (`completeness: partial`, or `pending` in `linked_chats`) is coverage too: read `meta.complete`, `missing` and the `linked_chats` lines before saying something is absent. The text names the command that syncs it (`tg <profile> messages sync …`), and `--json` puts it in each `linked_chats` row as `sync_command`; once the owner agrees to the download, run that, or add `--sync-first` to sync the project's partial linked chats before reading (bounded by `--sync-time`, 3 minutes by default). When several profiles of one messenger are signed in to a chat's account, memo does not choose: ask the owner which, and pass it as `--sync-profile max=<profile>`. A partial answer exits 0; trust `meta.complete`, not the exit code. A document too large to read is listed under `oversized`: open it with `memo notes show <ref>`. Continue a stopped run with `--cursor <checkpoint>` and the same options. Nothing is proposed or
confirmed: cite the references, then stage findings with `memo projects actions add` (MCP
`project_actions_add`), each reference with the `fingerprint` from the evidence. Review with `memo projects actions
list <project>`: it shows each cited text, whether it changed, and the messages or paragraphs around it.
Suggested key documents have `state: "untracked"` because no source fingerprint was saved; reread them before deciding. A changed
text refuses only the findings that cite it; confirm the others and stage a new batch for those. Every decision is
the owner's unless they set `agent_decisions: true`; a refusal with `proposals.agent-decisions-off` means hand the
batch to them. When it is on, decide what you are confident about with `confirm` or `reject` and `--reason` — the
reason is kept with the decision — and ask the owner about anything uncertain: who did what, dates, commitments
versus suggestions.

For an explicitly requested isolated reconstruction, `projects annotations export` writes a new private
file of selected aliases, facts and generic links. `projects annotations check` needs an existing
destination project/store and explicit reference bindings; show its coverage and conflicts. Notes,
meeting memberships, tasks, memories, labels and findings are omitted: never treat this as a full
project backup or use it to justify clearing live data. MCP offers `project_annotations_snapshot` and
`project_annotations_preview`; neither restores records. The generated `projects_annotations_restore`
requires the owner's explicit `projects.annotations.restore` permission. Never clear agent environment
markers to bypass that permission. Historical proposals stay proposed.

A person's `member-of` a project may carry `engagement`: `none`, `low`, `medium` or `high`, how much the owner deals
with that person himself, not how active they are; absent is unknown. A `low` or `none` member is still a member and
is still read by sender. `memo projects context` lists the project's people high, medium, unknown, low, none. A
`role` is one of the project's roles; the owner's words about it are `role_note`. Set either with
`memo relationships update <id> --engagement <level>` or `--role-note <text>`; yours waits for the owner in
`memo review`, and never guess a level from how much a person writes.
