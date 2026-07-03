# Performance Profiling

Use this reference when the compiled model is slower than expected, BPU
utilization is low, or board latency differs from compile-time estimates.

## Compile-Time Profiling

Run in the OpenExplorer Docker container:

```bash
hb_perf <prefix>.bin
```

Inspect the generated HTML report under `hb_perf_result/`. Focus on:

- BPU utilization.
- Operator placement on BPU vs CPU.
- Per-layer latency hotspots.
- Memory bandwidth pressure.
- Input/output tensor conversion overhead.

## Board Profiling

Run on the RDK X5 board:

```bash
hrt_model_exec perf --model_file=<prefix>.bin --core_id=0 --thread_num=1 --profile_path="."
```

Use underscore-style argument names. Many examples online accidentally use
hyphens; `hrt_model_exec` expects underscores.

## Common Latency Causes

| Symptom | Likely cause | Action |
|---|---|---|
| Low BPU utilization | CPU fallback or unsupported ops | Read checker report and reduce fallback. |
| High input overhead | Runtime format mismatch | Feed the format expected by `input_type_rt`. |
| Good hb_perf, bad board latency | Runtime/app integration issue | Profile preprocessing, copy, and postprocessing. |
| One layer dominates | Poor operator mapping | Try graph rewrite or precision/fallback changes. |
| Memory bandwidth bound | Large feature maps or compile mode | Try `compile_mode: bandwidth` and inspect report. |

## Compiler Settings

Start with:

```yaml
compiler_parameters:
  jobs: 16
  compile_mode: "latency"
  optimize_level: "O3"
  debug: true
```

If bandwidth dominates, test:

```yaml
compile_mode: "bandwidth"
```

Always compare both latency and accuracy after changing compiler options.

## Reduce CPU Fallback

CPU fallback may be necessary for unsupported operators, but it often dominates
latency. To reduce it:

1. Run `hb_mapper checker`.
2. Identify unsupported or CPU-assigned nodes.
3. Rewrite ONNX operators into supported equivalents when possible.
4. Keep fallback limited to the smallest necessary nodes.
5. Re-run `hb_perf` and board profiling.

## End-To-End Timing

`hb_perf` measures model execution characteristics, not the whole application.
For production latency, also measure:

- Camera capture or input loading.
- Resize/color conversion/normalization.
- Tensor copy to runtime.
- Model execution.
- Output copy.
- Decode, NMS, tracking, or other postprocessing.

Keep these timings separate so model-toolchain optimization is not confused with
application optimization.

## Reporting Template

Include:

- `.bin` file name and OpenExplorer version.
- `hb_perf` HTML report.
- `hrt_model_exec perf` output.
- YAML compiler settings.
- Checker operator placement summary.
- Board runtime version and CPU/BPU frequency settings.
