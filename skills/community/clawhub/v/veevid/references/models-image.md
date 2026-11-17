# Image models

Text-to-image and image editing. Results: `video_url` (first image) and `result_images` (all images) in the status response.

All of these are called with `POST /api/generate-video` using the `mode` and `generation_type` shown. Params marked 💲 change the price — get the exact cost with `POST /api/quote` before generating. Defaults are what the API uses when the field is omitted (not always what the website preselects).

## Index

- Google Nano Banana — `nano-banana`: `text-to-image`
- Google Nano Banana (Edit) — `nano-banana-edit`: `image-to-image`
- Google Nano Banana 2.1 — `nano-banana-2-1`: `text-to-image`, `image-to-image`
- Google Nano Banana 2 — `nano-banana-2`: `text-to-image`, `image-to-image`
- Flux Kontext — `flux-kontext`: `text-to-image`, `image-to-image`
- Krea 3 — `krea-3`: `text-to-image`, `image-to-image`
- FLUX 3 Image — `flux-3-image`: `text-to-image`, `image-to-image`
- Seedream 5.0 — `seedream-5.0-lite`: `text-to-image`, `image-to-image`
- Seedream 5.0 Pro — `seedream-5.0-pro`: `text-to-image`, `image-to-image`
- Seedream 5.0 Flash — `seedream-5.0-flash`: `text-to-image`, `image-to-image`
- Ideogram 4.5 — `ideogram-4-5`: `text-to-image`, `image-to-image`
- GPT Image 2 — `gpt-image-2`: `text-to-image`, `image-to-image`
- GPT Image 2.5 — `gpt-image-2-5`: `text-to-image`, `image-to-image`
- Qwen Image 2.1 — `qwen-image-2-1`: `text-to-image`, `image-to-image`
- Virtual Try-On — `virtual-try-on`: `image-to-image`
- Product Holding — `product-holding`: `image-to-image`

## Google Nano Banana — `nano-banana`

### `nano-banana` · `text-to-image`

Generates an image from text with Google Nano Banana (or Nano Banana Pro via modelVersion).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 20000 characters. |
| `modelVersion` 💲 | string | "nano-banana", "nano-banana-pro" | "nano-banana" | nano-banana = base model; nano-banana-pro = Nano Banana Pro. |
| `video_quality` 💲 | string | "standard", "1K", "2K", "4K" | "standard" | Send 'standard' with nano-banana; with nano-banana-pro, send the output resolution 1K, 2K or 4K. |
| `aspect_ratio` | string | "auto", "1:1", "9:16", "16:9", "3:4", "4:3", "3:2", "2:3", "5:4", "4:5", "21:9" | "16:9" | Use one of the listed values. nano-banana-pro does not support auto (it produces 1:1). |
| `output_format` | string | "PNG", "JPEG" | "PNG" | Output image format. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- aspect_ratio: use one of the listed values; with nano-banana-pro, auto produces 1:1.
- Text-to-image does not use images; send images: [] or omit it.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "nano-banana", "generation_type": "text-to-image", "prompt": "A beautiful sunset over mountains with golden light", "duration": "0", "aspect_ratio": "auto", "video_quality": "standard", "modelVersion": "nano-banana", "output_format": "PNG", "images": []}
```

## Google Nano Banana (Edit) — `nano-banana-edit`

### `nano-banana-edit` · `image-to-image`

Edits one or more uploaded images from a text instruction with Google Nano Banana (or Nano Banana Pro).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 20000 characters. |
| `images` **required** | string[] |  |  | Input image URLs to edit (1-10). |
| `modelVersion` 💲 | string | "nano-banana", "nano-banana-pro" | "nano-banana" | nano-banana = base model; nano-banana-pro = Nano Banana Pro. |
| `video_quality` 💲 | string | "standard", "1K", "2K", "4K" | "standard" | Send 'standard' with nano-banana; with nano-banana-pro, send the output resolution 1K, 2K or 4K. |
| `aspect_ratio` | string | "auto", "1:1", "9:16", "16:9", "3:4", "4:3", "3:2", "2:3", "5:4", "4:5", "21:9" | "16:9" | Use one of the listed values. nano-banana-pro does not support auto (it produces 1:1). |
| `output_format` | string | "PNG", "JPEG" | "PNG" | Output image format. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-10 image URLs; public https URLs or files uploaded with POST /api/storage/upload

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- aspect_ratio: use one of the listed values; with nano-banana-pro, auto produces 1:1.
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Send 1-10 input images.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "nano-banana-edit", "generation_type": "image-to-image", "prompt": "Change the background to a blue sky", "duration": "0", "aspect_ratio": "auto", "video_quality": "standard", "modelVersion": "nano-banana", "output_format": "PNG", "images": ["https://example.com/input.jpg"]}
```

## Google Nano Banana 2.1 — `nano-banana-2-1`

### `nano-banana-2-1` · `text-to-image`

