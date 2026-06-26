---
name: storyboard-prompt-generator
description: Parse anime storyboard scripts and generate four types of prompts: character prompts, scene prompts, Sora video generation prompts, and standard storyboard prompts.
---

# Anime Storyboard Prompt Generation

Generate high-quality AI prompts from storyboard scripts, supporting four types: character, scene, Sora video, and standard storyboard.

## Trigger Scenarios

- User provides a storyboard script and requests prompt generation
- User mentions "storyboard prompt", "character prompt", "scene prompt", "Sora prompt", "storyboard description"
- Need to convert storyboard scripts into formats usable by AI generation tools
- Need to learn storyboard prompt writing techniques
- Anime/film storyboard related prompt requirements

## Workflow

```
User inputs storyboard → Identify prompt type → Generate from template → Bilingual output
```

### Type Identification

| Input Characteristics | Recommended Type |
|-----------------------|------------------|
| Character appearance, clothing, expression, pose | Character Prompt |
| Environment, location, atmosphere, lighting | Scene Prompt |
| Action sequences, camera movement, duration | Sora Video Prompt |
| Shot type, composition, line art style | Standard Storyboard Prompt |

---

## I. Character Prompt

### Structure
```
[Identity], [age gender], [body type], [hair style color], [face], [eyes], [clothing], [pose], [expression], [accessories], [scene], [art style], [quality]
```

### Example

**Input:** A girl standing under a cherry blossom tree, gentle wind blowing her long hair, melancholic eyes looking into the distance

**Output:**
```
anime girl, 16 years old, female, slender figure, long flowing black hair, gentle facial features, sad wistful expression, looking into distance, white school uniform with pink ribbon, standing under cherry blossom tree, petals floating in wind, melancholic mood, Makoto Shinkai style, detailed eyes, cinematic lighting, 8k, masterpiece
```

**Key points:** Describe appearance details → Specify clothing details → Capture emotional changes → Add art style and quality keywords

---

## II. Scene Prompt

### Structure
```
[Scene type], [environment], [time], [weather/atmosphere], [main elements], [details], [lighting], [perspective], [art style], [quality]
```

### Example

**Input:** City rooftop at dusk, sunset glow falling on railings, bustling urban night view in the distance

**Output:**
```
urban rooftop scene, Japanese city skyline, golden hour sunset, warm orange pink sky, dramatic lighting, metal railings with golden reflection, distant city lights glowing, modern buildings silhouette, power lines, peaceful evening, wide shot, Makoto Shinkai style, volumetric lighting, detailed background, 4k
```

**Key points:** Specify time setting → Describe lighting effects → Layering (foreground/midground/background) → Use atmospheric vocabulary to enhance emotion

---

## III. Sora Video Prompt

### Structure
```
A [subject] [action] in [scene], [camera movement], [duration], [lighting], [atmosphere], [quality/style]
```

### Example

**Input:** A teenage boy riding a bicycle downhill from a slope, camera following, dusk street

**Output:**
```
A teenage boy riding bicycle downhill on suburban street, wind blowing hair and clothes, camera following from behind and side, dynamic tracking shot, golden hour sunset, Japanese neighborhood with houses and power lines, 10 seconds, shallow depth of field, nostalgic summer atmosphere, anime style video, smooth motion, cinematic, 16:9
```

**Key points:** Action should have a sense of timeline → Specify camera movements (push in/pull out/pan/tilt/track/follow) → Duration 3-15 seconds → One shot, one action for most stability

### Camera Movement Keywords
- Push in: push in, dolly in, camera moving forward
- Pull out: pull out, dolly out, camera moving backward
- Follow: following shot, tracking shot, camera following
- Orbit: orbit shot, arc shot, camera circling around
- Static: static camera, fixed camera position

---

## IV. Standard Storyboard Prompt

### Structure
```
[Shot type] storyboard, [composition], [subject], [action], [emotion], [angle], line art, manga style, [aspect ratio]
```

### Example

**Input:** Close-up shot, protagonist clenching fists, determined expression

**Output:**
```
特写分镜, close-up, 中心构图, anime protagonist face, clenched fists at bottom of frame, determined expression with fiery eyes, strong emotional intensity, dramatic low angle, black and white line art, manga panel, clean lines, screentone shading, 16:9
```

**Key points:** Specify shot type → Note composition method → Emotion affects visual tension → Use line art style for storyboards

### Shot Type Reference
| Chinese | English | Range |
|---------|---------|-------|
| 大远景 | extreme wide shot | Full environment |
| 远景 | wide shot | Full body + environment |
| 全景 | full shot | Full body |
| 中景 | medium shot | Knee up |
| 近景 | medium close-up | Chest up |
| 特写 | close-up | Face |
| 大特写 | extreme close-up | Local detail |

---

## Reference Resources

- [terminology.md](references/terminology.md) - Complete reference of storyboard terminology, camera language, art style keywords
- [templates.md](references/templates.md) - Complete templates for each type, variant templates, negative prompts, batch generation format

---

## Output Specifications

1. **Bilingual parallel**: Chinese and English side by side for better understanding and tool compatibility
2. **Negative prompt suggestions**: Provide negative prompts for image generation
3. **Consistent style**: Keep art style keywords unified within the same project
4. **Aspect ratio suggestions**: 16:9 or 3:2 for images, 16:9 or 9:16 for video

## Batch Processing

Supports batch generation for multiple storyboard panels. Input format:
```
Shot No.: 001
Shot Type: Medium shot
Description: [Storyboard description]
Action: [Character action]
Emotion: [Emotional tone]
---