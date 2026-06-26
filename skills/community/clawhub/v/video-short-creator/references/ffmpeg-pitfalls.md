# FFmpeg on Windows: Pitfalls & Solutions

A reference guide for common FFmpeg issues encountered during video short creation on Windows. These are hard-won lessons from real debugging sessions.

## 1. Never Use drawtext on Windows

**Problem**: `drawtext` filter requires embedding text in a filter string that gets passed through multiple escaping layers (Python string -> shell/cmd.exe -> FFmpeg parser). Line breaks (`\n`) and special characters (`:`, `%`, `'`, `&`) each require different levels of escaping depending on whether you use `os.system()` or `subprocess.run()`.

**Symptoms**:
- Literal `n` characters appearing in subtitles
- Missing or garbled subtitle text
- Silent failures (returncode 0 but no subtitles rendered)

**Solution**: Always use `.srt` file + `subtitles` filter with `subprocess.run()` (list args, no shell):

```python
# WRONG - drawtext with os.system (escaping nightmare)
cmd = f'ffmpeg -y -i "{input}" -vf "drawtext=text=\'{text}\'" "{output}"'
os.system(cmd)

# CORRECT - SRT file with subprocess (no shell escaping)
subprocess.run([
    "ffmpeg", "-y", "-i", input_path,
    "-vf", f"subtitles='{srt_escaped}':force_style='...'",
    "-c:v", "libx264", "-preset", "fast", "-crf", "20",
    "-pix_fmt", "yuv420p", output_path
])
```

## 2. SRT File Path Escaping for subtitles Filter

The `subtitles` filter in FFmpeg uses libass, which parses paths differently from FFmpeg itself. On Windows, paths must be escaped:

```python
# Required escaping for FFmpeg subtitles filter
srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")
# Example: C:\Users\me\video.srt -> C\:/Users/me/video.srt
```

Without this escaping, the subtitles filter silently fails (returncode 0, no subtitles rendered).

## 3. xfade Filter Label Naming

**Problem**: FFmpeg's filter_complex parser has restrictions on label naming. Labels starting with numbers (e.g., `v01`, `v02`) cause parsing errors.

**Symptoms**: `Error parsing filterchain` or `No such filter: 'v01'`

**Solution**: Use `tmp0`, `tmp1`, `tmp2` format (letter prefix + number):

```python
# WRONG
out_label = f"v{i}"           # v0, v1, v2 - may fail
in1 = f"v{i-1}" if i > 1 else "0:v"

# CORRECT
out_label = f"tmp{i-1}" if i < n - 1 else "v"
in1 = "0:v" if i == 1 else f"tmp{i-2}"
```

## 4. edge-tts Boundary Events

**Problem**: `WordBoundary` events from edge-tts contain fragment text (e.g., "n" at the end of some words). `SentenceBoundary` events contain clean, complete sentences.

**Rule**: Always use `SentenceBoundary` for subtitle text, never `WordBoundary`.

```python
# CORRECT - only collect SentenceBoundary
async for chunk in communicate.stream():
    if chunk["type"] == "audio":
        audio_data += chunk["data"]
    elif chunk["type"] == "SentenceBoundary":
        sentence_events.append(chunk)
    # Do NOT collect WordBoundary
```

## 5. edge-tts Does Not Cache Boundary Events

**Problem**: When audio files are cached from a previous run, skipping the TTS generation also loses the boundary event data (timing information for subtitles).

**Solution**: Always stream the TTS communicate object, even if the audio file already exists:

```python
# WRONG - skip TTS entirely when audio exists
if audio_path.exists():
    return get_duration(audio_path), []  # Empty entries!

# CORRECT - always stream to get timing
if audio_path.exists():
    dur = get_duration(audio_path)
else:
    dur = 0

async for chunk in communicate.stream():
    if chunk["type"] == "audio":
        if not audio_path.exists():
            audio_data += chunk["data"]
    elif chunk["type"] == "SentenceBoundary":
        sentence_events.append(chunk)

# Only write audio file if it's new
if not audio_path.exists() and audio_data:
    with open(audio_path, "wb") as f:
        f.write(audio_data)
```

## 6. Detecting Silent Subtitle Burn Failures

The `subtitles` filter can silently succeed (returncode 0) without actually burning subtitles. Detect this by comparing file sizes:

```python
in_size = os.path.getsize(input_path)
out_size = os.path.getsize(output_path)
if in_size == out_size:
    # Subtitles were NOT burned - file was just copied
    # Try again without force_style, or investigate path escaping
```

## 7. FFmpeg stderr vs stdout

When using `subprocess.run()` with `capture_output=True`, FFmpeg writes its progress output (frame count, bitrate, etc.) to stderr, not stdout. To see Python print statements alongside FFmpeg output:

- In PowerShell: `python script.py 2>$null` (suppress stderr) or pipe selectively
- In bash: `python script.py 2>/dev/null`
- Or redirect Python's stdout to a file and let stderr go to console
