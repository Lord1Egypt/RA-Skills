# Current Risha Capabilities

- Refreshed at: `2026-04-02T21:10:19Z`
- Base URL: `https://adminxcore-api.risha.ai/api`
- Capability count: `17`

## Categories

- `multimodal`: 15
- `text_generation`: 1
- `tts`: 1

## Capability Inventory

### Virtual Try-On (`1`)

- Internal name: `try-on-diffusion`
- Category: `multimodal`
- Output type: `image`
- Supports async: `false`
- Base credit cost: `3`
- Required inputs: `model_image, cloth_image, category`
- Inputs:
  - `model_image` (file) required, file=image
  - `cloth_image` (file) required, file=image
  - `category` (string) required, choices=enum_values [Upper Body, Lower Body, Dress]
  - `num_inference_steps` (integer)
  - `guidance_scale` (number)
  - `seed` (integer)
  - `base64` (boolean)
- Outputs:
  - `output` (string)

### Chatterbox (`2`)

- Internal name: `segmind-custom-audio-workflow`
- Category: `multimodal`
- Output type: `audio`
- Supports async: `true`
- Base credit cost: `3`
- Required inputs: `str_uo3s1`
- Inputs:
  - `audio_05x5h` (file), file=audio
  - `str_uo3s1` (string) required
- Outputs:
  - `status` (string)
  - `output` (string)

### Seedance 1.5 Pro Image to Video (`3`)

- Internal name: `byteplus-seedream-1-5pro`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `150`
- Required inputs: `model, content[0].text, content[0].type`
- Inputs:
  - `model` (string) required
  - `content[0].text` (string) required
  - `content[0].type` (string) required
  - `content[1].image_url.url` (file), file=image
  - `content[1].type` (string)
  - `generate_audio` (boolean)
  - `ratio` (string), choices=enum_values [Adaptive, 16:9, 9:16, 1:1]
  - `duration` (integer), choices=enum_values [5, 10]
  - `watermark` (boolean)
- Outputs:
  - none

### Music Generation (`5`)

- Internal name: `suno-music-generation`
- Category: `multimodal`
- Output type: `audio`
- Supports async: `true`
- Base credit cost: `1`
- Required inputs: `model, callBackUrl, customMode, instrumental, prompt`
- Inputs:
  - `model` (string) required
  - `callBackUrl` (string) required
  - `customMode` (boolean) required
  - `instrumental` (boolean) required
  - `prompt` (string) required
  - `style` (string)
  - `title` (string)
- Outputs:
  - `taskId` (string)
  - `response.sunoData[0].sourceAudioUrl` (string)
  - `response.sunoData[0].sourceImageUrl` (string)
  - `response.sunoData[0].title` (string)
  - `response.sunoData[0].prompt` (string)
  - `response.sunoData[0].tags` (string)
  - `response.sunoData[0].duration` (number)
  - `response.sunoData[0].modelName` (string)

### Ai Avatar DuoTalk (`6`)

- Internal name: `ai-avatar-podcast`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `1`
- Required inputs: `left_audio, right_audio, image, prompt, resolution, seed`
- Inputs:
  - `left_audio` (file) required, file=audio
  - `right_audio` (file) required, file=audio
  - `image` (file) required, file=image
  - `prompt` (string) required
  - `resolution` (string) required, choices=enum_values [480p, 720p]
  - `seed` (number) required
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Text to Image (`7`)

- Internal name: `bytedance-seedream-v4`
- Category: `multimodal`
- Output type: `image`
- Supports async: `true`
- Base credit cost: `10`
- Required inputs: `prompt, size, enable_base64_output, enable_sync_mode`
- Inputs:
  - `prompt` (string) required
  - `size` (string) required, choices=enum_values [Square, Horizontal, Vertical]
  - `enable_base64_output` (string) required
  - `enable_sync_mode` (string) required
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Kling 3.0 Pro Image to Video (`8`)

- Internal name: `kling-v3.0-pro-image-to-video`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `10`
- Required inputs: `prompt, image`
- Inputs:
  - `prompt` (string) required
  - `image` (file) required, file=image
  - `negative_prompt` (string)
  - `end_image` (file), file=image
  - `duration` (integer)
  - `cfg_scale` (number)
  - `sound` (boolean)
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Kling 3.0 Pro Text to Video (`9`)

- Internal name: `kling-v3.0-pro-text-to-video`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `10`
- Required inputs: `prompt`
- Inputs:
  - `prompt` (string) required
  - `negative_prompt` (string)
  - `duration` (integer)
  - `aspect_ratio` (string), choices=enum_values [16:9, 9:16, 1:1]
  - `cfg_scale` (number)
  - `sound` (boolean)
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Kling 3.0 Standard Image to Video (`10`)

