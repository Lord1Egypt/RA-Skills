---
name: smartclaws-tariff-file-source
description: >
  Local tariff data source contract for SmartClaws master agents. Defines the
  tariff snapshot file schema and how to use it during control decisions.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "$"
    homepage: https://github.com/skalenetwork/smartclaws
---

# Tariff File Source Contract

This is a local data source contract. It does not install SmartClaws, publish
on-chain messages, or define an agent role. Use it with
`smartclaws-master-agent`.

## Source

This is optional and setup-specific. It is not part of the generic
`SMARTCLAWS.md` template. If this skill is installed, add a `tariff` block to
the workspace `SMARTCLAWS.md`:

```yaml
tariff:
  skill: smartclaws-tariff-file-source
  source: local-file
  snapshotFile: ./state/tariff.json
  staleAfterSeconds: 120
```

Read the file at `snapshotFile` with normal file-reading tools. Do not use
SmartClaws channel reads for this source; tariff data is local/off-chain.

For human-in-the-loop demos, a `staleAfterSeconds` value around `120` is a good
default: lenient enough for multi-tool agent cycles, still short enough to catch
a stopped simulator.

## Snapshot Schema

```json
{
  "now": {
    "price_eur_mwh": 87.4,
    "tier": "expensive",
    "tier_started_s_ago": 45,
    "tier_ends_in_s": 124
  },
  "lookahead": [
    { "offset_s": 0, "price_eur_mwh": 87.4, "tier": "expensive" }
  ],
  "config": {
    "day_seconds": 7200,
    "started_at_iso": "2026-07-01T12:00:00Z",
    "tier_thresholds": {
      "cheap_max": 45.0,
      "expensive_min": 95.0
    },
    "lookahead_horizon_s": 1800,
    "lookahead_step_s": 120
  },
  "tick": 12,
  "updated_at_iso": "2026-07-01T12:03:00Z"
}
```

Fields:

- `now.price_eur_mwh`: current electricity price in EUR/MWh.
- `now.tier`: one of `cheap`, `mid`, or `expensive`.
- `now.tier_started_s_ago`: seconds since the current tier began, or `null`.
- `now.tier_ends_in_s`: seconds until the current tier changes, or `null`.
- `lookahead`: future samples ordered by `offset_s`.
- `config.tier_thresholds`: thresholds used to classify tiers.
- `updated_at_iso`: timestamp for freshness checks.

## Master-Agent Use

A master may:

- Read the snapshot before a control cycle.
- Prefer running flexible load during `cheap` periods.
- Avoid starting or continuing flexible load during `expensive` periods unless
  safety/comfort rules require it.
- Use `lookahead` and `tier_ends_in_s` to decide whether to wait, preheat, hold,
  or stop a commandable device.

A master must not:

- Treat stale, missing, or malformed tariff data as authoritative.
- Invent future tariff values beyond the provided lookahead.
- Change the tariff file.
- Publish tariff data to device channels unless explicitly instructed by the
  owner.

## Sanity Rules

- `tier` must be `cheap`, `mid`, or `expensive`.
- Prices must be numeric when present.
- Lookahead samples must have numeric `offset_s` and `price_eur_mwh`.
- If the snapshot is missing or stale, run a conservative control cycle and
  report the tariff source issue.
