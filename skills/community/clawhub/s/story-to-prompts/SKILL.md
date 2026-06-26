---
name: story-to-prompts
description: "Convert story synopses or single-scene descriptions into high-quality text-to-image prompts. Two modes: (1) multi-scene - a story outline is split into multiple coherent scenes, each with its own prompt; (2) single-scene - a single scene description gets a prompt directly. Outputs scored prompts with bilingual versions. Use when users say story to images, generate prompts for this scene, story split, storyboard prompts, text-to-image prompt, 文生图, 分镜, 故事拆分."
---

# Story to Prompts

One-shot conversion from story/scene to text-to-image prompts. No interactive confirmation — output the final result directly.

## Output Language

Detect language from user input:
- Chinese input → primary prompt in Chinese, secondary in English
- English input → primary prompt in English, secondary in Chinese
- Explicit language override (e.g. "output in English", "用中文输出") → follow user instruction
- All structural text (titles, character sheets, scene descriptions) matches the primary language

## Entry Point

Determine mode based on user input:

- **Multi-scene mode**: Input contains multiple events/plot points, or user explicitly requests N images
- **Single-scene mode**: Input describes only one scene/画面, or user asks for a prompt for "one scene"

## Split Strategy (Multi-scene Mode)

Priority for determining image count and split:

1. **User specifies count** (e.g. "4 images", "拆成6张") → use directly
2. **User does not specify** → split by spatiotemporal boundaries:
   - Identify distinct time-space units (location change, time jump)
   - Each independent time-space = one image
   - Within the same time-space, if multiple key actions exist, split into 2-3 images with different shot types
3. **Default range**: 3-6 images unless the story is extremely simple or very long

## Workflow (Multi-scene Mode)

Complete all steps in one pass. Output final result only.

### Step 1: Extract Story Baseline

Determine internally (do not output separately):

- Story core (one sentence)
- Character fixed features (age, hair, clothing, signature accessories)
- Unified visual style
- Color palette
- Lighting style

### Step 2: Structure Split

Determine N images, assign for each:

- Shot type (refer to `references/shot-types.md` narrative rhythm template, adjacent images must differ)
- Camera angle
- Narrative function (establishing / progression / climax / resolution)

### Step 3: Generate Prompt per Image

Requirements for each prompt:

- **Repeat character fixed features** in every prompt (consistency)
- **Vary** viewpoint, composition, posture across images (diversity)
- Only include characters/objects mentioned in the current scene (appearance rule)
- Include negative prompt (anti-failure)
- Follow the writing spec below

### Step 4: Score and Optimize

Self-evaluate each prompt on 10 dimensions and optimize:

**Structure Completeness (40 pts)**
1. Core intent clarity (10): Is the goal unambiguous?
2. Subject and hierarchy (10): Is the main subject clear with size ratio?
3. Composition and ratio constraints (10): Aspect ratio, viewpoint, composition technique?
4. Style anchor clarity (10): Specific style/medium specified?

**Generation Quality Control (40 pts)**
5. Motif unity (10): Do visual details serve a unified theme?
6. Material and lighting description (10): Specific material and light logic?
7. Constraints and negative prompts (10): Anti-failure constraints present?
8. Text-image integration (10): Text layout handled or explicitly absent?

**Productization and Reusability (20 pts)**
9. Parameterization (10): Easy to adjust and reuse?
10. Failure anticipation (10): Common AI errors preemptively blocked?

Logic check per prompt: character consistency, scene continuity, physics plausibility, style coherence. Fix contradictions if found.

**Target: each prompt ≥ 80 points (High Quality).** If below, self-optimize and output the improved version.

## Workflow (Single-scene Mode)

Simpler, one pass:

1. Extract character features and visual style from the scene
2. Determine optimal shot type and composition
3. Generate prompt (same requirements as Step 3-4 above)
4. Output

## Output Format

Primary language marked ★, secondary marked ☆:

```
### Image N | [Shot Type] | [Narrative Function]

**Scene Description:** [Detailed description in primary language]

**Text-to-Image Prompt ★ ([Primary Language]):**
[Complete detailed prompt, ready to copy-paste]

**Text-to-Image Prompt ☆ ([Secondary Language]):**
[Complete prompt adapted to target language conventions]

**Negative Prompt:** [negative keywords]

Score: [X]/100 | Level: [Product-grade / High Quality / Usable]
Strengths: [One sentence]
Improvements: [If applicable, one sentence]
```

## Prompt Writing Spec

**Structure** (by priority):
```
[Style] + [Shot type + Composition + Camera angle] + [Subject + fixed features] + [Action/Expression] + [Environment/Background] + [Lighting/Atmosphere] + [Material/Texture] + [Quality tags] + [Negative prompt]
```

**Bilingual output rules:**
- Primary language prompt: complete and detailed, ready to copy-paste
- Secondary language prompt: equally complete, adapted to target language prompt conventions (not a literal translation)

**Consistency rules:**
- Character fixed features (age, hair, clothing) must be explicitly repeated in every prompt
- Style, color palette, lighting baseline must carry through all images
- Key props appearance must remain consistent

**Diversity rules:**
- Adjacent images use different shot types
- Encourage different composition techniques
- Character posture, expression, position may vary
- Lighting intensity may be adjusted, style remains constant

## Reference Files

Read on demand:

- `references/shot-types.md` — Shot types, camera angles, narrative rhythm templates
- `references/composition-patterns.md` — 12 composition patterns with prompt fragments
- `references/style-params.md` — 30+ style parameters (keywords, quality tags, avoid list, lighting)
