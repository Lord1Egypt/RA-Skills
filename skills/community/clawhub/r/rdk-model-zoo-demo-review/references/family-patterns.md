# Family Patterns

Use this file to avoid false positives when a sample follows a valid branch or family-specific pattern.

## X3 Branch Pattern

Applies under `rdk_model_zoo_mc_rdkx3` (RDK X3, Bernoulli2).

Characteristics:

- RDK X3 branch, migrated from the legacy `demos/` layout to the standardized `samples/vision/` structure (same target shape as `rdk_x5`).
- Runtime artifacts are commonly `.bin`; Python runtime uses `hbm_runtime`.
- **Python-only runtime is the norm** — no maintained C++ runtime on this branch.
- BPU alignment on X3 is 32 bytes (X5/S are 64 bytes) — preprocessing and tensor-alignment code must be X3-aware.
- Root README is the primary model index; `samples/vision/README*` may be absent if the branch has chosen root README-only indexing.

Accept:

- Python-only samples with no `runtime/cpp/` directory, even without an explicit "Python only" note, as long as docs do not claim C++.
- Missing `samples/vision/README*` when the root README carries the full model index.
- X3-specific download URLs, model paths, and 32-byte alignment handling in preprocessing code.

Flag:

- 64-byte BPU alignment assumptions copied from X5/RDK S code or `utils/py_utils` without X3 adaptation (a known source of silent numeric errors on X3).
- C++ runtime claims in docs with no working `runtime/cpp` implementation.
- Legacy `demos/` layout, PascalCase sample directory names, or notebook (`.ipynb`) entry points presented as the maintained sample structure after the standardization migration.
- X5/RDK S-specific model suffixes, SoC detection logic, or toolchain references copied into X3 docs without explanation.

## X5 Branch Pattern

Applies under `rdk_model_zoo_mc_rdkx5`.

Characteristics:

- RDK X5 main delivery branch.
- Runtime artifacts are commonly `.bin`.
- Python runtime commonly uses `hbm_runtime`.
- Many samples are Python-only.
- Sample root docs are often bilingual and use the Model Zoo normalized flow.

Accept:

- `.bin` model suffixes.
- Python-only implementation when docs do not claim C++.
- X5-specific download URLs and model paths.

Flag:

- RDK S-only `.hbm` or SoC path assumptions copied into X5 docs without explanation.
- C++ runtime claims with no working `runtime/cpp` implementation.
- Vision samples missing from root README and required `samples/vision/README*` indexes.

## RDK S Branch Pattern

Applies under `rdk_model_zoo_mc_rdks`.

Characteristics:

- RDK S branch for S100 / S100P / S600.
- Runtime artifacts are commonly `.hbm`.
- Samples may need SoC-specific paths or runtime detection.
- Conversion docs should point users to OpenExplorer/OE Docker/toolchain docs when conversion is described.
- Contains vision, speech, and VLA categories.

Accept:

- Board-specific model folders such as `s100`, `s100p`, or `s600`.
- Runtime defaults that derive SoC at runtime.
- Python-only or Python+C++ depending on the sample family.
- `.bin` model files in speech samples (e.g. `paraformer` uses INT16 quantized artifacts with a `.bin` suffix) — `.hbm` is the default for vision/llm/vla, not a hard rule for speech.

Flag:

- `.bin` paths copied from X5 without a clear exception.
- Missing SoC consistency when README claims multiple boards.
- Conversion docs that explain conversion but omit OE entry points.
- Vision samples missing from root README and required `samples/vision/README*` indexes.

## Classification Pattern

Representative samples: `mobilenetv1`, `convnext`, `efficientnet`.

Characteristics:

- Classification-only sample.
- Runtime output is top-k class/probability, not boxes or masks.
- Usually one Python wrapper.
- C++ may be absent or present depending on branch/sample.

Accept:

- one `main.py`
- one model wrapper such as `mobilenetv1.py` or `convnext.py`
- Python-only implementation when documented that way

Flag:

- detection/segmentation result wording copied into classification docs
- top-level docs implying ready C++ runtime when only Python exists

## YOLO Detection Pattern

Representative sample: `yolov5`.

Characteristics:

- Single detection task.
- `run.sh` may auto-download or check the default model.
- Runtime output is boxes/classes/scores and a result image.
- Some branches include both Python and C++ runtime.

Accept:

- one `main.py`
- one wrapper such as `yolov5.py` or `yolov5_det.py`
- Python-only or Python+C++ depending on target branch

Flag:

- README and code disagree on default model, image path, result path, or thresholds
- C++ docs/build files missing when C++ support is claimed

## Multi-Task YOLO Pattern

Representative samples: `ultralytics_yolo`, `ultralytics_yolo26`.

Characteristics:

- One `main.py` dispatches by task, often with `--task`.
- Separate wrappers may exist for detect, seg, pose, cls, and obb.
- Runtime README documents task switching and multiple examples.
- `run.sh` may default to one representative task or accept a task argument.

Accept:

- one shared `main.py`
- multiple task wrappers
- per-task result image names

Flag:

- supported tasks in code are not documented
- top-level README claims tasks not implemented
- `run.sh` task defaults conflict with README examples

## Segmentation / Lane / Depth Pattern

Representative samples: `lanenet`, `unetmobilenet`, `depth_anything_v2`.

Characteristics:

- Output may be masks, lane maps, or dense prediction images.
- Result files can include multiple visualization images.
- C++ runtime may exist for some samples.

Accept:

- task-specific output structures rather than detection-style boxes
- multiple result images in `test_data/`

Flag:

- copied detection parameter names or result descriptions that do not match the task
- missing explanation for multiple output files

## Speech Pattern

Representative samples in RDK S: `samples/speech/kws`, `samples/speech/asr`.

Characteristics:

- Input is usually audio rather than image.
- Runtime docs should describe audio sample path, sample rate/format when relevant, and model output meaning.
- Python runtime is common.

Accept:

- no image result screenshot when audio output is textual/classification-like
- audio-specific `test_data` files such as `.wav`

Flag:

- image-specific template text left in speech docs
- missing audio input/default path documentation

## `sample_template` Pattern

Purpose:

- baseline skeleton
- documentation structure target
- placeholder C++ and Python runtime docs

Use it as a shape template, not as a strict implementation oracle.

Do not flag a real sample solely because:

- it does not implement both Python and C++
- X5 uses `.bin` instead of `.hbm`
- RDK S uses SoC-specific model directories
- it adds family-specific scripts under `conversion/` or `evaluator/`

Still flag a real sample when:

- extra files are not part of a known family pattern and are not explained
- `conversion/` contains generated artifacts, model binaries, logs, caches, notebooks, or unrelated assets
- `model/` lacks a quantized model download URL or `download_model.sh` flow
- sample-local code duplicates available `utils/py_utils` or `utils/c_utils` helpers without a clear reason
- maintained public code omits required module/class/function or Doxygen comments
- root README and `samples/vision/README*` indexes are missing, stale, or inconsistent for vision samples
