# Vertical Layout System

## Contents

1. Canvas and safe zones
2. Global visual rules
3. Layout templates
4. Typography
5. Image treatment
6. Motion and transitions
7. Layout rejection checklist

## Canvas And Safe Zones

Design at 1080x1920 and 30 fps.

```text
y=0-120       top platform safety
y=120-330     title / section identity
y=330-1380    primary visual and evidence
y=1380-1620   supporting facts / CTA
y=1620-1780   burned-in caption zone
y=1780-1920   bottom platform safety
```

These are guides, not equal-height boxes. Let a strong product or factory image cross zones when it improves composition. Keep essential text, QR codes, logos, and packaging names inside x=80-1000.

## Global Visual Rules

- Use at least two focal points: for example headline then product, or factory then founding year.
- Anchor content to an edge or a clear grid. Avoid centered floating stacks.
- Aim for a visually occupied frame. Blank space is intentional only when it directs attention.
- Use one tinted neutral background, one dark text color, and one or two brand accents.
- Avoid generic blue glow circles, nested cards, identical card grids, thin web borders, and tiny interface labels.
- Cards are allowed only when they represent a real information unit. They are not the default page structure.
- Give adjacent scenes different silhouettes.
- Keep source photography and packaging legible; do not blur it into atmosphere.

For `compact-standard`, shorten scene holds without shrinking the design:

- use 6-8 scenes with one information job each
- keep the same typography and product-image minimums as standard mode
- place supporting critical facts on screen when narration omits them
- never solve duration pressure by stacking more text into one frame

## Layout Templates

### Cover

Purpose: earn the click and provide a valid frame-0 poster.

- brand/platform marker: 5-8%
- headline: two lines maximum, 64-96 px
- supporting line: one concise benefit or product family
- primary visual: factory, product pair, or article key art occupying 40-55% of the frame
- CTA/trust line: clear, not a tiny button

The cover must be complete at frame 0. Ambient motion may begin later, but no essential element may start at opacity 0.

### Company Profile

Purpose: establish credibility without producing a blank corporate slide.

Preferred compositions:

- factory image across 45-55% of the frame plus a strong fact rail
- split frame with image on one side and 2-3 large facts on the other
- large founding year as a visual anchor with the company image behind or beside it

Do not show only the company name at the top while waiting for later animation.

### Product Hero

Purpose: make the actual product inspectable.

- product image width: normally 65-80% of frame
- remove excessive source-image white margins before placement
- product name and dosage form are separate hierarchy levels
- show at most 2-3 concise fact tags
- alternate left/right or top/bottom composition for adjacent products

Do not place a small product image inside a large empty white card.

### Fact Focus

Purpose: communicate a number, qualification, platform benefit, or comparison.

- one large number or statement
- one evidence line
- optional supporting image or diagram
- structural rule, marker, or data rail for depth

Do not turn three unrelated facts into three equal cards by habit.

### CTA

Purpose: make the next action unmistakable.

- CTA is the primary focal point
- platform/miniprogram identity is visible
- QR or entry image, when supplied, stays unobstructed
- disclaimer has its own readable zone
- use a strong compositional ending rather than a generic centered card

## Typography

At 1080x1920:

| Role | Typical size |
| --- | ---: |
| Cover headline | 84-108 px |
| Scene headline | 72-96 px |
| Product name | 76-104 px |
| Large number | 112-180 px |
| Body / fact | 36-48 px |
| Label | 30-34 px |
| Captions | 44-54 px |
| Disclaimer | 28-34 px |

Use strong weight contrast. Keep body lines short. Fit long Chinese names dynamically instead of shrinking every title globally.

## Image Treatment

For each asset record:

```json
{
  "path": "source/images/product.jpg",
  "subject": "示例滴眼液包装和滴眼瓶",
  "crop": "contain",
  "vertical_safety": "safe",
  "focal_point": "center",
  "minimum_width_pct": 68,
  "risks": ["source contains wide white margins"]
}
```

- `contain`: packaging, screenshots, charts, QR codes
- `cover`: factory/environment photos where cropping is acceptable
- `cutout`: product assets with removable white background

When source images have large white margins, crop the margins nondestructively before layout. Never stretch a horizontal image to 9:16.

## Motion And Transitions

- Main information must be visible by 0.4 seconds.
- Keep product visible from scene entry; animate scale or position for emphasis.
- Use 0.3-0.6 second entrances with overlap.
- Alternate motion direction and emphasis across scenes.
- Keep captions stable while visuals move.
- Use 0.2-0.45 second transitions; transitions must not create black frames.
- Every scene's static end-state must already be a good poster.

## Layout Rejection Checklist

Reject and revise when any answer is yes:

- Is the lower half of the frame mostly unused?
- Does the product look like a thumbnail?
- Does the first half-second show only a label or heading?
- Are two adjacent scenes compositionally identical?
- Does the page resemble a website card stack or presentation slide?
- Is the subtitle smaller than surrounding secondary copy?
- Does the subtitle cover packaging, QR, CTA, or disclaimer?
- Is important text within 80 px of the left/right edge or 120 px of top/bottom?
- Does animation need to finish before the frame makes sense?
