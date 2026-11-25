# Experimental local TRELLIS runner

`scripts/u1_trellis.py` is an advanced adapter for a separately installed, compatible TRELLIS Mac runtime. It accepts one or several **real photos of the same physical subject**. The public Microsoft TRELLIS and DINOv2 assets require no Tripo/Meshy account or gated DINOv3 access.

This wrapper does not install dependencies or download missing files. The runtime and dependencies must already exist. It uses one fresh process per job with the tested low-memory lifecycle, mesh/Gaussian outputs, and default MPS allocation guards. The compatible patched runtime and its dependency environment are not included; this is not a self-contained installer.

## Configure an existing reviewed installation

The expected runtime includes `.runtime/trellis-v1/scripts/run_real_pipeline.py`, its executable `.venv/bin/python`, `public_weights.json`, the pinned cached Microsoft checkpoints, and the pinned DINO checkout/checkpoint. These are prerequisites, not files created by `configure`. A stock upstream checkout may not match this contract. See [compatibility notes](TRELLIS_MAC.md).

After provisioning and reviewing that compatible runtime, explicitly pin its current source and cached assets:

```sh
.venv/bin/python scripts/u1_trellis.py configure
.venv/bin/python scripts/u1_trellis.py doctor --verify-assets
```

`configure` creates `.runtime/trellis-engine.json` unless `local-runtime.json` supplies `trellis_manifest`. It checks the pinned upstream source/DINO/model revisions, compares the six TRELLIS checkpoints to their previously verified setup metadata, and hashes local model/configuration/source files. It records the existing DINOv2 checkpoint and environment-pointer files. It performs no downloads or inference. Use `--replace-manifest` only after reviewing intentional changes, not to silence an integrity error.

`doctor` checks source/configuration integrity and cached-file presence/sizes. Add `--verify-assets` to hash the large model files too. Doctor does not run a GPU availability test or reconstruct a model. Third-party package contents are outside this manifest's complete integrity scope.

## Generate from local references

Run using the configured skill Python interpreter (the examples assume the project directory):

```sh
.venv/bin/python scripts/u1_trellis.py generate front.jpg back.jpg \
  --output-dir /absolute/path/to/new-candidate
```

One image is also accepted. `--seed` defaults to 1 and `--steps` defaults to 25 per sampling stage. The output path must not exist, including an empty directory or symlink. The runner refuses duplicate files used as supposed additional views. Photos should be JPEG/PNG formats supported by the configured Pillow installation.

The runner preserves original bytes in `inputs/`, records SHA-256 provenance, and keeps the full EXIF-oriented frame. Supplied nonempty transparency is preserved. Opaque images use the configured native `apple_vision_binary` for foreground extraction; absent or failed Vision does not silently select rembg or fetch another model. Review masks, especially multiple objects or delicate details. This wrapper has not measured which reference count or viewpoint arrangement best preserves a particular subject.

Before generation it verifies pinned local source/model files, sets offline Hugging Face/Transformers flags and explicit local TRELLIS/DINO/cache paths, requires nonempty transparent input at the engine boundary, and restores the default MPS allocation limits if inherited environment variables disabled them. A missing or changed checkpoint stops the job; it does not trigger an automatic replacement download.

The runtime launches through `scripts/u1_offline_exec.py`, which blocks Python IP socket connection/sending and DNS functions before loading the model script. AF_UNIX IPC remains available for local services. This guard is limited to the runtime Python socket APIs; it is not an OS-wide air gap and does not establish that arbitrary native code or independently spawned processes cannot access a network. The wrapper itself performs local file/native Vision operations, with no remote service or download fallback.

## Outputs and quality boundaries

- `job.json` records preprocessing/generation/failure or `candidate_pending_visual_review`. It never marks likeness, geometry validation or print readiness accepted.
- `run.log` contains actual model progress/errors; `command.json` records the local invocation.
- `model_raw.glb`, `model_slat.pt` and `model.ply` preserve earlier geometry/latent/appearance output when the runtime reaches those stages.
- `model.glb` is the final generated texture/geometry candidate. Texture colors are not calibrated U1 filament assignments.

Several internet photos can condition the generative model without forming a valid photogrammetry capture set. Missing views remain inferred; front/back references do not establish measured side geometry. Inspect the actual color and clay mesh, compare it with references, and screen geometry before printing. For a true overlapping capture set, use [Apple Object Capture](APPLE_CAPTURE.md) instead.


Execution does not establish reliable portrait likeness or complete geometry. Reject incomplete form and request appropriate real views rather than repeating a technically completed result as an accepted print.
