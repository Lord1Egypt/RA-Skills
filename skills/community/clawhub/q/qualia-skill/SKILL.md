---
name: qualia
description: "Fine-tune robot foundation models (VLA, vision-language-action) on cloud GPUs: pi0, pi0.5 (π0.5), GR00T N1.5, ACT, SmolVLA, SARM reward models. Robotics and robot training with LeRobot-format HuggingFace datasets. Launch, monitor, and cancel fine-tune jobs from the CLI. Agent-native: --json output and stable exit codes."
version: 2.1.0
metadata:
  openclaw:
    emoji: "🤖"
    homepage: https://qualiastudios.dev
    requires:
      env:
        - QUALIA_API_KEY
      bins:
        - python3
    primaryEnv: QUALIA_API_KEY
    envVars:
      - name: QUALIA_API_KEY
        required: true
        description: Qualia API key from app.qualiastudios.dev (Settings -> API Keys). Account needs credits to launch training jobs.
---

# Qualia

Fine-tune Vision-Language-Action (VLA) models for robotics on cloud GPUs.

## Setup

1. Sign up at [app.qualiastudios.dev](https://app.qualiastudios.dev/)
2. Create an API key (Settings → API Keys)
3. Set the env var:
   ```bash
   export QUALIA_API_KEY="your-api-key"
   ```

## Verify your install

First thing after setup, run the self-test:

```bash
python3 {baseDir}/scripts/qualia.py doctor
```

It checks the API key, auth/connectivity (`/v1/credits`), and the models endpoint. Exit 0 means everything works. Add `--json` for machine-readable results.

## Machine-readable output

Every command accepts a global `--json` flag. In JSON mode, stdout carries exactly one JSON object or array and nothing else. Errors are emitted on stdout as `{"error": {"code": <int>, "message": "...", "details": ...}}` with the matching exit code.

```bash
python3 {baseDir}/scripts/qualia.py --json credits
# {"balance": 90784}
```

Prefer `--json` when driving the CLI programmatically; parse stdout, branch on exit code.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic/unknown failure |
| 2 | Usage error (bad arguments, unknown command) |
| 3 | Auth error (HTTP 401/403 or missing `QUALIA_API_KEY`) |
| 4 | Insufficient credits (HTTP 402) |
| 5 | Validation error (bad camera mapping, hyperparams, or dataset; HTTP 400/422) |
| 6 | Not found (HTTP 404) |
| 7 | Connection/network error |

## When Someone Asks to Train a Model

They probably won't give you everything upfront. Here's what you need and how to get it:

1. **Dataset**: ask for their HuggingFace dataset ID (e.g. `your-org/your-dataset`)
2. **Model type**: if they don't specify, run `models` and help them choose:
   - Quick prototyping → suggest ACT (fast, no base model needed)
   - Production quality → suggest π0.5 or π0
   - Humanoid robots → suggest GR00T N1.5
   - Resource-conscious → suggest SmolVLA
3. **Training duration**: if unspecified, suggest 2 to 4 hours for a first run
4. **Camera mapping**: run `dataset-keys` on their dataset, then `models` to see required slots, and map them automatically. Confirm with the user before launching.

If the user already has a project, use it. Otherwise create one.

## When Things Go Wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Job stuck at `credit_validation` | Insufficient credits | Run `credits`, tell user to top up |
| Fails at `dataset_preprocessing` | Bad camera mapping or invalid dataset | Re-check `dataset-keys` output, verify mapping |
| Fails at `instance_booting` | GPU capacity issue | Try a different instance type or region |
| Job failed with no clear error | Check phase events | Run `status <job_id>` and read the event messages |

Always run `status <job_id>` and share the full phase history with the user when debugging.

## Quick Start

```bash
# See what models are available (always check, new ones are added regularly)
python3 {baseDir}/scripts/qualia.py models

# Check GPU options and pricing
python3 {baseDir}/scripts/qualia.py instances

# Check your credit balance
python3 {baseDir}/scripts/qualia.py credits
```

## Train a Model

```bash
# 1. Discover image keys in your dataset
python3 {baseDir}/scripts/qualia.py dataset-keys your-org/your-dataset

# 2. Create a project
python3 {baseDir}/scripts/qualia.py project-create "My Robot"

# 3. Launch training
python3 {baseDir}/scripts/qualia.py finetune <project_id> <vla_type> your-org/your-dataset 4 \
  '{"cam_1": "observation.images.top"}' \
  --model <base_model_id> \
  --name "My run"

# 4. Monitor
python3 {baseDir}/scripts/qualia.py status <job_id>
```

**Notes:**
- Run `models` first to see which VLA types require `--model` and which don't
- Camera mappings map model slots (from `models`) to dataset image keys (from `dataset-keys`)
- **Smart camera mapping:** The API returns generic slot names (`cam_1`, `cam_2`, `cam_3`) but the underlying models have a specific input order. Map semantically using these known orders:
  - **π0.5 / π0:** `cam_1` = base/overview camera, `cam_2` = left wrist/arm, `cam_3` = right wrist/arm
  - **GR00T N1.5:** `cam_1` = base/overview camera, `cam_2` = left wrist/arm, `cam_3` = right wrist/arm
  - **ACT / SmolVLA:** `cam_1` = primary camera, `cam_2`/`cam_3` = secondary views
  - Fuzzy-match dataset keys to these roles: `context_camera` or `base_0` → `cam_1`; `left_wrist` ≈ `left_arm` → `cam_2`; `right_wrist` ≈ `right_arm` → `cam_3`
- Omit `--model` for types that don't support custom models
- **Estimate cost before launching:** run `instances` to get credits/hr, multiply by hours. Tell the user the estimated cost before confirming.
- Dataset IDs on HuggingFace are **case-sensitive**, double-check the exact ID

## Manage Jobs & Projects

```bash
python3 {baseDir}/scripts/qualia.py projects                     # List projects and jobs
python3 {baseDir}/scripts/qualia.py status <job_id>              # Job status and phase history
python3 {baseDir}/scripts/qualia.py cancel <job_id>              # Cancel a running job
python3 {baseDir}/scripts/qualia.py project-delete <project_id>  # Delete a project
```

## Custom Hyperparameters

```bash
# Get defaults
python3 {baseDir}/scripts/qualia.py hyperparams <vla_type> [model_id]

# Validate overrides
python3 {baseDir}/scripts/qualia.py hyperparams-validate <vla_type> '{"learning_rate": 1e-4}'

# Use in training
python3 {baseDir}/scripts/qualia.py finetune ... --hyper-spec '{"learning_rate": 1e-4, "num_epochs": 50}'
```

## Finetune Flags

| Flag | Description |
|------|-------------|
| `--model <id>` | Base model ID (required for some VLA types) |
| `--name <str>` | Job display name |
| `--instance <id>` | GPU instance type |
| `--region <name>` | Cloud region |
| `--batch-size <n>` | Batch size (1-512, default 32) |
| `--hyper-spec '<json>'` | Custom hyperparameters |
| `--rabc <model_path>` | Enable RA-BC with SARM reward model (HF path) |
| `--rabc-image-key <k>` | Image key for reward annotations |
| `--rabc-head-mode <m>` | RA-BC head mode (e.g. sparse) |

## RA-BC (Reward-Aware Behavior Cloning)

Use a trained SARM reward model to weight training samples. Supported on smolvla, pi0, pi05.

```bash
python3 {baseDir}/scripts/qualia.py finetune \
  <project_id> pi0 your-org/your-dataset 4 \
  '{"cam_1": "observation.images.top"}' \
  --model lerobot/pi0 \
  --rabc your-org/sarm-reward-model \
  --rabc-image-key observation.images.top \
  --rabc-head-mode sparse
```

## Job Phases

`queuing → credit_validation → instance_booting → instance_activation → instance_setup → dataset_preprocessing → training_running → model_uploading → completed`

Terminal: `completed`, `failed`, `cancelled`

## Live Docs

For the latest models, endpoints, and capabilities, always check the live documentation:

- **LLM context:** [docs.qualiastudios.dev/llms.txt](https://docs.qualiastudios.dev/llms.txt)
- **API reference:** [dev-docs.qualiastudios.dev/api/reference](https://dev-docs.qualiastudios.dev/api/reference)
- **SDK:** [docs.qualiastudios.dev/sdk/overview](https://docs.qualiastudios.dev/sdk/overview/)
- **Guides:** [docs.qualiastudios.dev/global/guides](https://docs.qualiastudios.dev/global/guides/)

## Links

- Platform: https://app.qualiastudios.dev
- Docs: https://docs.qualiastudios.dev
- API: https://api.qualiastudios.dev (auth via `X-API-Key` header)
