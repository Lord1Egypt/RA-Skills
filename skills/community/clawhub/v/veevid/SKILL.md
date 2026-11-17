---
name: veevid
version: 1.3.4
description: "Veevid API for AI video, image and audio generation. Use when the user asks to generate or edit a video (text-to-video, image-to-video, reference-to-video), generate or edit an image, make speech (TTS), music or a transcript, or run a video tool: upscale, resize, extend, edit, lip-sync, motion control, character swap, virtual try-on. Covers Veo 3.1, Kling 3.0, Seedance, Wan, MiniMax H3, Nano Banana, GPT Image, Seedream, Eleven v4, Lyria and more; also quotes prices and checks credits."
keywords:
  - ai video generator
  - text to video
  - image to video
  - ai image generator
  - image editing
  - text to speech
  - ai music
  - speech to text
  - video upscaler
  - lip sync
  - kling
  - veo
  - seedance
  - nano banana
  - veevid
metadata:
  clawdis:
    config:
      stateDirs:
        - "~/.config/veevid"
      requiredEnv: []
    requires:
      env: []
      config:
        - path: "~/.config/veevid/api_key"
          description: "Veevid API key for authentication (get one at veevid.ai/settings/api-keys)"
---

# Veevid — AI video, image & audio API

One API key for everything on [veevid.ai](https://veevid.ai): video generation, image generation and editing, speech, music, transcription and video tools. Every model is called through the same endpoint, `POST /api/generate-video`, with a `mode` (the model) and a `generation_type` (the task).

## Setup

1. Get an API key at [veevid.ai/settings/api-keys](https://veevid.ai/settings/api-keys)
2. Save it:

```bash
(
  umask 077
  mkdir -p ~/.config/veevid
  chmod 700 ~/.config/veevid
  printf 'Veevid API key: '
  read -rs KEY; echo
  [ -n "$KEY" ] || { echo "No key entered, nothing saved" >&2; exit 1; }
  printf '%s\n' "$KEY" > ~/.config/veevid/api_key
  chmod 600 ~/.config/veevid/api_key
)
```

This needs a terminal. If you have no TTY, ask the user to run it themselves; don't ask them to paste the key in chat.

All requests send `Authorization: Bearer $(cat ~/.config/veevid/api_key)`. Base URL: `https://veevid.ai`.

## Workflow

1. **Pick the model** with the picker below, then open the matching reference file and find the model's section (search for ``### `<mode>` ``). It lists every param with allowed values and defaults, the input files, upload folders, rules and an example body. Don't guess params.
2. **Quote and confirm — always, before generating.** `POST /api/quote` with the body you will generate with, including the prompt (some models check it). The quote endpoint does not read video URLs and does not always count the `images` array, so describe input files with the quote fields the model's rules ask for (`input_image_count`, `has_video_input`, `input_video_count`, `input_video_duration`, …; see [api-reference.md](references/api-reference.md#post-apiquote)). File URLs are not needed to quote, except the audio URL for `scribe-v2` and `veed-clean-audio` — for those, ask the user before uploading the file to price it. Declare real input lengths (`input_video_duration`, `input_audio_duration`, …): if they are too low, some models charge the difference after the job. Tell the user the model and the exact `required_credits`, and wait for a yes. If `sufficient` is false, offer a cheaper option or [veevid.ai/pricing](https://veevid.ai/pricing).
3. **Upload local files** after the user says yes, and tell them first that the selected files are sent to Veevid for storage and processing by the chosen model; ask before uploading anything private or sensitive. `POST /api/storage/upload` with `file` and the model's upload `folder` (`veed-clean-audio` uses `/api/storage/presign-upload`). Public https URLs can be passed directly unless the model's rules say the file must be uploaded to Veevid.
4. **Generate** with the confirmed params: `POST /api/generate-video` → `{"generation_id": "vg_…", "status": "processing"}`.
5. **Poll** `GET /api/video-generation/{generation_id}/status` every 5–10 s until `completed` or `failed`. The result is in `video_url` for every media kind (video, image or audio); multiple images are in `result_images`. Videos take about 1–3 minutes, images and audio seconds to a minute.

```bash
KEY=$(cat ~/.config/veevid/api_key)
BODY='{"mode":"veo3","generation_type":"text-to-video","prompt":"A golden retriever running through sunflowers, cinematic","video_quality":"standard","aspect_ratio":"16:9"}'
curl -X POST https://veevid.ai/api/quote -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY"
# → {"required_credits":<n>,"current_balance":<n>,"sufficient":true}
# STOP: tell the user the model and <n> credits, and only continue after they say yes.

curl -X POST https://veevid.ai/api/generate-video -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "$BODY"
# → {"generation_id":"vg_abc123","status":"processing",...}

curl https://veevid.ai/api/video-generation/vg_abc123/status -H "Authorization: Bearer $KEY"
```

Prompts are sent to the model as-is — the website's automatic prompt translation is not applied to API calls. Keep the user's language by default. Most image and video models do best with English, so offer to translate before quoting, and only use a translation if the user agrees. Never translate text to be spoken.

## Model picker

| Task | Good default | Other options | Reference |
|---|---|---|---|
| Text/image to video, budget | `grok-imagine`, `veo3` with `video_quality: "lite"` | `ltx-2-3` | [models-video.md](references/models-video.md) |
| Text/image to video, quality | `kling-3`, `veo3` with `"pro"`, `seedance-2.5` | `minimax-h3-max`, `wan-3.0`, `gemini-omni`, `ltx-2-5` (up to 4K) | models-video.md |
| Video from reference images/videos | `seedance-2.5`, `minimax-h3-max` (`reference-to-video`) | `wan-3.0`, `wan-2.7`, `veo3` | models-video.md |
| Image to video with a scripted camera move | `minimax-h3-max-camera` | | models-video.md |
| Talking photo / presenter or ad clip | `minimax-h3-max-lip-sync`, `creatify-boreal` | `ltx-2-5` with `audio` | models-video.md |
| Text to image | `nano-banana-2`, `gpt-image-2` | `nano-banana-2-1`, `seedream-5.0-pro`, `ideogram-4-5` (text in images), `flux-3-image`, `qwen-image-2-1` | [models-image.md](references/models-image.md) |
| Edit an image | `nano-banana-2` / `gpt-image-2` with `image-to-image` | `nano-banana-2-1`, `krea-3` (multi-reference edits), `nano-banana-edit`, `qwen-image-2-1` (masks), `flux-kontext` | models-image.md |
| Virtual try-on / product in hand | `virtual-try-on`, `product-holding` | | models-image.md |
| Text to speech | `eleven-v4-turbo` | `eleven-v4`, `grok-tts` | [models-audio.md](references/models-audio.md) |
| Music | `lyria-music` | | models-audio.md |
| Transcribe audio | `scribe-v2` | | models-audio.md |
| Remove background noise | `veed-clean-audio` | | models-audio.md |
| Upscale / resize a video | `upscale`, `reframe` | | [models-tools.md](references/models-tools.md) |
| Edit / extend a video | `seedance-2.5`, `wan-3.0` (`edit-video`, `video-extend`) | `wan-2.7-edit`, `minimax-h3-max-extend`, `ltx-2-3` extend | models-tools.md |
| Insert a shot / swap a character | `minimax-h3-max-insert`, `minimax-h3-max-recast` | | models-tools.md |
| Lip-sync an existing video | `video-lip-sync` | | models-tools.md |
| Copy motion from a video | `motion-control-standard` / `motion-control-pro` | `wan-animate` | models-tools.md, models-video.md |
| Hug / kiss video from photos | `ai-hug`, `ai-kissing` | | models-tools.md |

Prices depend on duration, resolution and tier — never quote from memory, always call `/api/quote`.

## Getting files from chat

If the user refers to an image, video or audio file they sent in the conversation but no URL reached you, look through their recent messages for attachments from that same user, show which file you picked (quote or reply to that message) and ask them to confirm before uploading. When several files are needed (start/end frames, reference images), ask which ones and in what order.

## Other endpoints

- `GET /api/credits` → `{"success": true, "credits": <n>, "balance": <n>}`
- `GET /api/user/creations?page=1&pageSize=20&includeAudio=1` — the user's past generations
- `DELETE /api/user/creations/{id}` — permanently removes a saved creation, its result files and, for some models, the uploaded input audio. Only when the user explicitly asks to delete that specific creation; show which one and get a yes first
- `POST /api/video-generation/{id}/upgrade-draft` — upgrade a Seedance 2.5 480p draft to 1080p. It spends credits: quote it with `{"draft_upgrade_id": "<id>"}` and get the user's confirmation first, like any generation

Details, response fields and every error code: [references/api-reference.md](references/api-reference.md).

## Errors

| Code | Meaning | What to do |
|---|---|---|
| 400 / 422 | Invalid params or combination | Read the error and the model's rules |
| 401 | Bad or missing API key | Check `~/.config/veevid/api_key` |
| 402 | Insufficient credits | Tell the user `required` vs `balance`; suggest a cheaper option or a top-up |
| 403 | Account suspended | Contact support |
| 409 | Input video longer than declared (character swap), or draft not ready / already upgraded | Nothing was charged. For character swap, show the user the new `required_credits` and only resend with `input_video_duration = measured_duration` after they agree |
| 500 | Server error | Retry after a few seconds |

A `failed` status includes `error_message`; credits are normally refunded automatically.
