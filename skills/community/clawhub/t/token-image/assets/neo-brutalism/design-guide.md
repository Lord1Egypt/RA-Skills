# Neo-Brutalism Design System — Design Guide

This guide describes the Neo-Brutalism design system. Follow these rules when generating image components using Neo-Brutalism tokens.

## Overview

High-energy rebellion against smooth, polished design. Cream backgrounds, thick black borders, hard offset shadows, and pop-art color clashes. Every element is a sticker slapped onto a collage board — heavy, tactile, unapologetic. Movement is mechanical, not graceful. Structure is enforced, not hidden.

## Hierarchy

3 visual layers:
- **Primary** (textDisplay (`tokens.color.textDisplay`)): Headlines, hero statements. Black on cream. Maximum weight (`tokens.fontWeight.bold`).
- **Secondary** (text (`tokens.color.text`)): Body copy, descriptions. Same ink color but smaller scale (`tokens.fontSize.h4` and below).
- **Tertiary** (textSecondary (`tokens.color.textSecondary`)): Labels, metadata, captions. ALL CAPS with wide letter spacing (`tokens.letterSpacing.wide`). Still black — no grays.

accent (`tokens.color.accent`) is a pop-art interrupt. Use for buttons, badges, single highlight words, or a single call-to-action. Never wash entire sections with it.

## Typography

- **Space Grotesk** (display + body): The only typeface. Bold (`tokens.fontWeight.normal`, 700) for body, Black (`tokens.fontWeight.bold`, 900) for headlines.
- **Space Mono** (mono): Labels, metadata, code-like elements. ALL CAPS with `tokens.letterSpacing.wide`.
- Max 2 font families, 3 sizes, 2 weights per image.
- Letter spacing: `tokens.letterSpacing.tight` for large display text, `tokens.letterSpacing.wide` for ALL CAPS labels.
- Line height `tokens.lineHeight.tight` (1.0) for headlines, `tokens.lineHeight.normal` (1.5) for body.
- No Regular (400) or Light weights. Everything is Bold or heavier.

## Spacing Philosophy

Aggressive and deliberate. Dense clusters of content inside thick-bordered containers with generous padding (`tokens.spacing.lg` to `tokens.spacing.xl`) to keep text clear of borders. Between sections, use large gaps (`tokens.spacing.2xl`) to create sticker-like separation. Don't distribute evenly — stagger, offset, rotate. Let elements feel hand-placed, not grid-aligned.

## Composition

- Sticker-layering aesthetic: overlapping cards, slight rotations (`transform: rotate(-2deg)` / `rotate(2deg)`), absolute-positioned badges slapped onto corners.
- Staggered grids over perfectly aligned columns. Offset adjacent elements with small margin shifts.
- Asymmetric layouts preferred. Centered is acceptable only for a single dominant headline.
- Hard offset shadows on every bordered element: `box-shadow: 4px 4px 0px 0px var(--color-border)`.
- Divide space with thick borders, not whitespace alone.
- Optional: repeating dot/grid SVG patterns in background headers for texture.

## Visual Texture

- Thick black borders: `border: 4px solid var(--color-border)` on containers, buttons, badges, inputs.
- Hard offset shadows with zero blur: `box-shadow: 4px 4px 0px 0px #000000` (small), `8px 8px 0px 0px #000000` (medium).
- No gradients. No soft shadows. No blur. Solid color blocks only.
- Flat fills on `tokens.color.surface` containers against `tokens.color.bg` canvas.
- Rotated cards and badges create a scattered, hand-placed feel.
- Accent color used as bold blocks, never as subtle tinted backgrounds.

## Anti-patterns (NEVER)

- No border-radius. All corners sharp — `tokens.radius.sm`, `tokens.radius.md`, `tokens.radius.lg` are all 0. Pill shapes (`border-radius: 999px`) only for small badges, never containers.
- No gradients or soft shadows of any kind. Blur is always 0.
- No subtle grays. Use `tokens.color.text` (black) or palette colors.
- No smooth easing animations. Interactions are snappy — spring-based or instant.
- No rounded or soft shapes on primary containers.
- No transparency, glass effects, or blurred backdrops.
- No Regular/Light font weights. Only Bold (700) and Black (900).

## Style Factory Guidance

Build shared styles with these principles:
- Borders: `border: 4px solid var(--color-border)` on every container, button, badge, and interactive element.
- Offset shadows: `box-shadow: 4px 4px 0px 0px #000000` as the default depth indicator.
- Mechanical press interaction: On active/pressed state, apply `transform: translate(4px, 4px)` and remove the shadow to simulate a physical button press.
- Sticker rotation: Apply slight rotations (`-2deg` to `3deg`) to cards and badges for a hand-placed look.
- Contrast through weight and scale: Pair `tokens.fontSize.hero` with `tokens.fontWeight.bold` against `tokens.fontSize.small` ALL CAPS labels.
- Pop-art accents: accent color as solid blocks behind key text or as button fills — never decorative washes.
