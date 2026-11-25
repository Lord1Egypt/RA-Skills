---
name: routepilot-cn
display_name: RoutePilot 行程智算
display_name_en: RoutePilot — Route & Trip Cost Intelligence
description: >-
  给自驾出行者的路线算账技能：把多条路线的油费、过路费、时间成本与疲劳成本算成同一口径的总成本，给出唯一推荐，并把节假日免费窗口与多日行程预算一起排出来。
description_en: >-
  Route and trip cost intelligence for self-drive travel. It turns origin, destination, vehicle fuel economy and party size into one comparable total cost per route — fuel, tolls, time value and fatigue — then returns a recommendation, a holiday free-toll schedule and a multi-day budget.
version: 1.0.0
category: life-service
sub_categories:
  - key: pro-travel
    name: 出行规划
tags: [路线比价, 过路费核算, 油耗计算, 自驾行程, 节假日出行, 行程预算]
tags_en: [route-comparison, toll-cost, fuel-economy, road-trip, holiday-travel, trip-budget]
icon: 🧭
platforms: [WorkBuddy, QClaw, ima, Claude Code, Codex]
trigger_keywords: [哪条路线更划算, 走高速还是走国道, 过路费值不值, 油费怎么算, 节假日高速免费, 多日自驾行程, 行程预算表, 路线对比, 自驾总成本, 时间成本怎么算]
author: DeepCraft Studio
license: Commercial
pay_skill: true
price_cny: "1.99"
---

# RoutePilot — Route & Trip Cost Intelligence

Turn "which road is actually cheaper" into an auditable number: compare every candidate route on one total-cost basis covering fuel, tolls, time value and fatigue, then issue a single recommendation together with the holiday free-toll schedule and a multi-day budget.

## What This Is

- It fixes a comparison gap. Navigation apps report duration and tolls but never answer "what are those extra 34 minutes worth, and what do the extra 15 kilometres cost". This skill converts both into money and adds them into one sortable total.
- Every run delivers four artefacts: a decision card (recommendation, reason, rule ID), a cost table (five cost lines plus total), a free-toll schedule (when the travel date falls inside a free-toll holiday), and a multi-day itinerary with a line-item budget (when the trip exceeds one day).
- It differs from asking a general model in three ways. Every figure is reproducible, carrying its formula, parameter and unit. The thresholds form a system: the min/km rule family R1-R8 handles fast verdicts, cross-checks and arbitration. And no number is invented: fuel price, toll rate and free-toll policy are always labelled "verify against the actual value on the travel day" together with a verification method.
- It suits drivers who would rather spend two minutes on arithmetic than pick a road by feel, and anyone who must hand a family itinerary to someone else and needs a budget sheet that survives the handover.
- One-line principle: **compute the total cost first, then explain it with thresholds**. The rule family is a fast path and a fallback, not a shortcut around the arithmetic.

## When to Use It

1. I am choosing between routes: the expressway is fast but tolled, the national road is free but has many lights. Which one wins?
2. I am travelling over Spring Festival, Qingming, Labour Day or National Day and want the free window on the long legs. Which segment should be free and which should be paid?
3. I am driving three days with elderly parents and a child. How long can we drive each day, where do we sleep, and what is the total budget?
4. I must arrive before a fixed time and I am willing to pay for speed. How much is reasonable, and when should I change the plan instead?
5. Navigation says route A is five minutes faster but has 12 more traffic lights. Is that "faster" even real?
6. I want to compare driving, high-speed rail and flying door to door, not on in-vehicle hours.
7. I want to review the last trip: where exactly did the tolls go, and was any mileage wasted on a detour?

## When NOT to Use

- Live traffic, live tickets, or road closures: this skill compares plans from supplied parameters.
- Cross-border driving or plate-restriction rules: flag for official verification.
- Trips where time cannot be priced (e.g. patient transport): list trade-offs, no single recommendation.
- Requests for a guaranteed fastest route: provide probability and buffers instead.

## Quick Reference

| Situation | Use |
|---|---|
| Total cost, fuel, value of time | `references/cost-model.md` + `scripts/route_cost.py` |
| Two plans, different trade-offs | `references/route-decision.md` |
| Holiday free-toll windows | `references/holiday-window.md` |
| Itinerary for companions | `references/itinerary-template.md` |

## Inputs and Outputs

