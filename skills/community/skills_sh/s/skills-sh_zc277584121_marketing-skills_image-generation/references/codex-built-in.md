# Codex Built-In Image Path

Use this path when the current agent is Codex and the built-in `image_gen` tool is available.

## Selection Rules

- Prefer the built-in tool for normal image generation and image editing.
- Do not ask for `OPENAI_API_KEY` on this path.
- If the user names a destination, generate first, then move or copy the selected output into that destination.
- If the image is meant for the current project, never leave the final asset only in the default Codex image output location.
- If the user explicitly asks for script/API execution, do not use this path; use `scripts/generate_image.py` instead.

## Prompt Shape

Use the same base style as the script unless the user requests a different style:

```text
Use a clean, modern color palette with soft tones.
Minimalist flat illustration style with clear visual hierarchy.
Professional and polished look suitable for technical blog articles.
No photorealistic rendering.
No excessive gradients or shadows.
```

Add the user's actual concept after the style guidance. Keep in-image text short and quote it exactly.

## Output Handling

1. Generate the image with the built-in tool.
2. Inspect the result.
3. If the asset is project-bound, move or copy the final selected image into the workspace.
4. Use a lowercase, hyphenated filename such as `rag-pipeline-overview.png`.
5. Report the final workspace path.
