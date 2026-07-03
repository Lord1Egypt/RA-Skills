# Calibration Data

Calibration estimates activation ranges for PTQ. Bad calibration data is one of
the most common causes of low cosine similarity, poor task metrics, or unstable
board outputs.

## General Rules

- Use representative samples from the same distribution as deployment.
- Start with 20-50 samples. More samples can improve stability but increase time.
- Match the training preprocessing path: resize, crop, padding, channel order,
  layout, normalization, and color space.
- Write raw binary tensors. Do not write `.npy` files unless the toolchain
  explicitly asks for them.
- Verify file size before compiling.

## NV12 Runtime Path

For `input_type_rt: nv12` and `input_type_train: rgb`, prepare RGB CHW float32
calibration files and let YAML handle normalization:

```python
import cv2
import numpy as np
from pathlib import Path

src = Path("./cal_src")
out = Path("./calibration_data")
out.mkdir(exist_ok=True)

W, H = 640, 640
for p in src.glob("*.jpg"):
    img = cv2.imread(str(p))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (W, H))
    x = np.transpose(img, (2, 0, 1))
    x = np.expand_dims(x, 0).astype(np.float32)
    x.tofile(out / f"{p.stem}.rgbchw")
```

YAML:

```yaml
input_parameters:
  input_type_rt: "nv12"
  input_type_train: "rgb"
  input_layout_train: "NCHW"
  norm_type: "data_scale"
  scale_value: 0.003921568627451

calibration_parameters:
  cal_data_dir: "./calibration_data"
  cal_data_type: "float32"
```

## RGB/BGR Runtime Path

Use this only if the board-side application feeds RGB or BGR tensors directly.
Set runtime and training input types to match the actual data path:

```yaml
input_parameters:
  input_type_rt: "rgb"
  input_type_train: "rgb"
  input_layout_train: "NCHW"
```

If your model was trained with BGR input, use `bgr` consistently.

## YUV/NV12 Files

If you produce true NV12/YUV calibration files yourself, make sure the format,
width, height, stride, and file size match exactly. NV12 files are not the same
as RGB tensors saved with a different extension.

For many models, the safer path is to prepare RGB/BGR training-format tensors
and let `hb_mapper` perform the runtime conversion configured in YAML.

## Multi-Input Models

Use one calibration directory per input, or the exact directory structure
expected by the current OpenExplorer version. File ordering must be stable and
aligned across inputs.

Checklist:

- Each input has the same number of samples.
- Sample names sort in the same semantic order.
- Every input tensor file has the expected byte size.
- YAML names match ONNX input names when `input_name` is not empty.

## Featuremap Calibration

Use featuremap calibration when image-domain calibration cannot represent the
actual model input or when preprocessing is too complex to reproduce in YAML.

Typical cases:

- The model consumes intermediate features rather than images.
- Preprocessing includes custom normalization, tokenization, or packed channels.
- Accuracy drops remain after normal calibration tuning.

For featuremap calibration, dump real model input tensors from the floating-point
pipeline and feed those tensors directly to calibration. Keep dtype, layout, and
shape exact.

## File Size Formula

For `float32` NCHW:

```text
bytes = N * C * H * W * 4
```

For `uint8` NHWC:

```text
bytes = N * H * W * C
```

Check quickly:

```python
from pathlib import Path
for p in Path("calibration_data").iterdir():
    print(p.name, p.stat().st_size)
```

## Common Calibration Mistakes

- Saving `.npy` headers and raw tensor bytes together.
- Applying normalization in both the preprocessing script and YAML.
- Using BGR data while YAML says RGB.
- Using letterbox during training but direct resize during calibration.
- Sampling too few images or using only simple backgrounds.
- Mixing image sizes without matching dynamic-shape configuration.