Generates a 1K/2K/4K image from text with Google Nano Banana 2.1.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" | Output tier. |
| `aspect_ratio` | string | "auto", "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "21:9", "4:1", "1:4", "8:1", "1:8" | "16:9" | auto lets the model pick from the prompt. Always send it (the API default is 16:9). |
| `output_format` | string | "JPEG", "PNG" | "JPEG" | Output format: JPEG or PNG (default JPEG). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- Price by resolution only: 1K = 3 credits, 2K = 5, 4K = 8. Aspect ratio and the number of reference images do not change the price.
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of the listed values (400).
- resolution must be 1K, 2K or 4K (422).
- prompt max 5000 characters (400).
- This is a different model from nano-banana-2 (separate mode and price).
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "nano-banana-2-1", "generation_type": "text-to-image", "prompt": "A minimalist coffee shop poster with the headline \"SLOW MORNINGS\" in bold serif type", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "JPEG", "images": []}
```

### `nano-banana-2-1` · `image-to-image`

Edits/combines up to 10 reference images from a prompt with Google Nano Banana 2.1 at 1K-4K.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `images` **required** | string[] |  |  | 1-10 reference image URLs. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" | Output tier. |
| `aspect_ratio` | string | "auto", "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "21:9", "4:1", "1:4", "8:1", "1:8" | "16:9" | auto keeps the aspect ratio of the first reference image. Always send it (the API default is 16:9). |
| `output_format` | string | "JPEG", "PNG" | "JPEG" | Output format: JPEG or PNG (default JPEG). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-10 reference image URLs

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- Price by resolution only: 1K = 3 credits, 2K = 5, 4K = 8. Aspect ratio and the number of reference images do not change the price.
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of the listed values (400).
- resolution must be 1K, 2K or 4K (422).
- prompt max 5000 characters (400).
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Max 10 reference images (400).
- This is a different model from nano-banana-2 (separate mode and price).
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "nano-banana-2-1", "generation_type": "image-to-image", "prompt": "A minimalist coffee shop poster with the headline \"SLOW MORNINGS\" in bold serif type", "duration": "0", "aspect_ratio": "auto", "resolution": "1K", "output_format": "JPEG", "images": ["https://example.com/ref.jpg"]}
```

## Google Nano Banana 2 — `nano-banana-2`

### `nano-banana-2` · `text-to-image`

Generates an image from text with Google Nano Banana 2 (1K-4K).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 20000 characters. |
| `video_quality` 💲 | string | "1K", "2K", "4K" | "1K" |  |
| `aspect_ratio` | string | "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1" | "16:9" | Output aspect ratio. Use one of the listed values. |
| `output_format` | string | "JPG", "PNG" | "JPG" | Output format: JPG or PNG (default JPG). |
| `google_search` | boolean |  | false | Enable Google Search grounding. |
| `image_search` | boolean |  | false | Optional; has no effect for this model and can be omitted. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- Use one of the listed values.
- aspect_ratio: use one of the listed values.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "nano-banana-2", "generation_type": "text-to-image", "prompt": "A beautiful portrait with stunning details", "duration": "0", "aspect_ratio": "1:1", "video_quality": "1K", "output_format": "JPG", "google_search": false, "image_search": false, "images": []}
```

### `nano-banana-2` · `image-to-image`

Edits/combines reference images from a text prompt with Google Nano Banana 2.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 20000 characters. |
| `images` **required** | string[] |  |  | Reference image URLs (1-14). |
| `video_quality` 💲 | string | "1K", "2K", "4K" | "1K" |  |
| `aspect_ratio` | string | "match_input_image", "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1" | "16:9" | Output aspect ratio. 'match_input_image' keeps the input image's ratio. Use one of the listed values. |
| `output_format` | string | "JPG", "PNG" | "JPG" | Output format: JPG or PNG (default JPG). |
| `google_search` | boolean |  | false | Enable Google Search grounding. |
| `image_search` | boolean |  | false | Optional; has no effect for this model and can be omitted. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-14 reference image URLs

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- Use one of the listed values.
- aspect_ratio: use one of the listed values.
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Send 1-14 reference images.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "nano-banana-2", "generation_type": "image-to-image", "prompt": "A beautiful portrait with stunning details", "duration": "0", "aspect_ratio": "match_input_image", "video_quality": "1K", "output_format": "JPG", "google_search": false, "image_search": false, "images": ["https://example.com/ref.jpg"]}
```

## Flux Kontext — `flux-kontext`

### `flux-kontext` · `text-to-image`

