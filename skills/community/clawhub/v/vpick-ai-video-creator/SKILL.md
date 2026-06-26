---
name: vpick-ai-video-creator
description: "All-in-one AI video production studio on a visual canvas. Generate videos (Kling 3.0, Veo 3.1, Sora 2, Runway, Grok, Midjourney Video), generate images (nano-banana, Midjourney, Grok, Seedream), add voiceover (ElevenLabs TTS), generate music (Suno), lip-sync faces (Kling AI Avatar), separate vocals (Demucs), change voices (ElevenLabs STS), combine clips with audio — all in one workflow. Use when the user says 'create a video', 'generate video', 'make a short film', 'AI video', 'video production', 'MultiShot', 'add voiceover', 'lip sync', 'generate music', 'combine videos', or wants end-to-end AI video creation."
version: 1.0.1
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://vpick-doc.10xboost.org/guide/mcp-connection.html
---

# VPick Video Creator

All-in-one AI video production studio — from image generation to video creation, voiceover, music, lip-sync, and final export — all on a visual canvas. Powered by [VPick](https://vpick.10xboost.org).

## Security & Data Handling

- **MCP link is a credential**: Your MCP config contains an embedded authentication token in the URL (`https://vpick.10xboost.org/mcp/t/xxxxx...`). Treat it like a password — do not share it publicly.
- **Token scope**: The embedded token grants **generation access** to your VPick account. It can create/manage canvas nodes, trigger video/image/audio generations, upload media, and export results. It cannot access your social media accounts or any services outside VPick.
- **Token storage**: The token is stored server-side in VPick's database (Google Cloud, us-central1). It is never written to your local filesystem. You can regenerate it anytime at [vpick.10xboost.org/settings](https://vpick.10xboost.org/settings).
- **Data flow**: All generation requests go through VPick's server (`vpick.10xboost.org` on Google Cloud). VPick routes requests to third-party AI model providers (Kling, Veo, Runway, Sora, ElevenLabs, Suno) on your behalf. Your prompts and uploaded media are sent to these providers for processing.
- **Storage**: Generated files are stored in Google Cloud Storage under your VPick account. Uploaded images/videos are used only for generation and stored in your project.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Billing**: Generation costs are charged to your VPick credit balance, not directly to any third-party service.
- **Third-party service**: This skill relies on [VPick](https://vpick.10xboost.org), a cloud AI video production platform. Documentation: [vpick-doc.10xboost.org](https://vpick-doc.10xboost.org). Source code: [github.com/snoopyrain](https://github.com/snoopyrain).

## Prerequisites

1. **Sign up** at [vpick.10xboost.org](https://vpick.10xboost.org) (Google OAuth — new users get $1 free credit)
2. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token)
3. **Add to Claude**: Paste the MCP link into Claude settings as a Connector — no install, no API keys needed
4. **Top up credits** if needed — generation costs are deducted from your VPick balance

## Supported Models

### Video Generation Models

| Model | Duration | Sound | Cost | MultiShot | Best For |
|-------|----------|-------|------|-----------|----------|
| **Kling 3.0 Standard** | 3-10s | Yes | ~$0.30/sec | Yes | MultiShot scenes, character consistency |
| **Kling 3.0 Professional** | 3-10s | Yes | ~$0.405/sec | Yes | Higher quality MultiShot |
| **Veo 3.1 Fast** | 8s fixed | Yes | $0.90/video | No | Quick high-quality clips |
| **Sora 2** | 10-15s | Yes | $0.525-$0.60 | No | Creative, artistic videos |
| **Runway 720p/1080p** | 5-10s | No | $0.18-$0.45 | No | Fast iteration |
| **Grok Imagine** | 6-15s | Yes | $0.15-$0.60 | No | Budget-friendly with audio |
| **Midjourney Video** | 5s | No | $0.90 | No | Stylized, artistic clips |

### Image Generation Models (for references, storyboards, thumbnails)

| Model | Cost | Output | Best For |
|-------|------|--------|----------|
| **nano-banana-2** | $0.16/image | 1 image | Default, fast, multi-reference |
| **Midjourney** (relaxed/fast/turbo) | $0.045-$0.24/grid | 4 images | Artistic, stylized |
| **Grok Imagine** | $0.06/call | 6 images | Bulk, budget |
| **Seedream 5.0** (Lite/HD) | $0.0825/image | 1 image (2K-3K) | High resolution |

### Audio & Voice Models

| Model | Type | Cost | Features |
|-------|------|------|----------|
| **ElevenLabs V3** | Text-to-Speech | $0.21/1000 chars | 29+ voices, multi-language, stability control |
| **Suno V4.5** | Music Generation | $0.10/song | Custom style, instrumental toggle, vocal gender |
| **Kling AI Avatar** | Lip Sync | $0.12/sec | Face animation from image + audio |
| **Demucs** | Vocal Separation | $0.30/call | Isolate vocals/accompaniment from audio |
| **ElevenLabs STS v2** | Voice Changer | Free (user API key) | Speech-to-speech, noise removal |

## Production Pipeline Overview

VPick covers the **entire video production workflow** in one place:

```
Image Gen → Video Gen → Voiceover/Music → Lip Sync → Vocal/Voice Edit → Combine & Export
```

1. **Pre-production**: Generate character designs, environments, storyboard frames
2. **Video generation**: Single shot or MultiShot with character consistency
3. **Audio production**: Voiceover (ElevenLabs TTS), music (Suno), vocal separation (Demucs), voice changing
4. **Lip sync**: Animate a face image to speak with generated audio (Kling AI Avatar)
5. **Post-production**: Combine video clips, mix audio tracks, export final video

## Core Workflow

### Step 1: Set Up the Canvas

Start by understanding the user's project:
- Call `get_canvas` to see the current state
- Call `list_projects` to check existing projects
- Use `create_project` if starting fresh

### Step 2: Prepare Assets

Create input nodes on the canvas:

**Text prompts:**
```
add_node(type: "text", name: "Scene 1 Prompt", data: { content: "A samurai walking through rain, cinematic lighting" })
```

**Reference images (for start/end frames or character consistency):**
```
upload_image(url: "https://example.com/character.jpg")
```

**Generate images first if needed:**
```
run_image_generator(nodeId: "<image_node_id>", prompt: "samurai portrait, white background", model: "nano-banana-2")
```

### Step 3: Generate Video

#### Simple Video (Single Shot)
```
add_node(type: "video-generator", name: "Scene 1")
connect_nodes(sourceId: "<prompt_node>", targetId: "<video_node>", sourceHandle: "text-out", targetHandle: "prompt-in")
connect_nodes(sourceId: "<image_node>", targetId: "<video_node>", sourceHandle: "image-out", targetHandle: "start-image-in")
run_video_generator(nodeId: "<video_node>", model: "kling-3.0", duration: 5, sound: true)
```

#### MultiShot Video (Multiple Connected Shots — Kling 3.0 Only)

MultiShot generates 3-15 seconds of video with multiple camera angles and character consistency in a single API call.

```
run_video_generator(
  nodeId: "<video_node>",
  model: "kling-3.0",
  multiShot: true,
  multiPrompt: [
    { "prompt": "@character walks into frame, wide shot", "duration": 4 },
    { "prompt": "@character looks at camera, medium close-up", "duration": 3 },
    { "prompt": "@character turns away, slow dolly out", "duration": 3 }
  ],
  elements: [
    {
      "name": "character",
      "description": "Main protagonist, male samurai",
      "imageUrls": ["https://.../char-front.jpg", "https://.../char-side.jpg"]
    }
  ],
  sound: true
)
```

**MultiShot Rules:**
- Minimum 2 reference images per element (white background, isolated figure)
- Element `name` must **exactly match** `@name` in prompts (case-sensitive)
- Total duration: 3-15 seconds
- Max 5 shots per group
- Sound is forced ON in MultiShot mode

### Step 4: Audio Production

Audio is a core part of video production. VPick supports 5 audio tools:

#### 4a. Voiceover — ElevenLabs Text-to-Speech

Generate natural narration or dialogue from text. 29+ built-in voices, multi-language support.

```
add_node(type: "audio-generator", name: "Narration")
run_audio_generator(
  nodeId: "<audio_node>",
  prompt: "The samurai stood alone in the rain, waiting for dawn.",
  model: "elevenlabs",
  voiceId: "<voice_id>",
  stability: 0.5
)
```

You can connect a Text node as input:
```
connect_nodes(sourceId: "<text_node>", targetId: "<audio_node>", sourceHandle: "text-out", targetHandle: "text-in")
```

#### 4b. Music Generation — Suno

Create original background music, theme songs, or jingles.

```
add_node(type: "music-generator", name: "BGM")
run_music_generator(
  nodeId: "<music_node>",
  prompt: "epic cinematic orchestral, tension building, dark atmosphere",
  model: "suno",
  instrumental: true,
  style: "cinematic orchestral"
)
```

Set `instrumental: false` to include AI-generated vocals with lyrics from the prompt.

#### 4c. Lip Sync — Kling AI Avatar

Animate a character's face to speak with any audio. Turns a still image into a talking head video.

```
add_node(type: "lipsync-generator", name: "Talking Character")
connect_nodes(sourceId: "<face_image>", targetId: "<lipsync_node>", sourceHandle: "image-out", targetHandle: "image-in")
connect_nodes(sourceId: "<audio_node>", targetId: "<lipsync_node>", sourceHandle: "audio-out", targetHandle: "audio-in")
run_lipsync_generator(nodeId: "<lipsync_node>")
```

Cost: ~$0.12/sec. Great for dialogue scenes, explainer videos, or virtual presenters.

#### 4d. Vocal Separation — Demucs

Isolate vocals from background music in any audio/video file. Outputs: vocals track, accompaniment track, and original.

```
add_node(type: "vocal-separator", name: "Separate Audio")
connect_nodes(sourceId: "<video_or_audio>", targetId: "<separator_node>", ...)
run_vocal_separator(nodeId: "<separator_node>")
```

Use cases: Extract dialogue from a scene, remove background music, remix audio.

#### 4e. Voice Changer — ElevenLabs Speech-to-Speech

Transform any voice recording into a different voice while preserving speech patterns and emotion.

```
add_node(type: "voice-changer", name: "New Voice")
connect_nodes(sourceId: "<original_audio>", targetId: "<voice_changer_node>", sourceHandle: "audio-out", targetHandle: "audio-in")
run_voice_changer(nodeId: "<voice_changer_node>", voiceId: "<target_voice_id>", removeBackgroundNoise: true)
```

Requires user's own ElevenLabs API key (free, no credit charge).

#### 4f. Audio Mixing

Combine multiple audio tracks (e.g., voiceover + BGM) into one:

```
add_node(type: "audio-combine", name: "Mixed Audio")
connect_nodes(sourceId: "<voiceover>", targetId: "<mix_node>", sourceHandle: "audio-out", targetHandle: "audio-in")
connect_nodes(sourceId: "<bgm>", targetId: "<mix_node>", sourceHandle: "audio-out", targetHandle: "audio-in")
run_audio_combine(nodeId: "<mix_node>")
```

Supports up to 10 audio inputs.

### Step 5: Combine & Export

**Combine multiple video clips:**
```
add_node(type: "combine", name: "Final Video")
connect_nodes(sourceId: "<video_1>", targetId: "<combine_node>", sourceHandle: "video-out", targetHandle: "videos-in")
connect_nodes(sourceId: "<video_2>", targetId: "<combine_node>", sourceHandle: "video-out", targetHandle: "videos-in")
connect_nodes(sourceId: "<bgm_node>", targetId: "<combine_node>", sourceHandle: "audio-out", targetHandle: "audio-in")
run_combine(nodeId: "<combine_node>")
```

**Mix audio tracks:**
```
run_audio_combine(nodeId: "<audio_combine_node>")
```

### Step 6: Organize Canvas

Keep the canvas clean:
```
auto_layout(nodeIds: ["<id1>", "<id2>", ...], direction: "horizontal", spacing: 200)
create_group(nodeIds: ["<id1>", "<id2>", ...], overrides: { label: "Scene 1", color: "#4A90D9" })
```

## Workflows (Automated Pipelines)

For repeatable processes, create workflows:
```
create_workflow(nodes: [...], edges: [...])
run_workflow(workflowId: "<id>")
```

## Checking Results

- `list_nodes` — See all nodes with their generation status and output URLs
- `get_node(id)` — Get specific node details including generated video/audio URLs
- `list_generated_files(limit: 10)` — Recent generation history
- `get_generation_stats` — Usage breakdown by model and cost

## Tips

- **Start with image generation** to create reference images for characters/environments before video
- **Use MultiShot** for scenes with character consistency — it's the most powerful feature
- **White background** reference images work best for Elements
- **Check credits** before large generations — use `get_generation_stats` to see spending
- **Element name mismatch** is the most common bug — always verify `@name` matches exactly
- **Aspect ratio** is set once and affects all generations — confirm with user first (16:9, 9:16, 1:1)

## Error Handling

| Error | Solution |
|-------|----------|
| Generation timeout | Auto-retries up to 2 times; check node status with `get_node` |
| Insufficient credits | Prompt user to top up at vpick.10xboost.org |
| Element name mismatch | Verify `@name` in prompts matches element `name` exactly |
| Invalid media format | Videos: MP4 recommended; Images: JPG/PNG |
| Node not found | Use `list_nodes` to get current node IDs |

## Documentation

- VPick App: [vpick.10xboost.org](https://vpick.10xboost.org)
- Available models: Call `list_models` tool for current pricing and capabilities
