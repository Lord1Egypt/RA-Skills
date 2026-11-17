# Restore and upscale - worked recipes

Three end-to-end recipes covering the main paths: a straight still upscale, an old-photo restore, and a video upscale. No model guide exists for these, so every field and range below was read off the live request schemas. Re-confirm with `runware-run` before calling, since the catalog moves.

The still upscalers are `taskType: "upscale"` and return the result on the same call. The restore via Bria FIBO Edit is `taskType: "imageInference"` and also returns inline. The Topaz video path is `taskType: "upscale"` but async, so you poll for it. Each recipe states its own result shape.

## Verified `upscaleFactor` limits

Read off each model's request schema. Send only a listed value or the call is rejected.

- Real-ESRGAN (`runware:504@1`): **2 or 4**
- SwinIR (`runware:503@1`): **2 or 4**
- CCSR (`runware:501@1`): **2 only**
- Clarity (`runware:500@1`): **2 only**

## 1. Straight upscale - enlarge a real photo (Real-ESRGAN)

**Scenario.** The user hands over a 768 x 512 photo from an old phone and asks to "make it 4x bigger and sharper." Nothing is broken, it is just small and a little soft. This is pure super-resolution, no restoration.

Use **Real-ESRGAN** (`runware:504@1`). It is the default GAN upscaler for real-world photos, denoises while it enlarges, and supports the 4x the user asked for. Pass the source in `inputs.image` and the factor in `upscaleFactor`.

```json
{
  "taskType": "upscale",
  "model": "runware:504@1",
  "inputs": {
    "image": "https://example.com/phone-photo-768.jpg"
  },
  "upscaleFactor": 4
}
```

Result (returns on the same call, no polling):

```json
{
  "data": [
    {
      "taskType": "upscale",
      "taskUUID": "<echoes your request>",
      "imageUUID": "<uuid of the result>",
      "imageURL": "https://im.runware.ai/image/.../<imageUUID>.jpg"
    }
  ]
}
```

Field notes (verified against the live schema):

- `inputs.image` is required. `upscaleFactor` is an integer enum, **2 or 4** on this model.
- `imageUUID` is the only guaranteed field on the result. `imageURL` is present when you deliver by URL. Reference either downstream.
- For a genuinely degraded capture (heavy JPEG blocking, very low res) where there is little real detail to enlarge, switch to **CCSR** (`runware:501@1`), a diffusion upscaler that fills missing detail. CCSR is **2x only**, so for a bigger jump run it at 2x and stop, do not chain a second pass.

## 2. Old-photo restore - scratches, fading, color cast (Bria FIBO Edit)

**Scenario.** The user uploads a scanned 1960s family photo: scratches, dust, a yellow color cast, faded contrast. The ask is "restore this old photo," which is broader than upscaling. There is damage to undo, not just pixels to add.

Use **Bria FIBO Edit** (`bria:21@1`). It is instruction-driven editing, so write the restoration as a plain instruction and tell it to preserve everything else. This is `taskType: "imageInference"`, not `upscale`.

```json
{
  "taskType": "imageInference",
  "model": "bria:21@1",
  "inputs": {
    "image": "https://example.com/scan-1960s.jpg"
  },
  "positivePrompt": "restore this old photograph: remove scratches and dust, correct the faded yellow color cast, recover contrast, sharpen gently, keep the original composition and faces unchanged",
  "CFGScale": 5,
  "steps": 50
}
```

Result (returns inline, this is an `imageInference` response):

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "<echoes your request>",
      "imageUUID": "<uuid of the result>",
      "imageURL": "https://im.runware.ai/image/.../<imageUUID>.jpg"
    }
  ]
}
```

Field notes (verified against the live schema):

- `inputs.image` and `positivePrompt` are both required. `positivePrompt` is 2 to 3000 characters.
- `inputs.mask` is optional. Add one to scope the fix to a damaged region (a torn corner, a stain) without touching the rest.
- `CFGScale` is an enum, one of `3`, `4`, `5` (default `5`). `steps` ranges 20 to 50 (default `50`).
- Restore first, enlarge last. If the restored photo is still small, run the result through Real-ESRGAN (recipe 1) as a second step. Do not enlarge before restoring or you scale up the scratches.
- **Faces:** there is no face-specific restoration model on Runware. Bria FIBO Edit improves a face as a side effect, but do not promise eyes, teeth, or identity were reconstructed. If a barely-recognizable face must come back sharp and correct, that is reference-guided regeneration (see `character-consistency`), not this path.

## 3. Video upscale - denoise and enlarge footage (Topaz Starlight Precise 2.5)

**Scenario.** The user has a noisy 1280 x 720 clip and wants it cleaned up and pushed to 4K. This is video, so the still upscalers do not apply.

Use **Topaz Starlight Precise 2.5** (`topazlabs:starlight-precise@2.5`). It is a diffusion video upscaler that denoises, de-aliases, and sharpens with full temporal consistency. It takes `inputs.video` and a target `width` and `height` (both required), and it runs **async**, so submit and poll, do not block a sync call on it.

```json
{
  "taskType": "upscale",
  "model": "topazlabs:starlight-precise@2.5",
  "inputs": {
    "video": "https://example.com/clip-720p.mp4"
  },
  "width": 3840,
  "height": 2160,
  "fps": 30,
  "deliveryMethod": "async"
}
```

Result (poll `getResponse` until it lands, then read `videoURL`):

```json
{
  "data": [
    {
      "taskType": "upscale",
      "taskUUID": "<echoes your request>",
      "videoUUID": "<uuid of the result>",
      "videoURL": "https://vm.runware.ai/video/.../<videoUUID>.mp4"
    }
  ]
}
```

Field notes (verified against the live schema):

- `inputs.video`, `width`, and `height` are all required. `width` maxes at 3840, `height` at 2160. Aspect ratio is preserved by computing the factor from the shorter edge, so pick a target box and the model fits the clip inside it.
- `fps` is optional, range 15 to 120. The floor is 15 or the input's own frame rate, whichever is higher.
- This is the only video path here. The still upscalers (recipes 1 and 2) are image-only and will reject a video input.
