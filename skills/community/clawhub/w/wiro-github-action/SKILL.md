---
name: wiro-github-action
description: Write GitHub Actions workflows that call Wiro AI with the Wiro AI Action (wiroai/Wiro-Action@v1). It runs any of 1,000+ models for images, video, audio and 3D, runs a saved Wiro AI workflow, or asks an LLM through the Wiro AI gateway, and returns URLs, files, text and the cost for later steps. Covers the inputs and outputs, the WIRO_API_KEY secret, the price estimate and the max-cost limit, and ready workflows for an image, a pull request summary, release media and a workflow run. Use when the user wants AI images, video, audio, text or reviews in GitHub Actions, mentions wiroai/Wiro-Action or a WIRO_API_KEY secret, or wants to run Wiro AI from CI.
---

# Wiro AI Action for GitHub workflows

`wiroai/Wiro-Action` is a JavaScript action (Node.js 24) that calls Wiro AI from one workflow step and waits for the result. Use `wiroai/Wiro-Action@v1`, which follows the latest 1.x release. It has three modes:

- **model** runs one of the 1,000+ models at https://wiro.ai/models (image, video, audio, 3D, LLM and more), waits for the task and returns the output URLs, the text and the cost. It uploads workspace files as inputs and downloads the outputs.
- **workflow** runs one of the user's saved Wiro AI workflows (https://wiro.ai/workflows) with the inputs you give it and returns what its End node shows.
- **llm** sends one prompt, with files if needed, to the Wiro AI LLM gateway and returns the answer.

For Wiro AI outside GitHub Actions, use the wiro-ai skill (task API and MCP) or the wiro-llm skill (LLM gateway).

## Key and secret

- Read the key from a repository secret: `api-key: ${{ secrets.WIRO_API_KEY }}`. A project that uses signature authentication also needs `api-secret: ${{ secrets.WIRO_API_SECRET }}`.
- If the repository has no `WIRO_API_KEY` secret yet, ask the user to create a project at https://wiro.ai/panel/project/new and add its key under **Settings → Secrets and variables → Actions** themselves. Never ask for the key in the chat, and never write it into a workflow file, a commit or a log.
- The action masks the key in the logs and needs no GitHub token. Give the job only what its other steps need, such as `pull-requests: write` to comment or `contents: write` to upload release assets.
- Workflows started by pull requests from forks, or by Dependabot, don't receive repository secrets. Skip them with a job condition, as the pull request example below does.

## Write the step

- `mode`: leave it out for model mode, or when `workflow` is set. Set `mode: llm` for the LLM gateway.
- `model` (model and llm modes): the exact ID, `owner/model`, from the model's page on wiro.ai, such as `pruna/p-image`, `pruna/p-video-2` or `openai/gpt-5-4-mini`. The page also lists the model's parameters and its price. The LLMs for llm mode are at https://wiro.ai/models?categories=llm-tool-call.
- `workflow` (workflow mode): the workflow's link on wiro.ai, or its full slug, such as `product-ad-a1B2c`.
- `prompt`: in llm mode, the message (required). In model and workflow modes, it fills the `prompt` parameter or input.
- `system` (llm mode): the system prompt.
- `params`: a YAML or JSON mapping. In model mode, the model's parameters by their IDs on the model page, with values as the page shows them, such as `duration: "5"`. In workflow mode, the inputs by the names the Start node shows. In llm mode, extra Chat Completions fields such as `max_tokens`, `reasoning_effort` or `response_format`. A required model parameter you leave out gets the default the model's form starts with; file inputs and the prompt are never filled in.
- Free text from a person, an issue or a pull request goes into `params` through `toJSON()`, such as `brief: ${{ toJSON(inputs.brief) }}`, so quotes, colons and line breaks can't break the YAML.
- `files`: in model and workflow modes, a mapping from a file parameter or input to a workspace path, list or glob, such as `inputImage: assets/photo.png`. The action uploads each file in the form the parameter expects; a public URL in `params` works too. In llm mode, paths or globs, one per line: text files are added as text, and PNG, JPEG, GIF, WebP and PDF files go to models that read them.
- `download: true` saves the output files in `download-dir` (`wiro-output` by default).
- `timeout`: seconds to wait, 600 by default; give video models 900 or more. In model mode, the action stops the task when the timeout runs out or the workflow run is cancelled (`cancel-on-timeout`, on by default). In workflow mode, it stops waiting and fails, while the run goes on and shows its results on wiro.ai when it ends, so give long workflows a generous `timeout`.
- `summary` (on by default) writes the result, with images and answers, to the job summary.

