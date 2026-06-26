---
name: residential-property-rolling-suds-estimator
description: Estimate exterior cleaning services for Rolling Suds from a U.S. residential property address using public property information, attached exterior photos, map/listing context, and a fixed pricing rubric for power washing and window cleaning. Use when a user wants a ballpark quote, pre-quote assessment, or sales estimate for house washing, driveways, patios, porches, sidewalks, decks, fences, or window cleaning, especially for St. Louis metro residential properties that will later be entered into Workiz.
homepage: https://github.com/mwdearing/residential-property-rolling-suds-estimator
metadata:
  {
    "openclaw":
      {
        "emoji": "🏠"
      },
  }
---

# Residential property Rolling Suds estimator

Current skill version: **0.1.9**

Estimate residential exterior cleaning work from an address. Produce a salesperson-friendly estimate that is useful for later entry into Workiz.

This skill works best when fed a cleaned handoff from `quote-intake`, though it can also work from direct user input.

## Core rules

- Require the salesperson to provide the **Lead number** before estimating. Example: `Lead 502` or `Lead 501`.
- If the Lead number is missing, stop and ask for it before continuing.
- Treat every result as an **estimate**, not a final quote.
- If the customer is getting only one service, enforce a **$250 minimum service charge**.
- Prefer attached exterior photos when available; they are often more useful than public listing snippets.
- Use public property/listing/map data when available.
- If property data is incomplete or conflicting, say so clearly and give a conservative range.
- Ask for photos when condition, material, access, or feature count cannot be estimated confidently.
- Keep tone practical and sales-friendly, not legalistic.
- Always include the estimate disclaimer.
- Service area is the **St. Louis, MO metro area** with a maximum radius of **50 miles**.

## Output format

Use this structure:

0. **Lead reference**
   - Lead number

1. **Property summary**
   - address
   - estimated square footage
   - stories if inferable
   - likely exterior materials
   - visible extras (driveway, patio, deck, fence, walkways, window count clues)

2. **Service estimate**
   - each service line item with assumptions
   - quantity basis (sq ft, linear ft, counted windows)
   - price per service

3. **Estimate summary**
   - low estimate
   - target estimate
   - high estimate
   - confidence: low / medium / high

4. **Follow-up notes**
   - what should be confirmed by salesperson or photos
   - upsell opportunities

5. **Disclaimer**
   - This is an estimate only. Final pricing may change after photo review or on-site inspection before entry into Workiz.

## Research workflow

1. Confirm the address is a valid U.S. residential property.
2. If exterior photos are attached, inspect them first for:
   - siding/material type
   - driveway width/length class
   - visible patio/porch/walkway area
   - deck type and finish
   - fence type and approximate length
   - window count clues
   - access difficulty, staining, algae, oxidation, and condition
3. Gather public property facts where possible:
   - square footage
   - stories
   - exterior materials
   - lot layout
   - visible driveway/patio/deck/fence/walkway features
   - listing photos or map imagery when available
4. Prefer real public property/listing data for square footage when available.
5. If exact dimensions are still unavailable, recommend Google Earth measurement as the fallback for house footprint, driveway/patio/deck square footage, and walkway/fence linear footage.
6. Prefer photo-backed assumptions over weak public-web assumptions when the two conflict.
7. Infer likely service scope.
8. Apply the pricing rules in `references/pricing-rules.md`.
9. If exact measurements are unavailable, estimate conservatively and state assumptions.
10. If the property appears outside the St. Louis service area or beyond 50 miles, say so.

## Estimating guidance

### House wash
- Use known square footage if available.
- If exact square footage is unavailable, estimate based on public listing data.
- Apply stucco/brick or wood upcharges when exterior type likely matches.
- Use conservative assumptions when material is unclear.
- If the customer asks for only part of the house, remember the single-service minimum is $250.
- When partial house washing would still hit the minimum, recommend whole-house pricing as the better customer value.
- For partial house requests, provide both: (1) a confident recommended whole-house quote and (2) a separate partial-only quote at the $250 minimum so the value comparison is obvious.

