---
name: war-conflict-intel-and-forecast
description: Collect, verify, and forecast war or geopolitical conflict developments using authoritative sources, cross-validation, and scenario-based prediction.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛰️"
---

# War / Geopolitical Conflict Intelligence & Forecast Skill

## Purpose
Turn a request like:

- “Collect the latest battlefield situation”
- “Use authoritative sources”
- “Give a more precise assessment”
- “Predict what the U.S., Iran, Israel, or other actors may do next”
- “Estimate likely end-state trajectories”

into a stable workflow that is:
- fact-first
- source-ranked
- cross-verified
- explicit about uncertainty
- disciplined in prediction

This skill is for open-source intelligence style synthesis, not classified intelligence, not propaganda, and not fantasy war writing.

---

## Core Rules

### 1) Separate facts from judgments
Every answer must be split into:
- Confirmed facts
- Assessment / inference
- Forecast

Never present a forecast as if it were already confirmed reality.

### 2) War information is adversarial by default
In war, every side has incentives to:
- exaggerate success
- hide losses
- shape public opinion
- pressure allies and markets
- trigger psychological effects

Therefore:
- a single belligerent’s statement is not enough
- strong claims require stronger verification
- “destroyed”, “eliminated”, “full control”, “crippled”, “collapsed” should be treated as claims to verify, not instant facts

### 3) Use concrete dates and time windows
Do not write:
- today
- recently
- just now

Write:
- exact date
- if needed, exact time and timezone
- explicit forecast window such as next 24 hours / next 3–7 days / next 2–6 weeks

### 4) Precision beats confidence theater
Do not sound certain when evidence is thin.
Prefer:
- high probability
- medium probability
- low probability / high impact
- too early to confirm
- single-source claim
- preliminary signal

### 5) Every forecast needs a trigger and a disconfirming signal
For each prediction, state:
- what evidence supports it
- what new evidence would strengthen it
- what evidence would weaken or overturn it

---

## What to Collect Every Time

For any armed conflict or fast-moving geopolitical crisis, collect at least these five buckets:

### A. Battlefield / operational developments
- strikes, missile launches, drone attacks, naval incidents
- target sets
- claimed damage
- defensive interceptions
- territorial / airspace / maritime control changes
- underground or hardened facility status if relevant

### B. Military capability changes
- air defense degradation
- missile inventory depletion
- logistics and fuel strain
- command-and-control damage
- reserve mobilization
- naval disruption capability
- survivability of leadership and strategic assets

### C. Political and diplomatic signaling
- head of state statements
- defense ministry / military spokesperson statements
- legislative action
- alliance commitments
- mediation or ceasefire signals
- red lines and ultimata

### D. Regional and global spillover
- shipping and chokepoints
- oil and gas markets
- refugee / humanitarian indicators
- proxy fronts
- neighboring states’ alert status
- UN / IAEA / international organization warnings

### E. Forward indicators
- what would signal escalation
- what would signal negotiated de-escalation
- what would signal a shift in probable end-state

---

## Source Hierarchy

Build the answer from the top of this hierarchy downward.

## Tier 1: Core authoritative backbone
Use these first to build the main factual structure.

### Reuters
Use for:
- fast and relatively restrained reporting
- official statements
- battlefield + diplomacy + market linkage
- shipping, oil, energy, sanctions, legislative context

### AP
Use for:
- live war updates
- casualties and immediate developments
- domestic political reaction
- field-level narrative updates

### Official primary sources
Use to confirm what an actor said, not automatically whether the claim is true:
- White House
- U.S. Department of Defense / State Department
- Israeli PM office / defense ministry / IDF
- Iranian foreign ministry / military / official state outlets
- UN, IAEA, UNHCR, ICRC, etc.

### Hard-data and system indicators
Use where available:
- shipping traffic data
- oil price reactions
- public market data
- satellite imagery reporting
- port advisories
- aviation / maritime notices

---

## Tier 2: Strong supporting sources
Use to add depth, background, or insider context.

### Financial Times / BBC / Wall Street Journal / New York Times
Use for:
- deeper diplomatic context
- insider sourcing
- strategic framing
- policy debates

