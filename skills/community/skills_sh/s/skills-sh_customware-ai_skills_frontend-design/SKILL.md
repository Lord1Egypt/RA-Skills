---
name: frontend-design
description: >
  Strict frontend design guardrails for building modern, minimal-visual-noise, airy,
  non-generic app UIs. Use whenever creating or changing frontend UI, React components,
  shadcn/ui themes, Tailwind styles, app layouts, or first-version product screens.
  This skill complements vertical/domain skills like CPQ, CRM, and similar app builders:
  follow the selected domain skill's workflow and layout requirements, then enforce
  this skill's shared visual rules for brand-aware theming, generous spacing,
  typography, contrast, roundedness, shadows, surface hierarchy, cardless defaults,
  no-sidebar defaults, and anti-pattern avoidance.
---

# Frontend Design

This is a visual design guardrail skill, not a domain workflow skill. Domain skills own required product structure, terminology, workflows, and output views. This skill owns visual quality and must be applied inside that structure.

## Mandatory References

Before visual planning or implementation, read both files. Skipping either file is a skill violation.

- `.agents/skills/frontend-design/references/visual-style-references.md`
- `.agents/skills/frontend-design/references/shadcn-setup-and-theming.md`

## Required Workflow

1. Read the active task, domain context, and selected domain skills.
2. Read `.tasks/domain.md` when it exists. Extract brand colors, company name, domain tone, terminology, workflows, entities, statuses, roles, and constraints.
3. Read both frontend-design references.
4. Produce the design pass before coding:
   - **Vision**: domain-specific product and visual direction. Reject generic SaaS purple, card-heavy dashboards, and generic admin shells.
   - **First-version features**: working screens, controls, routes, dialogs, and localStorage-backed state.
   - **Design tokens**: primary, secondary/accent, background, canvas, focal contrast treatment, text, border, radius, contact shadow, status colors, typography, generous spacing, and cardless plan.
   - **Design direction**: enforce brand color usage, actual logo usage, airy spacing, airy inner density, rounded controls, strong input contrast, soft/tight shadows, minimal visual noise, cardless defaults, and authored composition. Where the selected domain skill does not specify structure, use stronger visual ideas like asymmetry, deliberate negative space, vivid accent hierarchy, motion, and atmospheric background detail.
5. Pass the design compliance gate.
6. Configure CSS variables, Tailwind/shadcn theme tokens, and the relevant shadcn component styles before building screen details.
7. Build the UI with those tokens. Use Tailwind where it is useful, and write custom CSS classes when Tailwind is limiting; custom CSS must reuse the global CSS variables, radius, color, and shadow tokens.
8. Run the pre-completion audit and revise before finishing.

## Non-Negotiables