- Internal name: `kling-v3.0-std-image-to-video`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `7`
- Required inputs: `prompt, image`
- Inputs:
  - `prompt` (string) required
  - `image` (file) required, file=image
  - `negative_prompt` (string)
  - `end_image` (file), file=image
  - `duration` (integer)
  - `cfg_scale` (number)
  - `sound` (boolean)
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Kling 3.0 Standard Text to Video (`11`)

- Internal name: `kling-v3.0-std-text-to-video`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `7`
- Required inputs: `prompt`
- Inputs:
  - `prompt` (string) required
  - `negative_prompt` (string)
  - `duration` (integer)
  - `aspect_ratio` (string), choices=enum_values [16:9, 9:16, 1:1]
  - `cfg_scale` (number)
  - `sound` (boolean)
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Image to Video - 1080p (`12`)

- Internal name: `seedance-v1-pro-i2v-1080p`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `1`
- Required inputs: `duration, image, prompt, seed`
- Inputs:
  - `duration` (number) required, choices=enum_values
  - `image` (file) required, file=image, choices=enum_values
  - `prompt` (string) required, choices=enum_values
  - `seed` (number) required, choices=enum_values
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (string)

### Image to Video - 720p (`13`)

- Internal name: `seedance-v1-pro-i2v-720p`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `1`
- Required inputs: `duration, image, prompt, seed`
- Inputs:
  - `duration` (number) required, choices=enum_values
  - `image` (file) required, file=image, choices=enum_values
  - `prompt` (string) required, choices=enum_values
  - `seed` (number) required, choices=enum_values
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (string)

### Google Veo 3.1 - Image to Video (`14`)

- Internal name: `veo31-image-to-video`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `1`
- Required inputs: `aspect_ratio, duration, generate_audio, image, prompt, resolution`
- Inputs:
  - `aspect_ratio` (string) required, choices=enum_values [16:9, 9:16]
  - `duration` (number) required, choices=enum_values [4, 6, 8]
  - `generate_audio` (boolean) required, choices=enum_values [true, false]
  - `image` (file) required, file=image
  - `prompt` (string) required
  - `resolution` (string) required, choices=enum_values [720p, 1080p]
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (string)

### Ai Avatar Image & Audio to Video (`15`)

- Internal name: `image-audio-to-video`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `300`
- Required inputs: `audio, image`
- Inputs:
  - `audio` (file) required, file=audio, choices=enum_values
  - `image` (file) required, file=image, choices=enum_values
  - `mask_image` (string), choices=enum_values
  - `prompt` (string), choices=enum_values
  - `resolution` (string), choices=enum_values [480p, 720p]
  - `seed` (integer), choices=enum_values
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### Video Translation (`17`)

- Internal name: `heygen/video-translate`
- Category: `multimodal`
- Output type: `video`
- Supports async: `true`
- Base credit cost: `1`
- Required inputs: `video, output_language`
- Inputs:
  - `video` (file) required, file=video
  - `output_language` (string) required, choices=enum_values [English, Spanish, French, Hindi, Italian, German]
- Outputs:
  - `id` (string)
  - `status` (string)
  - `outputs` (array)
  - `created_at` (string)

### AI Script Writer (`16`)

- Internal name: `openai-script-generation`
- Category: `text_generation`
- Output type: `text`
- Supports async: `false`
- Base credit cost: `1`
- Required inputs: `model, creator, prompt`
- Inputs:
  - `model` (string) required
  - `creator` (string) required, choices=creators [New Media Academy, Tarek Takhayal]
  - `prompt` (string) required
  - `platform` (string), choices=enum_values [General, TikTok, Instagram, YouTube, X (Twitter)]
  - `dialect` (string), choices=dialects [Algeria, Bahrain, Egypt, Iraq, Jordan, Kuwait]
- Outputs:
  - none

### Arabic Dialects Text-to-Speech (`4`)

- Internal name: `gemini-tts`
- Category: `tts`
- Output type: `audio`
- Supports async: `false`
- Base credit cost: `10`
- Required inputs: `text`
- Inputs:
  - `text` (string) required
  - `system_instruction` (string), choices=dialects [Algeria, Bahrain, Egypt, Iraq, Jordan, Kuwait]
  - `voice` (string), choices=voices [Abdullah, Ahmed, Aisha, Ali, Amira, Fatima]
  - `speed` (string), choices=enum_values [Extra Slow, Slow, Medium, Fast, Extra Fast]
  - `mood` (string), choices=enum_values [Neutral, Happy, Angry, Social, Whisper]
- Outputs:
  - `data.audio_data` (string)
  - `data.audio_format` (string)
  - `data.file_path` (string)
  - `data.file_saved` (boolean)

