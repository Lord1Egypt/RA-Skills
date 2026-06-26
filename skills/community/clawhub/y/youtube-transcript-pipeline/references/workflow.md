# Workflow Reference

## Speaker correction strategy

1. Identify anchor segment in the first 30s using reliable word-level speaker IDs.
2. Force intro mapping if needed (e.g., opening questioner lines).
3. Apply short/interjection heuristic:
   - keep very short lines like short questions as interviewer
   - avoid flipping long explanatory turns unless strongly matched
4. Keep a count audit:
   - total lines unchanged
   - speaker totals changed only slightly and intentionally

## Translation strategy

- Keep input/output line granularity: one input line -> one translated line
- Parse strict pattern: `[HH:MM:SS] Speaker: text`
- If JSON API returns malformed rows, keep source for that line and retry.
- Use retries and final row-count checks.

## Packaging strategy

- Use deterministic naming convention: `yt_<video_id>_YYYY-MM-DD`
- Include:
  - final reviewed transcript (txt/json)
  - translated version
  - thumbnail(s)
  - short boss-ready summaries (30s/1min)
  - manifest
- Optionally initialize git and commit for handoff traceability.
