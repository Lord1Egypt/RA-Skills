---
name: publish-models
description: >
  Push and publish custom AI models to Replicate, and set up CI/CD for
  releasing new model versions safely. Use when running cog push,
  deploying a model to Replicate, releasing a new version, validating
  a model with cog-safe-push before publishing, configuring a Replicate
  deployment, setting up GitHub Actions for model releases, or porting a
  community model to an official one. Trigger on phrases like "push a
  model to Replicate", "publish a model", "deploy a model", "release a
  new version", "cog push", "cog-safe-push", "model CI", "r8.im", or
  "schema compatibility", and when referencing
  github.com/replicate/cog-safe-push or
  github.com/replicate/model-ci-template. Covers cog push, the full
  cog-safe-push config (test cases, fuzz, deployment, official_model),
  GitHub Actions patterns, multi-model matrix pushes, and post-publish
  monitoring. Assumes you already have a working Cog project; see
  build-models if you need to package one first.
---

## Docs

- Cog reference: <https://cog.run/llms.txt>
- `cog push` reference: <https://cog.run/cli#cog-push>
- cog-safe-push: <https://github.com/replicate/cog-safe-push>
- Model CI template: <https://github.com/replicate/model-ci-template>
- Continuous deployment guide: <https://replicate.com/docs/guides/continuous-model-deployment>

## When to use this skill

