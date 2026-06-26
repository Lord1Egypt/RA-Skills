---
name: real-estate-listing-coach
description: Coach real-estate agents and FSBO sellers through listing optimization — pricing strategy, MLS description writing, photo direction, staging priorities, marketing channel mix, open-house playbook, and negotiation prep. Diagnoses overpriced/stale listings, weak photos, weak description, wrong price band positioning. Calibrates by market type (seller's, balanced, buyer's), property type (SFR, condo, multifamily, land), and price tier (entry, move-up, luxury). Also coaches buyer's agents on offer strategy and listing critiques. Use when asked to write or improve a listing description, set list price, plan a listing, get a stale listing unstuck, prepare for an open house, structure a price reduction, write an offer, or critique a listing. Triggers on "real estate listing", "MLS description", "list price", "stale listing", "price reduction", "open house", "FSBO", "for sale by owner", "real estate marketing", "offer letter", "buyer offer".
metadata:
  tags: ["real-estate", "listings", "mls", "sales", "marketing", "fsbo", "negotiation", "agents"]
---

# Real Estate Listing Coach

Coach a listing through pricing, marketing, presentation, and negotiation — like a top-producing agent in the same market. Assumes the user is either a licensed agent looking for a critique or a FSBO seller who can't afford one.

## Usage

**Basic invocation:**
> Write an MLS description for a 3BR/2BA Craftsman in Portland, OR
> My listing's been on market 45 days with 3 showings — diagnose
> Set list price for [address or specs]
> Plan my open house this weekend

**With context:**
> 1924 Craftsman, 1,820 sf, walkable East Portland, garage ADU rental potential, original woodwork. List target $725k.
> Suburban Texas SFR, 4/3, 2,800 sf, neighborhood comp range $410k–$485k, just appraised at $458k.
> NYC 2BR coop, $1.4M, 4 weeks, 12 showings, no offers. Maintenance $2,800/mo.
> Tampa FL condo, 1/1 oceanfront, $389k, hurricane insurance issue surfaced after offer.

The coach takes inputs (listing specs, market data, photos if available, days-on-market, showing/offer count) and returns a diagnosis, fixed-position recommendations, and ready-to-paste copy.

## Coaching Modes

The agent runs different playbooks based on what the user needs:

1. **New listing prep** — pricing, photos, description, marketing plan, open-house calendar
2. **Stale listing rescue** — diagnosis (price, presentation, exposure, terms), corrective plan
3. **Description rewrite** — MLS-compliant, SEO-aware, agent-voice copy
4. **Pricing strategy** — comp analysis, market-condition adjustment, price-band positioning
5. **Open house playbook** — timing, signage, sign-in process, follow-up
6. **Buyer offer prep** — offer letter, escalation clause, contingency strategy, counter playbook
7. **Listing critique** — read a competitor's listing or your own as a third party

## Pricing Strategy

The job: find the price that maximizes seller's net while clearing in target days. Inputs:

- 3 active comps (currently listed)
- 3 sold comps (last 90 days, same submarket, same property type, ±15% sf, ±20yr age)
- 1–2 expired/withdrawn comps (warning data)
- Market temperature: months of inventory (<3 = seller's, 3–6 = balanced, >6 = buyer's)
- Seasonal adjustment (Spring 5–8% premium in most US markets)
- Property condition relative to comps
- Unique features (view, lot, ADU, energy, etc.)

Three pricing approaches:

| Approach | Use when |
|---|---|
| **Anchor below psychological band** ($999k vs $1.05M) | Hot market, need showings, buyers searching with caps |
| **Market-rate, room to negotiate** | Balanced market, comp range tight |
| **Above market, "luxury / unique"** | Truly differentiated property, willing to wait, price-discovery |

**Pricing red flags the coach calls out:**

