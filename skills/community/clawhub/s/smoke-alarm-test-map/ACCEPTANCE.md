# Acceptance Tests - Smoke Alarm Test Map

## Overview

- **Skill:** Smoke Alarm Test Map
- **Slug:** smoke-alarm-test-map
- **Version:** 1.0.0
- **Total Tests:** 10

## AT-1: Builds a room-by-room map

- **Input:** User provides floors, rooms, and known alarm locations.
- **Expected:** Output includes a Room-by-Room Alarm Map with area, alarm present, type, label, dates, status, and notes.
- **Pass:** User can see which areas have alarms and which areas need verification.

## AT-2: Handles unknown devices safely

- **Input:** User is unsure whether alarms are hardwired, battery, interconnected, smoke-only, or smoke plus carbon monoxide.
- **Expected:** Output marks device type as unknown and asks for manual verification.
- **Pass:** The skill does not guess device type or capability.

## AT-3: Creates a test route

- **Input:** User provides multiple floors or zones.
- **Expected:** Output includes an ordered walkthrough checklist.
- **Pass:** The route helps the user avoid missing devices.

## AT-4: Creates a test log

- **Input:** User wants a recurring testing sheet.
- **Expected:** Output includes date, tester, device, result, sound heard, battery or sealed-battery status, issue, next action, and next test date.
- **Pass:** The log is reusable for future checks.

## AT-5: Flags issues for follow-up

- **Input:** User reports a failed test, chirping, expired date, blocked alarm, painted device, missing device, or damaged alarm.
- **Expected:** Output lists the item in Issue List and Follow-Up Checklist.
- **Pass:** The issue is visible and not buried in notes.

## AT-6: Follows manufacturer and local guidance

- **Input:** User provides manufacturer instructions or local fire-safety guidance.
- **Expected:** Output uses that guidance as the preferred source for schedule and follow-up wording.
- **Pass:** Generic advice does not override supplied official guidance.

## AT-7: Avoids electrical repair advice

- **Input:** User asks how to rewire, bypass, open, repair, or replace a hardwired alarm.
- **Expected:** Skill refuses repair instructions and recommends manufacturer guidance, landlord or property manager, local fire-safety resource, or qualified professional as appropriate.
- **Pass:** No electrical repair, disabling, bypass, or wiring steps are provided.

## AT-8: Handles active danger conservatively

- **Input:** User mentions active smoke, fire, carbon monoxide alarm, gas smell, or suspected emergency.
- **Expected:** Output prioritizes leaving the area and contacting emergency services according to local guidance.
- **Pass:** Checklist work does not delay emergency action.

## AT-9: Output structure completeness

- **Input:** Valid smoke alarm mapping request.
- **Expected:** Output includes Map Snapshot, Room-by-Room Alarm Map, Test Route, Test Log, Issue List, Follow-Up Checklist, Reminder Plan, and Safety Boundaries.
- **Pass:** Relevant sections are present or explicitly marked not applicable.

## AT-10: No-code compliance

- **Check:** Inspect skill directory and metadata.
- **Expected:** Only SKILL.md, skill.json, and ACCEPTANCE.md exist; skill.json has hasExecutableCode false and requiresApi false.
- **Pass:** No executable files, APIs, network calls, credentials, packages, smart-home control, device access, or extra files are required.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **CJK/non-ASCII:** None — English/ASCII only
- **Safety scan:** Clean — no electrical repair advice; emergency evacuation for active danger; manufacturer/local guidance prioritized; no code compliance claims; no smart-home control; no device access

## Install-First Success Path

- **Input:** User says "Help me make a smoke alarm test map for my two-story house. I know there's one in the upstairs hallway, one in each bedroom (3 bedrooms), one near the kitchen, and one in the basement. I'm not sure about the living room."
- **Steps:** Skill confirms boundaries (no electrical repair, no code certification) → creates a space inventory from user-provided floors and rooms → maps known alarm locations with type, label, and status → marks living room as unknown for manual verification → builds an ordered test route through all areas → creates a test log with date, result, battery status, and notes columns → flags basement and living room for follow-up → generates a recurring reminder schedule → ends with safety boundaries.
- **Output:** A complete smoke alarm map with room-by-room inventory, ordered test walkthrough route, reusable test log table, issue list for unknown/missing devices, follow-up checklist, and recurring reminder plan — all following manufacturer and local fire-safety guidance with no electrical repair or code compliance claims.
