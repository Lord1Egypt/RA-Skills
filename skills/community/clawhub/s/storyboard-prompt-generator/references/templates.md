# Prompt Template Library

## Character Prompt Templates

### Basic Template
```
[Character identity], [age], [gender], [body type], [hair style color], [facial features], [eye color shape], [clothing], [pose], [expression], [emotion], [accessories], [scene location], [art style], [quality keywords]
```

### Complete Example
```
anime protagonist, 17 years old, male, athletic build, short messy black hair with blue highlights, sharp facial features, determined golden eyes, wearing black school uniform with white collar, arms crossed, confident smile, heroic aura, silver necklace, standing on school rooftop, anime style, cinematic lighting, 8k, masterpiece
```

### Variant Templates

**Standing Illustration Template:**
```
[Character name], character design sheet, multiple angles, front view, side view, back view, [appearance description], [clothing], white background, reference sheet, anime style, clean lines
```

**Expression Reference Template:**
```
[Character name], expression sheet, multiple expressions, happy, sad, angry, surprised, embarrassed, [appearance], [clothing], white background, anime style, detailed face
```

**Action Reference Template:**
```
[Character name], action pose reference, dynamic pose, [specific action], [appearance], [clothing], motion blur, action lines, anime style, dramatic angle
```

---

## Scene Prompt Templates

### Basic Template
```
[Scene type], [location], [time], [weather/atmosphere], [main elements], [detail elements], [lighting], [perspective], [art style], [quality keywords]
```

### Complete Example
```
Japanese high school classroom, desks arranged in rows, afternoon sunlight streaming through windows, dust particles floating in light, chalkboard at front, cherry blossoms visible outside window, nostalgic atmosphere, golden hour lighting, wide angle shot, anime style, Makoto Shinkai style, detailed background, 4k
```

### Variant Templates

**Indoor Scene:**
```
[indoor type], [furnishings], [light source], [atmosphere mood], [detail decorations], interior design, [perspective], anime style, detailed
```

**Outdoor Scene:**
```
[location type], [natural elements], [architectural elements], [time/weather], [season], [atmosphere], landscape, [composition], anime style, cinematic
```

**Fantasy Scene:**
```
[fantasy location], [supernatural elements], [magic effects], [fantastical creatures], [mysterious atmosphere], fantasy world, magical glow, ethereal lighting, [art style], highly detailed
```

---

## Sora Video Prompt Templates

### Basic Template
```
A [subject description] [action description] in [scene description], [camera movement], [duration suggestion], [lighting], [atmosphere mood], [video quality/style]
```

### Complete Example
```
A young anime girl with long black hair walking slowly through a sunlit forest, camera following from behind, dappled sunlight filtering through leaves, peaceful morning atmosphere, 8 seconds, anime style video, smooth motion, cinematic quality, 16:9 aspect ratio
```

### Camera Movement Templates

**Tracking Shot:**
```
[subject] [action], camera following from [direction], tracking shot, smooth motion, [environment], [duration]s
```

**Push In:**
```
[subject] [action], camera slowly pushing in towards [target], dramatic reveal, [environment], [duration]s
```

**Orbit Shot:**
```
[subject] [action], camera orbiting around subject, 360 degree rotation, [environment], [duration]s
```

**Static Shot:**
```
[subject] [action], static camera, slight movement from subject only, [environment], [duration]s
```

### Action Sequence Templates

**Walking:**
```
[character] walking [direction/manner], [emotion] expression, natural walking motion, [environment], [camera], [duration]s
```

**Running:**
```
[character] running [direction], hair and clothes flowing, dynamic motion, [emotion], [environment], tracking shot, [duration]s
```

**Dialogue:**
```
[character A] and [character B] talking to each other, [emotion], subtle body language and hand gestures, [environment], over the shoulder shot, [duration]s
```

**Emotional Expression:**
```
[character] [expression change], subtle micro expressions, [emotion] mood, close-up shot, shallow depth of field, [duration]s
```

---

## Standard Storyboard Prompt Templates

### Basic Template
```
[Shot type] storyboard, [composition], [subject description], [action state], [emotional tone], [camera angle], line art, manga style, black and white, [aspect ratio]
```

### Complete Example
```
特写分镜, close-up, 中心构图, anime girl face close-up, tears streaming down cheeks, deep sadness and heartbreak, slight low angle, manga style line art, detailed eyes, screentone shading, 16:9
```

### Shot Type Templates

**Wide Shot Storyboard:**
```
远景分镜, establishing shot, [full environment], [subject position], [atmosphere], wide composition, manga style, 16:9
```

**Medium Shot Storyboard:**
```
中景分镜, medium shot, [upper body of character], [action], [expression], narrative focus, manga style, 16:9
```

**Close-up Storyboard:**
```
特写分镜, close-up, [facial features], [expression details], [emotion], [angle], detailed, manga style, 16:9
```

**Action Storyboard:**
```
动作分镜, action panel, [character], [dynamic action], speed lines, impact frame, dynamic angle, manga style, diagonal composition
```

---

## Negative Prompts Reference

### Universal Negative Words
```
low quality, worst quality, bad quality, blurry, pixelated, distorted, deformed, ugly, bad anatomy, bad proportions, extra limbs, missing limbs, floating limbs, disconnected limbs, mutation, mutated, watermark, signature, text, username, artist name, logo, cropped, out of frame, worst face, bad face, deformed face
```

### Scene-Specific Negative Words
```
simplified, plain background, low detail, empty, uninspiring, generic, stock photo look
```

### Character-Specific Negative Words
```
bad hands, missing fingers, extra fingers, malformed hands, bad eyes, crossed eyes, deformed eyes, bad hair, flat color, amateur
```

### Video-Specific Negative Words
```
static, stuck, frozen, glitching, jittery, discontinuous motion, morphing, distortion, flickering, noise
```

---

## Batch Generation Format

### Multi-Panel Storyboard Input Format
```
Shot No.: [number]
Shot Type: [wide/medium/close-up etc.]
Description: [storyboard description]
Action: [character action]
Emotion: [emotional tone]
---
```

### Batch Output Format
```
## Shot No. [number] - [Shot Type]

**Type**: [Character/Scene/Sora/Storyboard]

**Prompt**:
[Generated prompt]

**Negative Prompt** (if applicable):
[Negative prompt]

---