# Optional local Modly workflow

[Modly](https://github.com/lightningpixel/modly), by Lightning Pixel, is a separately installed desktop app with local model extensions, an API and JSON CLI. This skill does not install the app, extension environments, weights or model-specific patches. Keep their licenses and setup records separately.

## Connect an existing installation

Store optional absolute `modly_app`, `modly_cli`, `modly_user_data` and `modly_api_url` values in ignored `local-runtime.json`. Use the actual local CLI path, not a presumed executable name. Confirm health, model availability and parameters before submitting a job:

```sh
python3 /path/to/modly/tools/modly-cli/agent.py health
python3 /path/to/modly/tools/modly-cli/agent.py model list
python3 /path/to/modly/tools/modly-cli/agent.py model params --model triposg/generate
```

Check whether port 8765 is already occupied before launching a new app instance: reviewed desktop startup can stop listeners on that port. Never launch over an unrelated service. Prefer an isolated `--user-data-dir` and preserve its configured workspace, model, extension and cache paths. Configure cloud providers only when the user chooses them.

## Generate a candidate

Create a fresh output directory first; the upstream CLI can overwrite an export destination.

```sh
python3 /path/to/modly/tools/modly-cli/agent.py generate \
  --model triposg/generate --image /absolute/preserved-input.png \
  --output /absolute/new-job/model.glb --remesh none \
  --params-json '{"num_inference_steps":50,"guidance_scale":7.0,"foreground_ratio":0.85,"faces":-1,"seed":42,"use_flash_decoder":"Marching Cubes"}' \
  --timeout 1800 --progress
```

Keep source bytes/hash, parameters, job ID, output and progress. Poll `workflow-run status <id>` or cancel that same ID rather than submitting a duplicate. `--remesh none` preserves the generated shape before likeness review. TripoSG exports geometry without reconstructed color/texture in this route; inspect the file rather than trusting a generic CLI `texture_enabled` field.

## Compatibility limits

- Each extension has its own device support and license. An Apple Silicon desktop app does not make a CUDA-only generator compatible with Metal.
- A reference TripoSG environment used torch 2.7.0, torchvision 0.22.0, Diffusers 0.31.0, Transformers 4.46.3 and PEFT 0.14.0. These are compatibility notes, not a bundled lockfile or fresh-machine installer. Keep environments separate from TripoSR.
- On MPS, dense extraction can exceed memory despite completing diffusion. Preserve normal memory guards, run heavy jobs sequentially and record any local source changes. A smaller synchronized extraction batch was useful in development; that runtime patch is not shipped by this skill.
- The extension may apply rembg even to alpha images. Pre-cache the actual selected segmentation model. Hugging Face offline flags do not stop rembg/Pooch downloads and are not an OS-wide network sandbox.
- Discover available mesh operations before calling them. The reviewed 0.4.3 package lacked `inspect_mesh` even though newer source documented it. An inspection's `printable` field is not proof of supports, stability, thickness or U1 fit.
- Unload a completed model through the supported local API before another heavy stage. Do not interrupt a running job for an unrelated model.

Preserve the raw mesh and inspect actual untextured views. Cropped face studies can diagnose detail limits but must not replace a requested full figure. Hidden sides/back remain inferred. A successful run is neither accepted likeness nor commercial-service parity.

The built-in Orca shortcut converts to STL, losing appearance. For color, retain a genuine appearance master and follow [Full Spectrum](FULL_SPECTRUM.md). The general painted-target exporter rejects calibrated multi-filament templates; it does not implement arbitrary recipe-preserving project rewrites. No Modly output automatically configures calibrated U1 colors, supports, infill or a verified plate.

Primary integration contract: [Modly CLI](https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md). The external app and models are not distributed here.
