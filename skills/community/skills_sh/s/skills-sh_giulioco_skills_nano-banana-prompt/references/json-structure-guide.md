# JSON Structure Guide

## When to Use JSON Format

JSON prompts provide precise control for complex image generation tasks. Use JSON when:

1. **Multiple elements require detailed specification**
   - Different accessories with specific properties
   - Complex wardrobe with multiple pieces
   - Scene with many distinct objects

2. **Era-specific aesthetics**
   - Y2K, 2000s, 1990s styles
   - Period-accurate details across multiple categories
   - Nostalgic recreations

3. **Complex scenes with multiple subjects**
   - Group photos with individual styling
   - Multiple poses of same person
   - Interactive scenes

4. **Precise technical requirements**
   - Camera specifications
   - Lighting setups
   - Rendering parameters

5. **Multi-layered compositions**
   - Surreal effects with multiple realms
   - Complex editing operations
   - Layered artistic effects

## Core JSON Structure

### Basic Template

```json
{
  "subject": {
    "description": "Main subject description",
    "face": {
      "preserve_original": true,
      "reference_match": true
    },
    "hair": {
      "color": "color value",
      "style": "style description"
    },
    "clothing": {
      "top": {
        "type": "garment type",
        "color": "color",
        "details": "specific details"
      },
      "bottom": {
        "type": "garment type",
        "fit": "fit description"
      }
    },
    "expression": "expression description"
  },
  "accessories": {
    "jewelry": {
      "type": "jewelry type",
      "details": "specific details"
    },
    "other": "additional accessories"
  },
  "photography": {
    "camera_style": "camera type",
    "lighting": "lighting description",
    "angle": "camera angle",
    "shot_type": "framing type",
    "texture": "texture and grain"
  },
  "background": {
    "setting": "location description",
    "elements": [
      "element 1",
      "element 2",
      "element 3"
    ],
    "atmosphere": "mood description",
    "lighting": "lighting style"
  },
  "negative": {
    "content": "elements to avoid",
    "style": "style elements to avoid"
  }
}
```

## Era-Specific Templates

### 2000s Mirror Selfie

```json
{
  "subject": {
    "description": "Young woman taking mirror selfie",
    "age": "young adult",
    "expression": "confident and slightly playful",
    "hair": {
      "color": "dark / blonde / red",
      "style": "very long voluminous waves with soft wispy bangs / straightened with side part / messy bun"
    },
    "clothing": {
      "top": {
        "type": "fitted cropped t-shirt / baby tee / tank top",
        "color": "cream white / pink / baby blue",
        "details": "cute graphic (anime character, band logo, butterfly, etc.)"
      },
      "bottom": {
        "type": "low-rise jeans / mini skirt / cargo pants",
        "fit": "form-fitting / relaxed",
        "color": "blue denim / black / khaki"
      }
    },
    "face": {
      "preserve_original": true,
      "makeup": "natural glam makeup with soft pink dewy blush and glossy lips in [color]"
    }
  },
  "accessories": {
    "earrings": {
      "type": "gold geometric hoops / butterfly clips / small studs"
    },
    "jewelry": {
      "necklace": "choker / layered thin chains / pendant",
      "waistchain": "silver waistchain",
      "rings": "multiple thin rings"
    },
    "hair_accessories": [
      "butterfly clips",
      "claw clip",
      "thin headband"
    ],
    "device": {
      "type": "smartphone / flip phone / digital camera",
      "details": "patterned case / bedazzled / stickered"
    }
  },
  "photography": {
    "camera_style": "early-2000s digital camera aesthetic",
    "lighting": "harsh super-flash with bright blown-out highlights but subject still visible",
    "angle": "mirror selfie",
    "shot_type": "tight selfie composition / 3/4 body",
    "texture": "subtle grain, retro highlights, crisp details, soft shadows"
  },
  "background": {
    "setting": "nostalgic early-2000s bedroom",
    "wall_color": "pastel tones (pink, blue, lavender, mint)",
    "elements": [
      "chunky wooden dresser",
      "CD player / portable CD player",
      "posters of 2000s pop icons (Britney, NSYNC, etc.)",
      "hanging beaded door curtain",
      "cluttered vanity with lip glosses and body sprays",
      "fairy lights",
      "lava lamp (optional)",
      "inflatable furniture (optional)"
    ],
    "atmosphere": "authentic 2000s nostalgic vibe",
    "lighting": "retro, warm bedroom lighting"
  }
}
```

### Y2K Scrapbook Collage

