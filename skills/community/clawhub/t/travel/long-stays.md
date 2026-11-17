# Long Stays — A Month Or More In One Place

Past roughly four weeks, travel stops being a trip and starts having consequences: day counts with legal weight, a lease instead of a booking, healthcare instead of insurance, and an address. Moving somewhere permanently is a different job — `expat`.

**Contents:** [The Thresholds That Change The Rules](#the-thresholds-that-change-the-rules) · [Counting Days Properly](#counting-days-properly) · [Visa Runs And Why They Fail](#visa-runs-and-why-they-fail) · [Working While Travelling](#working-while-travelling) · [Accommodation Past A Month](#accommodation-past-a-month) · [Connectivity](#connectivity) · [Money For A Long Stay](#money-for-a-long-stay) · [Health Cover Past The Policy](#health-cover-past-the-policy) · [Home, Mail, And Continuity](#home-mail-and-continuity) · [The Pace Problem](#the-pace-problem)

**Before planning anything past four weeks**, read `## Presence` in `~/Clawic/data/travel/memory.md` — or `presence/<year>.md` if `## Boxes` points there — and `## Documents`. Every question in this file is answered by the day count first.

## The Thresholds That Change The Rules

Different thresholds, different authorities, and they do not line up:

| Around | What changes | Whose rule |
|---|---|---|
| 30-90 days | Visa-free allowance runs out; a rolling window like Schengen's 90/180 binds | Immigration |
| 90 days | Many countries require a residence registration for stays past this point, even for citizens of visa-free countries | Immigration / local registry |
| ~183 days | A common — but far from universal — tax-residence trigger. Some jurisdictions use multi-factor tests instead of a day count, and some count a rolling or averaged period | Tax authority |
| Any day, in some countries | Working while physically present can create a tax or permit obligation independently of the day count | Tax authority / labour law |
| Typically 30-90 days | Standard travel insurance stops covering a single trip past its per-trip limit | Insurer |
| Varies | Home-country health cover lapses after a period of absence | Home health system |

Two rules for handling this responsibly: record the days in `## Presence` in `memory.md` (or `presence/<year>.md` once split) and state what they add up to, and route the conclusion — tax residence, work rights, benefit entitlement — to a professional in the relevant jurisdiction. The day count is a fact worth keeping; the legal conclusion is not this skill's to draw.

## Counting Days Properly

- Entry day and exit day each count as **full days** in most rules, including Schengen's.
- A rolling window is counted **backwards from the date in question**, never per calendar year (`documents.md`).
- Days spent on somebody else's trip, on a work trip, and on a layover where immigration was cleared all count.
- The record is the row, kept as it happens: `In | Out | Country/area | Days | Purpose | Counts toward`. Reconstructing two years of crossings from old boarding passes is a weekend nobody enjoys.
- Keep the physical evidence trail — boarding passes, stamps, entry records — for as long as the longest applicable rule looks back, because the burden of proof is on the traveller.

## Visa Runs And Why They Fail

Leaving briefly and re-entering to reset an allowance works where the allowance is per-entry, and does not work where it is rolling — a Schengen exit and re-entry resets nothing, because the previous 180 days come with you. Even where it is technically per-entry, repeated short exits are the pattern border officers are trained to spot, and refusal is discretionary and effectively unappealable at the border.

Where a long stay is actually wanted, the correct instrument is a long-stay visa, a digital-nomad or remote-work visa where the country offers one, or a student or working-holiday route. These take weeks to months and are applied for from outside the country in most cases. Record the procedure that worked as `artifacts/visa-<country>.md`.

## Working While Travelling

- **Tourist status usually excludes work**, and the definition of work varies: remote employment for a foreign employer sits in a grey zone in many countries and is explicitly prohibited in some. Digital-nomad visas exist precisely because the grey zone is a problem.
- **The employer has exposure too**: an employee working from another country can create a permanent-establishment or payroll obligation there. Anyone doing this for more than a few weeks should have told their employer.
- **Time zones**: a stay that puts the working day at 02:00 is unsustainable regardless of the visa. Check the overlap with the people who need synchronous time before choosing the country, not after.
- **Infrastructure**: a specific, tested upload speed, a backup connection, and a place to work that is not a bed. A café is not a working setup for a month.
- Business trips are a different set of rules — company policy, per diem, expense evidence — in `business-trips.md`.

## Accommodation Past A Month

Monthly rates are typically far below thirty nightly rates on the same platform, and negotiating direct usually beats both. What to verify before committing to a month somewhere sight-unseen:

- **Which floor, which direction, what is outside the window** — noise is the thing that ends long stays early
- **Bills included or metered**, and heating or cooling costs in the actual season
- **Laundry, kitchen, and a work surface**, all of which stop being optional past two weeks
- **Cancellation terms for a long booking**, which are usually far stricter than a nightly rate's
- **Registration**: some countries require the host to register a foreign guest, or the guest to register at a local office within days of arrival, and failing to do so is a fine at exit

Prefer a short first booking followed by a longer one chosen in person. A week in the wrong apartment is a lesson; a month is a ruined stay.

## Connectivity

Buy and install an eSIM **before departure**, while there is Wi-Fi — activation typically requires a connection, which is exactly what is missing on arrival. For a stay past a month, a local physical SIM or a local plan is usually cheaper and comes with a local number, which many local services require. Check whether the country requires identity registration for a SIM, because that turns a five-minute purchase into a passport-and-address errand.

## Money For A Long Stay

A long stay is a cost-of-living problem, not a travel-budget problem: rent, groceries, local transport and a gym replace hotels and restaurants, and the per-day rate falls sharply after the first fortnight. Record the long-stay rate as its own row in `## Spend Baselines`, marked as such, because mixing it with a two-week holiday rate for the same city makes both numbers useless (`money.md`).

Watch for: a card issuer flagging sustained foreign use, an account requiring a home-country address, and the cost of moving money — a local account may be required for rent and may be impossible to open on a tourist status.

## Health Cover Past The Policy

Standard travel insurance has a per-trip maximum, commonly 30-90 days, and the trip clock does not reset by crossing a border. Past that limit the instruments are an annual multi-trip policy with a long per-trip allowance, an international health insurance policy, or local cover. Check whether home-country public cover lapses after an absence, and what reinstating it requires (`health.md`).

## Home, Mail, And Continuity

Mail redirected or handled by someone with a key; subscriptions and deliveries paused; anything requiring a physical signature or an in-person renewal identified before leaving; the home insurance's unoccupied-property clause read, because most policies limit cover after a stated number of consecutive unoccupied days. The person holding the key goes in `~/Clawic/data/contacts/contacts.md`; the alarm code goes nowhere (`safety.md`).

## The Pace Problem

The failure mode of a long stay is treating it as a long holiday: sightseeing every day for a month exhausts people and ends the stay early. What works is a **weekly rhythm** — a routine on most days, one exploring day, one genuine rest day — and accepting that a month somewhere means seeing less per day and more in total. Say this out loud when planning it, because the itinerary people write for a month is the one they wrote for a week, repeated four times.

**After any stay past four weeks**, write in the same turn: every crossing into `## Presence` (or `presence/<year>.md`), the long-stay per-day rate into `## Spend Baselines` marked long-stay, any registration or visa procedure into `artifacts/visa-<country>.md`, the apartment and neighbourhood findings into `artifacts/place-<name>.md`, each with its `## Boxes` line. Split rule and formats: `memory-template.md`.
