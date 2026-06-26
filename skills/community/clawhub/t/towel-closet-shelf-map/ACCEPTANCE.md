# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary keeps advice practical and non-alarmist.
- [x] Boundary avoids medical hygiene, sanitation, infection-prevention, clinical, hotel, daycare, rental, or public facility compliance claims.
- [x] Deliverable is a towel closet shelf map with zones, quantity targets, label text, reset cadence, and restock notes.
- [x] Workflow covers listing towel types, counting current stock, assigning shelf zones, writing labels, and setting reset cadence.
- [x] Slug matches the accepted design: towel-closet-shelf-map.

## Clean Scan Evidence

- [x] No executable code, scripts, binaries, or package files.
- [x] No secrets, credentials, API keys, tokens, or environment variables.
- [x] No network calls, API endpoints, or internet dependencies.
- [x] No CJK characters. Documentation is English/ASCII only.
- [x] `skill.json` is valid JSON with `version=1.0.0`, `license=MIT-0`, `language=en`, `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, `ACCEPTANCE.md`.
- [x] No temp files, log files, or build artifacts.

## Install-First Success Path

**Input:** "Our linen closet is a disaster — towels are everywhere. Help me build a shelf map with labels."

**Steps:**
1. Skill asks for number of shelves, towel categories (bath, hand, washcloth, guest), current counts, household size, and shelf constraints.
2. Skill guides user through listing towel types, counting current stock, setting realistic quantity targets, and assigning shelf zones by frequency of use.
3. Skill creates printable labels, restock notes, overflow handling rules, reset cadence (weekly or laundry-day), and a do-not-mix zone for cleaning rags.

**Output:** A towel closet shelf map with shelf zone assignments, quantity targets, printable labels, reset routine, and restock overflow notes.
