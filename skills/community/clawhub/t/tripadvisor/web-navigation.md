# Tripadvisor Web Navigation Playbook

Use this when API key is missing, rate-limited, or when user wants visual confirmation.

## Stable URL-first paths

- Hotels in city: `https://www.tripadvisor.com/Hotels-g{geoId}-{City}-Hotels.html`
- Restaurants in city: `https://www.tripadvisor.com/Restaurants-g{geoId}-{City}.html`
- Attractions in city: `https://www.tripadvisor.com/Attractions-g{geoId}-Activities-{City}.html`
- Entity detail pages follow `/Hotel_Review-...`, `/Restaurant_Review-...`, `/Attraction_Review-...`

## Practical flow

1. Open destination vertical page directly when geoId is known.
2. Apply visible filters (price, amenities, rating tiers).
3. Capture top candidates with rating + review count + price signal.
4. Open detail pages for finalists only.
5. Build shortlist with tradeoffs and confidence notes.

## Known blockers in live browsing

- Cookie consent dialogs (`I Accept` / `Reject All`) can block progress until resolved.
- Dynamic overlays can temporarily hide controls after search interactions.
- Some search flows may redirect to anti-bot interstitial pages.

## Safe fallback strategy

- If an interaction fails due overlays, use direct URLs.
- If anti-bot page appears, stop and continue via API mode or user-driven manual navigation.
- Never attempt bypass tooling.
