# Video Export Task Basics

The **Export** task allows you to render or re-render clips from an existing **AI Clipping** or **Find Moments** task. Use this to change aspect ratio, resolution, caption style, or add AI hooks to previously generated clips.

## Usage
`wayinvideo submit export --id "<original_id>" [options]`

*Note: For no-install method, use `PYTHONPATH=<ABS_PATH_TO_SKILL>/wayinvideo-cli python3 -m wayinvideo submit ...`.*

## Options
- `--id <id>`: (Required) The original task ID returned by a `clip` or `search` task.
- `--clip-indices <list>`: Comma-separated indices of clips to export (e.g., `0,2,5`). If omitted, all clips in the project are exported.
- `--target <lang>`: Target language code for output content and subtitles. See `references/supported_languages.md`. Defaults to the source task's language.
- `--ratio <ratio>`: Aspect ratio for export: `RATIO_16_9`, `RATIO_1_1`, `RATIO_4_5`, `RATIO_9_16` (default). AI reframing is automatically enabled.
- `--resolution <res>`: Output resolution: `SD_480`, `HD_720`, `FHD_1080` (default), `QHD_2K`, `UHD_4K`.
- `--caption-display <mode>`: Caption mode: `none`, `both`, `original`, `translation`. Defaults to `original` (or `translation` if `--target` is provided).
- `--cc-style-tpl <id>`: Caption style template ID. See `references/caption_style.md`. Defaults to `temp-static-2` if `--caption-display` is `both`, otherwise `word-focus`.
- `--ai-hook`: Enable automatically generated, attention-grabbing text hooks.
- `--no-ai-hook`: Disable automatically generated text hooks.
- `--ai-hook-style <style>`: Style of the generated hook text (e.g., `serious`, `humorous`, `dramatic`). (Requires AI hook enabled)
- `--ai-hook-pos <pos>`: Position of the generated hook text: `beginning` (default), `end`. (Requires AI hook enabled)
- `--ai-hook-keywords <text>`: Optional keywords to steer the generated AI hook text. (Requires AI hook enabled)
- `--ai-hook-text-duration <ms>`: Duration of the AI hook text overlay in milliseconds. (Requires AI hook enabled)
- `--save-dir <path>`: Directory for result JSON file.
