# Research budget

Read this before launching any research fan-out — a Workflow call, parallel Agent calls, or
`codex exec` children. It governs how much you buy, in what order, and when you stop.

## Why this file exists

A measured Construction run (Qiqihar→Tokyo, 2026-08-04) spent **~1.8M subagent tokens, 1000+ tool
calls, and its entire 200-call web-search budget** on a five-day trip — roughly three times what
the deliverable needed. The output was good. The spend was not, and two of the causes also
*created defects*:

- An entire visa-procedure branch (~100KB: consular jurisdiction, designated-agency rules, fee
  schedules, processing times) was voided by the traveller's next sentence, "我有签证".
- Anchor and opening-hours research ran before the date window was locked. When the dates moved
  by one day, every weekday-keyed fact had to be re-mapped by hand — and that manual re-mapping
  is what introduced an off-by-one in every `day_number` and `planned_day`, which the verify pass
  then had to catch. Researching too early did not just cost tokens; it manufactured a
  trip-breaking bug.

So the rule is not "research less". It is **research in an order where nothing you buy can be
invalidated by an answer you have not asked for yet.**

## 1. Ask the disqualifiers before you spend anything

Before the first agent is launched, ask up to three questions whose answers can delete whole
research branches. They are cheap, they are fast, and they are the highest-return act in the
whole pipeline:

| Question | What a "yes" deletes |
| --- | --- |
| Do you already hold the visa / entry permission for where you want to go? | The entire entry-research branch. Verify the held document instead. |
| Are the dates genuinely immovable, or "prefer not to move"? | Prevents anchor/hours research from being re-keyed to a different weekday later. |
| Have you already booked any flight, hotel, or ticket? | Removes those categories from pricing and comparison work. |

The intake form now asks the first one directly (`trip_geography.scope` is a yes/no on whether a
new visa is needed). Ask the other two in chat if the form did not settle them.

## 2. Three phases, three separate invocations, one checkpoint

Do **not** put feasibility, design, and adversarial challenge in one fan-out.

1. **Feasibility** — only the things that can kill the trip: entry, can they physically get there
   on the stated dates, does the money work. **Research no anchors, no opening hours, no
   weather.** These are keyed to a weekday that is not yet final.
2. **Checkpoint with the traveller.** Show the feasibility result and get the shape confirmed:
   final dates, final routing, final ticket structure. Surface any conflict here rather than
   engineering around it.
3. **Design** — anchors, opening hours, seasonality, service routing. Only now are the weekdays
   real.

Discovery does not have a design phase in this sense: it produces a shortlist, not day plans, so
it never researches opening hours and the weekday rule does not bite. Its equivalent of the
checkpoint is the shortlist itself — the traveller picks a destination, dates get fixed, and only
then does the Construction pipeline above start at phase 1.

Separate invocations, not separate phases inside one call. In the measured run a single
`ECONNRESET` late in a combined workflow destroyed 587k tokens of *already-completed* feasibility
work, because the surviving results sat behind a barrier. Separate calls are independently
resumable and independently cacheable.

**The checkpoint must be one consolidated question, not a series.** It exists to save wall-clock,
and it only does that if it replaces several round-trips rather than adding one. The measured run
put four separate questions to the traveller at four different moments — profile confirmation,
visa type, return-day structure and outbound structure, then ticket structure — each one stalling
the pipeline. Every decision that feasibility has surfaced goes into a single prompt: dates,
routing, ticket structure, and any constraint that turned out to conflict. If you find yourself
asking a second question before design starts, the first one was incomplete.

## 3. Cap what each agent may spend

State a budget in every agent prompt. Without one, agents will exhaust a shared session-wide
search quota and leave later stages — including verification — with no network at all. That
happened: the verify pass had to run WebFetch-only because research had used 200 of 200 searches.

Tier the cap by what the domain can cost if it is wrong — a feasibility miss cancels the trip, a
thin anchor list only makes a day duller:

| Stage | Searches per agent | Why |
| --- | --- | --- |
| Feasibility (entry, reachability, budget) | ~15 | These decide whether the trip happens. Underspending here is how a suspended air route or a broken cap survives to the page. |
| Design (anchors, hours, seasonality, service routing) | ~8 | Mostly official pages you can address directly once the district is chosen. |
| Verification | ~10 | Needs enough to fetch every cited source and refute it. |
| Discovery candidate generation | ~10 per candidate batch, not per candidate | Breadth here is the product; cap the batch, not the search. |

That is roughly 3×15 + 3×8 + 7×10 ≈ 139 for a Construction trip, inside a 200-call session budget
with headroom for the orchestrator. Also:

- **Prefer fetching a known official URL directly over searching for it.**
- **Name the primary sources you expect them to use** in the prompt. An agent given
  `csair.com`, `keisei.co.jp`, `tokyometro.jp` does not need to search for them.
- **One domain per agent, and say what is out of scope.** "Do not price hotels" in the flights
  prompt is worth more than any instruction about what to include.
