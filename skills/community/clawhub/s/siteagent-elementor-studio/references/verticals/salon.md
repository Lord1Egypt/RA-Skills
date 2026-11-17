# Salon — studio build pack

**When to use:** a hair salon, beauty studio, barber, or spa selling on style and experience.

## Voice & positioning
Warm, stylish, a little aspirational — the page should feel like the chair you can't wait to sit in. The visitor wants to picture themselves looking great and know it's easy to grab a slot. Let the imagery carry the mood; keep copy short and inviting. **Primary conversion: book now** (sticky/header button, repeated through the page). Show price ranges so booking feels low-risk.

## Design system
- **Palette** (maps onto brand-kit tokens — `brand` / darker shade / `accent` / `heading` / `text` / `muted`):
  - primary `#B07A57` · primary-dark `#7E5238` · accent `#E6C7A8` · dark `#2A2320` · body-text `#4A423C` · muted `#9A8E84`
  - Warm taupe + soft caramel reads premium and editorial; let large photos breathe against it.
- **Typography:** an elegant serif for headings (Playfair Display or Cormorant, 500) paired with a clean sans body (Inter/Nunito Sans, 400). Use `<em>` inline for a single italic emphasis word in display headings.
- **Spacing/rhythm:** editorial — section padding 100–120px, boxed ~1280px, full-bleed gallery rows. Subtle, not loud.

## Section flow (top → bottom)
1. **Hero** — mood headline + subhead + **Book Now** CTA over a strong lifestyle image.
2. **Services menu** — cuts, color, styling, treatments with price ranges; use Tabs by category if the list is long.
3. **Gallery / portfolio** — before/after or "looks we love" grid; this is the real sales pitch.
4. **Stylists** — team cards with names, specialties, and a "book with [name]" link.
5. **Offers / membership** — first-visit offer, loyalty or package pricing; one clear value prop, not a coupon dump.
6. **Reviews** — short client quotes, first name + initial.
7. **Contact / booking** — booking widget or form, hours, location/map + footer.

## Build notes
- Use the matching recipes in `references/recipes.md` (Hero, Services grid, Testimonials, Pricing for the menu, Contact); bind colors/fonts to the named tokens in `references/brand-kit.md`.
- Gallery: build one image card with native widgets, then `duplicate-element` per shot — keep it editable, never an HTML dump. If posts/CPT drive the gallery on Pro, use Loop Grid.
- Gotcha: real, well-lit photos make or break this vertical — if the client has none yet, flag it; placeholder stock undercuts the aspirational tone. Keep the price menu easy to update (one container, duplicated rows).