Generates an image from text with Flux Kontext (Flux 1 or Flux 2, Pro or Max).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. |
| `fluxModelVersion` 💲 | string | "flux1", "flux2" | "flux1" | Flux Kontext 1 (flux1) or Flux 2 (flux2). |
| `fluxModel` 💲 | string | "flux-kontext-pro", "flux-kontext-max" | "flux-kontext-pro" | Pro or Max (with flux2, Max is Flux 2 Flex). |
| `fluxResolution` 💲 | string | "1K", "2K" | "1K" | Output resolution; affects price and output only with flux2. |
| `video_quality` | string | "1K", "2K" | "1K" | Send the same value as fluxResolution. |
| `aspect_ratio` | string | "16:9", "21:9", "4:3", "1:1", "3:4", "9:16", "16:21", "3:2", "2:3", "auto" | "16:9" | With flux1: 16:9, 21:9, 4:3, 1:1, 3:4, 9:16, 16:21. With flux2: 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, auto. |
| `output_format` | string | "PNG", "JPEG" |  | Output format, PNG or JPEG (flux1 only). When omitted the model picks the format. |
| `promptUpsampling` | boolean |  | false | Prompt upsampling (flux1 only). |
| `enableTranslation` | boolean |  | false | Prompt translation (flux1 only). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- aspect_ratio: use a value supported by the selected fluxModelVersion.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "flux-kontext", "generation_type": "text-to-image", "prompt": "Serene mountain landscape at sunset with lake reflection", "duration": "0", "aspect_ratio": "16:9", "video_quality": "1K", "fluxModel": "flux-kontext-pro", "fluxModelVersion": "flux1", "fluxResolution": "1K", "promptUpsampling": false, "enableTranslation": false, "output_format": "PNG"}
```

### `flux-kontext` · `image-to-image`

Edits an image (or up to 8 references with Flux 2) from a text instruction with Flux Kontext.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. |
| `image` | string |  |  | Input image URL (first image); flux1 uses only this. Required unless you send it as images[0]. |
| `images` | string[] |  |  | flux2 only: all reference image URLs, up to 8. |
| `fluxModelVersion` 💲 | string | "flux1", "flux2" | "flux1" | Flux Kontext 1 (flux1) or Flux 2 (flux2). |
| `fluxModel` 💲 | string | "flux-kontext-pro", "flux-kontext-max" | "flux-kontext-pro" | Pro or Max (with flux2, Max is Flux 2 Flex). |
| `fluxResolution` 💲 | string | "1K", "2K" | "1K" | Output resolution; affects price and output only with flux2. |
| `video_quality` | string | "1K", "2K" | "1K" | Send the same value as fluxResolution. |
| `aspect_ratio` | string | "16:9", "21:9", "4:3", "1:1", "3:4", "9:16", "16:21", "3:2", "2:3", "auto" | "16:9" | With flux1: 16:9, 21:9, 4:3, 1:1, 3:4, 9:16, 16:21. With flux2: 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, auto. |
| `output_format` | string | "PNG", "JPEG" |  | Output format, PNG or JPEG (flux1 only). When omitted the model picks the format. |
| `promptUpsampling` | boolean |  | false | Prompt upsampling (flux1 only). |
| `enableTranslation` | boolean |  | false | Prompt translation (flux1 only). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `image`: 1 image URL (flux1)
- `images`: 1-8 image URLs (flux2 only)

Upload folders (`folder` for `POST /api/storage/upload`): image → `flux-kontext`

Rules:
- aspect_ratio: use a value supported by the selected fluxModelVersion.
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- flux1 uses only the single input image in image; flux2 accepts up to 8 reference images in images.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "flux-kontext", "generation_type": "image-to-image", "prompt": "Serene mountain landscape at sunset with lake reflection", "duration": "0", "aspect_ratio": "16:9", "video_quality": "1K", "fluxModel": "flux-kontext-pro", "fluxModelVersion": "flux1", "fluxResolution": "1K", "promptUpsampling": false, "enableTranslation": false, "output_format": "PNG", "image": "https://example.com/input.jpg"}
```

## Krea 3 — `krea-3`

### `krea-3` · `text-to-image`

Generates a 1K or 2K image from text with Krea 3.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `resolution` 💲 | string | "1K", "2K" | "1K" | Output tier: 1K (about 1 MP) or 2K (about 4 MP). |
| `aspect_ratio` | string | "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "21:9" | "16:9" | Output aspect ratio (no auto). Always send it. |
| `output_format` | string | "JPEG", "PNG" | "JPEG" | Output format: JPEG or PNG (default JPEG). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of the 10 listed values (400). Always send aspect_ratio.
- resolution must be 1K or 2K (422).
- prompt max 5000 characters (400).
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "krea-3", "generation_type": "text-to-image", "prompt": "A cozy bookshop window at dusk with a cat asleep on a stack of books", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "JPEG", "images": []}
```

### `krea-3` · `image-to-image`

Edits or combines 1-8 reference images from a prompt with Krea 3 at 1K or 2K; refer to them as <image-1>...<image-N>.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. Refer to reference images as <image-1>, <image-2>, ... in upload order. |
| `images` **required** 💲 | string[] |  |  | 1-8 reference image URLs, in the order of <image-1>...<image-N> in the prompt. |
| `resolution` 💲 | string | "1K", "2K" | "1K" | Output tier: 1K (about 1 MP) or 2K (about 4 MP). |
| `aspect_ratio` | string | "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "21:9" | "16:9" | Output aspect ratio (no auto). Always send it. |
| `output_format` | string | "JPEG", "PNG" | "JPEG" | Output format: JPEG or PNG (default JPEG). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-8 reference image URLs

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of the 10 listed values (400). Always send aspect_ratio.
- resolution must be 1K or 2K (422).
- prompt max 5000 characters (400).
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Max 8 reference images (400); each reference image adds one output-size charge.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "krea-3", "generation_type": "image-to-image", "prompt": "Place the ceramic mug from <image-2> on the wooden table in <image-1>. Keep everything else unchanged.", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "JPEG", "images": ["https://example.com/scene.jpg", "https://example.com/mug.jpg"]}
```
## FLUX 3 Image — `flux-3-image`

