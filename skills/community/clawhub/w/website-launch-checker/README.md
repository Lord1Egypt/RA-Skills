# Website Launch Checker

A Claude skill that checks a small business website before it goes live.

Ask Claude to check your site, and it goes through a 15-point list,
then gives you a pass/fail report with evidence and fixes. No guessing.
If something cannot be verified, it says so.

## The 15 checks

1. Custom 404 page
2. Unique page titles
3. Meta descriptions
4. Social preview images
5. Image alt text
6. Internal links
7. Sitemap and Google Search Console
8. robots.txt
9. HTTPS everywhere
10. Spam protection on forms
11. Thank-you page after submit
12. Google Analytics
13. Privacy policy, with a cookie note
14. FAQ
15. Only real testimonials

It also gives separate design notes: no AI slop layouts, consistent
number formatting, and plain, readable information.

## Who it is for

Small business owners and the people who build their websites.
Made for simple sites: a few pages, a contact or lead form, and
visitors who may read English as a second language.

## How to use it

1. Install the skill in Claude (see below).
2. Give Claude your site URL, demo link, or folder of site files.
3. Ask: "Check my website with website-launch-checker."
4. Read the report. Fix the blockers first: fake testimonials,
   a form with no spam protection, or a form with no thank-you
   confirmation will always block a "Ready" verdict.

Two steps need the site owner, and the skill will list them
separately: Google Search Console and Google Analytics need the
owner's Google account, and testimonials need to be confirmed
as real, with permission to show them.

## How to install it

### In Claude

Paste this repo link into Claude and ask it to install the
`website-launch-checker` skill. If your version of Claude shows
a different install screen, use the manual method below.

### Manual method (Claude Code and other tools)

Copy the `SKILL.md` file into your skills folder, in a folder
called `website-launch-checker`, then restart Claude Code.
The skill file itself is just instructions. It collects no data
and sends nothing anywhere.

## What it will not do

- It will not redesign your site.
- It will not invent testimonials, statistics, or reviews.
- It will not mark a check as passed without evidence.
- It will not submit a real form unless you say it may.

## Files

- `SKILL.md` - the full skill: instructions, checklist, hard rules,
  and report format.

## License

MIT - free to use and adapt. If you improve it, a credit is
appreciated but not required.
