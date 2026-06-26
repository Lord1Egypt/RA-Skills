# QA Checklist for Car-Sleep Guides

Clear this checklist before exporting PDF.

## 1. Data integrity

- [ ] Every route number was checked after the latest night-anchor decision.
- [ ] Scenic latest entry / opening hours were verified.
- [ ] Charger and parking claims are verified.
- [ ] Toilet claims are verified if the guide depends on them.
- [ ] Generic 24h parking/charging was not misrepresented as explicit overnight permission.
- [ ] No schedule-critical number was guessed.

## 2. Itinerary logic

- [ ] Each night anchor is chosen intentionally, not just by scenic proximity.
- [ ] A generic public charger parking lot is not ranked above a stronger camping / car-sleep signal point without reason.
- [ ] Day 1 first-night strategy is realistic after a long drive.
- [ ] The next-morning departure logic is plausible.
- [ ] Holiday traffic buffer is visible.
- [ ] If the night anchor changed, dependent scenic order and times were updated.

## 3. Visual quality

- [ ] No blank screenshots.
- [ ] No QR-heavy screenshots.
- [ ] No clutter-heavy full-page screenshots.
- [ ] Images support the overnight decision instead of filling space.

## 4. Copy quality

- [ ] Tone is formal enough for a guide.
- [ ] The chosen overnight anchors are explicit.
- [ ] The reason each anchor wins is explicit.
- [ ] Risks and fallback options are visible.
- [ ] Candidate / fallback / retreat labels are clear when certainty differs by point.

## 5. Output quality

- [ ] HTML renders cleanly before export.
- [ ] File name matches the car-sleep scenario.
- [ ] Local file delivery uses relative `MEDIA:./...` paths when applicable.