### `flux-3-image` · `text-to-image`

Generates a native 1K/2K/4K image from text with FLUX 3.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" | Output tier. |
| `aspect_ratio` 💲 | string | "21:9", "2:1", "16:9", "3:2", "7:5", "4:3", "5:4", "1:1", "4:5", "3:4", "5:7", "2:3", "9:16", "1:2" | "16:9" | Output aspect ratio (no auto). Always send it. |
| `output_format` | string | "JPEG", "PNG" | "JPEG" | Output format: JPEG or PNG (default JPEG). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of the 14 listed values (400). Always send aspect_ratio.
- resolution must be 1K, 2K or 4K (422).
- prompt max 5000 characters (400).
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "flux-3-image", "generation_type": "text-to-image", "prompt": "A bakery storefront at golden hour with a hand-painted sign that reads \"Morning Loaf\"", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "JPEG", "images": []}
```

### `flux-3-image` · `image-to-image`

Edits/combines up to 10 reference images from a prompt with FLUX 3 at 1K-4K.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `images` **required** | string[] |  |  | 1-10 reference image URLs. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" | Output tier. |
| `aspect_ratio` 💲 | string | "21:9", "2:1", "16:9", "3:2", "7:5", "4:3", "5:4", "1:1", "4:5", "3:4", "5:7", "2:3", "9:16", "1:2" | "16:9" | Output aspect ratio (no auto). Always send it. |
| `output_format` | string | "JPEG", "PNG" | "JPEG" | Output format: JPEG or PNG (default JPEG). |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-10 reference image URLs

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of the 14 listed values (400). Always send aspect_ratio.
- resolution must be 1K, 2K or 4K (422).
- prompt max 5000 characters (400).
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Max 10 reference images (400); references do not change the price.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "flux-3-image", "generation_type": "image-to-image", "prompt": "A bakery storefront at golden hour with a hand-painted sign that reads \"Morning Loaf\"", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "JPEG", "images": ["https://example.com/ref.jpg"]}
```

## Seedream 5.0 — `seedream-5.0-lite`

### `seedream-5.0-lite` · `text-to-image`

Generates HD images (optionally a batch) from text with Seedream 5.0 Lite.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. |
| `video_quality` | string | "2K", "3K" | "2K" | Output size: 2K or 3K. |
| `aspect_ratio` | string | "1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9", "21:9" | "16:9" | Output aspect ratio. Use one of the listed values and always send it. |
| `output_format` | string | "PNG", "JPEG" | "PNG" | Output format: PNG or JPEG. |
| `sequential_image_generation` | string | "disabled", "auto" | "disabled" | 'auto' enables batch (multi-image) output. |
| `max_images` 💲 | number | 1–15 | 1 | Number of images in a batch. Set it above 1 only together with sequential_image_generation='auto'. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- Set max_images > 1 only with sequential_image_generation='auto'.
- If a batch returns fewer images than requested, unused credits are refunded automatically.
- Always send aspect_ratio, using one of the listed values.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field. Batch results appear in result_images.

Example body:

```json
{"mode": "seedream-5.0-lite", "generation_type": "text-to-image", "prompt": "A cozy reading nook with warm light", "duration": "0", "aspect_ratio": "1:1", "video_quality": "2K", "output_format": "PNG", "sequential_image_generation": "disabled", "max_images": 1, "images": []}
```

### `seedream-5.0-lite` · `image-to-image`

Edits/blends reference images into new HD images (optionally a batch) with Seedream 5.0 Lite.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. |
| `images` **required** | string[] |  |  | Reference image URLs (1-14). |
| `video_quality` | string | "2K", "3K" | "2K" | Output size: 2K or 3K. |
| `aspect_ratio` | string | "match_input_image", "1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9", "21:9" | "16:9" | Output aspect ratio; 'match_input_image' keeps the input image's ratio. Use one of the listed values and always send it. |
| `output_format` | string | "PNG", "JPEG" | "PNG" | Output format: PNG or JPEG. |
| `sequential_image_generation` | string | "disabled", "auto" | "disabled" | 'auto' enables batch (multi-image) output. |
| `max_images` 💲 | number | 1–15 | 1 | Number of images in a batch. Set it above 1 only together with sequential_image_generation='auto'. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-14 reference image URLs

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- Set max_images > 1 only with sequential_image_generation='auto'.
- If a batch returns fewer images than requested, unused credits are refunded automatically.
- Always send aspect_ratio, using one of the listed values.
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Send 1-14 reference images.
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field. Batch results appear in result_images.

Example body:

```json
{"mode": "seedream-5.0-lite", "generation_type": "image-to-image", "prompt": "A cozy reading nook with warm light", "duration": "0", "aspect_ratio": "match_input_image", "video_quality": "2K", "output_format": "PNG", "sequential_image_generation": "disabled", "max_images": 1, "images": ["https://example.com/ref.jpg"]}
```

## Seedream 5.0 Pro — `seedream-5.0-pro`

### `seedream-5.0-pro` · `text-to-image`

