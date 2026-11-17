---
name: ui-master
description: "Use this skill whenever the user wants to build, refine, or review a production-grade user interface with Tailwind CSS v4 and shadcn/ui. Triggers include: building a landing page, dashboard, auth flow, admin panel, marketing site, SaaS UI, or any React/Next.js component or page; requests to 'make it look production-grade / polished / professional'; setting up Tailwind v4 (@theme, CSS-first config) or installing/theming shadcn/ui; establishing a design token system (color, type, spacing, radius, shadow); or auditing an existing UI for accessibility, responsiveness, and visual quality. Works for both Next.js App Router and general React (Vite, React Router, TanStack Start) projects. Do NOT use for backend-only tasks, non-Tailwind CSS frameworks (Bootstrap, Chakra, MUI) unless the user is migrating to Tailwind, or one-off brand/marketing design exploration with no code output — see the frontend-design skill for pure aesthetic direction."
---

# UI Master — Production-Grade UI with Tailwind v4 + shadcn/ui

Approach this as a senior UI engineer who owns the design system of a real product, not a prototype. Every screen you produce should be something a design lead would ship without a "make it feel less AI-generated" pass. That means: a token system that a real theme is built from (not a scattering of arbitrary hex values), components composed from shadcn/ui primitives rather than reinvented, and a UI that survives contact with real content — long names, empty states, slow networks, keyboards, screen readers, and small viewports.

This skill covers the full production loop: **set up the foundation → establish tokens → compose with shadcn/ui → build the layout → verify quality.** Read the reference file that matches the step you're on; don't load everything up front.

## Step 0 — Confirm the stack

Before writing code, resolve two things (infer from the repo if present, otherwise ask once, briefly):

