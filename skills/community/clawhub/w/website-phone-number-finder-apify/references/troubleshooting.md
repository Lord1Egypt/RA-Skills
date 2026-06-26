# Troubleshooting

## No phone rows returned

Check:

- `resultMode` is `phonesOnly` when phone leads are required
- `extractPhones` is enabled
- submitted domains are live and reachable
- `maxResults` is greater than `0`
- `maxTotalChargeUsd` is high enough for the requested saved results
- `maxPagesPerWebsite` is high enough for sites that hide phones on locations, booking, staff, legal, imprint, or contact pages

Some websites publish only contact forms, booking widgets, or social profiles instead of direct phone numbers.

## Fewer rows than requested

This can happen when the submitted websites have fewer public phone numbers, when `phonesOnly` filters out no-phone websites, or when the run budget is reached. Inspect `RUN_SUMMARY`.

## Optional emails are missing

If `extractEmails=false`, emails are intentionally not extracted. If `includePersonalData=false`, person-like emails are filtered when optional email extraction is enabled.

## Results include social links but no phone

This is expected in `contactsOnly` or `allWebsites`. Use `phonesOnly` when the dataset should contain only phone lead rows.

## Budget stopped early

The actor respects Apify `maxTotalChargeUsd`. The script passes this as `--budget-usd`. Check `RUN_SUMMARY.chargeLimitReached`.

## Website-level errors

The actor is designed to suppress individual website errors into `RUN_SUMMARY` and finish successfully where possible. Inspect `RUN_SUMMARY` before rerunning.
