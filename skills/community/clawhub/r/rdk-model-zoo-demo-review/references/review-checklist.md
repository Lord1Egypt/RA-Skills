# Review Checklist

Use this checklist when reviewing a sample under `samples/` in `rdk_model_zoo_mc_rdkx5` or `rdk_model_zoo_mc_rdks`.

## 1. Rule Sources

Review in this precedence order:

1. Target branch `docs/Model_Zoo_Repository_Guidelines.md`.
2. Target branch `docs/README.md` and `docs/source_reference/README.md` for documentation and generated source-reference expectations.
3. Target branch `README.md` and `README_cn.md` platform, directory tree, and model list claims.
4. Actual filesystem and code in the target sample.
5. Closest sibling sample in the same branch and family.
6. `sample_template` skeleton.

If sources conflict:

- filesystem and code beat README claims for evidence
- repository guideline beats template wording
- target branch convention beats the other branch's convention
- stable family convention beats guesswork

Before writing findings, inspect the full target sample file list. The review must catch unexpected files, not just missing required files. For vision samples, also inspect root README indexes and `samples/vision/README*` indexes when present or expected.

## 2. Branch And Platform Fit

For `rdk_model_zoo_mc_rdkx5`:

- Accept `.bin` model artifacts and paths.
- Expect X5-specific docs and examples.
- Do not require S100 / S100P / S600 SoC path handling.
- Do not require C++ runtime when the sample is Python-only and docs say so.

For `rdk_model_zoo_mc_rdks`:

- Expect `.hbm` model artifacts in runtime docs and defaults for vision/llm/vla samples.
- Speech samples may legitimately use `.bin` (e.g. `paraformer` INT16 artifacts) — accept when documented, do not flag the suffix alone.
- Check board support claims for S100 / S100P / S600.
- Check SoC-specific paths and detection logic when multi-board support is claimed.
- Check OpenExplorer/OE Docker/toolchain references when conversion is documented.

Flag when:

- model suffix or default path contradicts the branch convention
- sample claims unsupported boards
- docs mix X5 and RDK S instructions without explanation

## 3. Directory Structure

Normalized sample roots generally contain:

- `README.md`
- `README_cn.md`
- `conversion/`
- `evaluator/`
- `model/`
- `runtime/`
- `test_data/`

Conventions:

- `runtime/` may include `python/`, `cpp/`, or both.
- Python-only samples are acceptable when docs clearly say Python only.
- `model/` usually contains `download_model.sh` and model READMEs.
- `test_data/` usually contains example inputs, labels, or result images.
- Legacy or lightly migrated samples may be monolingual; flag missing bilingual parity only when standardization is expected or the sample already has both languages partially.

Flag when:

- required sample content is placed in arbitrary new top-level folders
- top-level README lists directories that do not exist
- conversion/evaluator/model/runtime content is mixed into the wrong directory without reason
- generated outputs, caches, temporary files, personal notes, debug dumps, notebooks, archives, compiled binaries, or unrelated assets are mixed into sample directories
- files exist outside the standard layout without a documented task-family reason

## 4. Naming Rules

Hard requirements from repository guidelines:

- Entry program must be named `main`:
  - Python: `main.py`
  - C/C++: `main.cc` (preferred; `main.cpp` is also acceptable — do not flag a compliant sample for using one extension over the other, but header/source file names must match each other)
- One-click script must be named `run.sh`.
- Model wrapper files should use the model or task name.
- C/C++ header/source names should match the model name.

Accepted variants:

- Single-task wrappers: `mobilenetv1.py`, `convnext.py`, `yolov5.py`, `yolov5_det.py`.
- Multi-task wrappers: `yolo26_det.py`, `yolo26_seg.py`, `yolo26_pose.py`, `yolo26_obb.py`, `yolo26_cls.py`.
- Speech wrappers: model/task-specific names such as `kws.py` or `asr.py`.

Model naming:

- RDK S docs commonly use `<model_name>_<input_resolution>_<chip_or_soc>... .hbm`.
- X5 samples commonly use `.bin`; do not flag `.bin` by itself in X5.

## 5. Top-Level README Review

Check `README.md` and `README_cn.md` where present.

Expected normalized sections:

- language switch first when bilingual
- model title
- short sample-scope paragraph
- algorithm overview/introduction
- algorithm capabilities
- algorithm features when meaningful
- platform compatibility or platform notes when board support matters
- directory structure
- quick start
- model conversion
- runtime / model inference
- model evaluation
- result, performance data, or validation status when data exists
- license

