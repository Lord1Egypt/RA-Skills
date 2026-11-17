---
name: runware-run
description: >
  How to actually call the Runware API correctly for any task - inspect the
  model's schema, send the right fields, run synchronously for images or
  asynchronously for video/audio/3D, and read the result. Load this whenever an
  agent is about to make a real Runware generation call. Foundation skill that
  every outcome skill builds on.
---

# Running a Runware task

Runware exposes one request shape across every modality: you send a task with a `taskType`, a `model` (the AIR), and the parameters that model's schema allows. This skill is the execution contract. Outcome skills decide *what* to run; this skill is *how* to run it without guessing.

## The contract (follow in order)

1. **Pick the model + taskType.** Get the model from `runware-models` (live lookup). The `taskType` follows the modality: `imageInference` for images, `videoInference` for video, `audioInference` for audio, `modelUpload` for custom models. A just-launched model not yet in the SDK registry throws "Unknown model" - pass `taskType` explicitly to bypass that.
2. **Inspect the schema before calling.** Resolve the model's JSON Schema (the SDK and MCP do this for you). Use **only** fields the schema allows, and mirror its field names exactly. Never invent or guess parameter names - if it's not in the schema, it does not exist.
3. **Provide inputs as URLs or base64.** Local files get uploaded first (the SDK/MCP have an upload step). Reference images, source video, audio, masks all go under the model's documented input fields.
4. **Run with the right delivery mode:**
   - **Images / fast tasks → synchronous.** The call returns the finished result.
   - **Video / audio / 3D / training → asynchronous.** The task returns a `taskUUID`; poll `getResponse` until it reports terminal. Don't block a single sync call on a minutes-long job.
5. **Read the result.** Images return image URLs; video returns `videoURL`; 3D returns files under `outputs.files[].url`. Check the modality's result shape, don't assume.

## Cost discipline

- **Dry-run first when uncertain.** Add the header `X-Runware-Dry-Run: 1` to validate a request and get its cost without executing or being charged. Safe even for destructive task types. Use it to confirm the schema gate and the price before a real run.
- Set `includeCost: true` to get the real cost back on a live run.

## Identity

- Models are addressed by **AIR** (e.g. `bfl:7@1`, `google:3@2`, `runware:400@2`). Slugs also resolve and are the future-canonical form. Communicate AIRs in calls.
- Account-owned / test models use the `runware` source (e.g. `runware:sdk_test@1`).

## Surfaces

The same contract holds whether the agent drives the **TypeScript SDK** (`@runware/sdk`), the **Python SDK** (`runware`), the **MCP** tools, or the **CLI**. Prefer the SDK/MCP - they handle schema resolution, upload, and async polling for you. For LLM/text models, Runware also exposes an OpenAI-compatible endpoint at `api.runware.ai/v1`.

## Quality bar

- The request used only schema-valid fields (verified, not assumed).
- Time-based tasks were run async and polled, not blocked on a sync call.
- Cost was known (dry-run or `includeCost`) before committing to a batch.

## Related skills

`runware-models` (pick the model), `runware-prompting` (write the prompt), and every outcome skill (they specialize this contract).
