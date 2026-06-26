# vn-tools-cli Reference (Windows)

Full command reference for VN Tools CLI on Windows.

Typical install locations (searched in order):
- `%LOCALAPPDATA%\Programs\*\CLI\bin\vn-tools-cli.exe`
- `%LOCALAPPDATA%\*\CLI\bin\vn-tools-cli.exe`
- `%ProgramFiles%\*\CLI\bin\vn-tools-cli.exe`

## Common options

All commands accept:

- `-o`, `--output <dir>` — output directory (default: current directory)

All file paths must be **absolute Windows paths**. Quote paths containing spaces.

---

## extract-audio

Export the audio stream from a video file.

```
vn-tools-cli extract-audio <video-path> [-o <dir>] [-f <format>]
```

- `-f`, `--format <fmt>` — `mp3`, `aac`, `wav` (re-encodes to the specified format)

Without `-f`, the audio track is stream-copied without re-encoding. Stream copy auto-detects the output extension from the source codec (aac, mp3, opus, ogg, etc.).

---

## extract-frame

Save a single frame from a video as an image.

```
vn-tools-cli extract-frame <video-path> [-o <dir>] [-p <pos>] [-t <seconds>] [-f <fmt>] [--max-size <pixels>]
```

- `-p`, `--position <pos>` — `first` (default), `last`, `custom`
- `-t`, `--time <seconds>` — required when position is `custom`
- `-f`, `--format <fmt>` — `png` (default), `jpeg`
- `--max-size <pixels>` — max dimension in pixels; `0` keeps original size

---

## compress-image

Compress and/or convert an image.

```
vn-tools-cli compress-image <image-path> [-o <dir>] [-f <fmt>] [-q <quality>] [-w <px>] [-h <px>] [--no-keep-aspect-ratio]
```

- `-f`, `--format <fmt>` — `jpeg`, `png`, `webp`, `heic` (default: same as input)
- `-q`, `--quality <0.0-1.0>` — compression quality (default: 0.8); ignored for PNG
- `-w`, `--max-width <px>` — max width
- `-h`, `--max-height <px>` — max height
- `--no-keep-aspect-ratio` — disable aspect-ratio preservation

Constraints: `-q` must be 0.0–1.0.

---

## compress-video

Re-encode a video with optional resolution, frame-rate, bitrate, or HDR.

```
vn-tools-cli compress-video <video-path> [-o <dir>] [-r <resolution>] [--fps <fps>] [-b <kbps>] [--hdr]
```

- `-r`, `--resolution <px>` — target short-edge resolution (e.g. `720`, `1080`, `2160`); minimum 144
- `--fps <fps>` — target frame rate (e.g. `24`, `30`, `60`); range 1-120
- `-b`, `--bitrate <kbps>` — target bitrate in kbps (default: auto); minimum 100
- `--hdr` — enable HDR output (HEVC 10-bit)

---

## add-caption

Burn an existing SRT subtitle file into a video.

```
vn-tools-cli add-caption <video-path> --srt <srt-path> [-o <dir>] [style options]
```

Required:

- `--srt <path>` — path to SRT subtitle file

Style options:

- `--font-family <name>` — font family (default: `Inter`)
- `--font-size <pt>` — font size in points (default: `13`)
- `--text-color <RRGGBB>` — text color as hex (default: `FFFFFF`)
- `--stroke-color <RRGGBB>` — stroke color as hex (default: `000000`)
- `--stroke-width <pt>` — stroke width in points (default: `1.0`)
- `--background-color <RRGGBB>` — subtitle background color (default: none)
- `--opacity <0.0-1.0>` — subtitle opacity (default: `1.0`)

---

## concat-video

Join two or more video clips into a single output. Hard cut only (no transitions).

```
vn-tools-cli concat-video <video1> <video2> [video3 ...] [-o <dir>]
```

---

## auto-captions

Transcribe audio with local Whisper and burn subtitles into the video.

```
vn-tools-cli auto-captions <video-path> [-o <dir>] [-e <engine>] [-l <language>] [-j <threads>] [style options]
```