1. **Framework**: Next.js App Router, or general React (Vite / React Router / TanStack Start)? Setup commands and file locations differ — see `references/tailwind-v4-setup.md` and `references/shadcn-setup.md`, both cover both paths.
2. **Starting point**: greenfield project (needs Tailwind v4 + shadcn/ui installed from scratch) or existing project (needs an audit of what's already configured — check for `@theme` in the CSS entrypoint and a `components.json` before reinstalling anything).

Never re-run `shadcn init` on a project that already has a `components.json` — it will prompt to overwrite theme files. Check first.

## Step 1 — Foundation: Tailwind v4

Tailwind v4 is CSS-first: there is no `tailwind.config.js` to write. Design tokens are declared with `@theme` directly in the CSS entrypoint, and content detection is automatic. Read `references/tailwind-v4-setup.md` for exact install commands (differ by framework), the `@theme` syntax, and the v3→v4 migration pitfalls (renamed utilities, removed `@apply` patterns, the two-stage token setup needed for runtime dark mode).

Key thing to internalize now: because `@theme` values are baked into generated utility classes at build time, naive `@theme` color tokens **break runtime dark-mode switching**. The correct pattern is raw OKLCH/HSL channel values in `:root` / `.dark`, mapped through a non-inline `@theme`. Don't skip this — it's the single most common production bug in v4 setups.

## Step 2 — Design tokens

Before adding a single component, define the token system: color roles (not raw palette — `primary`, `muted`, `destructive`, not `blue-500`), a type scale with 2 font roles (display/body, plus an optional mono for data), spacing/radius scale, and elevation (shadow) scale. Read `references/design-tokens.md` for the full token checklist and OKLCH-based palette construction (OKLCH keeps perceptual lightness consistent across hues, which matters for accessible contrast at scale).

Naming by role, not value, is what makes a rebrand or theme swap a one-file change instead of a find-and-replace across the codebase.

## Step 3 — Component layer: shadcn/ui

shadcn/ui is not a component library you `npm install` — the CLI copies component source into your repo, so you own and can edit every component. Read `references/shadcn-setup.md` for the init flow, `components.json` fields, adding components, and theming via CSS variables (which meshes directly with the token system from Step 2).

Compose UI from shadcn primitives (`Button`, `Card`, `Dialog`, `Form`, `Table`, `Sheet`, `Command`, etc.) rather than building raw `<div>` soup — this is what makes the output read as production software rather than a mockup. Only drop to custom markup for layout scaffolding and truly bespoke elements.

## Step 4 — Layout and page composition

For full-page composition (landing pages, dashboards, auth flows), read `references/design-tokens.md`'s layout section and the worked examples in `examples/`:

- `examples/landing-page.tsx` — marketing/SaaS landing page: hero, social proof, feature grid, pricing, CTA, footer
- `examples/header.tsx` — standalone sticky/blurred header: desktop nav, mobile `Sheet` nav with correct focus trap, and a Cmd/Ctrl+K command-palette trigger
- `examples/sidebar.tsx` — deep dive on shadcn's `Sidebar` component family: `collapsible="icon"` mode, `SidebarRail` hover-toggle, grouped/collapsible nav sections, active-route styling via `isActive`, and the `group-data-[collapsible=icon]:hidden` pattern for hiding labels when collapsed
- `examples/dashboard-layout.tsx` — authenticated app shell: sidebar nav, topbar, content region, data table pattern, responsive collapse
- `examples/auth-page.tsx` — sign-in/sign-up pattern: split layout, form validation states, error/loading states
- `examples/ai-chat-components.tsx` — AI agent/chat UI pieces: message bubbles (user vs. assistant), typing indicator vs. streaming cursor (distinct states, don't conflate them), markdown-in-bubble rendering with a copyable code block, and an auto-resizing prompt input with the Enter-to-send / Shift+Enter-newline convention

Treat these as structural references to adapt, not templates to paste verbatim — the actual copy, imagery, and one signature visual choice per page should come from the specific brief (see the `frontend-design` skill if a distinctive art-direction pass is also needed; this skill is complementary — it covers the engineering and system side, `frontend-design` covers aesthetic risk-taking).

## Step 4b — Modern effects (optional, use deliberately)

If the brief calls for a visually distinctive moment — glassmorphism, layered/mesh gradients, scroll-driven reveals, 3D tilt, animated gradient borders, or richer micro-interactions than a plain `hover:` transition — read `references/modern-effects.md`. It covers each technique with Tailwind v4 syntax, the CSS escapes needed where no utility exists (multi-layer gradients, `animation-timeline`, `@property`), and the browser-support caveats and fallbacks each one needs.

**Restraint still applies**: pick the one effect that serves this screen's signature moment, keep the rest of the page quiet. A card with a glass blur AND an animated gradient border AND a 3D tilt all at once reads as a tech demo, not a product.

## Step 5 — Verify before calling it done

Read `references/accessibility-performance-checklist.md` and walk it before presenting the UI as finished. Non-negotiable production floor:

- Responsive from ~360px mobile through desktop, tested at real breakpoints, not just resized-browser eyeballing
- Keyboard-reachable and visibly focused on every interactive element (`focus-visible`, not just `:hover` styling)
- Color contrast meets WCAG AA at minimum for text and meaningful icons
- Loading, empty, and error states designed — not left as a blank `<div>` or a raw thrown error
- `prefers-reduced-motion` respected for any animation
- No layout shift from images/fonts loading (explicit dimensions, `font-display` handled)

## Common failure modes to avoid

- **Config drift**: writing `tailwind.config.js` out of v3 habit when the project is v4 CSS-first — check which one is present before configuring.
- **Raw hex sprinkled through components**: every color should resolve to a token (`bg-primary`, `text-muted-foreground`), never a literal `#3b82f6` in component code.
- **Reinventing shadcn primitives**: hand-rolling a modal when `Dialog` already exists in the project's `components/ui` — check what's already installed first.
- **Ignoring dark mode until the end**: if the product needs dark mode, wire the two-stage token pattern from Step 1 before building components, not after.
- **Decorative-only structure**: numbered steps, badges, or dividers that don't encode real information — see `frontend-design` skill's guidance on structure as information.
- **Untested empty/error states**: a dashboard demoed only with perfect seed data will visibly break in front of a real user on day one.
- **Hand-rolled sidebar collapse logic**: reimplementing icon-collapse/expand state instead of using `Sidebar`'s `collapsible="icon"` + `useSidebar()` — the built-in version already handles the mobile Sheet fallback, keyboard shortcut, and `group-data-[collapsible=icon]` styling hooks correctly.
- **Effects stacked without restraint**: combining glassmorphism, an animated gradient border, and a 3D tilt on the same element — see `references/modern-effects.md`'s restraint note.
- **Conflating "typing" and "streaming" states in a chat UI**: showing the bouncing-dots indicator while tokens are already arriving, or vice versa — they're different states and should render differently (see `examples/ai-chat-components.tsx`).
- **Rendering user input as markdown**: only the assistant's messages should go through a markdown renderer; rendering raw user text as markdown/HTML is both unnecessary and a potential injection surface.
