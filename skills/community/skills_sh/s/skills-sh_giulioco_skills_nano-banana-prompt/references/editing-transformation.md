# Editing & Transformation

## Smart Outpainting (Composition Rescue)

### Expand to Different Aspect Ratio

**Use case:** Convert portrait to landscape, square to widescreen, etc.

**Template:**
```
Zoom out and expand this image to a [TARGET ASPECT RATIO: 16:9, 4:3, 1:1] aspect ratio.

Context Awareness:
- Seamlessly extend the scenery on [both left and right sides / top and bottom / all sides]
- Match the original lighting perfectly:
  * Direction of light source
  * Color temperature
  * Shadow angles
  * Time of day atmosphere
- Match weather conditions exactly ([sunny, cloudy, rainy, snowy])
- Match texture quality and grain

Logical Completion:
If there are cut-off objects on borders (shoulder, tree branch, building edge, furniture):
- Complete them naturally based on logical inference
- Maintain correct proportions and perspective
- Continue patterns and textures realistically
- Ensure architectural/structural integrity

Preservation Rules:
- Do not distort the original center image
- Keep original composition as focal point
- Maintain original image quality
- No stretching or squashing of original content

Seamless Blending:
- No visible seams where new content meets original
- Consistent color grading throughout
- Uniform focus/sharpness matching original
- Natural continuation of elements

Technical Consistency:
- Match depth of field from original
- Consistent bokeh if present
- Same noise/grain level
- Identical color palette

Quality: Ultra-high resolution, seamless extension, photorealistic continuation
```

## Background Removal & Replacement

### Smart Crowd/Tourist Removal

**Use case:** Remove unwanted people from backgrounds while preserving main subject

**Template:**
```
Remove all the [tourists/people/bystanders] in the background behind the main subject.

Main Subject Preservation:
- Keep the [PRIMARY SUBJECT: person, couple, group] in the foreground completely untouched
- Maintain their exact pose, clothing, lighting, and details
- Preserve any intentional blur or depth of field effects on main subject

Background People Removal:
- Identify and remove ALL background people
- Include people who are:
  * Partially visible
  * Blurred in background
  * Far in distance
  * Behind objects

Intelligent Fill:
Replace removed people with realistic background elements that logically fit:

[For outdoor scenes:]
- Extend cobblestone pavement
- Continue grass textures
- Add more trees or foliage
- Extend sky
- Add empty park benches
- Continue architectural elements

[For indoor scenes:]
- Continue wall patterns
- Extend floor textures
- Add more furniture or decor
- Fill with architectural details

[For urban scenes:]
- Extend storefronts
- Continue sidewalk patterns
- Add street furniture
- Extend buildings

Consistency Requirements:
- No blurry artifacts
- No 'smudges' or obvious clone stamp marks
- Filled areas must have same:
  * Grain/noise level as original
  * Focus depth appropriate to distance
  * Lighting and shadows matching scene
  * Color temperature
  * Perspective and scale

Technical Quality:
- Clean, seamless fills
- Realistic textures
- Proper perspective
- Natural lighting on new elements
- Photorealistic integration

Final Result:
- Main subject unchanged
- Background appears naturally empty
- No evidence of removed content
- Professional, clean composition

Quality: High-resolution, seamless edits, photorealistic background reconstruction
```

### Background Replacement

**Use case:** Replace entire background while keeping subject

**Template:**
```
Keep [SUBJECT: person, object, vehicle] from the original image exactly as is.
Replace the background completely with [NEW BACKGROUND: beach sunset, city skyline, studio white, mountain landscape].

Subject Preservation (CRITICAL):
- Maintain exact facial features and identity
- Keep original clothing and accessories
- Preserve original pose and positioning
- Maintain subject's original lighting (don't relight subject)

Background Replacement:
New background: [DETAILED DESCRIPTION]
- [Setting: beach at sunset, modern office, mountain vista]
- [Lighting: golden hour, bright daylight, studio lighting]
- [Elements: palm trees, buildings, clouds, etc.]

Integration Requirements:

Lighting Consistency:
- Background lighting should [match subject's lighting / create coherent scene]
- If subject has [front lighting, side lighting, backlight], background should support this
- Shadows should be consistent between subject and environment
- Color temperature should harmonize

Edge Quality:
- Clean, precise cutout of subject
- Natural edge transition (slight color bleed appropriate to depth of field)
- Fine details preserved (hair strands, clothing texture)
- No harsh halos or outlines

Depth & Perspective:
- Background perspective should make sense with subject's position
- Appropriate scale (subject shouldn't look pasted on)
- Depth of field consistent with subject's sharpness
- If subject is sharp, background can be [sharp throughout / slightly blurred / heavily blurred]

Color Grading:
- Harmonious color palette between subject and background
- Adjust background colors to complement subject if needed
- Consistent contrast levels
- Natural color transitions

Realism Markers:
- Subject casts appropriate shadow onto new background (if applicable)
- Reflections if on reflective surface
- Natural atmospheric perspective if background is distant
- Proper ground contact/shadow

Quality: Seamless integration, photorealistic composite, professional quality
```

