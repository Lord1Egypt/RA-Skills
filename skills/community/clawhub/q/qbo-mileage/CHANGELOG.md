# Changelog

## 1.0.1 — 2026-06-10

### Fixed (tax correctness)
- **Chain legs now belong to the destination event.** Intermediate legs in a
  trip chain previously inherited the date, purpose, vehicle, and
  BUSINESS/PERSONAL type of the event being *left*, not the event being
  *driven to*. A personal stop between two business stops inverted the
  classification of both surrounding legs: the drive to the personal stop was
  exported as BUSINESS (overstating the deduction) and the drive from the
  personal stop to the next job site was exported as PERSONAL (losing a
  legitimate deduction). (`trip_builder.py`)
- **PERSONAL legs now export a 0.00 deduction** instead of `miles × IRS rate`,
  so the CSV and run report never overstate the deductible total.
  (`pipeline.py`)

### Fixed (reliability)
- A corrupt or half-written distance cache no longer crashes every run; the
  cache is rebuilt with a warning. Cache writes are now atomic
  (temp file + rename). (`cache.py`)
- Monthly cron script no longer computes the wrong month when run on the
  29th–31st (GNU date "last month" normalization bug); also falls back to
  `python3` when `python` is not on PATH. (`scripts/run_monthly.sh`)
- The skill entry point now adds the plugin's `src/` folder to `sys.path`,
  so it runs from a freshly installed plugin without `pip install`.
  (`skills/qbo-mileage/scripts/run.py`)
- Missing IRS rate for the requested year now fails fast before any source
  API calls are spent. (`pipeline.py`)

### Security
- SMTP STARTTLS now uses an explicit `ssl.create_default_context()` so the
  server certificate is always verified regardless of Python version
  defaults. (`senders/email.py`)

### Docs
- SKILL.md documents the `python3` fallback and the no-install entry point,
  and adds a PERSONAL-deduction check to the review checklist.

### Tests
- Regression tests for chain-leg attribution (mixed business/personal chains)
  and zero deduction on personal legs.
