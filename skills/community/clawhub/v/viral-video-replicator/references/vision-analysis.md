# Vision LLM Analysis

> **Role:** Defines Vision LLM system/user prompts and output schemas for video analysis (exact + rewrite modes).
> Load at: Step 4 (analyzing video frames). The prompts here are sent to the Vision API, not used as direct answers.
> It does NOT replace execution — always call the Vision API with frame grids, never fabricate analysis from training data.

## Two Analysis Modes

### 1. Exact Mode (reverse_video.py) — Nested structured analysis

**System Prompt:**
> 你是视频逆向分析专家。你的任务是从视频关键帧中提取能够 100% 复制该视频的所有参数。你的输出将被直接用于 Seedance 2.0 视频生成提示词。精确度是唯一标准——不要概括、不要美化、不要推断"应该是什么"，只描述"实际看到了什么"。

**10-field output schema:**
1. person: {gender, age_range, face, skin_tone, hair, build, makeup}
2. clothing: {type, color, pattern, material_look, neckline, sleeve, length, fit, details, accessories}
3. scene: {location, background_objects, floor, wall, lighting_source, color_temperature, overall_tone}
4. actions: timeline string (每1-2秒一个节点, must specify left/right hand)
5. dialogue: transcript with embedded action markers, preserve filler words
6. camera: {movement_type, orientation, timeline}
7. audio: {has_speech, speech_style, background_sounds, music, overall_audio_mix}
8. video_type: string
9. duration_seconds: {actual, recommended}
10. people_count: int

### 2. Rewrite Mode (video_analyzer.py) — Flat analysis for viral logic

**System Prompt:**
> 你是 Seedance 2.0 提示词逆向工程专家。根据视频关键帧和音频转录（如有），推理出能生成类似视频的 Seedance 2.0 提示词参数。

**10-field flat output:**
1. gender: male/female
2. scene: 2-3 sentences
3. clothing: 2-3 sentences
4. actions: timeline with台词时间对齐, 固定右手
5. dialogue: transcript with action markers
6. camera: movement + composition + framing changes
7. dialogue_style: one sentence description
8. video_type: string
9. has_speech: bool
10. duration_seconds: 5 or 10

## Vision API Call

```
POST {ARK_API_BASE}/api/v3/chat/completions
Headers:
  Authorization: Bearer {ARK_API_KEY}
  Content-Type: application/json
Body:
  model: {ARK_VISION_MODEL}
  messages:
    - role: system, content: system_prompt
    - role: user, content: [text_prompt, image_url(grid1), image_url(grid2), ...]
  temperature: 0.3
  max_tokens: 4096
Timeout: 120s
```

Image format: `data:image/jpeg;base64,{grid_base64}`

## JSON Parsing

Strip markdown code fences if present:
```python
if stripped.startswith("```"):
  stripped = stripped.split("\n", 1)[1].rsplit("```", 1)[0]
```
