---
name: smoke-alarm-test-map
description: Build a room-by-room smoke alarm map and recurring test log from user-provided home details, focusing on checklist tracking and manufacturer or local fire-safety guidance without electrical repair advice.
---

# Smoke Alarm Test Map

## Overview

Use this skill when the user wants to confirm that every smoke alarm or smoke detector in a home, apartment, office, studio, cabin, or rental unit is accounted for and tested. The deliverable is a room-by-room alarm map, test log, battery or replacement notes, and next-check schedule.

This is a prompt-only home safety organization skill. It does not provide electrical repair advice, wiring instructions, code compliance certification, installation design, or emergency response instructions beyond conservative safety guidance. Users should follow manufacturer instructions, local fire department guidance, landlord or building rules, and applicable local requirements.

## Trigger

Use this skill when the user asks to:

- Make a smoke alarm checklist for a home or unit.
- Map alarms by room, hallway, floor, sleeping area, or utility area.
- Run a monthly or seasonal smoke alarm test.
- Track battery dates, replacement dates, chirping devices, or failed tests.
- Prepare a landlord, family, roommate, caregiver, or house-sitter checklist.
- Create a reminder schedule for future alarm testing.

Do not use this skill to troubleshoot wiring, open electrical devices, bypass alarms, silence active alarms during danger, certify code compliance, or replace professional fire-safety guidance.

## Intake

Ask for the minimum details needed to create the map:

- Home type, such as apartment, house, dorm, cabin, office, or rental.
- Floors or zones, such as basement, main floor, upstairs, garage, hallway, or bedrooms.
- Rooms or areas to include.
- Known alarm locations and device types if known, such as smoke, smoke plus carbon monoxide, hardwired, battery, sealed battery, interconnected, or unknown.
- Last test date, last battery change date, manufacture date, or replacement date if known.
- Any devices that chirp, fail to sound, are missing, are blocked, are painted over, or have unclear labels.
- Manufacturer instructions or local guidance supplied by the user.

If the user is unsure, create a discovery checklist and mark unknown devices for manual verification.

## Workflow

1. **Confirm purpose and boundaries.** Explain that the output is a test map and log, not electrical repair or code certification.
2. **Create the space inventory.** List each floor, room, hallway, sleeping area, stair area, utility area, and special area the user provides.
3. **Map alarm locations.** For each area, record device present, device type, label, nearby room, height or ceiling/wall note if supplied, and accessibility.
4. **Build a test route.** Order locations so the user can walk through the space without missing devices.
5. **Add test-log fields.** Include test date, test result, sound heard, indicator light if relevant, battery or sealed-battery status, manufacture or replace-by date, notes, and next action.
6. **Flag issues for follow-up.** Mark no alarm found, failed test, weak sound, chirping, expired device, blocked device, painted or damaged device, unknown device type, inaccessible device, or unclear manufacturer instructions.
7. **Provide safe next steps.** For failed, damaged, expired, missing, or wiring-related concerns, advise following manufacturer guidance and contacting the landlord, property manager, local fire department non-emergency resource, or qualified professional as appropriate.
8. **Schedule the next check.** Create recurring reminders the user can add manually, based on manufacturer or local guidance if supplied.
9. **End with a safety note.** In an active alarm, smoke, fire, gas smell, or carbon monoxide concern, leave the area and contact emergency services according to local guidance.

## Output Format

Return these sections:

1. **Map Snapshot**: home type, floors or zones, date basis, supplied guidance, and assumptions.
2. **Room-by-Room Alarm Map**: area, alarm present, type, label, last test, battery or replacement date, status, and notes.
3. **Test Route**: ordered walkthrough checklist by floor or zone.
4. **Test Log**: date, tester, device, result, sound heard, battery or sealed-battery status, indicator notes, issue, next action, and next test date.
5. **Issue List**: failed tests, missing alarms, chirps, expired devices, blocked devices, unknown device types, inaccessible devices, or damaged devices.
6. **Follow-Up Checklist**: manual actions for the user, landlord, property manager, manufacturer support, local fire-safety resource, or qualified professional.
7. **Reminder Plan**: recurring test schedule and battery or replacement review prompts.
8. **Safety Boundaries**: follow manufacturer and local fire guidance; no electrical repair advice; active danger means leave and contact emergency services.

For a quick request, provide the Room-by-Room Alarm Map and Test Route first.

## Mapping Rules

- Treat bedrooms, sleeping areas, hallways near sleeping areas, stairways, kitchens, living areas, utility areas, basements, garages, and separate units as areas to ask about or list if provided.
- Mark unknown device types as unknown; do not guess hardwired, battery, interconnected, or carbon monoxide capability.
- Record the user's supplied manufacturer or replace-by date exactly when available.
- If a device fails a test, chirps, is expired, is missing, is blocked, is painted over, or is damaged, flag it for prompt manual follow-up.
- If the user has local fire department or manufacturer instructions, prioritize those over generic reminder wording.
- Do not state that a home is code compliant or safe based only on the checklist.

## Boundary Rules

- Do not give electrical repair, rewiring, bypass, disabling, soldering, battery-terminal repair, or hardwired replacement instructions.
- Do not tell the user to ignore chirps, remove devices permanently, cover devices, or silence an alarm in an unsafe situation.
- Do not certify compliance with building, rental, insurance, fire, or occupancy codes.
- For installed-system, hardwired, interconnected, landlord-owned, damaged, expired, missing, or repeatedly failing devices, recommend manufacturer guidance and appropriate local or professional help.
- For active smoke, fire, carbon monoxide alarm, gas smell, or suspected emergency, advise evacuation and emergency services according to local guidance.

## Acceptance Criteria

1. Produces a room-by-room alarm map and test log from user-provided home details.
2. Includes a clear test route and recurring reminder plan.
3. Flags failed, missing, expired, blocked, chirping, damaged, inaccessible, or unknown devices for follow-up.
4. References manufacturer instructions and local fire-safety guidance without claiming code compliance.
5. Avoids electrical repair advice, disabling instructions, and unsafe alarm handling.
6. Requires no code execution, credentials, API access, network access, device access, smart-home control, or extra files.

## Example Prompts

- "Help me make a smoke alarm test map for my apartment."
- "I have alarms in the hallway, bedrooms, and kitchen. Build a test log."
- "Create a checklist so I do not miss any smoke detectors this month."
- "One alarm is chirping and one failed the test. Make a follow-up list, no repair instructions."
- "Make a roommate-friendly smoke alarm walkthrough sheet."
