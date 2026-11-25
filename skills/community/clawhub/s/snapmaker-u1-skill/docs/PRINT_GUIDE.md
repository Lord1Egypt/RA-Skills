# Snapmaker U1 print guide

## Intent presets

| Intent | Starting approach | Typical use |
|---|---|---|
| Draft | Coarser layer preset, modest infill, minimal supports | Shape and fit checks |
| Normal | Standard quality preset, balanced walls and infill | General-purpose parts |
| Strong | Orient load across layers, add perimeters, reinforce locally, then tune infill | Brackets, clips, frequently handled parts |
| Flexible | U1-compatible TPU profile, gentle geometry and no sharp thin hinges | Grips, bumpers, compliant parts |

These are intent labels, not fixed slicer profiles. Use current Snapmaker Orca presets for layer height, speed, temperature, cooling, and material behavior.

## Portraits and Full Spectrum

For complete portrait models, read [image reconstruction](../references/IMAGE_TO_3D.md). Confirm actual facial geometry and 360° subject isolation before print preparation. Chin, nose, glasses and ears can need supports even when a mesh is closed.

For additional apparent colors from four loaded filaments, read [Full Spectrum](../references/FULL_SPECTRUM.md). Use the current compatible color mixing preset and actual spool calibration, then compare material/time against a standard color slice. Keep photographic target colors until that evaluation; do not force skin to a primary spool color.

## Material selection

- **PLA:** easy to print and dimensionally convenient for indoor prototypes and decorative parts. Avoid where sustained heat or outdoor exposure is expected.
- **PETG:** a practical tougher choice for everyday parts exposed to moisture or moderate warmth. Account for stringing and fit changes.
- **TPU:** use for flexible parts only; follow the dedicated U1 TPU recommendations and matching preset.
- **ABS/ASA:** use when the application needs their temperature or outdoor properties. Follow Snapmaker's enclosure, plate, ventilation, and material-specific guidance.
- **Support interface material:** where the model needs cleaner removable supports, the Snapmaker Support for PLA guide recommends using it as the interface rather than the entire support structure, to reduce time and material.

Verify exact material compatibility and settings against the spool maker and current Snapmaker Orca preset. Dry moisture-sensitive filament as directed by its manufacturer.

## Infill and strength

Infill supports top surfaces and contributes to stiffness, but walls and orientation often determine useful strength more directly. Start with the preset matched to the intent. For a functional part, orient the load so it does not pull layers apart; increase perimeters or add ribs/bosses in CAD before making the entire interior dense. Test critical fits and loads with a small coupon or prototype.

## Material and plate efficiency

1. Prefer hollow or ribbed geometry when it preserves function.
2. Keep supportable overhangs and orient the broad stable face down.
3. Use tree/organic supports when the current slicer and geometry benefit; compare with normal supports in preview.
4. Arrange parts in one plate only when the printable polygon, clearances, support footprints, and print sequence all fit.
5. Compare sliced filament usage and time across viable orientations in Snapmaker Orca. Include purge waste for multicolor work.

## Toolpath review

`scripts/u1_slice.py` automatically checks each distinct external or project-embedded G-code artifact. It checks explicit positive-extrusion movement across **all layers and feature types**, including supports, brim, skirt and prime tower where present. Bounds use the resolved machine's `printable_area`, `bed_exclude_area` and `printable_height`; the nominal bed size is not substituted. Straight paths crossing concave boundaries or excluded polygons also fail.

Each review writes `toolpath-review.json`, `toolpaths-top.png` and `toolpaths-3d.png`. These show actual extrusion paths in their sliced orientation, with support, brim/skirt, outer-wall and top-surface colors. Large previews sample paths per feature and label the displayed count; validation still checks every segment. They are static overviews; use Orca for individual-layer inspection.

For G-code exported from a native calibrated or multicolor project, use the standalone reviewer. Supply a **resolved machine JSON from that same project/profile**, with the actual bounds and height; do not substitute another printer's profile. This reads G-code without editing colors, rewriting it or sending it to hardware:

```sh
.venv/bin/python scripts/u1_gcode.py exported-plate.gcode \
  --machine-json resolved-machine.json --output-dir outputs/toolpath-review
```

The output directory must be fresh. Exit codes are 0 for passing checks and generated previews, 1 for failed/incomplete review, 2 for invalid input or setup. The integrated slicer records native export separately as `slicer_output_completed`; `slice_completed` additionally requires passing checks and generated previews. Review failures retain their reports and line numbers.

Supported motion is millimeter Klipper/Orca G0/G1, absolute/relative XYZ and E with G92 resets, and absolute-XYZ XY I/J arcs (including helical moves and P1). Arc subdivision includes exact bed-edge extrema; arc checks require a convex printable polygon without excluded areas. Inches, R arcs, other arc planes, multi-turn arcs, unsupported coordinate-state commands and unknown extrusion origins fail review. The reviewer uses explicit G-code coordinates; it is not a firmware simulator.

`TYPE:Custom` start/end extrusion blocks are explicitly excluded and counted. Firmware macros, homing behavior, printer-side offsets and tool changes are not simulated; unknown macro names are reported. Travel paths, nozzle/bead width, material mixing, support quality and toolhead collisions are outside the geometric check. A passing report keeps `ready_to_print: false`: review those details in native Orca with the actual machine and spools.

Feature grouping was informed by [Brent Bolinger's U1 toolkit](https://github.com/bbolinger/snapmaker-u1-toolkit/tree/c66284ce990fa71ccf969cae517fbd3b0c780450); the parser is local and uses no toolkit runtime. Modal behavior follows the documented [Klipper G-code semantics](https://www.klipper3d.org/G-Codes.html) and [arc support](https://github.com/Klipper3d/klipper/blob/master/klippy/extras/gcode_arcs.py), within the narrower supported scope above.

## Validation checklist

- [ ] Units and scale confirmed; critical dimensions measured in CAD.
- [ ] Mesh has no degenerate triangles and is closed where a solid is intended.
- [ ] No unexpected self-intersections, disconnected shells, or reversed/open surfaces.
- [ ] Part fits the current U1 build-plate boundary and height limit.
- [ ] Snapmaker Orca uses the U1 profile, actual nozzle, actual plate, and matching filament preset.
- [ ] Layer preview shows sound supports, bridges, walls, seams, tool changes, and no collisions.
- [ ] Sliced material use, purge waste, and print time reviewed.
- [ ] Critical fit/load parts have a test print plan.
