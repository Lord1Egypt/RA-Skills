# Basic Usage Example

## Scenario: Analyzing a Local Video

**Question**: "What happens in the first minute of the video?"

### Step 1: Get Video Info

```bash
videoarm-info video.mp4
```

**Output:**
```json
{
  "duration": 180.5,
  "fps": 30.0,
  "total_frames": 5415,
  "has_audio": true
}
```

### Step 2: Explore First Minute (0-1800 frames)

```bash
videoarm-scene --video video.mp4 \
  --ranges '[{"start_frame":0,"end_frame":1800}]' \
  --num-frames 30
```

**Output:**
```json
{
  "ranges": [
    {
      "start_frame": 0,
      "end_frame": 1800,
      "caption": "A person enters a kitchen and starts preparing ingredients..."
    }
  ]
}
```

### Step 3: Get Audio Context

```bash
videoarm-audio --video video.mp4 --start-frame 0 --end-frame 1800
```

**Output:**
```
[00:00:05] "Let me show you how to make this dish"
[00:00:15] "First, we need to chop the vegetables"
...
```

### Step 4: Ask Specific Question

```bash
videoarm-analyze-clip --video video.mp4 \
  --start-frame 0 --end-frame 1800 \
  --question "What ingredients are being prepared?"
```

**Output:**
```json
{
  "answer": "Tomatoes, onions, and garlic are being chopped",
  "confidence": 0.9,
  "evidence": ["Frame 300: tomatoes on cutting board", ...]
}
```
