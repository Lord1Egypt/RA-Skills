---
name: small-electronics-recycling-prep
displayName: "Small Electronics Recycling Prep Card"
version: "1.0.0"
description: "Create a sort list and prep checklist for safely bundling small electronics for recycling, with reminders to remove personal data without handling credentials or promising data recovery."
triggerKeywords:
  - electronics recycling prep checklist
  - small gadget recycling
  - recycle old electronics
  - device wipe checklist
  - old cables and chargers sort
  - battery removal reminder
  - e-waste drop off prep
  - electronics drawer cleanup
tags:
  - recycling
  - electronics
  - home-admin
  - decluttering
  - checklist
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Small Electronics Recycling Prep Card

## Purpose

Use this prompt-only skill when a user has a drawer, box, or shelf of small electronics and wants to prepare them for a recycling drop-off, mail-back box, repair charity, or local e-waste collection. The deliverable is a sort list plus a wipe, remove, battery, accessory, and packing checklist.

This skill helps with household organization and safe handoff preparation. It does not handle passwords, credential recovery, forensic data removal, data recovery, resale valuation, repair diagnostics, hazardous-material handling, or official recycler compliance.

## Safety Boundary

Do not ask for or store passwords, PINs, recovery keys, two-factor codes, account names, device unlock patterns, private files, serial numbers tied to an account, or photos of sensitive screens.

Do not promise secure erasure, certified destruction, data recovery, account removal, ownership verification, trade-in approval, or recycler acceptance. Recommend that the user follow manufacturer instructions and the recycler's published rules. If the device contains sensitive work, school, legal, medical, financial, or identity data, recommend using the user's organization-approved process or a qualified professional service.

Do not instruct the user to puncture, crush, open swollen batteries, disassemble sealed batteries, or bypass device locks. For swollen, hot, leaking, damaged, or smoking batteries, tell the user to stop handling the item and follow local hazardous waste guidance.

## Required Inputs

Ask only for practical sorting details:

- Device types, such as phones, tablets, cameras, headphones, smart watches, remotes, cables, chargers, mice, keyboards, drives, or small speakers.
- Approximate count of each type.
- Whether each item may contain personal data.
- Whether the user can access the device normally, without asking for credentials.
- Known battery type or whether batteries are removable.
- Accessories that should stay with each item.
- Intended destination, such as municipal drop-off, retailer bin, charity, mail-back, or unknown.
- Recycler rules the user already has, if any.
- Carrying container, transport limit, and desired drop-off date.

If the user is unsure, mark the item as "confirm recycler rule" or "data removal needed" rather than guessing.

## Workflow

1. **Inventory the pile.** Group items by device type and note approximate counts.
2. **Separate data-bearing devices.** Mark phones, tablets, laptops, drives, cameras, memory cards, smart watches, game devices, and any item that may store personal data.
3. **Create a data-removal reminder.** Tell the user to back up what they need, sign out or remove accounts using official instructions, and factory reset where appropriate, without asking for credentials.
4. **Sort batteries and hazards.** Identify removable batteries, rechargeable items, button cells, and any damaged, hot, swollen, leaking, or questionable items.
5. **Match accessories.** Bundle chargers, cables, adapters, cases, styluses, remotes, and manuals only when they help the recycler, donation recipient, or reuse path.
6. **Check destination rules.** Flag items that may need a special bin, tape on battery terminals, separate bag, mail-back label, or municipal hazardous waste handling.
7. **Pack the bundle.** Create bag or box labels by category and add a carry-ready checklist.
8. **Create a final drop-off card.** Summarize where the items go, what is ready, what is held back, and what must be confirmed.

## Sorting Categories

Use categories that fit the user's items:

- Ready to recycle: no personal data, no damaged battery, destination accepts it.
- Needs data removal first: storage-capable device or memory card.
- Needs battery rule check: lithium battery, rechargeable pack, button cell, or removable battery.
- Keep with accessory: charger, cable, case, dock, stylus, remote, or adapter.
- Donate or reuse candidate: working item with data removed and accessories matched.
- Hold for special handling: swollen battery, damaged item, leaking item, or unknown hazard.
- Do not place in regular trash unless local rules explicitly allow it.

## Output Format

Return a one-page electronics recycling prep card with these sections:

1. **Pile Snapshot**
   - Location of pile
   - Target drop-off or mail-back option
   - Desired ready date
   - Carrying container
2. **Sort List**
   - Device or item type
   - Count
   - Likely data-bearing? yes/no/unsure
   - Battery concern? yes/no/unsure
   - Destination status
3. **Data Removal Reminders**
   - Back up needed files
   - Remove memory cards and SIM cards if present
   - Sign out or remove accounts using official instructions
   - Factory reset when appropriate
   - Do not share passwords or recovery codes
4. **Battery and Safety Check**
   - Remove loose batteries if rules require
   - Tape terminals if recycler rules require
   - Keep damaged or swollen batteries out of the normal bundle
   - Confirm local hazardous waste guidance for problem batteries
5. **Accessory Match**
   - Device
   - Matching charger or cable
   - Case or adapter
   - Bundle note
6. **Pack Map**
   - Bag or box A
   - Bag or box B
   - Hold-back pile
   - Label text
7. **Confirm Before Drop-Off**
   - Open question
   - Where to check
   - Deadline
8. **Carry-Out Checklist**
   - Data-bearing devices reset or held back
   - Memory cards removed or handled
   - Batteries checked
   - Destination rules reviewed
   - Boxes labeled

## Quality Bar

A strong card turns clutter into a ready-to-carry bundle while protecting the user's privacy. It should clearly separate recyclable items from data-bearing, battery-sensitive, and special-handling items without asking for credentials or promising data recovery, secure destruction, or recycler acceptance.

## Example Prompts

- "Sort this drawer of old phones, cables, and remotes into a recycling prep list."
- "What do I need to wipe and remove before dropping off my old electronics?"
- "Build a pack-and-carry checklist for e-waste recycling day."
