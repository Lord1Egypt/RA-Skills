---
name: school-locker-setup-map
description: "Create a student locker layout map with zones, supplies, reset routines, photo-checklist prompts, and safety rules that keep valuables and private schedules off visible labels."
version: "1.0.0"
type: prompt-flow
tags:
  - school
  - organization
  - locker
  - student-routine
  - home-admin
author: Golden Bean / coder
---

# School Locker Setup Map

## Purpose

Help a student and caregiver design a locker setup that is simple to use during a busy school day. The deliverable is a locker layout map with zones, supply list, label plan, weekly reset routine, and photo checklist.

This is a prompt-only organization workflow. It does not collect or display valuables, locker combinations, private schedules, health details, addresses, or identifying personal information. Visible labels should be generic and safe if another student sees them.

## Use This Skill When

Use this skill when the user wants to:

- Set up a school locker for a new term, new school, or new routine.
- Plan zones for books, binders, notebooks, sports gear, weather gear, lunch items, and personal care basics.
- Make a supply list for shelves, magnets, bins, hooks, folders, pencil pouch, wipes, and small backup items.
- Create a weekly reset routine so the locker does not become a pile.
- Build a photo checklist the student can compare against after setup.
- Adapt a locker plan for a small locker, shared locker, top locker, bottom locker, or limited passing time.

Do not use this skill to create visible labels containing private schedules, locker combinations, home address, medication details, expensive items, payment cards, electronics, or other valuables.

## Best Inputs

Ask for only what is needed to make the setup practical:

- Locker dimensions or a rough description: tall, narrow, half-size, shared, top, bottom, hooks, shelf, no shelf, magnetic, or non-magnetic.
- School rules about shelves, magnets, stickers, mirrors, locks, food, sprays, decorations, and cleaning supplies.
- Student grade band and independence level.
- Typical items carried: binders, folders, notebooks, textbooks, Chromebook or laptop, lunch, water bottle, sports gear, instrument, coat, umbrella, or art supplies.
- Biggest pain point: forgotten homework, crushed papers, late to class, clutter, lost supplies, heavy backpack, wet gear, or messy lunch items.
- Passing time constraints and how often the student can visit the locker.
- Label style: icons, colors, initials, numbers, or plain words.

If exact dimensions are missing, make a flexible plan with adjustable zones.

## Workflow

1. **Set privacy and safety rules first.** No visible labels for valuables, private schedules, locker combinations, addresses, phone numbers, medical details, or expensive electronics.
2. **Capture constraints.** Note dimensions, shelf access, hooks, magnetic surfaces, school rules, shared use, and passing time.
3. **Inventory items.** Sort items into daily carry, locker storage, occasional items, wet or dirty items, lunch items, paper flow, and emergency basics allowed by school rules.
4. **Design zones.** Map top, middle, bottom, door, hooks, and bins. Keep heavy books low, frequently used items easy to reach, and loose papers in a clear intake spot.
5. **Choose supplies.** Recommend only practical supplies that fit the constraints. Avoid overdecorating or adding bulky organizers that reduce usable space.
6. **Create safe labels.** Use generic labels such as `Math`, `ELA`, `Science`, `Inbox`, `Return`, `Lunch`, `Gym`, `Weather`, and `Reset`. Use icons or colors for younger students.
7. **Plan the paper flow.** Add one place for papers coming in, one place for completed work going out, and one weekly cleanup step.
8. **Build routines.** Create a morning load, mid-day swap, end-of-day pack, and weekly reset routine based on passing time.
9. **Add a photo checklist.** Tell the user what photos to take for reference without showing private information.
10. **Deliver the map.** Return a layout and reset plan that the student can use without adult micromanagement.

## Output Format

Return the artifact in this order:

### 1. Locker Snapshot

| Field | Detail |
|---|---|
| Student grade band | |
| Locker type or size | |
| School rules noted | |
| Main pain point | |
| Passing time constraint | |
| Privacy rule applied | |
| Assumptions | |

### 2. Locker Layout Map

| Zone | Location | What goes there | Container or tool | Label text | Reset cue |
|---|---|---|---|---|---|
| Top | | | | | |
| Middle | | | | | |
| Bottom | | | | | |
| Door | | | | | |
| Hook | | | | | |
| Paper flow | | | | | |

### 3. Supply List

Group supplies as:

- Must-have:
- Nice-to-have:
- Skip unless school allows:
- Do not store visibly:

### 4. Daily Operating Routine

Include:

- Morning load:
- Between-class swap:
- Lunch or activity handling:
- End-of-day pack:
- Weekly reset:

### 5. Photo Checklist

Include safe photo prompts:

- Empty locker before setup.
- Final layout with only generic labels visible.
- Close-up of paper flow area.
- Supply bin or pouch layout.
- Do not photograph locker combination, private schedule, student ID, address, payment cards, or valuable items.

### 6. Troubleshooting

Provide fixes for:

- Backpack stays too heavy.
- Papers get crushed.
- Student is late during passing time.
- Lunch items leak or smell.
- Sports gear is bulky or wet.
- Locker becomes messy by midweek.

## Example Prompts

- "Set up my locker for grade 8. It's narrow with one shelf and two hooks. I keep crushing my papers and my backpack is heavy."
- "Help me redesign my middle school locker — biggest problem is I can't find anything between classes."
- "Give me a locker layout for a shared half-locker. We both have binders and lunch bags and only two minutes passing time."

## Message Style

- Keep it encouraging and student-friendly.
- Make the system simple enough to maintain.
- Prefer clear zones over lots of products.
- Use safe generic labels.
- Avoid shame about mess; design for reset.

## Safety Boundary

Do not put valuables or private schedules in visible labels. Do not ask for locker combinations, home addresses, student IDs, medication details, exact daily route, or other sensitive information. If the user provides sensitive details, omit them from the visible map and replace them with generic placeholders.
