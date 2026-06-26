# Photorealism & Portraits

## Identity Preservation Techniques

### Core Principles

**Most critical rule:** Explicitly state face preservation in the first sentence.

**Essential phrases (use one or more):**
- "Keep the facial features of the person in the uploaded image exactly consistent"
- "Preserve original face 100% accurate from reference image"
- "maintain the exact facial structure, identity, and key features of the person in the input image"
- "without changing her/his original face"
- "Important: do not change the face"

**In JSON format:**
```json
{
  "subject": {
    "face": {
      "preserve_original": true,
      "reference_match": true,
      "description": "The person's facial features must remain exactly the same as the reference image"
    }
  }
}
```

### Professional Headshot Template

**Use case:** Transform casual photos into corporate headshots

```
Keep the facial features of the person in the uploaded image exactly consistent.
Dress them in a professional [OUTFIT: navy blue business suit, smart casual blazer, etc.] with [SHIRT COLOR] shirt.

Background: Place the subject against a clean, solid [COLOR] studio photography backdrop.
The background should have a subtle gradient, slightly lighter behind the subject and darker towards the edges (vignette effect).
There should be no other objects.

Photography Style: Shot on a [CAMERA: Sony A7III, Canon EOS R5] with an [LENS: 85mm f/1.4, 50mm f/1.8] lens, creating flattering portrait compression.

Lighting: Use a classic three-point lighting setup.
The main key light should create soft, defining shadows on the face.
A subtle rim light should separate the subject's shoulders and hair from the dark background.

Crucial Details:
- Render natural skin texture with visible pores, not an airbrushed look
- Add natural catchlights to the eyes
- The fabric of the [OUTFIT] should show subtle [wool/cotton/silk] texture

Final image should be an ultra-realistic, 8k professional headshot.
```

