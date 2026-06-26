# Image Prompting Quick Reference

Photography parameters and style presets for AI image generation. Use with the 5-part framework in the main skill.

## Photography Parameters

### Lighting

| Description | Camera term | Best for |
|-------------|------------|----------|
| Warm, golden, inviting | "Golden-hour light, 4500K colour temperature" | Hospitality, wellness, food |
| Bright, even, clean | "Overhead softbox, even fill, 5500K daylight" | Product shots, clinical |
| Dramatic, moody | "Single key light at 45°, deep shadows, 3200K" | Portraits, luxury |
| Natural, soft | "Diffused window light, overcast daylight" | Lifestyle, editorial |
| Studio | "Three-point lighting: key, fill, and hair light" | Headshots, formal |

### Lens / Focal Length

| Focal length | Effect | Best for |
|-------------|--------|----------|
| 24mm | Wide angle, environmental context | Interiors, landscapes, establishing shots |
| 35mm | Moderate wide, natural perspective | Street, documentary, environmental portraits |
| 50mm | Standard, closest to human eye | General purpose, product-in-context |
| 85mm | Portrait lens, background compression | Headshots, beauty, food close-ups |
| 100mm+ | Telephoto, strong background blur | Detail shots, product isolation |

### Aperture (Depth of Field)

| f-stop | Effect | Use when |
|--------|--------|----------|
| f/1.4–f/2.0 | Very shallow DOF, creamy bokeh | Subject isolation, portraits |
| f/2.8–f/4.0 | Moderate DOF, soft background | Most commercial photography |
| f/5.6–f/8.0 | Deep DOF, most things sharp | Environmental shots, interiors |
| f/11–f/16 | Everything sharp | Architecture, landscapes |

### Camera Angle

| Angle | Effect | Best for |
|-------|--------|----------|
| Eye level | Natural, relatable | Portraits, conversational |
| Slightly elevated (15-30°) | Hero framing, authority | Business headshots, products |
| Low angle (looking up) | Power, grandeur | Architecture, hero shots |
| Overhead / flat lay | Organised display | Food, products, desk setup |
| 45° elevated | Documentary feel | Workshop, process shots |

## Style Presets

Repeat these keywords across all images in a set for visual consistency:

### Modern Clean
```
modern photography, clean composition, minimal background,
soft focus background, crisp detail, high contrast
```
Best for: Tech companies, agencies, SaaS

### Editorial Warm
```
editorial style, warm natural light, inviting atmosphere,
lifestyle photography, golden hour warmth
```
Best for: Hospitality, wellness, food, real estate

### Bold Industrial
```
documentary photography, dramatic lighting, work in progress,
authentic moment, high contrast, gritty texture
```
Best for: Trades, construction, manufacturing

### Minimal Elegant
```
elegant composition, refined lighting, sophisticated palette,
premium quality, controlled soft diffused light
```
Best for: Luxury brands, boutique services, fashion

## Colour Anchoring

Anchor the colour palette explicitly when generating multiple images:

```
Colour palette: warm terracotta (#C66A52), cream, natural wood.
Background should include terracotta-toned elements to maintain
brand consistency across all images.
```

List 3-4 specific colours or materials. The model picks these up more reliably than abstract terms like "warm tones".

## Aspect Ratios by Platform

| Platform / Use | Ratio | Gemini imageSize |
|---------------|-------|-----------------|
| Website hero (wide) | 16:9 | 2K |
| Website hero (ultra-wide) | 21:9 | 2K |
| Service card | 4:3 | 1K |
| Instagram post | 1:1 | 1K |
| Instagram story | 9:16 | 2K |
| LinkedIn post | 1.91:1 | 1K |
| OG image | 1.91:1 | 1K |
| Profile picture | 1:1 | 1K |
| Pinterest pin | 2:3 | 2K |
| Facebook cover | 2.63:1 | 2K |

## Negative Guidance (Always Include)

End every prompt with constraints. These prevent the most common AI image artifacts:

```
No text, no watermarks, no logos, no writing of any kind.
No extra fingers, no floating objects.
Photorealistic, not illustration or cartoon.
```

For specific domains, add targeted negatives:

| Domain | Add to negatives |
|--------|-----------------|
| Trade/construction | "No hard hat for indoor residential work, no tools left on ladder" |
| Medical/clinical | "No visible patient identification, no non-sterile items in sterile field" |
| Food | "No plastic utensils, no paper plates (unless street food)" |
| Real estate | "No people in the frame, no personal items visible" |
| Australian context | "No American-style architecture, no snow, no fall foliage" |
