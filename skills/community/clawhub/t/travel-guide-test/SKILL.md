---
name: travel-guide-pages
description: Plan trips end-to-end and turn them into polished static travel-guide webpages deployed to Cloudflare Pages. Use when a user wants help deciding where to go, comparing route/base options, shaping an itinerary around interests and constraints, choosing hotels and activities, building a visual travel guide, adding route maps or booking checklists, or publishing the result as a live Cloudflare Pages microsite.
---

# Travel Guide Pages

Build a useful trip first, then build the webpage.

## Core approach

Follow this sequence:
1. Discover the travellers, constraints, and vibe.
2. Decide the route logic before writing a day-by-day itinerary.
3. Build a realistic itinerary with energy management.
4. Add hotels, activities, transport legs, and booking urgency.
5. Turn the plan into a skimmable, image-led static webpage.
6. Deploy to Cloudflare Pages.

Do not jump straight to “top things to do”.
Do not optimise for maximum attractions.
Optimise for fit, flow, energy, and clarity.

## Discovery checklist

Before proposing an itinerary, gather or confirm:
- destination(s)
- trip length
- who is going
- ages if relevant
- whether they have been before
- interests
- explicit dislikes / hard nos
- budget level
- pace preference: slow / packed / balanced
- style preference: practical / premium / adventurous / relaxing / design-led / traveller-friendly
- willingness to drive
- luggage or mobility constraints
- likely airports / rail / car usage

If details are missing, ask only the highest-value questions first.

### Family / mixed-age optimisation branch

If the trip includes children, teens, mixed generations, or a group with clearly different energy levels, ask a more specific second layer:
- ages of each traveller
- interests by person, not just for the group overall
- any hard no's by person
- food pickiness / flexibility
- sleep, nap, jet lag, or bedtime constraints
- stamina / walking tolerance / motion sickness / transport tolerance
- rooming needs (e.g. one room vs two rooms, sofa bed vs separate beds, privacy needs)
- what the adults also want from the trip so the plan does not become child logistics only

Ask about gender only when it would materially affect rooming, privacy, safety, or comfort decisions.
Do not ask for personal details that do not change the plan.

## Route logic

Work out the structure before the days.

Always determine:
- number of bases
- best order of places
- whether the route should be rail, road, air, or mixed-mode
- where rental car pickup happens
- where rental car return happens
- where mixed-mode handoffs happen

For mixed-mode travel, label legs explicitly. Examples:
- `Train + car pickup`
- `Scenic drive`
- `Drive to rail gateway + train into city`

Do not collapse mixed-mode travel into vague one-line labels.
If a leg uses two modes, show both.

## Itinerary design rules

Design for humans, not robots.

Account for:
- arrival fatigue / jet lag
- group pacing / energy differences
- sensory overload
- realistic travel times
- recovery after big days
- flexibility for weather and mood
- rooming and sleep practicality when relevant

Use an energy curve:
- stimulating days
- slower reset days
- headline days
- transition days
- flexible buffer days

Common helpful pattern:
- arrival/reset day
- lighter recovery day after long travel if needed
- major highlight day once people are functioning well
- calmer or flexible day after a big one

## Recommendations structure

For each base/segment, provide:

### Why stay here
Explain what this base adds to the trip and why it suits the travellers.

### What to do
Recommend only high-fit activities.
For each one include:
- why it fits
- rough travel time
- whether it is essential / optional / weather-dependent
- whether it is half-day or full-day
- booking urgency if relevant

### Where to stay
Provide a short practical shortlist, ideally:
- best practical option
- best stylish option
- best upgrade option (if relevant)

Explain the hotel logic:
- space / room fit
- location convenience
- scenery
- transport access
- vibe

### Transport logic
Be explicit about:
- train start/end points
- car pickup location
- car return location
- rail handoff point
- what each leg is actually doing

## Day-by-day output

Create a realistic day-by-day plan.
For each day include:
- day title
- location/theme
- key plan
- travel mode/time if relevant
- effort/energy level when useful
- whether it is a highlight / reset / transition / flex day

Keep it concise and skimmable.

## Traveller profiles and reusable preferences

Support reusable traveller profiles when helpful.

Default to a shared profile for the main travelling unit:
- individual
- couple
- family
- recurring friend group
- recurring multi-generational group

