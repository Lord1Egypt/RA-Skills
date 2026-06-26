---
name: "zerocut-cli-tools"
description: "Use ZeroCut CLI media and document tools. Invoke when user needs generate media, run ffmpeg/pandoc, sync resources, or save outputs."
---

# ZeroCut CLI Tools

## Purpose

This skill provides a single reference for using ZeroCut CLI commands:
- image generation
- video generation
- music generation
- text-to-speech
- ffmpeg sandbox execution
- pandoc sandbox execution

## When To Invoke

Invoke this skill when the user asks to:
- generate image, video, music, or speech audio
- run ffmpeg or ffprobe command in sandbox
- run pandoc conversion in sandbox
- sync local/remote resources into sandbox
- save generated results to local output files

## Command Reference

### image

Default action: `create`

```bash
zerocut image --prompt "a cat on a bike" --output out.png
zerocut image create --prompt "a cat on a bike" --model seedream-5l --aspectRatio 1:1 --resolution 1K --refs ref1.png,ref2.jpg --output out.png
```

Options:
- `--prompt <prompt>` required
- `--model <model>`
- `--aspectRatio <ratio>`
- `--resolution <resolution>`
- `--refs <refs>` comma-separated local paths or URLs
- `--output <file>` save generated file

### video

Default action: `create`

```bash
zerocut video --prompt "city night drive" --video vidu --duration 8 --output out.mp4
zerocut video create --prompt "city night drive" --video vidu --aspectRatio 1:1 --refs ref1.png,ref2.png --output out.mp4
```

Options:
- `--prompt <prompt>` required
- `--video <model>`
- `--duration <seconds>`
- `--seed <seed>`
- `--firstFrame <image>`
- `--lastFrame <image>`
- `--refs <assets>`
- `--resolution <resolution>`
- `--aspectRatio <ratio>`
- `--withAudio`
- `--optimizeCameraMotion`
- `--output <file>`

### music

Default action: `create`

```bash
zerocut music --prompt "lofi beat" --output music.mp3
zerocut music create --prompt "lofi beat" --output music.mp3
```

Options:
- `--prompt <prompt>` required
- `--output <file>`

### tts

Default action: `create`

```bash
zerocut tts --text "你好，欢迎使用 ZeroCut" --voiceId voice_xxx --output speech.mp3
zerocut tts create --prompt "calm tone" --text "Hello world" --voiceId voice_xxx --output speech.mp3
```

Options:
- `--prompt <prompt>`
- `--text <text>` required
- `--voiceId <voiceId>`
- `--output <file>`

### ffmpeg

```bash
zerocut ffmpeg --args -i input.mp4 -vn output.mp3 --resources input.mp4
zerocut ffmpeg --args -i input.mp4 -vf scale=1280:720 output.mp4 --resources input.mp4
```

Options:
- `--args <args...>` required, arguments appended after `ffmpeg`
- `--resources <resources...>` optional, files/URLs to sync into sandbox materials

Behavior:
- command is validated to only allow `ffmpeg` or `ffprobe`
- for `ffmpeg`, `-y` is auto-injected when absent
- output file is auto-downloaded from sandbox to local current directory

### pandoc

```bash
zerocut pandoc --args input.md -o output.pdf --resources input.md
zerocut pandoc --args input.md --output=output.docx --resources input.md template.docx
```

Options:
- `--args <args...>` required, arguments appended after `pandoc`
- `--resources <resources...>` optional, files/URLs to sync into sandbox materials

Behavior:
- command is validated to only allow `pandoc`
- output file must be specified in args with `-o`, `--output`, or `--output=...`
- output file is auto-downloaded from sandbox to local current directory

## Output And Sync Rules

- Media URLs from generation are synced to TOS when available.
- `--output` saves files to an absolute path resolved from current working directory.
- Missing parent directories for `--output` are created automatically.
