---
name: safeharbor-check
description: Check a structured CSV against the HIPAA Safe Harbor identifier classes in 45 CFR 164.514(b)(2) — dates more precise than a year, ZIP codes longer than three digits, ages over 89, and columns holding names, phone numbers, SSNs, emails, URLs, IP addresses and the other classes (A) to (R). Use when asked to check a CSV for Safe Harbor identifiers, scan a dataset for HIPAA identifiers before sharing, or apply the mechanical Safe Harbor fixes (dates to year, ZIP to three digits, ages over 89 to 90+) to declared columns. Not for eGFR calculation (use egfr-batch), lab-unit conversion (use labunits), growth z-scores (use growthz), or randomisation lists (use blockrandom). A checker, not a certification; not legal advice.
license: MIT
compatibility: Requires Python 3.10+, standard library only, no dependencies. Installing needs network access to GitHub; the tool itself runs fully offline.
---

# safeharbor-check

## What this tool does

safeharbor-check checks a structured CSV against the 18 HIPAA Safe
Harbor identifier classes, (A)–(R), in 45 CFR 164.514(b)(2). `check`
reports per-class results: violations it can detect mechanically, and
— in the same report, every time — what cannot be verified
mechanically, marked CANNOT VERIFY and never reported as passing.
`apply` performs the rule's three mechanical fixes on columns you
declare, and nothing else. A checker, not a certifying tool.

## Install

```bash
pip install git+https://github.com/RakTikoo/safeharbor-check
```

This provides the `safeharbor-check` command.

## Run

```bash
safeharbor-check check patients.csv
safeharbor-check apply patients.csv --out cleaned.csv --dates admission_date --zips zip_code --ages age --drop patient_name,phone_number
```

Both commands accept `--delimiter CHAR` (comma by default). Use
`--delimiter "\t"` or an actual tab for TSV. The declared character is
used for input and `apply` output; it is never guessed. Other values
must be one character, excluding CR, LF and NUL, or the command returns
a one-line error and exit 2. Column lists remain comma-separated.
An explicitly supplied delimiter is recorded using escaped notation
in the report header and transform log. Without the flag, existing
comma-delimited output is unchanged.

- `--dates` columns are reduced to the year; `--zips` columns to the
  first three digits (`000` for restricted prefixes); `--ages` values
  over 89 become `90+`; `--drop` columns are removed. Undeclared
  columns are copied through unchanged, not examined.
- `apply` refuses to run with no declared columns, refuses columns not
  in the file, and refuses values it cannot read — an unparseable date or ZIP in a declared column is a clean error (exit 2), never a guess.

## Reading the results

The `check` report gives per-class results (A)–(R), each marked
VIOLATION or CANNOT_VERIFY with columns and example values, then a summary. The exit code is the verdict:

- `0` — no mechanical violations found, no column left unverified.
  The verdict line still says this is not a certification; the
  standing class-(R) and "no actual knowledge" items apply.
- `1` — violations found; the file fails the mechanical checks listed.
- `3` — no violations, but at least one column cannot be verified
  mechanically (free text, or a ZIP prefix the bundled list cannot
  settle). Not a pass: the file has only not failed the checks that can be run.

Read "not detected" as exactly that, never as proven absent: several
classes (names, medical record numbers, account numbers) are checked
by column name only, because their values have no pattern. Every report carries a residual-risk note — read it in full.

## Limits

- **This tool is a checker. It is not a certifying tool, and a clean
  report does not mean a file meets HIPAA requirements.** Research/
  educational tool. Not a medical device. Not legal advice. Verify before any real-world use, with a human who knows the data.
- Free text cannot be verified: notes and comment columns are flagged
  CANNOT VERIFY (pattern hits inside them are listed as extra
  evidence) and a person must read them. Class (R) — any other unique
  identifying number, characteristic, or code — cannot be verified mechanically at all.
- The bundled restricted-ZIP list is dated: the 17 prefixes published
  by HHS on November 26, 2012, from the 2000 Census. A prefix not in
  the list is reported as "not flagged by the bundled 2000-Census
  list — not verified against current Census data", never as safe.
- Column-name detection is a heuristic: renamed, abbreviated or
  non-English column names can evade the name-only classes. The
  value-pattern scans (SSN, email, phone, URL, IP, precise dates) run
  on unlabelled columns as a backstop, but several classes have no value pattern.
- Structured tables with one declared delimiter only (comma by default;
  use `--delimiter "\t"` for TSV) — no spreadsheets, databases, images or
  free-text documents. No medical judgements of any kind; the tool looks at identifier-shaped columns only.
- A transformed file is not a certified file: `apply` fixes only the
  columns you declared and certifies nothing.