Generates images with dense text and infographics from a prompt with Seedream 5.0 Pro.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `resolution` 💲 | string | "1K", "2K" | "1K" |  |
| `video_quality` | string | "1K", "2K" | "1K" | Send the same value as resolution; resolution determines price and output. |
| `aspect_ratio` | string | "1:1", "4:3", "3:4", "16:9", "9:16", "2:3", "3:2", "21:9" | "16:9" | Output aspect ratio; no auto (also for image-to-image). Always send it. |
| `output_format` | string | "PNG", "JPEG" |  | Output format: PNG or JPEG. When omitted the model picks the format. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Rules:
- aspect_ratio must be one of 1:1, 4:3, 3:4, 16:9, 9:16, 2:3, 3:2, 21:9 (400). Always send aspect_ratio.
- resolution must be 1K or 2K (422).
- prompt max 5000 characters (400).
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "seedream-5.0-pro", "generation_type": "text-to-image", "prompt": "An infographic poster explaining the water cycle with labeled arrows", "duration": "0", "aspect_ratio": "1:1", "video_quality": "1K", "resolution": "1K", "output_format": "PNG", "images": []}
```

### `seedream-5.0-pro` · `image-to-image`

Precision-edits up to 10 reference images from a prompt with Seedream 5.0 Pro.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, up to 5000 characters. |
| `images` **required** 💲 | string[] |  |  | 1-10 reference image URLs. |
| `resolution` 💲 | string | "1K", "2K" | "1K" |  |
| `video_quality` | string | "1K", "2K" | "1K" | Send the same value as resolution; resolution determines price and output. |
| `aspect_ratio` | string | "1:1", "4:3", "3:4", "16:9", "9:16", "2:3", "3:2", "21:9" | "16:9" | Output aspect ratio; no auto (also for image-to-image). Always send it. |
| `output_format` | string | "PNG", "JPEG" |  | Output format: PNG or JPEG. When omitted the model picks the format. |
| `duration` | string |  | "0" | Send "0" (not used for images). |

Input files:
- `images`: 1-10 reference image URLs

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- aspect_ratio must be one of 1:1, 4:3, 3:4, 16:9, 9:16, 2:3, 3:2, 21:9 (400). Always send aspect_ratio.
- resolution must be 1K or 2K (422).
- prompt max 5000 characters (400).
- image-to-image requires a non-empty images array (or image) (400 otherwise).
- Max 10 reference images (400).
- Asynchronous: the response is {generation_id, status:'processing', image_url:null, video_url:null, video_quality}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is then in video_url and all output images are in result_images (array). The status response has no image_url field.
- When quoting with `/api/quote`, send `input_image_count` (the number of images) — the quote does not count the `images` array for this model, so it would come out too low.

Example body:

```json
{"mode": "seedream-5.0-pro", "generation_type": "image-to-image", "prompt": "An infographic poster explaining the water cycle with labeled arrows", "duration": "0", "aspect_ratio": "1:1", "video_quality": "1K", "resolution": "1K", "output_format": "PNG", "images": ["https://example.com/ref.jpg"]}
```

## Seedream 5.0 Flash — `seedream-5.0-flash`

### `seedream-5.0-flash` · `text-to-image`

Fast, low-cost text-to-image up to 2K with Seedream 5.0 Flash.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, max 5000 characters. |
| `resolution` | string | "1K", "1.5K", "2K" | "1K" | Output size (1K, 1.5K or 2K). Set it with `resolution`; `video_quality` is not used. |
| `aspect_ratio` | string | "1:1", "4:3", "3:4", "16:9", "9:16", "2:3", "3:2", "21:9" | "16:9" | Output aspect ratio; no auto option. Always send it explicitly. |
| `output_format` | string | "PNG", "JPEG" | "PNG" | Output format in uppercase: PNG or JPEG. |
| `duration` | string |  | "0" | Send "0". |

Rules:
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of 1:1, 4:3, 3:4, 16:9, 9:16, 2:3, 3:2, 21:9 (400). Always send `aspect_ratio` explicitly.
- resolution must be 1K, 1.5K or 2K (422).
- prompt max 5000 characters (400).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "seedream-5.0-flash", "generation_type": "text-to-image", "prompt": "A cozy coffee shop interior at golden hour, warm light through large windows", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "PNG", "images": []}
```

### `seedream-5.0-flash` · `image-to-image`

