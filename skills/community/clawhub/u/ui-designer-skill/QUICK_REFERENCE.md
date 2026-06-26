# Quick Reference - Design System Selection Matrix

## Decision Logic

| Context | Design System | Reference |
|---------|---------------|-----------|
| **Platform: Windows/Microsoft** | fluent | `references/fluent-design.md` |
| **Platform: iOS/macOS** | apple-hig | `references/apple-hig.md` |
| **Platform: Android** | material | `references/material-you.md` |
| **Platform: Web (enterprise)** | ant, carbon, atlassian | See references/ |
| **Platform: E-commerce** | polaris | `references/shopify-polaris.md` |
| **Product: Admin panel/B2B** | ant, carbon | `references/ant-design.md` |
| **Product: Project management** | atlassian, carbon | `references/atlassian-design.md` |
| **Product: Dashboard** | fluent, ant, glass | `references/fluent-design.md` |
| **Product: Creative/Portfolio** | neo-brutalism, glass | `references/neo-brutalism.md` |
| **Product: Content/Blog** | minimal, swiss | `references/minimalism.md` |
| **Product: SaaS** | material, m3-pastel | `references/material-you.md` |
| **Style: Bold/Artistic** | neo-brutalism, claymorphism | `references/neo-brutalism.md` |
| **Style: Minimal/Clean** | minimal, swiss | `references/minimalism.md` |
| **Style: Modern/Trendy** | material, glass, neumorphism | `references/glassmorphism.md` |
| **Style: Corporate** | fluent, carbon, atlassian | `references/carbon-design.md` |
| **Style: Luxury/Tactile** | skeuomorphism | `references/skeuomorphism.md` |

## Available Systems

**Enterprise:** fluent, ant, carbon, atlassian
**Platform:** apple-hig, polaris, material
**Modern:** glass, neumorphism, neo-brutalism, claymorphism
**Classic:** minimal, swiss, skeuomorphism
**Hybrid:** m3-pastel, neo-m3

## Apply Command

```bash
python3 scripts/apply_ui_rules.py --style [system] --palette [pastel|dark|vibrant|mono]
```

## Quick Specs

| System | Color | Radius | Grid | Shadow |
|--------|-------|--------|------|--------|
| fluent | #0078D4 | 2-12px | Flex | Layered |
| ant | #1677FF | 2-8px | 12-col | Subtle |
| carbon | #0F62FE | 0-8px | 16-col | Sharp |
| atlassian | #0052CC | 3-8px | 8-col | Raised |
| apple-hig | #007AFF | 8-16px | Flex | Soft |
| polaris | #008060 | 4-12px | Flex | Card |
| material | Dynamic | 12-28px | 12-col | Elevation |
| glass | Vibrant | 12-20px | Flex | Blur |
| neumorphism | Mono | 12-24px | Flex | Dual |
| neo-brutalism | Bold | 8-16px | Flex | Hard |
| claymorphism | Pastel | 24-40px | Flex | Inner |
| minimal | Neutral | 0-8px | Flex | None |
| swiss | 1-2 accent | 0-4px | 12-col | None |
| skeuomorphism | Material | 8-12px | Flex | Rich |

Reference files: `references/[system-name].md`