```json
{
  "facelock_identity": "true",
  "accuracy": "100%",
  "scene": "Colorful Y2K scrapbook poster aesthetic, vibrant stickers, multiple subjects wearing same outfit and hairstyle with different poses and cutouts, colorful strokes and lines, frameless collage style",
  "main_subject": {
    "description": "Young Y2K-styled person as main focus in center of scrapbook collage",
    "style_pose": "Playful and confident Y2K pose",
    "multiple_poses": [
      "close-up shot with heart-shape fingers",
      "full-body squatting pose supporting chin while holding white polaroid camera",
      "mid-shot touching cheek while blowing pink bubblegum",
      "mid-shot smiling elegantly while holding a cat",
      "seated elegantly with one eye winking and peace sign",
      "mid-shot holding daisy flowers"
    ],
    "outfit": {
      "top": "Cropped oversized sweater in pastel color with embroidered patches / Y2K graphic tee",
      "bottom": "pastel skirt / cargo pants with white belt",
      "socks": "White ankle socks with colorful pastel stripes",
      "shoes": "white sneakers / platform shoes",
      "accessories": [
        "Colorful plastic bracelets",
        "Chunky colorful rings",
        "Sparkling belly chain"
      ]
    },
    "hairstyle": {
      "type": "Y2K half-up half-down",
      "details": "Pastel flower clips, thin front tendrils, wavy hair with bubblegum-pink tint on lower strands"
    }
  },
  "additional_visuals": [
    "Heart, star, and butterfly stickers",
    "Retro sparkles",
    "Polaroid frames",
    "Neon outlines",
    "Doodle borders",
    "Magazine cutout texts: 'SO CUTE!', '199X!', 'GIRL VIBES'",
    "Pastel lighting",
    "Glossy dreamy retro glow",
    "Holographic textures",
    "Pastel gradients",
    "Glitter accents",
    "Playful doodles"
  ],
  "photography_rendering": {
    "color_grading": "Cinematic neon Y2K",
    "lighting": "Soft flash lighting",
    "skin_texture": "Smooth glossy finish",
    "rendering": "High-detail hyperrealistic Y2K scrapbook tone",
    "quality": "8K",
    "composition": "Perfectly balanced and artistic, chaotic yet balanced layout"
  },
  "negative_prompt": "no realism that breaks Y2K aesthetic, no modern 2020s clothing, no messy composition, no blurry face, no distorted hands, no extra limbs, no face warping, no low resolution, no grain, no muted colors, no watermark, no AI artifacts"
}
```

### 1990s Film Camera Aesthetic

```json
{
  "image_parameters": {
    "style": "Canon IXUS / point-and-shoot aesthetic",
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
      "style": "Long, natural, lightly messy layered look / Short bob / Curtain bangs",
      "movement": "Blowing gently / Static",
      "details": "Strands slightly covering part of face / Tucked behind ear"
    },
    "makeup": {
      "cheeks_and_nose": "Soft pink/peach blush with blurred effect",
      "lips": "Subtle pink-orange/red tinted outline / Glossy"
    },
    "expression": [
      "Cute",
      "Candid",
      "Cheerful",
      "Playful"
    ],
    "pose": {
      "body_position": "Half-sitting, half-standing / Leaning against wall / Casual stance",
      "action": "Flicking hair / Looking over shoulder / Natural gesture"
    },
    "clothing": {
      "top": "Vintage band tee / Flannel shirt / Oversized sweater",
      "bottom": "Mom jeans / Cargo pants / Plaid skirt"
    },
    "accessories": [
      "Choker necklace",
      "Small pendant",
      "Scrunchie",
      "Watch"
    ]
  },
  "environment": {
    "setting": "Bedroom / Dorm room / Living room at night",
    "foreground_props": [
      "Wooden furniture",
      "Vintage electronics (CRT TV, boom box)",
      "Magazines",
      "Posters on wall"
    ]
  },
  "camera_specs": {
    "camera": "Compact digital camera simulation (Canon IXUS, Nikon Coolpix era)",
    "lens": "equivalent to 28-35mm",
    "aperture": "f/2.8",
    "iso": "400",
    "shutter_speed": "1/60 with flash",
    "white_balance": "auto flash",
    "lighting": "harsh direct flash on subject, ambient low light in background",
    "color_grading": "nostalgic digital-camera tones, high contrast flash, subtle display grain, slight yellow/cool tint"
  }
}
```

## Complex Scene Templates

### Multi-Realm Surreal Composition

