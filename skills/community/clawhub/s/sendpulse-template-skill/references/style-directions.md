# Visual Style Directions & Working With References

> Read this to give each email a distinct, non-generic look, and to reproduce a design the user
> likes. Two inputs: (a) a curated style-direction library so output isn't cookie-cutter, (b) a
> user-supplied reference (screenshot or URL) that you analyze and rebuild as valid email HTML.

## Table of Contents
1. How to choose a direction
2. The style-direction library
3. Analyzing a user-supplied reference
4. Where users can find references
5. Keeping it email-safe

---

## 1. How to choose a direction

- If a `brand-profile.md` exists, the brand's palette/typography wins — pick the direction that fits
  the brand, don't override it.
- Otherwise infer from the type + audience: promo → Bold Promo; luxury/beauty → Luxury Serif;
  SaaS/welcome → Clean Minimal; dev/finance → Corporate; consumer fun → Playful.
- Offer the user 2–3 named directions to choose from in Pro mode; just pick the best fit in Quick mode.
- Mixing is fine (e.g. Clean Minimal layout + one Bold Promo hero) — keep it coherent.

## 2. The style-direction library

Each direction is a coherent recipe: palette logic, typography, spacing, imagery, button shape.

**A. Clean Minimal / Editorial**
Lots of whitespace, 1 accent color, near-black text on white, generous line-height, thin separators,
left-aligned text, small uppercase labels. Buttons: solid accent, modest radius. Good for: welcome,
newsletter, SaaS, B2B.

**B. Bold Promo**
Big saturated hero, large headline, high-contrast CTA, color blocks, price/discount as a focal badge.
2–3 strong brand colors. Buttons: large, high-contrast, pill or sharp. Good for: sales, Black Friday,
flash deals.

**C. Luxury / Serif**
Restrained palette (black/cream/gold or muted tones), serif display headings, lots of negative space,
fine hairline rules, centered composition, small tracking-wide labels. Buttons: outline or thin solid.
Good for: fashion, beauty, jewelry, premium services.

**D. Playful / Friendly**
Rounded shapes, warm/bright palette, illustration-style imagery, friendly sans, emoji-light accents,
larger radius buttons, soft section backgrounds. Good for: D2C, food, lifestyle, kids, community.

**E. Dark Premium**
Dark background (near-black, not pure), light text, neon/jewel accent, glowing CTA, product imagery
on dark. Verify dark-mode behavior (already dark — watch full-invert clients). Good for: tech,
gaming, crypto, events. (See dark-mode-accessibility.md.)

**F. Corporate / Trust**
Blue/navy + grey, structured grid, conservative type, clear hierarchy, data/table-friendly, subtle
accents. Buttons: solid, small radius. Good for: finance, B2B, transactional, official notices.

For each: derive a 4–6 color palette (page bg, content bg, text, muted, primary, accent), one font
family, a radius value, and a spacing rhythm — then feed those into the html-rules.md patterns.

## 3. Analyzing a user-supplied reference

When the user shares a **screenshot or image** of an email/design they like (you are multimodal):
1. **Extract the palette** — name the dominant bg, text, and 1–2 accent colors as HEX.
2. **Read the layout** — single vs multi-column, hero style, card grid, spacing density.
3. **Read the typography** — serif vs sans, weight contrast, heading scale, alignment.
4. **Name the mood** — which library direction is it closest to?
5. **Rebuild, don't copy** — reproduce the *feel* (palette, rhythm, hierarchy) as a fresh,
   email-safe template using html-rules.md patterns. Do not pixel-copy a competitor's email or
   lift their copyrighted images; generate equivalents with placehold.co or the user's assets.

When the user shares a **URL**: ask them to send a screenshot if you can't fetch/render it reliably,
or use a fetch tool if available — but always rebuild as a valid SendPulse fragment, not a paste.

## 4. Where users can find references

Point users to galleries of **real production emails** (better than generic design pins):
- **Really Good Emails** (reallygoodemails.com) — categorized, some with HTML.
- **Milled** (milled.com) — searchable archive of brand emails.
- **Email Love** (emaillove.com) — curated gallery.
Pinterest can inspire mood, but its pins aren't email HTML and it can't be scraped — have the user
screenshot anything they like and send it for analysis.

## 5. Keeping it email-safe

Whatever the direction, the output must still obey html-rules.md: tables only, inline styles,
CSS-table buttons, separator-row spacing, Outlook fallbacks, dark-mode-safe colors. Style lives in
the **palette, type, spacing, and imagery choices** — never in unsupported CSS.
