---
name: video-frame-extractor
description: This skill should be used when extracting frames from video files, such as generating keyframe sequences from videos, creating video thumbnails at intervals, or preparing video frames for analysis. Triggers include requests like "extract frames from video", "sample frames every N seconds", "extract keyframes for video analysis", or "generate video thumbnail sequence".
---

# Video Frame Extractor

## Overview

This skill guides LLM agents to extract frames from video files using FFmpeg. It provides complete workflow for frame extraction including environment setup, parameter configuration, and command execution.

**Primary method: FFmpeg** (fast and reliable)  
**Fallback method: OpenCV** (if FFmpeg unavailable)

## Workflow

### Step 1: Verify FFmpeg Installation

Before extracting frames, check if FFmpeg is installed:

```bash
ffmpeg -version
```

If FFmpeg is not installed, see **FFmpeg Installation** section below.

### Step 2: Determine Extraction Parameters

Before extracting frames, the LLM MUST confirm these parameters with the user:

| Parameter | Description | Example |
|-----------|-------------|---------|
| **output_path** | Directory to save extracted frames | Default: `./tmp/frames` |
| **frame_rate** | Frames per second to extract | `0.25` (1 frame every 4 seconds) |
| **scale** | Short side resize target in pixels (optional) | `640` (short side → 640px) |

**Parameter Calculation Guide:**
- To extract 1 frame every X seconds: `frame_rate = 1/X`
- Example: 1 frame every 4 seconds → `frame_rate = 0.25`
- Example: 1 frame every 10 seconds → `frame_rate = 0.1`
- Example: 1 frame per second → `frame_rate = 1`

### Step 3: Execute FFmpeg Command

Generate and execute the FFmpeg command:

**Basic Command (no resize):**
```bash
ffmpeg -hide_banner -loglevel error -i "{video_path}" -vf "fps={frame_rate}" -fps_mode vfr -q:v 2 -f image2 "{output_path}/%06d.jpg"
```

**With Short Side Resize (recommended for analysis):**
```bash
ffmpeg -hide_banner -loglevel error -thread_queue_size 512 -i "{video_path}" -vf "fps={frame_rate},scale='if(gt(iw,ih),-2,{scale}):if(gt(iw,ih),{scale},-2)':flags=lanczos" -fps_mode vfr -q:v 2 -f image2 -atomic_writing 1 "{output_path}/%06d.jpg"
```

**Parameter Breakdown:**
| Flag | Purpose |
|------|---------|
| `-hide_banner` | Suppress build info |
| `-loglevel error` | Quiet mode, show only errors |
| `-thread_queue_size 512` | Increase thread queue for large files |
| `-vf "fps={rate}"` | Set frame extraction rate |
| `-fps_mode vfr` | Variable frame rate (skip duplicates) |
| `-q:v 2` | JPEG quality (1-31, lower = better) |
| `-atomic_writing 1` | Atomic file write (prevent corruption) |
| `%06d.jpg` | Sequential naming: 000001.jpg, 000002.jpg... |

### Step 4: Verify Output

After extraction, verify the output:
- Count frames: `ls {output_path}/*.jpg | wc -l`
- Check frame sizes: `ls -lh {output_path}/*.jpg | head -5`

## FFmpeg Installation

### Windows

**Option 1: winget (Recommended)**
```powershell
winget install ffmpeg
```

**Option 2: Chocolatey**
```powershell
choco install ffmpeg
```

**Option 3: Manual Download**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to a permanent location (e.g., `C:\tools\ffmpeg`)
3. Add to PATH: `setx PATH "$PATH;C:\tools\ffmpeg\bin`
4. Restart terminal

**Verify Installation:**
```powershell
ffmpeg -version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
```

### Linux (CentOS/RHEL/Fedora)

```bash
sudo dnf install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

## Common Use Cases

### Extract 1 frame every 4 seconds, resize to 640px
```
frame_rate = 0.25
scale = 640
```

### Extract 1 frame every 10 seconds, original size
```
frame_rate = 0.1
scale = 0 (no resize)
```

### Extract 1 frame per second for a 10-minute video (600 frames)
```
frame_rate = 1
video_duration = 600 seconds
expected_frames = 600
```

## Output Directory Structure

Frames are saved with sequential naming:
```
output_path/
├── 000001.jpg
├── 000002.jpg
├── 000003.jpg
└── ...
```

The sequential naming (`%06d`) ensures frames are in temporal order regardless of original frame numbers.

## Error Handling

| Error | Solution |
|-------|----------|
| `ffmpeg: command not found` | Install FFmpeg first |
| `No such file or directory` | Check video_path is correct |
| `Permission denied` | Check write permissions for output_path |
| `Output directory not empty` | Clear or use different output path |

## Notes

- FFmpeg is **much faster** than OpenCV for frame extraction (10-100x)
- The scale filter uses `-2` instead of `-1` to ensure dimensions are divisible by 2 (better codec compatibility)
- `-fps_mode vfr` (variable frame rate) skips duplicate frames when seeking
- Use `-q:v 2` for high quality JPEG (range 1-31, default 31)
