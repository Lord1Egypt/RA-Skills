---
name: output
description: Downloading and saving generated videos to the local filesystem
metadata:
  tags: download, save, output, video, mp4
---

# Downloading and Saving Videos

After retrieving the result from the queue, download the video to the user's project directory.

## Download flow

```bash
# Create output directory
mkdir -p ./output

# Generate filename with timestamp
FILENAME="fabric-video-$(date +%Y-%m-%d-%H%M%S).mp4"

# Download the video
curl -s -o "./output/$FILENAME" "$VIDEO_URL"
```

## Report to user

After download, tell the user:

1. **Local file**: `./output/{filename}` — ready to use
2. **Hosted URL**: `{VIDEO_URL}` — temporarily available on fal.ai CDN
3. **File size**: from the API response `video.file_size` (convert to human-readable, e.g., "1.2 MB")

Example message:
> Video saved to `./output/fabric-video-2026-03-16-143022.mp4` (1.2 MB)
> Hosted URL: https://v3.fal.media/files/.../generated_video.mp4

## Fallback

If the download fails (curl returns non-zero), show the hosted URL so the user can download manually:

> Download failed. You can grab the video directly from:
> https://v3.fal.media/files/.../generated_video.mp4
