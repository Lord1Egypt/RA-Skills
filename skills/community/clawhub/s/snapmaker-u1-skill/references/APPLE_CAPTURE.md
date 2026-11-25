# Native Apple multiview reconstruction

`scripts/u1_capture.swift` uses **RealityKit `PhotogrammetrySession`**, Apple's local Object Capture API. It reconstructs a capture set of overlapping real photographs. It does not turn a single portrait into a recovered 360° scan and does not use the Foundation Models language-planning helper.

## Capture input

Put original, full-frame JPEG, PNG or HEIC/HEIF photos in a dedicated directory. Keep camera metadata and the originals; do not independently crop, resize, generate or rotate reference views. The helper leaves these files unchanged and records their SHA-256 hashes.

Move the camera around a static subject with substantial overlap between neighboring shots. Apple's guidance recommends about **70% overlap**, consistent camera settings and diffuse lighting. Several widely separated front/profile/back portraits can help an image-conditioned model, but are not by themselves a reliable photogrammetry capture set. Cover the sides and back as well as the front, with multiple heights when needed.

For a person, maintain the same head/body pose and facial expression while the camera moves. Motion and changing hair or clothing can impair reconstruction. Reflective glasses, strong highlights and deep shadows can also interfere with landmark matching. Retain glasses if they are part of the desired portrait, and inspect the resulting geometry rather than assuming the reflection or texture has reconstructed correctly.

## Build and run

This helper targets macOS 14 or later and requires a compatible Mac. It checks `PhotogrammetrySession.isSupported` before starting a session.

```sh
mkdir -p .runtime/apple
xcrun swiftc -O -parse-as-library scripts/u1_capture.swift \
  -o .runtime/apple/u1_capture -module-cache-path /private/tmp/u1-swift-cache
.runtime/apple/u1_capture doctor
.runtime/apple/u1_capture generate \
  --input-dir /absolute/path/to/original-photos \
  --output-dir /absolute/path/to/new-capture \
  --detail medium
```

`--detail` accepts `reduced`, `medium` (default) or `full`. Higher detail can require more memory and time. The helper enables native object masking and uses unordered sample ordering with normal feature sensitivity. No photo upload, external model download, cloud fallback or system-preference change is performed.

The output directory must not already exist. Input/output aliases and ancestor/descendant paths are refused. Empty and single-photo folders, exact duplicates of one image, unreadable image metadata and image symlinks are rejected before a reconstruction session starts. This preflight does **not** determine sufficient overlap, coverage or portrait likeness.

## Artifacts and status

The native request targets a **directory URL for OBJ output**, as documented by Apple. A completed run must contain an OBJ file before the helper reports completion. Preserve the complete `model/` directory with its material/texture sidecars.

- `progress.jsonl` and stdout contain structured progress events, including invalid/skipped samples, request errors and automatic downsampling.
- `report.json` records input provenance, settings, completion or failure, output files and unverified downstream checks.
- `ready_to_print`, likeness acceptance, geometry validation and slicing verification remain false even after reconstruction succeeds.

Load the generated OBJ into the existing mesh preview/preparation tools, inspect the actual front/sides/back, confirm its up axis and scale to the requested dimensions. Screen/repair geometry and check physical facial detail with textures removed before U1 color conversion and slicing. Normal/displacement maps and a convincing texture do not establish physical printable facial detail. Native masking also does not prove that all unwanted scene geometry is absent.

## Limits and sources

The helper has been exercised with real overlapping object photos, but higher detail does not guarantee more triangles, complete thin accessories or better faces. Inspect actual geometry. A supported host and clean input checks do not establish adequate overlap or a complete reconstruction. Sandboxes may restrict host GPU/ML services.

Official sources: [Creating 3D objects from photographs](https://developer.apple.com/documentation/realitykit/creating-3d-objects-from-photographs), [capture guidance](https://developer.apple.com/documentation/realitykit/capturing-photographs-for-realitykit-object-capture), [OBJ requests](https://developer.apple.com/documentation/realitykit/photogrammetrysession/request), [detail levels](https://developer.apple.com/documentation/realitykit/photogrammetrysession/request/detail).
