# Local Webcam Demo Notes

Use this reference when the user wants to do a fast local validation loop on a laptop or workstation with a webcam.

## Recommended starter model

Use this SenseCraft model first for a minimal person-detection demo:

- `60080` — `Person Detection--Swift YOLO`
- current public file URL resolves to a `.tflite` model

Reason to prefer it:
- easy to demonstrate visually
- single-class output keeps the overlay simple
- small enough for CPU demo use

## Recommended environment on macOS arm64

Prefer Python `3.12` over `3.14` for this flow.

Use:
- `opencv-python`
- `numpy`
- `pillow`
- `ai-edge-litert`

Avoid assuming `tflite-runtime` is available. On macOS arm64 / newer Python versions, `tflite-runtime` wheels may be unavailable. `ai-edge-litert` works as a practical replacement for local TFLite inference.

Example setup:

```bash
bash scripts/setup_local_demo_env.sh
source .venv/bin/activate
```

Equivalent manual setup if needed:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy opencv-python pillow ai-edge-litert
```

## Download flow

From the skill root:

```bash
python3 scripts/sensecraft_models.py download --model-id 60080 --output-dir ./models --manifest ./models/downloaded.json --summary
```

This should produce a path like:

```text
./models/60080-Person-Detection--Swift-YOLO.tflite
```

## Demo script

Use the bundled launcher first:

```bash
bash scripts/run_local_person_demo.sh
```

Double-clickable macOS helper:

```bash
scripts/run_local_person_demo.command
```

Direct Python entrypoint if needed:

```bash
python3 scripts/sensecraft_webcam_person_demo.py --model ./models/60080-Person-Detection--Swift-YOLO.tflite
```

Useful options:

```bash
bash scripts/run_local_person_demo.sh --debug
bash scripts/run_local_person_demo.sh --camera 1
python3 scripts/sensecraft_webcam_person_demo.py --image ./sample.png --save ./annotated.png
```

Window controls:
- `s` — save the current annotated frame into `./captures/`
- `q` or `Esc` — quit

## Important decoding note

Do **not** assume every SenseCraft / SSCMA YOLO-family export can be decoded as plain `x1,y1,x2,y2` from the fused output tensor.

For the `60080` Swift-YOLO model used here, a plain `xyxy` interpretation produced visibly wrong boxes.
A more accurate practical decode for the single fused output `[1, 2268, 6]` was:

- first 4 values → treat as `cx, cy, w, h` in model-space
- 5th value → use as the candidate score for thresholding and NMS

This was validated empirically against sample imagery and local webcam output.

## SSCMA-Micro cross-check

When the user reports wrong boxes, check the SSCMA-Micro reference implementation before guessing.

Relevant repo:
- `https://github.com/Seeed-Studio/SSCMA-Micro`

Relevant source for YOLO-family postprocess patterns:
- `sscma/core/model/ma_model_yolo26.cpp`

Why it matters:
- SSCMA models may use exporter-specific fused outputs
- box meaning can differ from generic TFLite YOLO tutorials
- direct `xyxy` assumptions can be wrong even when inference runs successfully

## Camera permission reminder

On macOS, if OpenCV cannot open the webcam, remind the user to grant camera access to the terminal app they are using:

- System Settings → Privacy & Security → Camera

Typical symptom:
- `not authorized to capture video`

## Validation standard

Before calling the integration "good":
1. run on one obvious positive image
2. run on live webcam feed
3. save at least one annotated frame
4. confirm the box geometry looks plausible, not merely that the script runs

If geometry is still off:
- enable `--debug`
- inspect top candidates
- adjust decoding before chasing thresholds
