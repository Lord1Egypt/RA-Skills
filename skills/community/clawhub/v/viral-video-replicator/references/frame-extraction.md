# FFmpeg Frame Extraction

> **Role:** Defines FFmpeg commands and parameters for video frame extraction and audio extraction.
> Load at: Step 2 (extracting frames and audio).
> It does NOT replace execution — these are command specs to be executed, not cached results.

## check_ffmpeg()

Verifies ffmpeg and ffprobe availability. Returns dict with version info.

## extract_frame_grids()

### Parameters
- video_path: str
- fps: 3.0 (frames per second)
- grid_cols: 4
- grid_rows: 3
- max_grids: 3
- thumb_w: 360
- thumb_h: 640

### Pipeline
1. Get video duration via ffprobe
2. FFmpeg extraction with filter chain:
   ```
   fps=3,scale=360:640:force_original_aspect_ratio=decrease:flags=lanczos,
   pad=360:640:(ow-iw)/2:(oh-ih)/2:color=black
   ```
3. Output: JPEG frames at quality 5, VFR mode
4. Cap total frames: 4 * 3 * 3 = 36 max

### Grid Stitching
- PIL Image.new(RGB, 1440x1920, black)
- Paste each frame at (col * 360, row * 640)
- Draw timestamp label: yellow text on black rect at (x+6, y+6)
- Save as JPEG quality=85, encode base64

### Output
- list[str]: base64-encoded JPEG grid images
- float: video duration in seconds
- int: total frame count

### Example
10s video at 3fps = ~30 frames = 3 grids of 12 frames each

## extract_audio()

### Pipeline
1. FFmpeg: `-vn -acodec pcm_s16le -ar 16000 -ac 1`
2. Output: 16kHz mono WAV bytes
3. Returns None if no audio or < 5000 bytes (silence)
