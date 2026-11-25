# Account-free local reconstruction engine

This skill includes executable local inference and preparation tools. They use the public MIT-licensed **TripoSR** model, not a Tripo Studio/Meshy subscription or their private production models. Setup downloads public code and weights; image inference runs locally in offline mode.

TripoSR is a general-object baseline. Its generated side/back surfaces are inferred. Commercial-service parity and reliable portrait likeness are not established. Do not repeat an unsatisfactory result as though a watertight mesh established visual quality. Real multiview fusion and direct text-conditioned inference are not implemented by this backend. At the skill level, an available host image-generation tool can turn a text description into a reviewed clean reference, followed by this local image-to-3D stage. Text-to-functional-model uses the CAD branch.

## Runtime

Use Python 3.11. If installed, `local-runtime.json` in the skill directory identifies this machine's configured interpreter and runtime. Otherwise use the project-local virtual environment and `.runtime/` directory. Runtime files, weights, dependencies and private outputs are separate from the portable skill source.

```sh
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements-local.txt
.venv/bin/python scripts/u1_local.py doctor
.venv/bin/python scripts/u1_local.py setup
```

Setup clones a pinned official TripoSR revision, downloads a public model checkpoint (about 1.68 GB), a small DINO configuration, and human-segmentation weights. Allow several GB for dependencies and working space; setup checks for at least 4 GiB free before downloading model assets. Source and model revisions and hashes are recorded in `.runtime/engine.json`. Copies of upstream licensing remain with the checkout. Downloaded code and dependencies should be installed from the documented official sources.

MPS inference uses PyTorch on Apple Silicon; CPU and CUDA are also selectable when available. Some sandbox contexts cannot see Metal even when the host supports it; check the actual execution context. The isolated adapter calls the upstream TSR API directly, replacing native marching-cubes extraction with a tested CPU implementation and using a pinned local DINO configuration. These changes are recorded. Setup uses OS certificate trust; it does not disable HTTPS verification.

## Generate a volumetric candidate

```sh
.venv/bin/python scripts/u1_local.py generate portrait.jpg \
  --output-dir outputs/candidate-01 --device auto --resolution 192
```

Only one source photo is accepted. Multiple photos are not silently batched as though they were combined into one reconstruction. Use a real multiview backend for that capability.

The pipeline prefers the built Apple Vision helper on macOS (`--segmentation auto`), with explicit `vision`, `human`, and supplied `alpha` modes. It segments the subject locally, saves the alpha mask/cutout for review, crops and pads the foreground, runs trained 3D inference and extracts actual volumetric geometry with generated vertex RGB colors. To use a manually corrected alpha mask, supply an RGBA PNG and `--segmentation alpha`. Inspect hair, ears, glasses and the torso crop in the saved mask; segmentation is not guaranteed perfect.

Outputs include `subject_rgba.png`, `model_input.png`, `master.glb`, `master.ply`, `geometry_normalized.stl`, and `job.json`. The master is colored by vertices, not a baked UV atlas. Model coordinates are normalized until deliberately scaled. No background plaque, hand-traced face or image-luminance relief is substituted. The job remains a candidate pending visual acceptance and later print checks.

Generate records errors and elapsed time. It does not silently retry a failed model or substitute an illustration. If MPS fails, inspect the error and make an explicit CPU retry into a new output directory. Do not call a renderer preview a reconstruction result unless a real mesh was exported.

## Inspect, scale, and prepare colors

Render the actual candidate before accepting it:

```sh
.venv/bin/python scripts/u1_preview.py outputs/candidate-01/master.glb \
  --output-dir outputs/candidate-01/preview
```

The contact sheet and offline orbit viewer show appearance and clay geometry from several source-axis views. Inspect facial shape with color disabled; field/vertex color can make a smooth face look more detailed than its geometry. Preview sampling is labeled and affects display only.

After acceptance, scale and screen it:

```sh
.venv/bin/python scripts/u1_prepare.py outputs/candidate-01/master.glb \
  --output-dir outputs/candidate-01/prepared --height-mm 150 --up-axis z
```

