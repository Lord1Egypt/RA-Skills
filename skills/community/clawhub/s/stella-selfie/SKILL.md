---
name: stella-selfie
description: Generate persona-consistent selfies and third-person photos with OpenClaw native image generation; deliver to the current conversation or return image bytes to a same-host plugin.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - openclaw
    emoji: "📸"
    homepage: https://github.com/tower1229/Stella
---

# Stella Selfie

Use when asked for a picture of the assistant: "send a pic", "send a selfie", "show me what you look like", "发张照片", "发自拍", or an outfit, location, mood or activity photo. Keep the photographed subject the assistant/selected persona, never the human user.

For same-host plugin requests, use `{baseDir}/references/plugin-integration.md` and the module `{baseDir}/dist/scripts/plugin.js`. It returns one image buffer to the plugin, with no Stella backup or separate chat delivery. The plugin owns preview, any persistence and publishing.

## Prompt Modes

### Mode 1: Mirror Selfie (default)

Best for outfit showcases and full-body framing:

```text
A mirror selfie of this person, [user's context], showing full body reflection.
```

### Mode 2: Direct Selfie

Best for close-ups, emotions and immediate presence:

```text
A selfie of this person, [user's context], looking into the lens.
```

### Mode 3: Third-Person Photo

Best for explicit non-selfie viewpoints:

```text
A natural third-person photo of this person, [user's context], natural composition, not a selfie.
```

| Signal | Mode |
| --- | --- |
| outfit, wearing, clothes, dress, suit, fashion, full-body, mirror, reflection, pose | `mirror` |
| selfie, close-up, portrait, face, eyes, smile, looking into the lens | `direct` |
| third-person, not a selfie, candid shot, 他拍, 路拍, 抓拍 | `third_person` |
| Legacy keywords: travel photo, tourist photo, 旅拍, 打卡照, 风景合影 | `third_person` |

Interpret explicit user requirements first. Use `mirror` by default for outfit / full-body / self-presentation requests. Use `direct` for face/emotion-focused selfies. Use `third_person` only for explicit non-selfie intent or a clearly non-selfie shot. Do not change an explicit selfie into third_person because of timeline. Default mode when no keywords match and timeline is unavailable: `mirror`.

## Resolution And Aspect Ratio

| User says | Resolution |
| --- | --- |
| 2k, 2048, medium res, 中等分辨率 | `2K` |
| 1k, low res, 低分辨率 | `1K` |
| 4k, high res, ultra, 超清, 高分辨率 | `4K` |

Default model: `google/gemini-3-pro-image`. Other host-configured native models are allowed only when they support reference-image editing. Do not infer aspectRatio from prompt text: include it only when explicitly supplied. Do not send size or force a default ratio. Omit resolution from the request JSON unless the user asked for 1K, 2K or 4K; the helper applies 2K only when the selected model supports it. Each request generates exactly one image.

## Step-by-Step Instructions

### Step 1: Collect User Input

Determine explicit scene, outfit, activity, mode (`mirror`, `direct`, or `third_person`), resolution and explicitly requested aspect ratio. Use the current conversation's actual Agent ID; chat has no main fallback. Do not collect another channel/session target, batch count or save directory. Ordinary selfies do not support an extra persistent copy; explain this limitation if requested without inventing a saved path.

### Step 2: Enrich with Timeline Context Or Recent Scene Recall

timeline_resolve is optional, never a prerequisite.

- If unavailable, skip it and retain normal prompt behavior.
- If the request is a current-state `Sparse` prompt ("发张自拍", "发张照片", "想看看你", "send a selfie"), load and follow `{baseDir}/references/timeline-integration.md` when timeline_resolve is available.
- If the current request clearly refers back to a single recently resolved timeline scene in the current conversation, use that document's reuse/query rules even if the request is not Sparse.
- If the user already provided a clear standalone scene, outfit, location, activity, or camera requirement and it is not a callback to a recently resolved timeline scene, do not use timeline enhancement.
- Use the fixed query rules; never rewrite into output-slot questions. On error, timeout, empty fact or missing usable result.consumption, immediately use the default scene rules without explaining timeline internals.
- City/date/time anchors provide scene context, not proof of actual weather. Do not claim live weather synchronization without trusted weather data; this skill does not enable a search-grounding tool.

### Step 3: Assemble Prompt

Prepare the complete prompt using the selected template, explicit user intent and eligible timeline context. The execution helper does not rewrite it, call timeline, or describe the result.

```text
[mirror] A mirror selfie of this person, [context], showing full body reflection.
[direct] A selfie of this person, [context], looking into the lens.
[third_person] A natural third-person photo of this person, [context], natural composition, not a selfie.
```

### Step 4: Prepare Validated References

Use the file-writing tool to create a UTF-8 JSON request in a unique temporary file in the current workspace. Avoid shell interpolation of prompt text. Supported fields only:

```json
{
  "schemaVersion": 1,
  "agentId": "<actual current conversation Agent>",
  "prompt": "<complete Stella prompt>"
}
```

Optional fields: explicit resolution, explicit aspectRatio and user-provided caption. Caption is reply text, not part of the image prompt. Run the preparation helper with the actual request file path as an argument:

