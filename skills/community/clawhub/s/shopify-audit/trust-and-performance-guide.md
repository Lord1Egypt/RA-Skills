# Trust & Performance Guide — Signals and Speed Targets for Shopify

## Trust signal placement (where, not just whether)

| Signal | Best placement | Common mistake |
|---|---|---|
| Review stars + count | Under PDP title, visible without scroll on mobile | Buried in a tab or below the fold |
| Photo reviews | First 3 reviews shown | Sorted by date, surfacing thin reviews |
| Return policy | One line near ATC ("30-day free returns") | Footer-only |
| Shipping promise | Announcement bar + PDP near ATC + cart | Stated only at checkout (too late) |
| Payment badges | Checkout footer + cart | Plastered on homepage hero (signals insecurity) |
| Guarantee | PDP below ATC | Vague "satisfaction guaranteed" with no terms |
| Support contact | Header/footer + checkout | Chat widget covering the mobile ATC |
| UGC/press | Homepage strip + PDP gallery | Fake "as seen in" logos (legal + trust risk) |

Trust-stack rule of thumb for an unknown brand's PDP, top to bottom: stars → shipping/returns line → ATC → guarantee → photo reviews. The buyer should never have to scroll to learn the store is safe to buy from.

### Honesty boundaries

- Inventory scarcity only from live stock; review counts only from real reviews (purchased-review schemes get apps delisted and stores flagged).
- No resetting countdown timers; no fake "X people viewing".
- "Free shipping" must be unconditional or threshold-labeled everywhere it appears.

## Performance targets (mobile, the binding constraint)

| Metric | Target | Failing symptom |
|---|---|---|
| LCP | <2.5s | Hero/product image arrives late |
| CLS | <0.1 | Layout jumps as apps inject banners |
| INP | <200ms | Variant taps feel laggy |
| Page weight (PDP) | <2MB | Multi-MB images, autoplay video |
| App scripts | Every app justified | 10+ apps, several unused |

### The usual Shopify offenders, in fix order

1. **Hero media:** multi-MB images or autoplay video. Fix: WebP/AVIF, <300KB hero, poster + tap-to-play for video.
2. **App accumulation:** each review/upsell/popup/chat app injects JS site-wide. Fix: uninstall unused apps (and remove leftover theme code), defer chat widgets until interaction.
3. **Non-optimized uploads:** 4000px supplier images served raw. Fix: Shopify CDN handles resizing if the theme requests proper sizes — check `image_url` width parameters in older themes.
4. **Font stacking:** 4+ custom font weights. Fix: 2 weights max, `font-display: swap`.
5. **Carousel libraries:** heavy sliders for content nobody swipes. Fix: static hero, native scroll-snap galleries.

### Measurement protocol

- PageSpeed Insights on: homepage, top collection, top PDP — mobile scores.
- Test the PDP with the highest paid-traffic spend first; that's where speed converts to money fastest.
- Record before/after for every performance fix; attribute honestly (speed fixes land alongside copy fixes — don't double-count).

## Theme-editor quick wins (no developer needed)

- Enable star-rating block on product templates (most OS 2.0 themes)
- Free-shipping progress bar in cart (native in Dawn-family themes)
- Sticky ATC toggle (theme setting in most premium themes)
- Image lazy-loading (default in OS 2.0 — verify on older themes)
- Express checkout buttons (Settings > Payments, one toggle)
- Automatic discounts (Discounts > Automatic) to neutralize the code-field exit
