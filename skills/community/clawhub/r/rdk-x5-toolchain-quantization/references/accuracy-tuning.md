# Accuracy Tuning

Use this reference when the model compiles but cosine similarity or task metrics
drop after PTQ.

## First Checks

Before tuning algorithms, rule out data and configuration mistakes:

1. Calibration files have the expected byte size.
2. Calibration samples are representative and not all near-duplicates.
3. Resize, crop, padding, channel order, and layout match training.
4. Normalization is applied exactly once.
5. `input_type_rt`, `input_type_train`, and `input_layout_train` are correct.
6. ONNX outputs are the tensors you expect to compare.

Most severe accuracy drops come from one of these issues.

## Calibration Algorithm Search

Try a small controlled sweep:

```yaml
calibration_parameters:
  calibration_type: "default"
```

Then test:

- `mix`
- `kl`
- `max`

Keep everything else fixed. Record cosine and task metrics for each run.

## Sensitive Operator Strategy

If only a small number of layers cause the drop, make targeted overrides rather
than weakening the whole graph.

Typical sensitive areas:

- First and last layers.
- Small-range logits.
- Softmax inputs/outputs.
- Detection heads.
- Depthwise convolutions after aggressive activation clipping.
- LayerNorm / attention-adjacent nodes in Transformer-like models.

Use `node_info` to force higher precision or alternate behavior where supported
by the toolchain version.

## Featuremap Fallback

Use featuremap calibration when image preprocessing is too difficult to
represent accurately in YAML. Dump the exact tensor that enters the ONNX model
from the floating-point pipeline and use those raw tensors for calibration.

This is especially useful for:

- Non-image models.
- Multi-stage pipelines.
- Custom preprocessing implemented outside OpenExplorer.
- Models trained with letterbox or unusual normalization.

## Output Interpretation

Detection models can show low raw-head cosine while decoded boxes remain
acceptable, or high raw cosine while NMS/task metrics fail. Always check decoded
outputs and task metrics.

For classification, top-k agreement and confidence deltas are useful in addition
to cosine.

## Debugging Layer By Layer

If logs and artifacts include layer dumps:

1. Compare float and quantized outputs layer by layer.
2. Find the first layer where cosine sharply drops.
3. Inspect the preceding activation range and operator type.
4. Try higher precision or fallback on the smallest affected region.
5. Rebuild and re-measure full-model metrics.

Avoid broad CPU fallback unless latency is not important.

## Calibration Sample Selection

Use samples that cover:

- Common lighting/background conditions.
- Typical object scales and aspect ratios.
- Edge cases that happen in production.
- Class diversity for classification or detection.

Avoid:

- All blank/simple images.
- Only hard failure cases.
- Augmented images that are not deployment-like.
- Mixing incompatible preprocessing variants.

## Common Fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Cosine near zero | Wrong input layout, dtype, or normalization | Rebuild calibration files and YAML. |
| First layer diverges | RGB/BGR or scale mismatch | Check channel order and `scale_value`. |
| Final logits unstable | Sensitive output head | Try node-level precision override. |
| Detection boxes shifted | Letterbox/resize mismatch | Match training preprocessing exactly. |
| Simulator OK, board bad | Runtime integration mismatch | Check board runtime, input format, and stride. |
| Good cosine, poor mAP | Postprocessing mismatch | Verify decode, anchors, strides, NMS, and thresholds. |

## Stop Criteria

Stop tuning when:

- Task metrics meet product requirements.
- Cosine gates are stable across representative validation samples.
- Latency remains within budget.
- Remaining differences are understood and documented.