- **Brand first**: If `.tasks/domain.md` provides brand colors, use them. Map the main brand/accent color to primary actions, active navigation, selected state, focus, and links. Derive neutral surfaces, borders, muted text, and statuses from compatible tints. Do not default to generic purple/blue.
- **Readable foregrounds always**: Use brand colors for primary, secondary, accent, active, and focus roles, but choose foreground/text colors separately for legibility. Brand palettes usually do not provide all text colors. Every text, icon, label, placeholder, badge, button, disabled state, and data value must have high contrast against its actual background. When a brand color is the background, derive a readable foreground color for it instead of reusing another brand color. Prefer WCAG AA as the minimum: `4.5:1` for normal text and `3:1` for large text/icons.
- **Domain-skill compatibility**: If the app fits a selected business/domain skill like CPQ, CRM, trades, or similar, follow that skill's required workflow, terminology, and layout structure. For anything the domain skill does not specify, use this skill's visual rules and composition guidance rather than falling back to a generic admin shell.
- **Authored composition**: Every app should feel intentionally designed. Commit to a cohesive aesthetic, use CSS variables consistently, prefer dominant colors with sharp accents over timid evenly distributed palettes, use motion for high-impact moments, favor asymmetry or unexpected composition where it does not conflict with workflow clarity, and build atmosphere through brand-compatible backgrounds and visual details.
- **Use the real logo**: First look in `public/brand/logos/`. If that folder contains a usable logo file, use the correct actual logo from that folder in the header or primary app chrome. Only create or invent a logo if `public/brand/logos/` does not exist or has no usable logo files.
- **Cardless by default**: Aim for zero cards. If the UI works without a card, the card is not allowed. A bordered rounded surface occupying a major region of the page is a card even if `Card` is not imported. Cards are only allowed for dialog/popover/sheet containment, concise notice, or truly repeated items when rows, dividers, or tonal separation fail.
- **No top-level cards**: Never compose the main page from large sibling cards, a stack/grid of rounded panels, or a large framed hero/detail container. Top-level structure must be open sections, tonal bands, rows, dividers, workspace areas, or one open focal working zone.
- **No sidebars by default**: Use a sidebar only when the user explicitly asks for one or a selected domain skill explicitly requires one. Do not add a sidebar because the app is operational, business, admin-like, multi-step, or has multiple sections.
- **Airy spacing**: Use generous gaps, gutters, row rhythm, and section spacing. Slightly too much spacing is acceptable; cramped, dense, or compressed UI is failure.
- **Airy inner density**: Airiness must continue inside rows, tables, lists, cards, and compound components. Do not pack too many columns into one row when a cleaner stacked or richer row layout would breathe better. Inner content should use generous gaps between sub-elements, metadata, actions, and labels.
- **Table rhythm**: When using a surfaced table, give the table `shadow-xs` and use generous header padding, row padding, and taller row rhythm. Tables should not feel compressed, flat, or spreadsheet-tight.
- **Rounded by default**: If the selected domain skill does not explicitly require a sharper or specific radius language, prefer a clearly rounded modern system. Avoid timid 4px/6px/8px admin radii by default. Controls, chips, tabs, and key surfaces should usually feel distinctly rounded or pill-like.
- **Typography with character**: Choose fonts that are beautiful, distinctive, and interesting. Avoid generic defaults like Arial and Inter. Prefer a characterful display face paired with a refined body face when the product can support it. The typography should elevate the UI, not read like a default starter app.
- **One dominant working surface**: The first screen should focus on one clear operational object or working section. Do not try to show the whole product at once.
- **No major-region framed surfaces**: Do not turn the main working area, hero, inspector, or detail lane into a big bordered rounded panel. Prefer open layout, split rows, tonal bands, dividers, or a drawer/sheet for secondary detail.
- **Token-first shadcn and CSS**: Configure `app.css`/global CSS variables, Tailwind theme values, and relevant shadcn component styles before component work. Do not accept default shadcn colors or component styling as the design. shadcn components are base primitives only; always customize their classes/styles to fit the app's tokens, spacing, contrast, radius, shadow, and interaction rules. Tailwind is not mandatory for every visual decision; write custom CSS when it creates a more distinct, minimal, polished UI, while reusing the same CSS variables and theme tokens.
- **Strong soft contrast**: If a surface exists, it must separate from the canvas through tone first, border second, shadow last. Same-white or near-white surfaces with faint borders fail.
- **Interactive surface contrast**: Every editable control must be obvious. Regular text inputs, selects, textareas, comboboxes, date fields, search fields, command-bar controls, and shadcn form controls must all use a near-white or very light tinted background in light mode and a near-black background in dark mode. Do not only fix selects while leaving normal inputs page-colored. Controls must not use `bg-transparent`, `bg-background`, `bg-muted`, or the same fill as the page/panel. `--input` must be visibly lighter than `--background` in light mode and visibly darker than the canvas in dark mode. Search/filter controls must be among the clearest input surfaces on the screen.
- **Panel/card contrast when unavoidable**: If a card-like surface is truly unavoidable, including summary panels, live summary cards, inspectors, notices, and repeated item containers, it must use a clearly contrasting near-white or very light tinted background in light mode and near-black in dark mode. Same-fill panels on a tinted page fail even when borders are visible.
- **Header treatment when present**: If the app has a header/topbar, prefer a translucent near-white or very light tinted surface in light mode and near-black in dark mode with `backdrop-blur-md` and roughly `70-80%` opacity. The header must still have enough contrast from the page and must use the real logo when available.
- **Sidebar tone and space when required**: If a selected domain skill requires a sidebar, use a much darker shade derived from the primary color for the sidebar background or key sidebar surfaces. The sidebar must be wide enough for its labels, badges, and active states; do not clip text or squeeze actions off the edge. Use generous item padding, clear vertical rhythm, and deliberate truncation only for secondary descriptions.
- **Contact depth only**: Avoid `shadow-sm`, `shadow-md`, and `shadow-lg` as defaults for normal layout surfaces. Prefer `shadow-2xs` for buttons and other small interactive elements, `shadow-xs` for cards/tables/similar contained surfaces, `shadow-xl` for popovers and banners, and `shadow-2xl` for dialogs. Use soft, tight, contact-edge depth only when needed. Soft means no hard spread edge, not barely visible; the shadow can still be a clear gray if needed for contrast. Depth should read as edge contact, not lift.
- **Domain specificity**: The UI should not look unchanged if the domain name and labels are swapped.

