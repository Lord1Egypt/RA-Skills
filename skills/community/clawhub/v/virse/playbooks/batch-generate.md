# Batch Generate

Generate multiple images and arrange them on a canvas.

**Trigger keywords:** "generate N images", "batch generate", "create a set of", "lay them out"

## Steps

1. **Get workspace** — `list_workspaces` → save `canvas_id` and `space_id`
2. **Choose model** — `list_image_models` → let user pick or use default
3. **Check balance** — `get_account` → verify enough credits for N generations
4. **Check canvas** — `get_canvas(canvas_id=...)` → find an empty area to avoid overlapping existing elements
5. **Calculate element size** — Based on the chosen `aspect_ratio`, compute `size_w` and `size_h` (longer side = 512):
   | aspect_ratio | size_w | size_h |
   |-------------|--------|--------|
   | 1:1 | 512 | 512 |
   | 16:9 | 512 | 288 |
   | 9:16 | 288 | 512 |
   | 4:3 | 512 | 384 |
   | 3:4 | 384 | 512 |
6. **Generate in grid** — Call `generate_image` for each image with grid positions offset to the empty area:
   ```
   cols = min(N, 4)
   gap = 20
   for i in range(N):
       x = start_x + (i % cols) * (size_w + gap)
       y = start_y + (i // cols) * (size_h + gap)
       generate_image(prompt=..., model=..., space_id=..., canvas_id=..., position_x=x, position_y=y, size_width=size_w, size_height=size_h, aspect_ratio=...)
   ```
   Adjust prompts per iteration if user wants different styles.
7. **Group results** — `create_group(element_ids=[...])` to bundle all generated images

## Output

Report: N images generated, layout dimensions, model used, prompt(s).