Use individual subprofiles only when useful or explicitly requested.
A shared group profile should be the default; per-person profiles are optional layers, not mandatory dossiers.

The skill may:
- create a primary group profile
- create optional traveller-specific subprofiles when they materially affect planning
- reuse an existing profile for future travel planning
- update the profile after a trip or after the user clarifies a preference

Only store durable travel-planning preferences, such as:
- trip pace
- budget style
- hotel preferences
- transport tolerance
- rooming preferences
- food preferences
- activity preferences
- hard no's
- destination preferences
- children’s ages/interests when relevant to future planning
- traveller-specific constraints only when they materially affect planning

Good pattern:
- primary family/couple/group profile for shared defaults
- optional subprofile for notable exceptions, e.g. motion sickness, food restrictions, very different activity tolerance, or strong preferences

Do not treat the profile as a dossier.
Do not store unnecessary sensitive or irrelevant personal details.
Store only information that improves future travel recommendations.

When saving or updating profile information, follow the environment’s consent and memory rules.
If profile information is uncertain, summarise it as a tentative preference rather than a hard fact.

When a returning traveller or group is involved, check whether a profile already exists before re-asking basic planning questions.
Reuse what is durable, then ask only for what has changed.

## Planning extras

Always include:

### Book in advance
Split into:
- must book early
- can book later
- flexible / low urgency

### Weather / packing
Keep practical and brief.

### Travel tips / hacks
Include only useful tips:
- booking strategy
- luggage strategy
- local transport logic
- timing / crowd avoidance
- family pacing

Avoid social-media fluff unless it is genuinely helpful.

## Webpage requirements

Build a static HTML/CSS page suitable for Cloudflare Pages.

Style goals:
- premium travel editorial
- clean, skimmable, uncluttered
- image-led
- useful before clever

Suggested sections:
- cover / hero
- trip overview
- route summary
- route map + leg links
- day-by-day itinerary
- visual galleries by place
- hotel suggestions
- transport logic
- booking checklist
- final summary

## Writing rules for the page

The page must be user-facing only.
Do not include:
- “this version...”
- process commentary
- defensive caveats
- workshop notes
- tool chatter

Write like a polished guide, not a development log.

## Image rules

Prefer correctness over generic mood shots.

Good order of preference:
1. exact place-matched images
2. source pages with usable `og:image`
3. official tourism / venue pages
4. Wikimedia Commons
5. stable generic mood imagery only when clearly labeled as general atmosphere

If the page names a specific place, do not use obviously unrelated visuals.

When image sourcing is messy:
- use fewer stronger images
- use source-page share images when available
- make gallery cards clickable to the source page
- host assets locally when reliability matters

## Maps and leg links

Include a route summary visual where possible.
Also include leg-by-leg links.

For each leg, ensure:
- the origin is correct
- the destination is correct
- the travel mode matches reality

Examples:
- transit for rail legs
- driving for car legs
- separate links for mixed-mode handoffs

## Confidence gate before page build

Do not build or deploy the Cloudflare Pages site too early.
Only move into page creation once the itinerary is stable enough that major structural changes are unlikely.

Minimum confidence before page build:
- route order is agreed or strongly recommended and accepted
- number of bases is settled
- core transport logic is settled
- major activity choices are reasonably locked
- hotel shortlist is directionally right
- the user is no longer still deciding the basic shape of the trip

If confidence is still low:
- stay in planning mode
- keep refining route, pacing, and activities
- summarise open decisions clearly
- avoid premature page production that will just cause churn

Once confidence is high enough:
- build the webpage
- treat the page as a packaging/output step, not as the discovery step itself

## Cloudflare Pages deployment

After building the static page:
1. make sure assets are local or stable
2. create the Pages project if needed
3. deploy the static folder
4. return the live deploy URL and stable Pages URL

If Cloudflare auth is missing, ask for the minimum token/account/project info needed.

## Quality bar

A good result should be:
- genuinely useful
- visually coherent
- easy to skim in under 5 minutes
- internally consistent about route and transport
- tailored to the travellers

If tradeoffs exist, prefer:
- correct route logic over pretty simplifications
- exact imagery over generic filler
- traveller fit over attraction maximisation
- group harmony and energy management over trying to “do everything”
