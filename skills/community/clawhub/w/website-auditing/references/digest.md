# The digest

One Slack post a week, after the scans are recorded and the pull request is open.

```text
:robot_face: *Website audit: <ISO week>*
*<our domain>*: <score>/100 (<grade>), <+n | -n | no change | baseline> since last week. <Ora report link>
• Fixed: <check names, or "nothing">
• Newly failing: <check names, or "nothing">
*Competitors*
• <domain>: <score> (<grade>), <change>
*Where a competitor is ahead*
• <check name>: passes at <competitor domains>
*Fix pull request*: <link, or "none this week" and why>
*To do by hand*
• <check name>: <Ora's recommendation, one line>
```

## Rules for each line

- **Every number is Ora's.** Score, grade and check status come from this week's result; the change
  is against last week's `website_audits` row. The first week is the baseline and lists no change.
- **Check names, not ids**, and Ora's words for each recommendation. A reader acts on "Markdown
  link alternate", not on `markdown-link-alternate`.
- **Where a competitor is ahead** lists checks failing for us that a competitor passes in this
  week's scan. A check that does not apply to them is not a pass.
- **To do by hand** is at most three fixes from our topFixes that no change to the site's source can
  make: brand search, registry and directory listings, Wikipedia, packages, an API or an MCP server.
- **A partial or skipped scan says so** on its domain's line. Silence reads as a clean week.
- **An unreached site says so instead of a score.** When the bare domain does not land on the site,
  our line reads "Ora cannot reach the site: https://<bare domain> ends at <where it ended>", and
  the one to-do is to serve the site there or redirect it with a 301 or 308. No scan, no comparison
  and no pull request.
- A section with nothing in it is left out, except the first line.
