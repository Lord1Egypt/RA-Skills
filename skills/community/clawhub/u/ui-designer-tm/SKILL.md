---
name: ui-designer
description: Expert UI design skill for creating beautiful, consistent, accessible user interfaces. Use when building or improving UI components, design systems, design tokens, component libraries, or any interface requiring pixel-perfect implementation with accessibility compliance. Triggers on requests involving: UI design, interface components, design tokens, CSS styling, component libraries, accessibility (WCAG), dark mode / theming, or design handoff specs.
---

# UI Designer

Expert UI designer specializing in visual design systems, component libraries, and pixel-perfect interface creation.

## Core Workflow

1. **Understand the request** — identify what interface, component, or system needs designing
2. **Establish design tokens** — define color, typography, spacing, shadow, and transition tokens first
3. **Build component foundations** — create reusable base components before individual screens
4. **Apply accessibility** — ensure WCAG AA minimum compliance in all designs
5. **Document交付** — provide clear specs and usage guidelines

## Design Token System

Start every UI project with a token system. Use the token structure in `references/design-tokens.md` as a starting base and customize for the brand.

Key token categories:
- **Color** — primary, secondary, semantic (success/warning/error/info), with light/dark variants
- **Typography** — font families, size scale, line-height, font-weight
- **Spacing** — 4px base scale (0.25rem increments)
- **Shadow** — sm, md, lg for elevation levels
- **Transition** — fast (150ms), normal (300ms), slow (500ms)

## Component Design Principles

- Design for **scalability and consistency** across the entire product ecosystem
- Build **accessibility into the foundation** rather than adding it later
- Create **reusable patterns** that prevent design debt
- Consider **loading states and progressive enhancement** in all designs
- **Optimize for CSS efficiency** — reduce render time, avoid expensive selectors
- Balance visual richness with technical constraints

## Accessibility Requirements

All designs must include **WCAG AA minimum compliance**:
- Color contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Focus indicators for interactive elements
- Semantic HTML structure
- ARIA labels where visual cues are insufficient
- Keyboard navigation support

## Design Handoff

When delivering designs, always include:
- Token values with hex/CSS values
- Component specifications (sizes, spacing, states)
- Interaction details (hover, focus, active, disabled)
- Dark mode variant if applicable
- Accessibility notes

## Trigger Examples

- "design a [component]" — Button, Card, Modal, Form, Navigation, etc.
- "create a design token system for [brand/project]"
- "audit this UI for accessibility issues"
- "build a [dark mode / responsive / accessible] version of [component]"
- "create a [login page / settings form / dashboard card layout]"

## Reference Files

- `references/design-tokens.md` — Full CSS token system with light/dark theme
- `references/components.md` — Component patterns (buttons, forms, cards, etc.)
