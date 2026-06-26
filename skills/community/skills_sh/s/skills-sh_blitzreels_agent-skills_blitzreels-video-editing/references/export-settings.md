# Export Settings Reference

## Export Request Body

```json
{
  "resolution": "1080p",
  "frameRate": 30,
  "videoCodec": "h264",
  "audioCodec": "aac",
  "bitrateMode": "vbr",
  "crfValue": 23,
  "twoPassEncoding": false,
  "containerFormat": "mp4",
  "colorSpace": "bt709",
  "exportRange": "full",
  "includeWatermark": true
}
```

### Resolution Options
| Value | Description |
|-------|-------------|
| `"0.25x"` | Quarter resolution |
| `"0.5x"` | Half resolution |
| `"720p"` | 1280×720 |
| `"1080p"` | 1920×1080 (default) |
| `"1440p"` | 2560×1440 |
| `"4k"` | 3840×2160 |
| `"2x"` | Double resolution |

### Video Codecs
| Value | Description |
|-------|-------------|
| `h264` | H.264 — best compatibility (default) |
| `h265` | H.265/HEVC — better compression |
| `prores` | Apple ProRes — editing quality |
| `vp9` | VP9 — web-optimized |

### Audio Codecs
`aac` · `mp3` · `opus` · `pcm`

### Bitrate Modes
| Value | Description |
|-------|-------------|
| `cbr` | Constant bitrate — predictable file size |
| `vbr` | Variable bitrate — better quality/size ratio |
| `crf` | Constant rate factor — quality-targeted |

### Frame Rates
`24` · `25` · `30` · `48` · `50` · `60`

### Color Spaces
`bt709` · `bt2020` · `srgb`

### Export Range
| Value | Description |
|-------|-------------|
| `full` | Entire project |
| `in-out` | Between in/out points |
| `selection` | Currently selected items |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/export` | Start export job |
| GET | `/exports/{exportId}` | Get export status + download URL |
| GET | `/projects/{id}/exports` | List export history |
| DELETE | `/projects/{id}/exports` | Delete all exports |
| GET | `/jobs/{jobId}` | Generic job status polling |

## Export Polling Pattern

```bash
# 1. Start export
EXPORT_JSON=$(blitzreels.sh POST "/projects/${PID}/export" '{"resolution":"1080p"}')
EXPORT_ID=$(echo "$EXPORT_JSON" | jq -r '.export_id // .exportId // .id')

# 2. Poll until done
while true; do
  STATUS=$(blitzreels.sh GET "/exports/${EXPORT_ID}" | jq -r '.status')
  case "$STATUS" in
    completed|done|success) break ;;
    failed|error) echo "Failed"; exit 1 ;;
    *) sleep 5 ;;
  esac
done

# 3. Get download URL
blitzreels.sh GET "/exports/${EXPORT_ID}" | jq -r '.download_url // .downloadUrl // .url'
```

## Notes

- Export is an **expensive operation** — requires `BLITZREELS_ALLOW_EXPENSIVE=1`
- Typical export time: 30s–5min depending on project length and resolution
- Download URLs are temporary (24h TTL) — save/rehost promptly
- `editor.sh export` wraps the full poll loop for convenience
