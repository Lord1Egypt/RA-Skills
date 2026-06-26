# Integration Notes

## Preprocessing checklist

Always confirm:
- input tensor shape, usually `[1, height, width, channels]`
- channel order, usually RGB
- dtype: `uint8`, `int8`, or `float32`
- normalization: none, `[0,1]`, `[-1,1]`, or model-specific mean/std
- resize policy: direct resize, letterbox, or center crop

Do not guess these from model family alone if the artifact page documents them explicitly.

## Classification outputs

Common patterns:
- logits vector
- probabilities vector
- top-k labels through task library metadata

Verify whether softmax is already applied.

## Detection outputs

Common patterns:
- boxes tensor
- classes tensor
- scores tensor
- detection count tensor

Or a single fused tensor in some YOLO exports.

Always define:
- score threshold
- IoU / NMS threshold
- class label mapping
- coordinate convention: normalized vs pixel

## Quantized models

For `uint8` or `int8` models, inspect quantization parameters if raw interpreter output is used. Task libraries may handle this automatically.

Quantized models are usually the safest default for CPU-bound, always-on camera features.

## Metadata

If model metadata exists, use it. It often provides:
- label file association
- normalization hints
- task-library compatibility

If metadata is missing, capture the equivalent assumptions explicitly in code or config.

## Runtime risk factors

Watch for:
- unsupported custom ops
- delegate-specific behavior differences
- exporter-specific YOLO tensor formats
- mismatch between label files and class count
- wrong image orientation from camera pipeline

## Validation ritual

Before declaring a model “integrated,” run at least:
1. one obvious positive image
2. one near-miss image
3. one negative image

Check that confidence scores and false positives are reasonable. A model that technically runs but needs brittle thresholds is a weak default recommendation.
