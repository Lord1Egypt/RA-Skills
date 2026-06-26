---
name: wechat-svg-effects
description: |
  Create interactive SVG/CSS effects for WeChat Official Account (微信公众号) articles. WeChat bans JavaScript, so all interactivity must use pure SVG animations + inline CSS. Supports click-to-reveal layers, bounce feedback, multi-stage state machines, 3D card effects, animated decorations, and CSS Grid layouts. Use when: (1) creating WeChat article interactive effects, (2) building click-to-reveal or tap-to-unveil experiences, (3) adding SVG animations to WeChat posts, (4) designing interactive covers/headers for 公众号, (5) user mentions "微信公众号", "SVG交互", "点击揭示", "公众号特效", "SVG动画", "wechat svg".
---

# WeChat Official Account SVG/CSS Interactive Effects

> All interactivity must be pure SVG + inline CSS. **WeChat bans JavaScript entirely.**

## Core Constraints

- SVG events: `begin="mousedown"`, `begin="click"`, `begin="touchstart"`
- SVG animation: `<animate>`, `<animatetransform>`, `<animateMotion>`
- CSS: inline `style=""` only (no `<style>` blocks, no external sheets)
- `<foreignObject>` to embed HTML inside SVG
- Text in SVG: `<text>` + `<tspan leaf="">` (`leaf` attr is WeChat-specific)
- Append `<p style="display:none;"><mp-style-type data-value="10000"/></p>` at end to enable WeChat special rendering
- viewBox width: 750 (mobile-optimized)

## Four Architecture Patterns

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| A. HTML + SVG accents | Visual enhancement, animated decorations | ★☆☆ |
| B. Pure SVG state machine | Click games, step-by-step reveals | ★★☆ |
| C. SVG + HTML hybrid | Interactive header + long-form body | ★★☆ |
| D. CSS Grid + multi-SVG | Interactive courseware, multi-card reveals | ★★★ |

For detailed architecture patterns, examples, and animation templates, read `references/patterns.md`.

## Quick Start: Click-to-Reveal Template

Single-layer cover that disappears on click:

```xml
<g>
  <!-- 1. Fade out on click -->
  <animate attributeName="opacity" values="1;0"
           dur="0.01s" fill="freeze"
           begin="mousedown" restart="never"/>
  <!-- 2. Move off-screen after delay -->
  <animatetransform attributeName="transform" type="translate"
                    values="0 0;2000 0" dur="0.01s" fill="freeze"
                    begin="click+0.02s" restart="never"/>
  <!-- Background + content -->
  <rect width="750" height="2400" fill="#0d1117"/>
  <text x="375" y="500" fill="#c9d1d9" font-size="24" text-anchor="middle">
    <tspan leaf="">👆 Click to reveal</tspan>
  </text>
</g>
```

| Param | Fast (game) | Slow (ceremony) |
|-------|-------------|-----------------|
| click delay | click+0.02s | click+0.3s |

## Multi-Layer Reveal

Stack layers bottom-to-top in SVG (later elements render on top). Each layer has its own `mousedown`/`click` triggers with `restart="never"`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 600"
     style="display:block;width:100%;">
  <!-- Bottom: final reveal -->
  <rect width="750" height="600" fill="#0d1117"/>
  <text x="375" y="300" fill="#7ee787" font-size="36" text-anchor="middle">
    <tspan leaf="">🎉 Unlocked!</tspan>
  </text>
  <!-- Layer 2 -->
  <g>
    <animate attributeName="opacity" values="1;0"
             dur="0.01s" fill="freeze" begin="mousedown" restart="never"/>
    <animatetransform attributeName="transform" type="translate"
                      values="0 0;2000 0" dur="0.01s" fill="freeze"
                      begin="click+0.05s" restart="never"/>
    <rect width="750" height="600" fill="#161b22"/>
    <text x="375" y="300" fill="#FF8B2C" font-size="28" text-anchor="middle">
      <tspan leaf="">Level 2 → Tap again</tspan>
    </text>
  </g>
  <!-- Layer 1 (top, visible first) -->
  <g>
    <animate attributeName="opacity" values="1;0"
             dur="0.01s" fill="freeze" begin="mousedown" restart="never"/>
    <animatetransform attributeName="transform" type="translate"
                      values="0 0;2000 0" dur="0.01s" fill="freeze"
                      begin="click+0.05s" restart="never"/>
    <rect width="750" height="600" fill="#21262d"/>
    <text x="375" y="280" fill="#c9d1d9" font-size="28" text-anchor="middle">
      <tspan leaf="">👆 Tap to start</tspan>
    </text>
  </g>
</svg>
<p style="display:none;"><mp-style-type data-value="10000"/></p>
```

## Bounce Feedback

Add tactile bounce on every tap (`restart="always"`):

```xml
<g>
  <animatetransform attributeName="transform" type="translate"
                    values="0 0;0 22;0 0" dur="0.5s"
                    begin="mousedown" restart="always"/>
  <rect width="750" height="1000" fill="#161b22" opacity="0.01"/>
</g>
```

## Terminal UI Color Palette (GitHub Dark)

| Role | Hex |
|------|-----|
| Background | #0d1117 |
| Panel | #161b22 |
| Border | #30363d |
| Red | #ff5f56 |
| Yellow | #ffbd2e |
| Green | #27c93f |
| Body text | #c9d1d9 |
| Comment | #6e7681 |
| Highlight | #FF8B2C |
| Success | #7ee787 |

## Workflow

1. Choose architecture pattern (A–D) based on complexity
2. Read `references/patterns.md` for the chosen pattern's detailed template
3. Build SVG with proper layer ordering (bottom = final reveal, top = first visible)
4. Test all `restart="never"` vs `restart="always"` logic
5. Append `<mp-style-type data-value="10000"/>` at the end
6. Validate: no `<script>`, no `<style>` blocks, no external CSS, all styles inline