## Style Transfer While Preserving Identity

### Transform to Different Art Style

**Template:**
```
Transform the person in the uploaded image into [STYLE: 3D cartoon character, anime character, oil painting, watercolor portrait, pixel art].

Identity Preservation (ABSOLUTE):
- Face must be 100% recognizable as the same person
- Maintain key facial features:
  * Eye shape and color
  * Nose structure
  * Mouth shape
  * Facial proportions
  * Distinctive features (moles, dimples, etc.)
  * Hair color and general style

Style Transformation:
[For 3D Cartoon:]
- Exaggerated but recognizable features
- Clean, smooth 3D rendering
- [Pixar / Disney / DreamWorks] aesthetic
- Appealing stylization while keeping likeness

[For Anime:]
- Large expressive eyes maintaining original eye color
- Simplified but recognizable features
- [Style: shoujo, shonen, seinen] aesthetic
- Hair maintains original color with anime styling

[For Painting:]
- [Medium: Oil, watercolor, acrylic] technique
- Visible brushstrokes
- Traditional art aesthetic
- Likeness maintained through painterly interpretation

Technical Approach:
- Start with original facial structure as base
- Apply style while preserving proportions
- Maintain facial recognition despite stylization
- Keep original person clearly identifiable

Quality Markers:
- Professional execution of chosen style
- High detail appropriate to medium
- Cohesive stylistic choices
- Clear, recognizable result

The result should look like [the person] rendered in [style], not a generic character.
```

## Aspect Ratio & Format Changes

### Portrait to Landscape Conversion

**Template:**
```
Convert this portrait-oriented image to landscape [ASPECT RATIO: 16:9, 21:9].

Center Preservation:
- Keep original portrait image as central focal point
- Do not crop or lose any content from original
- Original remains primary subject

Extension Strategy:
Extend scene [LEFT AND RIGHT / horizontally]:

Logical Continuation:
Analyze original environment and extend naturally:

[If indoor scene:]
- Continue room architecture
- Add more furniture consistent with space
- Extend walls, windows, lighting
- Maintain interior design style

[If outdoor scene:]
- Continue landscape (trees, mountains, sky, water)
- Extend architectural elements
- Add environmental details (clouds, distant objects)
- Maintain horizon line consistency

[If studio/simple background:]
- Continue backdrop smoothly
- Maintain gradient or texture
- Extend any visible props or elements

Consistency Requirements:
- Match lighting direction and quality
- Continue perspective accurately
- Maintain depth of field
- Same color grading
- Identical atmospheric conditions
- Consistent time of day
- Same weather conditions

Seamless Integration:
- No visible seams
- Natural transition from original to extended areas
- Continuous textures and patterns
- Smooth color and tone matching

Technical:
- Maintain original resolution quality in extended areas
- Match grain/noise characteristics
- Preserve original sharpness level in appropriate zones
- Realistic depth cues in extended environment

Result: Original image naturally expanded to wider composition, looking like it was always shot this way
```

## Torn Paper Art Effect

### Add Torn Paper Layers

**Use case:** Surreal effect revealing different art styles underneath

**Template (JSON):**
```json
{
  "task": "edit-image: add widened torn-paper layered effect",
  "base_image": {
    "use_reference_image": true,
    "preserve_everything": [
      "character identity",
      "facial features and expression",
      "hairstyle and anatomy",
      "outfit design and colors",
      "background, lighting, composition",
      "overall art style"
    ]
  },
  "rules": [
    "Only modify the torn-paper interior areas",
    "Do not change pose, anatomy, proportions, clothing details, shading, or scene elements"
  ],
  "effects": [
    {
      "effect": "torn-paper-reveal",
      "placement": "across chest height",
      "description": [
        "Add a wide, natural horizontal tear across the chest area",
        "The torn interior uses the style defined in interior_style"
      ]
    },
    {
      "effect": "torn-paper-reveal",
      "placement": "lower abdomen height",
      "description": [
        "Add a wide horizontal tear across the lower abdomen",
        "The torn interior uses the style defined in interior_style"
      ]
    }
  ],
  "interior_style": {
    "mode": "[CHOOSE: line-art, sumi-e, figure-render, colored-pencil, watercolor, pencil-drawing]",
    "style_settings": {
      "line-art": {
        "palette": "monochrome",
        "line_quality": "clean, crisp",
        "paper": "notebook paper with subtle ruled lines"
      },
      "sumi-e": {
        "palette": "black ink tones",
        "brush_texture": "soft bleeding edges",
        "paper": "plain textured paper"
      },
      "colored-pencil": {
        "stroke_texture": "visible pencil grain",
        "palette": "soft layered hues",
        "paper": "rough sketchbook paper"
      },
      "watercolor": {
        "palette": "soft transparent pigments",
        "blending": "smooth bleeding",
        "edges": "soft contours",
        "paper": "watercolor paper texture"
      },
      "pencil-drawing": {
        "graphite_texture": "visible pencil grain",
        "shading": "smooth gradients",
        "tone": "gray-scale",
        "paper": "notebook paper with faint ruled lines"
      }
    }
  },
  "torn_edge_characteristics": {
    "edge_quality": "natural, irregular tears",
    "depth_effect": "realistic paper thickness visible at edges",
    "shadow": "subtle shadow inside tear revealing depth"
  }
}
```

