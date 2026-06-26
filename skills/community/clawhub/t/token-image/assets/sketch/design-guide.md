# Sketch Design System — Design Guide

This guide describes the Sketch/Hand-Drawn design system. Follow these rules when generating image components using Sketch tokens.

## Overview

Hand-drawn, notebook-on-desk aesthetic. Organic imperfection and human touch. Every element looks like it was sketched with markers and pencils on warm textured paper. Rejects geometric precision in favor of playful, wobbly irregularity. The feel is a portable sketchbook, sticky notes on a wall, or a well-loved notebook.

## Hierarchy

3 visual layers:
- **Primary** (textDisplay (tokens.color.textDisplay)): Headlines, key statements. Bold marker weight, slight rotation for energy.
- **Secondary** (text (tokens.color.text)): Body copy, descriptions. Pencil-weight, legible but human.
- **Tertiary** (textSecondary (tokens.color.textSecondary)): Metadata, timestamps, labels. Lighter pencil marks, recedes into the page.

accent (tokens.color.accent) is the red correction marker — use for single-word highlights, underlines, or a single call-to-action. Never as a background wash.

## Typography

- **Kalam** (display): tokens.fontSize.h2 and above. Bold weight. Felt-tip marker headlines with generous line-height for scribbled descenders.
- **Patrick Hand** (body): General content at tokens.fontSize.body to tokens.fontSize.h3. Highly legible but distinctly human.
- **Caveat** (mono): Captions, annotations, margin notes. Small or body size. Handwritten script feel.
- Max 2 font families, 3 sizes, 2 weights per image.
- Letter spacing: tight for large display text, normal for body, wide for labels.
- Line height tight (1.0) for headlines, normal (1.5) for body.
- Vary rotation slightly per text block to suggest hand-placed notes.

## Spacing Philosophy

Generous and organic. Let the paper breathe. Large gaps between sections (xl/2xl). Tight padding (sm/md) inside cards and containers. Avoid perfect symmetry — offset adjacent elements by a few pixels. Create visual rhythm through deliberate unevenness rather than a rigid grid.

## Composition

- No straight lines. Every container uses varied border-radius per corner to create wobbly edges.
- Slight rotation (transform: rotate -1deg to 1deg) on cards and images to break the rigid grid.
- Asymmetric layouts preferred. Overlap elements slightly for a collaged feel.
- Decorative SVG flourishes: hand-drawn arrows, stars, underlines, circles.
- Tape and tack decorations on cards: semi-transparent strips at corners, small red circle pins.
- Allow decorative elements to bleed slightly off edges for spontaneity.
- Layer with zIndex: tape over cards, cards over background scribbles.

## Visual Texture

- Borders: 2–3px solid var(--color-border). Bold and visible like pencil strokes. Use dashed borders for "cut-out" sections or empty states.
- Wobbly radius: Each corner gets a unique value (e.g., borderTopLeftRadius: 15, borderTopRightRadius: 25, borderBottomLeftRadius: 20, borderBottomRightRadius: 10) to reject geometric perfection.
- Hard offset shadows: No blur. A solid-colored rectangle offset by (4px, 4px) behind elements to create a cut-paper, layered collage aesthetic.
- Paper texture: Use a subtle noise overlay or dot-grid pattern on the background to simulate physical paper grain.
- Flat color fills on surfaces. No gradients.
- Optional: washi tape strips, push-pin dots, sticky-note yellow highlights (#fff9c4) for primary CTAs.

## Anti-patterns (NEVER)

- No geometric perfection. Every straight line should have slight irregularity.
- No blur shadows, glow effects, or soft gradients.
- No perfectly aligned grids. Break alignment intentionally.
- No corporate polish or minimalist sterility.
- No thin hairline borders — all strokes are bold and visible.
- No glass effects, frosted overlays, or transparency layers (except tape decorations).
- No machine-perfect circular shapes. Use slightly irregular curves.

## Style Factory Guidance

Build shared styles with these principles:
- Borders: `border: 2px solid var(--color-border)` on containers. Vary each corner's radius independently.
- Hard shadows: Place a second div behind the element, offset (4px, 4px), filled with var(--color-border) at low opacity.
- Rotation: Apply `transform: rotate(-1deg)` or `rotate(1deg)` to cards and images. Vary per element.
- Red marker accents: Single underlines, circle highlights, or one highlighted word — never full backgrounds.
- Hand-drawn SVGs: Arrows, stars, squiggly dividers, X marks for close buttons. Stroke-based, no fills.
- Tape effect: A semi-transparent strip (rgba(200, 200, 200, 0.5)) positioned at card edges, slightly rotated.
- Tack effect: A small solid circle in accent color positioned at top center of cards.
- Contrast through scale: Pair hero-size headlines with small-size margin notes and annotations.
- Jiggle animation for error states: Rapid rotation between -2deg and 2deg.
