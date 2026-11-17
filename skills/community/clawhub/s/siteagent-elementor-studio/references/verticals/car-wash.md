# Car wash — studio build pack

**When to use:** an express/tunnel car wash, detailing shop, or multi-location wash brand pushing memberships.

## Voice & positioning
Bold, fast, energetic — clean cars, quick in-and-out, big savings on the unlimited plan. The visitor wants to compare wash packages and see how cheap "unlimited" really is per month. Punchy headlines, strong numbers, high contrast. **Primary conversion: view plans / join unlimited** (header CTA + a sticky plan-pick button). Make the membership math obvious.

## Design system
- **Palette** (maps onto brand-kit tokens — `brand` / darker shade / `accent` / `heading` / `text` / `muted`):
  - primary `#0A6CE0` · primary-dark `#08489C` · accent `#FFC23D` · dark `#121A24` · body-text `#2C3742` · muted `#8390A0`
  - Electric blue + a high-energy yellow accent reads fresh, fast, and value-forward.
- **Typography:** a bold geometric sans for headings (Montserrat or Sora, 700–800) with a sturdy sans body (Inter, 400). Big, confident sizes.
- **Spacing/rhythm:** punchier than the calmer verticals — section padding 72–96px, boxed ~1280px, strong color blocks between sections. Rounded pill buttons.

## Section flow (top → bottom)
1. **Hero** — value headline ("Unlimited washes from $X/mo") + subhead + **View Plans** CTA over a dynamic wash/clean-car image.
2. **Wash packages + pricing** — 3–4 tier cards (Basic → Works), price + what's included, "most popular" highlighted; this is the page's center of gravity.
3. **Unlimited membership** — the recurring-plan pitch: per-month price, cancel-anytime, wash-as-often-as-you-want; clear join button.
4. **How it works** — 3 steps (pick a plan / drive up / scan & go).
5. **Locations & hours** — address list or map; per-site hours.
6. **App / loyalty** — app store badges or RFID/loyalty perk if they have one.
7. **Reviews** — quick, upbeat customer quotes.
8. **Contact / join** — plan-select form or signup, location picker + footer.

## Build notes
- Use the recipes in `references/recipes.md` (Hero, Pricing for the tiers, Stats band for the membership numbers, Contact); bind everything to the named tokens in `references/brand-kit.md`.
- Pricing tiers: build one tier card with native widgets, `duplicate-element` for the rest, then `update-element` per tier — keep it editable so the client can change prices without code.
- Gotcha: keep the unlimited plan's terms honest and visible (price, billing cadence, cancellation) — vague "unlimited" claims invite chargebacks. If signup isn't wired to a real processor yet, flag the form as visual-only.
