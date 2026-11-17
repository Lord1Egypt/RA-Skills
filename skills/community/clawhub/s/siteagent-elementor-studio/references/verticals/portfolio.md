# Portfolio — studio build pack

**When to use:** a web developer, designer, or creative freelancer who needs the work to do the selling.

## Voice & positioning
Minimal and confident — let the projects speak; the copy just frames them. The visitor (often a hiring manager or prospective client) is scanning for proof you can do *their* kind of work, then a low-friction way to reach you. First person, direct, no buzzword soup. **Primary conversion: hire me / get in touch** (header button + a closing CTA). One strong point of contact beats five.

## Design system
- **Palette** (maps onto brand-kit tokens — `brand` / darker shade / `accent` / `heading` / `text` / `muted`). Restrained, mostly monochrome with one accent:
  - primary `#6C5CE7` · primary-dark `#4A3FB0` · accent `#00D1B2` · dark `#0E0E12` · body-text `#3A3A42` · muted `#8A8A96`
  - Near-black + a single electric accent reads modern and technical; let whitespace and the work carry the page. Dark-mode-friendly.
- **Typography:** a sharp sans pairing — headings in Space Grotesk or Sora (600), body in Inter (400); optionally a mono (JetBrains Mono) for the tech stack labels.
- **Spacing/rhythm:** lots of air — section padding 100–140px, boxed ~1140px, big type, tight content. Restraint is the aesthetic.

## Section flow (top → bottom)
1. **Hero** — name + what you build, one line + **Get in Touch** CTA. Short. No tagline soup.
2. **Work / projects grid** — the centerpiece: 4–6 case-study cards (thumbnail, project name, role, stack, result), each linking to detail or live site.
3. **Skills / stack** — languages, frameworks, tools — grouped, scannable, honest about depth.
4. **About** — a few human lines + a photo; who you are and how you work.
5. **Process** — 3–4 steps (discover → build → ship) so clients know what working with you feels like.
6. **Testimonials** — short quotes from clients/colleagues (optional but powerful).
7. **Contact** — email/contact form + links (GitHub, LinkedIn) + footer. Make replying trivial.

## Build notes
- Use the recipes in `references/recipes.md` (Hero, Services/cards grid for the work grid, Logos strip for the stack, Split for About, Testimonials, Contact); bind colors/fonts to the named tokens in `references/brand-kit.md`.
- Project grid: build one case-study card with native widgets, `duplicate-element` per project, `update-element` for each — editable, not an HTML dump. On Pro, if projects are a CPT, use Loop Grid.
- Gotcha: every project should link somewhere real (live URL or write-up) — dead "coming soon" tiles erode credibility. Keep the contact path to one click; don't bury the email behind a multi-field form.