**Variables to customize:**
- OUTFIT: Business suit, smart casual, creative professional
- SHIRT COLOR: White, light blue, cream
- BACKGROUND COLOR: Dark gray, charcoal, navy, burgundy (#562226)
- CAMERA: Sony A7III, Canon EOS R5, Hasselblad
- LENS: 85mm f/1.4 (classic), 50mm f/1.8 (budget-friendly), 135mm f/2 (high-end)

## Era-Specific Aesthetics

### 2000s Mirror Selfie

**Characteristics:**
- Early digital camera aesthetic
- Harsh flash with blown-out highlights
- Nostalgic bedroom setting
- Characteristic accessories and styling

**Template (JSON):**
```json
{
  "subject": {
    "description": "Young woman taking mirror selfie",
    "age": "young adult",
    "expression": "confident and slightly playful",
    "hair": {
      "color": "dark",
      "style": "very long, voluminous waves with soft wispy bangs"
    },
    "clothing": {
      "top": {
        "type": "fitted cropped t-shirt",
        "color": "cream white",
        "details": "[GRAPHIC: anime cat face, band logo, vintage brand]"
      },
      "bottom": {
        "type": "[jeans/skirt]",
        "fit": "[low-rise/high-waisted]"
      }
    },
    "face": {
      "preserve_original": true,
      "makeup": "natural glam makeup with soft pink dewy blush and glossy [red/pink] lips"
    }
  },
  "accessories": {
    "earrings": {
      "type": "gold geometric hoop earrings"
    },
    "jewelry": {
      "necklace": "[choker/layered chains]",
      "waistchain": "silver waistchain"
    },
    "device": {
      "type": "smartphone",
      "details": "patterned case"
    }
  },
  "photography": {
    "camera_style": "early-2000s digital camera aesthetic",
    "lighting": "harsh super-flash with bright blown-out highlights but subject still visible",
    "angle": "mirror selfie",
    "shot_type": "tight selfie composition",
    "texture": "subtle grain, retro highlights, crisp details, soft shadows"
  },
  "background": {
    "setting": "nostalgic early-2000s bedroom",
    "wall_color": "pastel tones",
    "elements": [
      "chunky wooden dresser",
      "CD player",
      "posters of 2000s pop icons",
      "hanging beaded door curtain",
      "cluttered vanity with lip glosses",
      "fairy lights"
    ],
    "atmosphere": "authentic 2000s nostalgic vibe",
    "lighting": "retro"
  }
}
```

### 1990s Camera Flash Portrait

**Characteristics:**
- Point-and-shoot camera aesthetic
- Direct front flash creating nostalgic glow
- Film texture and grain
- Casual, intimate atmosphere

**Template:**
```
Without changing the original face, create a portrait of [PERSON DESCRIPTION] with [SKIN TONE] skin, captured with a 1990s-style camera using a direct front flash.

Hair: [HAIRSTYLE: messy dark brown tied up, sleek bob, curtain bangs]
Expression: [calm yet playful smile, soft gaze, candid laugh]
Outfit: Modern [CLOTHING: oversized cream sweater, vintage band tee, flannel shirt]

Background: Dark [WALL COLOR: white, beige, gray] wall covered with aesthetic [DECOR: magazine posters and stickers, band posters, photo collage], evoking a cozy [SETTING: bedroom, dorm room, personal room] atmosphere under dim lighting.

The 35mm lens flash creates a nostalgic glow with:
- Visible film grain texture
- Slight color shift (warm yellows and cool blues)
- Soft vignetting at edges
- Natural red-eye reduction
- Candid, snapshot quality
```

### Victoria's Secret Style Glamour

**Use case:** High-fashion, backstage beauty photography

**Template:**
```
Create a glamorous photoshoot in the style of Victoria's Secret.

Subject: The person from the uploaded reference image (Keep the face 100% accurate from the reference image).

Pose: Standing almost sideways, slightly bent forward, during final preparation for the show.
Action: Makeup artists apply lipstick to her (only their hands visible in the frame).

Outfit:
- Corset decorated with beaded embroidery and crystals
- Short fluffy skirt
- Large feather wings

Details:
- Emphasize expressiveness of gaze
- Luxurious look of outfit with intricate beadwork
- Individual crystals catching light

Background: Darkly lit room, probably under the podium, backstage atmosphere.

Lighting: Flash from camera emphasizing:
- Shine of beads and crystals on corset
- Glowing, dewy skin
- Soft catchlights in eyes
- Dramatic rim light on wings

Style: Victoria's Secret aesthetic - sensuality, luxury, glamour
Quality: Very detailed, ultra-high resolution, professional fashion photography

Important: Do not change the face.
```

## Film Photography Aesthetics

### Kodak Portra 400 Style

**Characteristics:**
- Warm, nostalgic tones
- Natural skin rendering
- Subtle grain
- Soft focus areas
- Dreamy quality

**Template:**
```
Keep the facial features of the person in the uploaded image exactly consistent.

Style: A cinematic, emotional portrait shot on Kodak Portra 400 film.

Setting: [ENVIRONMENT: Urban street coffee shop window, park bench, city rooftop] at Golden Hour (sunset).
Warm, nostalgic lighting hitting the side of the face.

Atmosphere: Apply subtle film grain and soft focus to create a dreamy, storytelling vibe.

Action: The subject is [ACTION: looking slightly away from camera, gazing at something off-frame, in candid moment], holding a [PROP: coffee cup, book, flower], with a relaxed, candid expression.

Technical:
- Shot on 35mm film camera
- Kodak Portra 400 film stock
- Natural light, golden hour
- Shallow depth of field
- Bokeh background of [BACKGROUND: city lights, foliage, urban scene]
- Soft focus on edges
- Rich, warm color palette

Quality: High quality, cinematic depth of field, professional film photography.
```

### Harsh Flash Photography (Canon IXUS Aesthetic)

**Characteristics:**
- Point-and-shoot camera from early 2000s
- Direct, harsh flash
- Realistic lighting with strong shadows
- Sharp, unforgiving detail
- Candid snapshot quality

**Template (JSON):**
```json
{
  "image_parameters": {
    "style": "Canon IXUS aesthetic",
    "type": "Point-and-shoot photography",
    "quality": "Hyper-realistic",
    "tone": "Sharp, direct",
    "lighting_and_atmosphere": "Realistic, flash-style/direct lighting"
  },
  "subject": {
    "constraints": {
      "facial_identity": "Match reference image exactly 100%",
      "face_edits": "None allowed"
    },
    "hair": {
      "style": "Long, natural, lightly messy layered look",
      "movement": "Blowing gently in the wind",
      "details": "Strands slightly covering part of face"
    },
    "makeup": {
      "cheeks_and_nose": "Soft pink blush with blurred effect",
      "lips": "Subtle pink-orange tinted outline"
    },
    "expression": [
      "Cute",
      "Naive",
      "Cheerful"
    ],
    "pose": {
      "body_position": "Half-sitting, half-standing",
      "action": "Flicking hair"
    },
    "clothing": {
      "top": "[STYLE: black strapless top, tank top, crop top]",
      "bottom": "[STYLE: low-waisted jeans, mini skirt]"
    }
  },
  "environment": {
    "setting": "[LOCATION: Modern pub, cafe, home interior]",
    "foreground_props": [
      "[PROP 1: Round table]",
      "[PROP 2: Bottle]",
      "[PROP 3: Glass]"
    ]
  },
  "camera_specs": {
    "camera": "compact digital camera simulation",
    "lens": "equivalent to 28-35mm",
    "aperture": "f/2.8",
    "iso": "400",
    "shutter_speed": "1/60 with flash",
    "white_balance": "auto flash",
    "lighting": "harsh direct flash on subject, ambient low light in background",
    "color_grading": "nostalgic digital-camera tones, high contrast flash, subtle display grain"
  }
}
```

## Advanced Portrait Techniques

### Multiple Pose Y2K Scrapbook

**Use case:** Social media content with multiple poses in one collage

**Key elements:**
- Same outfit and hairstyle across all poses
- Different expressions and actions
- Scrapbook aesthetic with stickers and doodles
- Pastel, vibrant color palette

**Template excerpt (see full JSON in user examples):**
```json
{
  "facelock_identity": "true",
  "accuracy": "100%",
  "scene": "Colorful Y2K scrapbook poster aesthetic, vibrant stickers, multiple subjects wearing the same outfit and hairstyle with different poses and cutouts",
  "main_subject": {
    "description": "A young Y2K-styled woman as the main focus",
    "multiple_poses": [
      "close-up shot with heart-shape fingers",
      "full-body squatting pose holding white polaroid camera",
      "mid-shot touching cheek while blowing pink bubblegum",
      "seated elegantly with one eye winking and peace sign"
    ]
  },
  "additional_visuals": [
    "Heart, star, and butterfly stickers",
    "Retro sparkles",
    "Polaroid frames",
    "Neon outlines",
    "Magazine cutout texts: 'SO CUTE!', '199X!'"
  ]
}
```

### Fisheye/Wide Angle Selfie

**Characteristics:**
- Ultra-wide lens distortion (12-18mm)
- Exaggerated perspective
- Close-up intimacy
- Playful, casual vibe

**Template:**
```
A hyper-realistic fisheye wide-angle selfie, captured with a vintage 35mm fisheye lens creating heavy barrel distortion.
Without any camera or phone visible in the subject's hands.

Subject & Action: A close-up, distorted photo featuring [Person From Uploaded Image] [ACTION: sipping drink, making silly face, leaning toward camera].
[Additional people can be included with exaggerated perspective]

Lens Effects:
- Ultra-wide 12mm fisheye lens
- Strong barrel distortion
- Subject's face and hands appear larger
- Background curves away
- Exaggerated features due to proximity

Lighting & Texture:
- [LIGHTING: Harsh direct flash, bright daylight, golden hour]
- Authentic film grain
- Slight motion blur on edges
- Chromatic aberration
- Looks like candid amateur snapshot, not studio photo

Depth of Field: Shallow, foreground sharp, background soft
Reflections: [If sunglasses present] glasses show distorted reflection of environment
Color Grade: Clean natural / warm nostalgic / high contrast
Composition: Face in extreme closeup, intimate, casual mood
```

### Character Consistency Selfie with Celebrity/Character

**Use case:** Take a selfie with a movie character or celebrity

**Template:**
```
I'm taking a selfie with [CHARACTER/CELEBRITY: Iron Man, Darth Vader, Sherlock Holmes] on the set of [MOVIE/SHOW NAME].

Keep the person exactly as shown in the reference image with 100% identical:
- Facial features
- Bone structure
- Skin tone
- Facial expression
- Pose
- Appearance

Setting: [ENVIRONMENT: movie set, iconic location from film, behind-the-scenes]
Lighting: [STYLE: natural daylight, studio lighting, dramatic cinematic]
Mood: [VIBE: excited, casual, candid, professional]

Both subjects should appear natural as if genuinely together.
1:1 aspect ratio, 4K detail.
```

## Quality Markers

Always include these quality specifications for photorealistic portraits:

**Resolution:**
- 8K ultra HD
- 4K high resolution
- Sharp, crisp detail

**Texture:**
- Natural skin texture with visible pores
- Individual strands of hair
- Fabric texture (wool grain, cotton weave, silk sheen)
- Not airbrushed

**Focus:**
- Crisp focus on eyes
- Shallow depth of field
- Soft bokeh background
- Natural catchlights in eyes

**Color:**
- Clean cinematic color grading
- Balanced tones
- Subtle warmth / cool tones
- Natural color accuracy

**Lighting:**
- Soft, even illumination
- Natural shadows
- Proper exposure
- No blown-out highlights (unless era-appropriate)
