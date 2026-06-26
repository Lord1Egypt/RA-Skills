# Tomoviee Audio Generation APIs

## Overview
Tomoviee provides four audio generation APIs covering music creation, sound effects, text-to-speech, and video soundtracks.

## API Endpoints

### 1. Text-to-Music (tm_text2music)
**Generate background music from text description**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2music`

**Parameters**:
- `prompt` (required): Music description (subject + scene/atmosphere/style)
- `duration`: Audio duration in seconds - 5 to 900 (default: 20)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Generate background music for videos
- Create royalty-free music for content
- Produce atmospheric soundtracks
- Generate music beds for podcasts/presentations

**Prompt Structure**:
```
[Subject/Theme] + [Scene/Atmosphere] + [Style/Genre]
```

**Examples**:
```python
# Upbeat commercial music
task_id = client.text_to_music(
    prompt="Upbeat corporate technology music, modern and energetic, electronic pop style with piano",
    duration=60
)

# Cinematic background
task_id = client.text_to_music(
    prompt="Epic cinematic orchestral music, dramatic and inspiring, Hollywood film score style",
    duration=120
)

# Calm ambient
task_id = client.text_to_music(
    prompt="Peaceful meditation music, calm and relaxing, ambient with soft synth pads",
    duration=300
)

# Specific genre
task_id = client.text_to_music(
    prompt="Jazz music for cafe scene, smooth and sophisticated, with piano and double bass",
    duration=90
)
```

**Duration Guidelines**:
- Short (5-30s): Intro/outro, transitions, jingles
- Medium (30-120s): Social media videos, ads, short presentations
- Long (120-900s): Full videos, podcasts, extended scenes

**Prompt Tips**:
- Specify genre (electronic, orchestral, jazz, rock, ambient, etc.)
- Include mood/atmosphere (upbeat, dramatic, calm, mysterious, etc.)
- Mention key instruments if important
- Add tempo hints (fast, slow, moderate)
- Reference use case for context

---

### 2. Text-to-Sound-Effect (tm_text2sfx)
**Generate sound effects from text description**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2sfx`

**Parameters**:
- `prompt` (required): Sound effect description
- `duration`: Audio duration in seconds - 5 to 180 (default: 10)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Create custom sound effects for videos
- Generate foley sounds
- Produce game audio assets
- Create notification/UI sounds
- Add environmental ambience

**Examples**:
```python
# Nature sounds
task_id = client.text_to_sound_effect(
    prompt="Heavy rain falling on roof with distant thunder",
    duration=30
)

# Action sounds
task_id = client.text_to_sound_effect(
    prompt="Car engine starting and revving",
    duration=8
)

# UI/notification sounds
task_id = client.text_to_sound_effect(
    prompt="Soft notification bell chime",
    duration=2
)

# Environmental ambience
task_id = client.text_to_sound_effect(
    prompt="Busy city street with traffic and people talking",
    duration=60
)

# Mechanical sounds
task_id = client.text_to_sound_effect(
    prompt="Keyboard typing sounds, mechanical switches",
    duration=15
)
```

**Duration Guidelines**:
- Very Short (1-5s): UI sounds, notifications, single events
- Short (5-15s): Action sounds, transitions, specific events
- Medium (15-60s): Ambience loops, environmental sounds
- Long (60-180s): Extended ambience, background environments

**Prompt Tips**:
- Be specific about the sound source
- Include context (heavy/light, fast/slow, near/far)
- Mention materials if relevant (wood, metal, glass)
- Describe sound character (crisp, muffled, echoing, etc.)
- For ambience, describe the environment

---

### 3. Text-to-Speech (tm_text2speech)
**Convert text to natural speech audio**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2speech`

**Parameters**:
- `text` (required): Text to convert to speech (max 5000 characters)
- `voice_id`: Voice ID (default: `zh-CN-YunxiNeural`)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Generate voiceovers for videos
- Create audio versions of text content
- Produce narration for presentations
- Generate dialogue for characters
- Accessibility features (text-to-audio conversion)

**Examples**:
```python
# Chinese voice (default)
task_id = client.text_to_speech(
    text="欢迎使用天幕AI视频生成平台。我们提供专业的视频、图像和音频生成服务。",
    voice_id="zh-CN-YunxiNeural"
)

# English voice
task_id = client.text_to_speech(
    text="Welcome to Tomoviee AI platform. We provide professional video, image, and audio generation services.",
    voice_id="en-US-JennyNeural"
)

