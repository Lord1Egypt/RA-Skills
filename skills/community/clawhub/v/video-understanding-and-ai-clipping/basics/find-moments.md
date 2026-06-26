# Find Video Moments Basics

The **Find Video Moments** task searches for specific scenes or topics in a video using a natural language query.

## Usage
`wayinvideo submit search --url "<url_or_id>" --query "<text>" [options]`

*Note: For no-install method, use `PYTHONPATH=<ABS_PATH_TO_SKILL>/wayinvideo-cli python3 -m wayinvideo submit ...`.*

## Options
- `--url <url_or_id>`: (Required) Video URL or identity token.
- `--query <text>`: (Required) Natural language search query. Keep it brief and self-contained.
- `--target <lang>`: Target language code. See `references/supported_languages.md`. Auto-detected if omitted.
- `--no-export`: Disable video rendering.
- `--top-k <int>`: The best K moments to return. Defaults to `10`. Pass `-1` for all matches. (Requires export enabled)
- `--ratio <ratio>`: Aspect ratio for export: `RATIO_16_9`, `RATIO_1_1`, `RATIO_4_5`, `RATIO_9_16` (default). AI reframing is automatically enabled. (Requires export enabled)
- `--resolution <res>`: Output resolution: `SD_480`, `HD_720`, `FHD_1080` (default), `QHD_2K`, `UHD_4K`. (Requires export enabled)
- `--caption-display <mode>`: Caption mode: `none`, `both`, `original` (default), `translation`. (Requires export enabled)
- `--cc-style-tpl <id>`: Caption style template ID. Defaults to `temp-static-2` if `--caption-display` is `both`, otherwise `word-focus`. See `references/caption_style.md`. (Requires export enabled and `--caption-display`)
- `--save-dir <path>`: Directory for result JSON file. Defaults to `~/.wayinvideo/cache` (or the value in your config). Do not specify unless requested.

## Best Practices
- **Query Strategy**: Keep queries brief and self-contained; English is preferred for better matching.
- **Subtitles Language**: To include subtitles in a specific language, use `--caption-display translation --target <lang>`.
- **Dual Subtitles**: If `--caption-display` is `both`, you MUST use a template ID starting with `temp-static-`.
- **Platform Mapping**: Consult `references/platform_ratio.md` for the best `--ratio` for your target platform.
