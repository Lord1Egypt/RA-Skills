# Tomoviee Prompt Engineering Guide

## Overview
This guide provides structured prompt formulas and best practices for all Tomoviee AI APIs to achieve optimal generation results.

---

## Video APIs

### Text-to-Video Prompt Formula
```
主体(描述) + 运动 + 场景(描述) + (镜头语言 + 光影 + 氛围)
Subject (description) + Motion + Scene (description) + (Camera + Lighting + Atmosphere)
```

**Component Breakdown**:

1. **Subject (主体)**: Main focus of the video
   - Who/what is in the scene
   - Key characteristics, appearance
   - Position and pose

2. **Motion (运动)**: Action and movement
   - What the subject is doing
   - Speed and direction of movement
   - Dynamic elements

3. **Scene (场景)**: Environment and context
   - Location and setting
   - Background elements
   - Time of day/season

4. **Camera (镜头语言)**: Optional camera work
   - Camera angle (wide, close-up, aerial, etc.)
   - Camera movement (pan, zoom, tracking, etc.)
   - Or specify `camera_move_index` parameter

5. **Lighting (光影)**: Optional lighting style
   - Natural/artificial light
   - Time of day (golden hour, blue hour, etc.)
   - Light direction and quality

6. **Atmosphere (氛围)**: Optional mood and tone
   - Overall feeling (dramatic, peaceful, energetic)
   - Color palette/grading
   - Weather/environmental effects

**Examples**:

**Minimal** (Subject + Motion + Scene):
```
"A red sports car driving fast on a coastal highway at sunset"
```

**Standard** (+ Camera + Lighting):
```
"A red sports car speeding along a winding coastal highway at golden hour, 
camera following from the side, warm orange sunlight reflecting off the car"
```

**Detailed** (+ Atmosphere):
```
"A sleek red Ferrari speeding along a dramatic coastal highway carved into cliffs, 
camera tracking smoothly from the side at car level, 
golden hour sunset casting long shadows and warm orange glow, 
cinematic and epic atmosphere with ocean waves crashing below"
```

**More Examples by Use Case**:

**Product Showcase**:
```
"White wireless headphones slowly rotating on a minimalist white surface, 
studio lighting with soft shadows, clean and modern atmosphere"
```

**Nature/Travel**:
```
"Majestic waterfall cascading down mossy rocks in a lush rainforest, 
slow zoom in from wide to medium shot, 
dappled sunlight filtering through the canopy, 
serene and peaceful atmosphere"
```

**Action/Sports**:
```
"Professional skateboarder performing a kickflip on urban street ramp, 
slow motion capture from low angle, 
bright daylight with high contrast shadows, 
energetic and dynamic atmosphere"
```

### Image-to-Video Prompt Formula
```
主体 + 运动 + 镜头语言
Subject + Motion + Camera
```

**Why simpler?** The image already provides:
- Scene and environment
- Lighting and color palette
- Composition and framing
- Atmosphere and mood

**Your prompt should focus on**:
- Motion to add to the static image
- Camera movement to apply
- Any new dynamic elements

**Examples**:

```
"Camera slowly zooming in, subject's hair gently blowing in the wind"
```

```
"Slow pan from left to right, leaves rustling, golden hour lighting"
```

```
"Camera orbiting around the subject, dramatic lighting, cinematic feel"
```

```
"Gentle push in toward the subject's face, bokeh background, emotional atmosphere"
```

### Video Continuation Prompt Formula
```
延续的动作 + 场景变化 + 镜头延续
Continued action + Scene evolution + Camera continuation
```

**Focus on**:
- How the action continues from the last frame
- Natural progression of movement
- Scene changes or transitions
- Camera movement consistency

**Examples**:

```
"The bird continues flying higher, soaring into the clouds, 
camera following the ascent"
```

```
"The car continues down the road, passing through a tunnel, 
maintaining tracking shot"
```

```
"The person continues walking, entering a brightly lit room, 
camera follows smoothly"
```

---

## Image APIs

### Image-to-Image Prompt Formula
```
参考图描述 + 保留要素 + 修改/新增指令
Reference description + Elements to preserve + Modifications/additions
```

**Component Breakdown**:

1. **Reference Description**: What's in the original image
2. **Preserve**: Explicitly state what to keep unchanged
3. **Modify/Add**: What to change or add

**Examples**:

```
"A woman in business attire at a modern office, 
preserve facial features and body pose, 
change background to outdoor garden with natural lighting, 
add warm sunset atmosphere"
```

```
"Portrait of a man wearing a blue shirt, 
keep facial features and expression, 
change clothing to formal black suit with tie, 
maintain studio lighting"
```

```
"Kitchen interior with white cabinets, 
preserve layout and appliance positions, 
change color scheme to navy blue cabinets with gold hardware, 
add marble countertops"
```

### Image Redrawing Prompt Formula
```
替换区域的新内容描述
Description of what replaces the masked area
```

**Focus on**:
- What should appear in the masked region
- Style/texture matching surrounding areas
- Lighting consistency
- Natural integration

**Examples**:

```
"Clear blue sky with white fluffy clouds"
(for replacing background)
```

