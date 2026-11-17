# Animation Standards (Mode 3)

> Extracted from `mode-2-prototype.md` to keep that file under 500 lines.
> Load this file when the user requests Mode 3 (Animation/Video) deliverables.

---

## Animation Reason Checklist (Mode 3 mandatory before generating)

Before generating any animation in Mode 3, answer this question for each animated element:

**"Why does this element need to move?"**

### Valid reasons (motion must serve one of these)

| Reason category | Description | Example |
|----------------|-------------|---------|
| Spatial consistency | Element enters/exits from a fixed direction to build mental model | Toast always slides from top-right; drawer always from right edge |
| State indication | Motion communicates a state change to the user | Button morphs to spinner when loading; checkmark draws in after success |
| Relationship explanation | Motion shows how elements relate or transform into each other | Card expands into detail view; item moves from list to cart |
| Prevent disorientation | Motion smooths abrupt changes so user doesn't lose their place | Element fading out instead of vanishing; content sliding instead of jumping |
| Feedback | Motion confirms a user action happened | Button scale(0.97) on press; ripple on touch |

### Invalid reasons (delete the motion if this is the only justification)

| Invalid reason | Why it's wrong | What to do instead |
|---------------|----------------|-------------------|
| "Looks cool" | Novelty wears off in 5 uses; distracts from content | Static design with better color/type/layout |
| "Makes the page alive" | Ambient motion competes with content for attention | Use whitespace and typography to create rhythm |
| "Everyone else does it" | Copying without context means the motion solves YOUR users' problems | Check if the motion serves a reason from the valid list above |
| High frequency + functional motion | Animation > 300ms on a 100x/day operation causes fatigue | Use instant feedback (color change) or near-instant (≤100ms) |

### Execution rule

For each Mode 3 request, the agent must:
1. Identify every element that will have motion
2. Map each motion to a valid reason from the table above
3. If no valid reason exists: **remove the motion** (don't generate it)
4. Record the reasoning in the HTML reasoning block:

```html
<!--
ANIMATION REASONING
├── Header fade-in: relationship explanation (page entrance)
├── Button press scale: feedback (user action confirmation)
├── Card stagger: relationship explanation (show group cohesion)
└── (removed) Logo ambient spin: no valid reason — replaced with static
-->
```

---

## Pre-flight Animation Quality Rules (additive to existing checks)

After the 10-item Pre-flight Checklist (CP4) in `mode-2-prototype.md`, run these animation-specific checks for Mode 3 deliverables:

| # | Check | Rule | Fail action |
|---|-------|------|-------------|
| 11 | No `transition: all` | Must specify exact properties: `transition: transform 200ms ease-out, opacity 200ms ease-out` | Replace `all` with explicit property list |
| 12 | No `ease-in` for UI enter animations | Entering elements use `ease-out` (fast start, slow settle); moving elements use `ease-in-out`; color/opacity use `ease` | Change easing curve |
| 13 | Duration bounds respected | Button feedback ≤160ms; tooltip/popover ≤250ms; modal/drawer ≤500ms; hero entrance ≤800ms | Clamp duration to bounds |
| 14 | Entrance not from `scale(0)` | Elements don't appear from nothing — use `scale(0.95) + opacity: 0` as starting state | Replace `scale(0)` with `scale(0.95)` |
| 15 | GPU-layer properties only | Only animate `transform` and `opacity` — never `width`, `height`, `margin`, `top`, `left` | Refactor to transform/opacity |
| 16 | Touch device safety | Hover-triggered animation must be wrapped in `@media (hover: hover) and (pointer: fine)` | Add hover media query guard |
| 17 | Reduced-motion granularity | `prefers-reduced-motion` retains opacity/color transitions but removes transform/position animation | Split animation into two layers: color (always) and transform (reduced-motion: none) |

---

## Physical Correctness Defaults

Entrance animations should follow physical realism:

- **Never start from `scale(0)`** — elements don't appear from nothing in reality. Use `scale(0.95) + opacity: 0` as the starting state.
- **Origin-aware reveals** — popovers/dropdowns should scale from their trigger point (`transform-origin: top center` for a button-triggered popover), not from the element's own center.
- **Asymmetric timing** — pressing a button can be slow (2s linear hold), releasing fast (200ms ease-out). Don't use the same duration for both directions.

These defaults are baked into `deck-studio/assets/animations/animations.css` (e.g., `kf-zoom` starts at `scale(.96)`, not `scale(.6)`).

---

## Reduced-Motion Granularity

The `prefers-reduced-motion` media query should NOT kill all animation. Instead:

1. **Keep**: opacity transitions, color changes, background shifts — these convey information
2. **Remove**: transform animations, position movements, scale effects — these trigger vestibular disorders

Example implementation:

```css
@media (prefers-reduced-motion: reduce) {
  /* Kill transform-based animation */
  .animated-element { animation-name: none !important; }
  .animated-element:hover { transform: none !important; }
  /* Preserve information-bearing transitions */
  .animated-element {
    transition: opacity var(--dur) ease, background-color var(--dur) ease !important;
  }
}
```

This is the default behavior in `deck-studio/assets/animations/animations.css`.