```json
{
  "meta": {
    "type": "Hyper-realistic Surrealism",
    "genre": "Composite Multi-Realm",
    "composition_style": "Layered Reality"
  },
  "realm_physical": {
    "description": "Real-world environment",
    "environment": {
      "surface": "Surface description (wooden table, concrete, grass)",
      "texture_attributes": ["grain", "tactile", "worn"]
    },
    "lighting_global": {
      "source": "Light source (natural, artificial)",
      "temperature": "Warm / Cool / Neutral",
      "quality": "Soft / Hard / Diffused"
    },
    "objects": [
      {
        "item": "Object name",
        "position": "Position in scene",
        "state": "Condition/status",
        "action": "What it's doing"
      }
    ]
  },
  "realm_digital": {
    "description": "Digital/screen content",
    "container_device": {
      "model": "Device model",
      "state": "Screen ON/OFF",
      "orientation": "Position"
    },
    "screen_content": {
      "subject_identity": "Person from reference",
      "subject_scale": "Framing",
      "expression": "Emotion",
      "setting": "Environment",
      "elements": ["Element 1", "Element 2"]
    }
  },
  "surreal_bridge_event": {
    "description": "Interaction connecting realms",
    "action_type": "Type of physics violation",
    "source": "Origin realm/element",
    "interaction_point": "Where realms meet",
    "destination": "Target realm/element",
    "physics_violation_rules": {
      "rule_1": "What impossible thing happens",
      "rule_2": "How physics is broken",
      "rule_3": "Transition behavior"
    },
    "visual_details": [
      "Specific visual effect 1",
      "Specific visual effect 2"
    ]
  },
  "rendering_specifications": {
    "visual_fidelity": "Hyper-realistic",
    "texture_focus": ["Texture 1", "Texture 2"],
    "mood": "Overall atmosphere",
    "resolution_target": "8K / 4K"
  }
}
```

### Fisheye/Wide Angle Portrait

```json
{
  "scene": {
    "environment": "Location description",
    "details": "Environmental elements",
    "lighting": "Light type and time",
    "sky": "Sky description"
  },
  "camera": {
    "lens": "ultra_wide_fisheye_12mm / fisheye_15mm",
    "distance": "very_close_up / close_up",
    "distortion": "strong_exaggeration / heavy_barrel_distortion",
    "angle": "slightly_low_upward / eye_level / high_angle"
  },
  "subject": {
    "type": "Person description",
    "expression": "Facial expression",
    "eyes": "large_due_to_lens_distortion / natural",
    "pose": "Body position and action",
    "clothing": {
      "top": "Top garment",
      "accessory": "Accessories visible"
    }
  },
  "distortion_effects": {
    "face": "Appears larger, closer",
    "hands": "Exaggerated if reaching toward camera",
    "background": "Curves away, barrel distortion",
    "edges": "Stretched and warped"
  },
  "effects": {
    "depth_of_field": "shallow_foreground_sharp_background_soft",
    "reflections": "If glasses/reflective surfaces present",
    "color_grade": "clean_natural / warm_nostalgic / high_contrast",
    "grain": "film_grain / digital_clean"
  },
  "composition": {
    "focus": "face_extreme_closeup / full_body_distorted",
    "mood": "funny_intimate_casual / dramatic / playful"
  }
}
```

## Advanced Editing Operations

### Torn Paper Effect

```json
{
  "task": "edit-image: add torn-paper layered effect",
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
      "placement": "Location description (e.g., across chest height)",
      "description": [
        "Add a wide, natural horizontal tear",
        "The torn interior uses the style defined in interior_style"
      ]
    }
  ],
  "interior_style": {
    "mode": "line-art / sumi-e / watercolor / pencil-drawing / colored-pencil",
    "style_settings": {
      "line-art": {
        "palette": "monochrome",
        "line_quality": "clean, crisp",
        "paper": "notebook paper with subtle ruled lines"
      },
      "watercolor": {
        "palette": "soft transparent pigments",
        "blending": "smooth bleeding",
        "edges": "soft contours",
        "paper": "watercolor paper texture"
      }
    }
  },
  "torn_edge_characteristics": {
    "edge_quality": "natural, irregular tears",
    "depth_effect": "realistic paper thickness visible",
    "shadow": "subtle shadow inside tear"
  }
}
```

### Wide Angle Phone Screen Edit

