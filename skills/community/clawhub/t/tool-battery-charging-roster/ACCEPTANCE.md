# Acceptance Tests - Tool Battery Charging Roster

## Overview
- **Skill:** Tool Battery Charging Roster
- **Slug:** tool-battery-charging-roster
- **Version:** 1.0.0
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 10

## AT-1: Metadata Contract
- **Check:** SKILL.md frontmatter and skill.json identify the same slug and purpose.
- **Expected:** Version is 1.0.0, license is MIT-0, language is en, and hasExecutableCode is false.
- **Pass:** Metadata is consistent and prompt-only.

## AT-2: Three-File Directory
- **Check:** The skill directory contains only SKILL.md, skill.json, and ACCEPTANCE.md.
- **Expected:** No scripts, packages, executable files, API files, credential files, or extra documentation exist.
- **Pass:** Directory is document-only.

## AT-3: Scope Boundary
- **Check:** The skill states its purpose as organization and basic charging reminders only.
- **Expected:** It directs users to manufacturer instructions and avoids safety guarantees.
- **Pass:** It does not claim the setup is fireproof or risk-free.

## AT-4: No Electrical Repair Guidance
- **Check:** The skill avoids repair and modification instructions.
- **Expected:** It does not instruct users to open chargers, open battery packs, replace cells, solder tabs, bypass fuses, defeat thermal protection, modify plugs, repair cords, test live circuits, or improvise adapters.
- **Pass:** Suspected defects are routed to manufacturer support or qualified repair.

## AT-5: Compatibility Holds
- **Check:** The workflow handles unknown compatibility.
- **Expected:** Unknown battery and charger pairs are marked hold for manual check and are not charged until resolved.
- **Pass:** The skill avoids guessing about compatibility.

## AT-6: Visible Condition Screening
- **Check:** The workflow uses visible-condition checks.
- **Expected:** It checks for swelling, cracks, leaking, corrosion, burn marks, melted plastic, damaged cords, missing labels, unusual odor, unusual heat, smoke, and error lights.
- **Pass:** Questionable items are separated from the active roster.

## AT-7: Fire-Safe Charging Reminders
- **Check:** The output includes basic charging reminders.
- **Expected:** It covers compatible charger only, dry and ventilated area, stable surface, clear space, no covered chargers, cool-down when indicated, and keeping flammables away.
- **Pass:** Reminders are practical and non-technical.

## AT-8: Roster And Charger Map
- **Check:** The output includes a battery roster and charger map.
- **Expected:** It captures labels, platform, printed voltage and capacity if available, current status, visible condition, location, next action, charger compatibility group, and clear-space reminder.
- **Pass:** The user can manage battery status and charger assignments.

## AT-9: Session Closeout
- **Check:** The output includes a closeout routine.
- **Expected:** It covers marking full batteries, removing or unplugging according to manufacturer guidance, queuing used batteries, separating inspect or retire items, clearing clutter, and noting missing items.
- **Pass:** The station can be reset after use.

## AT-10: English And No-Code Compliance
- **Check:** Skill content is English-only and prompt-only.
- **Expected:** No CJK text, no executable guidance, no API requirements, no network requirements, and no credential requirements.
- **Pass:** The skill remains a document-only prompt flow.

## Clean Scan Evidence

- Directory: `tool-battery-charging-roster/`
- Files: `SKILL.md`, `skill.json`, `ACCEPTANCE.md` (3 files, no extras)
- `SKILL.md`: English/ASCII only, frontmatter valid, no executable code blocks, no secrets
- `skill.json`: JSON valid, `hasExecutableCode: false`, `no_network: true`, `no_credentials: true`
- `ACCEPTANCE.md`: English/ASCII only, no CJK text
- No `.env`, `.git`, `node_modules`, `.log`, `.tsv`, `package.json`, `requirements.txt`, or credential files
- No network endpoints, no API keys, no tokens
- `grep -rE '(sk-|api_key|token|secret|password|BEGIN RSA|BEGIN OPENSSH)'`: 0 matches

## Install-First Success Path

**Input:** User says "I have 6 Ryobi 18V batteries and 2 chargers in the garage. Help me make a charging roster so I know which ones are full and which need charging before the weekend."

**Steps:**
1. Agent asks: battery labels/voltages, charger locations, current charge status, work pattern, and label method
2. Agent confirms all batteries and chargers are compatible (same platform)
3. Agent inspects batteries visibly: asks about swelling, cracks, leaking, corrosion, damaged cords, odor
4. Agent assigns each battery a status: full, charging, used, cool down, inspect, hold, retire
5. Agent builds rotation rule (oldest used first or numbered slots)
6. Agent produces a roster with battery labels, statuses, charger assignments, and fire-safe closeout routine

**Output:** A printable Tool Battery Charging Roster with battery status table, charger map, compatibility holds, rotation rule, fire-safe charging reminders, and session closeout checklist — ready to post on the garage wall or tool chest