Flag when:

- README contains placeholders (`TODO`, `待补充`, `Content to be added`)
- top-level docs duplicate detailed runtime parameter tables instead of linking to runtime docs
- public docs describe migration mechanics rather than current usage
- English and Chinese docs materially disagree
- quick start cannot be followed from the documented path

## 5A. Repository And Vision Index Synchronization

For any vision sample addition, deletion, rename, move, category change, model-name change, or platform-support change, check these files:

- repository root `README.md`
- repository root `README_cn.md`
- `samples/vision/README.md` when present or expected
- `samples/vision/README_cn.md` when present or expected

Required checks:

- Root README model list contains the sample with correct category, model name, path, supported platform, and detail link.
- Root README directory structure includes the sample path when that section enumerates vision samples.
- `samples/vision/README*` exists or is updated when the branch/task requires a vision-directory index.
- Vision README entries match root README vision entries for category, model name, path, supported platform, and detail link.
- English and Chinese versions are synchronized semantically.
- Links resolve to actual sample directories.

Flag when:

- a new or changed vision sample is documented only in its own folder
- root README is updated but `samples/vision/README*` is missing or stale when a vision index is required
- `samples/vision/README*` lists samples not present in root README or filesystem
- category/platform/path/detail-link data differs between root README and vision README
- English and Chinese index files are out of sync

## 6. Conversion Review

Check `conversion/README*` and every file under `conversion/`.

Accept:

- lightweight conversion docs when precompiled models are supplied and top-level docs are not misleading
- ONNX export scripts and mapping utilities under `conversion/`
- necessary Python scripts and reference YAML/config files used by conversion

Flag when:

- conversion docs are placeholders
- original conversion commands or source references were lost during migration
- RDK S conversion docs omit OpenExplorer/OE Docker/toolchain entry points while explaining conversion
- X5 conversion docs incorrectly reference RDK S-only toolchain paths or model suffixes
- `conversion/` contains files outside its role: datasets, quantized model files, ONNX exports, `.bin`, `.hbm`, result images, logs, caches, notebooks, archives, unrelated shell scripts, or temporary files
- special-case extra conversion files exist but are not explained in README or by a clear sibling-sample convention

## 7. Evaluator Review

Check `evaluator/README*` and evaluation scripts.

Accept:

- lightweight docs when the top-level README only points to evaluator details
- family-specific evaluator scripts such as per-task YOLO evaluation scripts

Flag when:

- evaluator docs are placeholders
- README claims accuracy/performance evaluation but no method or script exists
- benchmark/result tables lack enough context to identify platform/model/input

## 8. Model Directory Review

Check `model/README*` and `download_model.sh`.

Flag when:

- download script name is wrong or undocumented
- quantized model download address is missing from both `download_model.sh` and `model/README*`
- `model/README*` does not tell users how to obtain the quantized model
- model README lists files that do not match script output
- default model paths in runtime docs are inconsistent with model docs
- branch-specific suffix is wrong (`.bin` for RDK S without reason, `.hbm` for X5 without reason)
- model binaries are checked into a sample without a documented reason instead of being downloaded through the model directory flow

## 9. Python Runtime Review

Check `runtime/python/`.

Hard expectations:

- `main.py` exists.
- `run.sh` exists when quick start documents one-click execution.
- Runtime README exists.
- `main.py` uses `argparse.ArgumentParser` for CLI samples.
- Arguments use kebab-case, default-runnable values, and `type`, `default`, `help`.
- Model code separates config from model logic.
- Shared helper behavior should prefer existing `utils/py_utils` implementations when available.

Model class should cover, as applicable:

- initialization and metadata/model loading
- preprocessing
- inference / forward
- postprocessing
- predict or callable flow

Runtime README should include:

- dependency or environment notes
- directory structure
- argument table or equivalent CLI explanation
- `run.sh` quick start
- direct `python3 main.py ...` example
- output path/result description

Flag when:

- README and `main.py` defaults disagree
- `run.sh` invokes different paths, models, or tasks from the docs
- multi-task `main.py` supports tasks not documented by runtime README
- sample-local code duplicates existing repository utilities for preprocessing, postprocessing, visualization, tensor conversion, runtime setup, image/audio handling, or common math without a clear reason
- sample imports or copies ad-hoc helper files that belong under `utils/py_utils`

