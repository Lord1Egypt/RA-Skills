---
name: tool-battery-charging-roster
displayName: "Tool Battery Charging Roster"
version: "1.0.0"
description: "Create a practical charging roster for cordless tool batteries, chargers, labels, rotation status, storage locations, and basic fire-safe charging reminders without giving electrical repair guidance."
triggerKeywords:
  - tool battery charging roster
  - cordless tool battery checklist
  - battery charging schedule
  - tool charger station
  - power tool battery rotation
  - workshop charging log
  - drill battery charging plan
  - garage battery roster
tags:
  - workshop
  - tools
  - battery-safety
  - charging
  - checklist
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Tool Battery Charging Roster

## Purpose

Use this prompt-only skill when a user wants to organize cordless tool batteries and chargers for a garage, workshop, shed, job kit, maker space, maintenance closet, or household tool shelf. The deliverable is a charging roster with battery labels, charger locations, rotation status, safe charging reminders, and a closeout routine.

This skill supports ordinary organization and basic fire-safe charging habits only. It does not diagnose electrical faults, repair chargers, rebuild batteries, modify wiring, bypass protection circuits, or replace manufacturer instructions.

## Safety Boundary

Follow manufacturer instructions and use only compatible batteries, chargers, and power sources. If compatibility, condition, odor, heat, swelling, leaking, corrosion, damaged casing, damaged cord, missing label, or charger behavior is uncertain, stop using the item, move it away from combustible materials if safe to do so, and follow the manufacturer, retailer, recycler, or local disposal guidance.

Do not provide electrical repair guidance. Do not instruct users to open chargers, open battery packs, replace cells, solder battery tabs, bypass fuses, defeat thermal protection, modify plugs, repair cords, test live circuits, or improvise adapters. For suspected electrical defects, advise using manufacturer support or a qualified repair professional.

Do not promise that a charging setup is fireproof or risk-free. Keep guidance to basic reminders: use compatible equipment, charge on a stable noncombustible surface when practical, keep away from flammables, avoid unattended long charging where the manufacturer warns against it, unplug or remove batteries when charging is complete if recommended, and store batteries according to the manual.

## Required Inputs

Ask for practical roster details:

- Tool platform or brand family if known.
- Battery labels, voltage, capacity, chemistry if printed, and visible condition.
- Charger model or label and where it is plugged in.
- Battery count and current status: full, charging, used, cool down, inspect, retire, recycle, or unknown.
- Usual work pattern: weekend use, daily use, job kit, emergency tool shelf, shared workshop, or seasonal projects.
- Charging location: garage bench, shelf, cabinet top, utility room, work cart, or temporary station.
- Available label method: tape, marker, number stickers, color dots, case slots, or log sheet.
- Manufacturer instructions the user already has, including storage charge or temperature limits if printed.

If battery or charger compatibility is unknown, mark the item "hold for manual check" rather than charging it.

## Workflow

1. **List equipment.** Record each battery and charger by non-sensitive label, platform, printed voltage, capacity, condition, and location.
2. **Confirm compatibility.** Match batteries only to chargers intended for that battery platform. Mark unknown pairs for manual or manufacturer check.
3. **Inspect visibly.** Look for swelling, cracks, leaking, corrosion, burn marks, melted plastic, damaged cords, missing labels, unusual odor, unusual heat, or error lights.
4. **Assign status.** Use roster statuses: full, charging, used, cool down, inspect, hold for manual check, retire, recycle, or missing.
5. **Set rotation rule.** Choose a simple order such as oldest used first, numbered slots, left-to-right, or full-on-top and used-on-bottom.
6. **Set charging window.** Plan when charging happens, who checks it, and what marks charging complete. Keep it consistent with manufacturer guidance.
7. **Add fire-safe reminders.** Include compatible charger only, stable surface, clear surrounding clutter, no covered chargers, no damaged items, and completion check.
8. **Build the roster.** Produce a printable roster with labels, statuses, charger assignments, location, next action, and closeout routine.

## Basic Fire-Safe Charging Reminders

Include reminders like these without overstating safety:

- Use only the charger and battery combination approved for that platform.
- Charge in a dry, ventilated area on a stable surface.
- Keep chargers and batteries away from paper, sawdust piles, rags, solvents, fuels, aerosol cans, cardboard, upholstery, and other combustibles.
- Do not cover a charger or run it inside a closed bin unless the manufacturer says it is designed for that.
- Let hot batteries cool before charging when the manual or charger indicates it.
- Stop using batteries or chargers with swelling, leaking, burning smell, melted plastic, damaged cords, corrosion, smoke, unusual heat, or repeated error lights.
- Keep battery terminals protected from loose metal parts during storage and transport.
- Follow local rules for recycling or disposal of retired batteries.

## Output Format

Return a tool battery charging roster with these sections:

1. **Scope Note**
   - Organization and basic charging reminders only
   - Follow manufacturer instructions
   - No electrical repair, battery rebuilding, wiring, or charger modification guidance

2. **Battery Roster**
   - Battery label
   - Platform or brand family
   - Printed voltage and capacity if available
   - Current status
   - Visible condition
   - Storage or charging location
   - Next action

3. **Charger Map**
   - Charger label
   - Compatible battery group
   - Current location
   - Plug or outlet area description
   - Clear space reminder
   - Items to keep away

4. **Compatibility Holds**
   - Battery or charger label
   - What is unknown
   - Manual or manufacturer check needed
   - Do not charge until resolved

5. **Charging Rotation Rule**
   - How used batteries enter the queue
   - How full batteries are marked
   - How cool-down or inspect items are separated
   - Who checks completion if relevant

6. **Fire-Safe Charging Reminders**
   - Compatible charger only
   - Stable, dry, ventilated location
   - Keep flammables and clutter away
   - Do not cover chargers
   - Stop using damaged, hot, swollen, leaking, smoking, corroded, or odd-smelling items
   - Follow recycling guidance for retired batteries

7. **Session Closeout**
   - Mark full batteries
   - Remove or unplug according to manufacturer guidance
   - Put used batteries in the queue
   - Separate inspect or retire items
   - Clear sawdust, rags, paper, and clutter near the station
   - Note missing batteries or chargers

8. **Mini Station Card**
   - Active battery count
   - Charger count
   - Queue rule
   - Completion check
   - Hold-for-manual-check rule
   - Next roster review date

## Style Guidelines

- Keep instructions practical and conservative.
- Prefer labels, statuses, and visible-condition checks over technical diagnosis.
- Use "hold for manual check" when compatibility or condition is uncertain.
- Do not mention repair methods, electrical testing steps, or battery rebuilding steps.
- Make the roster printable enough for a wall, bench, cabinet door, or tool chest.

## Example Prompts

Copy and paste one of these to start:

1. **"I have 6 Ryobi 18V batteries and 2 chargers in the garage. Help me make a charging roster so I know which ones are full and which need charging before the weekend."**
2. **"Make a printable battery charging log for my workshop — I want to number the batteries, track charge status, and add a fire-safe closeout checklist."**
3. **"I found a swollen battery in my tool bag. Can you help me mark it for retirement and reorganize the remaining batteries into a rotation system?"**

## Quality Bar

A strong result helps the user know which batteries are full, which are charging, which need inspection, and which are not safe to use. It should make a charging station more orderly while staying within basic fire-safe habits and away from electrical repair guidance.
