# Existing Bambu Lab projects

Use this path for an editable Bambu Studio or MakerWorld project `.3mf` that contains model geometry and one to four source filament IDs. It converts printer settings and supported color assignments for local review in Snapmaker Orca; it does not reconstruct a new model or improve facial likeness. A sliced `.gcode.3mf` without editable geometry is unsupported. Obtain the original project instead. A geometry-only 3MF belongs in the skill's ordinary preparation workflow, where U1 settings can be assigned afresh.

The adapter runs the pinned [bambu-to-snapmaker-u1 backend](https://github.com/thadius83/bambu-to-snapmaker-u1/tree/639b822e2db3b59b0dc7379771f7cdf872b06910/backend) from a separately installed isolated `.runtime/bambu-to-u1` checkout. It needs neither the hosted converter nor a web server. Project files stay local. Runtime setup downloads are separate from conversion.

## Commands

Use absolute helper paths when invoked from an installed skill. The command below uses a repository checkout:

```sh
python3 scripts/u1_bambu.py doctor
python3 scripts/u1_bambu.py profiles
python3 scripts/u1_bambu.py convert existing-project.3mf --output-dir outputs/bambu-converted
```

The output directory must be fresh. The default bundled reference is `0.20 Standard - Cube`:

```sh
python3 scripts/u1_bambu.py convert existing-project.3mf \
  --output-dir outputs/bambu-converted \
  --profile '0.20 Standard - Cube'
```

Prefer a current reference project saved from Snapmaker Orca with the actual U1 printer, nozzle, plate and material settings selected. Include a small model when saving the reference:

```sh
python3 scripts/u1_bambu.py convert existing-project.3mf \
  --output-dir outputs/bambu-converted \
  --reference my-current-u1.3mf \
  --slot-map 1:1,2:2
```

`--slot-map` uses **one-based source slot:U1 toolhead** pairs. When supplied, it must cover every source slot with distinct destinations from 1 through 4. Without it, ordinary source slots retain their order. Inspect actual spool identities and routing in the GUI in either case.

`--apply-rules` opts into the upstream filament rules. These match source filament metadata and change process settings globally; they are not calibrated settings for the user's spools or per-object optimization. Keep the default unless those changes are wanted, and inspect `diff.json` when enabled.

## Runtime setup

Configure `bambu_runtime` in optional `local-runtime.json`, or download the pinned runtime separately, preserve its license, and install only its conversion dependencies in an isolated environment. No Docker, frontend or telemetry packages are needed:

```sh
mkdir -p .runtime
git clone https://github.com/thadius83/bambu-to-snapmaker-u1.git .runtime/bambu-to-u1
git -C .runtime/bambu-to-u1 checkout 639b822e2db3b59b0dc7379771f7cdf872b06910
python3.11 -m venv .runtime/bambu-to-u1/.venv
.runtime/bambu-to-u1/.venv/bin/python -m pip install pydantic==2.9.2 PyYAML==6.0.2 ijson==3.6.0
```

Python 3.11 is tested. Set `bambu_runtime` to the absolute checkout path, or pass `--runtime-dir /absolute/path/to/bambu-to-u1` before the subcommand. `doctor` and conversion check the revision and require unchanged backend, references, rules and license. The child process blocks Python IP networking and DNS; this is not an OS-wide network sandbox. Conversion itself uses local files only.

## Supported conversion boundary

This adapter handles ordinary projects with at most four logical filament colors and optional one-to-one routing. It rejects greater color counts and native mixing states for manual treatment. This is an adapter limit: **the U1 can produce more than four apparent colors through Full Spectrum**. For that workflow read [FULL_SPECTRUM.md](FULL_SPECTRUM.md), use actual loaded filaments and preserve calibrated virtual-color assignments. Upstream native mixing support is still [documented as in development](https://github.com/thadius83/bambu-to-snapmaker-u1/blob/639b822e2db3b59b0dc7379771f7cdf872b06910/README.md#known-limitations).

The initial adapter does not perform many-to-one color reduction or automatic spool-swap planning. Preserve the original project and use a deliberate manual workflow for those jobs; do not merge colors just to pass the four-slot check.

It also rejects variable-layer-height and layer-range override files: those need separate review of overridden settings and prime-tower compatibility. Ordinary pause/tool-change events are supported; arbitrary custom layer scripts are rejected. Whole-object, part and feature assignments receive the same slot-range checks as triangle painting.

Incomplete part metadata without `mesh_stat` is rejected: a native import probe failed with `std::bad_alloc` when that block was absent. Re-export from the source slicer rather than inventing repair statistics. The installed CLI also gates newer Bambu project versions; its documented `--allow-newer-file` flag was used for the synthetic import probe only. Do not disable validity checks or change application-version tags just to hide a failed import.

Bundled references use 0.4 mm nozzles. A suitable U1 reference is required for another nozzle; review inherited layer heights and line widths as well as the reported nozzle mismatch. Source temperatures and print intent are not proof that the material is appropriate for the U1 or the actual spool.

The wrapper clears filament start/end G-code rather than carrying demo-spool hooks from the bundled reference. It forces other G-code hooks, G-code flavor, machine limits and printer hardware fields from the U1 reference, removes post-processing settings and embedded preset configurations, normalizes supported pause/tool-change markers, rejects arbitrary per-layer commands and removes cached source G-code. These checks extend the upstream [machine-hook replacement](https://github.com/thadius83/bambu-to-snapmaker-u1/blob/639b822e2db3b59b0dc7379771f7cdf872b06910/backend/gcode_swapper.py) and [layer-metadata rewrite](https://github.com/thadius83/bambu-to-snapmaker-u1/blob/639b822e2db3b59b0dc7379771f7cdf872b06910/backend/metadata_helpers.py#L99). Source printer G-code must never become a U1 print job. Reselect the actual spool presets during Orca review; clearing hooks does not configure the material.

Conversion can translate source bed placement, but it does not scale or pack models, reduce plate count, optimize supports/infill/filament use, or validate mesh geometry. Apply the skill's geometry checks and print-planning workflow separately, preserving the model's intended dimensions.

## Outputs and review

Each successful job preserves the original project and its hash and writes:

- `converted.3mf`: editable U1 conversion awaiting review and a new slice.
- `diff.json`: upstream changes to identity, settings, slots and stripped artifacts.
- `report.json`: conversion provenance, checks, limitations and review state.

The conversion carries a manual-review marker. The generic CLI slice adapter refuses to replace its mappings with a provisional single-filament preset. Open `converted.3mf` **as a project** in Snapmaker Orca, reselect the actual spool presets and inspect U1 identity/nozzles, painted faces, part/feature assignments, temperatures, supports and every plate. Check printable boundaries, brim, tower, toolhead clearance and print sequence. Re-slice from geometry, inspect the layer/color preview, and save a new reviewed project before treating it as a printing candidate. Report time and consumption only from that actual slice.

Tests cover synthetic painted projects and, when the pinned optional backend is installed, real conversions of synthetic cubes and sparse routing. A native import probe is narrower than GUI color review or a fresh slice. Conversion success establishes neither mesh validity nor slicer readiness; retain unresolved checks in the print card.

The separately downloaded runtime retains its [PolyForm Noncommercial 1.0.0 license and required notice](https://github.com/thadius83/bambu-to-snapmaker-u1/blob/639b822e2db3b59b0dc7379771f7cdf872b06910/LICENSE). Its use is limited to purposes permitted by that license; the skill does not relicense upstream code.
