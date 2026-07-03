# Accuracy Verification

Accuracy verification should compare floating-point behavior, quantized ONNX
behavior, and compiled `.bin` behavior. Do not rely on a single sample unless
you are only doing a smoke test.

## Artifacts To Compare

After `hb_mapper makertbin`, inspect:

- `<prefix>_original_float_model.onnx`
- `<prefix>_optimized_float_model.onnx`
- `<prefix>_quantized_model.onnx`
- `<prefix>.bin`

The optimized float model helps separate graph optimization differences from
quantization differences.

## Recommended Gates

| Model type | Starting cosine gate |
|---|---:|
| Classification | >= 0.99 |
| Detection | >= 0.95 |
| Segmentation | >= 0.95 |
| Pose | >= 0.97 |
| Transformer-like models | >= 0.95 plus task metrics |

Cosine similarity is a diagnostic, not a complete product metric. Always verify
task-level metrics such as mAP, top-1/top-5, IoU, or downstream business metrics.

## Use hb_mapper infer

Plain `onnxruntime` cannot execute Horizon quantized custom operators reliably.
Use `hb_mapper infer` for quantized ONNX:

```bash
hb_mapper infer --config config.yaml \
  --model-file <prefix>_quantized_model.onnx \
  --model-type onnx \
  --image-file <input_node_name> sample.rgbchw \
  --input-layout NCHW \
  --output-dir infer_out/
```

## Use hb_verifier

Use simulator mode for quick checks:

```bash
hb_verifier -m <prefix>_quantized_model.onnx,<prefix>.bin -s True -i sample.rgbchw
```

Use board mode when simulator results look acceptable but board results differ.

## Manual Cosine Script

```python
import numpy as np

def cosine(a, b, eps=1e-12):
    a = np.asarray(a).reshape(-1).astype(np.float64)
    b = np.asarray(b).reshape(-1).astype(np.float64)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + eps))
```

Compare matching output tensors only. For detection models, compare decoded
outputs and task metrics too, because raw head tensors may be sensitive to
small numeric shifts.

## Accuracy Debug Order

1. Verify input preprocessing and calibration file size.
2. Compare original float ONNX vs optimized float ONNX.
3. Compare optimized float ONNX vs quantized ONNX.
4. Compare quantized ONNX vs `.bin` simulator.
5. Compare simulator vs board runtime.

This order identifies whether the issue is graph optimization, quantization,
compilation, or board integration.

## Report Template

When asking for help, include:

- OpenExplorer version and board runtime version.
- ONNX opset and model input/output names.
- YAML file.
- Calibration sample count and preparation script.
- Checker, makertbin, verifier, and perf logs.
- Cosine table per output tensor.
- Task metric before and after quantization.