- `-e`, `--engine <name>` — whisper engine (default: `whisper_base`)
- `-l`, `--language <code>` — source language (default: `auto`)
- `-j`, `--threads <n>` — whisper thread count
- All style options from `add-caption` are also accepted

### Whisper engines

| Engine | Model file | Size | Notes |
|--------|-----------|------|-------|
| `whisper_tiny` | ggml-tiny.bin | ~75 MB | Bundled, no download needed |
| `whisper_base` | ggml-base.bin | ~148 MB | One-time download on first use |
| `whisper_medium_en` | ggml-medium.en-q8_0.bin | ~785 MB | English only, one-time download |
| `whisper_medium` | ggml-medium-q8_0.bin | ~785 MB | Multilingual, one-time download |
| `whisper_turbo` | ggml-large-v3-turbo-q8_0.bin | ~833 MB | Multilingual, one-time download |

### Supported languages

`auto` `en` `zh` `ja` `ko` `es` `pt` `ar` `hi` `id` `fr` `de` `ru` `it` `tr` `vi` `th` `pl` `uk` `nl` `sv` `fi` `ro` `cs` `hu` `he` `el` `bg` `hr` `sk` `sl` `lt` `lv` `et` `ms` `ta` `ur` `sw` `mk` `mi` `is` `hy` `az` `af`

---

## denoise

Remove background noise from audio or video with DeepFilterNet.

```
vn-tools-cli denoise <audio-or-video-path> [-o <dir>] [-l <level>] [-v <value>] [--high-pass] [--audio-only] [--pf]
```

- `-l`, `--level <level>` — `low`, `moderate` (default), `high`, `veryHigh`, `custom`
- `-v`, `--custom-value <int>` — attenuation limit in dB; required when level is `custom`
- `--high-pass` — enable 80Hz high-pass filter
- `--audio-only` — output audio only, even if input is a video
- `--pf`, `--postfilter` — enable DeepFilterNet postfilter for additional clarity

Output behavior:
- Audio input → denoised audio
- Video input → video with denoised audio track
- Video input + `--audio-only` → denoised audio only

---

## cutout-video

Segment the foreground subject from a video and composite over green background.

```
vn-tools-cli cutout-video <video-path> [-o <dir>] [--feather <0-100>] [--expand <-20..20>] [-f <fmt>]
```

- `--feather <0-100>` — edge softness/blur on matte (default: 0)
- `--expand <-20..20>` — expand (+) or contract (-) matte edge (default: 0)
- `-f`, `--format <fmt>` — output container: `mp4`, `webm`, `mov` (default: same as input)

Constraints: `--feather` 0–100, `--expand` -20 to 20.

Output: subject composited over green background (opaque YUV420P, no alpha channel).

---

## Examples

```powershell
vn-tools-cli extract-audio "C:\Videos\clip.mp4" -o "C:\Output" -f mp3
vn-tools-cli extract-frame "C:\Videos\clip.mp4" -p custom -t 5.5 -f png -o "C:\Output"
vn-tools-cli compress-image "C:\Photos\big.jpg" -q 0.8 -w 1920 -o "C:\Output"
vn-tools-cli compress-video "C:\Videos\raw.mp4" -r 720 -o "C:\Output"
vn-tools-cli add-caption "C:\Videos\clip.mp4" --srt "C:\Subs\clip.srt" --font-size 28 -o "C:\Output"
vn-tools-cli concat-video "C:\Videos\part1.mp4" "C:\Videos\part2.mp4" -o "C:\Output"
vn-tools-cli auto-captions "C:\Videos\interview.mp4" -e whisper_base -l en -o "C:\Output"
vn-tools-cli denoise "C:\Audio\noisy.wav" -l high --pf -o "C:\Output"
vn-tools-cli cutout-video "C:\Videos\person.mp4" --feather 5 -f mp4 -o "C:\Output"
```

---

## Output behavior

- The CLI prints the output file path to stdout on success.
- Output filenames contain a timestamp to prevent overwrites.
- `auto-captions` removes the temporary SRT after burning; it does not return the SRT separately.
- `cutout-video` composites the subject over a green background (opaque YUV420P); no alpha channel.
- `concat-video` is hard cut only — no transition effects.

---

## Requirements

- Windows only
- All processing runs locally, No cloud upload, no API key required
