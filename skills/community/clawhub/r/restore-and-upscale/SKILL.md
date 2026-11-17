---
name: restore-and-upscale
description: >
  Improve image quality and resolution. Use when the user says "upscale this", "make it sharper /
  higher-res", "deblur", "denoise", "dehaze", "restore this old photo", "fix this low-res /
  pixelated image", "clean up this scan", or "enhance". Covers super-resolution and restoration of
  damaged, blurry, noisy, or small images, with no change to the content. To add, remove, or
  replace things in the image, use edit-image. For video, use video-upscale.
---

# Restore and upscale

Take a degraded or low-resolution image and return a cleaner, sharper, larger one: deblur, denoise, dehaze, recover detail, and enlarge 2x to 4x. The lever is matching the *kind* of damage to the right model, not running everything through one upscaler. For video, a dedicated temporal model exists. For worked end-to-end recipes (straight upscale, old-photo restore, video upscale), see `references/examples.md`.

## Inputs to collect

- **The source image (or video).** A URL or upload. (Ask only if none provided.)
- **What's wrong with it:** soft/blurry, noisy/grainy, hazy, compressed/JPEG artifacts, just too small, or an old/damaged photo. This routes the model.
- **Target size or factor:** 2x or 4x, or a target resolution. The supported factors vary by model, so confirm against the schema before promising one.
- **Fidelity vs invention:** "stay faithful to the original" (transformer/GAN upscalers) or "add believable detail" (diffusion upscalers). They behave differently and this is the most important routing question.
- **Content type:** photo, document/text, artwork, or screenshot. Documents and text demand a faithful (non-diffusion) path so characters don't get reinvented.

## Models

- **Default still-image upscaler: Real-ESRGAN** (`runware:504@1`). Practical GAN upscaler for real-world photos, 2x or 4x, denoises while enlarging. Reliable general pick.
- **Sharp, faithful, low-artifact: SwinIR** (`runware:503@1`). Transformer restorer, strong texture recovery with minimal hallucination. Good when you must stay true to the source. 2x or 4x.
- **Creative detail boost: Clarity** (`runware:500@1`). Enhances perceived detail during enlargement, accepts a guiding `positivePrompt`. 2x. Best when the input is clean and you want more pop.
- **Diffusion super-resolution for rough real-world inputs: CCSR** (`runware:501@1`). Restores detail on genuinely low-quality images while keeping artifacts controlled. 2x only.
- **General "restore / fix this photo" (edit-style): Bria FIBO Edit** (`bria:21@1`). Instruction-driven editing. Describe the restoration ("remove scratches, fix faded color, sharpen") in natural language. Use when the ask is broader than pure upscaling.
- **Video enhancement: Topaz Starlight Precise 2.5** (`topazlabs:starlight-precise@2.5`). Diffusion video upscaler that denoises, de-aliases, and sharpens with full temporal consistency. This one is **video-to-video**, not images.
- All four still upscalers are Runware-hosted (Optimized). Confirm the live model + its schema via the `runware-models` and `runware-run` skills before calling. Never hardcode a stale choice.

## No dedicated face restoration

There is currently **no face-specific restoration model** on Runware (no GFPGAN / CodeFormer-class model). Faces do improve as a side effect of the general upscalers above, but there is no model that targets faces, fixes eyes/teeth, or reconstructs identity from a degraded portrait. Set this expectation plainly before running:

- For a blurry or low-res face, run a general upscaler and report that the result on the face is best-effort, not a dedicated restore.
- Don't claim a face was "restored." It was upscaled, and fine facial detail may stay soft or shift slightly.
- If true identity recovery is the goal (a barely-recognizable face that must come back sharp and correct), that is a different workflow: reference-guided regeneration, see `character-consistency`. That trades faithfulness to the original pixels for a believable, sharp face.

## Workflow

