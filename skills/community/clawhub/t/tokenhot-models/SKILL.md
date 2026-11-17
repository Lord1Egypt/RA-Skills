---
name: tokenhot-models
description: Generate and save images when the user requests TokenHot. Check model parameters, inspect a local job, or recover its output without generating again.
metadata: {"openclaw":{"primaryEnv":"TOKENHOT_API_KEY","requires":{"bins":["node"],"env":["TOKENHOT_API_KEY"]}}}
---

# TokenHot Models

Use the included Node.js 22+ helper for [TokenHot](https://tokenhot.ai/) text-to-image requests. Run `node "{baseDir}/scripts/tokenhot-models.mjs" models` to list its supported model and sizes. Check the [live TokenHot catalog](https://tokenhot.ai/models) and [model reference](https://docs.tokenhot.ai/main/gpt-image-2) when the user asks about availability or current rates. Use the model's exact ID and size. This version supports one synchronous GPT Image 2 generation per job.

Generating an image requires a TokenHot account, an API key, and available balance. TokenHot bills each generation. Follow the [TokenHot OpenClaw guide](https://docs.tokenhot.ai/openclaw) to set `TOKENHOT_API_KEY` in the OpenClaw process environment. OpenClaw also loads it from the host's [global `.env` file](https://docs.openclaw.ai/help/environment). The skill works with the chat model already configured in OpenClaw.

1. Establish the prompt and destination from the user's request. Use `gpt-image-2` at `1024x1024` when model and size are unspecified. An explicit request to generate through TokenHot authorizes the scoped, billable generation. When the user specifies a strict price cap, submit only after verifying the rate for the account and size fits that cap. Keep the key in the local `TOKENHOT_API_KEY` environment variable.
2. Use the workspace file tool to write `{"prompt":"...","model":"gpt-image-2","size":"1024x1024"}` as UTF-8 JSON outside the skill directory. Pass the file path to the command and keep the prompt out of the command line. Choose a new local job directory, by default under the workspace's `outputs/tokenhot/`. Create its parent if needed. Run `node "{baseDir}/scripts/tokenhot-models.mjs" generate --request "<request-file>" --job "<new-directory>"`. Create one job for each explicitly requested image. If the user requests a specific output path, copy the saved image there without replacing an existing file unless requested. A preview request can use `models` or `plan` without sending a generation.
3. Report the local image path and returned usage. Usage counts alone cannot establish the billed amount. If the helper exits after reserving a job, use `status --job <directory>`. When a successful API response was saved, use `resume --job <directory>` to retrieve its image. Resume only downloads an existing result. If the API outcome is unknown, report the job and available request ID for reconciliation in TokenHot usage logs. A lost response is insufficient evidence to start another generation.

Use only content authorized for transmission to TokenHot. Keep secrets out of chat and request files. The job receipt can contain a temporary signed image link, so keep job files local. For editing, video, and other models, refer to their official documentation and report the scope of this helper.
