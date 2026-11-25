# Native Apple components (local only)

Use these for preprocessing and planning on a compatible Mac. They are not image-to-3D reconstruction engines. Native background removal does not establish portrait likeness. The current image-to-3D backend and its generated geometry still need separate visual testing.

## Apple Vision: subject extraction and reference analysis

Source: `scripts/u1_vision.swift`. This uses Apple's `VNGenerateForegroundInstanceMaskRequest`, not a language prompt or external service. It saves an oriented full-frame transparent PNG, reports foreground-instance and alpha statistics, and optionally reports detected faces and advisory face-capture quality. It retains all detected foreground instances, so inspect the mask when several objects or people are present. A capture-quality score is not a 3D likeness score.

Build once with the local SDK and a writable module cache:

```sh
mkdir -p .runtime/apple
xcrun swiftc -O -parse-as-library scripts/u1_vision.swift \
  -o .runtime/apple/u1_vision -module-cache-path /private/tmp/u1-swift-cache
```

Run:

```sh
.runtime/apple/u1_vision --input photo.jpg --output subject.png --report vision.json
```

For a portrait, optionally compare a separate people-only matte:

```sh
.runtime/apple/u1_vision --input photo.jpg --mode person \
  --output subject-person.png --report vision-person.json
```

The default `--mode foreground` retains all salient foreground instances. `--mode person` instead uses `VNGeneratePersonSegmentationRequest` at Apple's `accurate` quality level, which includes matting refinement. Its lower-resolution matte is scaled to the full oriented image frame. It predicts a separate matte without eroding hair or intersecting masks; it can still omit accessories or non-person objects. Compare hair, glasses, clothing and held objects before choosing one. Person-mode reports set `instance_count` to `null` because the matte does not count individuals; detected-face count is a separate advisory result.

Input, output and report must be different paths. Existing output/report files are refused. This helper does not enable Apple Intelligence, send photos elsewhere, or create mesh geometry. It requires macOS 14 or later for its Vision request and a suitable local SDK to build.

The local TripoSR runner accepts `--segmentation auto|vision|human|alpha`; `auto` prefers the built Apple Vision helper on macOS and currently uses its default foreground mode. `vision` is explicit and reports an error instead of silently selecting another model if the helper is absent or fails. Existing supplied alpha is preserved and labeled as such. To use the separate person-mode output in a later run, provide that transparent PNG with `--segmentation alpha`; the runner does not expose `--mode person` directly. `human` remains the earlier rembg baseline and `alpha` requires an already transparent input. The Apple path does not require the downloaded rembg model weights to be present.

## Foundation Models: structured print-intent planning

Source: `scripts/u1_apple_plan.swift`. It uses **only `SystemLanguageModel.default`** and no tools or cloud fallback. The helper checks availability before guided generation. It can interpret a text brief into Draft/Normal/Strong/Flexible intent, a tentative material family, an explanation and missing-information questions. Its schema excludes numeric printer settings; matching official U1 profiles and deterministic validation remain authoritative.

```sh
xcrun swiftc -O -parse-as-library scripts/u1_apple_plan.swift \
  -o .runtime/apple/u1_apple_plan -module-cache-path /private/tmp/u1-swift-cache
.runtime/apple/u1_apple_plan --doctor
.runtime/apple/u1_apple_plan --brief "An indoor decorative portrait bust; material is unknown."
```

This requires a FoundationModels-capable SDK, macOS 26 or later, a supported device, and an available on-device Apple Intelligence model. Do not automatically change the user's Apple Intelligence settings. If unavailable, report the reason and use the skill's explicit recommendation rules; do not route to Private Cloud Compute.

## Capability boundaries

Vision is the native segmentation/reference-analysis component. Foundation Models provides an on-device language-planning component; recent framework versions also document image understanding, but this helper does not implement that attachment API. Neither helper exports a detailed printable 360° mesh. For that stage use a separately tested reconstruction engine or a suitable real multiview/photogrammetry workflow.

Official documentation: [Vision foreground masks](https://developer.apple.com/documentation/vision/vngenerateforegroundinstancemaskrequest), [person matting](https://developer.apple.com/documentation/vision/vngeneratepersonsegmentationrequest), [Vision framework](https://developer.apple.com/documentation/vision), [Foundation Models](https://developer.apple.com/documentation/foundationmodels), [on-device availability and generation](https://developer.apple.com/documentation/foundationmodels/generating-content-and-performing-tasks-with-foundation-models).

## Apple-native multiview 3D option

RealityKit Object Capture reconstructs overlapping photographs locally. Use `scripts/u1_capture.swift` and read [APPLE_CAPTURE.md](APPLE_CAPTURE.md) for the device check, build command and capture requirements. One portrait is not a photogrammetry dataset; preserve real framing and camera metadata. The language model and Vision masks do not replace capture geometry.
