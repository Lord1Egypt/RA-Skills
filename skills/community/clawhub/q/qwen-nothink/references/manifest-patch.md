# Manifest Patch Reference

Use this reference only when the bundled script cannot be used or must be inspected.

## Why the patch exists

For Qwen thinking models, Ollama may infer thinking behavior from the model config even when the Modelfile has a direct-answer system prompt. A derived no-think tag should therefore patch only its own config blob:

- remove `"thinking"` from `capabilities`
- set `"renderer": ""`
- set `"parser": ""`

Then update the derived tag manifest to point at the new config blob digest and size.

## Local file layout

Default model store:

```text
~/.ollama/models/
├── blobs/
│   └── sha256-...
└── manifests/
    └── registry.ollama.ai/library/MODEL/TAG
```

If `OLLAMA_MODELS` is set, use that directory instead of `~/.ollama/models`.

Short names map like this:

```text
qwen3.6:35b-mlx-nothink
-> manifests/registry.ollama.ai/library/qwen3.6/35b-mlx-nothink
```

Names with registries map like this:

```text
modelscope.cn/namespace/model:tag
-> manifests/modelscope.cn/namespace/model/tag
```

## Manual patch outline

1. Read the target manifest JSON.
2. Locate `manifest["config"]["digest"]`, for example `sha256:abc...`.
3. Read `blobs/sha256-abc...` as JSON.
4. Patch:

   ```json
   {
     "renderer": "",
     "parser": "",
     "capabilities": ["completion", "vision"]
   }
   ```

   Preserve other fields exactly where possible.

5. Serialize compact JSON bytes, compute `sha256`, and write `blobs/sha256-NEW_DIGEST`.
6. Update the target manifest config digest and size.
7. Verify:

   ```bash
   ollama show TARGET_MODEL
   ollama run TARGET_MODEL "用一句话回答：1+1等于几？"
   ```

The final output should not contain `Thinking...`, `<think>`, `</think>`, or reasoning prose.
