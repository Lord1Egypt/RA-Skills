# Text-to-Image Generation

Generate images from text descriptions or reference images using ShortArt AI.

## Parameters

| Parameter | Options | Default |
|------|------|------|
| `--model` | `seedream4.5` \| `nano-banana-pro` \| `nano-banana-2` | `nano-banana-pro` |
| `--count` | 1-4 | 1 |
| `--resolution` | `1k` \| `2k` \| `4k` (nano-banana-2 also supports `0.5k`) | `2k` |
| `--aspect-ratio` | `1:1` \| `16:9` \| `9:16` | `1:1` |

## Execution

**IMPORTANT:** Ensure `SHORTART_API_KEY` is set in your environment. After setting it in `~/.zshrc`, restart your terminal or run `source ~/.zshrc`.

**Text-to-image:**
```bash
python3 scripts/text-to-image/impl.py "<prompt>" \
  --model {model} \
  --count {count} \
  --resolution {resolution} \
  --aspect-ratio {aspect-ratio}
```

**Image-to-image (with reference):**
```bash
# Use existing OSS path
python3 scripts/text-to-image/impl.py "<prompt>" --image "images/20260121/.../filename.jpg"

# Upload local image
python3 scripts/text-to-image/impl.py "<prompt>" --upload /path/to/local/image.jpg
```

## Workflow

1. **Understand Requirements** — Confirm subject, style, dimensions, quantity
2. **Optimize Prompt** — Refer to [prompt-guide.md](prompt-guide.md) to expand description
3. **Select Parameters** — Choose model/resolution/aspect-ratio based on use case
4. **Submit Task** — Run impl.py, returns `project_id` immediately
5. **Ask User to Wait** — "Task submitted (project_id: xxx). Wait for completion?"
6. **Poll for Completion** (if user agrees):
   ```bash
   python3 scripts/text-to-image/impl.py --poll {project_id} --model {model} --count {count} --resolution {resolution}
   ```
7. **Handle Result** — Success: ask to download; Timeout/Failed: ask to retry
8. **Download Images** (if user agrees):
   ```bash
   python3 scripts/text-to-image/impl.py --download '{json_result}'
   ```
9. **Inform User** — Tell local file paths (e.g., `~/Downloads/shortart_20260315_143022_1.jpg`)

## Polling Times

- **nano-banana-pro**: ~40s, polls every 5-6s
- **nano-banana-2**: ~43s, polls every 6s
- **seedream4.5**: ~74s, polls every 8s
- Timeout: 2-5 minutes