Fast, low-cost edits of up to 10 reference images up to 2K with Seedream 5.0 Flash.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, max 5000 characters. |
| `images` **required** | string[] |  |  | 1-10 reference image URLs. |
| `resolution` | string | "1K", "1.5K", "2K" | "1K" | Output size (1K, 1.5K or 2K). Set it with `resolution`; `video_quality` is not used. |
| `aspect_ratio` | string | "1:1", "4:3", "3:4", "16:9", "9:16", "2:3", "3:2", "21:9" | "16:9" | Output aspect ratio; no auto option. Always send it explicitly. |
| `output_format` | string | "PNG", "JPEG" | "PNG" | Output format in uppercase: PNG or JPEG. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: 1-10 reference image URLs.

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- generation_type must be text-to-image or image-to-image (422).
- aspect_ratio must be one of 1:1, 4:3, 3:4, 16:9, 9:16, 2:3, 3:2, 21:9 (400). Always send `aspect_ratio` explicitly.
- resolution must be 1K, 1.5K or 2K (422).
- prompt max 5000 characters (400).
- image-to-image requires a non-empty images array (or image) (400).
- At most 10 reference images (400).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "seedream-5.0-flash", "generation_type": "image-to-image", "prompt": "A cozy coffee shop interior at golden hour, warm light through large windows", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "output_format": "PNG", "images": ["https://example.com/ref.jpg"]}
```

## Ideogram 4.5 — `ideogram-4-5`

### `ideogram-4-5` · `text-to-image`

Generates 1-8 images with accurate in-image text from a prompt with Ideogram 4.5.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 10000 characters. |
| `quality` 💲 | string | "low", "medium", "high" | "low" |  |
| `num_images` 💲 | number | 1–8 | 1 | Images per request (1-8); the price is multiplied by num_images. |
| `enable_prompt_expansion` | boolean |  | true | Text-to-image only. |
| `aspect_ratio` | string | "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "16:10", "10:16", "2:1", "1:2", "12:5", "5:12", "22:9", "9:22", "23:9", "9:23", "8:3", "3:8", "3:1", "1:3" | "1:1" | Output aspect ratio. |
| `resolution` | string | "1K", "2K" |  | Resolution tier for the chosen aspect_ratio; defaults to the lowest available. 12:5, 5:12, 22:9, 9:22, 23:9, 9:23, 8:3, 3:8, 3:1, 1:3 are 2K only. |
| `seed` | number |  |  | Optional integer seed. |
| `duration` | string |  | "0" | Send "0". |

Rules:
- Credits for images that are not delivered are refunded automatically.
- generation_type must be text-to-image or image-to-image.
- prompt required, max 10000 characters (422).
- num_images must be an integer 1-8 (422).
- resolution must be valid for the chosen aspect_ratio (422).
- text-to-image must not include images (422); edit_precision and mask_url are rejected (422).
- aspect_ratio auto is not allowed for text-to-image.
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field. With num_images > 1, all images are in result_images.

Example body:

```json
{"mode": "ideogram-4-5", "generation_type": "text-to-image", "prompt": "A vintage travel poster with the bold title \"VISIT LISBON\" and a yellow tram", "duration": "0", "quality": "low", "num_images": 1, "aspect_ratio": "1:1", "resolution": "1K", "enable_prompt_expansion": true}
```

### `ideogram-4-5` · `image-to-image`

Edits an image (optionally with a mask and reference images) with accurate text rendering via Ideogram 4.5.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 10000 characters. |
| `images` **required** | string[] |  |  | images[0] = image to edit; images[1..] = up to 4 reference images (3 with a mask). http(s) URLs only. |
| `quality` 💲 | string | "very_low", "low", "medium", "high" | "very_low" |  |
| `num_images` 💲 | number | 1–8 | 1 | Images per request (1-8); the price is multiplied by num_images. |
| `edit_precision` | string | "regular", "high" | "regular" | Edit precision. |
| `mask_url` | string |  |  | Black/white mask URL, same size as the source image; black = area to change. |
| `aspect_ratio` | string | "auto", "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "5:4", "4:5", "16:10", "10:16", "2:1", "1:2", "12:5", "5:12", "22:9", "9:22", "23:9", "9:23", "8:3", "3:8", "3:1", "1:3" | "auto" | auto keeps the source image size. |
| `resolution` | string | "1K", "2K" |  | Resolution tier for the chosen aspect_ratio; defaults to the lowest available. 12:5, 5:12, 22:9, 9:22, 23:9, 9:23, 8:3, 3:8, 3:1, 1:3 are 2K only. Not allowed with aspect_ratio auto. |
| `seed` | number |  |  | Optional integer seed. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: 1 image to edit + 0-4 reference image URLs (0-3 with a mask).
- `mask`: Optional mask_url (PNG, black = edit area, same size as the source).

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`, mask → `image-generator`

Rules:
- Credits for images that are not delivered are refunded automatically.
- generation_type must be text-to-image or image-to-image.
- prompt required, max 10000 characters (422).
- num_images must be an integer 1-8 (422).
- resolution must be valid for the chosen aspect_ratio (422).
- very_low quality is available for image-to-image only.
- Needs at least 1 image; at most 4 reference images after the first (3 when mask_url is set). Image URLs must be http(s).
- enable_prompt_expansion is rejected for image-to-image (422).
- A non-auto aspect_ratio/resolution is only allowed with edit_precision=regular and no mask (422).
- mask_url is only accepted for qwen-image-2-1 and ideogram-4-5 and must be an http(s) URL.
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field. With num_images > 1, all images are in result_images.

Example body:

```json
{"mode": "ideogram-4-5", "generation_type": "image-to-image", "prompt": "Replace the sign text with \"OPEN\"", "duration": "0", "quality": "very_low", "num_images": 1, "aspect_ratio": "auto", "images": ["https://example.com/source.jpg"], "edit_precision": "regular"}
```

## GPT Image 2 — `gpt-image-2`

### `gpt-image-2` · `text-to-image`

