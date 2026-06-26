---
name: svg-artist
description: Generate SVG images using text LLM instead of image generation APIs. Use when user wants to create illustrations, icons, cartoons, diagrams, or any visual content without DALL-E/Midjourney/Stable Diffusion. The LLM writes SVG code directly - works great for simple graphics, cartoons, icons, and stylized art.
---

# SVG Artist

Generate images by writing SVG code with the text model. No image generation API needed.

## How It Works

1. **User describes the image** → "画一只可爱的小猫" / "create a cartoon cat"
2. **LLM writes SVG code** → Calculates coordinates, shapes, colors
3. **Convert to PNG** → Using `rsvg-convert` or `convert`

## Quick Start

```
User: 给我画一只小狗
You: [Generate SVG code] → Send the PNG
```

## SVG Drawing Guide

### Canvas Setup

Default size: 400x400 pixels. Origin (0,0) is top-left.

```svg
<svg width='400' height='400' xmlns='http://www.w3.org/2000/svg'>
  <!-- Background -->
  <rect width='400' height='400' fill='#87CEEB'/>
  <!-- Your shapes here -->
</svg>
```

### Basic Shapes

**Circle**
```svg
<circle cx='200' cy='200' r='50' fill='#FF6B6B' stroke='#333' stroke-width='2'/>
```

**Ellipse** (great for bodies, heads)
```svg
<ellipse cx='200' cy='200' rx='80' ry='50' fill='#D2691E' stroke='#8B4513' stroke-width='3'/>
```

**Rectangle** (legs, buildings)
```svg
<rect x='100' y='300' width='50' height='80' rx='10' fill='#666'/>
```

**Polygon** (ears, stars)
```svg
<polygon points='150,50 130,100 170,100' fill='#8B4513'/>
```

**Path** (curves, tails, mouths)
```svg
<!-- Arc -->
<path d='M 100 200 A 50 50 0 0 1 200 200' stroke='#333' stroke-width='3' fill='none'/>
<!-- Bezier curve -->
<path d='M 100 200 Q 150 150 200 200' stroke='#333' stroke-width='3' fill='none'/>
```

### Proportional Design Tips

Use percentages of canvas size (400px):
- Head: `rx='70' ry='60'` (about 15-20% of width)
- Body: `rx='100' ry='70'` (about 25% of width)
- Eyes: `r='15'` (about 4% of width)

Position using fractions:
- Center X: `200` (50%)
- Head Y: `140` (35%)
- Body Y: `250` (62%)

### Color Palette

**Warm colors**: `#D2691E` (chocolate), `#FF6B6B` (coral), `#FFB347` (orange)
**Cool colors**: `#87CEEB` (sky blue), `#98FB98` (pale green), `#DDA0DD` (plum)
**Neutrals**: `#8B4513` (saddle brown), `#808080` (gray), `#F5F5DC` (beige)

### Common Patterns

**Eyes (cute style)**
```svg
<!-- Eye white -->
<ellipse cx='180' cy='130' rx='15' ry='15' fill='white' stroke='black' stroke-width='2'/>
<!-- Pupil -->
<ellipse cx='183' cy='132' rx='7' ry='7' fill='black'/>
<!-- Highlight -->
<ellipse cx='186' cy='130' rx='3' ry='3' fill='white'/>
```

**Blush/cheeks**
```svg
<ellipse cx='150' cy='160' rx='15' ry='10' fill='#FFB6C1' opacity='0.6'/>
```

**Smile**
```svg
<path d='M 180 170 A 25 25 0 0 0 220 170' stroke='#8B4513' stroke-width='3' fill='none'/>
```

**Tongue**
```svg
<ellipse cx='200' cy='190' rx='10' ry='15' fill='#FF69B4'/>
```

## Step-by-Step Workflow

When user asks for an image:

### Step 1: Understand the Subject
- What animal/object? → dog, cat, house, car, etc.
- What style? → cute, realistic, minimalist, cartoon
- What pose? → sitting, standing, happy, sad

