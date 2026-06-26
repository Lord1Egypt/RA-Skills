# Comic Image Prompt Rules

Images must look like a comic page. All conversation use Chinese.

## Character Selection (Fixed Trio)

**Use only these 3 core characters for consistency:**

1. **Doctor** — Tactical commander, main instructor
   - Appearance: Black tactical coat with hood/mask, mysterious appearance
   - Role: Delivers core knowledge and explanations

2. **Amiya** — Assistant operator, learner perspective
   - Appearance: Brown hair with rabbit ears, Rhodes Island uniform, holding tablet
   - Role: Asks questions, expresses curiosity, represents audience

3. **Kal'tsit** — Medical/technical expert
   - Appearance: Green hair with cat ears, white lab coat, professional demeanor
   - Role: Explains technical details, security concerns, complex mechanisms

**DO NOT use**: Rosmontis, Blaze, or other secondary characters (AI recognition unreliable)

---

Requirements:

anime style
Arknights game characters (Amiya, Kal'tsit, Doctor ONLY)
tactical operator theme
comic panels
clean line art
educational storytelling
Chinese language
speech bubbles with actual Chinese text visible
visual consistency across all images

---

# Prompt Template

Use this structure.

Arknights-inspired anime comic page,
Rhodes Island research lab environment,
multiple comic panels,
educational explanation,
speech bubbles containing Chinese text,
clean line art,
detailed background,
Chinese language

Scene description:

{panel_summary}

---

# Panel Description Format

Each panel must include specific Chinese dialogue:

Panel X:
- Scene: [location/setting]
- Action: [what characters are doing]
- Dialogue:
  - Character A: "具体的中文对话内容"
  - Character B: "具体的中文回应内容"

---

# Critical Requirements

## 1. Chinese Text in Speech Bubbles

**MANDATORY**: Every speech bubble must contain actual Chinese text, not empty space.

Correct example:
```
Panel 1: Doctor pointing at screen saying "阿米娅，人工智能正在快速改变我们的生活方式", Amiya looking curious asking "博士，那人工智能是如何学习新知识的？"
```

Incorrect example:
```
Panel 1: Doctor explaining to Amiya, speech bubbles for Chinese dialogue
```

## 2. Complete Dialogue Chains

Each image should tell a complete mini-story with:
- Question/answer pattern
- Information delivery
- Natural conversation flow

## 3. Character Voice Guidelines

**Doctor**: Professional, authoritative, knowledgeable
- Uses terms like: "根据情报显示...", "核心问题在于...", "从战略角度分析..."

**Amiya**: Curious, eager to learn, thoughtful
- Uses terms like: "原来如此...", "那这意味着...", "我有点担心..."

---

# Visual Consistency (Input-Image Method)

To maintain visual continuity across all comic pages:

## Step 1: Generate Base Image
Generate the first image (comic_1.png) normally with full prompt.

## Step 2: Use Input-Image for Subsequent Pages
For images 2-6, use `--input-image` pointing to the FIRST image:

```bash
# Image 1: Normal generation
uv run ... --prompt "full description" --filename "comic_1.png"

# Images 2-6: Reference image 1 for consistency
uv run ... \
  --input-image "/path/to/comic_1.png" \
  --prompt "Continue the comic scene... [specific panel descriptions]" \
  --filename "comic_2.png"
```

**Why this works:**
- AI references the art style, color palette, and character designs from image 1
- Maintains consistent lighting and background aesthetic
- Characters look the same across all pages

## Step 3: Prompt Adjustments for Input-Image
When using input-image, modify prompt:
- Start with: "Based on the reference image style..."
- Describe scene changes: "Same characters in different poses..."
- Keep core descriptors: "same anime style, same lighting, continuing the story"

---

# Visual Consistency Strategy (CRITICAL)

## Method: Input-Image Chain

To maintain visual consistency across all comic pages:

### Step 1: Generate Base Image
Generate the first image (comic_1.png) normally with full detailed prompt.

### Step 2: Chain Generation for Images 2-6
For each subsequent image, use the previous image as input reference:

```bash
# Image 2 uses Image 1 as reference
uv run scripts/generate_image.py \
  --input-image "comic_1.png" \
  --prompt "Continue the comic story, same art style, same character designs..."

# Image 3 uses Image 2 as reference
uv run scripts/generate_image.py \
  --input-image "comic_2.png" \
  --prompt "Continue the comic story, maintaining visual consistency..."
```

### Benefits:
- ✅ Consistent character appearances across all pages
- ✅ Unified color palette and lighting
- ✅ Coherent art style throughout the comic
- ✅ Smooth visual narrative flow

### Important Notes:
- Each image still needs its own complete scene description
- Input-image preserves style, not content (scenes can change)
- Character poses and expressions should vary naturally
- Background can change while maintaining artistic coherence

---

# Image Specifications

## Count
Generate between **5 and 6 images**

Each image must contain multiple panels (3-4 panels recommended).

## Aspect Ratio (CRITICAL)
**Use portrait orientation 9:16 for all images**

This matches Xiaohongshu's mobile app reading experience.

### Why 9:16 Portrait:
- ✅ Optimized for phone screen viewing
- ✅ Better scrolling experience in Xiaohongshu
- ✅ More natural for comic panel layouts
- ✅ Matches platform's content format

### Prompt Addition:
Add to every image prompt:
```
portrait orientation, 9:16 aspect ratio, vertical layout,
optimized for mobile phone viewing,
panels arranged vertically
```

**Generation Order:**
1. Generate comic_1.png (base style)
2. Generate comic_2.png using comic_1.png as input-image
3. Generate comic_3.png using comic_1.png as input-image
4. Continue for all remaining images

---

# Common Mistakes to Avoid

1. ❌ Empty speech bubbles or "space for text"
2. ❌ English text in bubbles when Chinese is required
3. ❌ Vague descriptions like "explaining something"
4. ❌ Missing dialogue content in prompt
5. ❌ Inconsistent character voices

---

# Quality Checklist

Before generating, verify:
- [ ] Each panel has specific Chinese dialogue written out
- [ ] Dialogue matches the educational content
- [ ] Characters speak in consistent voices
- [ ] Conversation flows naturally between panels
- [ ] No placeholder text or empty bubbles