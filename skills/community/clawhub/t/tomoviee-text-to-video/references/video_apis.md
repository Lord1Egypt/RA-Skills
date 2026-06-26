# Tomoviee Video Generation APIs

## Overview
Tomoviee provides three video generation APIs supporting different input types and use cases.

## API Endpoints

### 1. Text-to-Video (tm_text2video_b)
**Generate video from text description only**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2video_b`

**Parameters**:
- `prompt` (required): Text description for video generation
- `resolution`: Video resolution - `720p` (default) or `1080p`
- `duration`: Video duration in seconds - only `5` is supported
- `aspect_ratio`: Video aspect ratio - `16:9` (default), `9:16`, `4:3`, `3:4`, `1:1`
- `camera_move_index`: Camera movement type (1-46, see camera_movements.md)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Create video from scratch with text only
- Generate establishing shots or B-roll footage
- Prototype video ideas quickly

**Example**:
```python
task_id = client.text_to_video(
    prompt="A golden retriever running through a sunlit meadow, slow motion",
    resolution="720p",
    aspect_ratio="16:9",
    camera_move_index=5  # Slow zoom in
)
```

---

### 2. Image-to-Video (tm_img2video_b)
**Generate video from image + text description**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_img2video_b`

**Parameters**:
- `prompt` (required): Text description guiding video generation
- `image` (required): Image URL (JPG/JPEG/PNG/WEBP format, <200M)
- `resolution`: Video resolution - `720p` (default) or `1080p`
- `duration`: Video duration in seconds - only `5` is supported
- `aspect_ratio`: Video aspect ratio - `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `original` (keeps image ratio)
- `camera_move_index`: Camera movement type (1-46, see camera_movements.md)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Animate still images with motion
- Create product demo videos from photos
- Add dynamic camera movements to static images
- Generate video variations from reference image

**Example**:
```python
task_id = client.image_to_video(
    prompt="Camera slowly panning right, golden hour lighting",
    image="https://example.com/sunset-beach.jpg",
    resolution="720p",
    aspect_ratio="original",
    camera_move_index=12  # Pan right
)
```

---

### 3. Video Continuation (tm_video_continuation_b)
**Continue/extend existing video**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_video_continuation_b`

**Parameters**:
- `prompt` (required): Text description for continuation
- `video` (required): Video URL (MP4 format, <200M, 5s duration, 720p resolution)
- `resolution`: Video resolution - `720p` (default) or `1080p`
- `duration`: Video duration in seconds - only `5` is supported (generates 5s continuation)
- `aspect_ratio`: Video aspect ratio - `16:9`, `9:16`, `4:3`, `3:4`, `1:1`
- `camera_move_index`: Camera movement type (1-46, see camera_movements.md)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Extend video clips beyond original length
- Create seamless video sequences
- Generate multiple continuation variations
- Overcome 5-second duration limit by chaining continuations

**Important Constraints**:
- Input video MUST be exactly 5 seconds, 720p resolution
- Output is always 5 seconds (extending the input)
- To create longer videos, chain multiple continuations

**Example**:
```python
# First generate 5s video
task_id_1 = client.text_to_video(
    prompt="A bird taking flight from a tree branch"
)

# Then continue it
task_id_2 = client.video_continuation(
    video="https://result.com/first_video.mp4",
    prompt="The bird soars higher into the blue sky"
)
```

---

## Common Parameters

### Resolution Options
- `720p`: 1280x720 (faster generation, lower quality)
- `1080p`: 1920x1080 (slower generation, higher quality)

### Aspect Ratio Options
- `16:9`: Widescreen (landscape) - standard video format
- `9:16`: Vertical (portrait) - mobile/social media
- `4:3`: Traditional TV format
- `3:4`: Vertical medium format
- `1:1`: Square - Instagram/social media
- `original`: (Image-to-Video only) Preserves input image ratio

### Duration
Currently only `5 seconds` is supported across all video APIs.

### Camera Movement
All video APIs support camera_move_index (1-46). See `camera_movements.md` for full list.
- Use `null`/`None` for automatic camera movement
- Specify index (1-46) for precise control

---

## Async Workflow

All video APIs are asynchronous:

1. **Create Task**: Call API endpoint → receive `task_id`
2. **Poll Status**: Call unified result endpoint with `task_id`
3. **Check Status**: 
   - `1` = Queued
   - `2` = Processing
   - `3` = Success (video ready)
   - `4` = Failed
   - `5` = Cancelled
   - `6` = Timeout
4. **Get Result**: When status=3, extract video URL from result JSON

**Unified Result Endpoint**: `https://openapi.wondershare.cc/v1/open/pub/task`

**Example Workflow**:
```python
# Create video
task_id = client.text_to_video(prompt="...")

# Poll for completion (built-in helper)
result = client.poll_until_complete(task_id, poll_interval=10, timeout=600)

# Extract video URL
import json
result_data = json.loads(result['result'])
video_url = result_data['video_path'][0]
```

---

## Error Handling

**Common Errors**:
- `400`: Invalid parameters (check resolution, aspect_ratio, duration)
- `401`: Authentication failed (verify app_key and access_token)
- `413`: File too large (image/video must be <200M)
- `422`: Invalid file format or constraints
- Task status `4`: Generation failed (check prompt or input quality)
- Task status `6`: Timeout (retry or contact support)

**Best Practices**:
- Always check response `code` field (0 = success)
- Implement exponential backoff for polling
- Set reasonable timeout (video generation typically takes 1-5 minutes)
- Validate file URLs are publicly accessible before API call
- Use callback URLs for production to avoid polling overhead

---

## Quota and Limits

- Maximum concurrent tasks: Check your plan
- File size limits: <200M for images/videos
- Video input constraints: Must be 5s, 720p for continuation API
- Supported formats: 
  - Images: JPG, JPEG, PNG, WEBP
  - Videos: MP4
- Generation time: Typically 1-5 minutes per 5-second video

---

## Chaining Videos

To create videos longer than 5 seconds:

```python
# Generate first 5s
task_1 = client.text_to_video(prompt="Scene 1...")
result_1 = client.poll_until_complete(task_1)
video_1_url = json.loads(result_1['result'])['video_path'][0]

# Continue for another 5s
task_2 = client.video_continuation(video=video_1_url, prompt="Scene 2...")
result_2 = client.poll_until_complete(task_2)
video_2_url = json.loads(result_2['result'])['video_path'][0]

# Continue again for another 5s
task_3 = client.video_continuation(video=video_2_url, prompt="Scene 3...")
result_3 = client.poll_until_complete(task_3)
video_3_url = json.loads(result_3['result'])['video_path'][0]

# Now concatenate all three 5s clips to create 15s final video
```

Note: You'll need to download and concatenate videos using a tool like ffmpeg or video editing software.
