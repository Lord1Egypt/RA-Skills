# Acceptance Criteria: School Locker Setup Map

## Must Do

- Produce a locker layout map with zones, supplies, labels, reset cues, routines, and photo-checklist prompts.
- Ask for or state assumptions about locker type, school rules, main pain point, and passing time.
- Keep labels generic and safe for public visibility.
- Include a supply list with must-have, nice-to-have, skip-unless-allowed, and do-not-store-visibly groups.
- Include daily operating routine and weekly reset routine.
- Include privacy warnings for photo checklist and visible labels.
- Replace sensitive details with generic placeholders if the user provides them.

## Must Not Do

- Do not include valuables in visible labels.
- Do not include private schedules, locker combinations, student IDs, addresses, medication details, payment cards, or exact daily routes in the visible map.
- Do not recommend storing expensive electronics, cash, jewelry, or sensitive documents in a visible or unsecured way.
- Do not ignore school rules about locker accessories, food, sprays, stickers, locks, or cleaning supplies.
- Do not overcomplicate the setup with bulky organizers when a simple zone plan is enough.
- Do not create executable code, package files, credential files, or network-dependent assets.

## Metadata Requirements

- Version is `1.0.0`.
- License is `MIT-0`.
- Language is `en`.
- `hasExecutableCode` is `false`.
- Directory contains exactly `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.

## Manual Test

Input:

- Student: grade 7
- Locker: narrow with one shelf and two hooks
- Pain point: papers get crushed and backpack is heavy
- Items: binders, lunch, coat, gym shoes, pencil pouch, calculator
- School rule: magnets allowed, food must be sealed

Expected result:

- The map puts heavy books or binders low or in an easy-reach zone.
- The paper flow has an inbox and return area.
- Lunch is sealed and separated.
- Labels are generic and do not reveal private schedules or valuables.
- The weekly reset routine is short and student-friendly.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description/version/type/tags/author | ✅ |
| skill.json | Valid JSON, version 1.0.0, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "Set up my locker for grade 8. It's narrow with one shelf and two hooks. I keep crushing my papers and my backpack is heavy."
2. **Steps:** The skill guides the assistant to: (a) set privacy and safety rules first, (b) capture constraints and inventory items, (c) design zones and choose supplies, (d) create safe generic labels, (e) plan the paper flow, routine, and photo checklist, (f) deliver the map.
3. **Output:** A locker layout card with snapshot, zone map, supply list, daily operating routine, photo checklist, and troubleshooting — all with generic labels and no sensitive information visible.

Expected first-run outcome: The student or caregiver receives an actionable locker setup map that is simple to follow during a busy school day, with safe labels and a weekly reset routine.
