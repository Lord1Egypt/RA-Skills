---
name: virtual-tryon-scorer
description: >
  Score and evaluate virtual try-on (VTON) results by analyzing identity preservation,
  garment fidelity, body consistency, and background stability. Use this skill whenever
  the user uploads virtual try-on images and wants quality assessment, scoring, or feedback.
  Trigger on phrases like "try-on scoring", "virtual try-on evaluation", "rate this try-on",
  "试穿打分", "试穿效果评价", "虚拟试穿评分", or when the user shares before/after clothing
  swap images and asks for quality judgment. Also trigger when the user mentions VTON,
  clothing transfer, garment swap, or outfit change evaluation — even if they don't
  explicitly say "virtual try-on".
---

# Virtual Try-On Effect Scorer (虚拟试穿效果打分)

Evaluate the quality of AI-generated virtual try-on results by comparing source person,
target garment, and the generated output. Produce structured per-dimension scores with
brief explanations, then aggregate into a weighted total score.

## Input Recognition

Users may provide images in two ways. Correctly identifying which format you're dealing
with is critical — getting this wrong invalidates the entire evaluation.

### Format A: Three Separate Images

The user uploads three distinct images:
1. **Source Person Image** — the original photo of the person before try-on
2. **Target Garment Image** — the reference clothing item to be tried on
3. **Try-On Result Image** — the AI-generated output showing the person wearing the target garment

When three images are provided, ask the user to clarify which is which if it's not
obvious from context or filenames. Common naming patterns: "person/model/source",
"cloth/garment/target", "result/output/generated".

### Format B: Single Concatenated Image

The user uploads one image that contains all three photos stitched together (side by side,
or in a grid layout). In this case:

1. Identify the panel layout (horizontal strip, vertical strip, 2×2 grid, etc.)
2. Determine which panel is which by visual cues:
   - The **source person** panel shows a person in their original outfit (different from the target garment)
   - The **target garment** panel typically shows clothing on a flat lay, mannequin, or a different model
   - The **try-on result** panel shows the same person from the source wearing the target garment
3. If the layout is ambiguous, describe what you see in each panel and ask the user to confirm

**Key distinction signals:**
- If one panel shows an isolated clothing item (no person or a mannequin), that's the garment reference
- If two panels show the same person but in different clothes, the one matching the garment reference is the result
- Pay attention to background consistency between panels — the source person and result often share the same background

## Evaluation Dimensions

Score each dimension on a **0–100** scale. The dimensions are listed in order of importance,
which also determines their weight in the final score.

### Dimension 1: Face Identity Preservation (Weight: 40%)

This is the single most important criterion. The person in the try-on result must be
recognizably the same individual as in the source image. The face is the primary carrier
of identity — if the face changes, the try-on is fundamentally broken regardless of
how good everything else looks.

**What to examine:**
- Facial structure: jawline, cheekbones, face shape
- Key facial features: eyes, nose, mouth, eyebrows
- Skin tone and complexion
- Facial expression (should be similar or naturally plausible)
- Hairstyle and hair color at the boundary with the face
- Accessories on the face (glasses, earrings, piercings)

**Scoring guide:**
- **90–100**: Face is virtually identical; the person is immediately recognizable
- **70–89**: Minor differences exist but identity is clearly preserved; would pass as the same person
- **50–69**: Noticeable changes to facial features; identity is questionable
- **30–49**: Significant facial distortion or identity shift; hard to confirm same person
- **0–29**: Face is severely altered, blurred, or unrecognizable

### Dimension 2: Garment Fidelity & Fit (Weight: 30%)

The clothing in the result should faithfully reproduce the target garment's visual
characteristics and fit naturally on the person's body. This matters because the whole
point of virtual try-on is to show how a specific garment looks on a specific person.

**What to examine:**
- Color accuracy: hue, saturation, brightness matching the reference
- Pattern/print fidelity: logos, stripes, patterns, text should be preserved
- Garment structure: collar style, sleeve type, hem shape, buttons, zippers
- Fabric texture: material appearance should match the reference
- Fit quality: the garment should drape naturally on the person's body
- Proportions: garment proportions should be appropriate for the person's body size
- Boundary quality: clean edges where garment meets skin/other clothing

**Scoring guide:**
- **90–100**: Garment is pixel-perfect in appearance and fits naturally
- **70–89**: Minor color shifts or small pattern distortions; fit looks natural
- **50–69**: Noticeable garment differences; some fit issues (floating/clipping)
- **30–49**: Significant garment deviations; poor fit or unnatural draping
- **0–29**: Garment is barely recognizable or severely distorted

