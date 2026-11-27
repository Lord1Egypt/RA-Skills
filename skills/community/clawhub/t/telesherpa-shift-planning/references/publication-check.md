# Publication check

Run before every push of this skill to the public repo. Every item must pass; a hit
is fixed in the file, never waved through. Run the commands from the repository root
(`industry-solutions/shift-planning/` is the directory under test).

## 1. Checklist

| # | Check | Pass when |
|---|---|---|
| 1 | No identifiers of the tested build: 32-character hex strings (object ids, form ids, hashes), shortened hex forms, commit hashes | rg 1 finds nothing |
| 2 | No scope numbers or object ids — only placeholders such as `<planning_scope_id>` | rg 2 finds nothing |
| 3 | No e-mail addresses except `@example.com` | rg 3 finds nothing |
| 4 | No absolute paths of a build machine (home, workspace, temp directories) | rg 4 finds nothing |
| 5 | No ticket, comment or notification numbers | manual read + rg 5 |
| 6 | No names of real people, agents or the reference business | rg 6 finds nothing |
| 7 | No platform internals: server files, line numbers, internal function names, database tables or columns, query language, privileged tools, the platform's version number, tool counts | rg 7 finds nothing; manual read of every code block |
| 8 | No source ids and no draft-status markers of unfinished files left | rg 8 finds nothing |
| 9 | No live identifiers of the tested build (German keys and values, reference view and action names) | rg 9 finds nothing; German display labels belong only in the country module |
| 10 | No German display labels or country-specific rules outside the country module; option values are English everywhere | rg 10: every hit is in the country module or a platform keyword (see notes) |
| 11 | No build-history wording for customers (how the authors built or tested it, query or loop internals) | rg 11 finds nothing |
| 12 | All relative links resolve; platform references are linked, not copied | link check (section 3) prints nothing |
| 13 | Nothing from internal working material enters the repo (section 4) | `git status` shows only files of this skill |
| 14 | "Verified against platform state <date>" updated in SKILL.md; smoke tests re-run on that date | date matches the last run log |
| 15 | Text is English throughout; German specifics and display labels occur only in the country module | manual read |

## 2. Search patterns (rg)

```bash
D=industry-solutions/shift-planning
# private lists, kept OUTSIDE the repo (never committed, see section 4):
#   $NAMES = file with names of people, agents and the reference business, one per line
#   $IDS   = file with scope numbers and other ids of the tested build, one per line
#   $LIVE  = file with live identifiers of the tested build, one per line
NAMES=../publication_names_intern.txt
IDS=../publication_ids_intern.txt
LIVE=../publication_live_ids_intern.txt   # German keys/values and names of the tested build

# 1 identifiers / hashes
rg -n -i '[0-9a-f]{32}' "$D"
rg -n -i '\b[0-9a-f]{8}…' "$D"
rg -n -i '\b[0-9a-f]{40}\b' "$D"

# 2 scope numbers and ids of the tested build
rg -n -i 'scope ?(id)? ?[0-9]+\b' "$D"
rg -n '"scope_id": ?[0-9]+|"scopes": ?\[[0-9]' "$D"
rg -n -w -F -f "$IDS" "$D"             # every hit must be ordinary text (e.g. a price), not an id

# 3 e-mail addresses other than example domains
rg -n -o '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+' "$D" | rg -v '@example\.com$'

# 4 build-machine paths
rg -n '/work[s]pace|/ro[o]t/|/ho[m]e/|/t[m]p/|C:[\\]' "$D"

# 5 ticket / comment / notification numbers
rg -n -i '(ticket|comment|notification|request) ?#? ?[0-9]{3,}' "$D"

# 6 names
rg -n -i -w -F -f "$NAMES" "$D"

# 7 platform internals (character classes keep this file from matching itself)
rg -n -i 's[q]l|a[d]min' "$D"
rg -n -i '\.p[h]p|line [0-9]+|server v[e]rsion|tools: ?[0-9]+|[0-9]+ tools' "$D"

# 8 leftovers
rg -n 'SR[C]-|ST[U]B|out[l]ine' "$D"

# 9 live identifiers of the tested build (German keys and values, reference view and
#   action names), kept in a third private list; case-sensitive, so German display
#   labels in the country module do not match
rg -n -w -F -f "$LIVE" "$D"

# 10 German option values (character classes keep this file from matching itself);
#    allowed: country-de.md, and the platform keywords
#    woche / monat / tag in view definitions
rg -n -i '\b(kr[a]nk|gesend[e]t|off[e]n|fr[u]eh|wunschfr[e]i|abges[a]gt|gepl[a]nt|ver[o]effentlicht|beantr[a]gt|genehm[i]gt|abgel[e]hnt|t[a]usch|k[u]eche)\b' "$D" \
  | rg -v 'references/country-de\.md'
rg -n -w 'mitteilung[S]tatus|stempel[S]tatus' "$D"

# 11 build-history wording (character classes keep this file from matching itself)
rg -n -i 'refer[e]nce build|custom quer[y]|dispatch l[o]op' "$D"
```

Notes:
- Block view keywords of the platform (`richtung`, `vorwaerts`, `rueckwaerts`,
  `werte`, `wo`, `wert`, `nur`, `nur_mit`, `bruecke`, `zeitfeld`, `zeitraum`,
  `woche`, `wochentag_datum`, `zeitspanne`, `waehrung`, `monat`, `warnung`,
  `stellen`, `ziel`, `stundenlohn`, `schwelle`, `schwelle_ab_2027`, `bedingung`, `spalte`, `betrag`, `monat_start`,
  `monat_ende`; see the glossary tables) are platform vocabulary, not live identifiers — they stay.
- `minijob` is a legal term and the `contractType` value; it stays.
- In rg 10, `woche`, `monat` and `tag` are platform keywords of view parameters
  (`param`, `basis`, `format`) and are not searched; `kalenderwoche` and
  `wochentag_datum` are formats. Platform tool responses may contain German words;
  they are never copied into the skill as values.
- German **labels** in [country-de.md](country-de.md) and the German names of laws are
  intended.

## 3. Link check

```bash
cd industry-solutions/shift-planning
for f in SKILL.md references/*.md; do
  rg -o '\]\(([^)#]+)' -r '$1' "$f" | rg -v '^https?://' | while read -r l; do
    [ -e "$(dirname "$f")/$l" ] || echo "BROKEN $f -> $l"
  done
done
```

Absolute links (`https://…`) are opened once by hand before the push.

## 4. Never into the repo

- Working copies of live reads (exports of action, view, form, function or trigger
  definitions; anything in a `live_reads` directory).
- Any file whose name ends in `_intern` (inventories, source lists, notes, the private
  name and id lists of section 2).
- Run logs with real balances, account ids or addresses; backups.
- Bundles built for review (one-file concatenations of this skill).

Check:

```bash
git status --porcelain | rg -v '^.. industry-solutions/shift-planning/(SKILL\.md|references/[a-z0-9-]+\.md)$'
rg --files industry-solutions/shift-planning | rg -i 'live_reads|_intern|backup|bundle'
```

Both commands must print nothing.

## 5. Record

Paste the output of sections 2–4 (empty or with the explained hits of rg 9) into the
release note with date and time (Europe/Berlin).