- **The flights agent runs `scripts/kiwi_flights.py` before any web search for fares** and reports
  its `CANDIDATE` and `LINK` lines. One call answers prices, flight numbers, times and baggage for
  the party; web research is for what it leaves `TODO:`, or for when it reports `KIWI UNAVAILABLE`.
- **Never let an agent silently exhaust the shared quota.** Tell it the cap and tell it to report
  what it could not check rather than spending past it. An unchecked fact that says so is a
  finding; an unchecked fact that does not is a defect.
- **Send a path, never a file of this skill's prose.** An agent's prompt is its domain, its cap,
  its named sources, its return schema, and a *path* to any artifact it needs — the plan, its
  domain slice, a scratch file a sibling wrote. The agent can open a path if it needs it and skip
  it if it does not; a paste is paid for in every prompt whether it is read or not, and it is the
  largest line in this budget that nothing above measures. Measured 2026-08-30,
  [booking-html-output.md](booking-html-output.md) is 42,639 bytes — roughly 10.7k tokens at the
  ~4 bytes-per-token ratio `scripts/check_plan_consistency.py` already uses for a plan. The rough
  target below contemplates 13 agents (3 feasibility + 3 design + 5 domains + 2 auditors), so
  pasting that one reference into each of them is ≈139k tokens of prompt before a single search,
  and the six research agents' share alone, ≈64k, is close to a third of the ≈220k those six cost
  in total. The exception is content the agent must apply **verbatim** — the adversarial
  instruction in [verification.md](verification.md#prompt-shape), a provider's coordinate-order
  rule — and that travels as the sentence, not as its file.

## 4. Bound the schema

Prose-heavy schemas return prose-heavy answers. In the measured run, fields worded "state the
basis", "show the arithmetic" and "explain the trade-off" produced 10–40KB per agent, of which a
small fraction reached the plan.

- Use enums, numbers, short strings, and `maxItems` on arrays.
- Ask for `source_url` + `checked_at` on every factual field — that is what makes a claim
  auditable, not a paragraph of reasoning.
- Reserve "show your arithmetic" for the **two or three numbers that decide feasibility** (the
  budget total against the cap, the journey time against the stated maximum). Everywhere else, a
  number and a source is the deliverable.

## 5. Buy each fact once

Agents "share no state" by design, which is right for *independent* domains and wrong for facts
that several domains need. In the measured run, Harbin–Tokyo flight schedules were researched by
four separate agents and Tokyo hotel prices by four more, each burning its own searches on the
same pages.

When two agents need the same fact, have the first write it to a scratch file and tell the second
to read that file. Flights, fares, and lodging prices are one fact set viewed from three angles —
not three domains.

The same economy holds *inside* a single lookup, and it is what keeps the fields added since this
file was measured from costing anything much. One visit to a venue's place page yields the name the
map provider indexes it under, its rating with the count and the scale, its hours for each weekday,
its address and its coordinate pair — five required fields for one page load. One visit to a
property's page on the platform that sells it yields the price, whether those dates are sellable,
and the guest score. Collect them on the way past, and the marginal cost of the newer gates is a few
per cent of a run; collect them later and you pay for every page twice, which is the duplication
this section exists to prevent, just wearing a different hat.

Rule 2 defers anchors, hours and weather until the dates are final because they are keyed to a
weekday. Coordinates and ratings are not — a restaurant's score does not change because the trip
moved a day — but they arrive on the same page as the hours, so there is no earlier moment worth
fetching them at either. Research the venue once, when the dates are settled.

### The arrival essentials ride with the entry check — they are not a phase

`arrival_essentials` adds four facts to every plan: can the traveller pay, get online, call for
help, and are they insured. Four facts is not a research phase and must never be commissioned as
one. **No new agent, no new round, no new checkpoint** — they go to the agent already doing the
entry domain in feasibility, inside its existing cap, because they sit on that agent's own axis:
every one of them is keyed to *nationality × destination*, which is the entry verdict's axis and
nobody else's. The consulate is a fact about one passport in one country. Whether a Dutch EHIC
works in Switzerland depends on the holder's nationality and not on the card. An agent that already
holds those two values answers all four cheaply; any other agent has to be told them first, which
costs more than the facts.

**Budget roughly 4–6 lookups for the whole block, per *country*, not per stop.** Two of the four
are usually one lookup each on the national tourist board (emergency numbers; plugs and voltage,
which arrive on the same kind of page as card acceptance). The other two are the ones worth the
searches, because they are the ones recalled wrongly: whether the traveller's own SIM and their own
health cover reach this country. On a multi-country trip, re-ask only what actually changes —
emergency numbers and consulates are per jurisdiction, while a roaming zone or a currency union
often answers once for the whole trip. Say which you reused; do not silently carry one country's
answer into another, which is the failure `entry_context.per_jurisdiction` already exists to stop.

**And `unverified` is the budgeted way out.** An entry may say, in a summary the traveller can
read, that it was not checked on this run — that is a valid status and the gate accepts it. So a
run that is out of quota degrades to an honest "we did not check this" instead of the two bad
options: inventing the number, or blocking delivery over four facts. What it may never do is stay
silent, which is why the block is required and each entry must carry *something*.

## 6. Do not challenge what the traveller has already decided

The adversarial pass is for claims *you* produced. A fact the traveller stated — "I have the
visa", "the dates are fixed", "I already booked the hotel" — is user-confirmed and outranks
research. Challenging it wastes an agent and, worse, invites the plan to argue with its own
owner. In the measured run an entry-challenge agent was still running after the traveller had
confirmed they held a valid visa.

Exception: verify a *consequence* of a user-confirmed fact when the consequence is checkable and
material. "You hold a multi-entry visa" is theirs to assert; "therefore you may self-book flights
and hotels" is a claim about a rule, and that is fair game.

## 7. Tokens are not time — measure the minutes separately

Everything above buys tokens. The traveller experiences minutes, and the two optimise in
different directions often enough that one number for both would mislead:

- **Compute is a fan-out, so its wall-clock is the slowest agent, not the sum.** Adding a seventh
  research agent to a six-agent phase costs a sixth of a token budget and almost no time.
  Removing one saves tokens and no time at all. Every rule in sections 1–6 is a *token* rule; do
  not expect any of them to make the run feel faster.
- **Waiting on the traveller is a round-trip with a human in it, and it is unbounded.** This is
  why the consolidated checkpoint in section 2 is a time rule rather than a tidiness rule, and
  why asking a second question before design starts is expensive in a way no token count shows.

Run `python scripts/trip_timer.py start <phase> --workspace "<ws>" --run <slug>` and `stop` around
each phase, naming the traveller-facing waits `checkpoint...` or `wait...` so they are counted
separately. `python scripts/trip_timer.py report --workspace "<ws>"` prints the split, and
`audit_workspace.py` summarises it across runs. It records stamps rather than durations, because
`now` is the only thing a caller can honestly assert.

**Do not optimise this from intuition — there is not yet enough data.** Until this file can quote
measured minutes the way it quotes measured tokens, the honest statement is that nobody knows
where the time goes. Report what the timer printed.

## 8. A stalled or dead agent is a finding, not a slow one

A fan-out has stragglers, and the failure mode is specific: **a batch where most agents died
returns the same shape as a batch that found nothing.** Measured on this repo's own design run,
2026-08-15: 64 agents launched, **41 died on a session usage limit** and 23 completed, and the
structured result came back as an empty list for one field. Read as "nothing survived review" it
was completely wrong; the reviewers had simply not run. Agents also stalled — "no progress after
200s — retrying" — which spends wall-clock on a barrier while producing nothing.

So:

- **Never read an empty or thin result without checking how many agents actually finished.** The
  journal records one line per completed agent; the count is the first thing to look at, before
  any conclusion is drawn from the content.
- **Say the survival rate out loud** when reporting a fan-out's findings. "16 rules survived" and
  "16 rules survived, and 41 of 64 reviewers never ran" support very different decisions.
- **Prefer more, smaller invocations over one wide one** when a usage limit is plausible. A batch
  that dies takes its whole barrier with it; three sequential batches lose a third.
- **A phase that stalls has already failed its budget.** Stop it and report what is missing rather
  than waiting it out — an unchecked fact that says so is a finding, one that stays quiet is a
  defect, and that rule applies to a whole phase exactly as it applies to a single claim.

## 9. What not to economise on

**The verification pass in [verification.md](verification.md) earns its cost every time.**
In two measured Construction runs it was the only stage that found trip-breaking defects, and in
both runs all three deterministic gates were green while those defects were present. Cut research
breadth, cap searches, bound schemas — but run the verify pass in full.

## Rough target

For a single-destination Construction trip of under a week: **feasibility ≈ 3 agents, design ≈ 3
agents, verification = 5 domains + 2 offline auditors**.

Budget it as the sum of its parts, because a target below the mandatory floor is not a target, it
is an instruction to cut the pass that catches trip-breaking defects. Six research agents cost
roughly 37k each in the measured run — **≈220k** — and verification measured **≈700k**, so the
honest figure is **900k–1.1M**.

Two corrections to those numbers, both measured after they were written. They were taken before
coordinates, ratings and dated property-scoped links became mandatory; re-measured on a rebuilt
eight-day plan, the added research was **20–40k**, roughly 2–4% of a run, because each of those
fields rides along on a page the design stage was already opening. And the **≈700k** is the *full*
verification tier. A plan that qualifies for the light tier — the conditions are in SKILL.md's
work-mode section, and `check_plan_consistency.py` decides it from the plan's own fields rather than
from how thorough anyone feels — runs four blocks instead of seven, closer to **300k**, which moves
the honest total for such a trip to roughly **550k–750k**. Read what the script printed; do not
argue with it, and do not assume the light tier because a trip feels simple. Past about 1.3M, the overrun is research nobody asked for: a second
agent on a domain the first already covered does not make the answer safer, it makes the same
answer twice and spends the quota verification needs. Say so when you exceed it rather than
quietly trimming the pass.
