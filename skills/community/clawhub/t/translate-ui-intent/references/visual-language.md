# Visual Language Translation

Use this reference to translate subjective language into testable design
hypotheses. The mappings are possibilities, not fixed definitions. Product
context and repository evidence decide which interpretation is valid.

## Common Expressions

| User expression | Possible design dimensions | Observable options | Typical implementation levers | Useful contrast question |
|---|---|---|---|---|
| "简洁 / clean" | hierarchy, disclosure, visual noise | fewer simultaneous actions; clearer groups; restrained decoration | grouping, progressive disclosure, action priority, border reduction | Should we remove choices, or keep the same capability with clearer grouping? |
| "高级感 / premium" | typography, rhythm, restraint, content quality | precise spacing; limited accents; deliberate imagery; calm motion | type scale, spacing tokens, surface treatment, motion timing | Should it feel editorial and spacious, or precise and tool-like? |
| "大气 / expansive" | scale, width, whitespace, focal point | wider composition; fewer competing regions; stronger primary content | max width, grid proportions, section rhythm, media scale | Is the goal brand impact or easier content comprehension? |
| "不要像后台 / not like an admin panel" | information architecture, density, navigation, control exposure | task-led flow; fewer persistent controls; content-first hierarchy | staged disclosure, page shell, action placement, form structure | Which operational controls must remain immediately available? |
| "紧凑 / compact" | density, repetition, scanning | shorter rows; tighter groups; more visible data | spacing scale, row height, typography, inline actions | Is speed of repeated work more important than first-time readability? |
| "有呼吸感 / airy" | spacing, line length, grouping | larger group separation; constrained reading width | spacing tokens, max width, line height, grid gap | Where should space improve comprehension rather than merely enlarge the page? |
| "现代 / modern" | current product conventions, typography, interaction | simpler surfaces; current controls; responsive behavior | tokens, component variants, icons, motion, layout | Which current product or reference best represents "modern" here? |
| "活泼 / lively" | color, motion, shape, illustration | stronger accents; responsive feedback; playful media | semantic color, motion, iconography, imagery | Is this for delight during discovery or energy during repeated work? |
| "重点突出 / emphasize the key point" | hierarchy, contrast, position | one dominant action or message; reduced secondary emphasis | size, weight, semantic color, placement, whitespace | What single action or fact should win the first three seconds? |
| "不要太花 / less decorative" | color count, effects, competing emphasis | fewer accents; flatter surfaces; consistent emphasis | palette, shadows, gradients, borders, animation | Which decoration is distracting from the task? |

## Design Dimensions

Translate feedback through these dimensions:

- **Information architecture:** grouping, sequence, disclosure, navigation
- **Hierarchy:** prominence of content and actions
- **Density:** amount of information and control per viewport
- **Rhythm:** spacing consistency and repeated alignment
- **Typography:** role, scale, weight, line length, readability
- **Surface:** background, border, elevation, containment
- **Color:** semantic roles, emphasis, status, contrast
- **Interaction:** control choice, feedback, focus, selection, recovery
- **Motion:** continuity, causality, duration, reduced-motion behavior
- **Responsive behavior:** reflow, collapse, priority, overflow

Use implementation terminology only after the intended visible behavior is
clear. For example:

> You chose a compact operational density. In frontend terms, that usually
> means the existing small control variants, the compact spacing tokens, and
> shorter table rows rather than a new visual theme.

Never treat a named style trend as sufficient instruction. Describe what the
user will see, understand, and be able to do.
