# Municipal Quantity Takeoff (shizheng-suanliang)

**[English](./README.en.md) | [中文](./README.md)**

**v0.1.0** · Formal quantities are taken only from `lis-skill-bus` by `contract_id`; this skill never parses drawings. It turns the `cad-file-reader` municipal geometry contract (`municipal-geometry` pack output) into **pipeline length bands + diameter bands + well counts + road area band + material list**.

The formal chain is fixed: `cad-file-reader -> cad-municipal-geometry/v1 -> lis-skill-bus -> shizheng-suanliang`. This skill never reads DWG/DXF/PDF and offers no second parsing path. The `--municipal`/positional file entry requires explicit `--allow-manual` and is always degraded to `manual` provenance — not formal quantities.

## Check prerequisites first

```bash
python3 scripts/municipal_qty.py --check-deps
```

- Exit 0: chain ready. Exit 20/21: missing `cad-file-reader` (>=0.41.0) or `lis-skill-bus` (>=0.1.11); copy the printed install commands.
- First produce `*.municipal.json` (schema `cad-municipal-geometry/v1`) with the `municipal-geometry` pack of `cad-file-reader`.

## What it does

- Consumes `cad-municipal-geometry/v1`, emits `cad-municipal-qty/v0.1` as `json + md + csv`.
- Pipeline length by system (storm/water supply/reclaimed water/heat/gas/power/telecom), drawing-length band ×[1.00, 1.15]; unmappable segments go to "unclassified", never force-mapped.
- Diameters parsed from `pipe_network[].pipe_size` (DN/De/d/Φ) into bands (300–1500+), **count only** — no diameter-to-segment pairing without evidence.
- Wells (manholes/gully inlets/drop/valve/pump) counted by system; network open endpoints/junctions used as cross-check only.
- Road area band = centerline/edge length × majority width label (±15%); missing width label → `unavailable`, never a default width.
- Pavement materials listed only (thickness flagged missing); no layer-by-layer areas.
- m-unit drawings require `unit_scale`; without it only counts and a missing-items list are produced.

## Usage

```bash
python3 scripts/municipal_qty.py --validate xxx.municipal.json
python3 scripts/municipal_qty.py --municipal xxx.municipal.json --allow-manual --out-prefix municipal_qty
python3 scripts/municipal_qty.py --from-contract <contract_id> --project <project> --out-prefix municipal_qty
```

## What it does NOT do

- No BOQ preparation, as-built measurement, settlement or pricing (`final_quantity=false`).
- No earthwork: without cross-section cut/fill data any earthwork number would be fabricated.
- No bridge/culvert/tunnel member quantities (piles, box girders, lining) — candidates and review items are passed through only.
- No hydraulic, structural or compliance calculations.

## License

CC-BY-NC-SA-4.0, non-commercial use only; commercial use requires separate written permission, see `LICENSE.md`.
