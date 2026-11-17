# EmbeddingGemma 2 — multimodal embeddings

Use this reference for:

- text, image, audio, video, or mixed vectors;
- the exact `POST /v1/embeddings` wire contract;
- Local mode in the Singularity Node app;
- dimensions, limits, billing, privacy, and retry behavior.

## Availability

EmbeddingGemma 2 is a **release candidate and default off**. The pinned runtime has passed real
Apple Silicon text/image/audio/video/mixed tests, but production discovery and traffic remain
closed until the release migration, packaged desktop lifecycle, and live billing/failover
canaries pass.

Always discover it first:

```bash
python {baseDir}/scripts/grid_embeddings.py models
# or:
curl "https://grid.x402compute.cc/v1/models?type=embedding"
```

Proceed only if the response contains `embeddinggemma-2`. A catalog row alone cannot make the
model callable. Grid admission also requires an active node with the exact ready protocol,
runtime, processor revision, requested dimensions/modalities, sealed-input encoding, and model id.

## Grid request contract

**Endpoint:** `POST https://grid.x402compute.cc/v1/embeddings`

**Credits auth:** `X-API-Key: x402c_...` with `grid:write`.

**x402:** omit the API key, read the `402` response's `accepts[]`, sign the payment, and retry
with `X-Payment`.

Fields:

| Field | Values |
|---|---|
| `model` | `embeddinggemma-2` |
| `input` | String, string array, or 1-16 multimodal items. One vector per top-level item. |
| `dimensions` | `768` (default), `512`, `256`, or `128` |
| `input_type` | Optional: `query` (default when omitted), `document`, or `unspecified`. Use `unspecified` only to opt out of a retrieval prefix. |
| `encoding_format` | Omit or use `float` |
| `tier` | Optional `standard` or `confidential` |

Legacy text remains valid:

```json
{
  "model": "embeddinggemma-2",
  "input": ["first item", "second item"],
  "input_type": "query",
  "dimensions": 256
}
```

A multimodal item has 1-16 ordered `content` parts:

```json
{
  "model": "embeddinggemma-2",
  "input_type": "document",
  "dimensions": 256,
  "input": [{
    "content": [
      { "type": "text", "text": "Product demo" },
      {
        "type": "image",
        "media": {
          "encoding": "base64",
          "mime_type": "image/png",
          "data": "iVBORw0KGgo...",
          "sha256": "<64 lowercase hex characters>"
        }
      },
      {
        "type": "audio",
        "duration_seconds": 4.2,
        "media": {
          "encoding": "base64",
          "mime_type": "audio/mpeg",
          "data": "SUQzBAAAAA...",
          "sha256": "<64 lowercase hex characters>"
        }
      }
    ]
  }]
}
```

Media is inline only. The Grid never fetches media URLs. `sha256` is the lowercase hash of the
decoded bytes, and `data` is canonical base64 for those exact bytes. Audio and video require
`duration_seconds`; the runtime verifies real decoded duration and rejects understatement.

Omitting `input_type` is exactly equivalent to `"input_type":"query"` for EmbeddingGemma 2.
The Grid seals that explicit value with the ordered input, so admission, the quote, and runtime
prefixing cannot disagree. `unspecified` is an explicit opt-out and is never the default.

Use `grid_embeddings.py` to hash and encode files without loading credentials from a `.env`:

```bash
export COMPUTE_API_KEY="x402c_..."

python {baseDir}/scripts/grid_embeddings.py embed \
  --text "Product demo" \
  --image ./frame.png \
  --audio ./narration.mp3 --audio-seconds 4.2 \
  --input-type document --dimensions 256

# Inspect the exact JSON without sending:
python {baseDir}/scripts/grid_embeddings.py embed \
  --part text:"Product demo" \
  --part image:./frame.png \
  --part audio:./narration.mp3@4.2 \
  --dimensions 256 --dry-run
```

Repeat `--part` to preserve an arbitrary text/media order. Convenient `--text`, `--image`,
`--audio`, and `--video` flags build text → images → audio → video. Use `--request-json`
for multi-item batches or a prebuilt body.

## Exact limits

| Limit | Value |
|---|---:|
| Encoded JSON body | 24 MiB |
| Top-level items | 1-16 |
| Parts per item | 1-16 |
| Images | Up to 8 per item; JPEG/PNG/WebP; 8 MiB each; 8 MiB total image bytes per item; 16 MP each |
| Audio | One per item; WAV/FLAC/MP3; 8 MiB; 30 seconds |
| Video | One per item; MP4; 16 MiB; 32 seconds; sampled at up to 1 fps and 32 frames |
| Decoded media | 20 MiB per request |
| Aggregate UTF-8 text | 10 MiB |
| Processed context | 8,192 tokens per item, including retrieval prefix, 12 template tokens, and media expansion |

The runtime verifies magic bytes, image shape, audio/video duration, bounded decoded work,
processor usage, output dimensions, finite floats, ordering, and unit normalization.

## Response and billing

The response is OpenAI-shaped:

```json
{
  "object": "list",
  "data": [
    { "object": "embedding", "index": 0, "embedding": [0.014, -0.031] }
  ],
  "model": "embeddinggemma-2",
  "usage": {
    "prompt_tokens": 313,
    "total_tokens": 313,
    "cost_usd": 0.000001,
    "breakdown": { "text": 32, "image": 256, "audio": 25, "video": 0 }
  },
  "processor_revision": "30f177f03cbcb42bc2f65496458de79f51b80c28",
  "embedding_protocol": "embedding-multimodal-v1"
}
```

