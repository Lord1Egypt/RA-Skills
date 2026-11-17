# Changelog

## 1.0.1
- Default lookup window is target date ±3 days.
- Prevents whole-year / year-to-date searches for normal single-transaction lookups.
- Expands once to ±7 days only if needed.
- Adds browser round-trip minimization rules.
- Adds one-pass transaction list extraction.
- Prefers browser evaluate or selector-scoped/efficient snapshots.
- Avoids visual row-by-row scanning.
- Opens only plausible candidate transactions.
- Avoids screenshots unless DOM/text extraction fails.
- Targets roughly 5-7 browser operations per normal lookup.
- Keeps native browser tool only; no Bash/exec/shell fallback.
- Preserves read-only and manual-authentication safety rules.

## 1.0.0
Initial ClawHub-ready PayPal reconciliation skill.
