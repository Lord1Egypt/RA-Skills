# tklr syntax reference

Every form below was validated against **tklr 1.0.43** with `tklr check`.
Where the published docs disagree with the binary, the binary wins and the
difference is flagged.

## Entry shape

```
<itemtype> <subject> @<key> <value> @<key> <value> ...
```

### Item types

| Type | Meaning | Notes |
|------|---------|-------|
| `*` | Event | appointment on the calendar; needs `@s` |
| `~` | Task | something to finish; `@s` optional |
| `^` | Project | container for `@~` jobs |
| `%` | Note | reference material, no schedule |
| `!` | Goal | N completions per period; needs `@s` and `@t` |
| `-` | Jot | quick timestamped entry (use `tklr jot`) |
| `?` | Draft | incomplete — **tklr also downgrades invalid entries to this** |
| `x` | Finished | set by `tklr finish` |

## Tokens

| Token | Meaning | Verified example |
|-------|---------|------------------|
| `@s` | scheduled start / due | `@s 2026-08-06 2p`, `@s fri 9a`, `@s today` |
| `@e` | extent (duration) | `@e 45m`, `@e 1h30m` |
| `@a` | alerts | `@a 1d, 1h, 15m: m, e` |
| `@d` | details / description | `@d Bring the survey printout.` |
| `@r` | recurrence | `@r d`, `@r w &i 2 &w TU`, `@r y`, `@r m &i 1` |
| `@b` | bin | `@b alex/users` — **leaf first** (see below) |
| `@p` | priority 1 (highest) – 5 | `@p 1` |
| `@l` | label / location | `@l Cafe Ambrosia` |
| `@i` | invitees (comma separated) | `@i sam@example.com` |
| `@n` | notice (early warning) | `@n 30d` |
| `@o` | offset — reschedule after finishing | `@o 3d` |
| `@w` | wrap: travel before, after | `@w 30m, 15m` — **comma, not `/`** |
| `@t` | goal target `count/period` | `@t 3/1w` — **period needs a number** |
| `@~` | project job — **every job needs `&r`** | `@~ Book flights &r a` |
| `@c` | context | `@c errands` |
| `@g` | goto — url or file path | `@g https://example.com` |
| `@u` | use (jot time tracking) | `@u billing` |
| `@+` / `@-` | add / exclude datetimes — **comma-separated in one token** | `@- 2026-08-11 9a, 2026-08-12 9a` |
| `@m` | masked (obfuscated) value | `@m account 1234` |
| `@z` | *not a token* — timezone rides on `@s` | `@s 3p z US/Pacific` |

### Project jobs — `@~` and `&r`

Every `@~` job **must** carry an `&r` label, and labels must be an **integer or
a single lowercase letter** (`do_requires`). `&r ID:REQ1,REQ2` declares
prerequisites.

```
^ Plan trip @~ Book flights &r a @~ Reserve hotel &r b @~ Pack &r c
^ Reno @~ Demo &r 1 @~ Rewire &r 2:1 @~ Drywall &r 3:2      # ordered chain
^ Launch @~ Draft &r a @~ Review &r b:a @~ Ship &r c:a,b    # fan-in
```

> **`tklr check` does not catch a missing `&r`.** It reports "Entry is valid",
> then `add` stores the entry as a draft with
> `@d Import error: Each @~ job requires an &r label`. Word labels fail too:
> `&r flights` is rejected, `&r f` is fine. So after adding a project, read
> what `add` printed and confirm the stored itemtype is `^` and not `?`.

### Corrections to the published docs

* `@t 3/w` is documented but **fails**. Use `@t 3/1w` — the period needs an
  explicit multiplier.
* `@w 30m/15m` fails. `@w` is a *list of two* periods: `@w 30m, 15m`.
* `@l` is described as "label"; it behaves as the location/label field.

## Recurrence

`@r` takes a frequency character, then `&` options.

| Frequency | Meaning |
|-----------|---------|
| `y` `m` `w` `d` `h` `n` | year, month, week, day, hour, minute |

| Option | Meaning | Example |
|--------|---------|---------|
| `&i` | interval | `@r w &i 2` = every 2 weeks |
| `&w` | weekdays `SU`–`SA` | `@r d &w MO,TU,WE,TH,FR` |
| `&m` | months 1–12 | `@r y &m 3,9` |
| `&d` | month days (negative counts from end) | `@r m &d -1` = last day |
| `&H` `&M` | hours / minutes | `@r d &H 9,17` |
| `&E` | days relative to Easter | `@r y &E 0` |

Verified: `* Team standup @s 2026-08-03 9a @e 30m @r d &w MO,TU,WE,TH,FR`

## Datetimes

**Resolve relative dates yourself and pass an absolute value.** tklr's fuzzy
parser is narrower than the docs suggest, and it rejects several phrases a
user will say out loud. Tested against 1.0.43:

| Expression | Result |
|------------|--------|
| `today`, `now`, `3p`, `fri`, `fri 9a`, `9a fri`, `mon 10a` | accepted |
| `2026-08-05`, `2026-08-05 3p`, `2026-08-05 15:00`, `8/5`, `8/5 3p` | accepted |
| `tomorrow` | **rejected** |
| `tomorrow 3p`, `3p tomorrow` | **rejected** |
| `3p today` | **rejected** (bare `today` is fine) |
| `next week` | **rejected** |

So when the user says "tomorrow at 3", compute the date and write
`@s 2026-08-01 3p`. Only `today`, `now`, and weekday names are safe to pass
through verbatim.

* A bare weekday means the *next* one.
* Date with no time = all-day.
* Timezone: `@s 3p z US/Pacific`; `z none` makes it naive/floating.

**Timedeltas:** combine `w` `d` `h` `m` `s` with numbers — `2h30m`, `1w`,
`45m`, `-15m`. Negative values are allowed.

## Alerts — `@a`

```
@a <offsets> : <channel letters>
```

* Offsets are timedeltas *before* the start; negative means after.
  `@a 1h, -15m: r` → one hour before, and fifteen minutes after.
* Letters are keys in `[alerts]` of the workspace `config.toml`, and must be
  **single lowercase letters** (`a`–`z`) — enforced by `is_lowercase_letter()`.
  Multi-character names like `alex_chat` are rejected. `n` is built-in (bell +
  popup), leaving 25 usable.
* Multiple offsets × multiple letters = **one Alerts row per combination**, so
  each row is one delivery.
* Repeat the token for different lead times per channel:
  `@a 1d: r @a 15m: a`.
* tklr renders `{name}`, `{when}`, `{start}`, `{time}`, `{location}`, and
  `{description}` into the stored `alert_command`.

> **Critical:** a letter that is not defined in `[alerts]` makes the whole
> entry invalid. tklr does not error out on `add` — it silently stores the
> entry as a **draft (`?`)** with `@d Import error: Undefined alert command`.
> Always `tklr check` a new pattern, and confirm the itemtype afterwards.