## Use the results

Give the step an `id` and read `steps.<id>.outputs.<name>`:

- `url` is the URL of the first output file, and `urls` is a JSON array of all of them.
- `files` is a JSON array of the downloaded paths, relative to the workspace.
- `text` is the answer in llm mode. In model mode it is an LLM's answer, or the text file a model returns, such as a transcript. In workflow mode it holds the text results.
- `outputs` is JSON: in model mode, the task's outputs (`name`, `contenttype`, `size`, `url`, and `content` for LLMs); in workflow mode, an object with each End node result by name.
- `cost` is the amount billed, in USD. `estimated-cost` is the price estimated before the run: empty when it isn't known in advance, and an upper estimate in llm mode.
- `task-id` (model mode), `run-token` (workflow mode, masked in the logs) and `response` (llm mode, the full Chat Completions response) are there for follow-up work.

Read JSON outputs with `fromJSON()` in expressions, such as `fromJSON(steps.image.outputs.urls)[0]`, or with `jq` in a script. Model output is untrusted text: pass it to scripts through `env:`, and never write `${{ steps.<id>.outputs.text }}` inside a `run:` script.

## Price and max-cost

- Before every run, the action logs `Estimated cost: $...` and sets `estimated-cost`. In model mode it is the model's price for the settings sent, defaults included. In workflow mode it is the sum over the steps that lead to the End node, plus the creator's fee of a priced gallery workflow. In llm mode it is an upper estimate from the prices per token, with the output counted from `max_tokens` or from the model's output limit.
- `max-cost`, in USD, such as `max-cost: '0.50'`, keeps a run from starting when its estimate is higher, or when its price is only known after it ends, such as a model billed by run time. LLM token use inside a model or workflow run is billed when the run ends, so the estimate leaves it out and the log says so.
- Set `max-cost` on every step of an automated workflow, a little above the expected price. In model mode, only a successful run is billed.
- Match the trigger to the price: a priced video step fits `release`, `workflow_dispatch` or a schedule better than every push.
- Run a new workflow once with `workflow_dispatch` and read the `Estimated cost` and `cost` lines in its log.

## Examples

Each one is a complete file for `.github/workflows/`, and each ran on GitHub Actions as written; the last one ran with a real workflow link in place of the example link. Change the models, prompts and limits to fit the task.

### Generate an image by hand and keep it as an artifact

```yaml
name: Generate an image

on:
  workflow_dispatch:
    inputs:
      prompt:
        description: What the image shows
        required: true
        default: A small paper boat on a calm lake at sunrise, soft light

jobs:
  image:
    runs-on: ubuntu-latest
    steps:
      - uses: wiroai/Wiro-Action@v1
        id: image
        with:
          api-key: ${{ secrets.WIRO_API_KEY }}
          model: pruna/p-image
          prompt: ${{ inputs.prompt }}
          params: |
            aspectRatio: "16:9"
          max-cost: '0.02'
          download: true

      - uses: actions/upload-artifact@v7
        with:
          name: image
          path: wiro-output/

      - name: Show the URL and the cost
        env:
          URL: ${{ steps.image.outputs.url }}
          COST: ${{ steps.image.outputs.cost }}
        run: |
          echo "URL: $URL"
          echo "Cost: $COST USD"
```

### Summarize a pull request

