# In-process integration for same-host plugins

This entry is for an OpenClaw plugin on the same host. It returns one image in memory, without a Stella material copy or chat delivery. Preview, persistence, uploading and publishing belong to the calling plugin. Do not serialize image buffers into model tool results or logs.

## Calling the adapter

The installed Stella skill ships `dist/scripts/plugin.js` and its supporting modules. Resolve the skill directory from explicit configuration in the calling plugin, never from the Agent workspace or process cwd. Load the CommonJS module from an ESM plugin with `createRequire`:

```ts
import { createRequire } from "node:module";
import path from "node:path";
import { listAgentIds } from "openclaw/plugin-sdk/agent-scope-runtime";

const require = createRequire(import.meta.url);
const { generateForPlugin } = require(path.join(stellaSkillDir, "dist/scripts/plugin.js"));

const result = await generateForPlugin(
  api, // The calling plugin's OpenClawPluginApi; pass the active host config/runtime.
  { listAgentIds, onWarning: message => api.logger.warn(message) },
  {
    schemaVersion: 1,
    agentId: callerConfig.agentId ?? "main",
    prompt: "A selfie of this person, sitting by a cafe window, looking into the lens.",
    // resolution: "2K", // Include only when explicitly requested; helper applies 2K when supported.
    // aspectRatio: "3:4", // Include only when explicitly requested.
  },
);

if (!result.ok) {
  // Return this safe error to the calling workflow; no automatic generation retry.
  return { ok: false, error: result.error };
}

// Keep these bytes inside the calling workflow, not in a model-facing tool response.
const { buffer, mimeType } = result.image;
// Feed buffer/mimeType into the caller's own preview, storage or publishing flow.
```

The adapter calls `api.runtime.imageGeneration.generate(...)` with `cfg`, the bound Agent's `agentDir`, exact `modelOverride`, `autoProviderFallback: false`, one output and validated reference buffers. `api.runtime.agent` resolves the actual workspace and authentication directory. `listAgentIds` validates the binding before those resolvers run; unknown bindings fail instead of falling back.

## Request and result

Request fields are `schemaVersion: 1`, required full `prompt`, optional `agentId`, optional `resolution` (1K/2K/4K; applied as 2K only when the selected model supports it), optional `aspectRatio`. The default Agent is the exact ID `main`. No count, target, channel, saveDir, description, or per-request credential fields are accepted. Follow the three Stella prompt modes and optional timeline rules in SKILL.md when composing prompt; the adapter does not rewrite it or call timeline/vision.

Success is an in-process object:

```ts
{
  schemaVersion: 1,
  ok: true,
  agentId: "main",
  generatedAt: "<UTC ISO timestamp observed after generation>",
  image: { buffer: Buffer, mimeType: "image/jpeg" }
}
```

There is no durable material ID, file path or content description. The adapter does not create a material database or file. `generatedAt` is an observed completion time, not a claimed provider timestamp. Preserve the result inside the calling plugin if later steps need the same image; repeated requests generate a new image.

Failure is `{ schemaVersion: 1, ok: false, error: { code, stage, message, actionHint?, generationOutcome } }`. `stage` is validate/reference/generate. An error before dispatch has outcome not_started; rejected native output has succeeded; exceptions during generation conservatively have unknown. A timeout does not prove that the upstream operation was cancelled or unbilled. No underlying response, credential or stack is exposed in this object.

The caller must await the result. Coordinate workflow timeouts with the host image-generation timeout. Stella adds no retry, fallback, task ID or polling API. The host/provider can have its own internal request policy.

## Shared settings and reference rules

Read settings from `skills.entries.stella-selfie.config`:

```json
{
  "model": "google/gemini-3-pro-image",
  "AvatarBlendEnabled": true,
  "AvatarMaxRefs": 3
}
```

`AvatarAllowedRoots`, when supplied, is a non-empty array of absolute directories replacing the default authorized roots. Defaults authorize only assets and avatars inside the actual Agent workspace; outward symlink/junction targets are not implicitly authorized. The existing AvatarBlendEnabled/AvatarMaxRefs/AvatarAllowedRoots environment settings remain readable, with config taking precedence, followed by process env and skill env.

At least one valid local JPEG/PNG/WebP reference is required, up to 20 MiB each. Main Avatar is preferred; AvatarsDir is optional. Blend disabled means main only. References are realpath-deduplicated, extra images are selected newest first, default at most three, limited by the selected model's native `maxInputImages`. Revalidation produces buffers so a later path change cannot replace the bytes passed to the runtime. No disk snapshot is needed for this in-process interface.

This direct-buffer path differs from ordinary chat: the native image tool may resize or re-encode local reference snapshots before upload. The in-process plugin path does not invoke that chat-tool optimization. Neither path changes the caller's original reference files.

Select a host-declared native model that supports reference-image editing and the requested parameters. Default is `google/gemini-3-pro-image`. The native provider owns auth and output size limits. Credentials are not read from the identity file or passed through request fields. Do not assume a legacy skill-only API key has already configured the host's native provider authentication.

## Verification scope

The adapter has local tests for Agent/auth binding, configuration precedence, reference authorization, single-output validation, parameter forwarding, no file creation and no retry. Real CLI and chat generations have separately exercised this host's native Google provider; other providers are covered by inventory mocks. A calling plugin's own preview/upload flow is outside this repository and still needs consumer-side validation.

Official interfaces: [Plugin runtime media helpers](https://docs.openclaw.ai/plugins/sdk-runtime/media#api-runtime-imagegeneration), [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace).
