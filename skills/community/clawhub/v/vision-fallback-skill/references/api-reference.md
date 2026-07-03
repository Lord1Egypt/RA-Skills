# API Reference — Volcengine Ark (doubao) vision

## Endpoint

```
POST https://ark.cn-beijing.volces.com/api/plan/v3/chat/completions
```

## Headers

```
Authorization: Bearer ${ARK_API_KEY}
Content-Type: application/json
```

## Request body

`content` is an ARRAY mixing text + `image_url` — this is mandatory for
multimodal input.

```json
{
  "model": "doubao-seed-2.0-lite",
  "messages": [
    {
      "role": "system",
      "content": "You are a multimodal vision reasoning fallback model. Your job is to interpret images when the primary model fails. Return strict, structured JSON only."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze the attached image and reconstruct its meaning.\n\nFailure reason:\n{{failure_reason}}\n\nOCR text (if any):\n{{ocr_text}}\n\nPrimary model output:\n{{primary_model_output}}\n\nTasks:\n1. Describe what is shown in the image\n2. Extract UI elements / objects / text\n3. Reconstruct layout or structure\n4. Infer missing parts if needed (mark clearly as inferred)\n\nRespond as JSON with keys: summary, objects, text_detected, ui_structure, inferred_elements, uncertainty_notes."
        },
        {
          "type": "image_url",
          "image_url": { "url": "{{IMAGE_URL}}" }
        }
      ]
    }
  ],
  "temperature": 0.2
}
```

A ready-to-fill template lives at
[../assets/payload-template.json](../assets/payload-template.json).

## Model note

Use `doubao-seed-2.0-lite` (configured for this skill).

## Image payload preparation

The doubao vision API requires the image inside the message `content` array as
an `image_url` part. Convert local files to a base64 data URL first:

```bash
IMG="$IMAGE_PATH"
MIME=$(file -b --mime-type "$IMG")
B64=$(base64 -w0 "$IMG")
IMAGE_URL="data:${MIME};base64,${B64}"
```

If `image` is already an `http(s)://` URL or a `data:` URL, use it directly.

## Minimal curl example

```bash
curl -sS https://ark.cn-beijing.volces.com/api/plan/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payload.json
```
