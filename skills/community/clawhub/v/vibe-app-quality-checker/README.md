# Vibe App Quality Checker

A Claude skill that checks an AI built app before it goes live.

Ask Claude to check your app, and it goes through a 5 point list,
then gives you a pass/fail report with evidence and fixes. No guessing.
If something cannot be verified, it says so.

## The 5 checks

1. Bottom navigation is clear
2. Save actions feel instant
3. Lists load in pages, not all at once
4. Database calls are not excessive
5. Heavy work runs in the background

It also gives separate quality notes: no AI slop layouts,
consistent number formatting, plain readable labels, and no
placeholder data shown as real.

## Who it is for

People who build apps with AI help, and small business owners
whose app was built that way. Made for simple apps: a few
screens, a database, and real users.

## How to use it

1. Install the skill in Claude (see below).
2. Give Claude your folder of app files, demo link, or a
   description of the app plus code access.
3. Ask: "Check my app with vibe-app-quality-checker."
4. Read the report. Fix the blockers first: a failed save
   that silently loses user work will always block a "Ready"
   verdict.

Some checks need code access, and the skill will list them
separately if you only gave a demo link: for example, counting
database calls per screen cannot be proven from outside.

## How to install it

### In Claude

Paste this repo link into Claude and ask it to install the
`vibe-app-quality-checker` skill. If your version of Claude shows
a different install screen, use the manual method below.

### Manual method (Claude Code and other tools)

Copy the `SKILL.md` file into your skills folder, in a folder
called `vibe-app-quality-checker`, then restart Claude Code.
The skill file itself is just instructions. It collects no data
and sends nothing anywhere.

## What it will not do

- It will not redesign your app.
- It will not invent statistics, user counts, or performance
  numbers.
- It will not mark a check as passed without evidence.
- It will not test with real user data, or submit a real
  payment, unless you say it may.

## Files

- `SKILL.md` - the full skill: instructions, checklist, hard rules,
  and report format.

## License

MIT - free to use and adapt. If you improve it, a credit is
appreciated but not required.
