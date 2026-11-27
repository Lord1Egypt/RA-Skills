# Publication check

Run before every push of this skill to the public repo. Every item must pass; a
hit is fixed in the file, never waved through. Run the commands from the
repository root (`industry-solutions/maintenance-inspections/` is the directory under
test).

## 1. Checklist

| # | Check | Pass when |
|---|---|---|
| 1 | No identifiers of a tested build: 32-character hex strings, shortened hex forms, commit hashes | rg 1 finds nothing |
| 2 | No scope numbers or object ids — only placeholders such as `<maintenance_scope_id>` | rg 2 finds nothing |
| 3 | No e-mail addresses except `@example.com` | rg 3 finds nothing |
| 4 | No absolute paths of a build machine (home, workspace, temp directories) | rg 4 finds nothing |
| 5 | No ticket, comment or notification numbers | manual read + rg 5 |
| 6 | No names of real people, agents or a reference business other than the fictional ExampleWorks | rg 6 finds nothing |
| 7 | No platform internals: server files, line numbers, internal function names, database tables or columns, query language, privileged tools, the platform's version number, tool counts | rg 7 finds nothing; manual read of every code block |
| 8 | No source ids and no leftover markers of unfinished files | rg 8 finds nothing |
| 9 | No live identifiers of a tested build | rg 9 finds nothing |
| 10 | No German display labels or country-specific rules outside the country module | rg 10: every display-label hit is in the country module |
| 11 | No build-history wording for customers (how the authors built or tested it, query or loop internals) | rg 11 finds nothing |
| 12 | All relative links resolve; platform references are linked, not copied | link check (section 3) prints nothing |
| 13 | Nothing from internal working material enters the repo | `git status` shows only files of this skill |
| 14 | "Verified against platform schema <date>" updated in SKILL.md | date matches the last schema read |
| 15 | Text is English throughout; German specifics and display labels occur only in the country module | manual read |

## 2. Search patterns (rg)

```bash
D=industry-solutions/maintenance-inspections
# private lists, kept OUTSIDE the repo (never committed):
NAMES=../publication_names_intern.txt
IDS=../publication_ids_intern.txt
LIVE=../publication_live_ids_intern.txt

# 1 identifiers / hashes
rg -n -i '[0-9a-f]{32}' "$D"
rg -n -i '\b[0-9a-f]{8}…' "$D"
rg -n -i '\b[0-9a-f]{40}\b' "$D"

# 2 scope numbers and ids of the tested build
rg -n -i 'scope ?(id)? ?[0-9]+\b' "$D"
rg -n '"scope_id": ?[0-9]+|"scopes": ?\[[0-9]' "$D"
rg -n -w -F -f "$IDS" "$D"

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

# 9 live identifiers of the tested build
rg -n -w -F -f "$LIVE" "$D"

# 10 German display labels (option values stay English in the core)
rg -n -i '\b(Prüfung erfassen|Prüfprotokoll|Mangel melden|Überfällig|Prüffrist|Prüfdatum|Unterschrift|Feuerlöscher|Ölwechsel)\b' "$D" \
  | rg -v 'references/country-de\.md'

# 11 build-history wording
rg -n -i 'we (built|tested|noticed)|in our (run|test|workspace)' "$D"
```

## 3. Link check

From the skill directory, every relative markdown link must resolve to a file
that exists (platform skill paths are `../../../telesherpa-ontology-platform/…`
and `../../shift-planning/…`, because this folder sits under
`industry-solutions/`). Do not keep a second copy of those references.

## 4. Keep out of the repo

Private name and id lists, run logs, screenshots with live identifiers, and any
MCP responses that contain identifiers stay outside the published tree.