Generates photoreal images with sharp text rendering from a prompt with GPT Image 2.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 20000 characters. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" |  |
| `aspect_ratio` | string | "auto", "1:1", "3:2", "2:3", "4:3", "3:4", "5:4", "4:5", "16:9", "9:16", "2:1", "1:2", "3:1", "1:3", "21:9", "9:21" | "auto" | Omitted = auto. |
| `background` | string | "auto", "opaque", "transparent" | "auto" | Values other than auto are only allowed at 1K. |
| `duration` | string |  | "0" | Send "0". |

Rules:
- generation_type must be text-to-image or image-to-image; prompt required, max 20000 characters (422).
- aspect_ratio auto (or omitted) only supports 1K (422).
- 1:1 does not support 4K (422).
- 5:4, 4:5, 3:1, 1:3 and 9:21 are not supported at 2K; 3:1, 1:3 and 9:21 are not supported at 4K (422).
- background other than auto is only allowed at 1K (422).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "gpt-image-2", "generation_type": "text-to-image", "prompt": "A modern storefront poster with the headline \"Summer Sale\" in bold serif type", "duration": "0", "aspect_ratio": "auto", "resolution": "1K", "images": []}
```

### `gpt-image-2` · `image-to-image`

Edits/combines up to 16 reference images from a prompt with GPT Image 2.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 20000 characters. |
| `images` **required** | string[] |  |  | 1-16 reference image URLs. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" |  |
| `aspect_ratio` | string | "auto", "1:1", "3:2", "2:3", "4:3", "3:4", "5:4", "4:5", "16:9", "9:16", "2:1", "1:2", "3:1", "1:3", "21:9", "9:21" | "auto" | Omitted = auto. |
| `background` | string | "auto", "opaque", "transparent" | "auto" | Values other than auto are only allowed at 1K. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: 1-16 reference image URLs.

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- generation_type must be text-to-image or image-to-image; prompt required, max 20000 characters (422).
- aspect_ratio auto (or omitted) only supports 1K (422).
- 1:1 does not support 4K (422).
- 5:4, 4:5, 3:1, 1:3 and 9:21 are not supported at 2K; 3:1, 1:3 and 9:21 are not supported at 4K (422).
- background other than auto is only allowed at 1K (422).
- image-to-image requires a non-empty images array (or image) (400).
- At most 16 reference images (400).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "gpt-image-2", "generation_type": "image-to-image", "prompt": "A modern storefront poster with the headline \"Summer Sale\" in bold serif type", "duration": "0", "aspect_ratio": "auto", "resolution": "1K", "images": ["https://example.com/ref.jpg"]}
```

## GPT Image 2.5 — `gpt-image-2-5`

### `gpt-image-2-5` · `text-to-image`

Generates sharper, detailed images from a prompt with GPT Image 2.5 (Flare/Sunburst).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 20000 characters. |
| `gptImage25Version` | string | "flare", "sunburst" | "flare" | Quality tier; flare and sunburst currently cost the same. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" |  |
| `aspect_ratio` | string | "auto", "1:1", "3:2", "2:3", "4:3", "3:4", "16:9", "9:16", "21:9", "27:16", "16:27", "9:8", "8:9" | "auto" | Omitted = auto. 27:16, 16:27, 9:8, 8:9 are 1K only. |
| `background` | string | "auto", "opaque", "transparent" | "auto" | Available at all resolutions. |
| `duration` | string |  | "0" | Send "0". |

Rules:
- generation_type must be text-to-image or image-to-image; prompt required, max 20000 characters (422).
- 27:16, 16:27, 9:8, 8:9 are only available at 1K (422).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "gpt-image-2-5", "generation_type": "text-to-image", "prompt": "A cinematic night city poster with neon reflections on a rainy street", "duration": "0", "aspect_ratio": "auto", "resolution": "1K", "gptImage25Version": "flare", "background": "auto", "images": []}
```

### `gpt-image-2-5` · `image-to-image`

Edits up to 16 reference images with stronger reference fidelity using GPT Image 2.5.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 20000 characters. |
| `images` **required** | string[] |  |  | 1-16 reference image URLs. |
| `gptImage25Version` | string | "flare", "sunburst" | "flare" | Quality tier; flare and sunburst currently cost the same. |
| `resolution` 💲 | string | "1K", "2K", "4K" | "1K" |  |
| `aspect_ratio` | string | "auto", "1:1", "3:2", "2:3", "4:3", "3:4", "16:9", "9:16", "21:9", "27:16", "16:27", "9:8", "8:9" | "auto" | Omitted = auto. 27:16, 16:27, 9:8, 8:9 are 1K only. |
| `background` | string | "auto", "opaque", "transparent" | "auto" | Available at all resolutions. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: 1-16 reference image URLs.

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`

