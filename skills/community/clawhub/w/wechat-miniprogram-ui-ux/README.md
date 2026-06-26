# WeChat Mini Program UI/UX Skill

[中文说明](./README.zh-CN.md)

A Codex skill for designing, implementing, refining, and reviewing WeChat Mini Program interfaces.

## Overview

This skill combines:

- WeChat Mini Program design principles and platform constraints
- A compact design-system workflow inspired by `ui-ux-pro-max`
- Anti-pattern filtering for mobile-first mini program UI
- A delivery checklist for production page states and interaction quality

## What It Is For

Use this skill when working on:

- WXML/WXSS/JS mini program pages
- Page redesigns and visual cleanup
- Detail pages, lists, forms, and management screens
- UI/UX reviews for mini program usability issues
- Design-system decisions for a mini program codebase

It is intended for WeChat Mini Program work specifically, not generic web UI work.

## What It Enforces

The skill pushes work toward:

- One clear page purpose
- One dominant action per major section
- Mobile-first hierarchy and tap comfort
- Explicit loading, empty, error, and permission states
- Safe-area aware bottom actions
- Visuals that feel native to mini programs instead of transplanted web landing pages

## Structure

```text
wechat-miniprogram-ui-ux/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── references/
    ├── design-system-pattern.md
    └── wechat-design-principles.md
```

## References

- WeChat Mini Program design guidelines
  `https://developers.weixin.qq.com/miniprogram/design/`
- `ui-ux-pro-max-skill`
  `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`

## How It Works

The skill guides the agent through this order:

1. Identify page type, user goal, and state complexity.
2. Read mini program design constraints and compact design-system guidance.
3. Define page intent, hierarchy, visual direction, and states.
4. Implement with mini program-native patterns in WXML/WXSS/JS.
5. Review against a mini program-specific checklist before delivery.

## Typical Output

For a page task, the skill steers the agent to think in this order:

1. Page intent
2. Primary action
3. Content hierarchy
4. State coverage
5. Visual system
6. Interaction details

## Example Use Cases

- Redesign a dish detail page so it feels native in WeChat and never blanks on load failure.
- Refactor a long form into clearer mobile sections with better validation and feedback.
- Review a management screen for permission clarity, destructive action safety, and state handling.
- Create a consistent visual direction for a mini program without overusing web-only effects.

## Notes

- This repo contains the skill itself, not a demo app.
- The skill is optimized for Codex-style local skills, but the guidance is reusable in any agent workflow.
