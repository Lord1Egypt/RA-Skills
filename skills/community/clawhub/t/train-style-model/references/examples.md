# Worked recipes

Two end-to-end recipes for training a custom style model on Exactly Illustrative Training (`exactly:illustrative@training`) and generating with the trained AIR. Each shows the scenario, the actual request with concrete values, and the result shape. Training is an async task, so each recipe submits once, polls `getResponse`, then generates. Confirm field names and the dataset bounds against the live schema (`runware-run`) before calling. Send requests as a JSON array even for a single task.

Contract notes for `exactly:illustrative@training`:
- `inputs.dataset` is a single ZIP (URL or UUID), `minItems` 10 and `maxItems` 50. Both bounds are hard. JPEG, PNG, or WebP inside. Max 50 MB per image (auto-downscaled to 4096px long side).
- `importModel` is required alongside `inputs`. It needs `air` and `name`. Optional: `shortDescription`, `version`, `private`, `heroImageURL`, `uniqueIdentifier`.
- The submit response returns only `taskType` + `taskUUID`. Poll with `getResponse` on that UUID. `status` is `processing` (with `progress` 0 to 100), then `success` (response carries the trained `air` and `outputs.files`) or `error` (response carries `error.code` + `error.message`).
- After `success`, generate with a normal `imageInference` request that passes the trained AIR in `model`.

## Dataset-curation rule

Before zipping, audit the set against three checks. The dataset is the only lever, so this is the work.

- **Hold the style constant.** Every image must read like the same hand on the same brief: one palette, one line-work language, one lighting, one level of detail and abstraction. The model learns the constant signal as "the style."
- **Vary the subject.** Different scenes, objects, framings. Varied subjects prove the style is decoupled from any one of them. If half the set is portraits, the model folds "is a portrait" into the style.
- **Trim outliers and accidental consistencies.** Cut any image that breaks the visual language, even a favorite, because the result averages across the set. Then cut unintended shared patterns (mostly landscapes, mostly centered, mostly low-key lit). Audit against the style brief and remove them.

## Recipe 1: Train a brand style LoRA end to end

Scenario: a fictional stargazing app, Stellar, wants its editorial cosmic illustration look as a reusable model. Visual identity is deep navy and dusky purple skies, warm gold accents, fine astronomical-engraving line work, slight grain. The team has curated 12 images that hold that style constant across varied subjects (a brass telescope, a Milky Way panorama, a Saturn diagram, an Orion constellation map, an observatory dome, a phone mockup) and zipped them.

Submit the async training task. The `importModel` block reserves the target AIR and registers the model in the same round trip. Keep `private: true` while iterating.

```json
[
  {
    "taskType": "training",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "exactly:illustrative@training",
    "inputs": {
      "dataset": "https://example.com/stellar-dataset.zip"
    },
    "importModel": {
      "air": "yourorg:exactly-illustrative@stellar",
      "name": "Stellar",
      "shortDescription": "Editorial cosmic illustration in the Stellar brand style",
      "version": "1.0.0",
      "private": true
    }
  }
]
```

Submit response (immediate acknowledgment, no result yet):

```json
{
  "data": [
    {
      "taskType": "training",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    }
  ]
}
```

Poll with `getResponse` on the same `taskUUID`. Training takes about two hours, so poll every 5 to 10 minutes. Do not block a sync call on it.

```json
[
  {
    "taskType": "getResponse",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }
]
```

Still processing (a `progress` integer 0 to 100 reports how far along):

```json
{
  "data": [
    {
      "taskType": "training",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "status": "processing",
      "progress": 47
    }
  ]
}
```

On success, the model at the reserved AIR is live. The response carries the trained `air` and an `outputs.files` array for the trained weights:

```json
{
  "data": [
    {
      "taskType": "training",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "status": "success",
      "air": "yourorg:exactly-illustrative@stellar",
      "outputs": {
        "files": [
          {
            "fileURL": "https://im.runware.ai/model/ws/2/tr/yourorg-exactly-illustrative-stellar.safetensors"
          }
        ]
      }
    }
  ]
}
```

If the dataset failed the format or count check, the poll returns `status: "error"` with an `error` object instead. Read `code` and `message`, fix the dataset, and resubmit:

```json
{
  "data": [
    {
      "taskType": "training",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "status": "error",
      "error": {
        "code": "invalidDataset",
        "message": "Dataset must contain between 10 and 50 images."
      }
    }
  ]
}
```

Bump `importModel.version` to `2.0.0` on a retrain rather than overwriting, so you can A/B old against new and roll back.

## Recipe 2: Generate with the trained model

Scenario: the Stellar model from Recipe 1 is live at `yourorg:exactly-illustrative@stellar`. The team wants on-brand assets for subjects that were never in the training set.

Pass the trained AIR in `model` and prompt only for the subject. The style is baked in, so do not restate palette, line work, or mood. Restating style cues makes output feel overcooked. To render the brand wordmark, quote the exact string (`a sign reading "STELLAR"`).

```json
[
  {
    "taskType": "imageInference",
    "taskUUID": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
    "model": "yourorg:exactly-illustrative@stellar",
    "positivePrompt": "A red fox sitting on a mossy rock at dusk, gazing upward at the aurora",
    "width": 1024,
    "height": 1024
  }
]
```

Result (one image, `imageUUID` always present, `imageURL` when `outputType` is `URL`):

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "imageUUID": "9d8c7b6a-5f4e-3d2c-1b0a-9e8d7c6b5a4f",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/9d8c7b6a-5f4e-3d2c-1b0a-9e8d7c6b5a4f.jpg"
    }
  ]
}
```

For ship assets, switch `settings.quality` to `"high"` (default `"low"` is fine while iterating) and raise the size. The trained AIR takes the same surface as base Exactly Illustrative: `positivePrompt`, `width`/`height` 1024 to 2048 in multiples of 64, optional single `inputs.referenceImages` (type `sketch` with `strength`, or `reference` for style guidance), and `settings.quality`.

```json
[
  {
    "taskType": "imageInference",
    "taskUUID": "c3d4e5f6-a7b8-9012-cdef-345678901234",
    "model": "yourorg:exactly-illustrative@stellar",
    "positivePrompt": "A vintage compass resting on an open star chart, soft candlelight",
    "width": 1536,
    "height": 1536,
    "settings": {
      "quality": "high"
    }
  }
]
```

Verify the trained model by generating 10 to 20 prompts on subjects deliberately absent from the dataset. If the style transfers cleanly, the dataset taught the right thing. If output only holds for near-training subjects, widen the subject variety, bump the version, and retrain.