Rule:
- anonymous sourcing should ideally be checked against another reliable source

### Al Jazeera and major regional outlets
Use for:
- regional framing
- Arab-world reactions
- local political atmosphere

Rule:
- do not rely on these alone for decisive battlefield claims

---

## Tier 3: Cautious-use sources
### Social media, Telegram, X, viral video
Use only for:
- early leads
- geolocation clues
- timeline hints

Never treat them as settled fact until checked.

If using them, verify:
- date
- location
- whether footage is old
- whether credible journalists or organizations have corroborated it

### Analysts / think tanks / military commentators
Use for:
- force structure
- campaign logic
- weapons context
- scenario analysis

Do not let commentary substitute for hard confirmation.

---

## Mandatory Verification Labels

For every major claim, implicitly or explicitly classify it as one of these:

- Confirmed  
  at least two reliable sources or one reliable source plus strong corroborating data

- Single-party claim  
  one side says it; independent confirmation is missing

- High-confidence inference  
  not formally confirmed, but several indicators point the same way

- Unverified / preliminary  
  not safe to treat as established

Examples:
- “State X says it destroyed underground missile infrastructure” → single-party claim unless independently supported
- “Tanker traffic through a chokepoint collapsed” → confirmed if supported by Reuters plus traffic data
- “Leadership is considering a ceasefire” → high-confidence inference or unverified unless solidly corroborated

---

## Standard Workflow

## Step 1: Establish the situation frame
Before details, answer:
1. What phase is the conflict in?
2. What are the most important events in the last 48 hours?
3. Is the conflict escalating, stabilizing, or fragmenting?
4. Are there any real negotiation signals?
5. What spillover risks are already visible?

Build this first with Reuters + AP + official primary sources.

---

## Step 2: Build a dated timeline
List at least 5–10 major events with:
- exact date
- what happened
- why it matters
- source confidence level

Format:
- 2026-03-05 — Israel signals a “second phase” focused on underground missile facilities.  
  Why it matters: target set shifts from visible assets to survivable strategic capacity.  
  Status: reported by Reuters.

---

## Step 3: Disaggregate actor goals
Always separate what each actor wants.

### U.S. usually cares about
- degrading opponent military capability
- protecting forces and allies
- maintaining deterrence credibility
- avoiding politically costly quagmire
- limiting oil-price and market damage
- preserving coalition support

### Israel usually cares about
- maximizing long-term reduction of hostile capability
- degrading missile, nuclear, proxy, and command networks
- converting battlefield opportunity into strategic depth

### Iran or similar regional state actors often care about
- regime survival
- preserving retaliatory capacity
- raising cost on adversaries
- using missiles, drones, proxies, and chokepoints asymmetrically
- turning a military disadvantage into a political/economic endurance contest

Do not merge these into one “allied side” goal.

---

## Step 4: Identify constraints
Prediction quality depends on knowing not just intent, but limits.

Check:
- munitions stockpiles
- air superiority status
- survivability of underground assets
- shipping chokepoint control
- domestic political support
- legislative constraints
- coalition cohesion
- proxy readiness
- economic pressure
- humanitarian blowback

---

## Step 5: Forecast by time horizon
Never give one undifferentiated prediction blob.

### Horizon A: next 24 hours
Look for:
- immediate retaliatory patterns
- strike tempo
- naval incidents
- emergency diplomacy
- casualty shocks that change behavior fast

### Horizon B: next 3–7 days
Look for:
- campaign phase shifts
- strikes on harder strategic targets
- proxy front activation
- widening to nearby states
- backchannel mediation

### Horizon C: next 2–6 weeks
Look for:
- sustained limited war
- negotiated freeze
- regionalization
- internal instability
- strategic exhaustion

---

## Forecast Template

For each forecast, use this structure:

### Conclusion
Example:
- “Over the next 3–7 days, the U.S. and Israel are likely to intensify strikes on hardened and underground missile infrastructure.”

### Why this is plausible
List the supporting signals:
- public rhetoric remains escalatory
- evidence of air-access advantage
- campaign messaging indicates a second phase
- strategic logic favors reducing residual retaliatory capability

