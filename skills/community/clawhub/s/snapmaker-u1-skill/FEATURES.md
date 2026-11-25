# Capability boundaries

| Feature | Included | Limits |
|---|---|---|
| Text to functional models | CAD workflow and editable original example | CAD tool/dependencies must exist; no direct neural text-to-3D backend |
| Images to 3D | TripoSR setup; optional Modly and TRELLIS workflows | Generated hidden surfaces and facial likeness require review; not a measured scan |
| Background removal | Native Apple Vision helper | macOS required; masks may retain backdrop or omit details |
| Multiview capture | Native Apple Object Capture helper | Compatible Mac and overlapping real capture set required |
| Print-intent planning | Draft / Normal / Strong / Flexible; optional Apple language helper | Suggestions are not calibrated printer settings |
| Mesh validation | Bounds, degenerates, edges, winding/components and serialized-export checks | No universal strength, thickness, self-intersection or fit certification |
| Previews | Actual mesh contact sheet and offline orbit viewer | Display sampling is labeled; a render does not validate printing |
| Sliced toolpath review | All-layer extrusion-centerline polygon/exclusion/height checks; feature-colored top/isometric PNGs from G-code | Custom blocks and firmware macros excluded; no bead-width or collision certification; supported arc checks need a convex bed without exclusions |
| Color preparation | Target color regions, generic 3MF and native paint export | Fresh single-filament template required; physical mixes not generated |
| U1 Full Spectrum | Matching/calibration workflow | Native Orca matching with actual spools and color review required |
| Bambu projects | Guarded wrapper, source/mapping audits, stale G-code removal | Separate noncommercial backend; up to four ordinary colors with bijective routing |
| Slicing and estimates | Local official U1 0.4 mm profiles, isolated runs, actual G-code estimates | Mixed projects use native project slicing; no printer upload; layer review required |
| Optional printer check | Read-only local status, temperatures, decoded RFID details, separate configured filament settings and four-slot comparisons | Explicit authorized target and physical mapping required; missing RFID stays unknown; conflicts need review; no controls, remaining-weight measurement or mix calibration |
| Filament and plate optimization | Geometry/infill/support/color-change tradeoffs and slice comparisons | No globally optimal packing or guaranteed material savings |

CAD and slice checks have been exercised locally. Public tests use synthetic geometry; optional dependencies are not bundled. Physical-print accuracy and portrait likeness are never inferred from automated test success.