- "I want $X" pricing without comp basis — this is how listings die
- Pricing based on what was paid + improvements (sunk cost; market doesn't care)
- Pricing $1 above a search-cap threshold ($500,001 vs $499,000 = invisible to a search bracketed at $500k)
- Net-pricing for FSBO without buyer-agent commission accounted for

**Days-on-market triggers for adjustment:**

| Market type | DOM trigger | Action |
|---|---|---|
| Seller's (<3 mo inventory) | 14 days no offer | Quality issue (photos/desc/showings) |
| Balanced (3–6 mo) | 30 days | Reduce 2–3% or improve presentation |
| Buyer's (>6 mo) | 45 days | Reduce 4–6% or significant change |

Price reductions of <3% are usually a waste — pull back to a fresh search bracket (round number) or skip.

## Description Writing (MLS)

Constraints:
- MLS character limit (varies, typically 800–1500 for public remarks, 200–300 for headline)
- Fair Housing compliance — no language about target demographics, no "perfect for", no community demographic descriptors, no school commentary that implies exclusion
- No URLs, phone numbers, agent contact in public remarks (varies by MLS)

**Anatomy of a great MLS description:**

1. **Hook** (first sentence) — the one thing this house has that the comps don't. Lead with it.
2. **Story paragraph** (3–5 sentences) — the lifestyle, the flow, the moments. Specific, sensory, not flowery.
3. **Spec paragraph** (3–4 sentences) — bedrooms, baths, square footage, lot, garage, year built, recent updates. Numbers and facts.
4. **Location paragraph** (2–3 sentences) — neighborhood, walkability, commute, named landmarks (no schools).
5. **Call to action** (1 sentence) — "schedule a private showing" / "open Saturday 11–1" / "offers reviewed Tuesday 5pm."

**Writing rules:**
- Specific verbs over adjectives. "Sun pours through south-facing windows at breakfast" beats "lovely natural light."
- Concrete details over labels. "Hand-honed soapstone counters and a 36-inch dual-fuel range" beats "chef's kitchen."
- Cut "must-see," "won't last," "rare opportunity." Lazy and meaningless.
- Use the property's actual era and architecture. "1926 Craftsman" lands; "charming home" floats.
- Don't oversell. Buyers are spooked by hyperbole.

**Headline templates (200 char):**

- "1924 Craftsman with original millwork + garage ADU, 4 blocks to Hawthorne"
- "Renovated 4/3 with primary suite addition, walk to top-rated [district name]"
- "Top-floor 2BR coop with park views, low maintenance, prewar charm"

**Public remarks template (full):**

> Sun pours through original leaded glass and a freshly refinished oak floor — this 1924 Craftsman in Portland's Sunnyside has been quietly modernized without losing its bones. The 1,820-square-foot floor plan opens at the front porch, flows through a formal dining with built-ins to a renovated kitchen with quartz, soapstone island, and Bertazzoni range. Three bedrooms upstairs, including a primary with a walk-in closet built behind original moldings. A finished, permitted detached ADU above the garage rents at $1,650/mo or hosts visitors. Newer roof (2022), updated electrical and plumbing, mini-split HVAC. Two blocks to Hawthorne Boulevard, four to Mount Tabor. Offers reviewed Monday 5pm.

## Photo Direction

Even the best description loses to a flat photo. Coach checklist for photographer brief:

- Hero exterior shot — twilight or "golden hour" if architecture justifies; bright daylight otherwise
- Wide-angle living spaces but NOT distorted (90° lens max, not fisheye)
- One vertical for each major room (works in carousel and PDF flyer)
- Detail shots: hardware, original features, custom millwork, new appliances, fixtures
- Yard / outdoor: at least 3 if there's any outdoor amenity
- Floor plan as image #5 or #6 (buyers consume floor plans heavily)
- Aerial / drone for >0.25 acre lot, view, or unique site
- Twilight shot if the home has a strong street presence or interior lighting
- 25–30 photos optimal; 40+ shows desperation; 12 shows laziness

**Pre-shoot checklist sent to seller:**
- All countertops cleared
- Toilet seats down
- Beds made hotel-style
- All blinds at the same height, fully open
- Lights on in every room (yes, even if photographer adjusts)
- Cars off the driveway, trash bins moved
- Fresh flowers on dining table, fruit in a bowl on kitchen island
- No personal photos, no kid's art on fridge
- Pets out for the day

## Marketing Channel Mix

| Channel | Use when | Effort/cost |
|---|---|---|
| MLS + Zillow / Realtor / Redfin syndication | Always | Auto |
| Listing-specific Instagram reel (60s) | Photogenic property, agent has audience | M |
| Single-property website | $1M+ or unique architecture | M |
| Facebook ad to local zip codes (radius targeting) | Slow market or unusual property | $300–800/wk |
| Just-listed mailer (1-mile radius, 500–1000 doors) | Neighborhood-pride markets | $500–1200 |
| Email blast to agent's database | Always | Low |
| Broker tour / agent open | $500k+, every listing | Low |
| Public open house | First weekend, then judiciously | Low |
| YouTube walkthrough | Luxury or vacation home | M |
| Print (newspaper, magazine) | $2M+ or local convention | $$$$ |

## Open House Playbook

**Pre-open:**
- Sign-up reminder via Just Listed neighbors
- Yard signs go up Friday afternoon, directional signs Saturday morning at 6 corners min
- Stage with light scent (lemon/herb, not cinnamon — too aggressive)
- Tunes low — instrumental, classical, jazz
- One light on every floor, blinds all open
- Print 25 4-page color flyers + 1-page agent contact
- Set up sign-in at the entry — names + email/phone, gentle ask
- Tray of water, light snack, but not branded coffee shop
- Bathrooms staged with fresh towels, flowers, soft soap

**During:**
- Greet, point them to flyer, mention three highlights
- Let buyers move freely; don't follow
- Listen — buyers say what they want when they think you're not listening
- Note any agent (other agent walking through = potential offer source)
- Strong closing on serious-looking buyers: "If you came back tomorrow, what would your offer feel like?"

**Post:**
- Same-evening text to every sign-in: "thanks for coming, here's the flyer link"
- Within 24h: phone follow-up to anyone who lingered
- Week-of: feedback summary to seller (turnout, comments, weak spots)

## Stale Listing Diagnosis

When a listing isn't moving, the issue is one of four:

1. **Price** — Most common. If showings >5 and no offers, price/value gap.
2. **Photos / presentation** — Showings <2/week in active market = top-of-funnel issue (photos, headline, syndication).
3. **Property issues** — Smell, layout, deferred maintenance, neighbor noise. Buyers come, leave fast.
4. **Terms / commission** — Buyer-agent commission below market in MLS = fewer agents push it. Co-op compensation matters.

The coach asks for these data points and runs the matrix:

- Price vs comps (over 5%? over 10%?)
- Showings per week (under benchmark for market temp?)
- Offer count (any low offers indicate price; zero offers indicates listing-side issue)
- Average DOM in submarket vs this listing's DOM
- Photos compared to top-3 active competitors
- Description compared to top-3 active competitors

Then proposes one of:
- **Refresh** — new photos, rewrite description, withdraw and relist with fresh DOM
- **Reduce** — to next bracket break (round number)
- **Restage** — declutter / move out / professional staging
- **Re-strategy** — different agent, different MLS sub-area, different listing approach

## FSBO Mode (no agent)

When the user is a FSBO seller, the coach addresses three things agents normally handle:

1. **Pricing** — without MLS access, use Zillow / Redfin / public records; pull 5 sold comps within 0.5 mi, 6 mo, ±15% sf.
2. **Photo / description** — pay $250–500 for pro photographer; copy the structure above.
3. **Buyer-agent commission** — offer 2.5–3% in the MLS or via flat-fee MLS service ($300–600); without this, agents won't bring buyers.

FSBO disclosure: by 2026, NAR settlement changed buyer-agent comp display. Verify what your local MLS rules require.

## Buyer Offer Strategy

Seven knobs an offer can use to win, in order of typical importance:

1. **Price** — 1–10% over list in hot market, at-list in balanced, below in cold
2. **Earnest money** — 1–3% standard; higher = signal of strength
3. **Down payment / financing** — cash > 25% down > 20% conventional > FHA/VA (perceived risk)
4. **Inspection contingency** — info-only inspection, shorter window, or limited remedy
5. **Appraisal contingency** — partial waiver up to $X gap; full waiver only with cash reserves
6. **Close timing** — match seller's needs (fast / leaseback / specific date)
7. **Personal letter** — banned/discouraged in many markets due to Fair Housing risk; coach default = skip

**Escalation clause template:**

> Buyer agrees to pay $X over the highest competing offer up to a maximum purchase price of $Y, provided that Buyer is notified of the competing offer in writing with seller's name redacted. Cap escalation at $Y to maintain budget discipline.

Don't escalate without a cap. Don't waive inspection if you don't have $20–50k in reserves for surprises.

## Output Format

The coach returns:

1. **Diagnosis** (if rescue mode) — top 3 reasons it's not selling
2. **Pricing recommendation** — list, target close, walk-away
3. **Description** — paste-ready, MLS-compliant
4. **Photo brief** — list of shots needed, staging requests
5. **Marketing plan** — first 14 days timeline
6. **Open house plan** (if applicable)
7. **Negotiation prep** — what offers to expect, counter strategy

No fluff. No "synergize." Just the play that wins this listing.
