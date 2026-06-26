# Shadcn Setup And Theming

Use this reference when implementing shadcn/ui + Tailwind.

## Order

1. Inspect `components.json`, global CSS, `tailwind.config.*`, app routes/layouts, `components/ui/*`, and `package.json`.
2. Read domain/brand inputs and selected domain skill rules.
3. Define tokens.
4. Update global CSS variables, Tailwind theme extension, and shadcn component styles.
5. Verify the tokens exist in the real files.
6. Build screen details with Tailwind utilities and/or custom CSS classes that reuse the same tokens.

Do not build screens first and theme later.
Do not let Tailwind utility availability limit the design. Custom CSS is allowed when it produces a cleaner, more distinct, minimal UI, but it must reuse global CSS variables and theme tokens.

## Required Token Roles

Set or verify:

- `--background`
- `--foreground`
- `--card`
- `--card-foreground`
- `--popover`
- `--popover-foreground`
- `--primary`
- `--primary-foreground`
- `--secondary`
- `--secondary-foreground`
- `--muted`
- `--muted-foreground`
- `--accent`
- `--accent-foreground`
- `--destructive`
- `--destructive-foreground`
- `--border`
- `--input`
- `--ring`
- `--radius`
- chart/status colors when used

Map tokens by role. Do not copy brand colors into every variable.
Foreground tokens must be derived for readability, not copied from the brand palette. Every `*-foreground` token must have clear contrast against its paired background token.
If the selected domain skill does not define a sharper or specific radius system, set `--radius` and component radii to a clearly rounded modern default rather than timid enterprise values.
For CPQ, CRM, trades, and similar business/domain skills, preserve the selected skill's required product structure while enforcing the theme rules: brand-aware tokens, actual logo usage, airy spacing, strong input contrast, rounded controls, soft/tight shadows, cardless defaults, and authored composition where the domain skill leaves room.
Use theme tokens to create a cohesive, vivid, authored aesthetic rather than a neutral default.

## Light Surface System

- Page background: tinted pale gray, stone, cream, porcelain, glacier, or brand-derived tint.
- App canvas: lighter off-white/porcelain, not raw white everywhere.
- Navigation chrome: translucent near-white or very light tinted tone unless a required sidebar uses the darker primary-derived treatment.
- Required sidebars: much darker primary-derived tone or a darker companion tone from the same palette, not a pale washed-out sidebar.
- Focal surface: clear tonal difference, not a repeated large card.
- Inputs: near-white or very light tinted in light mode, near-black in dark mode, and clearly editable across normal inputs, selects, textareas, search fields, date fields, and comboboxes.
- Unavoidable summary/inspector panels: clear near-white or light tinted surface in light mode, near-black in dark mode, not same-fill with the page.
- Borders: soft but visible and selective.
- Popovers/sheets/dialogs: clear separation with contact-edge depth.

Do not use the same white for body, app frame, cards, popovers, inputs, and controls.
Navigation chrome must remain visibly distinct from the main canvas. If a header/topbar exists, prefer `backdrop-blur-md` with roughly `70-80%` opacity on a tokenized near-white/light-tinted or near-black surface.
Do not rely on a faint border alone to separate a major surface from the canvas.
Editable controls must not share the page/background fill.
Inputs, selects, textareas, search fields, date fields, and similar controls must use near-white or very light tinted backgrounds in light mode.
In dark mode, those same controls must move to near-black so they still read distinctly against the overall canvas.
Do not only fix select components while leaving normal inputs, textareas, or search fields page-colored.
Pure white is not required. Near-white is usually enough when the separation is obvious.
Search inputs, filter fields, and command-row controls must use one of the clearest light surfaces on the screen in light mode so they remain obvious at a glance.
Do not style editable controls with `bg-transparent`, `bg-background`, `bg-muted`, or the same token/fill as the page or panel.
Set `--input` so it is visibly lighter than `--background` in light mode and visibly darker than the canvas in dark mode.

## Brand Mapping