```yaml
name: Pull request summary

on:
  pull_request:
    types: [opened, ready_for_review]

permissions:
  contents: read
  pull-requests: write

jobs:
  summary:
    # Pull requests from forks and from Dependabot don't receive repository secrets.
    if: github.event.pull_request.head.repo.full_name == github.repository && github.actor != 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0

      - name: Save the diff
        env:
          BASE: ${{ github.event.pull_request.base.sha }}
        run: git diff "$BASE" HEAD -- . ':!package-lock.json' > pr.diff

      - uses: wiroai/Wiro-Action@v1
        id: summary
        with:
          mode: llm
          api-key: ${{ secrets.WIRO_API_KEY }}
          model: openai/gpt-5-4-mini
          system: You write short, factual pull request summaries for reviewers.
          prompt: >-
            Summarize this pull request in at most five bullet points.
            Then list anything a reviewer should look at closely.
          files: pr.diff
          params: |
            reasoning_effort: low

      - name: Comment on the pull request
        env:
          GH_TOKEN: ${{ github.token }}
          PR: ${{ github.event.pull_request.number }}
          SUMMARY: ${{ steps.summary.outputs.text }}
        run: printf '%s\n' "$SUMMARY" | gh pr comment "$PR" --repo "$GITHUB_REPOSITORY" --body-file -
```

### Make a release banner, then a short video of it

The second step passes the banner's URL to a video model, and `max-cost` keeps it from starting if the price is above $0.20.

```yaml
name: Release media

on:
  release:
    types: [published]

permissions:
  contents: write

jobs:
  media:
    runs-on: ubuntu-latest
    steps:
      - uses: wiroai/Wiro-Action@v1
        id: banner
        with:
          api-key: ${{ secrets.WIRO_API_KEY }}
          model: pruna/p-image
          prompt: >-
            A clean, wide banner for a software release named
            "${{ github.event.release.name }}", abstract shapes, soft light
          params: |
            aspectRatio: "16:9"
          download: true
          download-dir: media

      - uses: wiroai/Wiro-Action@v1
        id: video
        with:
          api-key: ${{ secrets.WIRO_API_KEY }}
          model: pruna/p-video-2
          prompt: Slow camera push in, the shapes drift and the light shifts gently
          params: |
            inputImage: ${{ steps.banner.outputs.url }}
            duration: "5"
            resolution: 720p
          max-cost: '0.20'
          timeout: 900
          download: true
          download-dir: media

      - name: Attach the banner and the video to the release
        env:
          GH_TOKEN: ${{ github.token }}
          TAG: ${{ github.event.release.tag_name }}
          BANNER: ${{ steps.banner.outputs.files }}
          VIDEO: ${{ steps.video.outputs.files }}
        run: |
          cp "$(jq -r '.[0]' <<< "$BANNER")" release-banner.jpg
          cp "$(jq -r '.[0]' <<< "$VIDEO")" release-video.mp4
          gh release upload "$TAG" release-banner.jpg release-video.mp4 --repo "$GITHUB_REPOSITORY"
```

### Run a saved workflow

Replace the link with the user's workflow, and the input names with the ones its Start node shows.

```yaml
name: Product shot

on:
  workflow_dispatch:
    inputs:
      subject:
        description: What to photograph
        default: a ceramic coffee mug

jobs:
  shot:
    runs-on: ubuntu-latest
    steps:
      - uses: wiroai/Wiro-Action@v1
        with:
          api-key: ${{ secrets.WIRO_API_KEY }}
          workflow: https://wiro.ai/workflows/product-shot-a1B2c
          params: |
            subject: ${{ toJSON(inputs.subject) }}
          max-cost: '0.05'
          timeout: 1800
          download: true

      - uses: actions/upload-artifact@v7
        with:
          name: product-shot
          path: wiro-output/
```

## Before you hand over the workflow

- `api-key` comes from a secret, and no step prints it.
- `model` is an exact `owner/model` ID, and each `params` key is a parameter ID from its page, or a Start input name in workflow mode.
- `max-cost` is set, and `timeout` fits the model.
- Steps whose outputs are read have an `id`. JSON outputs go through `fromJSON()` or `jq`, and text reaches scripts only through `env:`.
- Jobs started by pull requests skip forks and Dependabot, and the permissions are the least the steps need.
