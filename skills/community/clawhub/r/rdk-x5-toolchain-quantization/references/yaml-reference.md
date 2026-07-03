# YAML Reference

This reference summarizes the fields most often needed for RDK X5 OpenExplorer
PTQ. Field availability can vary by OpenExplorer release; prefer the official
OE v1.2.8 documentation when a field behaves differently.

## Minimal Template

```yaml
model_parameters:
  onnx_model: "./your_model.onnx"
  march: "bayes-e"
  layer_out_dump: false
  working_dir: "bpu_model_output"
  output_model_file_prefix: "your_model_bayese"

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

## model_parameters

| Field | Purpose |
|---|---|
| `onnx_model` | Path to the source ONNX model. |
| `march` | Target architecture. Use `bayes-e` for RDK X5. |
| `working_dir` | Directory for generated artifacts. |
| `output_model_file_prefix` | Prefix for `.bin`, quantized ONNX, reports, and logs. |
| `layer_out_dump` | Enable layer dumps for debugging; disable for normal builds. |

## input_parameters

| Field | Purpose |
|---|---|
| `input_name` | ONNX input name. Empty string lets the tool infer it for simple single-input models. |
| `input_type_rt` | Runtime input format consumed by the board application. |
| `input_type_train` | Format used by the floating-point training pipeline. |
| `input_layout_train` | Usually `NCHW` or `NHWC`. |
| `norm_type` | Normalization strategy applied by `hb_mapper`. |
| `scale_value` | Commonly `1/255`; adjust to match training. |
| `mean_value` | Use if training subtracts mean values. |

## Input Type Matrix

| Deployment path | `input_type_rt` | `input_type_train` | Notes |
|---|---|---|---|
| Camera/video pipeline | `nv12` | `rgb` or `bgr` | Common X5 path. Let YAML handle conversion and normalization. |
| Tensor input from app | `rgb` | `rgb` | Use only if the app feeds RGB. |
| Tensor input from app | `bgr` | `bgr` | Use only if the app feeds BGR. |
| Custom tensor/features | `featuremap` | `featuremap` | Use for precomputed features or complex preprocessing. |

## calibration_parameters

| Field | Purpose |
|---|---|
| `cal_data_dir` | Directory containing raw calibration tensors. |
| `cal_data_type` | Tensor dtype such as `float32` or `uint8`. |
| `calibration_type` | Quantization range algorithm. Start with `default`; try `mix`, `kl`, or `max` for accuracy issues. |
| `optimization` | Optional quantization/graph optimizations. |

Recommended starting point:

```yaml
calibration_type: "default"
optimization: set_Softmax_input_int8,set_Softmax_output_int8
```

If cosine drops badly:

1. Verify preprocessing and file sizes.
2. Try `calibration_type: "mix"`.
3. Try `calibration_type: "kl"` or `max`.
4. Add `node_info` for sensitive operators.
5. Use featuremap calibration if input preprocessing is too complex.

## compiler_parameters

| Field | Purpose |
|---|---|
| `jobs` | Parallel compile workers. Use CPU core count as a starting point. |
| `compile_mode` | `latency` for speed; `bandwidth` for memory/bandwidth tradeoffs. |
| `optimize_level` | Usually `O3` for final builds. |
| `debug` | Keep debug artifacts and reports. |

## node_info

Use `node_info` to override quantization behavior for sensitive nodes. Typical
uses include forcing higher precision on numerically fragile layers or moving an
operator to CPU when BPU quantization is unacceptable.

Example shape:

```yaml
calibration_parameters:
  node_info:
    sensitive_node_name:
      OutputType: int16
```

Node names must match the graph after optimization. Use dumped graph artifacts
or log output to identify the correct names.

## CPU Fallback

CPU fallback can unblock unsupported or accuracy-sensitive operators, but it may
hurt latency. Use it surgically and re-run `hb_perf`.

Typical flow:

1. Run `hb_mapper checker`.
2. Identify unsupported or poor-accuracy nodes.
3. Add the minimal fallback rule.
4. Rebuild and compare latency and cosine.

## YAML Debug Checklist

- Paths are relative to the current working directory used inside Docker.
- ONNX input names match YAML.
- Input layout and type match calibration files.
- `scale_value` and `mean_value` are not applied twice.
- `march` is `bayes-e`.
- Output prefix does not contain spaces or non-ASCII characters.
