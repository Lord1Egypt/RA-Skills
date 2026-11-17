# Current Acxiom and LiveRamp careers rows

Dependency-free Node22 recipe for the two public boards in
[Firecrawl3552](https://github.com/firecrawl/firecrawl/issues/3552).
It returns title, location (or null), URL, source, fetch time and coverage.
No API key, Firecrawl credit, browser or wallet is required.

Save boards.mjs and boards.public.test.mjs beside this README:

```sh
node --test boards.public.test.mjs
node boards.mjs --stdout > careers.json
```

The fetch uses at most six requests per attempt, each with a15-second timeout.
Acxiom pagination is bounded to four pages. A successful process exit means
the observation was obtained, not that every board is complete. Inspect each
`coverage.status`, its missing fields and remaining count.

## What changed

LiveRamp's primary careers link is now the Ashby board, whereas the July issue
comment used Workday. The old Workday jobs request returned403 in the
October7 study. That is a source failure, not an empty board.
The [official Ashby posting API](https://developers.ashbyhq.com/docs/public-job-posting-api)
already supplies the required fields; no rendering model is needed for this route.

Acxiom's offset-zero total is the starting declaration. Later pages sometimes
return total0 with valid jobs; a past-end request can repeat the first page.
The recipe deduplicates posting paths and does not use either behavior as
proof that the board is empty. Missing-field rows remain explicit.

The independently received October7,16:15UTC cut has Acxiom37 usable rows
against declared38, with an unreadable JR014229 row also present in the
past-end probe. It is `partial_past_end_incomplete`, not complete.
LiveRamp Ashby has55 unique listed rows in that returned array, no separate
total. The old Workday source remains403. The separate cold standalone run at16:19UTC then returns37/37 Acxiom rows
with the missing stub removed, while Ashby remains55 and old Workday403.
Counts can change immediately; neither snapshot overwrites the other.

This is a full-board recipe, not a role-filtered answer to the original issue.
The source's Account Executive / Advertising Solutions Engineer wording does
not establish an exact Boolean title predicate. Choose that separately rather
than silently presenting every role as a match. The script sends no applicants,
credentials or private data and performs no purchase.

## Try it on a real task

If this helps your existing careers workflow, report which rows or coverage
you used and what remains missing. If you need a different public board or a
repeat refresh, describe the input and useful-output condition in the original
issue, or use SameDayDesk's free task-help entry:
https://samedaydesk.com/api/correspondence/v1/visitor-entry

No reward or paid execution is required to ask. This first source-compatible
trial is free; it does not promise maintenance of arbitrary sites. We will
scope any separate recurring work with the requester before offering it.
