# vnapp-cli Reference

Full command reference for the VN Video Editor OpenClaw skill.

Expected CLI path:

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli
```

## Global commands

### Show help

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli help
~/.openclaw/tools/vnapp-cli/vnapp-cli --help
~/.openclaw/tools/vnapp-cli/vnapp-cli -h
```

### Show version

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli version
~/.openclaw/tools/vnapp-cli/vnapp-cli --version
```

## Extract audio

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli extract-audio <video-path> [--stream]
```

Options:

- `--stream`: stream progress in real time

## Extract frame

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli extract-frame <video-path> [options] [--stream]
```

Options:

- `--position`, `-p <pos>`: `first` (default), `last`, `custom`
- `--time`, `-t <seconds>`: required when `position=custom`
- `--format`, `-f <fmt>`: `png` (default), `jpeg`
- `--max-size <pixels>`: max dimension in pixels, `0` keeps original size
- `--output`, `-o <dir>`: output directory
- `--stream`: stream progress in real time

## Compress image

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli compress-image <image-path> [options] [--stream]
```

Supported formats:

- `jpeg`
- `png`
- `webp`
- `heic`

Options:

- `--format`, `-f <fmt>`: output format, default is same as input
- `--quality`, `-q <0.0-1.0>`: compression quality, default `0.8`, ignored for PNG
- `--max-width`, `-w <pixels>`: max width
- `--max-height`, `-h <pixels>`: max height
- `--no-keep-aspect-ratio`: disable aspect-ratio preservation
- `--output`, `-o <dir>`: output directory
- `--stream`: stream progress in real time

## Compress video

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli compress-video <video-path> [options] [--stream]
```

Options:

- `--resolution`, `-r <pixels>`: target short-edge resolution, such as `720`, `1080`, `2160`
- `--fps <fps>`: target frame rate, such as `24`, `30`, `60`
- `--bitrate`, `-b <kbps>`: target bitrate in kbps, default auto
- `--hdr`: enable HDR output
- `--keep-draft`: keep the temporary VN draft after export
- `--output`, `-o <dir>`: output directory
- `--stream`: stream progress in real time

## Concatenate videos

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli concat-video <video1> <video2> [video3 ...] [options] [--stream]
```

Options:

- `--style`, `-s <name>`: transition style
- `--duration`, `-d <seconds>`: transition duration, `0.2` to `5.0`
- `--keep-draft`: keep the temporary VN draft after export
- `--output`, `-o <dir>`: output directory
- `--stream`: stream progress in real time

Basic transition styles:

- `none`
- `fade_black`
- `fade_white`
- `dissolve`
- `color_difference_dissolve`
- `blur`
- `pixelate`
- `zoom_blur`
- `zoom_blur_reverse`
- `rotate_zoom`
- `rotate_zoom_reverse`
- `rotate_blur`
- `rotate_blur_reverse`
- `spin`
- `spin_reverse`
- `circle_crop_center`
- `circle_crop_center_reverse`
- `slide_from_top`
- `slide_from_left`
- `slide_from_bottom`
- `slide_from_right`
- `wipe_from_top`
- `wipe_from_left`
- `wipe_from_bottom`
- `wipe_from_right`
- `push_from_top`
- `push_from_left`
- `push_from_bottom`
- `push_from_right`
- `reveal_vertical`
- `reveal_horizontal`
- `blink`
- `floodlight`
- `shake_from_top_left`
- `shake_from_bottom_left`
- `shake_from_bottom_right`
- `shake_from_top_right`
- `shake_from_top`
- `shake_from_left`
- `shake_from_bottom`
- `shake_from_right`

Matte transition styles:

- `circle_1`
- `circle_2`
- `square_1`
- `square_2`
- `square_3`
- `line_1`
- `line_2`
- `line_3`
- `ink_1`
- `ink_2`
- `paint_1`
- `paint_2`
- `zebra`
- `hexagon`
- `swirl`
- `memory`
- `sea`
- `glitch`
- `lens`

## Auto captions

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli auto-captions <video-path> [options] [--stream]
```

Options:

- `--engine`, `-e <type>`: `whisper_turbo` (default), `whisper_medium`, `whisper_base`, `whisper_tiny`
- `--language`, `-l <code>`: source language, default `auto`
- `--font-family <name>`: font family, default `Inter`
- `--font-size <pt>`: font size, default `37.4`
- `--text-color <hex>`: text color, default `#FFFFFF`
- `--stroke-color <hex>`: stroke color, default `#000000`
- `--stroke-width <pt>`: stroke width, default `0.5`
- `--keep-draft`: keep the temporary VN draft after export
- `--stream`: stream progress in real time

Notes:

- `whisper_turbo` and `whisper_medium` may download models on first use
- `whisper_base` and `whisper_tiny` are built in

## Add SRT subtitles

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli add-caption <video-path> --srt <srt-path> [options] [--stream]
```

Options:

- `--srt <path>`: required SRT path
- `--font-family <name>`: font family, default `Inter`
- `--font-size <pt>`: font size, default `13`
- `--text-color <hex>`: text color, default `#FFFFFF`
- `--stroke-color <hex>`: stroke color, default `#000000`
- `--stroke-width <pt>`: stroke width, default `0.5`
- `--background-color <hex>`: optional subtitle background color
- `--opacity <0.0-1.0>`: subtitle opacity, default `1.0`
- `--keep-draft`: keep the temporary VN draft after export
- `--output`, `-o <dir>`: output directory
- `--stream`: stream progress in real time

## Denoise audio or video

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli denoise <audio-or-video-path> [options] [--stream]
```

Options:

- `--level`, `-l <level>`: `low`, `moderate` (default), `high`, `veryHigh`, `custom`
- `--custom-value`, `-v <int>`: required when `level=custom`
- `--high-pass`: enable high-pass filter
- `--audio-only`: output denoised audio only even if input is video
- `--output`, `-o <dir>`: output directory
- `--stream`: stream progress in real time

Output behavior:

- audio input -> denoised audio
- video input -> video with denoised audio track
- video input + `--audio-only` -> denoised audio only

## Query job status

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli get-status <job-id>
```

## Cancel job

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli cancel <job-id>
```

## Common examples

```bash
~/.openclaw/tools/vnapp-cli/vnapp-cli extract-frame "/path/video.mp4" -p custom -t 5.5 --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli compress-image "/path/photo.jpg" -f webp -q 0.8 --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli compress-video "/path/video.mp4" -r 1080 --fps 30 -b 8000 --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli concat-video "/path/a.mp4" "/path/b.mp4" -s dissolve -d 1.0 --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli auto-captions "/path/video.mp4" -e whisper_medium -l en --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli add-caption "/path/video.mp4" --srt "/path/subtitles.srt" --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli denoise "/path/video.mp4" -l high --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli denoise "/path/video.mp4" --audio-only --stream
~/.openclaw/tools/vnapp-cli/vnapp-cli get-status job-abc123
~/.openclaw/tools/vnapp-cli/vnapp-cli cancel job-abc123
```

## JSON output format

The CLI emits JSON lines.

Typical message types:

- `discovering`
- `connected`
- `copying`
- `file-copied`
- `started`
- `progress`
- `completed`
- `error`
- `status`

Treat `completed` with `outputPath` as success.

## Requirements

- VN Video Editor must be installed
- VN MCP Server must be active in VN
- macOS only
- Minimum VN version: `0.22 (654)`
