# YouTube Video Example

## Scenario: Analyzing a YouTube Video

### Step 1: Download Video

```bash
videoarm-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Output:**
```json
{
  "local_path": "/Users/username/.videoarm/videos/dQw4w9WgXcQ.mp4",
  "title": "Video Title",
  "duration": 212.0
}
```

### Step 2: Analyze with Local Path

```bash
videoarm-info /Users/username/.videoarm/videos/dQw4w9WgXcQ.mp4
```

Then use other commands as shown in basic_usage.md
