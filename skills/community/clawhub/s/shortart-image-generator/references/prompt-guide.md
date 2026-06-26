# Image Prompt Writing Guide

## Table of Contents
1. [Basic Structure](#basic-structure)
2. [Style Keywords](#style-keywords)
3. [Commercial Scene Templates](#commercial-scene-templates)
4. [Chinese Prompt Tips](#chinese-prompt-tips)
5. [Negative Prompt](#negative-prompt)

---

## Basic Structure

A high-quality prompt consists of the following parts:

```
[Subject Description] + [Scene/Background] + [Style/Aesthetic] + [Lighting] + [Composition/Perspective] + [Quality Tags]
```

**Example:**
```
A surreal minimalist advertisement. Central product shot with photorealistic 
precision. Translucent frosted glass-paper aesthetic, clean white background. 
Soft cinematic lighting, gentle ambient shadows. Lilac accent color with liquid 
splash. Bold elegant slogan near subject. Ultra-detailed, 8k, product photography.
```

---

## Style Keywords

### Commercial Photography
- `product photography composition` — Commercial product photography composition
- `studio lighting` — Studio lighting
- `white background` — White background
- `photorealistic precision` — Photorealistic precision

### Art Styles
- `paper-glass style` — Paper-glass style (translucent frosted effect)
- `minimalist` — Minimalism
- `surreal` — Surrealism
- `cinematic` — Cinematic

### Lighting
- `soft cinematic lighting` — Soft cinematic lighting
- `natural window light` — Natural window light
- `dramatic side lighting` — Dramatic side lighting
- `golden hour` — Golden hour

### Quality Tags
- `4k resolution` — 4K resolution
- `ultra-detailed texture` — Ultra-detailed texture
- `organic imperfections` — Organic imperfections (adds realism)
- `realistic material properties` — Realistic material properties

---

## Commercial Scene Templates

### Product Main Image (White Background)
```
Clean product shot of {product} on pure white background. Studio lighting with 
soft shadows. Photorealistic, high-detail, product photography composition. 
No text, no watermark. 4k resolution.
```

### Scene Image (Lifestyle Photography)
```
{product} placed in {scene, e.g. cozy home office / outdoor cafe}.
{mood, e.g. warm and inviting / modern minimal} aesthetic.
Natural lighting, aspirational lifestyle photography. 8k, ultra-detailed.
```

### Infographic (Feature Showcase)
```
Product infographic for {product}. Highlight features: {feature1}, {feature2},
{feature3}. Clean callout lines, white background, professional sans-serif
typography. {brand color} accent. 2000×2000px.
```

### Advertisement Poster (Creative Style)
```
A surreal, minimalist {style, e.g. paper-glass / holographic / ink wash} 
advertisement. Central {product} with photorealistic precision. 
{accent color} color theme with {effect, e.g. liquid splash / light rays}. 
Elegant slogan '{slogan}' in modern sans-serif near the subject. 
Ultra-detailed, 8k, product photography composition.
```

---

## Chinese Prompt Tips

ShortArt backend supports Chinese prompts, recommended for:
- Using `seedream4.5` or `nano-banana-pro` models
- Scenarios requiring precise control of Chinese text content

**Chinese Example:**
```
Minimalist style product advertisement, white background, {product} centered,
soft studio lighting, light purple liquid splash decoration, modern sans-serif
font displaying slogan "{slogan}", ultra-high definition texture, 8K resolution,
commercial photography composition.
```

> If readable text is needed in the image, it must be explicitly written in the prompt, otherwise AI may generate garbled text.

---

## Negative Prompt

Appending the following content to the prompt field can filter out common issues:

```
Negative: cartoon, illustration, low quality, distorted, watermark, messy,
clutter, handwriting, jagged edges, blurry, oversaturated, ugly, deformed
```

> ShortArt API's `prompt` field can include negative prompt together, format:
> `"prompt": "{positive description}\nnegative_prompt: {negative description}"`