Rules:
- generation_type must be text-to-image or image-to-image; prompt required, max 20000 characters (422).
- 27:16, 16:27, 9:8, 8:9 are only available at 1K (422).
- image-to-image requires a non-empty images array (or image) (400).
- At most 16 reference images (400).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "gpt-image-2-5", "generation_type": "image-to-image", "prompt": "A cinematic night city poster with neon reflections on a rainy street", "duration": "0", "aspect_ratio": "auto", "resolution": "1K", "gptImage25Version": "flare", "background": "auto", "images": ["https://example.com/ref.jpg"]}
```

## Qwen Image 2.1 — `qwen-image-2-1`

### `qwen-image-2-1` · `text-to-image`

Generates images (including native transparent PNGs) from a prompt with Qwen Image 2.1.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 5000 characters. |
| `resolution` 💲 | string | "1K", "2K" | "1K" |  |
| `aspect_ratio` | string | "1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16" | "1:1" | Text-to-image default 1:1; auto is not available. |
| `background` | string | "opaque", "transparent" | "opaque" | transparent returns a native transparent PNG; 'auto' is rejected. |
| `duration` | string |  | "0" | Send "0". |

Rules:
- generation_type must be text-to-image or image-to-image; prompt required, max 5000 characters (422).
- resolution must be 1K or 2K (422).
- background must be opaque or transparent (422).
- Text-to-image aspect ratios: 1:1, 4:3, 3:4, 3:2, 2:3, 16:9, 9:16 (auto is rejected, 422).
- mask_url is rejected for text-to-image (422).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "qwen-image-2-1", "generation_type": "text-to-image", "prompt": "A glossy cartoon sticker of a corgi astronaut, transparent background", "duration": "0", "aspect_ratio": "1:1", "resolution": "1K", "background": "transparent", "images": []}
```

### `qwen-image-2-1` · `image-to-image`

Edits up to 10 reference images, or inpaints one image with a mask, using Qwen Image 2.1.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Required, non-empty, max 5000 characters. |
| `images` **required** | string[] |  |  | 1-10 reference image URLs (exactly 1 with mask_url). |
| `resolution` 💲 | string | "1K", "2K" | "1K" |  |
| `aspect_ratio` | string | "auto", "1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16" | "auto" | Image-to-image default auto. When mask_url is set, auto is always used. |
| `background` | string | "opaque", "transparent" | "opaque" | transparent returns a native transparent PNG; 'auto' is rejected. |
| `mask_url` | string |  |  | Black/white mask URL for inpainting; white = area to change. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: 1-10 reference image URLs (exactly 1 when using a mask).
- `mask`: Optional mask_url (black/white PNG, white = edit area).

Upload folders (`folder` for `POST /api/storage/upload`): image → `image-generator`, mask → `image-generator`

Rules:
- generation_type must be text-to-image or image-to-image; prompt required, max 5000 characters (422).
- resolution must be 1K or 2K (422).
- background must be opaque or transparent (422).
- image-to-image requires a non-empty images array (or image) (400).
- At most 10 reference images (422).
- mask_url requires exactly 1 image and cannot be combined with background=transparent (422); with a mask, aspect_ratio is always auto.
- Image-to-image aspect ratios: auto, 1:1, 4:3, 3:4, 3:2, 2:3, 16:9, 9:16 (422).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "qwen-image-2-1", "generation_type": "image-to-image", "prompt": "A glossy cartoon sticker of a corgi astronaut, transparent background", "duration": "0", "aspect_ratio": "auto", "resolution": "1K", "background": "opaque", "images": ["https://example.com/ref.jpg"]}
```

## Virtual Try-On — `virtual-try-on`

### `virtual-try-on` · `image-to-image`

Dresses the person in a photo in 1-3 garment images.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `images` **required** | string[] |  |  | [person photo, 1-3 garment images]; images[0] is always the person. |
| `prompt` | string |  |  | Optional extra instruction appended to the built-in try-on instruction, max 1000 characters. |
| `aspect_ratio` | string | "auto", "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9" | "auto" | Omit or send auto to follow the person photo's ratio. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: images[0] = person photo URL, images[1..3] = 1-3 garment image URLs.

Upload folders (`folder` for `POST /api/storage/upload`): image → `virtual-try-on`

Rules:
- generation_type must be image-to-image (422).
- images must be [person, 1-3 garment images] (422).
- prompt max 1000 characters (422).
- aspect_ratio must be auto or one of 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9 (422).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "virtual-try-on", "generation_type": "image-to-image", "prompt": "", "duration": "0", "images": ["https://example.com/person.jpg", "https://example.com/garment.jpg"]}
```

## Product Holding — `product-holding`

### `product-holding` · `image-to-image`

Places 1-3 product images into the hands of the person in a photo.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `images` **required** | string[] |  |  | [person photo, 1-3 product images]; images[0] is always the person. |
| `prompt` | string |  |  | Optional extra instruction appended to the built-in product-holding instruction, max 1000 characters. |
| `aspect_ratio` | string | "auto", "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9" | "auto" | Omit or send auto to follow the person photo's ratio. |
| `duration` | string |  | "0" | Send "0". |

Input files:
- `images`: images[0] = person photo URL, images[1..3] = 1-3 product image URLs.

Upload folders (`folder` for `POST /api/storage/upload`): image → `virtual-try-on`

Rules:
- generation_type must be image-to-image (422).
- images must be [person, 1-3 product images] (422).
- prompt max 1000 characters (422).
- aspect_ratio must be auto or one of 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9 (422).
- Asynchronous: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{generation_id}/status until status='completed'; the first image URL is in video_url and all output images are in result_images (array). The status response has no image_url field.

Example body:

```json
{"mode": "product-holding", "generation_type": "image-to-image", "prompt": "", "duration": "0", "images": ["https://example.com/person.jpg", "https://example.com/product.jpg"]}
```
