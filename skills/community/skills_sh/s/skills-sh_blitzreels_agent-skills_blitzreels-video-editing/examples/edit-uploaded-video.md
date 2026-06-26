# Example: Edit an Uploaded Video

Full workflow: upload → transcribe → trim → caption → export.

## 1. Create Project

```bash
bash scripts/blitzreels.sh POST /projects '{"name":"My Edit","aspect_ratio":"9:16"}'
# → {"id":"proj_abc123", ...}
```

## 2. Upload Media from URL

```bash
bash scripts/editor.sh upload-url proj_abc123 "https://example.com/video.mp4" "Interview Raw"
# → {"id":"media_xyz", "status":"processing", ...}
```

Wait for processing to complete (check via context).

## 3. Add Media to Timeline

```bash
bash scripts/editor.sh add-media proj_abc123 media_xyz
# → Adds clip starting at 0s on the timeline
```

## 4. Transcribe

```bash
bash scripts/editor.sh transcribe proj_abc123 media_xyz
# → Polls until transcription completes
```

## 5. Check Timeline State

```bash
bash scripts/editor.sh context proj_abc123 timeline
# → Shows all timeline items with timestamps
```

## 6. Trim Dead Air

Remove 2 seconds from the start and 3 seconds from the end of a clip:

```bash
bash scripts/editor.sh trim proj_abc123 item_001 2.0 -3.0
```

## 7. Silence Cleanup (Optional)

No public silence-detection endpoint is registered today. Use the dashboard/clipping flow, or inspect transcript/context and apply explicit trim/split/delete/move operations.

## 8. Apply Captions

```bash
bash scripts/editor.sh captions proj_abc123 viral-center
```

## 9. Add Emphasis to Key Words

```bash
bash scripts/blitzreels.sh POST /projects/proj_abc123/captions/words/emphasis \
  '{"words":["amazing","incredible","profit"]}'
```

## 10. Export

```bash
bash scripts/editor.sh export proj_abc123 --resolution 1080p
# → Polls until export completes, prints download URL
```
