# Modern Dark Design System — Design Guide

## Overview
Cinematic dark mode with near-black backgrounds, animated gradient blobs for ambient lighting, and frosted glass surfaces. Feels like a premium native app — technical but inviting, using soft glow sources to guide the eye.

## Hierarchy
3 visual layers via opacity and elevation:
- **Primary** (`textDisplay`, full opacity) — headlines, CTAs, key data
- **Secondary** (`text`, high contrast) — body copy, descriptions
- **Tertiary** (`textSecondary`, 50%) — captions, metadata, timestamps

## Typography
- **Inter** (display/body): Clean geometric sans-serif used throughout. Display headings use gradient text (white fading to 70% white) via `background-clip: text`.
- **JetBrains Mono** (mono): Labels, metadata, technical content. Uppercase with `letterSpacing.wide` for small labels.
- Letter spacing tightens at display sizes (`letterSpacing.tight`), normal for body.

## Spacing Philosophy
4pt base unit. Generous margins (`lg`–`xl`) around content areas. Compact internal padding (`sm`–`md`). Elements breathe at the macro level but stay tight within cards and containers.

## Composition
- Never use a single solid background — always layer a subtle gradient (near-black to deep dark) as the base.
- Animated gradient blobs: large, slow-moving, heavily blurred circles at low opacity that simulate ambient light pools.
- Cards and containers float on elevated surfaces with frosted glass (`backdrop-filter: blur`).
- Stack multiple translucent layers at different opacities for parallax-like depth.
- Accent glow: faint, non-distracting glow behind primary actions and active elements.

## Visual Texture
- **Background**: Gradient from `#0a0a0f` (top) to `#020203` (bottom) — never pure black.
- **Ambient blobs**: 2–3 large circles with high blur radius (30–50px), low opacity (0.1), slowly oscillating position.
- **Surfaces**: Translucent white at `opacity.subtle`–`opacity.muted` with `border` tokens for hairline edges.
- **Glow effects**: Soft `box-shadow` or radial gradient using accent color at 20% opacity around primary elements.

## Anti-patterns (NEVER)
- No pure black (`#000000`) backgrounds — causes visual artifacts. Use `bg` token (`#050506`) or darker.
- No solid opaque borders — always translucent via `border` token.
- No flat single-layer backgrounds — always create depth with gradient + blobs + surface layers.
- No bouncy animations — use precise easing curves. Sophistication over playfulness.
- No high-saturation accent splashes — accent glow should be subtle and non-distracting.

## Style Factory Guidance
Build in 4 layers: (1) gradient background base, (2) animated ambient light blobs, (3) frosted glass surface with `backdrop-filter: blur` using `surface` and `border` tokens, (4) content with typography hierarchy. Use `accent` sparingly — for glows, active states, and primary actions only. Every card gets a uniform `radius` (16px) and a subtle top-edge highlight for depth.
