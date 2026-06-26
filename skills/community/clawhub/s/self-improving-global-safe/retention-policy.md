# Retention Policy

## Goals

- keep memory useful
- prevent bloat
- keep auditability

## File Size Targets

- `global/rules.md`: <= 300 lines
- `global/corrections.md`: <= 500 lines
- `contexts/*/rules.md`: <= 200 lines
- `contexts/*/corrections.md`: <= 300 lines

When above limits, compact by dedupe and archive.

## Rule Lifecycle

1. pending (correction only)
2. confirmed (rule active)
3. stale (unused beyond threshold)
4. archived

## Staleness Thresholds

- context rule unused for 45 days -> mark stale
- global rule unused for 90 days -> mark stale
- stale for another full threshold window -> archive

## Archiving

Move archived entries into same file under `## Archived` with original metadata.
Do not hard-delete archived rules unless user requests deletion.

## Corrections Retention

Keep recent high-value history and compact noise:
- retain all confirmed/promoted correction records
- merge repeated pending corrections into one record with count
- trim verbatim text for low-value duplicates

## Privacy-First Deletion

If user requests deletion, deletion overrides retention policy.
