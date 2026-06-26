# Launch Teaser Templates

Building anticipation for product launches, feature drops, or brand reveals. Designed for "coming soon" energy.

## Countdown Teaser (4-8s)
Quick mystery reveal — perfect for a series of teasers leading up to launch.

```
Use case: launch teaser
Primary request: mysterious partial reveal of [PRODUCT/FEATURE/BRAND]
Scene/background: dark environment, emerging light, sense of anticipation
Subject: partially obscured [PRODUCT] — silhouette, shadow, single detail lit
Action: slow reveal — light gradually illuminates a portion, then cuts before full reveal
Camera: 1280x720, tight crop, slow push-in
Lighting/mood: dramatic, mysterious, building anticipation
Color palette: dark base, [1 BRAND ACCENT COLOR] as reveal light
Constraints: 4-8 seconds; never show the full product; leave viewer wanting more
Avoid: full product reveal; bright environments; casual feel
```

### CLI command:
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Mysterious silhouette of [PRODUCT], single accent light revealing one edge" \
  --use-case "launch teaser" \
  --scene "pitch dark, single beam of light" \
  --camera "tight crop, slow push-in" \
  --lighting "dramatic, single accent light" \
  --palette "black, [BRAND ACCENT]" \
  --seconds 4
```

## "Something's Coming" (8-12s)
Abstract energy building — no product shown at all.

```
Use case: launch teaser
Primary request: abstract energy building toward a moment of [REVEAL/ARRIVAL/TRANSFORMATION]
Scene/background: starts empty/minimal, fills with motion/energy
Subject: particles, light, abstract forms gathering and converging
Action: beat 1 (0-4s) stillness, single element; beat 2 (4-8s) energy gathers, motion builds; beat 3 (8-12s) convergence toward a point, hold at peak tension — don't resolve
Camera: 1280x720, starts wide, slowly tightens as energy builds
Lighting/mood: starts dim, builds to vibrant; tension without release
Color palette: [BRAND COLORS], building intensity
Constraints: 8-12 seconds; NO product; pure anticipation; end at peak tension
Avoid: resolution; reveal; calm endings; literal imagery
```

## Feature Drop (8-16s)
Reveal a specific new feature or capability.

```
Use case: feature announcement
Primary request: dramatic reveal of [FEATURE] capability
Scene/background: clean, focused environment highlighting the feature
Subject: [FEATURE visualization: speed → blur to sharp / scale → small to vast / precision → chaos to order]
Action: problem state → transformation → feature-enabled state
Camera: 1280x720, match motion to feature (fast feature = fast camera)
Lighting/mood: starts constrained, opens up with feature reveal
Color palette: [BRAND COLORS], before=muted / after=vibrant
Constraints: 8-16 seconds; feature must be visually obvious; no text
Avoid: multiple features at once; subtle reveal; anti-climax
```

## Launch Day (12-20s)
The big reveal — full product or brand unveiling.

```
Use case: product launch
Primary request: grand reveal of [PRODUCT/BRAND] — this is the moment
Scene/background: dramatic environment, designed for impact
Subject: [PRODUCT] in its full glory
Action: beat 1 (0-4s) anticipation build, final tension; beat 2 (4-8s) reveal moment — light, motion, arrival; beat 3 (8-16s) product hero moment — beauty shots, angles; beat 4 (16-20s) settle into confident, resolved state
Camera: 1280x720 or 1920x1080 (sora-2-pro), cinematic multi-angle feel
Lighting/mood: dramatic reveal → premium confidence
Color palette: [FULL BRAND PALETTE], peak vibrancy
Constraints: 12-20 seconds; this IS the full reveal; premium quality mandatory
Avoid: anticlimactic reveal; too many elements; rushed pacing
```

## Teaser Series Pattern
For maximum impact, generate a series of teasers leading to launch:

| Timing | Template | Duration | What Shows |
|--------|----------|----------|-----------|
| T-14 days | "Something's Coming" | 8s | Abstract energy, no product |
| T-10 days | Countdown Teaser #1 | 4s | Single material detail |
| T-7 days | Countdown Teaser #2 | 4s | Shape silhouette |
| T-3 days | Countdown Teaser #3 | 4s | Near-reveal, one feature visible |
| T-1 day | Feature Drop | 8s | Key feature demo |
| Launch Day | Launch Day | 16-20s | Full hero reveal |

## Usage Notes
- Teasers work best in series — plan the full arc
- Use `sora-2` for teaser iterations, `sora-2-pro` for final launch day video
- Keep teasers SHORT (4-8s) — social platforms favor brief content
- Generate 5+ variants per teaser, pick the most mysterious
- Never show more than intended — discipline drives anticipation
- Use `extend` to build a teaser into a longer launch day video
