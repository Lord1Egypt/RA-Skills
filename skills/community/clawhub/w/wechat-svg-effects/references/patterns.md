# Architecture Patterns & Animation Templates

## Pattern A: HTML + SVG Accents

Visual enhancement only, no interaction.

```xml
<section>
  <p style="...">Body text</p>
  <svg viewBox="0 0 800 400"><!-- Decorative SVG animation --></svg>
  <p style="...">More content</p>
</section>
```

- Body uses HTML, SVG embedded as animated illustrations
- CSS Grid responsive: `display:grid; grid-template-columns:repeat(auto-fit, minmax(300px,1fr));`

## Pattern B: Pure SVG State Machine

Entire article = 1 SVG. Click-through layers reveal content step by step.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 2400"
     style="display:block;width:100%;">
  <!-- Bottom: final reveal content -->
  <rect width="750" height="2400" fill="#0d1117"/>
  <text>Final content...</text>

  <!-- Cover layer N (removed first on click) -->
  <g>
    <animate .../> <!-- click to fade -->
    <animatetransform .../> <!-- move off-screen -->
    <rect .../> <!-- background mask -->
  </g>

  <!-- Cover layer 1 (topmost, initially visible) -->
  <g>...</g>
</svg>
```

**Layer order**: Later SVG elements render on top. Cover layers go bottom-to-top = click order top-to-bottom.

## Pattern C: SVG + HTML Hybrid

Interactive SVG header + long-form HTML body.

```xml
<section>
  <svg viewBox="0 0 750 1000" style="display:block;width:100%;">
    <!-- Interactive SVG header (multi-layer reveal) -->
  </svg>
  <section style="...">
    <p>Body paragraphs...</p>
  </section>
</section>
```

## Pattern D: CSS Grid + Multi-SVG Interactive Courseware

Multiple independent interactive cards using CSS Grid stacking.

```xml
<section style="display:grid; grid-template-rows:repeat(20,5%);">
  <!-- Bottom layer z-index:10 -->
  <svg style="grid-row-start:1; grid-column-start:1; z-index:10;">
    <foreignObject>
      <svg style="background-image:url('revealed-image'); background-size:cover;"/>
    </foreignObject>
  </svg>
  <!-- Cover layer z-index:20 -->
  <svg style="grid-row-start:1; grid-column-start:1; z-index:20;">...</svg>
  <!-- Click handler layer z-index:40+ -->
  <svg style="grid-row-start:1; grid-column-start:1; z-index:40;">
    <g>
      <rect pointer-events="visible" fill="transparent">
        <animate values="123456;123456" begin="touchstart"/>
      </rect>
      <animatetransform values="-1080 0;..." begin="click+0.31s"/>
    </g>
  </svg>
</section>
```

**3D perspective**: `perspective:50px` + `translateZ(-55px ~ +9px)` for depth layers.

### Pattern D: touchstart + keyTimes Reveal

Transparent touch detector:

```xml
<rect pointer-events="visible" fill="transparent"
      x="20%" y="30%" width="15%" height="8%">
  <animate values="123456;123456" dur="0.31s" begin="touchstart"/>
</rect>
```

`values="123456;123456"` → same before/after = no visual change, pure event registration.

keyTimes precision timing:

```xml
<animatetransform values="1080 0;1080 0;0 0;0 0"
                  dur="1000s" fill="freeze" begin="touchstart"
                  keyTimes="0;0.0003;0.00031;1"/>
```

1000s × 0.0003 = snap into position at 0.3s.

---

## SVG Animation Templates

### Basic Animation Elements

**Breathing / flicker / color cycle / pulsing radius:**

```xml
<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
<animate attributeName="fill" values="#ff5f56;#ffbd2e;#27c93f" dur="3s" repeatCount="indefinite"/>
<animate attributeName="r" values="5;8;5" dur="1.5s" repeatCount="indefinite"/>
```

**Rotate / translate / scale:**

```xml
<animatetransform type="rotate" values="0 375 500;360 375 500" dur="4s" repeatCount="indefinite"/>
<animatetransform type="translate" values="0 0;100 0;0 0" dur="2s" repeatCount="indefinite"/>
<animatetransform type="scale" values="1;1.2;1" dur="1s" repeatCount="indefinite"/>
```

**Path motion:**

```xml
<circle r="3" fill="#7ee787">
  <animateMotion path="M0,0 Q100,-50 200,0 T400,0" dur="3s" repeatCount="indefinite"/>
</circle>
```

### Common Animation Patterns

- **Flame flicker**: 3 diamonds (◆) at different dur (1.3s/1.5s/1.8s) for natural variation
- **Cursor blink**: `<rect>` + `opacity:1;0;1, dur=1s, indefinite`
- **Progress bar**: `<rect width="0">` + `animate width:0→592, fill=freeze`
- **Neural network pulse**: Multiple circles with staggered begin (+0.2s) for wave effect
- **Data flow**: rect + animateMotion along path + opacity fade-in/out
- **Image rounded mask**: `<path fill-rule="evenodd">` punches rounded-rect hole over image

---

## CSS Inline Style Techniques

### Text Decoration

**Highlighter underline:**
```
text-decoration:underline; text-decoration-thickness:5px;
text-decoration-color:rgba(101,208,169,0.5); text-underline-offset:-5px;
```

**Pill tag:**
```
padding:1px 4px; border:1px solid #dee0e3; border-radius:4px;
background-color:rgba(205,178,250,0.7);
```

### Card Styles

**Rounded shadow:** `border-radius:16px; box-shadow:0 4px 6px rgba(0,0,0,0.1);`

**Quote block:** `border-left:3px solid #cf4436; padding-left:12px; background:rgba(207,68,54,0.06);`

### Layout

**Grid responsive:** `display:grid; grid-template-columns:repeat(auto-fit, minmax(300px,1fr));`

**Grid stacking:** `grid-template-rows:repeat(20,5%);` + all children `grid-row-start:1; grid-column-start:1;`

### Background

**Gradient:** `background:linear-gradient(to right bottom, rgb(249,250,251), rgb(243,244,246));`

**Frosted glass:** `background:rgba(255,255,255,0.12); backdrop-filter:blur(20px);`

### 3D Effects

**Perspective container:** `transform-style:preserve-3d; perspective:50px;`

**Depth layers:** `transform:rotateY(2deg) translateZ(-25px);` (vary translateZ per layer)

**Horizontal scroll:** `width:198%;` (overflows screen, user swipes left/right)