- You have a working Cog project (see `build-models` if you don't yet).
- You want to publish a private or public model on Replicate.
- You're releasing a new version of an existing model and want to avoid breaking changes.
- You're setting up CI/CD for model releases.

## Prerequisites

- Cog installed and `cog login` against `r8.im` (or `echo $TOKEN | cog login --token-stdin`).
- A model created at `replicate.com/{owner}/{name}` via the API, web UI, or `r8-model` CLI.
- `REPLICATE_API_TOKEN` set in your environment.

## Plain `cog push`

The simplest path. Build and upload a new version:

```
cog push r8.im/owner/my-model
```

Or set `image: r8.im/owner/my-model` in `cog.yaml` and run a bare:

```
cog push
```

Useful flags:

- `--separate-weights` — store weights in a separate layer; faster cold boots and pushes for models with > 1GB of weights.
- `--x-fast` — faster pushes during iteration (skips some validation).
- `--secret id=hf,src=$HOME/.hf_token` — pass build-time secrets without baking them into image history.

## cog-safe-push (recommended for any model with users)

`cog-safe-push` pushes to a private `-test` model first, checks schema compatibility against the live version, runs prediction comparisons, and fuzzes inputs. Catches breaking changes before they reach users.

Install:

```
pip install git+https://github.com/replicate/cog-safe-push.git
```

Required env vars:

- `REPLICATE_API_TOKEN`
- `ANTHROPIC_API_KEY` (Claude judges output similarity for stochastic models)

Basic usage:

```
cog-safe-push --test-hardware=gpu-l40s owner/my-model
```

This will:

1. Lint `predict.py` with ruff.
2. Create a private test model `owner/my-model-test` if missing.
3. Push the local Cog model to the test model.
4. Lint the schema (descriptions, defaults, etc.).
5. Check schema compatibility against the live `owner/my-model` version.
6. Run prediction comparisons between live and test versions.
7. Fuzz the test model with AI-generated inputs.
8. If everything passes, push to `owner/my-model`.

## cog-safe-push.yaml schema

Drop a `cog-safe-push.yaml` in your project root (or `cog-safe-push-configs/<variant>.yaml` for multi-model repos). All five test-case checker types in one example:

```yaml
model: owner/my-model
test_model: owner/my-model-test
test_hardware: gpu-l40s

predict:
  compare_outputs: false              # set false for stochastic models
  predict_timeout: 600
  test_cases:
    - inputs:
        prompt: "a serene mountain landscape"
      match_prompt: "a landscape photo of mountains"   # AI-judged via Claude
    - inputs:
        prompt: "a cat"
      match_url: "https://example.com/reference-cat.png"   # binary/image match
    - inputs:
        prompt: ""
      error_contains: "prompt cannot be empty"           # negative test
    - inputs:
        mode: "json"
      jq_query: '.confidence > 0.8 and .status == "success"'   # JSON output
    - inputs:
        prompt: "echo this"
      exact_string: "echo this"                          # exact string match
  fuzz:
    fixed_inputs:
      seed: 42
    disabled_inputs:
      - debug
    iterations: 10
    prompt: "Generate creative and diverse prompts"

train:                                  # if your model has a trainer
  destination: owner/my-model-trained
  destination_hardware: gpu-l40s
  train_timeout: 1800
  test_cases:
    - inputs:
        input_images: "https://.../training.zip"
        steps: 10

deployment:                             # auto-create or update on push
  name: my-model
  owner: owner
  hardware: gpu-l40s

parallel: 4
fast_push: false
ignore_schema_compatibility: false
official_model: owner/my-model         # for proxy/wrapper models, see below
```

Test case checkers are mutually exclusive: pick exactly one of `match_prompt`, `match_url`, `error_contains`, `jq_query`, or `exact_string` per case. Use `compare_outputs: false` for any stochastic model (diffusion, LLMs); the default `true` is brittle.

## CI/CD: GitHub Actions

Two paths, depending on how much glue you want.

### Path A: roll your own

```yaml
# .github/workflows/push.yaml
name: Push to Replicate
on:
  workflow_dispatch:
    inputs:
      no_push:
        type: boolean
        default: false

jobs:
  push:
    runs-on: ubuntu-latest-4-cores       # builds need disk + cores
    steps:
      - uses: actions/checkout@v4
      - uses: jlumbroso/free-disk-space@v1.3.1
        with:
          tool-cache: false
          docker-images: false
      - uses: replicate/setup-cog@v2
        with:
          token: ${{ secrets.REPLICATE_API_TOKEN }}
      - run: pip install git+https://github.com/replicate/cog-safe-push.git
      - env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          REPLICATE_API_TOKEN: ${{ secrets.REPLICATE_API_TOKEN }}
        run: |
          cog-safe-push -vv ${{ inputs.no_push && '--no-push' || '' }}
```

Add a `concurrency:` block so PR builds cancel each other while main-branch pushes queue:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

### Path B: reusable workflow from model-ci-template

For Replicate-style multi-model repos, drop in:

```yaml
# .github/workflows/ci.yaml
name: CI
on:
  pull_request: { branches: [main] }
  push: { branches: [main] }
  workflow_dispatch:
    inputs:
      models: { type: string, default: "all" }
      ignore_schema_checks: { type: boolean, default: false }
      cog_version: { type: string, default: "latest" }
      test_only: { type: boolean, default: false }

jobs:
  ci:
    uses: replicate/model-ci-template/.github/workflows/template.yaml@main
    with:
      trigger_type: ${{ github.event_name }}
      models: ${{ inputs.models || 'all' }}
      ignore_schema_checks: ${{ inputs.ignore_schema_checks || false }}
      cog_version: ${{ inputs.cog_version || 'latest' }}
      test_only: ${{ inputs.test_only || false }}
    secrets: inherit
```

The reusable workflow expects:

- `cog-safe-push-configs/<model>.yaml` — one per model variant.
- `script/select-model` — bash file with `if/elif [[ "$MODEL" == "..." ]]` blocks listing valid model names.
- Secrets: `COG_TOKEN`, `REPLICATE_API_TOKEN`, `ANTHROPIC_API_KEY`.

## Multi-model matrix pushes

Pattern from `replicate/cog-flux`: one repo, N variants, push them in parallel.

```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set.outputs.matrix }}
    steps:
      - id: set
        run: |
          if [ "${{ inputs.models }}" = "all" ]; then
            echo 'matrix={"model":["schnell","dev","krea-dev"]}' >> "$GITHUB_OUTPUT"
          else
            list=$(echo "${{ inputs.models }}" | jq -Rc 'split(",")')
            echo "matrix={\"model\":$list}" >> "$GITHUB_OUTPUT"
          fi

  push:
    needs: prepare
    runs-on: ubuntu-latest-4-cores
    strategy:
      fail-fast: false
      matrix: ${{ fromJson(needs.prepare.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      - run: ./script/select.sh ${{ matrix.model }}     # produces cog.yaml from a template
      - run: cog-safe-push --config cog-safe-push-configs/${{ matrix.model }}.yaml -vv
```

## Two-pass push for proxy / official models

When you maintain a proxy that wraps a third-party API, you push to a private wrapper first, then update the public-facing official model card. Pattern from `replicate/cog-official-template`:

```bash
./script/write-api-key                                              # bake API key into config
cog-safe-push --config cog-safe-push-configs/${MODEL}.yaml -vv

./script/delete-api-key                                             # strip the key
cog-safe-push --push-official-model --config cog-safe-push-configs/${MODEL}.yaml -vv
```

Set `official_model: owner/name` in the config so `--push-official-model` knows where to publish.

## Deployments

Add a `deployment` block to `cog-safe-push.yaml` to create or update a Replicate deployment automatically on each push:

```yaml
deployment:
  name: my-model
  owner: owner
  hardware: gpu-l40s
```

Scaling defaults: CPU deployments scale 1-20 instances, GPU deployments scale 0-2. Adjust manually via the API or web UI when needed.

## Monitoring published models

Run an hourly canary that exercises the registry path. Pattern from `replicate/cog-pagerduty-check`:

```yaml
name: Hourly cog push check
on:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: |
          # generate a tiny model with a unique uuid, push it, run a prediction
          # by digest, fail loudly if anything breaks.
          ./script/canary.sh
```

Worth doing for any production-critical model, especially when revenue depends on the registry being up.

## Guidelines

- Don't break schema compatibility unless you mean to. cog-safe-push catches it; `--ignore-schema-compatibility` is the opt-out.
- Pin `test_hardware` so test pushes are reproducible.
- Use `--no-push` for dry runs in PR CI; full push on merge to main or on version tags.
- Push from CI rather than laptops once you have users.
- Use `compare_outputs: false` for stochastic models. Use `match_prompt:` for image/video outputs (VLM judgment), `match_url:` for binary outputs you control, `jq_query:` for JSON, `error_contains:` for negative tests.
- Never commit `REPLICATE_API_TOKEN` or `ANTHROPIC_API_KEY`. Use repo secrets.
- For models with weights > 1GB, push with `--separate-weights`.

## Production references

- <https://github.com/replicate/cog-safe-push> — the tool itself, plus its config schema.
- <https://github.com/replicate/model-ci-template> — reusable GitHub Actions workflow.
- <https://github.com/replicate/cog-official-template> — proxy/official model template.
- <https://github.com/replicate/cog-flux/blob/main/.github/workflows/push.yaml> — matrix push across FLUX variants.
- <https://github.com/replicate/cog-comfyui/blob/main/.github/workflows/ci.yaml> — ComfyUI model CI with custom-node install step.
- <https://github.com/replicate/cog-pagerduty-check> — hourly canary pattern.