### Step 2: Plan the Composition
```
Head position: cy = 35% (140)
Body position: cy = 62% (250)
Legs: cy = 78% (310)
Background: soft gradient or solid color
```

### Step 3: Write SVG Code
Use Node.js inline to generate:
```bash
node -e "
const fs = require('fs');
const svg = \`<svg>...</svg>\`;
fs.writeFileSync('/tmp/image.svg', svg);
"
```

### Step 4: Convert to PNG
```bash
rsvg-convert /tmp/image.svg -o /tmp/image.png
# or: convert /tmp/image.svg /tmp/image.png
```

### Step 5: Send the Image
```
<qqimg>/tmp/image.png</qqimg>
```

## Example: Drawing a Cat

```svg
<svg width='400' height='400' xmlns='http://www.w3.org/2000/svg'>
  <rect width='400' height='400' fill='#E6E6FA'/>

  <!-- Body -->
  <ellipse cx='200' cy='250' rx='100' ry='70' fill='#FFB347' stroke='#FF8C00' stroke-width='3'/>

  <!-- Head -->
  <ellipse cx='200' cy='140' rx='70' ry='60' fill='#FFB347' stroke='#FF8C00' stroke-width='3'/>

  <!-- Ears -->
  <polygon points='130,110 110,50 160,90' fill='#FF8C00'/>
  <polygon points='270,110 290,50 240,90' fill='#FF8C00'/>

  <!-- Eyes -->
  <ellipse cx='170' cy='130' rx='15' ry='20' fill='#90EE90' stroke='black' stroke-width='2'/>
  <ellipse cx='230' cy='130' rx='15' ry='20' fill='#90EE90' stroke='black' stroke-width='2'/>

  <!-- Pupils (vertical slits) -->
  <ellipse cx='170' cy='130' rx='4' ry='12' fill='black'/>
  <ellipse cx='230' cy='130' rx='4' ry='12' fill='black'/>

  <!-- Nose -->
  <ellipse cx='200' cy='160' rx='8' ry='5' fill='#FF69B4'/>

  <!-- Whiskers -->
  <line x1='120' y1='155' x2='165' y2='160' stroke='#666' stroke-width='1.5'/>
  <line x1='120' y1='165' x2='165' y2='165' stroke='#666' stroke-width='1.5'/>
  <line x1='235' y1='160' x2='280' y2='155' stroke='#666' stroke-width='1.5'/>
  <line x1='235' y1='165' x2='280' y2='165' stroke='#666' stroke-width='1.5'/>

  <!-- Mouth -->
  <path d='M 190 170 Q 200 180 210 170' stroke='#FF8C00' stroke-width='2' fill='none'/>

  <!-- Legs -->
  <ellipse cx='150' cy='310' rx='20' ry='30' fill='#FFB347' stroke='#FF8C00' stroke-width='2'/>
  <ellipse cx='250' cy='310' rx='20' ry='30' fill='#FFB347' stroke='#FF8C00' stroke-width='2'/>

  <!-- Tail -->
  <path d='M 300 250 Q 340 200 320 150' stroke='#FFB347' stroke-width='20' fill='none' stroke-linecap='round'/>
</svg>
```

## Script: generate_svg.js

Use the helper script for common subjects:

```bash
node scripts/generate_svg.js "cute puppy with big eyes" /tmp/puppy.png
```

The script provides templates and the LLM fills in details.

## Limitations

- Best for: cartoons, icons, simple illustrations, stylized art
- Not ideal for: photorealistic images, complex scenes, detailed textures
- Works well with: animals, characters, objects, simple backgrounds

## Tips for Better Results

1. **Start simple** - Basic shapes first, add details after
2. **Use layers** - Background → body → head → features → highlights
3. **Add character** - Big eyes, blush, expressive features
4. **Keep proportions** - Cute style = big head, small body
5. **Test incrementally** - Generate, check, adjust