## Design Compliance Gate

Do not code until all answers are acceptable.

- Did I read `.tasks/domain.md` and summarize brand colors when present?
- Did I check `public/brand/logos/` and plan to use an actual logo file from there if one exists?
- Did I read both frontend-design references?
- Did I define exact global CSS variable, Tailwind/shadcn token, and shadcn component style updates?
- Am I following required domain-skill structure while using authored visual composition wherever the domain skill leaves room?
- Did I choose a deliberate direction for color, motion, spatial composition, and background atmosphere instead of a generic shell?
- Can this UI be built with zero cards? If not, is every remaining card unavoidable under the narrow allowed cases?
- Are there no top-level cards?
- Am I avoiding sidebars unless explicitly requested or required by a selected domain skill?
- Does the first screen focus on one dominant working surface instead of title + filters + KPI strip + card grid + table?
- Am I avoiding large framed hero/detail/inspector surfaces?
- Is the layout airy with generous spacing, not dense?
- Is the inner density airy too: rows, tables, cards, and metadata blocks are not cramped or over-columned?
- If no domain skill overrides radius language, does the UI lean clearly rounded rather than vague enterprise 4/6/8 radii?
- Does the typography feel distinctive and intentional rather than default/generic?
- Do page background, canvas, nav chrome, and any focal surface separate clearly at thumbnail scale?
- Are all foreground colors readable against their backgrounds, including brand-colored areas, disabled states, labels, placeholders, badges, buttons, icons, and muted text?
- Do inputs, search/filter controls, tables, and header/nav chrome have enough tonal separation from the page background?
- In light mode, do all editable controls, including normal text inputs and selects, actually use near-white or very light tinted backgrounds rather than page-colored fills?
- Are editable controls free of `bg-transparent`, `bg-background`, `bg-muted`, and same-token page/panel fills?
- Do summary/inspector/live-summary panels use a clear near-white/light-tinted surface instead of blending into the page?
- If there is a header/topbar, does it use a clear translucent treatment with backdrop blur and enough contrast?
- If a table is surfaced, is it using `shadow-xs` plus generous header and row padding?
- If a sidebar is required, is it using a darker primary-derived tone with enough width, padding, row height, and overflow handling?
- Are shadows limited to contact-edge depth?
- Does the design feel specific to this domain and task?

## Implementation Rules