# Long narration (multiple sentences)
long_text = """
This is a comprehensive guide to using AI-generated content.
First, you need to understand the basics.
Then, you can explore advanced features.
Finally, apply what you learned to your projects.
"""
task_id = client.text_to_speech(
    text=long_text,
    voice_id="en-US-GuyNeural"
)
```

**Voice ID Options**:
Common voice IDs include:
- **Chinese**: `zh-CN-YunxiNeural`, `zh-CN-XiaoxiaoNeural`, `zh-CN-YunjianNeural`
- **English (US)**: `en-US-JennyNeural`, `en-US-GuyNeural`, `en-US-AriaNeural`
- **English (UK)**: `en-GB-SoniaNeural`, `en-GB-RyanNeural`
- **Other languages**: Check Tomoviee documentation for full list

**Text Guidelines**:
- Maximum 5000 characters per request
- For longer content, split into multiple requests
- Use proper punctuation for natural pauses
- Include phonetic spelling for unusual names/terms
- Avoid excessive special characters

**Prompt Tips**:
- Write naturally as you would speak
- Use commas and periods for pacing
- Consider the target language and voice gender
- Test different voices for best match to content
- For emphasis, try rephrasing rather than CAPS

---

### 4. Video Soundtrack (tm_video_scoring)
**Generate soundtrack tailored to video content**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_video_scoring`

**Parameters**:
- `video` (required): Video URL (MP4 format, <200M)
- `prompt`: Optional music style description
- `duration`: Audio duration in seconds - 5 to 900 (default: 20)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Auto-generate music that matches video mood/pacing
- Create synchronized soundtracks
- Add background music to silent videos
- Generate adaptive scores based on video content
- Quick soundtrack prototyping

**Examples**:
```python
# Auto-generate based on video analysis
task_id = client.video_soundtrack(
    video="https://example.com/my-video.mp4",
    duration=60
)

# Guided style
task_id = client.video_soundtrack(
    video="https://example.com/travel-vlog.mp4",
    prompt="Upbeat travel vlog music, adventurous and inspiring",
    duration=120
)

# Specific mood
task_id = client.video_soundtrack(
    video="https://example.com/product-demo.mp4",
    prompt="Modern corporate tech music, professional and clean",
    duration=45
)

# Dramatic scene
task_id = client.video_soundtrack(
    video="https://example.com/action-scene.mp4",
    prompt="Intense action music with driving rhythm",
    duration=30
)
```

**How It Works**:
1. API analyzes video content (scenes, pacing, mood)
2. Generates music that matches video characteristics
3. If `prompt` provided, combines video analysis with style guidance
4. Duration should match video length or intended music length

**Prompt Guidelines**:
- Optional - omit for fully automatic generation
- If provided, give high-level style/mood guidance
- Let the API handle sync and pacing based on video
- Don't over-specify - video analysis already provides context

**Video Requirements**:
- Format: MP4
- Size: <200M
- Publicly accessible URL
- Reasonable quality (not corrupted)

---

## Common Parameters

### Duration Ranges

| API | Min | Max | Default | Typical Use |
|-----|-----|-----|---------|-------------|
| Text-to-Music | 5s | 900s (15min) | 20s | Background music, full tracks |
| Text-to-SFX | 5s | 180s (3min) | 10s | Sound effects, ambience |
| Text-to-Speech | N/A | Based on text | N/A | Matches text length |
| Video Soundtrack | 5s | 900s (15min) | 20s | Match video duration |

### Callback URLs
All audio APIs support optional callback URLs for async notification when generation completes.

**Callback Payload**:
```json
{
  "task_id": "...",
  "status": 3,
  "result": "{\"audio_path\": [\"https://...\"]}"
  "params": "your_transparent_params"
}
```

---

## Async Workflow

All audio APIs are asynchronous:

1. **Create Task**: Call API endpoint → receive `task_id`
2. **Poll Status**: Call unified result endpoint with `task_id`
3. **Check Status**: 
   - `1` = Queued
   - `2` = Processing
   - `3` = Success (audio ready)
   - `4` = Failed
   - `5` = Cancelled
   - `6` = Timeout
4. **Get Result**: When status=3, extract audio URL from result JSON

**Unified Result Endpoint**: `https://openapi.wondershare.cc/v1/open/pub/task`

**Example Workflow**:
```python
# Create task
task_id = client.text_to_music(
    prompt="Upbeat electronic music",
    duration=60
)

# Poll for completion
result = client.poll_until_complete(task_id, poll_interval=5, timeout=300)

# Extract audio URL
import json
result_data = json.loads(result['result'])
audio_url = result_data['audio_path'][0]
```

**Generation Times**:
- Text-to-Music: 30s - 2min (depends on duration)
- Text-to-SFX: 10s - 1min
- Text-to-Speech: 5s - 30s
- Video Soundtrack: 1min - 3min (includes video analysis)

---

## Prompt Engineering Tips

### Music Prompts
**Structure**: `[Subject/Theme] + [Atmosphere/Mood] + [Style/Genre] + [Instruments]`

**Good Examples**:
- "Epic cinematic orchestral music, dramatic and heroic, with brass and strings"
- "Chill lofi hip hop beats, relaxed and contemplative, with piano and soft drums"
- "Energetic workout music, motivating and powerful, electronic dance with heavy bass"
- "Romantic piano music, gentle and emotional, solo piano with soft reverb"

