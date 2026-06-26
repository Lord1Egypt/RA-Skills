# Troubleshooting

## OpenSubtitlesComError: Bad Request
- Symptom: list/search intermittently fails.
- Action: retry with lower frequency; keep OpenSubtitles fallback enabled.

## dogpile.cache.exception.RegionNotConfigured
- Symptom: download stage fails after listing many candidates.
- Action: treat as provider instability; continue fallback chain.

## HTTP 429 / rate limit
- Symptom: provider returns 429 or timeouts.
- Action: add wait between files, reduce concurrency, process in smaller batches.

## Folder enter failure (special chars)
- Symptom: cannot open folder by name.
- Action: use `fid`-based enter instead of name-only navigation.

## Rollback delete returns 401 guest
- Symptom: file delete API denied.
- Action: manual web delete or authenticated headed session.

## Preventing false success
- Symptom: many files marked ok but subtitle content identical.
- Action: hash check + content spot check; rollback bad batch.
