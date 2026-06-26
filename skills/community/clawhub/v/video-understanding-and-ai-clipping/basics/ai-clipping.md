# AI Clipping Task Basics

The **AI Clipping** task identifies the most engaging moments in a video and extracts them as separate clips.

## Usage
`wayinvideo submit clip --url "<url_or_id>" [options]`

*Note: For no-install method, use `PYTHONPATH=<ABS_PATH_TO_SKILL>/wayinvideo-cli python3 -m wayinvideo submit ...`.*

## Options
- `--url <url_or_id>`: (Required) Video URL or identity token.
- `--target <lang>`: Target language code for output content. See `references/supported_languages.md`. Auto-detected if omitted.
- `--duration <duration>`: Expected duration range for each clip. Values: `DURATION_0_30` (0-30s), `DURATION_0_90` (0-90s) (default), `DURATION_30_60` (30-60s), `DURATION_60_90` (60-90s), `DURATION_90_180` (90-180s), `DURATION_180_300` (180-300s).
- `--no-export`: Disable video rendering.
- `--top-k <int>`: The best K clips to export. Defaults to `10`. Pass `-1` for all clips. (Requires export enabled)
- `--ratio <ratio>`: Aspect ratio for export: `RATIO_16_9`, `RATIO_1_1`, `RATIO_4_5`, `RATIO_9_16` (default). AI reframing is automatically enabled. (Requires export enabled)
- `--resolution <res>`: Output resolution: `SD_480`, `HD_720`, `FHD_1080` (default), `QHD_2K`, `UHD_4K`. (Requires export enabled)
- `--caption-display <mode>`: Caption mode: `none`, `both`, `original`, `translation`. Defaults to `original` (or `translation` if `--target` is provided). (Requires export enabled)
- `--cc-style-tpl <id>`: Caption style template ID. Defaults to `temp-static-2` if `--caption-display` is `both`, otherwise `word-focus`. See `references/caption_style.md`. (Requires export enabled and `--caption-display`)
- `--no-ai-hook`: Disable automatically generated, attention-grabbing text hooks. (Requires export enabled)
- `--ai-hook-style <style>`: Style of the generated hook text. Values: `serious` (default), `casual`, `informative`, `conversational`, `humorous`, `parody`, `inspirational`, `dramatic`, `empathetic`, `persuasive`, `neutral`, `excited`, `calm`. (Requires export and AI hook enabled)
- `--ai-hook-pos <pos>`: Position of the generated hook text in the video. Values: `beginning` (default), `end`. (Requires export and AI hook enabled)
- `--save-dir <path>`: Directory for result JSON file. Defaults to `~/.wayinvideo/cache` (or the value in your config). Do not specify unless requested.

## Best Practices
- **Subtitles Language**: To include subtitles in a specific language, use `--caption-display translation --target <lang>`.
- **Dual Subtitles**: If `--caption-display` is `both`, you MUST use a template ID starting with `temp-static-`.
- **Platform Mapping**: For social media, consult `references/platform_duration.md` and `references/platform_ratio.md` to pick the correct `--duration` and `--ratio`.
- **Duration Constraints**: If the user specifies the lower or upper bound of clip duration, choose an appropriate `--duration` value (e.g., if user wants "over 1 minute", use `DURATION_60_90` or `DURATION_90_180`).