**Avoid**:
- Too vague: "good music"
- Conflicting moods: "sad and happy upbeat music"
- Overly technical: "120 BPM, C major, with specific chord progressions" (AI determines this)

### Sound Effect Prompts
**Structure**: `[Sound Source] + [Action/Context] + [Characteristics]`

**Good Examples**:
- "Glass bottle breaking on concrete floor, sharp and crisp"
- "Ocean waves crashing on rocky shore, powerful and rhythmic"
- "Footsteps on wooden floor, slow and deliberate"
- "Wind howling through trees, eerie and continuous"

**Avoid**:
- Multiple unrelated sounds in one prompt (create separate requests)
- Vague descriptions: "some noise"
- Impossible sounds: "purple sounding like Tuesday"

### Text-to-Speech Tips
**Good Practices**:
- Write as you would naturally speak
- Use punctuation to control pacing: periods for pauses, commas for breath
- Spell out numbers and abbreviations for clarity
- Test pronunciation of brand names or technical terms
- Break very long text into logical segments

**Example Text Formatting**:
```
Good: "Welcome to our platform. Let me show you around."
Better: "Welcome to our platform... Let me show you around."
(Extra pause with ellipsis)

Good: "Call 1-800-555-0123"
Better: "Call one, eight hundred, five five five, zero one two three"
(For natural pronunciation)
```

### Video Soundtrack Prompts
**Structure**: `[Style/Genre] + [Mood] + [Optional: pacing/energy]`

**Good Examples**:
- "Upbeat travel music, adventurous and inspiring"
- "Corporate presentation music, professional and modern"
- "Emotional documentary score, contemplative and moving"
- "High-energy sports highlight music, intense and exciting"

**Avoid**:
- Over-specifying video content (API analyzes this)
- Conflicting with video mood (let video analysis guide)
- Too generic: "background music" (add style/mood)

---

## Error Handling

**Common Errors**:
- `400`: Invalid parameters (check duration ranges, text length)
- `401`: Authentication failed
- `413`: Video file too large (>200M)
- `422`: Invalid video format or text encoding
- Task status `4`: Generation failed (check prompt or input)

**Best Practices**:
- Validate duration is within allowed range
- Ensure video URLs are publicly accessible
- Keep text under 5000 characters for TTS
- Test prompts with shorter durations first
- Implement retry logic with exponential backoff

---

## Output Format

All audio APIs return:
- **Format**: MP3 (lossy compression)
- **Sample Rate**: 44.1kHz or 48kHz
- **Bitrate**: 128-320 kbps (varies by API)
- **Channels**: Stereo (2 channels)

For professional use, you may want to post-process:
- Normalize volume levels
- Apply EQ/mastering
- Trim silence
- Convert to other formats if needed

---

## Quota and Limits

- Concurrent tasks: Check your plan
- File size limits: <200M for video inputs
- Text length: Max 5000 characters for TTS
- Duration limits: See table above per API
- Generation time: Typically 10s - 3min depending on API and duration

---

## Use Case Combinations

### Complete Video Production
```python
# 1. Generate video
video_task = client.text_to_video(
    prompt="Product showcase on white background"
)
video_result = client.poll_until_complete(video_task)
video_url = json.loads(video_result['result'])['video_path'][0]

# 2. Generate voiceover
speech_task = client.text_to_speech(
    text="Introducing our revolutionary new product..."
)
speech_result = client.poll_until_complete(speech_task)
speech_url = json.loads(speech_result['result'])['audio_path'][0]

# 3. Generate background music
music_task = client.video_soundtrack(
    video=video_url,
    prompt="Upbeat modern tech music"
)
music_result = client.poll_until_complete(music_task)
music_url = json.loads(music_result['result'])['audio_path'][0]

# 4. Mix audio tracks (use external tool like ffmpeg)
```

### Podcast Production
```python
# Generate intro music
intro_task = client.text_to_music(
    prompt="Podcast intro jingle, energetic and catchy",
    duration=10
)

# Generate main content speech
content_task = client.text_to_speech(
    text="Welcome to episode 42...",
    voice_id="en-US-GuyNeural"
)

# Generate outro music
outro_task = client.text_to_music(
    prompt="Podcast outro, fade-out style",
    duration=15
)
```

### Game Audio Assets
```python
# Background ambience
ambience = client.text_to_sound_effect(
    prompt="Medieval tavern atmosphere with crowd chatter",
    duration=120
)

# UI sounds
click_sound = client.text_to_sound_effect(
    prompt="UI button click, soft and satisfying",
    duration=1
)

# Character voice
npc_voice = client.text_to_speech(
    text="Greetings, traveler! What brings you here?",
    voice_id="en-US-GuyNeural"
)
```
