---
name: ffmpeg
description: Using FFmpeg and FFprobe in Remotion
metadata:
  tags: ffmpeg, ffprobe, video, trimming
---

> Subclip sandbox: use only pinned, validated imports and native Subclip tools. Package/skill installation, external CLI execution, provider API keys, and standalone project setup are unavailable. Verify managed resources before use; use a supported alternative when unavailable.

## FFmpeg in Remotion

`ffmpeg` and `ffprobe` do not need to be installed. They are available via the Subclip's native validation, frame inspection, and export tools and Subclip's native validation, frame inspection, and export tools:

Subclip manages dependencies and execution. Use the installed runtime and native Subclip tools; package installation and standalone CLI execution are unavailable inside a layer.


### Trimming videos

You have 2 options for trimming videos:

1. **Preferred**: Use the `trimBefore` and `trimAfter` props of the `<Video>` component. This is non-destructive, requires no re-encoding, and you can change the trim at any time.

```tsx
import {Video} from '@remotion/media';

<Video
  src={staticFile('video.mp4')}
  trimBefore={5 * fps}
  trimAfter={10 * fps}
/>;
```

2. Use the FFmpeg command line. You MUST re-encode the video to avoid frozen frames at the start of the video. Only use this if you need a standalone trimmed file (e.g. for upload or external use).

Subclip manages dependencies and execution. Use the installed runtime and native Subclip tools; package installation and standalone CLI execution are unavailable inside a layer.

