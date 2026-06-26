# Layout Archetypes — Reference Examples

**This file is a vocabulary list, NOT a built-in mode.** The skill no longer has a "jazzed up" auto-mode — producing rich/varied/dramatic compositions well requires visual judgment that doesn't reduce to a programmatic recipe, and the skill's auto-attempts at it consistently produced amateur output.

**Use this file ONLY when the user supplies a reference image that uses one of these patterns.** When you study a user-supplied reference, you may recognize one of these archetypes; the descriptions below give you a vocabulary for analyzing and replicating it. Don't pick from this file as a free-form choice — it should always be in response to "this is what the reference is doing."

Six layouts + techniques that show up in real App Store campaigns. If a user-supplied reference uses one of these, the description here helps you describe what you're seeing back to the user before designing.

All examples assume a 1290×2796 stage. Coordinates and font sizes are approximate; tune per brand. The strict safe-zone rule from `render-pipeline.md` applies to every example: load-bearing text and readable product UI stay inside y=180..2616. Decorative background color, blur, and non-readable texture may extend outside that range; critical claims and usable app UI may not.

**Default device dimensions:** 1000px wide (≈ 78% of canvas), height ≈ 2168px at native iPhone 15/16 aspect (393/852). Fits fully within the canvas at top=580 (rounded bottom corners visible). For bleed variants, push top to ≥ 819. If you find yourself sizing devices below 800px wide, the layout is wrong, not the device — rework it.

---

## 1. Floating Device

The workhorse. Phone screen sits centered or slightly off-center on a splash background, with a headline above. Use for value and feature screens (positions 2-4 in the arc).

```
┌─────────────────────────────┐
│                             │
│   Big bold headline here    │  ← top ~25% (clear of status bar)
│   small subhead if any      │
│                             │
│        ┌─────────────┐      │
│        │             │      │  ← phone screen, ~70% width
│        │   PHONE     │      │     centered or slight tilt
│        │   FRAME +   │      │
│        │   APP UI    │      │
│        │             │      │
│        └─────────────┘      │
│                             │
└─────────────────────────────┘
```

**HTML skeleton:**

```html
<div class="stage" style="
  width: 1290px; height: 2796px;
  background: var(--brand-bg);
  position: relative;
  font-family: 'BrandDisplay', sans-serif;
">
  <div class="copy" style="
    position: absolute; top: 180px; left: 80px; right: 80px;
    text-align: center;
  ">
    <h1 style="font-size: 140px; line-height: 0.95; margin: 0; color: var(--brand-ink);">
      Sleep like you mean it.
    </h1>
  </div>

  <div class="device" style="
    position: absolute;
    top: 720px;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
  ">
    <!-- iPhone frame SVG wrapping the screenshot — see render-pipeline.md -->
  </div>
</div>
```

**When to use:** the headline does the storytelling, the device confirms it visually.

---

## 2. Full-Bleed UI

Phone canvas feels oversized and immersive, but the readable product UI remains inside the safe area. Use for the **hook** screen — biggest, boldest, most "this is the app" moment. If you want edge-to-edge drama, use a blurred or cropped duplicate as decorative background and place the real product UI inside y=180..2616.

```
┌─────────────────────────────┐
│   ┌─────────────────────┐   │
│   │                     │   │
│   │   APP UI FILLS      │   │  ← readable UI stays
│   │   THE SAFE AREA     │   │     inside y=180..2616
│   │                     │   │
│   │                     │   │
│   │   ▓▓▓▓▓▓▓▓▓▓▓       │   │
│   │   ▓ HEADLINE  ▓     │   │  ← typography overlay
│   │   ▓ STRIP    ▓      │   │     bottom 25%
│   │   ▓▓▓▓▓▓▓▓▓▓▓       │   │
│   └─────────────────────┘   │
└─────────────────────────────┘
```

**HTML skeleton:**

```html
<div class="stage" style="width: 1290px; height: 2796px; background: var(--brand-bg); overflow: hidden;">
  <img class="decorative-bg" src="https://cdn.pika.art/.../screenshot.png" style="
    position: absolute; inset: -80px;
    width: calc(100% + 160px); height: calc(100% + 160px);
    object-fit: cover; filter: blur(28px); opacity: 0.18;
  ">
  <img class="product-ui" src="https://cdn.pika.art/.../screenshot.png" style="
    position: absolute; top: 240px; left: 80px;
    width: 1130px; height: 1500px; object-fit: cover;
    border-radius: 88px;
  ">
  <div class="overlay" style="
    position: absolute; bottom: 180px; left: 0; right: 0;
    height: 720px;
    background: linear-gradient(to top, var(--brand-ink) 30%, transparent);
    display: flex; align-items: flex-end; padding: 0 80px 200px;
  ">
    <h1 style="font-size: 160px; line-height: 0.92; color: var(--brand-cream); margin: 0;">
      The one tap night routine.
    </h1>
  </div>
</div>
```