```json
{
  "edit_type": "extreme_wide_angle_phone_edit",
  "source": {
    "mode": "EDIT",
    "preserve_elements": ["Person", "Face", "Hairstyle", "Clothing", "Environment style"],
    "change_rules": {
      "camera_angle": "Ultra-wide or fisheye lens (12-18mm)",
      "angle_options": [
        "Looking up from directly in front",
        "Looking down from directly in front",
        "Extreme low angle",
        "High angle",
        "Tilted composition"
      ],
      "perspective_effect": "Nearby objects exaggerated, distant objects smaller",
      "body_parts_close_to_camera": "1-3 body parts extremely close",
      "body_part_options": ["Hands", "Feet/shoes", "Knees/thighs", "Face", "Shoulders/chest"],
      "pose_variety": [
        "Extending hand/leg toward camera",
        "Squatting or lying halfway",
        "Sitting on ground or object",
        "Leaning sharply toward camera",
        "Twisting body for dynamic pose"
      ]
    },
    "phone_handling": {
      "allowed": true,
      "grip_options": ["One-handed", "Two-handed", "Low angle", "High angle", "Tilted"],
      "screen_replacement": {
        "target": "Only the smartphone screen portion",
        "source": "Second reference image",
        "fitting_rules": "Strictly match screen shape, no stretching",
        "interface_rules": "No icons, status bars; only image content"
      }
    }
  },
  "global_restrictions": [
    "No new characters",
    "No age/gender changes",
    "No clothing changes",
    "No location type changes",
    "No text/logos/watermarks added"
  ]
}
```

## Technical Specification Templates

### Professional Portrait with Full Specs

```json
{
  "subject": {
    "identity_preservation": {
      "source": "reference image",
      "accuracy": "100% facial features",
      "maintain": ["bone structure", "skin tone", "eye color", "facial proportions"]
    },
    "styling": {
      "outfit": "Professional business suit in navy blue",
      "shirt": "White dress shirt",
      "grooming": "Well-groomed, professional"
    }
  },
  "photography": {
    "camera": {
      "model": "Sony A7III",
      "sensor": "35mm full-frame"
    },
    "lens": {
      "focal_length": "85mm",
      "aperture": "f/1.4",
      "effect": "flattering portrait compression"
    },
    "settings": {
      "shutter_speed": "1/125s",
      "iso": "200",
      "white_balance": "5500K daylight"
    }
  },
  "lighting": {
    "setup": "three-point lighting",
    "key_light": {
      "type": "softbox",
      "position": "45 degrees camera left",
      "intensity": "main illumination",
      "effect": "soft defining shadows on face"
    },
    "fill_light": {
      "type": "reflector or soft fill",
      "position": "camera right",
      "intensity": "1/2 key light",
      "effect": "soften shadows"
    },
    "rim_light": {
      "type": "small strobe with grid",
      "position": "behind subject",
      "intensity": "subtle",
      "effect": "separate subject from background"
    },
    "eye_light": {
      "type": "ring flash or catchlight panel",
      "effect": "natural catchlights in eyes"
    }
  },
  "background": {
    "type": "solid studio backdrop",
    "color": "#562226",
    "gradient": "subtle gradient, lighter behind subject, darker at edges",
    "vignette": "gentle vignette effect"
  },
  "rendering_requirements": {
    "skin": "natural texture with visible pores, not airbrushed",
    "fabric": "show subtle wool texture on suit",
    "hair": "individual strand definition",
    "eyes": "sharp focus with catchlights",
    "overall": "ultra-realistic, 8K professional headshot"
  },
  "composition": {
    "framing": "chest up with ample headroom",
    "gaze": "directly at camera",
    "depth_of_field": "shallow, soft bokeh background",
    "focus_point": "eyes critically sharp"
  },
  "color_grading": {
    "overall": "clean cinematic color grading",
    "tone": "balanced with subtle warmth",
    "saturation": "natural, not oversaturated",
    "contrast": "professional, balanced"
  }
}
```

## Best Practices

### JSON Formatting
- Use proper JSON syntax (validated)
- Consistent indentation (2 or 4 spaces)
- Use arrays for lists
- Use objects for grouped properties
- Include comments in "description" fields

### Organization
- Group related properties
- Use hierarchical structure
- Separate major sections (subject, photography, background, etc.)
- Keep technical specs together

### Specificity
- Be precise with measurements and values
- Use exact color codes when possible (#hexcodes)
- Specify camera models and lens specs
- Include negative prompts

### Consistency
- Use consistent naming conventions
- Maintain same structure across similar prompts
- Group photography specs in same location
- Keep identity preservation rules at top

### Testing & Iteration
- Start with simpler JSON, add complexity
- Test one new element at a time
- Document what works well
- Refine based on results