| Field | Required | Notes |
|:--|:--|:--|
| Origin and destination | Yes | City or landmark; list the provinces crossed so the toll rate can be resolved |
| Travel date and time window | Yes | Decides whether the trip falls inside a free-toll window and whether night driving applies |
| Candidate routes | Yes (2 or more) | Distance (km), duration (min), toll (CNY) and traffic-light count per route; mark missing items "not provided" instead of estimating |
| Vehicle and fuel economy | Yes | Displacement or vehicle class plus combined consumption (L/100km). Example: mid-size sedan (1.8T, 7.5L/100km) |
| Party composition | Yes | Adults, children, seniors, and whether anyone has a hard deadline |
| Time value per person | Yes | CNY per hour; convert from net hourly pay with a 0.6-0.8 factor and state the basis |
| Fuel price that day | Yes | Pump price for the grade you will buy (CNY per litre) |
| Toll rate and free-toll policy | Yes | Class-1 passenger-car rate per province, whether the day is free, ETC discount |
| Hard deadline | Yes | An arrival time, or "none" |
| Parking and transfer costs | No | Required only for door-to-door comparison |
| Preferences | No | Avoid expressways, fewer lights, child rest frequency, no night driving |

`scripts/route_cost.py --json input.json` accepts the same fields as a `params` object plus a `routes` array; the schema is in `SKILL.md`.

**Outputs** (Markdown, body of 1200 words or fewer plus 2-4 tables):

- Decision card (200 words or fewer): recommendation, one-line reason, rule IDs.
- Cost table: one row per route with fuel, toll, time cost, fatigue, risk premium, total, and the gap to the best option.
- Ratio line: rhythm (min/km), delta-T over delta-S, and net cost per minute divided by the effective time value.
- Free-toll schedule when applicable: recommended entry and exit times, plus the boundary contingency.
- Multi-day itinerary when longer than one day: daily distance, driving time, anchor, overnight stop, plus a budget with 8-10 percent contingency, total and per-person figures, and three to six risks each with a trigger and an action.

Every delivery uses the same decision-card shape so results stay comparable: recommendation with the total and the gap, reason with rule ID and three ratios, trade-off with the parameter range that reverses the verdict, and concrete actions.

When driving is compared with rail and air, use the door-to-door basis for all three and count every leg, including station or airport access, waiting time and the final transfer.

## Workflow

1. **Collect inputs and set defaults**
   - Do: gather every field above in one pass and list the gaps together; for each gap, state the conservative default and which way it biases the verdict.
   - Criterion: all nine required fields present. Up to two gaps with defaults is workable if flagged.
   - If it fails: with three or more gaps, produce only an order-of-magnitude estimate (plus or minus 15 percent) plus a gap list, then rerun once the user fills them in.
2. **Enumerate routes and extract features**
   - Do: record seven features per route - distance D (km), duration T (min), toll, light count L, light density L/D, congestion variance sigma (half the spread between slowest and fastest duration), and free-flow duration.
   - Criterion: two or more routes with all seven features. If sigma is missing, estimate it as 0.12 times T and mark it "estimated".
   - If it fails: with a single route, switch to a cost-review mode that reports total cost and optimisation options only. With identical distances, skip the delta ratio and decide with R6 plus R5.
3. **Calibrate the three price inputs**
   - Do: write down the value, source and verification date for fuel price, toll and free-toll policy.
   - Criterion: all three traceable to a same-day pump price or the current year's official notice.
   - If it fails: run a low-high range twice, present the answer as a range labelled "to be verified", and state the verification action.

   | Input | How to obtain | How to verify |
   |:--|:--|:--|
   | Fuel price | Pump price on the travel day for the grade you will buy | Check the station board the evening before, or the current fuel-price adjustment notice |
   | Toll | Navigation quote, or province rate times billed distance | Compare with a past ETC statement on a similar segment; add bridge and tunnel surcharges separately |
   | Free-toll policy | Current-year notices from the transport ministry and provincial transport authorities | Confirm the vehicle class, the window, and that the exit-lane timestamp governs |
4. **Build the cost model**
   - Do: compute the five cost lines below and add them on one basis. Let the script or a spreadsheet do the arithmetic, never mental math.
   - Criterion: every route reproducible to within 2 percent. Any single stint over four hours must include a 20-minute rest inside T first.
   - If it fails: when parameters contradict each other (average speed below 15km/h priced as expressway, a toll above rate times distance), return to step 2 and fix the raw data instead of fudging the model.

   ```text
   fuel      = D / 100 * consumption(L/100km) * price(CNY/L)
   toll      = 0 inside a free-toll window, otherwise the quoted toll
   V         = time value(CNY/h) / 60 * weight sum        unit: CNY/min
   time cost = T * V
   fatigue   = max(0, T - 120min) * V * 0.3 * context factor
   risk      = z * sigma * V        (z defaults to 0.5, about the 70th percentile)
   total     = fuel + toll + time cost + fatigue + risk
   ```

   Passenger weights are examples to replace with real ones: driver 1.0, adult passenger 0.6, child 0.3, retired senior 0.1, time-pressed business companion 1.5-2.0. The weight sum is not a head count; counting heads forces every verdict toward the expressway. Context factor: 1.5 at night (22:00-06:00), in rain or fog, or on continuous mountain roads; 1.0 otherwise.
