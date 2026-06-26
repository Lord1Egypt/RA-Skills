# E-commerce Suit Image Generation

Generate professional product images for e-commerce from a single reference image.

## Execution

**IMPORTANT:** Ensure `SHORTART_API_KEY` is set in your environment. After setting it in `~/.zshrc`, restart your terminal or run `source ~/.zshrc`.

**With OSS path:**
```bash
python3 scripts/suit-image/impl.py "<prompt>" --image "images/path/to/image.jpg"
```

**With local file:**
```bash
python3 scripts/suit-image/impl.py "<prompt>" --upload /path/to/local/image.jpg
```

## Workflow

1. **Understand Requirements** — Confirm product and desired output style
2. **Prepare Reference Image** — Determine if user has OSS path or local file
3. **Optimize Prompt** — Create clear description (e.g., "给该手机产品制作亚马逊商品主图")
4. **Submit Task** — Run impl.py, returns `project_id` immediately
5. **Ask User to Wait** — "Task submitted (project_id: xxx). Wait for completion?"
6. **Poll for Completion** (if user agrees):
   ```bash
   python3 scripts/suit-image/impl.py --poll {project_id}
   ```
7. **Handle Result** — Success: ask to download; Timeout/Failed: ask to retry
8. **Download Images** (if user agrees):
   ```bash
   python3 scripts/suit-image/impl.py --download '{json_result}'
   ```
9. **Inform User** — Tell local file paths (e.g., `~/Downloads/shortart_suit_20260317_143022_1.jpg`)

## Polling

Polls every 6 seconds with 5-minute timeout.