- Main brand/accent -> `--primary`, primary buttons, links, active navigation, selected records, focus.
- `--primary-foreground` -> high-contrast text/icon color over `--primary`; derive it for contrast, do not reuse another brand color just because it is in the palette.
- Secondary brand colors -> supporting accents only when useful.
- `--secondary-foreground`, `--accent-foreground`, `--card-foreground`, `--popover-foreground`, and `--muted-foreground` must remain readable on their paired surfaces.
- Compatible tints -> backgrounds, muted surfaces, borders, status colors.
- Destructive stays red.
- No generic purple/blue unless brand/domain supports it.
- First check `public/brand/logos/`. If that folder contains a usable logo file, use that actual logo in the header or primary app chrome. Only create or invent a logo if that folder does not exist or has no usable logo files.

## Tailwind Use

Use Tailwind when it is the clearest fit for:

- shell dimensions
- topbar/tabs/command rows or explicitly required sidebar behavior
- spacing/gutters/grid tracks
- row rhythm
- table density
- status chips
- responsive behavior

Prefer larger section padding, wider gutters, taller row rhythm, and more space between control groups. Slightly over-spaced is acceptable; cramped is not.
Carry that spacing into inner content as well. Table rows, list rows, cards, badges, metadata groups, and inline actions should breathe; do not solve a data-dense view by cramming too many narrow columns onto one line.
When a table is surfaced as a primary or secondary working object, give it `shadow-xs`, generous header padding, and generous row padding by default.
If no selected domain skill overrides radius language, prefer rounded/pill-like controls and avoid defaulting to 4px/6px/8px-style admin radii.
Where the selected domain skill leaves room, let the layout become more asymmetrical, expressive, and product-shaped instead of defaulting to safe symmetry.

## Custom CSS

Use custom CSS classes when Tailwind utilities make the UI too generic, cramped, or hard to tune.

- Reuse global tokens with `var(...)` for colors, borders, radii, shadows, focus rings, and background treatments.
- Keep custom CSS in the app's normal stylesheet path, usually `app.css` or the project equivalent.
- Custom CSS is appropriate for authored backgrounds, layered surfaces, table rhythm, sidebar layout, complex responsive grids, input contrast, and shadcn component refinements.
- Do not hardcode unrelated one-off colors, radii, or shadows when an existing token should express the system.
- Do not hardcode low-contrast foreground colors. If custom CSS uses a brand background, set a high-contrast foreground with the appropriate token or a readable derived color.
- Prefer custom classes over long unreadable Tailwind strings when the design needs precision.

## Cards

Do not import `Card` by default.

- No top-level cards.
- No large sibling `Card` panels.
- No card grids.
- No cards inside cards.
- Do not use card wrappers as generic spacing/grouping.
- No large rounded bordered hero/detail/inspector regions that still read like cards.

If a card-like wrapper remains, justify it inline. Acceptable reasons: unavoidable repeated item separation after row/divider options fail, dialog/popover/sheet containment, concise notice, or true emphasis.
If a card is unavoidable, it must have intentional tonal contrast from the canvas plus a visible but soft border. Same-white cards fail.

## Sidebars

Do not build a sidebar by default.

- Use a sidebar only when the user explicitly requested one or a selected domain skill explicitly requires one.
- Prefer topbar, tabs, segmented controls, breadcrumbs, command rows, step flows, sheets, drawers, or detail routes.
- If required, keep the sidebar quiet and secondary, but not cramped.
- Required sidebars need enough width, row height, padding, and overflow handling for readable labels, badges, icons, and active states.
- Do not let primary labels, badges, icons, or actions clip off the sidebar edge; truncate only secondary descriptions.
- Never combine a sidebar with top-level cards or a card-heavy workspace.

## Depth

Use contact-edge depth only:

- Contact 0: no shadow plus low-opacity border.
- Contact 1: `0 0 0 1px rgba(16,24,40,0.07), 0 1px 0 rgba(16,24,40,0.08)`.
- Contact 2: `0 0 0 1px rgba(16,24,40,0.08), 0 1px 2px rgba(16,24,40,0.10)`.
- Contact 3: `0 0 0 1px rgba(16,24,40,0.08), 0 2px 3px rgba(16,24,40,0.10)` for floating UI only.