### Dimension 3: Non-Face Body Identity Preservation (Weight: 20%)

Beyond the face, other body characteristics should remain consistent between the source
and result. This reinforces the overall sense that this is genuinely the same person,
not a face-swap on a different body.

**What to examine:**
- Body shape and proportions (build, height impression, body type)
- Skin tone on visible body parts (arms, hands, neck, legs)
- Hands: finger count, pose, natural appearance
- Tattoos, scars, or other visible body markings
- Jewelry and accessories not on the face (watches, bracelets, rings)
- Parts of the outfit that shouldn't change (pants if only top is swapped, shoes, etc.)
- Hair (length, style, color) in areas away from the face

**Scoring guide:**
- **90–100**: Body characteristics are perfectly preserved
- **70–89**: Minor inconsistencies but overall body identity is intact
- **50–69**: Some body parts look different or have artifacts
- **30–49**: Noticeable body shape changes or significant artifacts
- **0–29**: Severe body distortion or completely different body characteristics

### Dimension 4: Background Preservation (Weight: 10%)

The background should remain stable between the source person image and the try-on
result. Background changes are distracting and reduce the realism of try-on.

**What to examine:**
- Scene consistency: same environment, objects, spatial layout
- Color and lighting: consistent tones and illumination
- Artifacts: blurring, ghosting, or warping around the person's silhouette
- Object integrity: furniture, walls, patterns should be unaltered
- Edge blending: smooth transition between person and background

**Scoring guide:**
- **90–100**: Background is identical or virtually indistinguishable
- **70–89**: Very minor changes; need close inspection to notice
- **50–69**: Some noticeable background alterations or artifacts
- **30–49**: Significant background changes or heavy artifacts
- **0–29**: Background is severely altered or replaced

## Output Format

Present the evaluation in this exact structure:

```
## 虚拟试穿效果评分报告

### 输入识别
- 输入格式：[三张独立图片 / 单张拼接图]
- 原始人物：[简要描述人物特征]
- 目标服装：[简要描述服装特征]
- 试穿结果：[简要描述试穿效果概况]

### 分项评分

#### 1. 人脸身份保持 (权重 40%)
- **得分：XX/100**
- 评价：[1-2 sentences explaining the score]

#### 2. 服装还原与贴合 (权重 30%)
- **得分：XX/100**
- 评价：[1-2 sentences explaining the score]

#### 3. 非人脸身体特征保持 (权重 20%)
- **得分：XX/100**
- 评价：[1-2 sentences explaining the score]

#### 4. 背景保持 (权重 10%)
- **得分：XX/100**
- 评价：[1-2 sentences explaining the score]

### 总分
- **加权总分：XX.X/100**
- 计算方式：(人脸 × 0.4) + (服装 × 0.3) + (身体 × 0.2) + (背景 × 0.1)

### 总体评价
[2-3 sentences summarizing the overall quality, highlighting the strongest and
weakest aspects, and suggesting what could be improved in the try-on pipeline]
```

## Evaluation Philosophy

The scoring should be honest and calibrated. A few guiding principles:

- **Don't grade on a curve.** A score of 95 should mean genuinely excellent quality,
  not just "better than average." Reserve scores above 90 for results that would fool
  a careful human observer.

- **Weight the dimensions as specified.** Face identity (40%) dominates because a
  face change means the try-on has failed its core purpose — showing what *this person*
  would look like in *that outfit*. A technically perfect garment transfer with a
  different face is worthless.

- **Be specific in feedback.** Don't just say "looks good" or "has issues." Point to
  concrete observations: "the nose bridge appears slightly narrower" or "the striped
  pattern on the left sleeve is distorted."

- **Consider the use case.** Virtual try-on is a practical tool — users want to know
  if they'd look good in a piece of clothing before buying it. Evaluate from that
  perspective: would this result help someone make a confident purchase decision?

## Edge Cases

- **If garment type doesn't match** (e.g., the source wears a t-shirt and the result
  shows a completely different category like a dress), note this but still evaluate
  the result against the target garment reference.

- **If the image quality is very low**, note the limitation and explain that the scores
  might not be fully reliable due to resolution constraints.

- **If the user only provides two images** (missing one of the three), ask which one
  is missing and whether they can provide it. If they can't provide the garment
  reference, you can still evaluate face/body/background but should caveat the
  garment score.

- **If the try-on only changes part of the outfit** (e.g., only the top), only evaluate
  the changed portion for garment fidelity, and note what was preserved from the original.