```
"Natural grass texture with small wildflowers"
(for replacing foreground)
```

```
"Modern glass windows with reflections of cityscape"
(for replacing building facade)
```

```
"Empty wooden table surface with subtle wood grain"
(for removing objects from table)
```

### Image Recognition Prompt Formula
```
要识别的对象/区域描述
Description of objects/regions to identify
```

**Focus on**:
- Clear object identification
- Specific vs. general (depending on need)
- Spatial context if helpful

**Examples**:

```
"person" / "all people"
```

```
"the red car in the foreground"
```

```
"sky and clouds"
```

```
"text and logos"
```

```
"background behind the main subject"
```

---

## Audio APIs

### Text-to-Music Prompt Formula
```
主体 + 场景(氛围/风格)
Subject/Theme + Scene (Atmosphere/Style)
```

**Component Breakdown**:

1. **Subject/Theme**: Purpose or topic of the music
2. **Atmosphere**: Mood and emotional quality
3. **Style/Genre**: Musical style and genre
4. **Instruments** (optional): Key instruments to feature

**Examples**:

**Simple**:
```
"Upbeat electronic music, energetic and modern"
```

**Standard**:
```
"Corporate presentation background music, professional and clean, 
soft piano and ambient synth"
```

**Detailed**:
```
"Epic cinematic orchestral score, dramatic and heroic, 
soaring strings and powerful brass, 
Hans Zimmer style, for action scene"
```

**By Genre**:

**Electronic/Pop**:
```
"Energetic EDM track, festival atmosphere, heavy bass and synth drops"
```

**Jazz**:
```
"Smooth jazz for evening ambience, sophisticated and relaxed, 
piano trio with double bass"
```

**Orchestral**:
```
"Emotional film score, contemplative and moving, 
piano and string ensemble"
```

**Ambient**:
```
"Peaceful meditation music, calm and spacious, 
soft pads and gentle chimes"
```

### Text-to-Sound-Effect Prompt Formula
```
声音来源 + 动作/环境 + 特征
Sound source + Action/Context + Characteristics
```

**Component Breakdown**:

1. **Sound Source**: What's making the sound
2. **Action/Context**: What's happening / where it is
3. **Characteristics**: Sound qualities (loud, soft, sharp, etc.)

**Examples**:

**Single Events**:
```
"Glass bottle shattering on concrete, sharp and crisp"
```

```
"Car door closing, solid thunk, reverb in garage"
```

```
"Notification bell sound, soft and pleasant"
```

**Continuous Sounds**:
```
"Heavy rain on metal roof, steady and rhythmic"
```

```
"City traffic ambience, cars passing, distant sirens"
```

```
"Forest birds chirping, peaceful morning atmosphere"
```

**By Category**:

**Nature**:
```
"Ocean waves crashing on beach, powerful and continuous"
```

**Mechanical**:
```
"Old typewriter keys typing, mechanical clicks and dings"
```

**Human**:
```
"Crowd cheering and applauding, enthusiastic and loud"
```

**UI/Digital**:
```
"Futuristic UI beep, high-tech and clean"
```

### Text-to-Speech Tips

**Structure**:
- Write naturally as you would speak
- Use punctuation for pacing and pauses
- Spell out numbers and abbreviations

**Examples**:

**With Pacing**:
```
"Welcome to our platform... Let me show you around."
(Ellipsis adds natural pause)
```

**With Emphasis**:
```
"This is extremely important. Pay close attention."
(Period creates strong pause for emphasis)
```

**Numbers**:
```
"Call one, eight hundred, five five five, zero one two three"
(Instead of "Call 1-800-555-0123")
```

### Video Soundtrack Prompt Formula
```
风格/类型 + 情绪 + (节奏/能量)
Style/Genre + Mood + (Optional: pacing/energy)
```

**Why simpler?** The API analyzes video content automatically.

**Examples**:

**Minimal** (let API analyze):
```
(no prompt - fully automatic based on video)
```

**Guided Style**:
```
"Upbeat travel vlog music, adventurous and inspiring"
```

```
"Corporate tech presentation music, modern and professional"
```

```
"Emotional documentary score, contemplative and moving"
```

---

## General Best Practices

### Do's ✅

1. **Be Specific**: Clear descriptions yield better results
   - Good: "Golden retriever puppy playing with red ball"
   - Bad: "Dog playing"

2. **Use Descriptive Adjectives**: Add relevant details
   - Good: "Sleek modern smartphone with edge-to-edge display"
   - Bad: "Phone"

3. **Specify Mood/Atmosphere**: Set the tone
   - Good: "Dramatic sunset with vibrant orange and purple clouds"
   - Bad: "Sunset"

4. **Include Context**: Where, when, why
   - Good: "Professional product photography on white background"
   - Bad: "Product"

5. **Mention Key Visual Elements**:
   - Lighting conditions
   - Color palette
   - Composition style
   - Movement characteristics

### Don'ts ❌

1. **Don't Be Vague**:
   - Bad: "Nice video"
   - Bad: "Good music"
   - Bad: "Cool image"