## Coordinate Visualization

### Location from Coordinates

**Use case:** Generate scene from GPS coordinates

**Template:**
```
[LATITUDE]° [N/S], [LONGITUDE]° [E/W] at [TIME: 19:00, dawn, noon]

Instructions for Nano Banana:
1. Identify the location from coordinates
2. Research what exists at these coordinates
3. Create photorealistic image of that specific location
4. Show scene as it would appear at specified time

Scene Requirements:
- Accurate geographical location
- Recognizable landmarks if famous location
- Appropriate time of day lighting
- Typical weather for location and season
- Cultural/regional accuracy
- Local architectural style
- Native vegetation
- Authentic environmental details

Perspective:
- [Street level / Aerial view / Tourist perspective]
- Natural composition
- Photorealistic rendering

Lighting:
- Accurate for specified time ([19:00 = evening, golden hour / dawn = early morning light])
- Proper sun position for coordinates and time
- Realistic shadows and atmospheric effects

Quality: Photorealistic, accurate representation, high detail, authentic atmosphere
```

## Face Detection CCTV Simulation

**Use case:** Security camera aesthetic with face detection overlay

**Template:**
```
Create a high angle CCTV surveillance shot using the uploaded image as the source.

Camera Characteristics:
- High angle view (looking down)
- CCTV security camera perspective
- Slightly noisy and security-camera-like quality:
  * Soft grain
  * Slight distortion
  * Muted colors
  * Lower resolution feel (but still clear)

Face Detection Graphics:
Detect every visible person in the image:
- Draw white rectangular bounding box around each face
- Boxes should be:
  * Clean, thin white lines
  * Just large enough to frame face
  * Aligned with face angle

Zoom-In Inset (Most Prominent Person):
- Large enhanced close-up of their face
- Displayed in floating rectangular frame
- Connected to main face box with thin white line
- Inset characteristics:
  * Clearer than main image
  * Brighter and more detailed
  * Sharp and enhanced
  * Higher contrast

Visual Hierarchy:
- Main image: Slightly noisy CCTV quality
- Zoom inset: Clear, enhanced, detailed
- Both maintaining same color palette

Restrictions:
- No text overlays
- No timestamps
- No UI elements except boxes and connecting lines
- No status indicators

Layout:
- Maintain original scene layout
- Keep original camera angle from source
- Preserve environment
- Inset positioned to not obscure important elements

Quality: CCTV surveillance aesthetic with modern face detection overlay
```

## Wide Angle Phone Screen Replacement

**Use case:** Edit photo with extreme wide-angle AND replace phone screen with different image

**Template (JSON):**
```json
{
  "edit_type": "extreme_wide_angle_phone_edit",
  "source": {
    "mode": "EDIT",
    "preserve_elements": ["Person", "Face", "Hairstyle", "Clothing", "Environment style"],
    "camera_transformation": {
      "new_lens": "Ultra-wide or fisheye (12-18mm equivalent)",
      "angle_options": [
        "Looking up from directly in front",
        "Looking down from directly in front",
        "Extreme low angle",
        "High angle",
        "Tilted composition"
      ],
      "perspective_effect": "Nearby objects exaggerated, distant objects smaller",
      "emphasized_body_parts": {
        "count": "1-3 body parts extremely close to camera",
        "options": ["Hands", "Feet/shoes", "Knees/thighs", "Face", "Shoulders"]
      }
    },
    "phone_handling": {
      "person_holds_phone": true,
      "grip_options": [
        "One-handed",
        "Two-handed",
        "Low angle",
        "High angle",
        "Tilted",
        "Sideways",
        "Close to chest",
        "Casual grip"
      ],
      "screen_replacement": {
        "target": "Only the smartphone screen portion",
        "source": "Second reference image provided",
        "fitting_rules": "Strictly match the screen shape, no stretching or compression",
        "interface_rules": "No icons, status bars, or app borders; only display content from original image",
        "perspective_match": "Screen content should match phone's angle and perspective"
      }
    },
    "environment_consistency": {
      "location": "Maintain same location as original",
      "lighting": "Maintain direction and intensity",
      "extension_rules": "Keep same buildings, walls, materials, colors, lighting style"
    }
  },
  "global_restrictions": [
    "No new characters",
    "No changes to age or gender",
    "No clothing changes",
    "No changes to location type",
    "No text, logos, or watermarks added",
    "No illustration or anime style"
  ]
}
```

**Key Requirements:**
- Transform to wide-angle perspective
- Person holds phone in shot
- Phone screen shows different image (from second reference)
- Screen content properly fitted to screen shape
- Maintains perspective correctness
