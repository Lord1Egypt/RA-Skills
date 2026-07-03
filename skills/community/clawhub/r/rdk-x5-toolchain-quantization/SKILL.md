---
name: rdk-x5-toolchain-quantization
description: Toolchain-level skill for D-Robotics / Horizon Robotics RDK X5 OpenExplorer v1.2.8 post-training quantization (PTQ). Use when converting arbitrary ONNX models to RDK X5 deployable .bin / .hbm artifacts with hb_mapper, hb_perf, and hrt_model_exec. Covers OE Docker setup, operator compatibility checks, calibration data preparation (nv12, RGBCHW, YUV, featuremap fallback), YAML configuration (calibration_type, node_info, optimization), hb_mapper makertbin compilation, accuracy verification (cosine, hb_verifier, hb_mapper infer), performance profiling, and accuracy tuning for cosine drops or BPU utilization issues. Model-agnostic for YOLO, ResNet, ViT, Transformer, and other ONNX models. Trigger on keywords such as RDK X5, OpenExplorer, OE 1.2.8, PTQ, hb_mapper, hb_perf, hrt_model_exec, ONNX quantization, convert to .bin, convert to .hbm, calibration data, calibration_type, featuremap, cosine mismatch, accuracy drop, and BPU utilization.
---

# RDK X5 OpenExplorer PTQ Quantization

Use this skill to convert an arbitrary ONNX model into an RDK X5 deployable `.bin`
artifact with D-Robotics OpenExplorer **v1.2.8 (Python 3.10)**.

The workflow is model-agnostic. It focuses on the toolchain layer:
environment setup, calibration, YAML configuration, compilation, accuracy checks,
and performance profiling. It does not cover end-to-end YOLO training or ROS2
deployment.

## When To Use

1. You have an ONNX model and need an RDK X5 `.bin` or `.hbm`.
2. You need to write or debug an `hb_mapper makertbin` YAML file.
3. Quantization causes low cosine similarity or board-side outputs differ from floating point outputs.
4. `hb_mapper checker` reports unsupported operators and you need rewrite or fallback strategies.
5. The compiled model is slower than expected or BPU utilization is poor.
6. Calibration data format, quantity, preprocessing, or normalization alignment is unclear.
7. OpenExplorer Docker, SDK, or dependency setup fails.

## When Not To Use

- End-to-end YOLO training -> quantization -> board deployment -> ROS2: use an RDK YOLO Toolkit workflow.
- RDK X3, RDK Ultra, S100, or other chips: this skill targets X5 / `bayes-e`.
- Quantization-aware training (QAT): this skill covers PTQ only.
- Pure ONNX export without quantization: use the framework exporter.

## Main Workflow

### 1. Check Operator Compatibility

Run inside the OpenExplorer Docker container:

```bash
hb_mapper checker --model-type onnx --march bayes-e --model ./your_model.onnx
```

Read `hb_mapper_checker.log` to see BPU and CPU operator placement.
If unsupported operators appear, use `references/troubleshooting.md`.

### 2. Prepare Calibration Data

For the common NV12 deployment path, keep raw pixel values in the calibration
files and let `hb_mapper` apply normalization through YAML.

```python
import cv2
import numpy as np
from pathlib import Path

src_dir = Path("./cal_src")
out_dir = Path("./calibration_data")
out_dir.mkdir(exist_ok=True)

width, height, count = 640, 640, 20
images = [p for p in src_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
if len(images) > count:
    indexes = np.random.choice(len(images), count, replace=False)
    images = [images[i] for i in indexes]

for path in images:
    img = cv2.imread(str(path))                 # BGR uint8 HWC
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # match input_type_train: rgb
    img = cv2.resize(img, (width, height))
    tensor = np.transpose(img, (2, 0, 1))
    tensor = np.expand_dims(tensor, 0).astype(np.float32)
    tensor.tofile(out_dir / f"{path.stem}.rgbchw")
```

Important constraints:

- Start with at least 20 representative samples. Avoid using only easy cases or only hard cases.
- Align resize, channel order, layout, and normalization with training.
- Write raw bytes with `tofile`; do not use `.npy`.
- File size must equal `N * C * H * W * 4` bytes for `float32`.

See `references/calibration.md` for NV12, RGB/BGR, YUV, multi-input, and featuremap paths.

### 3. Write YAML Configuration

Minimal NV12 deployment template:

```yaml
model_parameters:
  onnx_model: "./your_model.onnx"
  march: "bayes-e"
  layer_out_dump: false
  working_dir: "bpu_model_output"
  output_model_file_prefix: "your_model_bayese_640x640_nv12"

input_parameters:
  input_name: ""
  input_type_rt: "nv12"
  input_type_train: "rgb"
  input_layout_train: "NCHW"
  norm_type: "data_scale"
  scale_value: 0.003921568627451

calibration_parameters:
  cal_data_dir: "./calibration_data"
  cal_data_type: "float32"
  calibration_type: "default"
  optimization: set_Softmax_input_int8,set_Softmax_output_int8

compiler_parameters:
  jobs: 16
  compile_mode: "latency"
  debug: true
  optimize_level: "O3"
```

Change `onnx_model`, `output_model_file_prefix`, `cal_data_dir`, input shape
settings, and `scale_value` for your model. See `references/yaml-reference.md`
for advanced fields such as `node_info`, `run_on_cpu`, and input-type matrices.

### 4. Compile

Run inside the OpenExplorer Docker container:

```bash
hb_mapper makertbin --config config.yaml --model-type onnx
```

Expected outputs:

- `<prefix>.bin` for deployment.
- `<prefix>_quantized_model.onnx` for quantized ONNX verification.
- `<prefix>_original_float_model.onnx` and `<prefix>_optimized_float_model.onnx`.
- `hb_mapper_makertbin.log` and an HTML compile report.

### 5. Verify Accuracy And Performance

Use `hb_mapper infer` for quantized ONNX inference because Horizon custom
operators are not handled by plain `onnxruntime`.

```bash
hb_mapper infer --config config.yaml \
  --model-file <prefix>_quantized_model.onnx \
  --model-type onnx \
  --image-file <input_node_name> sample.rgbchw \
  --input-layout NCHW \
  --output-dir infer_out/
```

Use `hb_verifier` for ONNX-vs-bin checks:

```bash
hb_verifier -m <prefix>_quantized_model.onnx,<prefix>.bin -s True -i sample.rgbchw
```

Typical gates:

- Classification: cosine similarity >= 0.99.
- Detection / segmentation: cosine similarity >= 0.95.
- Pose: cosine similarity >= 0.97.
- Transformer-like models: cosine similarity >= 0.95, then verify task metrics.

Profile compile-time performance:

```bash
hb_perf <prefix>.bin
```

Profile on the board:

```bash
hrt_model_exec perf --model_file=<prefix>.bin --core_id=0 --thread_num=1 --profile_path="."
```

Use underscore-style arguments for `hrt_model_exec`; do not replace them with hyphens.

## Reference Map

| Situation | Read |
|---|---|
| Install OE Docker / SDK and verify tools | `references/setup.md` |
| Configure YAML, input types, and advanced compiler fields | `references/yaml-reference.md` |
| Prepare calibration data or featuremap calibration | `references/calibration.md` |
| Measure cosine and compare floating-point vs quantized outputs | `references/accuracy.md` |
| Tune accuracy after cosine drops | `references/accuracy-tuning.md` |
| Improve BPU utilization and latency | `references/performance.md` |
| Resolve checker, makertbin, calibration, or runtime errors | `references/troubleshooting.md` |
