# Character Prompting for Realistic UGC

The key to realistic AI characters is **imperfection**. Most AI-generated faces look like mannequins because they're too clean, too smooth, too perfect.

## The Anti-Perfection Framework

### Skin Texture (Critical)

**Always include:**
```
visible micro-pores across the nose and cheeks, faint peach fuzz catching sidelight
along the jawline, natural oils breaking through on the forehead and nose bridge,
no foundation, no filter
```

**By age range:**
| Age | Texture Details |
|-----|-----------------|
| 20s | Slight shine on T-zone, occasional texture variation, natural flush |
| 30s | Fine lines beginning at eye corners, forehead texture, slightly larger pores |
| 40s | Deeper smile lines, crow's feet, visible pores, skin texture variation |
| 50+ | Pronounced lines, age spots, texture throughout, natural sageing |

### Facial Imperfections

Add 2-3 from this list:
- `faint dark circles under eyes`
- `2-day stubble` / `subtle stubble shadow`
- `barely visible acne scar`
- `slight redness around nose`
- `uneven skin tone`
- `natural lip dryness`
- `visible pore variation`
- `slight asymmetry in features`

### Expression Details

Don't just say "smiling"—be specific:
```
a genuine, broad smile revealing straight teeth with natural slight imperfections,
a hint of gum line visible, laugh lines crinkling at the outer corners of eyes
```

**Expression vocabulary:**
- `crow's feet activated by genuine smile`
- `slight squint from bright light`
- `cheeks raised authentically`
- `forehead muscles relaxed`
- `natural brow position`

## Camera Realism (iPhone Aesthetic)

The goal is to look like a selfie video, not a professional shoot.

### Lens Characteristics
```
Native iPhone 11 lens (26mm equivalent): slightly wide, honest perspective,
mild barrel softness at edges, minimal compression
```

### Depth Artifacts
```
Only tiny pockets of neural blur appear around hair edges and watch face—
true iPhone depth-map artifacts. NOT professional bokeh.
```

### Sensor Limitations
```
ISO noise from 500-900 sits naturally in midtones, producing sensor grain
and mild vignetting (12% falloff)
```

## Lighting (Available, Not Studio)

**WRONG:** `professional studio lighting`, `three-point lighting`, `softbox`

**RIGHT:**
```
Available Light: a mix of cool overcast daylight filtering through a large window
from the left and warm tungsten from a brass desk lamp on the right, creating
imperfect balance and natural falloff. Shadows are soft but asymmetric, with
slight warmth pooling under the cheekbones and cooler tones washing across
the white wall.
```

### Light Temperature Mix

| Source | Color Temp | Position |
|--------|------------|----------|
| Window (overcast) | Cool, 6500K | Side/back |
| Desk lamp | Warm, 2700K | Opposite side |
| Overhead | Neutral, 4000K | Above |

This creates **color temperature discord**—exactly what happens in real rooms.

## Background (Readable, Not Blurred)

Studio AI videos blur backgrounds heavily. Real UGC has **readable backgrounds**.

```
The background remains mostly sharp: a dark wood bookcase filled with hardcovers
and a few framed photos is clearly readable to the left; a black Peloton bike
with its red accent screen sits in the corner to the right, identifiable down
to the handlebar grips.
```

**Include specific objects:**
- Bookshelf with actual book spines visible
- Exercise equipment (brand identifiable)
- Plants (specific type)
- Wall art or framed photos
- Electronics (laptop, monitor edge)

## Foreground Elements

Real videos often have stuff in front:
```
In the immediate foreground: hands rest naturally on the oak desk surface,
fingers relaxed and slightly interlaced, visible veins and knuckle texture
catching the light. Nearby sits a half-empty water bottle, wireless earbuds
case, and a notebook with a pen—NOT heavily blurred, just a mild iPhone-style
computational depth gradient.
```

## Reality Artifacts

Add technical "flaws" that scream authenticity:
```
gentle 35mm film grain, light fingerprint smudge on lens glass, tiny dust haze
in the air, and minimal chromatic aberration around high-contrast edges where
the black shirt meets the bright wall. No cinematic bloom, no studio finish.
```

**Artifact checklist:**
- [ ] Film/sensor grain
- [ ] Lens smudge or fingerprint
- [ ] Dust in air
- [ ] Chromatic aberration at edges
- [ ] Slight vignetting

## Character Templates by Type

### Professional/Business
```
A [gender] in their [age]s with [ethnicity] complexion, wearing a fitted [color]
button-down, top button undone. Hair is [description]—professional but not
overly styled. Expression is engaged and trustworthy—slight smile, direct eye
contact, brows slightly raised in openness. Visible: natural oils on forehead,
pore texture on nose, faint lines at eye corners.
```

### Casual/Lifestyle
```
A [gender] in their [age]s, [ethnicity], wearing a comfortable [casual garment].
Hair is [natural/messy description]. Expression is relaxed and authentic—half-smile,
eyes slightly crinkled, conversational posture. Skin shows real texture: visible
pores, natural shine, [age-appropriate imperfections].
```

### Fitness/Health
```
A fit [gender] in their [age]s with [skin tone], slight sheen of perspiration on
forehead. Wearing [athletic wear]. Hair is [post-workout description]. Expression
is energized—bright eyes, genuine smile showing teeth, cheeks flushed naturally.
Visible: chest rising from breathing, veins slightly prominent on arms.
```

## Common Mistakes to Avoid

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| "Beautiful skin" | Too perfect | Specify texture, pores, oils |
| "Studio lighting" | Too professional | Use available light mix |
| "Blurred background" | Looks staged | Keep background readable |
| "Perfect smile" | Uncanny valley | Add asymmetry, gum line, lines |
| "Clean composition" | Too intentional | Add foreground clutter |
| "High fashion" | Wrong aesthetic | Casual, slightly disheveled |

## Enhancing Generated Images

After Nano Banana generation, consider:

1. **Enhancor AI** - Upscaling tool that adds realistic micro-texture
2. **Photoshop Neural Filters** - Can add subtle imperfections
3. **Manual touch-up** - Add slight grain, color correction for mixed lighting

## Style Override Tag

End every prompt with:
```
Styling Overlay: raw UGC realism, available indoor light, mixed color temperature,
minimal depth blur, slight lens smudge, visible ISO noise, no cinematic polish,
emphasis on authenticity and true iPhone capture.
```
