# Pricing rules

Current pricing rules version: **0.1.6**

## Service area
- St. Louis, MO metro area
- Maximum service radius: 50 miles

## Global quoting rule
- All outputs are estimates only
- Final pricing may change after photo review or on-site inspection before entry into Workiz
- If the customer is only buying one service, minimum total charge is $250

## House wash
Minimum: $250

### Partial house requests
- If only one portion of the house is requested, the single-service minimum still applies.
- In most cases, present whole-house pricing as the better value because partial house washing would still hit the $250 minimum.
- For partial house requests, show both:
  - recommended whole-house quote
  - partial-only quote at $250 minimum
- This comparison should make the better-value whole-house recommendation obvious to the customer.

### Size-based pricing
- 1500 sq ft -> $300
- 1700 sq ft -> $325
- 2000 sq ft -> $325
- 2500 sq ft -> $350
- 3000 sq ft -> $375
- 3500 sq ft -> $400
- 4000 sq ft -> $425
- 4500 sq ft -> $470
- 5000 sq ft -> $500
- Over 5000 sq ft -> $0.10/sq ft

### Material upcharges
Apply to likely stucco/brick exteriors:
- 1500-2500 sq ft -> +$50
- 3000-4000 sq ft -> +$100
- 4500-5000+ sq ft -> +$150

Apply to likely wood exteriors:
- 1500-2500 sq ft -> +$50
- 3000-4000 sq ft -> +$100
- 4500-5000+ sq ft -> +$150

## Flatwork pricing
Use for driveways, patios, and front porches.

### Visual driveway classes
Use these heuristics when exact dimensions are unavailable but photos are available:
- small / short single-width driveway -> usually map to 100-150 sq ft pricing
- standard residential driveway -> usually map to 200 sq ft pricing
- larger 2-car or extended driveway -> usually map to 400 sq ft pricing
- oversized or clearly expanded driveway -> consider 400-600 sq ft pricing and mention uncertainty

### Vehicle-based driveway heuristics
Use these when the user describes what fits on the driveway instead of giving dimensions:
- one standard sedan with little spare room -> 100-150 sq ft class
- two vehicles side-by-side but not much extra depth -> 200 sq ft class
- two-car width with useful extra room behind at least one vehicle -> 200-400 sq ft class
- two-car width with a full-size pickup and trailer or clearly long parking depth -> 400 sq ft class
- extra-wide or extra-deep parking apron with multiple long vehicles and obvious spare area -> 400-600 sq ft class

When using these heuristics, note that the driveway size is inferred from vehicle fit rather than measured directly.

### Flatwork table
- 100 sq ft -> $50
- 150 sq ft -> $75
- 200 sq ft -> $100
- 400 sq ft -> $150
- 600 sq ft -> $200

### Paver/slate add-on
Tentative from pricing sheet:
- smaller jobs -> +$25
- larger jobs -> +$50
If size tier is unclear, mention the add-on as a possible adjustment rather than hard-coding it.

## Sidewalks / walkways
Price by linear feet.

- 10 ln ft -> $25
- 25 ln ft -> $50
- 50 ln ft -> $75
- 75 ln ft -> $100
- 100 ln ft -> $125
- 150 ln ft -> $150

## Decks
Use for deck footprint pricing.

- 100 sq ft -> $75
- 150 sq ft -> $100
- 200 sq ft -> $125
- 400 sq ft -> $150
- 600 sq ft -> $200
- 800 sq ft -> $250

### Natural wood deck disclaimer
If deck is natural wood:
- Washing may strip stain/finish
- Customer is responsible for re-staining after cleaning

### Heavy deck rule
There is an unconfirmed note indicating more pressure / more time and possibly 1.75x charge.
Do not apply 1.75x automatically unless the user later confirms it.
For now, mention unusual deck condition as a possible photo-required adjustment.

## Fences
Estimate by likely fence type and visible linear feet.

### Black iron fencing (soft wash)
- 100 ln ft -> $50
- 200 ln ft -> $100
- 300 ln ft -> $125

### Vinyl fencing
- 100 ln ft -> $75
- 200 ln ft -> $150
- 300 ln ft -> $225

### 3-panel fencing
- 100 ln ft -> $100
- 200 ln ft -> $175
- 300 ln ft -> $250

### Natural wooden, no stain
- 100 ln ft -> $125
- 200 ln ft -> $250
- 300 ln ft -> $450

### Chain link fencing
- Recognize chain link as a valid fence type
- Do not auto-price chain link fencing
- Mark chain link as manual review / custom quote
- Exclude chain link from automatic estimate totals unless the user later provides a pricing rule

### Natural wood fence disclaimer
If fence is natural wood or wood finish is uncertain:
- Washing may strip stain/finish
- Customer is responsible for re-staining after cleaning
- Recommend photo confirmation when finish is unclear

## Window cleaning
- $4 per window
- Exterior only
- Count 1 pane as 1 window
- If a window opens by sliding up, count it as 2 windows technically
- If only some elevations are visible, estimate visible count first and note unseen sides as assumptions

### Window pricing note
Use this as a simple exterior-only estimate rule for now.
If only one service is being quoted and the window total falls below $250, use the $250 minimum service charge.

## Estimate disclaimer
Use this wording or very close to it:
- This is an estimate only. Final pricing may change after photo review or on-site inspection before entry into Workiz.

## Sales workflow note
This estimator is for a salesperson to later input into Workiz.
Prefer practical ranges and explicit assumptions over fake precision.
If only one service is requested, enforce the $250 minimum before presenting the final total.
