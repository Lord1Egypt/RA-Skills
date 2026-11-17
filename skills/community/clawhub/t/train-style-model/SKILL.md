---
name: train-style-model
description: >
  Fine-tune a reusable brand, style, or character model (a LoRA) from a small set of reference
  images, then generate on-brand imagery from any prompt. Use when the user says "train a model on
  our brand style", "make a LoRA from these images", "fine-tune on our look", "a custom model that
  draws in our style", or "consistent illustrations at scale". An async training job, not one-shot
  generation. To upload a model you already trained elsewhere, use bring-your-own-model. For
  same-identity output without training, use character-consistency.
---

# Train a style model

Train a custom image model (a LoRA) on a brand's visual identity from 10 to 50 reference images, then generate new imagery in that exact look from any prompt. This is the durable, at-scale answer when a team needs the *same hand* across endless asset variations. For a few consistent images right now, prefer `character-consistency` (references) instead. Training takes about two hours and is submitted once, then polled.

## Inputs to collect

- **The training dataset.** A single ZIP of 10 to 50 images that share one visual style across deliberately varied subjects. (Ask for this if not provided. It is the whole job.)
- **The target AIR** to register the trained model under (your org namespace, e.g. `yourorg:brand-illustration@1`). Suggest a stable, versioned one if the user has none.
- **Model name + short description** for the registered model, and whether it should be `private` (default `true` while iterating).
- Optional: what subjects they will generate after, so you can sanity-check the dataset has the right subject variety.

## Models

- **Default: Exactly Illustrative Training** (`exactly:illustrative@training`, live) - trains a style LoRA from a ZIP dataset and registers it for `imageInference`. The only live `op:train` model today.
- Confirm the live trainer and its schema via `runware-models` (capability `op:train`) + `runware-run` before calling. Never hardcode a stale choice. The catalog moves.

## Workflow

1. Resolve the trainer's schema (`runware-run`) and confirm the input field names and the dataset bounds before building the request.
2. Curate and zip the dataset (see Technique), host the ZIP at a public URL the platform can fetch, and pass it as `inputs.dataset`.
3. Submit the **async** `training` task with an `importModel` block that reserves the target AIR, name, description, and `private` flag in one round trip.
4. **Poll for completion.** The submit returns a `taskUUID` immediately. Submit `getResponse` with that UUID every 5 to 10 minutes. `status` moves from `processing` (with `progress`) to `success` (model live at the AIR) or `error` (read `error.code` / `error.message`).
5. On `success`, generate with the trained model exactly like any other: a normal `imageInference` request with the trained AIR in `model`. The skill is over once the model is live and produces on-brand output.

For two worked recipes (train a brand LoRA end to end with poll loop, then generate with the trained AIR), see `references/examples.md`.

## Technique

The dataset is the lever. Every other parameter is mechanical. Two principles do most of the work.

- **Hold the style constant, vary the subject.** Every image should look like it came from the same hand on the same brief: same palette, line work, lighting, composition language, level of detail and abstraction. Then make subjects as varied as you can (different scenes, objects, framings). The model learns the *constant signal* as "the style" and treats the varying subjects as proof the style is decoupled from any one of them. If half the set is portraits, the model concludes "is a portrait" is part of the style.
- **Trim outliers.** One image that breaks the visual language pulls the averaged result off-brand, even if it is the team's favorite. Cut it.
- **Watch for accidental consistencies.** If the dataset shares anything beyond the style (mostly landscapes, mostly centered, mostly low-key lit), the model absorbs that too. Audit against the style brief and remove unintended patterns.
- **Generate with no style cues.** Once trained, prompt only for the subject. The style is baked in, and restating it makes output feel overcooked. The trained model picks up in-brand wordmarks automatically: quote the exact string (`a sign reading "STELLAR"`) to render it.
- **Treat it as a loop.** A first training rarely lands. Train, evaluate on subjects deliberately absent from the set, find what it learned wrong, adjust the dataset, bump the version, retrain.

Run this checklist over the set before zipping:

- [ ] One style across every image (palette, line work, lighting, detail, abstraction).
- [ ] Subjects deliberately varied (scenes, objects, framings).
- [ ] Outliers cut, even favorites.
- [ ] No accidental shared pattern beyond the style (mostly landscapes, mostly centered, mostly low-key lit).
- [ ] Count inside the 10 to 50 bound.

## Parameters that matter

- `inputs.dataset` - a single **ZIP** at a public URL. **10 to 50 images**, a hard bound (below 10 and above 50 both reject). JPEG, PNG, or WebP. Max 50 MB per image (auto-downscaled to 4096px long side, so no pre-resize needed).
- `importModel` - embeds the model registration in the training request: `air` (the target AIR you reserve), `name`, `shortDescription`, `version`, `private`. Bump `version` (`@2`) on retrain rather than overwriting, for A/B and rollback.
- Poll cadence: every 5 to 10 minutes is plenty against the ~2 hour wall time. Do not block a sync call on it.
- Generation (after training): the trained AIR takes the same surface as base Exactly Illustrative - `positivePrompt`, `width`/`height` 1024 to 2048 in multiples of 64, optional single `inputs.referenceImages` (type `sketch` with `strength`, or `reference` for style guidance), and `settings.quality` (`"low"` default for iterating, `"high"` for ship assets).
- Confirm exact field names against the live schema (`runware-run`). Never guess.

## Quality bar

- The dataset holds the style constant and varies the subject, with outliers and accidental consistencies trimmed, and sits inside the 10 to 50 bound.
- The job was submitted async and polled to a terminal `status`, not blocked on a sync call.
- The trained model transfers cleanly to subjects that were *not* in the dataset (test 10 to 20 outside-set prompts). If it only works on near-training subjects, widen subject variety and retrain.
- Generated output reads as one consistent on-brand look across varied subjects and formats.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `character-consistency` (consistent images now via references, no training), `bring-your-own-model` (import or manage an existing model), `game-assets-2d` (a style-consistent asset set this can feed).
