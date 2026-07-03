# Troubleshooting

This reference lists common failures in the RDK X5 OpenExplorer PTQ workflow.

## hb_mapper checker Reports Unsupported Operators

Actions:

1. Read `hb_mapper_checker.log` and identify exact operator names.
2. Check whether the unsupported op can be replaced with an equivalent supported pattern.
3. Export ONNX with a different opset if the exporter introduced unsupported forms.
4. Use custom operator registration only when rewrite is not practical.
5. Use CPU fallback only for the smallest necessary region.

After changes, run checker again before attempting `makertbin`.

## makertbin Fails Immediately

Likely causes:

- Wrong path inside Docker.
- YAML indentation or quoting error.
- ONNX input name mismatch.
- Unsupported model ops missed by checker.
- Output directory permission issue.

Actions:

```bash
pwd
ls -lah
python - <<'PY'
import yaml
print(yaml.safe_load(open("config.yaml", encoding="utf-8")))
PY
```

Then re-run with a simple ASCII path and inspect `hb_mapper_makertbin.log`.

## Calibration Data Shape Error

Likely causes:

- Wrong H/W/C/N dimensions.
- `NCHW` vs `NHWC` mismatch.
- `float32` vs `uint8` mismatch.
- `.npy` file used instead of raw bytes.
- Multi-input sample counts not aligned.

Verify file sizes:

```python
from pathlib import Path
for p in Path("calibration_data").iterdir():
    print(p.name, p.stat().st_size)
```

## Cosine Similarity Is Very Low

Use this order:

1. Check RGB/BGR order.
2. Check normalization is not applied twice.
3. Check resize/letterbox/padding.
4. Check calibration sample representativeness.
5. Try `calibration_type: mix`, then `kl` or `max`.
6. Use `node_info` for sensitive layers.
7. Try featuremap calibration.

See `accuracy-tuning.md` for the full workflow.

## hb_mapper infer Fails On Quantized ONNX

Do not use plain `onnxruntime` for Horizon quantized ONNX. Use:

```bash
hb_mapper infer --config config.yaml \
  --model-file <prefix>_quantized_model.onnx \
  --model-type onnx \
  --image-file <input_node_name> sample.rgbchw \
  --input-layout NCHW \
  --output-dir infer_out/
```

If it still fails, confirm that input node names, tensor layout, and sample file
sizes match YAML.

## Board Runtime Cannot Load .bin

Likely causes:

- Runtime/toolchain version mismatch.
- File copied incompletely.
- Wrong chip target.
- Board runtime lacks required support for the generated model.

Actions:

```bash
hrt_model_exec model_info --model_file=<prefix>.bin
hrt_model_exec perf --model_file=<prefix>.bin --core_id=0 --thread_num=1
```

Confirm `march: bayes-e` and check board runtime version.

## hrt_model_exec Argument Errors

Use underscores:

```bash
hrt_model_exec perf --model_file=model.bin --core_id=0 --thread_num=1
```

Do not use:

```bash
hrt_model_exec perf --model-file=model.bin --core-id=0
```

## Good Simulator Results, Bad Board Results

Check:

- Board-side input format and stride.
- Whether app preprocessing matches calibration preprocessing.
- Runtime version compatibility.
- Whether the app reads output tensors in the correct order.
- Postprocessing thresholds, anchors, strides, and NMS.

Dump board input tensors if possible and compare them with the simulator input.

## Good Cosine, Bad Task Metrics

Likely causes:

- Postprocessing mismatch.
- Wrong output tensor order.
- Anchor/stride mismatch.
- Different confidence or NMS thresholds.
- Comparing raw heads instead of decoded outputs.

Run a small validation set and compare decoded outputs, not only raw tensors.

## Slow Model

Actions:

1. Run `hb_perf`.
2. Inspect BPU/CPU operator placement.
3. Remove avoidable CPU fallback.
4. Try graph rewrite for hotspot operators.
5. Test `compile_mode: bandwidth` if memory bandwidth dominates.
6. Measure board-side preprocessing and postprocessing separately.

## Environment Problems

If Docker or tool binaries are missing:

- Confirm the OE v1.2.8 image is loaded.
- Confirm the project directory is mounted into the container.
- Avoid paths with spaces or non-ASCII characters.
- Check Python version and package conflicts inside the container.
- Recreate the container from a clean image if environment drift is suspected.