**When to use:** the app UI itself is the wow moment — beautiful state, hero generated output, dramatic data visualization.

---

## 3. Side-by-Side

Device on one side, lifestyle imagery on the other. Headline spans top or bottom. Use when you want to connect the app to a real moment in life — emotional features, social features, anything where context matters.

```
┌─────────────────────────────┐
│   Headline across the top   │
│                             │
│  ┌────────┐  ┌────────────┐ │
│  │        │  │            │ │
│  │ PHONE  │  │ LIFESTYLE  │ │  ← device left,
│  │        │  │ IMAGE      │ │     image right
│  │        │  │            │ │     (or reversed)
│  │        │  │            │ │
│  └────────┘  └────────────┘ │
│                             │
│      subhead if needed      │
└─────────────────────────────┘
```

**HTML skeleton:**

```html
<div class="stage" style="
  width: 1290px; height: 2796px;
  background: var(--brand-cream);
  padding: 200px 60px;
">
  <h1 style="font-size: 130px; line-height: 0.95; margin: 0 0 100px; text-align: center; color: var(--brand-ink);">
    Made for the dinner-table hour.
  </h1>
  <div style="display: flex; gap: 40px; height: 1600px;">
    <div class="device" style="flex: 1;">
      <!-- phone -->
    </div>
    <div class="lifestyle" style="
      flex: 1;
      background-image: url('https://cdn.pika.art/.../lifestyle.png');
      background-size: cover; background-position: center;
      border-radius: 80px;
    "></div>
  </div>
</div>
```

**When to use:** the value is contextual — "for X moment", "with X person", "in X place".

---

## 4. Parallax Stack

Phone in front, a large branded shape or generated image floating behind it. Tilt the phone slightly (3-6°) and offset it from the back layer for depth. Use sparingly — once per campaign max — for the "wow moment" feature screen.

```
┌─────────────────────────────┐
│        Bold headline        │
│                             │
│      ▓▓▓▓▓▓▓▓▓▓▓▓▓          │  ← back layer:
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │     brand shape /
│  ▓▓▓ ┌────────┐ ▓▓▓▓▓       │     generated img
│  ▓▓▓ │        │ ▓▓▓▓▓       │
│  ▓▓▓ │ PHONE  │ ▓▓▓▓▓       │  ← phone tilted ~5°,
│  ▓▓▓ │ (tilted)│▓▓▓▓▓       │     z-index above
│  ▓▓▓ └────────┘ ▓▓▓▓▓       │
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │
│      ▓▓▓▓▓▓▓▓▓▓▓▓▓          │
│                             │
└─────────────────────────────┘
```

**HTML skeleton:**

```html
<div class="stage" style="width: 1290px; height: 2796px; background: var(--brand-bg); position: relative;">
  <h1 style="
    position: absolute; top: 180px; left: 80px; right: 80px;
    text-align: center; font-size: 140px; line-height: 0.95;
    color: var(--brand-ink); margin: 0;
  ">
    Your handwriting, alive.
  </h1>

  <div class="back-layer" style="
    position: absolute; top: 700px; left: 50%;
    transform: translateX(-50%);
    width: 1100px; height: 1700px;
    background-image: url('https://cdn.pika.art/.../brand-shape.png');
    background-size: contain; background-repeat: no-repeat;
  "></div>

  <div class="device" style="
    position: absolute; top: 800px; left: 50%;
    transform: translateX(-50%) rotate(-4deg);
    width: 850px;
    z-index: 2;
    filter: drop-shadow(0 60px 80px rgba(0,0,0,0.25));
  ">
    <!-- phone -->
  </div>
</div>
```

**When to use:** showing off a feature that's hard to capture in a static screenshot (animation, generation, transformation).

---

## 5. Quote Card

Big pulled quote dominates the page, with a small device tucked in a corner. Use exactly once — for the **proof** screen (position 5).

```
┌─────────────────────────────┐
│                             │
│   "                         │
│      A quote that            │
│      sells the app          │
│      better than            │
│      any feature.           │
│                          "  │
│                             │
│   — Source, Publication      │
│                             │
│              ┌─────┐        │
│              │PHONE│ ← small│
│              │     │  20%   │
│              └─────┘        │
└─────────────────────────────┘
```

**HTML skeleton:**

```html
<div class="stage" style="
  width: 1290px; height: 2796px;
  background: var(--brand-accent);
  padding: 280px 100px;
  display: flex; flex-direction: column; justify-content: space-between;
">
  <div>
    <div style="font-size: 240px; line-height: 0.6; color: var(--brand-ink); font-family: serif;">"</div>
    <blockquote style="
      font-size: 110px; line-height: 1.05;
      color: var(--brand-ink); margin: 40px 0 80px;
      font-family: 'BrandDisplay', sans-serif;
    ">
      The first app that didn't ruin my morning.
    </blockquote>
    <cite style="font-size: 42px; color: var(--brand-ink); opacity: 0.7; font-style: normal;">
      — The Verge
    </cite>
  </div>

  <div class="device" style="
    width: 420px;
    align-self: flex-end;
    transform: rotate(-3deg);
  ">
    <!-- phone -->
  </div>
</div>
```

