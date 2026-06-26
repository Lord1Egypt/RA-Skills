# PARA Workflows

## 1) Weekly Inbox Processing

Time estimate: 15 minutes for ~20 items.

Steps:
1. Open `00_INBOX` and process items one by one.
2. Apply the three questions (Project, Area, Resource).
3. Move item to the first matching destination.
4. If no destination exists, decide whether to create a new folder (only if recurring and meaningful).
5. Empty inbox to zero.

Walkthrough:
- Item: "Vendor quotes for office move" -> Active project `Office Move July`.
- Item: "Manager coaching notes template" -> Area `People Management`.
- Item: "Article: Async communication patterns" -> Resource `Communication`.

## 2) Monthly Review

Time estimate: 30-60 minutes.

Steps:
1. Review all `10_PROJECTS/Active` projects for status and relevance.
2. Flag projects with no activity in 30+ days.
3. Decide for each stale project: archive, activate, or delete.
4. Review Areas for standard drift and needed updates.
5. Move completed projects to archive and capture outcomes.

Walkthrough:
- `Website Migration` inactive 42 days, status marked complete -> archive.
- `Hiring Backend` inactive 35 days, still needed -> activate with next actions.

## 3) New Project Setup

Time estimate: 10 minutes.

Template structure (all markdown files):
- `AGENTS.md` - project outcome, timeline, ownership, and operating guidance
- `Tasks.md` - executable task list
- `Notes.md` - working notes, decisions, and references

Steps:
1. Create project folder in `10_PROJECTS/Active/`.
2. Add `AGENTS.md`, `Tasks.md`, and `Notes.md`.
3. Define desired outcome and due date/timeline in `AGENTS.md`.
4. Add first action items to `Tasks.md`.

Walkthrough:
- Project: `Q2 Webinar Launch`
- Create files, define outcome (launch by May 30), add kickoff tasks.

## 4) Project Completion and Close-Out

Time estimate: 10-15 minutes.

Required completion summary fields:
- Outcome
- What worked
- What didn't
- Reusable assets

Steps:
1. Confirm deliverable is complete.
2. Create completion summary using the required fields.
3. Extract reusable assets to Resources if applicable.
4. Mark project complete.
5. Move project to `40_ARCHIVE/Projects/`.

Walkthrough:
- Project: `Customer Onboarding Rewrite`
- Outcome: onboarding completion rate improved 11%.
- Reusable assets: onboarding checklist and interview guide moved to Resources.

## 5) Archiving

Time estimate: 5-10 minutes per project.

Steps:
1. Verify project is complete or intentionally retired.
2. Ensure completion summary exists.
3. Move project folder to `40_ARCHIVE/Projects/`.
4. Preserve original file structure.
5. Add archive date in project metadata.

Walkthrough:
- `Q1 Planning` moved to archive after retrospective and summary capture.
