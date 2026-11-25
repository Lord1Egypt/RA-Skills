# Optional read-only U1 printer check

Use `scripts/u1_printer_check.py` when the user requests printer status or a comparison with loaded physical spools. It runs on the Mac using Python's standard library and connects only to an explicit private/loopback IP. The user may provide the address or authorize obtaining it from their selected Orca device details. No automatic discovery, hostname resolution, cloud requests, uploads, print controls or G-code execution are implemented. Model/project contents are read locally and never sent to the printer.

The helper takes a single snapshot using at most three fixed HTTP GETs: printer info, available objects and a query of supported status objects, including `filament_detect` and `print_task_config` when available. It reports printer/print state, whether idle is confirmed, progress, bed/four-nozzle temperatures and four physical tools' filament data. Missing objects, absent metadata and disabled sensors remain unknown. The helper does not claim a successful connection is print readiness.

## Status only

```sh
python3 scripts/u1_printer_check.py --host 192.168.1.123
```

Replace the address with the actual printer IP. Port 80 is the default; use `--port` if the actual local Moonraker service uses another port. If the user authorizes using Orca's device details, read the selected device's saved LAN host and confirm its provenance; distinguish printer addresses from Orca's own gateway addresses. Do not scan address ranges or change Orca settings. Keep local addresses and device records out of public source. The configurable socket timeout defaults to 5 seconds and is capped at 10 seconds. Public IPs, arbitrary endpoints, redirects, malformed responses, HTTP failures and API error objects are rejected. Authentication, network access and available U1 objects depend on firmware/configuration; do not change those settings automatically.

## RFID and configured metadata

Each slot keeps the existing `material`, `color`, `manufacturer` and `metadata_available` fields based on `filament_detect`, and now labels their `metadata_source` explicitly. Additional data is separated:

- `tag_metadata` contains allowlisted decoded tag attributes: vendor/manufacturer/material/subtype, up to five declared RGB colors, alpha, the reported official flag and card UID, diameter/weight/length, drying values, nozzle/bed temperature values and SKU. Missing, invalid and unpopulated measurement fields are null. An absent vendor produces no tag record; default white fields do not establish a tag reading. Unused secondary colors are omitted as null.
- RGB values are normalized to `#RRGGBB`. Other numeric tag attributes retain the firmware's decoded encoding; no diameter/length scale is guessed. For example, an encoded diameter value must not be read directly as millimeters. `WEIGHT` is a tag attribute, never a measured remaining-weight counter. UID and `OFFICIAL` are printer-reported values, not independent authentication by this helper.
- `configured_filament` is separately labelled `printer_configuration`. It reports configured type, vendor/subtype, RGB/alpha and official flag when a material is configured. This can reflect touchscreen entry or RFID synchronization. It is never substituted for missing RFID identity in automated comparisons. Empty/default configuration remains unknown.
- `metadata_conflicts` identifies known material/RGB disagreements between tag data and printer configuration. Such conflicts prevent comparison success even if the RFID values alone match expectations. Missing configuration does not erase an otherwise usable tag record. Presence is checked independently from the physical sensor, not inferred from configuration defaults.
- `logical_to_physical_tools` reports the firmware's current-task mapping as one-based physical tools, with unknown entries null. Unused logical entries may carry firmware defaults. This is informational, cannot establish a new project's mapping and is never used to rewrite recipes or replace `--slot-map`.

These are cached metadata reads; the helper does not trigger a tag scan, edit or refresh. Reports can contain card identifiers and local addresses. Store them privately in ignored `outputs/`, not in tests, releases or screenshots shared publicly.

For a service requiring an API key, provide `SNAPMAKER_API_KEY` through the local process environment. Do not put it in a command argument, project, report or Git-tracked config. The helper sends it only as `X-Api-Key`. This direct HTTP interface is intended for the trusted local network; it does not implement HTTPS or login/token acquisition. Do not bypass authentication to make a check pass.

## Compare an ordinary Orca project

```sh
mkdir -p outputs
python3 scripts/u1_printer_check.py --host 192.168.1.123 \
  --project your-u1-project.3mf --slot-map 1:2,2:1 \
  --output outputs/printer-check.json
```