This preserves aspect ratio, places the base at Z=0, centers the model in the nominal U1 envelope, exports a colored master and STL, and records geometry checks and provisional print recommendations. It does not automatically fix likeness, close every hole, add a fused base or determine supports. `--largest-component` is opt-in because it can remove intended eyewear. Exit 1 indicates an exported candidate needs geometry review; exit 2 is invalid input.

Extract target color regions while preserving the original colors:

```sh
.venv/bin/python scripts/u1_color.py outputs/candidate-01/prepared/prepared.glb \
  --output-dir outputs/candidate-01/colors --colors 8
```

This creates a standard color-capable generic 3MF and a target-color report. Perceptual Lab coverage preserves supported minority hues, such as a small face against a large jacket, instead of letting the largest color regions consume the whole palette. The default palette can contain more than four **target** colors; it is not constrained to four solid spools. It does not guess physical mixing ratios. A separate explicit nearest-filament mode can simplify colors if requested.

For native Snapmaker Orca target-color preparation, use the native painted-target adapter after creating an ordinary local baseline project:

```sh
.venv/bin/python scripts/u1_orca_colors.py outputs/candidate-01/colors/prepared_color_regions.3mf \
  --template outputs/candidate-01/slicing/run_0001/project.3mf \
  --output outputs/candidate-01/colors/portrait_orca_targets.3mf
```

The template must be a fresh single-filament, non-mixed project. The adapter rejects calibrated multi-filament or mixed templates before writing anything; it cannot preserve those recipes while replacing the palette. It takes machine/process settings and copies no stale G-code, plate or slice data. It maps target colors to native whole-face paint, with mixed-corner approximations recorded, and retains up to 16 logical target colors. It does not assign those to four physical toolheads or calculate mixing recipes. Actual CLI geometry import was tested; color interpretation in the application and export roundtrip remain unverified. The tested CLI needs `--allow-newer-file` because its internal version string differs from the app version; this flag does not validate colors or a print setup. Calibrated multi-filament projects require the native matching workflow; a recipe-preserving rewrite is not provided by this generic exporter.

Use Full Spectrum Manual Match and review the application colors, then save and reslice a calibrated project in Orca. The baseline CLI adapter rejects unmatched targets, generic/unrecognized 3MFs and native multi-filament/mixed projects, including after a GUI save removes custom markers, to protect their mappings from its single-material override. Confirm size units and final import behavior.

## Local slicing and estimates

```sh
.venv/bin/python scripts/u1_slice.py outputs/candidate-01/prepared/prepared.stl \
  --output-dir outputs/candidate-01/slicing --intent normal \
  --material 'Generic PLA' --supports auto
```

This adapter resolves installed U1 preset inheritance, snapshots the settings, applies a documented process-normalization compatibility fix, runs an isolated local CLI slice and records estimates/transcripts. It never sends a print job. Select the actual material family; Generic PLA is only a provisional test choice. `--mixing` selects the dedicated installed mixing process, but does not assign virtual-color recipes. A single-color STL slice does not validate a Full Spectrum result.

The report distinguishes native export (`slicer_output_completed`) from a completed slice with passing toolpath checks and previews (`slice_completed`). Every distinct exported G-code is reviewed across all layers against the resolved machine polygon, excluded area and height. Reports include line numbers for failures and actual sliced-path previews, including supports/brim. Failed or unsupported paths prevent completion even when Orca exits zero. See [toolpath review](../docs/PRINT_GUIDE.md#toolpath-review) for scope, standalone review of native multicolor exports and limits. Human layer/color/clearance review is still required. Keep failed run transcripts. Do not use a stale G-code/project file from a previous run as evidence of success.

## Finish in Snapmaker Orca

Preserve target colors and evaluate the actual spools in the Full Spectrum workflow described in [FULL_SPECTRUM.md](FULL_SPECTRUM.md). Colored geometry is not a calibrated toolpath. Actual texture/color conversion compatibility, virtual-color recipes, supports, seams, base stability, tower clearance, material use and duration require slicer verification. Report planned and verified outcomes separately.

Primary sources: [TripoSR code and MIT license](https://github.com/VAST-AI-Research/TripoSR), [public model files](https://huggingface.co/stabilityai/TripoSR), [upstream inference API](https://github.com/VAST-AI-Research/TripoSR/blob/main/tsr/system.py), [rembg human segmentation](https://github.com/danielgatis/rembg).
