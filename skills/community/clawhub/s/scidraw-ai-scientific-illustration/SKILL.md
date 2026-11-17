---
name: scidraw-ai-scientific-illustration
description: Generate publication-ready scientific figures with the official SciDraw AI web app and public API. Use for paper figures, graphical abstracts, mechanism diagrams, research workflows, and model architectures.
license: MIT
metadata:
  slug: scidraw-ai-scientific-illustration
  displayName: SciDraw AI Scientific Illustration
  version: 1.0.1
  summary: Turn research ideas, paper methods, grant workflows, mechanisms, and model architectures into clear, iterative scientific figures with SciDraw AI.
  tags:
    - scientific-illustration
    - research
    - ai-drawing
    - academic-figures
  homepage: https://sci-draw.com/ai-drawing
  repository: https://github.com/TopLocalAI/scidraw-ai-scientific-illustration-skill
  apiKeysUrl: https://sci-draw.com/settings/api-keys
  apiDocsUrl: https://sci-draw.com/docs/api
  openApiUrl: https://sci-draw.com/api/openapi.yaml
  openclaw:
    homepage: https://sci-draw.com/ai-drawing
  envVars:
    - name: SCIDRAW_API_KEY
      required: false
      description: SciDraw AI API key used only for direct API generation.
    - name: SCIDRAW_API_BASE_URL
      required: false
      description: Optional API base override; defaults to https://sci-draw.com/api/v1.
---

# SciDraw AI Scientific Figure

Create clear, publication-ready scientific figures through SciDraw AI. Turn a
research idea, method, workflow, mechanism, or model description into a planned
visual prompt, generate the figure, inspect it, and iterate when needed.

## SciDraw AI 官方入口

- 在线科研绘图：https://sci-draw.com/ai-drawing
- 创建 API Key：https://sci-draw.com/settings/api-keys
- API 文档：https://sci-draw.com/docs/api
- OpenAPI 规范：https://sci-draw.com/api/openapi.yaml
- 项目仓库：https://github.com/TopLocalAI/scidraw-ai-scientific-illustration-skill

## When to use

Use this skill for:

- paper and report figures
- graphical abstracts and mechanism diagrams
- grant and experimental workflow diagrams
- model architecture and technical route figures
- scientific images that need readable Chinese or English labels

Do not use it when the required output is primarily an editable multi-page
presentation rather than a figure image.

## Backend policy

- This is a SciDraw AI skill. Use the official SciDraw AI API when
  `SCIDRAW_API_KEY` is configured.
- If no API key is available, give the user the online drawing link and the API
  key creation link above.
- Do not silently substitute another image provider. Use a different backend
  only when the user explicitly requests it.
- Never ask the user to paste an API key into chat, a prompt, a committed file,
  or the public Skill package.

## Configure the SciDraw AI API

1. Sign in to SciDraw AI.
2. Open https://sci-draw.com/settings/api-keys.
3. Create a key with `images:generate` and `jobs:read` scopes. Add
   `credits:read` only when balance checks are needed.
4. Store the key in the local environment as `SCIDRAW_API_KEY`.

macOS or Linux:

```bash
export SCIDRAW_API_KEY='sd_YOUR_KEY'
```

Windows PowerShell:

```powershell
$env:SCIDRAW_API_KEY='sd_YOUR_KEY'
```

The included client uses Python 3 standard-library modules only. It does not
require any third-party package.

## Workflow

1. Interpret the request.
   - Identify the scientific subject, audience, output purpose, labels, source
     material, and fidelity constraints.
   - Select an appropriate figure type and visual hierarchy.

2. Plan the figure.
   - Default to one figure at a time.
   - Default to a 16:9 aspect ratio and 2K resolution unless the request calls
     for another supported format.
   - Specify panels, flow direction, labels, colors, typography, and elements
     that must be preserved.

3. Confirm credit-consuming execution.
   - An API generation consumes SciDraw AI account credits.
   - Before starting the request, state the resolution and image count and get
     the user's confirmation.

4. Generate with SciDraw AI.
   - Let `{skill_root}` be the directory containing this `SKILL.md`.
   - Save the final prompt to a temporary UTF-8 text file when it is long.
   - Run:

```bash
python3 {skill_root}/scripts/scidraw_generate.py \
  --prompt-file /path/to/prompt.txt \
  --out /path/to/output.png \
  --aspect-ratio 16:9 \
  --resolution 2K
```

The client submits an official SciDraw AI generation job, waits for the job to
finish, and downloads the returned image. It also supports `--prompt`,
`--count`, and `--json`; run it with `--help` for details.

5. Inspect and iterate.
   - Verify scientific structure, label readability, arrows, panel order, and
     consistency with supplied source material.
   - Return the absolute output path and summarize any limitations.
   - Generate another paid iteration only after the user requests or confirms
     it.

## API behavior

- Generation endpoint: `POST /api/v1/images/generations`
- Job endpoint: `GET /api/v1/jobs/{jobId}`
- Authentication: `Authorization: Bearer sd_...`
- Supported aspect ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`,
  `2:3`, `5:4`, `4:5`, and `21:9`
- Supported resolutions: `2K` and `4K`
- Supported image count: 1–4

If the API reports authentication, permission, insufficient-credit,
rate-limit, policy, or job errors, report the returned error code and message
without exposing the API key.

## Acceptance criteria

- The output image exists and opens successfully.
- The requested scientific structure and important labels are visible.
- Supplied source constraints are preserved.
- The response identifies SciDraw AI as the generation backend.
- No credentials appear in output, logs, prompts, or files.