### Driveways, patios, porches
- Estimate visible flatwork area in square feet.
- When photos are attached, classify driveways visually as narrow/small, standard, or large and map that to the pricing table.
- Front porches use patio pricing.
- If shape/coverage is unclear, provide a low-target-high range.

### Sidewalks
- Estimate by linear feet.
- If walkway layout is unclear, state that the estimate assumes visible front and side walk sections only.

### Decks
- Use deck pricing table for visible deck footprint.
- If deck appears natural wood, include the stain-strip disclaimer.
- If deck condition/material is unclear, ask for photos for confirmation.

### Fences
- Estimate by visible linear feet and likely fence type.
- Distinguish between black iron, vinyl, 3-panel, natural wood, and chain link when possible.
- If fence type is chain link, recognize it but do not price it automatically.
- For chain link, mark it as manual review / custom quote and exclude it from automatic totals.
- If wood finish is unclear, use caution and request photos.
- For natural wood fences, include the stain-strip disclaimer.

### Windows
- Use $4 per counted window.
- Window cleaning is **exterior only** for now.
- Count 1 pane as 1 window.
- If a window opens by sliding up, count it as 2 windows.
- If photos are attached, estimate only from visible sides and clearly note unseen elevations.
- If exact count is not visible, estimate from visible elevations and state assumptions.
- Treat window pricing as estimate-only unless photos or counts are provided.

## Confidence rules

Use **high** confidence when:
- square footage is known or strongly supported
- major surfaces are visible in attached photos or clear public imagery
- materials are identifiable
- service scope is straightforward

Use **medium** confidence when:
- square footage is known or strongly inferred
- some features are estimated from imagery
- counts are partly inferred

Use **low** confidence when:
- square footage is missing
- materials are unclear
- rear-yard features are not visible
- window/fence/deck counts are mostly guessed

## Required disclaimers

Always include:
- **Estimate only:** Final pricing may change after photo review or on-site inspection before entry into Workiz.

Include for natural wood decks and fences when relevant:
- **Natural wood notice:** Washing may strip stain/finish. Customer is responsible for re-staining after cleaning.

## Workiz-oriented behavior

Optimize for salespeople who will later enter the job into Workiz:
- require the Lead number before estimating
- preserve the Lead number in output so the estimate stays tied to the correct lead
- keep line items clean
- keep assumptions obvious
- avoid over-explaining
- prefer a usable range over fake precision
- note missing information that salesperson should confirm
- if only one service is requested, make sure the total reflects the $250 minimum service charge

## When information is missing

If the Lead number is missing, do not estimate yet. Ask for the Lead number first.

If public data is too thin, do not invent certainty.
Instead:
- use attached photos if available
- provide a conservative estimate range
- list assumptions
- say what photos or answers would tighten the quote
- recommend Google Earth measurement when surface dimensions or linear footage are the main blocker

## Photo-first estimating mode

When 1-5 exterior photos are attached:
- treat them as primary evidence for visible scope and condition
- still use public property data for square footage and general property context when available
- separate what is **visible** from what is **assumed**
- never pretend unseen rear-yard or side-yard features are confirmed unless visible or documented
- tighten the range when photos materially reduce uncertainty

Useful photo observations include:
- siding type: vinyl, brick, stucco, wood, mixed
- driveway class: 1-car short, 1-car long, 2-car standard, 2-car extended, oversized
- patio/porch footprint class
- fence type and visible length class
- deck size and finish
- visible mildew, algae, oxidation, rust, or heavy buildup
- window style clues for count estimation

## Vehicle-based driveway estimating

When the user describes parked vehicles instead of giving dimensions or photos, use vehicle fit as a practical sizing clue.

Examples:
- one standard sedan fitting tightly in width with little extra depth -> usually 100-150 sq ft class
- two vehicles side-by-side with shallow depth -> usually 200 sq ft class
- two-car width with one sedan/SUV and clear extra space behind -> often 200-400 sq ft class
- two-car width with pickup/truck plus trailer or long extra depth -> often 400 sq ft class
- clearly oversized parking apron or multiple long vehicles with abundant spare room -> consider 400-600 sq ft class

State that vehicle-based sizing is an estimate heuristic, not a measured dimension.

Read `references/pricing-rules.md` before estimating.
