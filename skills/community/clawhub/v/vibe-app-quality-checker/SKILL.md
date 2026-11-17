---
name: vibe-app-quality-checker
description: Check an AI built app for 5 common quality problems before launch. Use when a user asks to review, audit, or check an app built with AI, or asks why an app feels slow, confusing, or crashy. Give it a folder of app files, a demo link, or a description of the app and it returns a pass/fail report with evidence and fixes.
---

# Vibe App Quality Checker

## Purpose

Check an AI built app before it goes live, so the common problems
that make apps feel cheap or break under real use are caught early.
The checker does not redesign the app. It checks quality, reports
what fails, and says exactly what to fix.

It is made for small apps built with AI help: a few screens,
a database, and real users who expect the app to work first time.

## How to use it

1. Ask the user for one of these:
   - A folder of app files
   - A demo or staging link
   - A description of the app, plus access to the code
2. If the user gives only a demo link, say clearly what cannot be
   checked from outside. Do not guess those items. Mark them
   "Needs code access" instead of Pass.
3. Check every item in the checklist below, in order.
4. For each item, record evidence: the screen, file, function,
   or observed behaviour where you saw it. No evidence means
   no Pass.
5. Finish with the report format at the end of this file.

## The 5 point quality checklist

Check all 5. Do not skip one because it looks small.

### 1. Bottom navigation is clear
- The bottom bar holds only the obvious, everyday actions.
- Everything else lives in a top menu with text labels, not
  mystery icons the user has to guess.
- Fail if the bottom bar is crowded with icons, or if key
  actions hide behind icons with no labels.
- How to check: open the app, count the bottom icons, tap
  each one, and note which ones are unclear. In code, find
  the bottom navigation component.

### 2. Save actions feel instant
- When the user taps save, add, or submit, the screen updates
  at once, before the database confirms.
- If the save later fails, the app says so plainly and puts
  the old value back, or offers a retry. It never silently
  loses the user's change.
- Fail if the user waits on a spinner for every save with no
  instant feedback, or if a failed save loses their work
  silently.
- How to check: try a save, ideally on a slow connection,
  and read the save handler code to see what happens on
  failure.

### 3. Lists load in pages, not all at once
- Lists load a page at a time, for example 20 items, and load
  more on scroll or on tap.
- Fail if opening a list loads the full dataset every time,
  especially when the data will keep growing.
- How to check: watch the data calls when opening a list,
  and read the list query code for a limit or page size.

### 4. Database calls are not excessive
- Each screen makes a small number of planned database calls,
  not one call per item or per small piece of data.
- Fail if a single screen fires dozens of direct database
  calls, or if the same data is fetched again and again on
  every screen change. This is what overloads the database
  and crashes the app under real users.
- How to check: count the calls per screen in code or in
  network logs, and look for loops that call the database
  once per row.

### 5. Heavy work runs in the background
- Heavy tasks, for example image processing, large file work,
  big calculations, or sending many messages, run as
  background jobs, not on the main thread the user is
  waiting on.
- The user can keep using the app while the job runs, and
  gets told when it finishes.
- Fail if a heavy task freezes the screen, or if the user
  must wait for it before doing anything else.
- How to check: trigger a heavy task and see if the screen
  stays responsive, and read the code for background job
  or worker usage.

## Extra quality notes

These are not part of the 5 points above, but report them
separately as "Quality notes". Do not mix them into the
5 point score.

- No AI slop: no purple gradients, no generic layout
  repeated on every screen, no placeholder look.
- Numbers are consistent app wide: one format, one size
  system. Do not mix "AED 500", "500 AED", and "500"
  for the same kind of price.
- Key information is easy for a weak English reader:
  short simple sentences, clear labels, and help or
  contact details that are easy to find.
- No placeholder data shown as real. Demo data must be
  labeled as demo, on screen.

## Hard rules

- Never mark Pass without evidence.
- Never invent a statistic, a user count, or a performance
  number.
- Never say an app is ready if a failed save loses user
  work silently. That is a blocker.
- Never test with real user data, and never submit a real
  payment, unless the user says you may. Check the code
  or a demo instead.
- Never use a placeholder to fill a gap. Report the gap.
- Keep the report in plain, short sentences. The owner
  may not be a technical reader.

## Report format

Always finish with this format, in this order:

### Quality report: [app name]

**Verdict: Ready / Not ready / Not ready - blockers found**

Use "Ready" only if there is no Fail, or if the only
open items are owner steps the client has confirmed they
will do on launch day. "Not applicable" does not by itself
block a Ready verdict, but list it as a gap. Otherwise use
"Not ready".

**Results**

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Bottom navigation is clear | Pass / Fail / Needs code access / Not applicable | screen or file |
| 2 | Save actions feel instant | ... | ... |
| 3 | Lists load in pages | ... | ... |
| 4 | Database calls are not excessive | ... | ... |
| 5 | Heavy work runs in the background | ... | ... |

**Fixes, in priority order**

1. Blocker first: [what to fix, on which screen, in plain words]
2. Next fix: ...
3. ...

**Owner steps - needs the client**

- [For example: give code access so database calls can be counted]
- [For example: confirm which screens real users use most]

**Quality notes**

- [Any note from the Extra quality notes section, or "None".]

**What was not checked, and why**

- [For example: database call counts could not be verified from a demo link alone.]
