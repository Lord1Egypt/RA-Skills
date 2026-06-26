---
name: webcodecs-string-finder
description: Finds valid WebCodecs strings for video and audio by researching codec support tables and detailed specifications on webcodecsfundamentals.org.
repository: https://github.com/socratescli/webcodecs-string-finder-skill.git
version: "1.0.0"
---

# WebCodecs String Finder

This skill helps you find the most supported and appropriate codec strings for WebCodecs, whether for video or audio.

## Workflow

### 1. Requirements Gathering
Understand the user's requirements:
- **Type**: Video or Audio?
- **Platform**: Chrome, Edge, Android, iOS, etc.?
- **Resolution**: 1080p, 4k, etc. (for video)?
- **Codec Name**: h264 (avc1), h265 (hev1/hvc1), vp9, av1, opus, aac, etc.?

### 2. Search for Supported Codecs
Use `web_fetch` to access the codec support table:
- URL: `https://webcodecsfundamentals.org/datasets/codec-support-table/`
- Identify the most supported codecs based on the requirement (platform and codec type).

### 3. Confirm Codec Details
For the top candidates found in the previous step, confirm their details:
- Use `web_fetch` to visit the detail page: `https://webcodecsfundamentals.org/codecs/<CODEC-STRING>.html`
- Replace `<CODEC-STRING>` with the identified candidate (e.g., `avc1.42e01e`).
- Verify that it meets the specific requirements (e.g., profile, level, platform support).

### 4. Recommendation
Return the 2-3 most fitted codec strings.
- Provide a brief explanation of why each was chosen.
- Include the browser/platform support if relevant.

## Tips
- Common video codec strings: `avc1.42e01e` (H.264 Baseline), `avc1.4d401f` (H.264 Main), `hev1.1.6.l93.b0` (H.265), `vp09.00.10.08` (VP9).
- Common audio codec strings: `opus`, `mp4a.40.2` (AAC-LC).
- When in doubt, prefer widely supported codecs like H.264 and Opus for maximum compatibility.