## 10. C/C++ Runtime Review

Only apply when C/C++ files exist or docs claim C++ support.

Expected structure:

- `CMakeLists.txt`
- `run.sh`
- `inc/<model>.hpp`
- `src/<model>.cpp` or `.cc`
- `src/main.cc` (or `src/main.cpp`)
- runtime README

Hard expectations:

- documented build/run commands match actual files
- C++ model implementation/header names match
- public types and functions use Doxygen-style comments when code is intended as maintained sample code
- shared helper behavior should prefer existing `utils/c_utils` implementations when available

Flag when:

- top-level docs claim ready C++ runtime but only placeholders exist
- CMake or `run.sh` references missing files
- default C++ model path conflicts with Python/model docs without explanation
- sample-local code duplicates existing repository utilities for common preprocessing, postprocessing, memory alignment, tensor handling, visualization, or runtime setup without a clear reason

## 11. Comment And Docstring Review

Python expectations from guidelines:

- Google-style docstrings for public classes and methods.
- Classes and main model methods documented.
- Complex flows use short comments.
- Inline comments are concise and preferably English in code.
- Every externally visible `.py` file has a top-level module docstring, except shebang/encoding.
- Every public Python function/method has a meaningful docstring unless it is a trivial private helper; do not overlook missing docs in `main.py` or model wrappers.
- `Args` and `Returns` describe semantics, not just variable names; complex return structures describe fields.

C/C++ expectations:

- Doxygen-style file/type/function comments for public sample interfaces.
- File comment before includes when following the guideline examples.
- Public struct/class members and public fields have comments.

Flag when:

- module, class, public method/function, public C/C++ type, or public C/C++ function comments are missing
- comments are vague, stale, copied from another model, or inconsistent with current code
- complex preprocessing/postprocessing lacks step comments

Do not over-flag:

- private, tiny, obvious helpers with short comments
- generated or third-party code excluded from sample interface review

## 12. Cross-Document Consistency

Always check:

- top-level README versus actual directories
- root `README*` model list and directory tree versus actual sample directories
- `samples/vision/README*` versus root README vision entries and actual `samples/vision` directories
- full sample file list versus standard layout and family-specific allowed files
- runtime README versus `main.py`
- runtime README versus `run.sh`
- model README versus `download_model.sh`
- `model/README*` and `download_model.sh` versus quantized model download URL
- conversion/evaluator claims versus actual files
- English versus Chinese docs
- branch README platform claims versus sample platform claims
- sample-local helper code versus existing `utils/py_utils` and `utils/c_utils`

Known regression patterns:

- default model path mismatch between `main.py` and `run.sh`
- output result path mismatch
- wrong visualization/result file names
- wrong `.bin`/`.hbm` suffix for branch context
- stale branch names or migration-history wording in public docs
- unexpected files in `conversion/` or sample root
- missing quantized model download address
- duplicated utility implementations instead of using `utils`
- missing mandatory docstrings/comments
- missing or stale root README model-list/directory-tree entry for a vision sample
- missing or stale `samples/vision/README*` index entry for a vision sample
- mismatch between root README and vision README category, platform, path, or detail link

## 13. Severity Guidance

Use `blocking` when:

- required runnable entry is missing (`main.py`, `main.cc`/`main.cpp`, or documented `run.sh`)
- docs claim a runtime path or language that does not exist
- documented default execution cannot work because paths or file names are wrong
- wrapper is missing core inference stages
- branch/platform model artifact assumptions make the sample unusable
- sample includes non-standard files that break packaging or user execution
- model download path is absent and the runtime cannot obtain the quantized model
- README index links point to missing directories or materially wrong sample paths

Use `major` when:

- README sections exist but are materially incomplete or misleading
- code defaults and docs are inconsistent but easy to fix
- conversion/evaluator docs are placeholders
- comment/docstring coverage is incomplete on public pipeline code
- runtime README omits task-switch usage for a multi-task sample
- conversion contains extra non-standard files with no explanation but they do not directly break runtime
- sample duplicates existing `utils` behavior without justification
- root README or `samples/vision/README*` index is missing or stale for a new/changed vision sample

Use `minor` when:

- bilingual parity is incomplete but not misleading
- sample-family convention is missing without breaking usage
- formatting or wording reduces clarity but not correctness
- template shape differs for a defensible local reason but docs should clarify it
