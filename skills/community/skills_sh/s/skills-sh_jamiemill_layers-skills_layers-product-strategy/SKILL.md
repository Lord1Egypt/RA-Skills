---
name: layers-product-strategy
description: Techniques for connecting user opportunities to business outcomes and solution bets, and testing the riskiest assumptions cheaply
---

# /layers-product-strategy

*Assumes `/layers-intro` has been loaded. This skill is a library of techniques, not a script — see "How to use these skills" there.*

Strategy is the first layer of the solution space — where problem-space understanding converts into deliberate decisions about scope and direction. It is about choices: which user needs to serve, and which business outcomes to target.

---

## The decisions this layer makes

- The business outcome this work serves
- Which user opportunities (needs, pains, desires) genuinely connect to that outcome
- What solution bets we're placing on those opportunities
- How to test the riskiest assumptions cheaply
- Which bets to pursue first, and why

If the outcome and the bets are already clear, don't rebuild the tree for its own sake.

---

## Disciplines — what keeps strategy honest

- **The outcome is measurable, meaningful, and bounded.** Not "grow the product" but "increase users who activate in the first 30 days." One outcome per tree.
- **Opportunities are customer needs/pains/desires — anchored to a journey moment.** First-person, problem-space statements ("I don't know which streaming service has this movie"), not job stories and not features. Apply the **flip test**: if you can restate it as a feature, it's a solution in disguise. Keep them specific, not generic. **Group opportunities by journey moment** — the forcing function that exposes vague opportunities and surfaces moments left unaddressed. (Teresa Torres.)
- **Every opportunity connects to the outcome.** If serving it wouldn't move the outcome, it doesn't belong in this tree.
- **Every bet names its riskiest assumption,** and there's more than one bet per opportunity — resist early convergence.
- **Every experiment is the cheapest way to test the core assumption** — days, not months.

---

## Techniques

The Opportunity Solution Tree is the default; the rest serve particular strategic questions.

| Technique | Use it when |
|---|---|
| **Opportunity Solution Tree** (Teresa Torres) | Default. Makes outcome → opportunity → solution → experiment explicit. Good for ongoing discovery. |
| **Solution bets** | For a chosen opportunity: *"We could [solution], which we believe would [serve the opportunity] because [reasoning]."* Generate several; name each one's key assumption. |
| **Experiments** | Cheapest test of a bet's core assumption — prototype, fake door, concierge, a targeted interview, data analysis. |
| **Impact mapping** (Gojko Adzic) | B2B with multiple stakeholders who each must change behaviour. |
| **Jobs portfolio mapping** | Many job stories — decide which to target by frequency, severity, strategic fit. |
| **Now / Next / Later roadmap** | The team needs a shared timeline view of bets. |
| **Kano analysis** | Sort candidate features into hygiene, performance, and delight. |
| **HEART / North Star** (Google / Amplitude) | Choosing the outcome metric. HEART structures the choice; North Star distils to one. |
| **Wardley mapping** | Positioning depends on where capabilities sit on the evolution curve; build/buy/partner. |
| **Bundling / unbundling** (Christensen) | Should this product own more of the workflow, or one job precisely? |
| **NPE Canvas** | Consumer products: Narrative, Primitive, Enablers. |
| **Critical User Journeys** (Google / Reforge) | Which flows to prioritise — the minimal path to core value (high-traffic, high-revenue, or metric-critical). |

When you build the tree as a diagram (`graph TD`): outcome at the top, branching down through opportunities **grouped by journey moment**, then bets, then experiments. Top-to-bottom reads as dependency, not sequence.

---

## Working with the designer

Settle the desired outcome first, pushing for specificity. Then map the opportunities that connect to it (applying the disciplines above), generate bets for the ones worth pursuing, and identify the cheapest experiment for the most promising. Prioritise by opportunity size, assumption risk, effort, and reversibility — start with high size, manageable risk, and a clear experiment path, not necessarily the most ambitious.

Offer the technique that fits the question — an OST to connect things end to end, Kano or jobs-portfolio to choose among many candidates, Wardley or bundling for positioning. Don't run them all.

Capture only the residue: the outcome, the opportunity tree (opportunities grouped by journey moment), the top 2–3 bets with their experiments, deferred bets worth returning to, and the open questions (untested assumptions, ungrounded needs). If the needs underneath were weak or assumed, say plainly that the strategy is a bet on assumptions.

The bets chosen here define what needs designing next — the objects, relationships, and vocabulary those solutions work with: `/layers-conceptual-model`.
