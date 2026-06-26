---
name: text-to-image
description: Render text into an image and return a temporary local image file path, with optional data URI. Use when Clawhub or Codex needs to convert plain text, styled text, colored text, multilingual text, slogans, posters, captions, or text snippets into an image with controllable width, height, format, font size, full-text color, or partial text colors. Support svg, png, jpg, and jpeg output, return a real temp file path under the skill tmp folder, and work across Windows and macOS with built-in font fallback. Also use for 文本转图片、文字转图片、生成文字海报、彩色文字图片、指定尺寸文字图、局部文字颜色、高亮部分文字、输出临时图片地址、返回本地图片路径、返回 image 文件路径、指定 svg/png/jpg 格式、Mac 兼容、Windows 兼容、return temp file path, local image path, or data URI output.
---

# Text to Image

Use `scripts/render_text_image.py` to generate an image and return a local file path. The script can also include a `data:` image URL when needed.

Prefer the script over hand-writing image payloads. The script already handles:

- fixed image width and height
- output format: `svg`, `png`, `jpg`, `jpeg`
- temp file output by default under `tmp/`
- absolute and relative file paths in the response
- file path, file name, and file size in the response
- whole-text color
- partial text colors through friendly highlight fields or raw segments
- explicit font size
- automatic font-size fitting when `font_size` is omitted
- newline-aware wrapping
- transparent or solid backgrounds
- Windows and macOS font fallback

## Input Shape

Pass a JSON spec through `--spec-json` or `--spec-file`.

Supported fields:

```json
{
  "text": "Hello\nWorld",
  "highlight_ranges": [
    { "start": 0, "end": 5, "color": "#111111" },
    { "start": 6, "end": 11, "color": "#ff4d4f" }
  ],
  "highlight_texts": [
    { "match": "World", "color": "#1677ff", "occurrence": "all", "case_sensitive": true }
  ],
  "segments": [
    { "text": "Hello ", "color": "#111111" },
    { "text": "World", "color": "#ff4d4f" }
  ],
  "width": 1200,
  "height": 630,
  "format": "png",
  "font_size": 72,
  "min_font_size": 12,
  "default_color": "#111111",
  "background": "#ffffff",
  "padding": 48,
  "line_height": 1.2,
  "align": "center",
  "valign": "middle",
  "font_family": "Microsoft YaHei, PingFang SC, Arial, sans-serif"
}
```

Rules:

- Provide either `text` or `segments`. If both are present, `segments` wins.
- Prefer `text` + `highlight_texts` for simple "make this word red" requests.
- Use `highlight_ranges` when the caller knows character positions.
- Use `segments` only when the caller already has exact pieces split out.
- Keep `\n` when a hard line break is required.
- Omit `font_size` to make the script auto-fit the whole text inside the image.
- If `font_size` is provided, the script keeps that size and still wraps lines as needed.
- `svg` is the default format.
- Prefer `png` over `jpg` for text-heavy images.
- If `format` is `jpg` or `jpeg`, transparent background is converted to white.

Priority:

1. `segments`
2. `text` + `highlight_ranges` / `highlight_texts`
3. `text` only

Friendly highlight format:

```json
{
  "text": "ClawHub makes text visible",
  "highlight_texts": [
    { "match": "ClawHub", "color": "#1677ff" },
    { "match": "visible", "color": "#fa541c" }
  ]
}
```

Range format:

```json
{
  "text": "Hello World",
  "highlight_ranges": [
    { "start": 6, "end": 11, "color": "#ff4d4f" }
  ]
}
```

## Recommended Workflow

1. Build the JSON spec from the user's request.
2. Run the script.
3. Return `file_path` to the caller when the next step is file upload.
4. Use `image_url` only when the caller explicitly needs a data URI.

Example:

```powershell
@'
{
  "segments": [
    { "text": "Claw", "color": "#111111" },
    { "text": "Hub", "color": "#1677ff" }
  ],
  "width": 1024,
  "height": 512,
  "format": "png",
  "background": "#ffffff",
  "padding": 40
}
'@ | Set-Content spec.json

python scripts/render_text_image.py --spec-file spec.json --no-data-url
```

## Output Contract

The script prints JSON:

```json
{
  "file_path": "E:\\clawhub\\text-to-image\\tmp\\rendered-0000.png",
  "relative_file_path": "tmp/rendered-0000.png",
  "file_name": "rendered-0000.png",
  "file_size": 21550,
  "mime_type": "image/png",
  "format": "png",
  "width": 1024,
  "height": 512,
  "font_size": 96.0,
  "line_count": 1,
  "resolved_segments": [
    { "text": "Claw", "color": "#111111" },
    { "text": "Hub", "color": "#1677ff" }
  ]
}
```

## Notes

- `svg` is lightweight, crisp, and ideal for text rendering.
- `png` is the best general-purpose bitmap choice for text images.
- `jpg` is supported for compatibility, but it is usually not the best default for text.
- Auto-fit uses width-aware wrapping and a font-size search; it is approximate but reliable for mixed Chinese and Latin text.
- The script writes files to the skill's own `tmp/` folder by default.
- Pass `--output path.ext` to control where the file is written.
- Pass `--no-data-url` when the caller only needs upload-ready file metadata.
- On macOS the script tries system fonts such as `PingFang` and `STHeiti` before falling back.
- On Windows the script tries fonts such as `Microsoft YaHei`, `SimHei`, and `Arial`.
- Reusable sample specs live in `testcases/`, including `13-wrap-example.json` for fixed-size wrapping.
