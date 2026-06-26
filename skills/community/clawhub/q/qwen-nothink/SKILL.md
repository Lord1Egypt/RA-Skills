---
name: ollama-qwen-nothink
description: Create and verify no-thinking variants of local Qwen/Qwen3-series Ollama models. Use when a user asks to disable thinking, hide or remove think-tag output, make /no_think the default, create a non-thinking tag, or convert a local Qwen Ollama model such as qwen3, qwen3.5, qwen3.6, qwen-vl, or custom Qwen MLX/GGUF tags to answer directly without requiring ollama run --think=false every time.
---

# Ollama Qwen Nothink

## Overview

Create a new Ollama tag that reuses an existing Qwen model's weights but defaults to direct answers. Prefer a reversible derived tag such as `qwen3.6:35b-mlx-nothink`; do not modify or delete the source model.

This skill exists because prompt-only approaches usually fail for Qwen thinking models in Ollama. The reliable path is to combine a no-thinking chat template with a local manifest/config patch that removes thinking renderer metadata from the derived tag.

## Quick Workflow

1. Inspect the source model:
   ```bash
   ollama show SOURCE_MODEL
   ollama show --parameters SOURCE_MODEL
   ollama show --template SOURCE_MODEL
   ```

2. Verify the runtime switch works:
   ```bash
   ollama run --think=false SOURCE_MODEL "用一句话回答：1+1等于几？"
   ```
   If this still emits thinking content, stop and report that the local Ollama/model build does not honor the runtime switch.

3. Create a derived no-thinking tag with the bundled script:
   ```bash
   python3 scripts/create_qwen_nothink_ollama.py SOURCE_MODEL --target TARGET_MODEL
   ```

4. Confirm `ollama show TARGET_MODEL` lists `completion` and, if relevant, `vision`, but not `thinking`.

5. Verify both CLI and API output do not contain `Thinking...`, `<think>`, or reasoning prose:
   ```bash
   ollama run TARGET_MODEL "用一句话回答：1+1等于几？"
   curl -s http://127.0.0.1:11434/api/chat -d '{"model":"TARGET_MODEL","messages":[{"role":"user","content":"用一句话回答：1+1等于几？"}],"stream":false}'
   ```

In Codex sandboxes, local Ollama calls or writes under `~/.ollama` may require user approval. Request escalation plainly when needed.

## Using The Script

Run the script from the skill directory or pass an absolute path:

```bash
python3 /path/to/ollama-qwen-nothink/scripts/create_qwen_nothink_ollama.py qwen3.6:35b-mlx
```

Default target naming appends `-nothink` to the source tag:

```text
qwen3.6:35b-mlx -> qwen3.6:35b-mlx-nothink
qwen3:latest -> qwen3-nothink:latest
```

Useful options:

```bash
python3 scripts/create_qwen_nothink_ollama.py qwen3.6:35b-mlx --target qwen3.6:35b-mlx-nothink
python3 scripts/create_qwen_nothink_ollama.py qwen3.6:35b-mlx --dry-run
python3 scripts/create_qwen_nothink_ollama.py qwen3.6:35b-mlx --skip-verify
python3 scripts/create_qwen_nothink_ollama.py custom-model:latest --allow-non-qwen
```

The script:

- Builds a temporary Modelfile from the source model.
- Preserves existing generation parameters where possible.
- Uses a Qwen chat template that pre-fills an empty `<think></think>` block at the assistant prefix.
- Runs `ollama create` for the derived target.
- Patches only the target manifest/config in the local Ollama model store.
- Removes `thinking` from `capabilities` and clears `renderer`/`parser` so Ollama CLI does not re-enable thinking mode.
- Verifies the target through the local Ollama chat API unless `--skip-verify` is set.

## Tradeoffs

This workflow is optimized for direct text answers. Clearing the thinking-aware renderer/parser can also remove Ollama's automatic `tools` capability for that derived tag, and vision behavior should be verified separately with a real image prompt if the user needs multimodal use. If tool calling or advanced renderer behavior matters more than a default no-think tag, prefer keeping the source model and calling it with `--think=false` or the API equivalent for each request.

## Manual Fallback

If the script cannot run, create a Modelfile like this:

```modelfile
FROM SOURCE_MODEL
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
<think>

</think>

"""
PARAMETER stop "<|im_end|>"
SYSTEM """
你是一个直接回答的助手。
默认关闭思考模式；不要输出思考过程、推理草稿、<think>、thinking 或 reasoning 内容。
直接给出最终答案。
"""
```

Then run:

```bash
ollama create TARGET_MODEL -f Modelfile
```

After creation, patch the target's local config blob as described in `references/manifest-patch.md`. This second step is important; without it, Ollama may still treat the target as a thinking model.

## Safety Rules

- Never edit the source model's manifest or blobs.
- Never use the target name equal to the source name.
- Prefer creating a new tag over overwriting a user's existing no-think tag unless the user asked for that exact tag.
- Keep a copy of the generated Modelfile in the working directory when useful; it documents how the tag was made.
- If verification fails, report the exact failing marker and suggest using `--think=false` at runtime as the reliable fallback.

## Notes

- `PARAMETER think false` is not accepted by many Ollama versions, even though `ollama run --think=false` works.
- `/no_think` in the system prompt often fails because Qwen thinking models may treat it as ordinary text after Ollama has already selected thinking rendering.
- Removing `thinking` from the target config is not enough by itself if `renderer`/`parser` still point to a thinking-aware Qwen renderer.