Alert commands are executed with `shlex.split()` and no shell (mirroring
tklr's `execute_alert()`), so quote arguments containing spaces and wrap pipes
in `sh -c "..."`. A `"` inside a subject or `@d` makes the rendered command
unparseable.

## Bins — `@b`

Bins are the structured grouping mechanism, and this skill uses them to
record **which people a reminder belongs to**.

```
@b Leaf/Parent/Grandparent      ← leaf FIRST, the reverse of a file path
```

* `@b alex/users` creates bin `alex` inside bin `users`, and links the
  reminder to the **leaf** (`alex`).
* Repeat the token for several bins: `@b alex/users @b jordan/users`
  links one reminder to both people.
* Bin names are globally unique, case-insensitive (`Bins.name`).
* A single-segment `@b foo` is filed under the system bin `unlinked`.
* `tklr details <id>` prints the collapsed leaf (`@b alex`), not the path.

Default bins shipped by tklr: `root`, `unlinked`, `activities`, `journal`,
`library` (`books`, `ideas`, `poetry`, `quotations`, `series`, `video`),
`people`, `places`, `projects`.

## Hashtags

`#word` anywhere in the subject or `@d` details. Free-form, no declaration
needed — good for themes (`#cooking`), not for people (bins are structured).

## Commands

| Command | Use |
|---------|-----|
| `tklr add "<entry>"` | create; `-f FILE` or `--batch` for many — entries in a file are separated by lines containing only `...`, **not** by newlines |
| `tklr check "<entry>"` | validate without saving — **use before add** |
| `tklr agenda [--ids]` | next 3 days + tasks by urgency |
| `tklr days --start DATE --end N\|DATE [--ids]` | day-by-day listing |
| `tklr weeks --start DATE --end N` | week grid |
| `tklr details <id>` | full record, shows raw tokens |
| `tklr find <regex>` | search subject and `@d` |
| `tklr query '<dsl>' [--ids]` | structured query (below) |
| `tklr finish <id> [datetime]` | complete a task; `-y` to skip prompt |
| `tklr alerts [--end N] [--format json]` | alerts for today .. +N days |
| `tklr jot`, `tklr jots`, `tklr uses` | time tracking |
| `tklr urgency-report` | why tasks rank as they do |
| `tklr ui` | **never run this** — interactive, blocks the terminal |

Add `--width N` to `agenda`/`days`/`weeks` for narrow chat output, and
`--plain` to strip colour codes.

### Query DSL

```
tklr query 'in b alex and equals itemtype *'
```

Commands: `begins`, `in` (substring/regex), `equals`, `more`, `less`,
`exists`, `any`, `all`, `one`, `dt`, `info <id>`.
Fields: `itemtype`, `subject`, and any token key (`b`, `s`, `d`, `p`, `c`, …).
Join clauses with lowercase `and` / `or`; prefix a command with `~` to negate.

* `in b alex` — regex *search*, so it also matches `alexis`. Use
  `equals b alex` when the distinction matters.
* Quote the whole query: `equals itemtype *` needs quoting or the shell
  expands `*`.
* `dt <field> ? date|time` — test whether a datetime is date-only or timed.

## Workspace layout

```
<TKLR_HOME>/
  config.toml      # [alerts] letters live here
  tklr.db          # SQLite: Records, DateTimes, Alerts, Bins, ReminderLinks, …
  logs/
```

**Home resolution order** — first match wins:

1. the current directory, if it holds both `config.toml` and `tklr.db`
2. `$TKLR_HOME`
3. `$XDG_CONFIG_HOME/tklr`
4. `~/.config/tklr`

Rule 1 makes an unqualified `tklr` call depend on where it was run from, so
**always pass `--home` explicitly**.

## Derived tables and the staleness bug

`DateTimes`, `Alerts`, `Notice`, and `Urgency` are generated caches, rebuilt
only when the day changes or when a version string derived from
`max(Records.modified)` — which has only **minute** resolution — changes.
`Records.modified` is stored as `YYYYMMDDTHHMMZ`, so two reminders saved in
the same clock minute yield the same version string.

A reminder saved in the same minute as the previous rebuild leaves that
version unchanged, so **its `DateTimes` row is never generated. Its alerts
never fire (alert generation joins `DateTimes`) and it is missing from
`days` / `weeks` / `agenda`,** even though `details` and `find` still show it.

The poller detects this (a scheduled reminder with alerts but no `DateTimes`
row) and heals it. After adding or editing anything with alerts, run:

```bash
python3 ~/.hermes/scripts/tklr_alert_poller.py --heal
```

`--heal` is a flag on this skill's dispatcher script, **not** a tklr option.
tklr has no command to force a rebuild of its derived tables.

## Alerts table

> Reference only — this documents why the poller's three sanctioned database
> exceptions are safe. **Do not query `tklr.db` yourself**; use the `tklr`
> commands above. See "Direct SQLite use" in SKILL.md.

```sql
CREATE TABLE Alerts (
  alert_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  record_id        INTEGER NOT NULL,
  record_name      TEXT    NOT NULL,
  trigger_datetime TEXT    NOT NULL,  -- 'YYYYMMDDTHHMM', local-naive
  start_datetime   TEXT    NOT NULL,  -- 'YYYYMMDD' or 'YYYYMMDDTHHMM'
  alert_name       TEXT    NOT NULL,  -- the channel letter
  alert_command    TEXT    NOT NULL
);
UNIQUE INDEX ON (record_id, start_datetime, alert_name, COALESCE(trigger_datetime,''))
```

* `populate_alerts()` inserts only alerts triggering between *now* and
  end-of-day, and its cleanup deletes only rows with `trigger_datetime >= now`.
  A row whose trigger has already passed is never regenerated — which is
  precisely why deleting a fired alert is permanent and safe.
* `tklr alerts --format json` reports **`alert_id` as `null`**. Never key on
  it; use the four columns of the unique index.

---

## Hand-composition hazards

Only relevant when using `tklr_agent_wrapper.py --raw`. The wrapper handles all of
this for you; these are the traps it removes.

### Getting `@s` right first time

**Compute the date yourself.** tklr's parser is narrower than it looks, and
inconsistently so — `fri 3p` works but `today 3p` does not. Verified against
1.0.43:

| Accepted | Rejected |
|----------|----------|
| `2026-08-01`, `2026-08-01 15:00`, `2026-08-01 3p` | `tomorrow`, `tomorrow 3p`, `tomorrow at 3pm` |
| `8/1 3p`, `08/01/2026 3p`, `Aug 1 3p`, `1 Aug 2026 3pm` | **`today 3p`**, `next monday`, `next week` |
| `3pm`, `15:00`, `today`, `now` | `tonight`, `this evening`, `in 2 hours` |
| `fri`, `fri 3p`, `9a fri`, `sat 15:00` | anything else conversational |

Safest habit: emit `@s YYYY-MM-DD HH:MM`. Bare `today`, bare `now`, and weekday
names with or without a time are the only relative forms worth passing through.

### Two traps `tklr check` will not catch

`check` validates parsing only, so it can approve an entry that `add` then
files as a draft:

1. **A `@~` job without `&r`.** Every project job needs a label, and labels must
   be an integer or a *single lowercase letter* — `&r a` or `&r 1`, never
   `&r flights`. `check` says "Entry is valid"; `add` says
   `Import error: Each @~ job requires an &r label`. Use `&r b:a` for "b depends
   on a".
2. **A missing itemtype character.** `add` reports `Added 0 entries
   successfully` with an `=== Invalid items ===` block. Read it — an entry
   starting with anything other than `* ~ ^ % ! - ?` is not stored.

Both are why step 2 means *reading* the output of `add`, not just running it.

