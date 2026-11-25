---
name: snapmaker-u1
description: Create parametric 3D models and prepare image-guided meshes or Bambu projects for Snapmaker U1 printing, with geometry, toolpath, color and print settings checks, plus optional local printer status and loaded-spool queries.
---

# Snapmaker U1

Create the requested shape and a reviewable U1 print project. Distinguish visual acceptance, mesh checks, a completed slice and physical print testing. A model file or attractive render alone establishes none of the later stages.

Resolve helper paths relative to this skill directory. Use the interpreter and runtime paths in optional `local-runtime.json`; otherwise use the local virtual environment and `.runtime/`. Discover installed capabilities before promising inference, CAD or slicer operations. The CLI slicer currently targets U1 **0.4 mm** profiles.

Respect the user's local/cloud choice. With `execution_policy: local_only`, keep photos and generation prompts on the machine, including when a host image tool runs remotely. Public weight downloads are setup, not permission to upload photos. Missing local stages should be reported explicitly.

## Choose the route

- **Dimensioned parts, organizers, gifts, fidgets:** prefer parametric CAD with an available solid-modeling tool or installed Manifold Python kernel. Preserve editable source and units. See [the CAD example](examples/moon-jewelry-dish/README.md). Check moving clearances and print a small fit coupon for mechanisms; do not infer physical motion from an animation.
- **Image-guided organic models:** read [image reconstruction](references/IMAGE_TO_3D.md). Local options are [TripoSR](references/LOCAL_ENGINE.md), a separately configured [Modly](references/MODLY.md) app, or the advanced [TRELLIS adapter](references/TRELLIS_RUNNER.md). These are candidates, not guaranteed likeness or commercial-service parity.
- **Text-guided organic models:** use a permitted reference-image generator followed by an available reconstruction engine; do not claim TripoSR accepts text directly. Keep generated references distinct from observed photos.
- **An overlapping photographic capture set:** use [Apple Object Capture](references/APPLE_CAPTURE.md). Sparse front/side portraits are references, not a complete photogrammetry capture set.
- **Background removal or on-device planning:** use the native helpers in [Apple tools](references/APPLE_NATIVE.md). Vision segmentation and Foundation Models planning do not reconstruct detailed 3D geometry.
- **Existing Bambu/MakerWorld project:** follow [Bambu conversion](references/BAMBU_CONVERSION.md). The adapter supports editable projects with one to four ordinary logical filaments and one-to-one routing. Mixed colors, many-to-one routing and unsupported projects require a manual workflow.
- **Printer status or loaded-spool check:** use the optional [read-only printer check](references/PRINTER_CHECK.md). Use an IP provided by the user or obtained from their selected Orca device details when authorized; never scan the network or infer physical slots from a Full Spectrum palette. Keep decoded tag metadata separate from editable printer configuration. Missing/disabled sensors and missing RFID identity remain unknown for automated checks; configured values alone cannot turn them into a pass. This check cannot establish print readiness or calibrated colors.
- **Color printing:** read [Full Spectrum](references/FULL_SPECTRUM.md). STL is geometry-only. A GLB can store appearance but may contain no colors; inspect the actual asset. Standard Snapmaker Orca uses a compatible painted project 3MF for this workflow.
- **Online reference collection:** follow [reference provenance](references/WEB_REFERENCES.md). Provider options and source links are in [research](references/RESEARCH.md); documentation does not establish an authenticated integration.

Ask only for details that change the result: intended use, dimensions, desired form/body extent, critical fits/loads, actual filament family/nozzle, and whether accessories belong in the model. Preserve an accepted master; keep each new attempt in a fresh job directory.

## Images and likeness

Isolate the requested subject and inspect narrow gaps, hair, glasses, hands and clothing. Preserve original photos and preprocessing provenance. Background removal and sharpening do not recover hidden geometry. A single photo leaves the sides and back inferred; request real closer/side/back views when likeness needs them.

Preserve the requested full figure, torso or bust. Do not substitute a relief, silhouette, generic analytic head, image displacement or a diagnostic head crop for a full 360° subject. Generated additional angles remain inferred.

Render actual mesh front, both sides, back and three-quarter views with `scripts/u1_preview.py`. Inspect physical facial features with textures disabled. Sampling must be labeled. Obtain portrait likeness acceptance before substantial color conversion or final slicing. When a result is rejected, change the inputs or method rather than repeating the same failed route or claiming smoothing restored missing anatomy.

## Geometry and print plan

Preserve originals. Inspect and repair only unintended defects; record changes and recheck form. Confirm units, axis, dimensions, stable bed contact, thin features, disconnected shells, winding and self-intersections where supported. Do not remove all but the largest component without checking whether details or moving parts are intentional.

Run `scripts/u1_mesh_check.py` on every delivered STL. `scripts/u1_prepare.py` also screens the serialized STL/GLB bytes: float32 export can collapse triangles that passed an in-memory check. The bundled checker cannot certify likeness, self-intersections, strength or physical fit.

Use **Draft / Normal / Strong / Flexible** intent and current official material/process presets. Read [print planning](docs/PRINT_GUIDE.md) for infill, walls, orientation, supports and material tradeoffs. Compare actual viable slices for material/time savings; include multicolor purge/prime waste. Fit includes supports, brim, tower and toolhead clearance inside the actual U1 profile, not just the nominal 270 mm cube. For print-in-place mechanisms, preserve gaps and prevent brims/supports from fusing components.

## Color and slicing

Retain source appearance before converting it to native paint/part assignments. A generic 3MF palette, texture or render does not prove the slicer kept printable colors. Four physical filaments can produce additional apparent colors through Full Spectrum's optical layer mixing; do not invent recipes or promise exact RGB reproduction.

`scripts/u1_orca_colors.py` requires a fresh **single-filament, non-mixed** template. It deliberately rejects calibrated multi-filament templates; use native Orca matching while preserving their recipes. Do not present a job-specific calibrated-project rewrite as a general packaged capability.

Complete native Manual Match with the actual spools, review achievable colors, recompute purge values and save a matched project. Use the compatible installed Color Mixing process. `scripts/u1_slice.py` applies single-filament overrides and therefore rejects unmatched, generic/unrecognized, converted and multi-filament/mixed 3MF projects. Slice those natively without erasing mappings. Conversion strips stale G-code; a fresh U1 slice is required.

The local slicer never sends a print job. It checks explicit extrusion centerlines across all layers against the resolved profile polygon, exclusions and height, then renders actual toolpath top/isometric views with support and brim colors. Unsupported geometry/state or out-of-bounds paths prevents `slice_completed`; retain failed reports. For native multicolor exports, run `scripts/u1_gcode.py` with that project's resolved machine JSON without changing its mappings. Read [toolpath scope and commands](docs/PRINT_GUIDE.md#toolpath-review): custom start/end blocks, macros, bead width and toolhead clearance remain outside these checks.

A completed slice still needs layer/support/seam/clearance and material mapping review. If UI automation fails, make bounded attempts, preserve errors and provide a concrete project plus the required manual step.

## Deliver

Provide editable source where applicable, the preserved master, usable STL/project 3MF, actual mesh previews and a short print card. Include dimensions, intended use, filament identities, color/matching status, orientation, infill/walls/supports, verified plate count, actual slice estimates and unresolved checks. Report whether the object has been physically printed; CAD motion and topology checks are not physical validation.
