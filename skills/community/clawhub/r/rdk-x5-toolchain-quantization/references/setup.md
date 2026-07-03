# OpenExplorer Setup For RDK X5

This reference covers the environment required to run the RDK X5 PTQ workflow.
The target toolchain is D-Robotics / Horizon Robotics OpenExplorer **v1.2.8
(Python 3.10)** with X5 `bayes-e` compilation.

## Required Tools

Run the following tools inside the OpenExplorer Docker container:

- `hb_mapper checker`
- `hb_mapper makertbin`
- `hb_mapper infer`
- `hb_verifier`
- `hb_perf`

Run `hrt_model_exec` on the RDK X5 board after copying the compiled `.bin`.

## Recommended Layout

```text
project/
  model/
    your_model.onnx
  calibration_data/
    sample_000.rgbchw
  config.yaml
  bpu_model_output/
```

Keep paths simple and ASCII-only when possible. Some versions of the toolchain
are fragile around spaces, non-ASCII paths, and network-mounted directories.

## Docker Checklist

1. Pull or load the OE v1.2.8 Docker image supplied by D-Robotics.
2. Mount your project directory into the container.
3. Confirm the container can see your ONNX model and calibration files.
4. Confirm `hb_mapper --help`, `hb_perf --help`, and `python --version` work.
5. Use the CPU image unless you specifically need GPU utilities for data preparation.

Example:

```bash
docker run --rm -it \
  -v "$PWD:/workspace" \
  -w /workspace \
  <openexplorer-image>:v1.2.8 \
  bash
```

## Board Checklist

1. Copy `<prefix>.bin` and test inputs to the RDK X5 board.
2. Confirm the board runtime version matches the model toolchain family.
3. Run `hrt_model_exec model_info --model_file=<prefix>.bin`.
4. Run `hrt_model_exec perf --model_file=<prefix>.bin --core_id=0 --thread_num=1`.

Use `scp`, removable media, or your normal deployment path. Keep board and
toolchain versions aligned before investigating model-level issues.

## Version Alignment

Use the same major OpenExplorer/toolchain family for compilation and runtime.
If the board runtime is older than the compiler, symptoms may include model load
failure, unsupported segment errors, or unexpected output differences.

Record these values in bug reports:

```bash
hb_mapper --version
hb_perf --version
hrt_model_exec --version
uname -a
```

## Quick Smoke Test

```bash
hb_mapper checker --model-type onnx --march bayes-e --model ./model/your_model.onnx
hb_mapper makertbin --config config.yaml --model-type onnx
hb_perf bpu_model_output/<prefix>.bin
```

If the checker fails, fix ONNX compatibility first. If `makertbin` fails after
checker passes, inspect YAML, calibration data, and tensor shapes.
