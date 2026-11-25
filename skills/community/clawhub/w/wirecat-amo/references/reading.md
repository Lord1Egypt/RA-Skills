# Reading the CRM

The profile rule, the store and the account, and "missing is not absent" are in [SKILL.md](../SKILL.md). This file
has the detail behind them.

## Query lists

- `amo work deals list status:open stage:"Quote sent" pipeline:Sales`. `amo help deals list` lists the fields.
  `deals list` also takes `updated:>=1d`, `created:>=30d`, `closed:>=7d` and `owner:` (`owner:me` is your own amoCRM
  user), and `--format csv` prints a page as a table. `activities list` and `changes list` take `owner:me` too.
- `people`, `organizations` and `users` are read live and page with `--limit` (1 to 250, 50 when left out) and
  `--page`. A bare word or `name:` matches the name: `amo work people list "Anna"`.
- **Owner and time on a live list need amoCRM's paid API filter add-on.** `people list` and `organizations list`
  narrow by `assigned_to:` and by time only when the account has it. Without it they refuse with `amo.filters-off`:
  search by name instead. A sync without it reads contacts and companies one request at a time, so it is slower.
- **`assigned_to:me` is the sign-in's own user** (the owner of the token). A live list uses `assigned_to:`, a stored
  one `owner:`. They are not interchangeable.
- **A contact list cannot filter by `created_at`,** even with the add-on: amoCRM's contact list takes no such filter,
  and `amo` refuses it (`crm.record-field`), although `--help` lists the field. Use `updated_at`. A company list takes
  both `created_at` and `updated_at`, with the add-on.

## A deal

- It answers `ref` (`deal:12`), `pipeline`, `stage`, `status` (`open`, `won` or `lost`), `close_date`, and `amount`
  as a decimal string in `currency`. Every `show` and every write takes that `ref`.
- **There are no leads apart from deals.** amoCRM's API names deals "leads"; `amo` has only `deals`. Won or lost is
  `status`, never the stage's name. amoCRM's won and lost stages have the same ids in every pipeline (`142` and
  `143`).
- `deals show` answers `stage_history`, which `sync` reads from the account's events.
- **The funnel:** `amo work pipelines show Sales --since-time 30d --json` counts the deals of a window: each stage's
  number and sum per currency (never converted), how many reached a stage and went on, and the win rate.

## Custom fields

- `amo work fields list deals` (or `people`, `organizations`) lists them with type and options, **as the last `sync`
  stored them**. A field added in amoCRM since then is unknown until the next `sync`.
- A person's or a company's own fields are in `provider_metadata`; `--json=id,name,provider_metadata.<code>` keeps
  one. A contact's job title is one of those fields too.

## Tasks, notes and calls on a deal

When the owner set `crm.amocrm:<address>.activities` to `on` (off by default; only the owner can, an agent is
refused), each `sync` also copies the tasks, comments and calls on the deals it keeps and on their clients, from the
last 90 days. `deals show` lists them, and `activities list` reads them: `overdue:true`, `due:today`, `deal:12`,
`kind:call`, `status:done`. Without the setting `activities list` has nothing to read. Those on a colleague's deal are
never stored, and a call keeps only its direction, never the phone number or the recording.

## Whose data the copy holds

- **The store holds the chosen users' deals only.** A sync copies the deals of the users in
  `crm.amocrm:<address>.unassigned` (by default the sign-in's own user) and the clients on them
  ([setup.md](setup.md)). A deal that is not in `deals list` may belong to a user nobody chose. Read any contact or
  company live with `people list` or `organizations list`.
- **`scope` is `mine` by default, and `sync` refuses `all`** (`amo.scope-all-refused`): `amo` never copies the whole
  CRM, an administrator's either.
- **A sync can be partial and still exit `0`.** Read `complete`, `scope` and `issues`, and answer "unknown", not
  "none", for what they name. `crm.unassigned-dropped` means a chosen user was left out: only an administrator may
  choose a colleague.
- **`search all` leaves out a kind it may not read** and names it in `missing`. Treat `missing` as "not searched",
  not "not found". Before you say something is not there, search in other words, and `sync` if the store is old.

## Phones and e-mails

A contact on the user's own deals comes with its phones and e-mails. A user who is not an administrator sees those of
at most 100 other contacts and companies a UTC day, counted by `amo` on this computer; `crm.foreign-contacts-spent`
says the day's reads are spent. Show only the one the task needs. `api call` refuses to anyone but an administrator every read of contacts, companies,
notes, events and unsorted, and a deal read that embeds its contacts (`crm.client-reads-admin-only`): they hold
clients' phones and e-mails. Do not retry it; tell the owner.

## Pace

amoCRM allows 7 requests a second per integration, and `amo` stays under it, so a long sync takes time. Run one
`sync` at a time. One command has 30 seconds by default (`--timeout 2m` changes it); a `sync` stops before
its deadline or `--max-pages`, says `complete: false`, and the next one goes on from there. `amo.blocked` means
amoCRM blocks every request from here: stop every `amo` command on the account and tell the owner.

The usual read path is in [SKILL.md](../SKILL.md); the write steps that follow it are in [writing.md](writing.md).
