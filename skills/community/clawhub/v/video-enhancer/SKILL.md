---
name: video-enhancer
description: >
  Cloud-based video enhancement skill that uploads a user-selected local video file to Wondershare-hosted endpoints for AI enhancement,
  then downloads the processed result back to local storage. Use only when
  the user explicitly agrees to third-party cloud processing for a non-sensitive video,
  when user says "enhance video", "improve video quality", "upscale video",
  "make video clearer", "fix blurry video", "restore old footage", "video enhancement",
  "convert to HD", or provides a video file and requests quality improvement.
  supports MP4/MOV.
metadata: {"clawdbot":{"emoji":"🎞️","requires":{"bins":["ffmpeg"]},"install":[{"id":"brew","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg"}]}}
---

# Video Enhancer

Enhance a user-selected local video using Wondershare-hosted cloud processing.

This is a **cloud workflow**, not a fully local or offline enhancement pipeline.

## Use This Skill When

Use this skill when the user wants to:
- Enhance a blurry or low-quality local video
- Upscale a local `.mp4` or `.mov` video
- Convert a local video to a clearer HD result using cloud processing

Do not use this skill when:
- The user wants a fully local or offline workflow
- The task is trimming, editing, subtitle work, or format conversion only
- The input is a remote URL instead of a local file
- The user does not accept third-party cloud upload

## Preconditions

Before running:
- Confirm the input file exists
- Confirm the file extension is `.mp4` or `.mov`
- Confirm `ffprobe` is available
- ⚠️ Tell the user this workflow uploads the source file to a third-party cloud service  operated by Wondershare
- ⚠️ Use the skill only after the user accepts cloud processing
- ⚠️ The file is not sensitive, private, or confidential
- Enforce these limits:
  - If `max(width, height) <= 1920`, duration must be `<= 300` seconds
  - If `max(width, height) > 1920`, duration must be `<= 60` seconds
- Refuse the request if any limit fails and explain which limit was exceeded

## Privacy and Network Disclosure

This workflow uploads the local video file and basic metadata to Wondershare-operated cloud endpoints.

Uploaded data includes:
- The source video file
- Video duration
- Video width and height
- File MD5 checksum
- Computer name and MAC address to generate a non‑reversible SHA‑256 device ID. Raw data is never uploaded or stored, used only for device identification

Network endpoints used by the bundled script:
- `https://filmora-cloud-api-alisz.wondershare.cc/open/v1/resources/upload`
- `https://filmora-cloud-api-alisz.wondershare.cc/open/v1/tasks`
- `https://filmora-cloud-api-alisz.wondershare.cc/open/v1/tasks/<task_id>`
- The final download URL returned by the task result

Do not use this skill for sensitive files unless the user explicitly accepts third-party processing.

## Permissions

This skill requires:
- Read access only to the user-specified input video file
- Write access only to the selected output directory, or the input file's parent directory if no output directory is provided
- Network access to the Wondershare-hosted endpoints listed above
- Local execution of the fixed `ffprobe` binary for metadata inspection

This skill must not:
- Modify the original input file in place
- Scan directories for other media files
- Upload any file other than the user-specified input file
- Write arbitrary files outside the chosen output location

## Preferred Execution

Run the script using an absolute path:

```bash
python {baseDir}/scripts/video_enhance.py -i "/absolute/path/to/video.mp4" -o "/output/dir"
```

If the output directory is omitted, the script saves the enhanced file next to the input video.

## Workflow

1. Validate that the input file exists and has a supported extension
2. Read the local video metadata with `ffprobe`
3. Enforce duration and resolution limits
4. Upload the video file and metadata to the Wondershare cloud API
5. Submit the enhancement task
6. Poll until the task succeeds or fails
7. Download the enhanced result to the output directory
8. Report the saved file path to the user

## Input and Output

Input:
- Local video path
- Optional output directory

Output:
- Enhanced video saved to disk
- Filename pattern:

```text
<input_stem>_hd_YYYYMMDD_HHMMSS.<ext>
```

## Supported Formats

Supported input formats:
- `.mp4`
- `.mov`

## Security Notes

- This is a third-party cloud processing workflow
- The bundled script invokes only the fixed `ffprobe` binary with predefined arguments for local metadata inspection
- The workflow does not require arbitrary shell execution
- The workflow should use only the declared Wondershare-hosted endpoints and the final HTTPS task result download URL
- The tool should be treated as unsuitable for sensitive or confidential media

### Cloud Processing
- Videos are uploaded to filmora cloud services for AI enhancement
- Cloud providers temporarily store videos during processing
- Enhanced videos are downloaded to local storage
- Cloud-side data is deleted after processing completes

## Troubleshooting

Check that the file exists:

```bash
ls -lh "/absolute/path/to/video.mp4"
```

Check that `ffprobe` is available:

```bash
ffprobe -version
```

If the task fails:
- Verify network connectivity
- Re-run the script and inspect the error output
- Confirm the file is within the documented duration and format limits

## Script Location

Bundled script:
- `{baseDir}/scripts/video_enhance.py`

## Agent Guidance

- Always tell the user that the selected local video will be uploaded to a Wondershare-operated third-party cloud service before running the workflow
- Require explicit user consent in the current conversation before execution
- Refuse sensitive, private, or confidential videos
- Keep the response focused on the saved file path, cloud-processing disclosure, and any relevant warnings