1. **Diagnose the damage** from the input and the user's words, then route to the model above.
2. **Resolve the schema** (`runware-run`) and confirm the input field and the allowed `upscaleFactor` values for that model. They differ (some are 2x only, some 2x/4x).
3. **Upload the source** into the model's input field (`inputs.image` for the still upscalers, `inputs.video` for Topaz).
4. **Run with the right taskType and delivery mode:**
   - Still upscalers (Real-ESRGAN, SwinIR, Clarity, CCSR) → `taskType: "upscale"`, **synchronous**. The call returns the upscaled image.
   - Bria FIBO Edit → `taskType: "imageInference"`, synchronous, with the restoration written as an instruction.
   - Topaz Starlight (video) → `taskType: "upscale"` over video, **asynchronous + poll** `getResponse`. It returns a `videoURL`. Don't block a sync call on it.
5. **Inspect the output** at full resolution before returning. If it over-smoothed or invented wrong detail, switch model class (see Technique) and retry.

## Technique

- **Match the model to the damage.** Noise/grain and "just enlarge a real photo" → Real-ESRGAN. Must stay faithful with crisp texture (documents, product shots, anything where invented detail is wrong) → SwinIR. Clean input, want more punch → Clarity. Genuinely degraded real-world capture (heavy compression, very low res) → CCSR, where diffusion fills missing detail. Broad "fix this old photo" with scratches, fading, and color casts → Bria FIBO Edit as an edit instruction, then upscale the result if it's still small.
- **GAN/transformer vs diffusion is the core tradeoff.** GAN (Real-ESRGAN) and transformer (SwinIR) upscalers stay close to the pixels and rarely invent. Diffusion upscalers (CCSR, and Clarity when prompted) recover or *imagine* detail, which is great for soft inputs and risky for documents, faces, or anything where invented detail is wrong. When fidelity is non-negotiable, prefer the non-diffusion path. When the input is so soft there's no real detail to recover, diffusion is the only thing that helps.
- **Upscale once, at the right factor.** Don't chain 2x then 2x again hoping for better. Pick the factor the model supports and run it once. Re-upscaling compounds artifacts.
- **Restore before you enlarge.** If an image is both damaged *and* small, fix the damage first (denoise, descratch, color-correct) and upscale last, so you're not enlarging the artifacts. For a one-shot "fix and enlarge" on a clean-ish photo, a single upscaler pass is fine.
- **Guide Clarity with a short prompt.** Clarity accepts a `positivePrompt` to steer the enhancement (e.g. "sharp natural skin texture, fine fabric detail"). Keep it descriptive of texture, not a new scene, or it starts inventing.
- **For restoration via Bria FIBO Edit, write the fix as an instruction** and preserve everything else: "restore this old photograph: remove scratches and dust, correct faded color, sharpen, keep the original composition and faces unchanged." Don't ask it to re-render the scene. A mask scopes the fix to a damaged region without touching the rest.
- **Faces:** state up front there is no face-restore model. Run a general upscaler, and if a face still looks wrong, that's the ceiling here, not a tuning problem. The escape hatch is regeneration, not a different upscaler.

## Parameters that matter

- `inputs.image` (still upscalers) / `inputs.video` (Topaz) is the source. Confirm the exact field against the live schema and never guess.
- `upscaleFactor` is **2 or 4** on Real-ESRGAN and SwinIR, and **2 only** on CCSR and Clarity. Check the schema enum before sending an unsupported value.
- `settings.positivePrompt` is available on Clarity to steer enhancement. Optional, texture-focused.
- Topaz video: `width` / `height` (target, aspect preserved from the shorter edge, up to 3840x2160) and `fps` (15 to 120, at least the input's rate). Both `width` and `height` are required.
- Bria FIBO Edit runs as a standard `imageInference` edit. Put the restoration in the instruction prompt, optionally with a mask for localized fixes.

## Quality bar

- Output is sharper and cleaner *and* still looks like the original subject. No plastic over-smoothing, no invented detail where fidelity matters (text, documents, faces).
- The enlargement hit the requested factor/size and the schema accepted the `upscaleFactor`.
- For diffusion upscalers, confirm hallucinated detail is plausible and wanted. If not, rerun on a GAN/transformer model.
- Faces were handled honestly: improved via a general upscaler, with the no-dedicated-face-restore limitation communicated, not silently papered over.
- Video upscales were run async and the `videoURL` was retrieved, not blocked on a sync call.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `edit-image` (instruction edits and broader fixes), `product-photography` (clean, high-res product shots), `character-consistency` (reference-guided regeneration when a degraded face needs identity recovery).