5. **Apply the threshold rules**
   - Do: rank by total cost (R6), cross-check with R1-R5, then commit to a verdict in arbitration order and state the reasoning.
   - Criterion: the verdict cites rule IDs and reports three ratios - rhythm, delta-T over delta-S, and net cost per minute divided by V.
   - If it fails: a gap under 3 percent is a tie; when the rule family and the total disagree, the total wins and the conflict must be written up, usually because the effective time value exceeds the one the thresholds imply.

   | ID | Rule | Test | Verdict when triggered |
   |:--|:--|:--|:--|
   | R1 | Zone shift | Short route rhythm above 2.4 and fast route below 1.5 | Take the fast route; escaping the idle trap dominates |
   | R2 | Fuel signal lost | Rhythm difference below 0.15 | Ignore fuel, compare traffic lights and turns |
   | R3 | Delta ratio break-even | 4.5 without a toll difference, 7.5 with one, 4.5 inside a free window | Above the line take the fast route, below it the short one |
   | R4 | Cost-per-minute ratio | Net cost per minute divided by V | Below 0.5 buy time; 0.5-1.0 lean to buying; 1.0-1.5 only if in a hurry; above 1.5 take the short route |
   | R5 | Traffic-light override | Delta-T under 8 minutes and light difference times 0.5 minutes exceeds delta-T | The time advantage is noise; take fewer lights |
   | R6 | Total-cost ranking | Gap to the best option of 3 percent or more | Lower total wins; under 3 percent is a tie |
   | R7 | Hard deadline | Deadline minus duration minus sigma is negative | Route eliminated; if all are eliminated, change the plan |
   | R8 | Detour ceiling | Detour over 35 percent in the city, over 40 percent with expressway | Fast route rejected unless R7 forces it |

   Arbitration runs in this order, each level overriding the next: R7 and access restrictions, then R8, then R6, then R1 followed by R3 and R5, with R2 and R4 as the fallback path when inputs are thin.
6. **Optimise the free-toll window**
   - Do: push the longest uncongested inter-provincial leg into the free window, move the most congested return leg to a paid working day after the window, and give the boundary contingency.
   - Criterion: free status is judged by the timestamp of leaving the exit lane; toll is zero inside the window, so the delta ratio reverts from 7.5 to 4.5 and the same destination deserves the fastest route.
   - If it fails: when the exit timestamp is uncertain, price it as paid. If the car is still on the expressway two hours before the window closes, leave at the nearest exit and re-enter so the long segment splits into two billed segments.
7. **Build the itinerary and budget**
   - Do: split the trip against daily ceilings, produce the day-by-day table, use backward scheduling for fixed-time tickets, pick lodging by next-day departure direction, and add a contingency line.
   - Criterion: no day exceeds either ceiling (adjust the defaults for fitness and terrain, but satisfy both), budget total equals the sum of line items, contingency is 8-10 percent.
   - If it fails: split a day or add a night and price the increment (one night plus one day of meals) for the user to decide; never quietly drop the anchor.

   | Party | Daily driving | Daily distance | Extra requirement |
   |:--|:--|:--|:--|
   | Solo driver | 4 hours max (legal limit), 3.5 recommended | 350km or less | A rest of 20 minutes or more every 4 hours |
   | Two or more drivers | 7 hours or less | 600km or less | Swap every 2-3 hours |
   | With children or seniors | 5 hours or less | 400km or less | Each stint 2 hours or less, one rest stop or sight |
   | Night 22:00-06:00 | 2 hours or less | 150km or less | Avoid if possible; never counts as a long leg |

## Output Format

```
Comparison: plan | km | duration | tolls | fuel | total cost | risk
Recommendation: primary plan + switch trigger
Time window: departure window, free-toll boundaries
Risks: works, restrictions, service-area gaps, fatigue points
```

## Quality Gate

