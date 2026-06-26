# Troubleshooting

## No email rows returned

Check:

- `resultMode` is `emailsOnly` when email leads are required
- submitted domains are live and reachable
- `maxResults` is greater than `0`
- `maxTotalChargeUsd` is high enough for the requested saved results
- `maxPagesPerWebsite` is high enough for sites that hide contacts on team, staff, legal, imprint, or contact pages

Some websites publish only contact forms, booking widgets, or social profiles instead of direct emails.

## Fewer rows than requested

This can happen when the submitted websites have fewer public contacts, when `emailsOnly` filters out no-email websites, or when the run budget is reached. Inspect `RUN_SUMMARY`.

## Personal emails are missing

If `includePersonalData=false`, person-like emails and personal LinkedIn profile URLs are intentionally excluded. If it is true, the website still may not publish personal contacts.

## Results include phones or social links but no email

This is expected in `contactsOnly` or `allWebsites`. Use `emailsOnly` when the dataset should contain only email lead rows.

## Budget stopped early

The actor respects Apify `maxTotalChargeUsd`. The script passes this as `--budget-usd`. Check `RUN_SUMMARY.chargeLimitReached`.

## Website-level errors

The actor is designed to suppress individual website errors into `RUN_SUMMARY` and finish successfully where possible. Inspect `RUN_SUMMARY` before rerunning.