2. **Don't Contradict**:
   - Bad: "Bright and dark scene"
   - Bad: "Fast and slow motion"
   - Bad: "Happy sad music"

3. **Don't Over-specify Technical Details**:
   - Bad: "1920x1080 resolution 24fps H.264 codec"
   - Bad: "120 BPM in C major with I-V-vi-IV progression"
   - (API handles technical parameters automatically)

4. **Don't Use Negations**:
   - Bad: "Not blurry, not dark, not boring"
   - Good: "Sharp, bright, engaging"

5. **Don't Mix Multiple Unrelated Concepts**:
   - Bad: "Cat playing piano in space while cooking pasta"
   - Better: Split into multiple generations or choose one focus

---

## Advanced Techniques

### Chaining Outputs

Use output from one API as input to another:

```python
# 1. Generate image
img_task = client.image_to_image(
    prompt="Modern office space, clean and minimal",
    image="reference.jpg"
)
img_url = get_result_url(img_task)

# 2. Animate image
video_task = client.image_to_video(
    prompt="Camera slowly panning right, golden hour lighting",
    image=img_url
)
video_url = get_result_url(video_task)

# 3. Add soundtrack
audio_task = client.video_soundtrack(
    video=video_url,
    prompt="Professional corporate music"
)
```

### Iterative Refinement

1. **Start Simple**: Test with minimal prompt
2. **Evaluate Output**: What's missing or wrong?
3. **Add Details**: Incrementally add specificity
4. **Test Again**: Compare results

**Example Iteration**:
```
V1: "Car driving"
→ Too generic

V2: "Red sports car driving fast on highway"
→ Better, but lighting unclear

V3: "Red Ferrari speeding on coastal highway, golden hour sunset, dramatic"
→ Good result!
```

### A/B Testing

Generate multiple variations to compare:

```python
# Test different camera movements
variants = [
    client.image_to_video(image=img, prompt="Slow zoom in", camera_move_index=5),
    client.image_to_video(image=img, prompt="Pan right", camera_move_index=12),
    client.image_to_video(image=img, prompt="Orbit around subject", camera_move_index=23)
]
```

### Consistency Across Assets

For cohesive content, maintain consistent prompt elements:

```python
# Consistent style keywords across multiple generations
style_guide = "cinematic, golden hour lighting, dramatic atmosphere"

video1 = client.text_to_video(f"Mountain landscape, {style_guide}")
video2 = client.text_to_video(f"Forest scene, {style_guide}")
video3 = client.text_to_video(f"Beach sunset, {style_guide}")
```

---

## Prompt Templates by Use Case

### Marketing/Commercial
```
"[Product name] showcased on [surface/background], 
[camera movement], 
studio lighting with soft shadows, 
premium and elegant atmosphere"
```

### Social Media
```
"[Subject] [action], 
[camera angle/movement], 
vibrant colors and high energy, 
engaging and eye-catching for [platform]"
```

### Documentary/Educational
```
"[Subject] in [environment], 
[natural action], 
natural documentary style cinematography, 
informative and authentic atmosphere"
```

### Artistic/Creative
```
"[Abstract concept] visualized as [imagery], 
[unique camera work], 
[lighting style], 
[artistic mood/style reference]"
```

---

## Troubleshooting

### Problem: Output doesn't match prompt
**Solutions**:
- Simplify prompt to core elements
- Remove contradictory instructions
- Be more specific about key aspects
- Check for typos or ambiguous terms

### Problem: Output quality is poor
**Solutions**:
- Add style keywords (cinematic, professional, high quality)
- Specify lighting conditions
- Mention camera quality/style
- Add atmosphere/mood descriptors

### Problem: Inconsistent results
**Solutions**:
- Use more specific prompts
- Reference specific styles or examples
- Test with variations to find optimal wording
- Use consistent style keywords across generations

### Problem: Generation fails (status=4)
**Solutions**:
- Check prompt for inappropriate content
- Simplify overly complex prompts
- Verify input files (images/videos) are valid
- Ensure parameters are within valid ranges
- Try with default parameters first

---

## Language Considerations

Tomoviee supports both **Chinese** and **English** prompts.

**Tips**:
- Use language you're most comfortable with
- Be aware of cultural/contextual nuances
- Technical terms may work better in English
- Artistic descriptions may vary by language interpretation

**Example Comparisons**:

Chinese:
```
"一只金毛寻回犬在阳光明媚的草地上奔跑,镜头跟随,电影级画质"
```

English:
```
"A golden retriever running through a sunlit meadow, camera following, cinematic quality"
```

Both can produce excellent results - choose based on your fluency and precision needs.

---

## Summary Checklist

Before submitting your prompt, verify:

- [ ] **Clear Subject**: What's the main focus?
- [ ] **Specific Action**: What's happening?
- [ ] **Scene Context**: Where is this taking place?
- [ ] **Visual Style**: What's the look and feel?
- [ ] **Technical Parameters**: Resolution, duration, aspect ratio set correctly?
- [ ] **No Contradictions**: All elements work together?
- [ ] **Appropriate Specificity**: Not too vague, not over-specified?

A well-crafted prompt is the foundation of excellent AI-generated content. Take time to refine your prompts for best results!