**Quote sourcing:** if the user doesn't have real press, write plausible ones tied to the brand's actual differentiator and attribute to outlets that fit the brand's target audience tier (TechCrunch / Verge / NYT / a specific newsletter / a known reviewer). Stay believable; don't fabricate quotes from real specific people.

**Variant — review stars:** swap the quote with a row of "★★★★★ 4.9 — 12,000 reviews" + a tight subhead. Same layout role.

---

## 6. Floating UI Elements

The signature "jazzed up" move: pull specific UI components *out* of the phone frame and float them in the canvas space with their own shadows and scale. The phone reads as the anchor; the floated element reads as the action. Best for feature screens that have one clear hero interaction (a sent message, a generated result, a notification, a CTA).

```
┌─────────────────────────────┐
│   Headline goes here.       │
│                             │
│         ┌─────────────┐     │
│         │             │     │
│         │   PHONE     │     │  ← phone in frame
│         │   (full)    │     │     fully visible
│   ┌──────────────┐    │     │
│   │ FLOATED UI   │    │     │  ← extracted UI element,
│   │ ELEMENT      │ APP│     │     positioned to overlap
│   │              │    │     │     the phone edge
│   └──────────────┘    │     │
│         │             │     │
│         └─────────────┘     │
└─────────────────────────────┘
```

**How to execute:**

1. **Pick the element.** Look at the source screenshot and find the ONE component that carries the screen's story — a sent chat bubble, a "Specialize" button, a notification card, a single skill tile. Skip anything ambient (status bars, navigation chrome).
2. **Extract or request it.** Prefer a separate component export from the design source, or ask the user for one. If a crop/edit MCP primitive becomes available, use that. Do not make local PIL cropping a default dependency.
3. **Compose the screen.** Place the full phone at the default position (top=580). Place the floated element in front, overlapping the phone edge — usually the bottom or one side — at 1.1–1.4× the size it appears inside the phone (so it reads as "scaled up for emphasis").
4. **Shadow the floated element.** Add a heavier drop-shadow than the phone itself, so the element reads as floating *in front of* the device.

```html
<div class="stage">
  <!-- headline + sub at top -->
  <h1>...</h1>

  <!-- the phone, normal default position -->
  <div class="device" style="top: 580px; width: 1000px; ...">
    <img src="https://cdn.pika.art/.../clean_chat.png">
  </div>

  <!-- the floated UI element, overlapping -->
  <div class="float-ui" style="
    position: absolute;
    bottom: 380px;       /* overlapping the bottom-left of the phone */
    left: 60px;
    width: 580px;        /* ~1.2× the in-phone size */
    transform: rotate(-2deg);
    filter: drop-shadow(0 40px 60px rgba(28,26,24,0.32));
    z-index: 2;
  ">
    <img src="https://cdn.pika.art/.../extracted_chat_bubble.png" style="width: 100%;">
  </div>
</div>
```

**Why this works:** the user's eye lands on the floated element first (it's the brightest, most-defined object), then traces back to the phone as context. Standard editorial hierarchy — "thing on top of thing" reads as importance.

**Pitfalls:**
- **Don't float more than one element per screen.** Two floating things compete and the eye doesn't know where to go.
- **Don't float ambient UI** (status bars, nav). Float something that *does* something — a message, a button, a result.
- **The element must visibly overlap the phone.** If it's just floating in negative space, you've just made the device smaller — bad trade.
- **Vary the overlap direction per screen.** One bottom-left, one top-right, etc. Otherwise the campaign looks formulaic.

**When NOT to use:** if the source screen is dense with content (e.g. a long settings list), there's no single hero element worth extracting — fall back to Floating Device (#1) and let the screen speak for itself.

---

## Picking one per screen

A solid 6-screen mix (jazzed-up mode):

| Position | Role    | Default archetype                            |
| -------- | ------- | -------------------------------------------- |
| 1        | Hook    | Full-Bleed UI **or** Floating Device (huge type) |
| 2        | Value   | Floating Device                              |
| 3        | Feature | Floating UI Elements                         |
| 4        | Feature | Parallax Stack (the wow one)                 |
| 5        | Proof   | Quote Card                                   |
| 6        | Close   | Floating Device (smaller, branded outro)     |

Don't repeat the same archetype back-to-back unless the user explicitly wants a "feature parade" vibe — in which case do 3 Floating Devices in a row with distinct dominant colors per screen.
