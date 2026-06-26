---
name: travel-grid-generator
description: "Generate a 3x3 grid (9-square) travel blogger style collage based on user photos and a specific destination. Use for: creating social media style travel photos, maintaining character consistency across multiple scenes, and generating realistic iPhone-style travel snapshots. Trigger: when user says '九宫格', 'travel grid', '旅行照片', '生成旅行照', or provides photos with a destination."
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/qclaw/travel-grid-generator
    requires:
      tools:
        - generate_image
---

# Travel Grid Generator

Generate high-quality, character-consistent 3x3 travel photo grids in "Travel Blogger" style.

## When to Use

User triggers this skill when they:
- Upload photos and mention a destination
- Say "用 travel-grid-generator 生成一张去[目的地]的九宫格"
- Request "九宫格旅行照" or "travel grid photos"

## Workflow

### Step 1: Analyze User Photos

When user uploads photos:
1. **Identify key facial features**: face shape, eye shape, nose, lips, skin tone
2. **Note hairstyle and hair color**: essential for consistency
3. **Capture temperament/persona**: natural, relaxed, energetic, etc.
4. **Describe the "Travel Blogger" persona**: young, natural, pretty, relaxed, and smiling

### Step 2: Determine Destination

Get the destination from user input. If not specified, ask:
- "请问您想去哪个目的地？例如：京都、伦敦、土耳其、巴黎、纽约..."

### Step 3: Research Destination Landmarks

**IMPORTANT**: Before generating, search for 9 iconic locations/landmarks at the destination:

1. Use `web_search` to find: "{destination} 必去景点" or "{destination} top attractions Instagram spots"
2. Select 9 diverse locations:
   - 2-3 iconic landmarks (must-see spots)
   - 2-3 street/neighborhood scenes (local vibe)
   - 1-2 cafe/restaurant scenes (lifestyle)
   - 1-2 nature/outdoor scenes (if applicable)
   - 1 evening/night scene (for variety)

3. Create a scene list with specific poses and expressions for each

### Step 4: Construct Prompt

Use the template below. Fill in:
- Character description from Step 1
- 9 scenes from Step 3
- Photography style parameters

### Step 5: Execute Generation

Call `generate_image` with:
```
aspect_ratio: "1:1"
model: "gpt-image-2"
```

## Prompt Engineering Framework

### Character Description Template

```
CHARACTER (MUST MAINTAIN STRICTLY):
- Same person from reference image in ALL 9 frames
- Face: [face shape], [eye shape], [nose], [lips], [skin tone]
- Hair: [color], [length], [style]
- Expression: Natural smile, relaxed demeanor
- Style: Travel blogger aesthetic - casual, trendy, comfortable
- Outfit: Appropriate for [destination] and [season]
```

### Photography Style Parameters

```
PHOTOGRAPHY STYLE:
- Camera: iPhone snapshot / Fujifilm film camera style
- Quality: Low clarity, slight motion blur acceptable
- Lighting: Natural lighting, sometimes slightly overexposed
- Composition: Casual, candid, not perfectly framed
- Vibe: Real-life memory, travel diary snapshot, NOT professional commercial photography
- Color: Natural tones, avoid over-saturation
```

### Grid Structure Template

```
3x3 GRID LAYOUT (9 frames):

Frame 1 (Top-left): [Location] - [Pose] - [Expression]
Frame 2 (Top-center): [Location] - [Pose] - [Expression]
Frame 3 (Top-right): [Location] - [Pose] - [Expression]
Frame 4 (Middle-left): [Location] - [Pose] - [Expression]
Frame 5 (Center): [Location] - [Pose] - [Expression]
Frame 6 (Middle-right): [Location] - [Pose] - [Expression]
Frame 7 (Bottom-left): [Location] - [Pose] - [Expression]
Frame 8 (Bottom-center): [Location] - [Pose] - [Expression]
Frame 9 (Bottom-right): [Location] - [Pose] - [Expression]
```

### Full Prompt Template

```
Generate a 3x3 grid image (9 frames arranged in a square) featuring the same person in different travel scenes at [DESTINATION].

[CHARACTER DESCRIPTION FROM STEP 1]

PHOTOGRAPHY STYLE:
- iPhone snapshot aesthetic, casual and candid
- Natural lighting, slight overexposure acceptable
- Low clarity, minimal post-processing
- Real-life memory feel, travel diary style
- NOT professional commercial photography

9 SCENES:

1. [Scene 1 details with location, pose, expression]
2. [Scene 2 details]
3. [Scene 3 details]
4. [Scene 4 details]
5. [Scene 5 details]
6. [Scene 6 details]
7. [Scene 7 details]
8. [Scene 8 details]
9. [Scene 9 details]

CONSTRAINTS:
- MUST be the SAME PERSON in all 9 frames with identical facial features
- No deformed limbs, fingers, or AI artifacts
- No westernization or generic template faces
- Realistic outfits appropriate for [destination] and season
- Each frame should feel like a genuine iPhone photo memory
- Maintain travel blogger aesthetic throughout
```

## Pose & Expression Variety

Mix these across the 9 frames:

**Poses:**
- Selfie (close-up)
- Walking towards camera
- Walking away (back view)
- Looking back over shoulder
- Sitting at cafe
- Standing with landmark
- Candid laugh
- Profile shot
- Looking at scenery (not camera)

**Expressions:**
- Natural smile
- Laughing
- Thoughtful/contemplative
- Excited/happy
- Relaxed/calm
- Looking away

## Constraints Checklist

Before generating, verify:
- [ ] Character features explicitly described
- [ ] 9 distinct scenes with specific locations
- [ ] Varied poses across frames
- [ ] Varied expressions
- [ ] Photography style parameters set
- [ ] Season-appropriate outfits
- [ ] Destination-appropriate settings

## Output

After generation:
1. Present the image to user
2. Optionally save to a designated folder if requested
3. Offer to regenerate specific frames if needed

## Example Usage

**User**: *uploads photo* "用 travel-grid-generator 生成一张去巴黎的九宫格"

**Agent**:
1. Analyze photo features
2. Search "Paris top Instagram spots attractions"
3. Select 9 locations: Eiffel Tower, Louvre, Montmartre, Seine River, cafe scene, Marais district, Champs-Élysées, Sacré-Cœur, evening Seine cruise
4. Build prompt with character description + 9 scenes
5. Call generate_image with aspect_ratio: "1:1", model: "gpt-image-2"
6. Present result

## References

See `references/destinations.md` for pre-built scene templates for popular destinations.