Prefer `shadow-2xs` for buttons and compact interactive controls.
Prefer `shadow-xs` for cards, tables, and similar contained surfaces.
Reserve `shadow-xl` for popovers and banners.
Reserve `shadow-2xl` for dialogs.
Avoid `shadow-sm`, `shadow-md`, `shadow-lg`, blur halos, muddy gray clouds, colored glows, and heavy card shadows as broad defaults.
Depth should read as soft, tight edge contact, not lift.
Soft means the edge is diffused and not harsh. It does not mean the shadow must be extremely faint; a decently gray tight shadow is acceptable when needed for contrast.

## shadcn Components

Add only components required by the workflow. Common examples:

```bash
npx shadcn@latest add button input label select textarea badge separator dialog dropdown-menu table avatar tooltip scroll-area sheet popover tabs checkbox radio-group
```

Do not install components because dashboard examples usually include them.
After adding or using shadcn components, always customize their classes/styles. Treat shadcn as base primitives, not finished UI. Inputs, selects, textareas, tables, tabs, buttons, dialogs, sheets, popovers, and navigation must inherit the app's tokenized visual system rather than looking like default shadcn.

## Typography

- Avoid generic defaults like Arial and Inter.
- Choose a more beautiful and distinctive font direction.
- Prefer a characterful display face plus a refined body face when the product can support it.
- Encode that choice into the actual theme and component styling instead of mentioning it only in planning text.

## QA

Before finishing:

- Theme variables are configured before component styling.
- shadcn component styles are customized for the app rather than used as-is.
- Custom CSS, when used, reuses global variables instead of hardcoded one-offs.
- Domain brand colors are mapped when present.
- Major groups have generous gaps.
- Inner row/table/card content has generous gaps too and is not cramped by too many same-line columns.
- Surfaced tables use `shadow-xs` and generous header/body padding.
- No top-level cards exist.
- Any remaining card is unavoidable and justified.
- No large hero/detail/inspector surface still reads like a card.
- Major surfaces separate from the canvas through tone, not only border.
- Foreground/background token pairs are readable: primary, secondary, accent, card, popover, muted, input, sidebar, and destructive.
- Text, icons, labels, placeholders, disabled text, badges, buttons, table text, and data values have enough contrast against their actual rendered background.
- Inputs, search/filter controls, and header/nav chrome read clearly against the page background in both light and dark modes.
- Editable controls use near-white/lightest-surface backgrounds in light mode and near-black backgrounds in dark mode.
- Normal inputs, textareas, search fields, and selects all share the same contrast rule; selects cannot be the only controls with proper surface contrast.
- Editable controls do not use transparent, muted, background, or same-fill treatments.
- Summary/inspector/live-summary panels use clear near-white or light-tinted contrast surfaces when they are unavoidable.
- If a header/topbar exists, it uses a tokenized translucent surface with `backdrop-blur-md` and enough contrast.
- If no selected domain skill overrides radius language, controls and key UI surfaces read clearly as a rounded modern system.
- Typography feels intentional and distinctive rather than default.
- If a sidebar is required, it uses a darker primary-derived tone rather than a pale generic surface.
- If a sidebar is required, it has enough width, row height, padding, and overflow handling to avoid clipped labels/actions.
- Theme and composition feel authored rather than like a default admin shell, including inside business/domain skill layouts where the skill leaves room.
- No sidebar exists unless explicitly requested or required by selected domain skill.
- No heavy Tailwind shadows remain.
- `shadow-2xs` is used for buttons/small interactive items when shadow is needed.
- `shadow-xs` is used for cards/tables/similar contained surfaces when shadow is needed.
- Any use of `shadow-xl` is limited to popovers and banners.
- Any use of `shadow-2xl` is limited to dialogs.
- Buttons, links, menus, dialogs, tabs, forms, routes, and localStorage-backed state work.