- Prefer topbar, tabs, segmented controls, breadcrumbs, command rows, stepped flows, drawers, sheets, dialogs, or detail routes over sidebars.
- Before adding any card-like wrapper, try open spacing, typography, dividers, rows, tonal bands, tables, drawers, sheets, dialogs, or detail routes.
- In tables and row-based views, prefer fewer columns, richer rows, taller row rhythm, and clearer vertical stacking when that makes the UI feel more airy and readable.
- Surfaced tables should usually use `shadow-xs`, generous header padding, and generous body row padding rather than relying only on borders.
- Detail views should prefer inline split layout, selected rows, dividers, tonal sections, drawers, or sheets before any framed panel.
- If a `Card` component is imported or a card-like wrapper remains, add a nearby inline justification explaining why it is unavoidable under the allowed cases.
- Use good readable UI fonts. Avoid typewriter/blog fonts unless the domain explicitly requires that character.
- Use more expressive composition, stronger accent hierarchy, and more atmospheric backgrounds wherever they do not conflict with required workflow structure or operational clarity.
- Keep surfaces distinct through tone, spacing, and hierarchy rather than borders and boxes around everything.
- Choose foreground/text colors for contrast first. Do not treat brand primary/secondary/accent colors as body text colors unless they are clearly readable on that exact surface.
- Give inputs/selects/textareas/search fields explicit contrasting fills; do not leave them transparent or page-colored.
- Give summary/inspector/live-summary panels explicit contrasting fills when they are unavoidable.
- If a header/topbar exists, use token-driven translucent background, `backdrop-blur-md`, and clear contrast rather than a flat same-color strip.
- For required sidebars, use enough width and item height for readable labels, visible active states, and non-clipping badges/actions.
- If a card is truly unavoidable, give it intentional tonal contrast from the canvas plus a visible but soft border. Weak same-white cards fail.
- Add only shadcn components required by the actual workflow.
- Always customize shadcn component classes/styles so inputs, buttons, tables, tabs, dialogs, sheets, popovers, and navigation follow this app's visual rules instead of default component styling.
- Use custom CSS classes for enhanced layouts, backgrounds, spacing, and component treatments when Tailwind utilities become limiting; keep those classes token-driven through `var(...)` colors, radii, borders, and shadows from the global theme.
- Keep all buttons, links, menus, dialogs, tabs, forms, routes, and localStorage-backed state functional.

## Pre-Completion Audit

Search the implementation for `Card`, `card`, `bg-card`, `shadow-md`, `shadow-lg`, `shadow-xl`, repeated `rounded-* border` wrappers, and large `rounded-* border p-*` sections.

Reject and revise if:

- Any top-level card exists.
- Any avoidable card remains.
- Any large rounded bordered region reads as a hero card, inspector card, or detail card.
- A sidebar exists without an explicit user request or selected domain-skill requirement.
- The first screen is mostly panels, cards, KPI blocks, helper boxes, or equal-weight modules.
- Surface separation depends mostly on borders instead of tone.
- Same-white or near-white panelization makes major surfaces blend together.
- Any text, icon, label, placeholder, disabled text, badge, button text, table text, or data value is hard to read against its background.
- Brand colors are used without deriving a high-contrast foreground/text color for the actual background.
- Inputs, search/filter controls, data rows, or header/nav chrome blend into the page background.
- Editable controls in light mode are not near-white or very light tinted and therefore do not read clearly.
- Selects are contrasted but normal text inputs remain page-colored or muted.
- Editable controls use `bg-transparent`, `bg-background`, `bg-muted`, or the same token/fill as the page or panel.
- Summary/inspector/live-summary cards or panels use the same fill as the page instead of a near-white/light-tinted contrast surface.
- A header/topbar exists but lacks a clear translucent `backdrop-blur-md` style or blends into the page.
- Row/table content is cramped, over-columned, or too tight inside the first column and metadata blocks.
- A surfaced table is missing `shadow-xs` or its header/rows are padded too tightly.
- `public/brand/logos/` contains a usable logo file but the header still uses a placeholder logo or no logo without reason.
- Brand colors from `.tasks/domain.md` are not reflected in primary/active/focus treatment.
- The UI defaults to a generic admin shell instead of using authored composition where the workflow allowed it.
- A required sidebar uses a weak pale surface instead of a darker primary-derived tone.
- A required sidebar clips labels, badges, icons, or actions, or uses cramped item padding/row height.
- The UI falls back to vague enterprise middle-radius controls even though no domain skill asked for that.
- Typography falls back to generic fonts or lacks a distinctive display/body pairing when the product could support one.
- Theme variables were not configured before component styling.
- shadcn components are used as-is without app-specific class/style customization.
- Custom CSS uses hardcoded one-off colors/radii/shadows instead of global theme variables.
- The screen feels cramped or all modules have equal weight.
- The UI looks like a starter admin template, Bootstrap dashboard, or generic AI/SaaS app.
