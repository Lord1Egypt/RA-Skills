# Version history

## 0.1.9
- Require Lead number before intake handoff


## 0.1.8
- Require Lead number before estimator flow


## 0.1.7
- Added ClawHub publish metadata headers (`homepage`, `metadata.openclaw.emoji`) for registry publishing.


## 0.1.6 - 2026-04-05
- Clarified that public real estate/property data should be preferred for square footage when available.
- Added Google Earth measurement fallback guidance for houses, driveways, patios, decks, walkways, and fences when dimensions are missing.

## 0.1.5 - 2026-04-05
- Renamed skill from `property-estimator` to `residential-property-rolling-suds-estimator`.
- Updated Rolling Suds branding in skill metadata and repo/project naming.

## 0.1.4 - 2026-04-05
- Added rule: partial-house requests should produce two quotes: a confident recommended whole-house quote and a separate $250 partial-only minimum comparison quote.

## 0.1.3 - 2026-04-05
- Added rule: partial house requests should generally convert to a whole-house recommendation because the $250 minimum makes full-house pricing the better customer value.
- Clarified that partial-scope internal notes can still be preserved while presenting whole-house pricing.

## 0.1.2 - 2026-04-05
- Added explicit version markers inside `SKILL.md` and `pricing-rules.md`.
- Added `iteration-notes.md` as a scratchpad for future collaboration and refinement.

## 0.1.1 - 2026-04-05
- Added rule: if only one service is requested, minimum total charge is $250.
- Set window cleaning to exterior-only.
- Clarified that single-service estimates must reflect the minimum charge before presentation.

## 0.1.0 - 2026-04-04
- Initial release of property-estimator.
- Added St. Louis service-area rules, house-wash pricing, flatwork pricing, sidewalks, decks, fences, and simple window-count pricing.
- Added photo-first estimating mode and vehicle-based driveway heuristics.
- Added chain-link fence manual-review rule.