### Constraints
List what could slow or limit this:
- munitions expenditure
- oil price pressure
- domestic political pushback
- escalation risk to shipping or bases
- allied caution

### Confirming signals to watch
- more reporting on bunker-busting or underground target sets
- repeated strikes on command-and-control nodes
- expanded evacuation notices
- intensified maritime protection operations

### Disconfirming signals
- public move toward talks
- partial restoration of commercial shipping under de-escalation arrangements
- legislative effort constraining operations
- credible third-party mediation producing reciprocal restraint

---

## End-State Forecasting

Do not write one cinematic ending.
Use scenario trees.

### Scenario 1: Limited-war advantage followed by ceasefire or frozen conflict
Typical signs:
- one side achieves clear conventional military superiority
- the other side is badly degraded but not collapsed
- international pressure builds
- both sides redefine victory politically

### Scenario 2: Protracted regionalized conflict
Typical signs:
- multiple proxy fronts remain active
- shipping and energy disruption persist
- strikes continue episodically
- no side can impose a decisive settlement

### Scenario 3: Internal regime or command-structure fracture
Typical signs:
- decapitation or severe leadership disruption
- fragmented control
- growing elite splits
- security apparatus inconsistency
- rising uncertainty over strategic asset control

For each scenario:
- assign rough probability
- state why
- state what would move probability up or down

---

## Variables That Most Often Change the Outlook

### Military variables
- who owns the airspace
- survivability of underground facilities
- remaining missile inventory
- maritime interdiction capability
- resilience of command networks

### Political variables
- leadership rhetoric shifts
- legislative constraints
- coalition discipline
- tolerance for casualties and economic pain

### Economic variables
- oil price trajectory
- insurance and shipping disruption
- domestic consumer price impact
- sanctions tightening or leakage

### Diplomatic variables
- whether mediators are active
- whether allies begin pressing for de-escalation
- whether international watchdogs issue sharper warnings
- whether a face-saving negotiation channel appears

---

## Output Structure

Use this order:

# 1. One-sentence bottom line
Example:
- “The conflict has moved into a deeper, more dangerous phase, and the near-term outlook favors continued escalation before any serious public ceasefire opening.”

# 2. Confirmed facts
Group into:
- recent battlefield developments
- political signaling
- regional/economic spillover

# 3. Assessment
Explain:
- what phase the conflict is in
- which side currently has initiative
- what each side is trying to achieve
- what the key constraints are

# 4. Forecast
Split by:
- next 24 hours
- next 3–7 days
- next 2–6 weeks

Within each, separate:
- high probability
- medium probability
- low probability / high impact

# 5. End-state scenarios
At least three:
- most likely
- plausible alternative
- lower-probability but high-risk

# 6. Watchlist
Give 3–7 indicators that would change the assessment fastest.

---

## Common Failure Modes

### Failure 1: repeating propaganda as fact
Fix:
- attribute clearly
- verify independently
- downgrade confidence where needed

### Failure 2: focusing only on kinetic events
Fix:
- always include oil, shipping, politics, diplomacy, and humanitarian spillover

### Failure 3: prediction without time horizon
Fix:
- always separate near-term, short-term, and multi-week outlook

### Failure 4: overconfidence
Fix:
- use probability bands
- include disconfirming evidence
- show what would change your mind

### Failure 5: actor-blending
Fix:
- separate U.S., Israel, Iran, proxies, Gulf states, and other actors where relevant

---

## Final Discipline Checklist

Before delivering, verify:

- [ ] Facts and forecasts are clearly separated
- [ ] Dates are concrete
- [ ] Reuters / AP / primary sources form the backbone
- [ ] Major claims are cross-checked
- [ ] Single-party claims are labeled as such
- [ ] Military, political, economic, and diplomatic dimensions are covered
- [ ] Forecasts are time-boxed
- [ ] End-state analysis uses scenarios, not one rigid ending
- [ ] There is a watchlist of indicators that could change the view
- [ ] Language is disciplined, not theatrical

---

## One-line operating principle
Be slower than propaganda, but more accurate than hype.
