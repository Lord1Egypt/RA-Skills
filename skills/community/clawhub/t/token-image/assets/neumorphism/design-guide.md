# Neumorphism Design System — Design Guide

## Overview
Soft extruded interfaces molded from a single material. Dual light/dark shadows create a tactile, ceramic-like surface where every element is either "pillowed" (convex) or "wells" (concave/inset). Calm, monochromatic depth over color-based hierarchy.

## Hierarchy
3 layers via shadow depth, not color: Primary (textDisplay, extruded shadow, largest), Secondary (text, medium shadow), Tertiary (textSecondary, inset or minimal shadow). Accent for active toggles and primary CTAs only.

## Typography
- Plus Jakarta Sans (display): tokens.fontSize.h2 and above, Bold (700). Tight letter spacing for headings.
- Plus Jakarta Sans (body): Clean and geometric. Medium weight for body text.
- JetBrains Mono (mono): Data, labels, technical content.
- Never mix display and body families — Plus Jakarta Sans handles both roles through weight contrast.

## Spacing Philosophy
8pt grid system. Elements should feel physically grounded with consistent breathing room. Generous padding on cards and containers to maintain the "continuous material" illusion.

## Composition
- Everything shares the same background material (`${tokens.color.bg}`) — no contrasting surfaces.
- Dual shadows define all hierarchy: light source top-left, dark shadow bottom-right.
- Buttons are always extruded (convex) at rest, inset (concave) when pressed.
- Cards use nested depth — an extruded card containing inset icon wells.
- Inputs are always inset (concave) to simulate a physical slot.
- No sharp edges — minimum `tokens.radius.sm` on everything.

## Visual Texture
Extruded (convex — resting state):
```tsx
boxShadow: '6px 6px 12px rgba(163, 177, 198, 0.7), -6px -6px 12px rgba(255, 255, 255, 0.6)'
```
Inset (concave — pressed/active/input state):
```tsx
boxShadow: 'inset 4px 4px 8px rgba(163, 177, 198, 0.7), inset -4px -4px 8px rgba(255, 255, 255, 0.6)'
```
Scale-press interaction (not shadow-change):
```tsx
transform: 'scale(0.97)'
transition: 'transform 250ms cubic-bezier(0.4, 0, 0.2, 1)'
```

## Anti-patterns (NEVER)
- No black shadows — shadows must be blue-grey, never `rgba(0,0,0,x)`.
- No pure white or pure black backgrounds — violates the continuous material principle.
- No sharp corners — `borderRadius < 12` is forbidden.
- No flat borders as depth substitute — borders only for focus states (1.5px accent).
- No high-contrast color palettes — hierarchy comes from shadow depth, not color contrast.
- No flat design — every element must have extruded or inset shadow definition.

## Style Factory Guidance
Build with dual shadows (light top-left, dark bottom-right) on a uniform background. Plus Jakarta Sans Bold for all headings. Every interactive element uses scale-press on interaction, not shadow transitions. The entire surface is one continuous material — never break the illusion with contrasting card backgrounds or colored surfaces.
