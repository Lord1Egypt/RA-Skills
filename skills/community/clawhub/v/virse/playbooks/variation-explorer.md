# Variation Explorer

Compare different models or styles on the same prompt.

**Trigger keywords:** "try different models", "compare", "generate variations", "show me what other models produce"

## Steps

1. **Get original** — `get_element(canvas_id=..., id=...)` → note `artifact_version_id`
2. **Get prompt** — `get_asset_detail(artifact_version_id=...)` → extract original prompt, model, aspect_ratio
3. **Select models** — `list_image_models` → pick 3-4 diverse models (excluding original)
4. **Check balance** — `get_account`
5. **Check canvas** — `get_canvas(canvas_id=...)` → verify there is enough space to the right of the original; if not, pick an open area
6. **Determine element size** — Use the original element's `size_width` / `size_height` from `get_element` to match the original dimensions. If the original has a non-1:1 aspect ratio, use those dimensions for variations too.
7. **Generate row** — Place variations in a horizontal row to the right of the original:
   ```
   size_w = original_size_width   # from get_element
   size_h = original_size_height  # from get_element
   gap = 40
   for i, model in enumerate(models):
       x = original_x + (i + 1) * (size_w + gap)
       y = original_y
       generate_image(prompt=original_prompt, model=model, size_width=size_w, size_height=size_h, aspect_ratio=original_aspect_ratio, ...)
   ```
8. **Add labels** — `create_element(element_type="text", text=model_name, ...)` below each image
9. **Connect** — `create_edge(source=original_id, target=variation_id)` for each
10. **Group** — `create_group(element_ids=[original, ...variations, ...labels])`

## Output

Original info + list of variations with model names and element IDs.