Vectors are returned in top-level input order and are normalized again after 768/512/256/128
Matryoshka truncation. Billing is input only at the catalog input-token rate. The Grid validates
vectors and actual processor usage before debiting credits or settling x402.

When an x402 capture succeeds but its durable accounting finalizer still needs recovery, the
successful response also contains `"billing_pending":true` and a `job_id`. Do not resubmit that
paid request. The idempotent billing outbox completes the operator/platform split by job id.

## Privacy and retention

The orchestrator seals the complete ordered input and explicit effective `input_type` to the
selected node with negotiated v2/base64 X25519 transport. There is no plaintext media fallback.
The job row temporarily persists that **encrypted envelope**, not plaintext media. Node results
are also persisted as encrypted envelopes.

After a job becomes terminal, `input_payload` becomes eligible for deletion at **30 minutes**
and `encrypted_result` at **one hour**. The purge runs hourly, so the practical upper bounds are
about **90 minutes** for input and **two hours** for results.

Node failure text can contain prompts, media, paths, or tracebacks. Node-supplied failure text is
classified transiently and persisted only as `embedding_input_invalid`,
`embedding_context_overflow`, or `embedding_runtime_failed`. Orchestrator-owned validation
paths can store bounded service reasons, but `GET /v1/jobs/{id}` normalizes every EG2 runtime
failure to the same stable public codes.

## Public errors

| HTTP | Type/code | Action |
|---:|---|---|
| 400 | `invalid_request_error` | Fix JSON, MIME/base64/SHA, duration, batch, encoding, or dimensions. |
| 400 | `invalid_request_error / embedding_input_invalid` | Decoded media or supported input shape failed runtime validation. Reduce/fix input. Not charged and no paid failover. |
| 400 | `invalid_request_error / embedding_context_overflow` | Reduce the item. Not charged and no paid failover. |
| 401 | `invalid_api_key` | Replace an invalid or revoked API key. |
| 401 | `invalid_session` | Reconnect the wallet session used with `use_credits:true`. |
| 403 | `insufficient_scope` | Use a key with `grid:write`. |
| 402 | `payment_required` | Complete x402 payment or use credits. |
| 402 | `insufficient_credits` | Top up credits or reduce the request. |
| 402 | `pod_cap_reached` | Raise the pod's daily compute cap or wait for reset. |
| 402 | `payment_error` | Verification or a definitively rejected settlement failed. Follow the message; a definite rejection is not charged. |
| 404 | `model_not_found` | Correct the model id. If the embeddings feature itself is off, the route returns plain `Not found`. |
| 413 | `invalid_request_error` | Encoded JSON exceeds 24 MiB. |
| 500 | `server_error` | Dispatch or billing infrastructure failed. Read the charge/retry statement in the message. |
| 502 | `inference_error` | Node output failed validation. The Grid may fail over; invalid vectors are not returned or billed. |
| 503 | `model_not_available` | Release flag, confidential transport, or an exact capable ready node is unavailable. |
| 503 | `node_not_available` | A claimed node lost the negotiated confidential transport boundary. Not charged; the Grid may fail over. |
| 503 | `server_error` | The payment service is not configured in this environment. Wait for configuration repair. |
| 504 | `timeout` | Timed out and not charged. Credits may fail over once. |

The request endpoint returns client-safe messages. `GET /v1/jobs/{id}` can expose only the
stable stored failure reason: `embedding_input_invalid`, `embedding_context_overflow`, or
`embedding_runtime_failed`. Plaintext node reason text is never persisted.

## Local mode

On a supported Apple Silicon Mac:

1. Open Singularity Node.
2. Choose **Local → Embeddings → EmbeddingGemma 2**.
3. Download the pinned BF16 snapshot.
4. Add/reorder text, images, audio, or video.
5. Choose `query`, `document`, or `unspecified`, then 768/512/256/128 dimensions.
6. Start Local AI and select **Generate embedding**.

The Local runtime binds loopback only after real text/image/audio/video/mixed startup vectors
pass. During the candidate phase, builds need `VITE_EMBEDDINGGEMMA2_ENABLED=true` and the native
runtime needs `SGL_EMBEDDINGGEMMA2_ENABLED=true`. Both values must be the exact lowercase
string `true`. These opt-ins are for release testing and do not enable production Grid traffic.

Local request errors are deliberately bounded:

- `400 {"error":"Invalid embedding input."}` for expected client input failures.
- `413 {"error":"Request body exceeds the limit."}`.
- `503 {"error":"Embedding runtime unavailable."}` for runtime or output-accounting failure;
  readiness is removed.

## Immutable candidate

- Official model: `google/embeddinggemma-2@914f7f89142e33e77833254d9c9b90c3cef7303b`
- Apple BF16 model: `mlx-community/embeddinggemma-2-bf16@1a4ffddb7905d3f63486748deabe091a01fb6201`
- MLX: `0.32.3`
- Transformers: `5.19.0`
- MLX-VLM / processor: `30f177f03cbcb42bc2f65496458de79f51b80c28`

FP16 is rejected. Keep the model, processor, runtime, asset hashes, and startup fixtures pinned
together.
