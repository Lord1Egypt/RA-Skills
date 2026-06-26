# Reference Board

Search for reference images and build a mood/reference board on canvas.

**Trigger keywords:** "find references", "build a moodboard", "search for ... and organize"

## Steps

1. **Workspace** — `list_workspaces` → pick or create one with `create_workspace`
2. **Search** — `search_images(query=...)` — split broad queries into multiple searches and merge results
3. **Check canvas** — `get_canvas(canvas_id=...)` → find an empty area to avoid overlapping existing elements; use it as `start_x, start_y`
4. **Add title** — `create_element(element_type="text", text="Reference Board: <keyword>", position_x=start_x, position_y=start_y, fontSize=32)`
5. **Upload in grid** — For top N results (default 9). Use `size_w=512, size_h=512` by default, or adjust if a specific aspect ratio is desired:
   ```
   cols = 3, gap = 20
   size_w = 512, size_h = 512
   for i, img in enumerate(results[:9]):
       x = start_x + (i % cols) * (size_w + gap)
       y = start_y + 150 + (i // cols) * (size_h + gap)
       upload_image(image_url=img.url, space_id=..., canvas_id=..., position_x=x, position_y=y, size_width=size_w, size_height=size_h)
   ```
6. **Connect** — `create_edge` from title to first image
7. **Group** — `create_group(element_ids=[title_id, ...image_ids])`

## Output

Report: keyword, images found, images placed, grid layout.