`--slot-map` is required: each pair is **one-based project filament : physical U1 tool**. The example compares project filament 1 with tool 2 and filament 2 with tool 1. Map every configured filament exactly once to a distinct tool 1–4; unused project entries are still included. Never assume palette order equals physical tool order. Read the actual mapping in native Orca first.

The project must contain native settings for 1–4 ordinary filaments with complete `filament_settings_id`, `filament_type` and `filament_colour` arrays. Unknown/generic projects, target-palette exports and Full Spectrum definitions require the separate physical-spool list below. Project bytes, assignments, calibration and recipes are never edited.

## Full Spectrum or manually specified physical spools

For a mixed project, read the physical base-spool identities and tool assignments in Orca. Write those expectations to a local JSON file, for example `outputs/physical-spools.json`:

```json
{
  "1": {"material": "PLA", "color": "#FF0000"},
  "2": {"material": "PLA", "color": "#FFFFFF"},
  "3": {"material": "PLA", "color": "#000000"},
  "4": {"material": "PLA", "color": "#FFFF00"}
}
```

These example colors and tool positions are illustrative. Replace them with the physical spool metadata expected by the actual project. One to four tools may be listed. Do not enter virtual target colors or mixing recipes.

```sh
python3 scripts/u1_printer_check.py --host 192.168.1.123 \
  --expected-slots outputs/physical-spools.json \
  --output outputs/printer-check.json
```

`--expected-slots` and `--project` are alternatives. This avoids interpreting Full Spectrum's virtual filaments as loaded spools and preserves calibrated projects verbatim. No recipes are parsed, assigned or validated.

## Interpret the result

- `snapshot_completed: true` means the fixed read requests returned usable responses. Status-only mode leaves `preflight_passed: null`; it performs no spool comparison.
- With expectations, each requested tool receives separate `match`, `mismatch` or `unknown` results for presence, material family and RGB metadata; a metadata conflict adds a failing consistency check. A disabled/missing sensor cannot confirm presence. A `VENDOR: NONE` entry cannot supply usable RFID material/color identity, even if defaults or separate configured fields say PLA or white.
- `preflight_passed: true` requires a known ready/idle printer and all requested metadata/presence checks matching. A busy/paused/unknown printer, mismatch or unknown check prevents that result. Unrequested tools are reported but not compared.
- Color matching is exact stored RGB equality, accepting opaque RGB/RGBA project values; it does not measure pigmentation, translucency, printed appearance, brand or Full Spectrum calibration. Reported metadata can be stale or manually assigned. Third-party spools without usable metadata need manual verification; the helper does not convert unknown to pass.
- Spool weight fields are not used as remaining-filament measurements. Supports, slicer/material settings, bead/toolhead clearance and physical fit are outside this check. `ready_to_print` always remains false.

Exit codes: **0** for a successful snapshot-only read or passing requested checks; **1** for requested checks needing review; **2** for invalid input, connection/API/response failure or output failure. `status` and `preflight_passed` distinguish snapshot-only from comparison success. An optional `--output` file must be fresh, with an existing parent directory; existing files and symlinks are preserved. Reports include observation time and the expectations file's hash. Keep these private in `outputs/` and recheck after changing spools; a snapshot is not a print-time interlock.

## Sources and verification

The original helper uses Moonraker's documented [printer info/object queries](https://moonraker.readthedocs.io/en/latest/external_api/printer/) and [API-key header](https://moonraker.readthedocs.io/en/latest/external_api/authorization/). Field schemas were checked against Snapmaker's [filament protocol](https://github.com/Snapmaker/u1-klipper/blob/main/klippy/extras/filament_protocol.py), [RFID status object](https://github.com/Snapmaker/u1-klipper/blob/main/klippy/extras/filament_detect.py) and [print task configuration](https://github.com/Snapmaker/u1-klipper/blob/main/klippy/extras/print_task_config.py); [Luca Kaufmann's skill v1.0.0](https://clawhub.ai/lucakaufmann/skills/snapmaker) was also a query reference. No upstream implementation or control route was copied.

Tests use synthetic HTTP responses, including missing/invalid fields, source separation, metadata conflicts and unchanged source projects. A local U1 was also successfully queried through all three GETs with both filament objects available, without changing printer state. That establishes compatibility with the tested device/firmware only; other versions remain subject to validation. No live response, address or card UID is bundled.
