---
name: socialkit-content-calendar
description: Plans and publishes social posts across platforms from one calendar file, reporting which posts are scheduled, due, waiting for approval or already published, and publishing approved posts when they are due. Use when the user wants a posting schedule, content calendar, or to publish queued posts at set times.
license: MIT
metadata:
  author: Ahmad Hussain
  requires: socialkit-social-core
---

# Content calendar

Each calendar entry points at a post folder (made by a platform posting skill or by
socialkit-content-repurpose) and a publish time. The calendar never approves anything: every post
still needs the user's own approval through the socialkit-social-core post script.

## Steps

1. Create `calendar.json` from [the example](assets/calendar.example.json) with entries
   `{ "dir": "<post folder>", "publishAt": "<ISO 8601 with offset>" }`.
2. Check: `node scripts/calendar.mjs --status --file calendar.json`. Report entries that
   are invalid or need approval, and ask the user to approve those they want.
3. Preview what is due: `node scripts/calendar.mjs --publish-due --dry-run --file calendar.json`
4. Publish due posts: `node scripts/calendar.mjs --publish-due --file calendar.json`.
   For hands-off publishing the user can run this command from cron every 15 minutes.

## Output contract

A status table per entry (platform, kind, publish time, status, problems) and, after
publishing, the result or error per entry.

## Failure handling

- `needs-approval`: list the problems (changed files or no approval) and ask the user.
- One entry failing does not stop the others; report each failure with its hint.
- Instagram and Threads have no API scheduling: they publish when `--publish-due` runs
  after their time, so the command must actually be run.