- [ ] All nine required inputs recorded, or flagged "to be confirmed" with the default source named.
- [ ] Seven features per candidate route, with gaps marked "not provided"; no invented distances or durations.
- [ ] Five cost lines plus total for every route, reproducible from the stated formulas to within 2 percent.
- [ ] Verdict cites R1-R8 IDs and reports rhythm, delta-T over delta-S, and net cost per minute, with the effective time value (time value divided by 60 times the weight sum) shown alongside.
- [ ] Fuel price, toll rate and free-toll policy each labelled "verify on the travel day" with a verification method; free-toll judgement states the exit-lane timestamp basis and carries a boundary contingency.
- [ ] Gaps under 3 percent are reported as a tie with a secondary tie-breaker; no winner is invented.
- [ ] Every day satisfies both ceilings; overruns were split and priced.
- [ ] Budget carries an 8-10 percent contingency with total and per-person figures; three to six actionable risks.

## Limits

- No live traffic, fare or fuel-price feeds. Distances and durations come from the navigation snapshot the caller supplies; live data must be supplied too. This skill models and adjudicates.
- No promises of "guaranteed congestion-free" or "guaranteed X percent cheaper". It returns reproducible costs, thresholds and sensitivity bands, and the verdict moves when the inputs move.
- Out of scope: freight, coaches, ferries, cross-border tolls and EV charging networks, each needing its own cost model; and when time value cannot be quantified (pure leisure, no deadline) it returns a per-kilometre and per-hour view instead of forcing a verdict.
- Driving restrictions, permits, parking height limits and child-seat rules follow local rules in force; they enter the analysis only after the user confirms them.
- Routing engines usually understate distance. Apply a 5-10 percent margin and never treat one engine's figure as ground truth.

## Common Traps

- **Taking map ETAs as reality**: add 5-10% plus a break every two hours.
- **Missing bridge and tunnel surcharges**: price segment by segment.
- **Free-toll boundary confusion**: billing depends on the exit time, not entry.
- **Comparing distance instead of cost**: decide on total cost, not one metric.

## Example Delivery

Input (three lines):

- City A to City B, Saturday 08:00 departure, two adults and one child, no deadline.
- Candidates: A expressway 118km, 78min, toll CNY 46, 12 lights; B national road 103km, 112min, no toll, 31 lights.
- Example vehicle: mid-size sedan (1.8T, 7.5L/100km), fuel CNY 7.60/L that day, time value CNY 60 per hour.

Output skeleton (figures are illustrative; recalculate with same-day parameters):

```text
[Recommendation] Route A, total CNY 268.11, CNY 13.38 (5.0%) cheaper than route B.
[Reason] R6 ranking, supported by the R4 band; rhythm A 0.66, B 1.09 min/km.

| Route | Fuel | Toll | Time cost | Fatigue | Risk premium | Total |
| A expressway | 67.26 | 46.00 | 148.20 | 0.00 | 6.65 | 268.11 |
| B national road | 58.71 | 0.00 | 212.80 | 0.00 | 9.97 | 281.49 |

Ratio: delta-T over delta-S = 34 / 15 = 2.27 min/km against the tolled threshold of 7.5.
Net cost per minute (fuel gap 8.55 plus toll gap 46.00) / 34 = CNY 1.60/min, divided by the
effective time value of CNY 1.90/min gives 0.84, a lean toward buying time.
Cross-check: the fuel dimension points to the national road because that threshold implies a
time value near CNY 0.60/min while this case runs three times higher; the total wins and the
conflict is stated so the verdict does not look self-contradictory.
Window: not a free-toll holiday, so tolls are charged as quoted. Risks: route B's 31 lights
give sigma around 10.5 minutes, so the worst case can reverse; the fuel price is a same-day
quote and must be refreshed.
```

## Related Skills

- **TableScribe (paid)**: tabulate candidate plans before comparing.
- **PriceLens (paid)**: pair with en-route purchasing comparisons.

## Reference Files

- `references/cost-model.md` - five cost formulas and parameters, effective time value, physical derivation of the 4.5 and 7.5 min/km thresholds, sensitivity analysis.
- `references/route-decision.md` - the R1-R8 rule family, arbitration order, six scenario cards with their failure conditions.
- `references/holiday-window.md` - how free-toll status is judged, boundary contingencies, the threshold switch inside a window, scheduling template and checklist.
- `references/itinerary-template.md` - multi-day template, daily ceilings, backward scheduling for fixed-time tickets, budget structure and risk list.
- `scripts/route_cost.py` - standard-library cost calculator; feed it routes and parameters to get the cost table and rule cross-check.