```text
node "{baseDir}/dist/scripts/skill.js" prepare "<request.json>"
```

The helper resolves the Agent via the host, uses shared settings and reference checks, and returns toolInput and an internal referenceToken. It does not generate images. If ok=false, report the actionable error and stop. Failed preparation attempts to remove every file it created, including partially written references or manifest. If cleanup is incomplete, its diagnostic identifies the scratch directory for explicit cleanup. Never bypass preparation or fall back to unreferenced generation.

Use complete prepare/release commands, not the bare script as an environment probe. Metadata reads can take longer than a process tool's initial yield window: finish the existing helper process and parse its result before advancing; do not launch duplicate helpers. This waiting applies only to preparation/cleanup, never to image-generation task status.

When using PowerShell with a full executable path, invoke it with `&`:

```powershell
& "<supported-node.exe>" "{baseDir}/dist/scripts/skill.js" prepare "<request.json>"
```

Use the same supported Node executable for release. If the required Node/CLI/configuration is unavailable, report the missing prerequisite and stop rather than trying unrelated environment probes.

### Step 5: Call Native Image Generation Once

Call `image_generate` once using the returned toolInput exactly: the prepared model, full prompt, count=1, prepared images, and any resolution or aspectRatio the helper included. Do not swap the model or use message send, an SDK, CLI generation, or a second call to regenerate.

In the supported host, image_generate loads references before it returns its async task ID. After that invocation returns (including an error), release only this request's reference snapshots in the initiating turn:

```text
node "{baseDir}/dist/scripts/skill.js" release "<same Agent ID>" "<referenceToken>"
```

Remove the temporary input JSON you created. These are input scratch files, not generated-image backups. Do not wait for a completion turn to clean them; that turn may be read-only. If cleanup fails, leave the diagnostic for explicit cleanup and do not retry generation or recursively delete other directories.

On PowerShell, delete only that known request file with `Remove-Item -LiteralPath "<request.json>"`. Do not pass forward-slash Windows paths to cmd deletion commands.

Then end the initiating turn, with at most a short acknowledgement such as "正在生成。" No polling, waiting loop, internal task/session IDs or premature "已发送" claim. The host's later completion delivers the generated attachment to this conversation. Preserve an explicit caption in the completion reply. If native generation fails, report the error in the same conversation; timeout means the upstream outcome can be uncertain.

Later process-completion notices are not image-completion events. Handle only the named process or cleanup result; do not call image_generate action=status in response. Deliver the image only from the host's structured image-completion event.

## Configuration

Requires OpenClaw 2026.10.9 or a compatible host exposing the native image tool, provider inventory and Agent resolvers; use a Node version supported by that host (verified baseline: >=24.22.1 <25 or >=26.12.1). Configure the selected Agent's host-native image provider authentication. Stella has no provider SDK dependencies or skill-specific provider-key install steps.

In the actual Agent workspace's IDENTITY.md:

```markdown
Avatar: ./assets/avatar-main.png
AvatarsDir: ./avatars
```

At least one valid local reference is sufficient. AvatarsDir is optional. Retired AvatarsURLs fields are ignored; only authorized local images are supported.

Configure non-sensitive values under `skills.entries.stella-selfie.config`:

```json
{
  "model": "google/gemini-3-pro-image",
  "AvatarBlendEnabled": true,
  "AvatarMaxRefs": 3
}
```

Optional AvatarAllowedRoots is a nonempty array of absolute directories replacing the defaults. Old AvatarBlendEnabled/AvatarMaxRefs/AvatarAllowedRoots env settings remain readable: config → process env → skill env → default. Remove leftover `Provider` fields; `Provider=gemini` is ignored, other legacy values must be deleted. Use `config.model` instead. Old skill-only API keys are not assumed to configure the host native provider.

References must be regular JPEG/PNG/WebP files, each at most 20 MiB, with valid signatures. Default allowed roots are assets/avatars inside the actual Agent workspace; outward symlinks/junctions are not implicitly authorized. Main Avatar is preferred, realpath duplicates removed, extras selected newest first (birthtime, then mtime/ctime fallback); default maximum three, limited by the selected model's native `maxInputImages`. Blend disabled means main only. The selected model must be listed by the host and support reference-image editing.

For chat, input snapshots preserve the validated bytes, but the native image tool may resize or re-encode them before upload, changing format, dimensions or fine detail. Original-byte upload is not guaranteed. The 20 MiB Stella input limit is separate from the host's media limits and optimization; requesting 4K output does not preserve reference resolution. The in-process plugin path passes validated buffers directly to the native runtime without this chat-tool optimization.

The prompt and selected reference bytes go to the configured native image provider through OpenClaw. Generated media storage, retention and current-conversation delivery belong to the host. Stella creates no generated-image archive and does not delete host attachments or historical user files. It does not promise attachment availability forever.

Install with `clawhub install stella-selfie` in the intended host/profile/workspace scope. No npm runtime dependency installation is needed. An optional capability snippet ships at `{baseDir}/templates/SOUL.fragment.md`; do not overwrite the user's personality files.

Official behavior: [Image generation](https://docs.openclaw.ai/tools/image-generation), [Plugin runtime media](https://docs.openclaw.ai/plugins/sdk-runtime/media#api-runtime-imagegeneration).
