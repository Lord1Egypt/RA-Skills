# Brand Spot Templates

Medium-form videos (8-20s) for brand identity, company culture, and brand storytelling. These are the "who we are" videos.

## Brand Essence (12-16s)
Captures the core feeling of the brand.

```
Use case: brand identity
Primary request: visual metaphor for [BRAND VALUE: innovation / craftsmanship / sustainability / connection]
Scene/background: [ENVIRONMENT that evokes brand]: modern architecture / natural landscape / workshop / urban pulse
Subject: abstract or symbolic — light, water, texture, motion
Action: beat 1 (0-4s) establish environment; beat 2 (4-8s) reveal symbolic element; beat 3 (8-12s) element transforms or evolves; beat 4 (12-16s) settle into resolved, balanced state
Camera: cinematic 1280x720, mixed focal lengths, fluid motion
Lighting/mood: [BRAND MOOD: warm and human / cool and precise / natural and honest]
Color palette: [BRAND COLORS], graded for cinematic feel
Constraints: no people; no text; no product; pure brand feeling; 12-16 seconds
Avoid: literal product shots; corporate stock feel; generic imagery
```

### CLI command:
```bash
uv run --with openai python "$SORA_CLI" create-and-poll \
  --prompt "Visual metaphor for craftsmanship — hands of light shaping raw material into refined form" \
  --use-case "brand identity" \
  --scene "warm workshop, golden hour light through dusty windows" \
  --camera "cinematic, fluid dolly, shifting focal lengths" \
  --lighting "warm, natural, golden" \
  --palette "amber, warm grey, cream" \
  --seconds 16 \
  --download \
  --out brand-essence.mp4
```

## Culture Vignette (8-12s)
Abstract representation of company culture.

```
Use case: brand culture
Primary request: abstract representation of [CULTURE THEME: collaboration / creativity / precision / growth]
Scene/background: spaces that suggest human activity without showing people
Subject: objects in motion, workspaces, tools, organic processes
Action: gentle, contemplative movement — things coming together, aligning, growing
Camera: 1280x720, slow tracking shots, observational
Lighting/mood: natural, authentic, unposed
Color palette: [BRAND COLORS], muted, warm
Constraints: 8-12 seconds; no people; no text; workplace adjacent but abstract
Avoid: corporate clichés; sterile offices; handshakes; sticky notes on glass
```

## Origin Story (16-20s)
Visual journey from beginning to present.

```
Use case: brand story
Primary request: visual journey from [ORIGIN: raw material / seed / spark] to [CURRENT STATE: refined product / growing forest / bright creation]
Scene/background: transitions from raw/simple to refined/complex
Subject: transformation of a symbolic element over time
Action: continuous transformation arc — rough to refined, small to expansive, simple to complex
Camera: 1280x720, evolving perspective — starts tight, gradually widens
Lighting/mood: starts moody/raw, evolves to bright/confident
Color palette: evolves from [MUTED] to [VIBRANT BRAND COLORS]
Constraints: 16-20 seconds; single continuous take feel; no people; no text
Avoid: jump cuts; literal timelines; before/after split screen
```

## Values Montage Element (4-8s each)
Individual clips representing each brand value. Designed to be used as standalone elements or edited together.

```
Use case: brand values
Primary request: visual representation of [VALUE: trust / quality / speed / care / innovation]
Scene/background: environment that embodies the value
Subject: symbolic action or object
Action: single clear motion or transformation that represents the value
Camera: 1280x720, consistent style across all values
Lighting/mood: consistent brand-aligned lighting
Color palette: [BRAND COLORS]
Constraints: 4-8 seconds; one value per clip; no text; consistent visual language
Avoid: literal interpretation; cliché symbols (lightbulbs for innovation, etc.)
```

## Usage Notes
- Use `sora-2-pro` for brand spots — quality matters more than speed
- Generate at 1920x1080 for hero brand content (requires `sora-2-pro`)
- Create 2-3 variants of each spot and curate the best
- Brand spots work best with abstract/symbolic imagery, not literal product shots
- Use `--no-augment` when prompts are already carefully structured
- Consider generating a character reference for recurring brand mascots
