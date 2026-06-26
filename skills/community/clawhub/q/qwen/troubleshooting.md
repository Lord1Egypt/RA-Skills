# Qwen Troubleshooting

## 401, 403, or Empty Model List

Symptoms:
- hosted requests fail immediately
- `/models` returns auth errors or nothing useful

Checks:
1. Confirm the correct `DASHSCOPE_API_KEY` is loaded in the current shell.
2. Confirm the region base URL matches the key and enabled deployment mode.
3. Re-run the minimal `/models` request before changing any prompt logic.

## Model Not Found or Stale ID

Symptoms:
- request shape is fine but the model is rejected

Checks:
1. Fetch the live `/models` list from the current surface.
2. Replace copied IDs with the exact live name.
3. Remove saved defaults that include dated or region-specific suffixes no longer available.

## Local Qwen Is Too Slow

Symptoms:
- laptop gets hot
- first token is slow
- long prompts degrade sharply

Checks:
1. Reduce model size before changing prompts.
2. Shrink context length to a realistic value.
3. Re-check quantization choice and available unified memory.
4. Compare one short prompt against one long prompt to isolate context pressure.

## JSON or Tool Calls Drift

Symptoms:
- prose appears where JSON is expected
- tool name or arguments are malformed

Checks:
1. Force a strict schema and `temperature: 0`.
2. Separate reasoning from structured output into two passes.
3. Validate parser assumptions for the exact backend.
4. Fail closed instead of executing guessed arguments.

## Migration From Another OpenAI-Compatible Backend Breaks

Symptoms:
- same client works elsewhere but fails on Qwen
- stop tokens, tool calls, or reasoning traces differ

Checks:
1. Compare one minimal payload on both providers.
2. Check model family, not just endpoint shape.
3. Inspect chat template, parser mode, and streaming expectations separately.
4. Only after the minimal repro is stable should application prompts be tuned.

## Vision or Multimodal Route Fails

Symptoms:
- image requests are rejected
- text-only behavior works but image input does not

Checks:
1. Confirm the model list exposes a vision-capable route.
2. Verify the payload format expected by the current surface.
3. Test with one small image and one short question before larger workflows.

## Good Final Question

When debugging stalls, ask:

"What is the smallest request that should work right now?"

If that request is not stable, the problem is still infrastructure or route selection, not prompt sophistication.
