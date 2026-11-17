# Changelog

## Version gap — read this before trusting `_meta.json`

`_meta.json` is a **publication record**, not a source version stamp. It says
`1.0.0` because **1.0.0 is what ClawHub actually serves**.

Everything below 1.2.2 existed in the source tree only. If you installed this
skill from ClawHub, or read it from
`~/.openclaw/workspace/skills/ultimate-skills-finder/`, you had **1.0.0**,
which:

- built install commands by string interpolation (`f"clawhub install {slug}"`)
  from registry-controlled names;
- had **no `--share-urls` consent gate** — `--scan` disclosed without asking;
- parsed the scan response with `data.get("status") == "done"`, a key no live
  response carries, so every scan silently returned nothing.

`_meta.json` is only bumped by publishing. It is left alone by hand.

## 1.2.2 — review-driven hardening

Two independent reviews of the 1.2.1 source. Confirmed findings, each fixed
with a failing test first.

### Security

- **Terminal escape injection.** Registry `name` and `summary` reached the
  terminal raw. A description of `\x1b[1;31mSAFE (advisory)\x1b[0m …` could
  forge a scan verdict or install instruction; an OSC-52 sequence could write
  to the clipboard. `sanitize_text()` now strips C0/C1, bidi overrides and
  zero-width joiners.
- **Unvalidated URL disclosure.** The markdown-link gate accepted
  `skills://evil/x` because the *scheme* contained the substring `skill`.
  `is_disclosable_url()` now permits only `http(s)` with a host, and is
  applied at result construction.
- **Description/URL hijack.** `merge()` took the *longest* description, so a
  hostile browse-only entry could displace the registry's own summary and
  supply the URL later scanned. A structured source now outranks a browse-only
  index.

### Correctness

- **Dedup collapsed distinct skills.** Substring containment merged
  `mail`/`email` and `sql`/`mysql`, and composed transitively: `pdf`,
  `pdf-editor`, `pdf-editor-pro`, `pdf-editor-pro-max` became one result that
  then inherited all four sources, inflating its own breadth score. Matching
  now requires normalised equality, else token-prefix alignment plus a 0.90
  similarity floor.
- **The test suite skipped 21 of its own tests.** `unittest.main()` sat
  mid-file, so `python3 tests/test_find_skill.py` ran 40 of 61 and skipped the
  entire scan-parsing half. It is now the last statement in the file; both
  invocations run the full suite.
- **`--limit 0` / `-1` looked like an empty registry.** Now rejected with
  exit 2.
- **Failed sources were invisible.** `gather(return_exceptions=True)`
  discarded every exception, so a registry returning malformed JSON made a
  source vanish into a confident "No skills found". Failures are now named on
  stderr with their cause.
- **The event loop froze during scans.** The scan POST called blocking
  `urlopen` inside the coroutine while the GET helpers correctly used
  `asyncio.to_thread`. Worst heartbeat gap: **1200 ms → 11 ms**.
- **Scan reasons were discarded.** SKILL.md instructed the agent to read "the
  reasons" before installing; they were read off the wire and thrown away, so
  the instruction was impossible to follow in exactly the `HIGH`/`CRITICAL`
  case. Now captured, sanitised, displayed, and emitted as `security_reasons`
  in `--json`.
- **Network reads were unbounded.** Now capped at `MAX_RESPONSE_BYTES`.
- The semaphore no longer holds a slot during the throttle sleep.

### Documentation

- **A false privacy claim.** `references/sources.md` stated the scan was "the
  only part of the tool that sends data to a third party". Every search
  already sends the raw query to ClawHub, skills.sh, SkillsMP and GitHub with
  no consent flag. Corrected, and SKILL.md rule 4 now says so *before* the
  user searches.
- Unverified severities (`LOW`, `HIGH`, `CRITICAL`) are no longer presented as
  fact; only `SAFE` and `MEDIUM` have been observed live.
- Test-count claim corrected: 40 → 91 tests, 27 hostile identifier forms.
- Added the missing Python 3.9+ floor, the `upstreamScanners` limitation, and
  the corrected identifier-allowlist length cap.
- Removed five throwaway dev probes that would have shipped.

## 1.2.0 / 1.2.1 — source only, never published

- The scan parser was rewritten after live probing revealed the response
  carries `severity` and **no** `status` field, and that errors arrive at
  **HTTP 200** with `status: "error"`.
- `normalize_scan_url()` was added: the scanner parses exactly two path
  segments, so ClawHub's repo-style URLs (`/owner/skills/name`) were being
  read as the skill name `skills` and reported "not found" for every skill
  under such a path. Verified live — the raw form 404s, the normalised form
  returns a verdict.