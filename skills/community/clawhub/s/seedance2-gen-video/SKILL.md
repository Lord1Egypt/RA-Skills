---
name: seedance2-gen-video
description: Generate videos using the Volcengine Doubao Seedance 2.0 model series. Supports text-to-video, image-to-video (first frame/last frame), multimodal reference-to-video, video editing, video extension, and more. Can generate videos with audio, and supports custom resolution/aspect ratio/duration. Use this skill when the user needs to generate, edit, or extend videos, or mentions Seedance or video generation API.
compatibility: Requires Python 3.8+ and volcengine-python-sdk[ark], requires the ARK_API_KEY environment variable to be configured, requires access to the Volcengine API (https://ark.cn-beijing.volces.com)
metadata:
  author: SkillDeveloper
  version: "1.0"
allowed-tools: Bash(python3:*) Bash(pip:*)
---

# Seedance 2.0 Video Generation Skill

Generate videos using the Volcengine Doubao Seedance 2.0 model series.

## Prerequisites

1. **API Key**: The `ARK_API_KEY` environment variable is configured, or provided by the user.
2. **SDK Installation**: `pip install 'volcengine-python-sdk[ark]'`
3. **Asset URLs**: Reference images, videos, and audio must be **publicly accessible** URLs (or platform asset IDs in `asset://` format).

## Usage Steps

### Step 1: Collect Parameters

Confirm the following information with the user:

| Parameter | Description | Default |
|-----------|-------------|---------|
| Prompt | Describes the video content to generate | Required |
| Model | `doubao-seedance-2-0-260128` (high quality) or `doubao-seedance-2-0-fast-260128` (fast) | High quality |
| Aspect Ratio | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, or `adaptive` (follows the input image) | `16:9` |
| Duration | 4~15 seconds | `5` |
| Generate Audio | Whether to generate video with audio | No |
| Watermark | Whether to add a watermark | No |
| Reference Image URLs | 0~9 images, optional (role: reference_image / first_frame / last_frame) | None |
| Reference Video URLs | 0~3 videos, optional (role: reference_video) | None |
| Reference Audio URLs | 0~3 audio clips, optional (role: reference_audio) | None |
| Web Search | Whether to enable (only effective for plain text input) | No |

**Prompt asset referencing rules**: In the prompt, use "Image N", "Video N", "Audio N" to reference corresponding assets (N is the order of assets of the same type in the content array, starting from 1).

### Step 2: Install Dependencies (First Time)

```bash
pip install 'volcengine-python-sdk[ark]'
```

```bash
ARK_API_KEY=$ARK_API_KEY
```


### Step 3: Run the Script

Call `scripts/gen_video.py` to execute the video generation task.

**Basic example (text-to-video):**
```bash
python3 scripts/gen_video.py \
  --prompt "A cat running on a grassy field, bright sunlight, slow motion" \
  --ratio "16:9" \
  --duration 5
```

**Image-to-video (first frame):**
```bash
python3 scripts/gen_video.py \
  --prompt "The scene in Image 1, camera slowly pushes forward" \
  --images "https://example.com/frame.jpg" \
  --image-roles "first_frame" \
  --ratio "16:9" \
  --duration 5
```

**First and last frame image-to-video:**
```bash
python3 scripts/gen_video.py \
  --prompt "Image 1 is the starting frame, Image 2 is the ending frame, camera pans from left to right" \
  --images "https://example.com/start.jpg" "https://example.com/end.jpg" \
  --image-roles "first_frame" "last_frame" \
  --ratio "16:9" \
  --duration 5
```

**Multimodal reference-to-video:**
```bash
python3 scripts/gen_video.py \
  --prompt "Mimic the camera style of Video 1, use Image 1 as the scene, with Audio 1 as background music" \
  --images "https://example.com/scene.jpg" \
  --image-roles "reference_image" \
  --videos "https://example.com/style.mp4" \
  --audios "https://example.com/music.mp3" \
  --generate-audio \
  --duration 8
```

**Edit video:**
```bash
python3 scripts/gen_video.py \
  --prompt "Replace the red car in Video 1 with a blue car, keep the camera movement unchanged" \
  --videos "https://example.com/original.mp4" \
  --duration 5
```

**Extend video (multi-segment concatenation):**
```bash
python3 scripts/gen_video.py \
  --prompt "The scene in Video 1 transitions to Video 2, then continues with Video 3" \
  --videos "https://example.com/v1.mp4" "https://example.com/v2.mp4" "https://example.com/v3.mp4" \
  --duration 10
```

**Video with audio + web search:**
```bash
python3 scripts/gen_video.py \
  --prompt "Macro shot of a glass frog, showing its beating heart through its transparent abdomen" \
  --generate-audio \
  --web-search \
  --duration 8
```

### Step 4: Get Results

After the script succeeds, it outputs the video URL, which is valid for 24 hours. Advise the user to download or transfer to TOS promptly.

## Notes

- **Face policy**: Directly uploading images/videos containing real human faces is not supported. Use platform-provided virtual avatars (`asset://asset-xxx`) or authorized real-person assets.
- **Video URL validity**: Generated video URLs are valid for only 24 hours; save them promptly.
- **Unsupported input combinations**: "Text + Audio" or "Audio only" input is not supported.
- **Adaptive aspect ratio**: When using first/last frame images, it is recommended to set `--ratio adaptive` to avoid frame jumps.

## Parameter Details

See [references/api-guide.md](references/api-guide.md)
