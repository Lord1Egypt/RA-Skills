# Parallel verification

Read this before delivering any Construction plan, and whenever `check_plan_consistency.py`
is run with `--verification`.

## Why this stage exists

`render_final_trip_html.py` proves the plan is well-formed. `validate_trip_html.py` proves the
page has every required region, link, and enum. `check_plan_consistency.py` proves the plan
agrees with itself. **None of them prove anything in it is true.**

A real run passed all three while shipping: a visa conclusion that stopped short of EVUS and
would have produced a denied boarding at check-in; two "competing" flight options that were the
same aircraft sold twice; a free tour booked on a day it does not run; dinners at venues that
close three hours earlier; and a fare charged in one direction billed as round trip. An
adversarial pass found 68 such defects, six of them trip-breaking.

The lesson is not "check harder". It is that **truth-checking is a different axis from
structure-checking, and it fans out cleanly** — the entry rules, the transit fares, the opening
hours, the lodging inventory, and the seasonality of a plan share no state. Verifying them
sequentially costs five times the wall-clock and, worse, spreads one agent's attention across
five domains until each gets a fifth of it. That is how a dinner gets scheduled at a closed
restaurant: not from ignorance, but from attention already spent elsewhere.

<a id="verify-domains"></a>
## Run the five domains concurrently — plus the two auditors

Always all five, always in one fan-out, and always with the two network-free auditors described
under *Prompt shape* below. A domain that looks irrelevant still returns `findings: []`, which is
a claim someone made — silence from a domain nobody ran is not. The gate rejects a report missing
any block **the plan's own tier requires**: seven on the full pass, and four on the light tier
(`sights_and_hours`, `transport`, and both auditors). `required_domains_for` in
`check_plan_consistency.py` computes which of the two applies by reading the plan, so it is not a
choice you make — and running all seven anyway is never rejected, because the gate only refuses
blocks that are *missing* or that name a domain outside the protocol. That asymmetry is why the
instruction above is still "always all five": over-verifying costs tokens, under-verifying ships
a fare nobody checked.

| Domain | Verify |
| --- | --- |
| `entry` | Visa requirement per **nationality × residence status**, not nationality alone. Anything required *after* the visa and before boarding — EVUS for PRC passports holding 10-year B1/B2, ETA/eTA schemes, transit visas for the actual connection airports. Passport-validity rule as the destination states it (commonly six months beyond intended stay), not "covers the trip". Current appointment waits, dated. |
| `transport` | Every fare, duration, headway, and season in the plan, against the operator. Which direction a fare is collected in. Whether a named route exists, on the planned weekday, in the planned season. Whether a fallback is reachable from where the traveller would actually be stranded. **Open every day and segment map button and confirm the pin lands where the label says** — a directions URL whose endpoint does not resolve returns HTTP 200 and looks identical to a working one, which is how a button offering a 65-hour drive from Taiwan passed every structural gate. |
| `sights_and_hours` | Opening hours and closure days for every venue and attraction, against the specific dates. Whether a tour or service is daily or weekday-gated. Whether a combo ticket may be split across days. Timed-entry rules. Accessibility conditions the plan asserts. **Whether each recommended venue exists at the name the plan uses**, and whether its rating and price band match what its own page says — one plan's dinner venue returned no listing on any platform, and two of its lunches were at restaurants that open at 20:00. |
| `booking_and_lodging` | Whether the dates are sellable yet — airline windows apply to **both** legs of a round trip, and codeshare inventory opens no earlier than the operating carrier's. Who actually operates each flight. Whether the property offers the room product claimed, in that season. Whether search URLs load a prefilled search. Applicable lodging taxes. **For every ticket a day actually schedules, when do the seats go on sale, and where does the plan have the traveller at that moment?** That pair is what `sale_opens_at` records, and this domain is the one with a network, so it is the one that can answer it: Kabukiza single-act seats are released 12:00 the day before, and the plan itself had the traveller in the Narita immigration queue at that hour. `check_plan_consistency.py` compares the two once the field is filled; nothing but this pass can fill it honestly, and a guessed `always_available` is an invented fact rather than a blank. **Open each property-scoped link and read the price and availability off that page**: this domain exists in its current form because two hotels shipped behind one city search, and only opening them showed that one cost more than the traveller's entire cap and the other had no availability on the dates at all. |
| `seasonality` | Climate figures with the right statistic — a monthly *mean* is not the mean daily *maximum*, and quoting the latter as the former oversells a destination by ~5 °C. Daylight and sunset times where the plan schedules a sunset. Whether seasonal services still run on the planned dates. |

A Kiwi.com result (`scripts/kiwi_flights.py`) is a comparison-platform source, not the airline. Re-running the script with the plan's dates is an accepted way for `booking_and_lodging` to re-check a fare and its availability; record the run's time as the check time.

### How to fan out, per runtime

"Concurrently" is a property of the harness, not of this file, so use whatever the one you are in
actually provides:

- **Claude Code** — the Workflow tool, or several Agent calls issued in a single message. Give
  each agent one domain and a schema so the results come back structured.
- **Codex** — no subagent tool, but `codex exec` is a normal command: launch one non-interactive
  child per domain from the shell, each writing to its own `--output-last-message` file, then
  collect the files. Cap the number in flight so the five do not contend.
- **Anything else, or when a fan-out is unavailable** — run the five **sequentially but
  separately**, one domain per pass, and do not carry one domain's findings into the next.

That last option is not a consolation prize, and understanding why matters more than the
mechanism. The reason to split verification was never wall-clock: it is that a single pass asked
to check entry rules, fares, opening hours, lodging inventory, and seasonality at once gives each
of them a fifth of its attention, and the thing that gets dropped is whatever is least
interesting at that moment — which is how a dinner ends up booked at a restaurant that closes at
17:00. Five sequential focused passes preserve that benefit entirely and cost only time. Five
domains crammed into one prompt do not, however fast they return.

<a id="prompt-shape"></a>
### Prompt shape

Each verifier gets **its own domain slice** of the plan — `python scripts/plan_slice.py <plan.json>
--domain <name>`, which writes `slices/<plan-stem>.slice-<name>.json` beside the plan — and this
instruction. Hand over that path, not the plan's, and read [the slice](#plan-slice) below for what
it does and does not remove. The default must be doubt, because an agent asked to "check" a claim
tends to find support for it:

> Be adversarial: try to **refute** each claim. Use official sources — government, transit
> agency, operator, airline — over aggregators and blogs. If a fact cannot be confirmed from a
> primary source, return `unverifiable` rather than `confirmed`. Report only claims that are
> wrong, misleading, or stated as fact while unverifiable. Do not report confirmed claims.

Add two auditors alongside the five, in the same fan-out — they need no network:

- **consistency** — duplicates what `check_plan_consistency.py` decides. Run the script; use the
  agent only for what the script cannot express, such as whether a day's pacing is physically
  plausible.
- **completeness** — "what is missing?" Which stated preference is served only by a token
  anchor, which hard constraint is asserted but never measured, which collected field never
  reaches the page.

<a id="plan-slice"></a>
### The slice each verifier reads

`scripts/plan_slice.py <plan.json> --domain <name>` writes a projection of the plan for one of the
five domains and prints exactly which top-level blocks it removed. It removes nothing else: kept
blocks are byte-identical and in their original order, so a `claims_checked` pointer into one of
them resolves against the real plan too, which is what the gate will check.

The five domains **do not partition the plan**, and the table above is prose, not a schema. So the
tool subtracts rather than selects: `trip`, `days` and `budget` are kept unconditionally, a block
is dropped only where that domain's row cannot be answered from any field in it, and a top-level
key the tool has never seen is kept and reported. Building it the other way round — an allow-list
per domain — takes `days` away from `booking_and_lodging`, which needs it to answer where the
traveller is when the seats go on sale, and takes the flight cards away from `entry`, which needs
them for the connection airports.

**Accept the smaller saving; it is not the same size on every plan.** Measured 2026-08-30 across
the 15 plans in one real workspace, five domains each:

- On the median plan (85,836 bytes) the slices come out 3.3%–7.4% smaller. That is the ordinary
  case, and most of what a domain does not read is small.
- On the largest plan (2,132,252 bytes) they come out ~96% smaller, because that plan carries an
  `imagery` block of base64 photographs and no truth domain reads a photograph. On a plan like
  that, five verifiers reading the plan is the dominant line in the ~700k this pass costs.
- 13 of those 75 slices come out **larger** than the plan: all five domains on each of the two
  smallest plans, and single domains on two more. A small plan carries almost none of the
  droppable blocks, so all that is left is the tool's own provenance header. It says so, in
  those words, and when it does, hand that domain the plan path instead.

What is *kept* is the part worth understanding, because each one was an argument someone lost.
`booking_options` stays in all five: `sights_and_hours` needs the timed-entry rules on the ticket
cards, `entry` needs the connection airports on the flight cards, and `seasonality` needs it
because 3 of those 15 plans state a **sunset or daylight fact inside `booking_options`** — twice
on a flight card, as the stated reason for preferring one flight over another. `sources` stays in all five because the first move
in refuting a claim is opening the source the plan leaned on, and dropping entries from it would
renumber `sources[n]` and break pointers. `destination_experience_anchors` stays for `seasonality`
because 2 of those 15 plans state a season-dependent fact inside `why_it_matters` — a winter
closing time in one, a January sea temperature in the other.

Two rules for using it:

1. **If a claim you need is not in the slice, open the full plan** — its path and SHA-256 are in
   the file's `plan_slice` header — and say so in your findings. Reporting `unverifiable` because
   a block was projected away would turn a token saving into a defect, which is the one way this
   change can make the pass worse.
2. **Never hand a slice to `check_plan_consistency.py`, and never slice the two auditors.** The
   gate reads the whole plan. So do `consistency` and `completeness`: every question they ask
   compares two parts of the plan to each other, so a block removed from the file is
   indistinguishable from a block the plan never had. The tool refuses their names for that
   reason rather than with a usage error.

Slices land in `slices/` beside the plan rather than in `plans/` itself, and that is not tidiness:
`audit_workspace.py` recognises a plan by its *shape* — a `days` list and a `trip` key, which every
slice has — over a non-recursive `plans/*.json` glob, so five slices dropped in there become five
extra "plans" in every later audit, each reported as an itinerary missing blocks it never had.
Point `--out` somewhere else if you like; the tool warns when you aim it back at `plans/`.

## Merging: the part that is not automatic

Fan-out is easy; the merge is where parallel verification goes wrong. Agents will contradict
each other and themselves.

1. **Rank by source, not by confidence.** One agent citing the operator beats three citing
   aggregators. A high-confidence claim with a blog URL loses to a low-confidence one with a
   `.gov` URL.
2. **Prefer the narrower claim.** "Walk-on fares are $11.35 each way" and "fares are collected
   westbound only" are not a tie — the second explains the first and is checkable at the source.
3. **`unverifiable` is a result, not a failure.** Record it and mark the plan's own claim as an
   estimate. Never promote it to `confirmed` because it sounded right.
4. **Every `wrong` or `misleading` finding must be either fixed in the plan or explicitly
   accepted by the traveller** before delivery. The gate enforces this: a finding with those
   verdicts and `resolved` unset fails `check_plan_consistency.py --verification`.
5. **Fixing one finding can break another.** Re-run the consistency script after edits — moving
   a dinner changes the route, which changes the walking totals, which the walking check reads.

<a id="report-schema"></a>
## Report schema

Start from [templates/verification-report.json](../templates/verification-report.json), which
carries all five domain blocks, both audit blocks, and an inline note on each required field. Write the filled copy to
`<workspace>/plans/verification-<slug>.json`:

```json
{
  "checked_at": "2026-08-03",
  "plan": "plans/2027-09-08-seattle.json",
  "domains": [
    {
      "domain": "entry",
      "claims_checked": [
        "entry_context.status",
        "entry_context.traveler_basis",
        "trip.destination"
      ],
      "findings": [
        {
          "claim": "the plan states a B1/B2 visa is sufficient to board",
          "verdict": "misleading",
          "correction": "PRC passports with 10-year B1/B2 must also hold a current EVUS enrolment; airlines check it at check-in",
          "severity": "critical",
          "evidence_url": "https://china.usembassy-china.org.cn/visas/nonimmigrant-visas/",
          "resolved": true,
          "resolution": "entry_context and recheck_before_purchase now require EVUS before departure"
        }
      ]
    }
  ],
  "audits": [
    {
      "audit": "consistency",
      "claims_checked": ["days[2].route.duration_minutes", "days[2].route.walking_burden"],
      "findings": []
    },
    {
      "audit": "completeness",
      "claims_checked": ["budget.cap_per_person", "assumptions[0]"],
      "findings": []
    }
  ]
}
```

`domain` must be one of the five names above, and no others are allowed. How many must appear is read off the plan by `check_plan_consistency.py`, not chosen: the full pass needs all five, and a plan that qualifies for the light tier (see SKILL.md's work-mode section) needs `sights_and_hours` and `transport`. Both audits are required either way. The
two auditors go in a sibling `audits` array — `{"audit": "consistency"|"completeness",
"claims_checked": [...], "findings": [...]}` — with exactly those two names, both required, and
findings in the same shape as a domain's. They are a separate array rather than two more domains
because the five check the plan against the outside world and these two check it against itself;
they are *required* because the schema used to accept five while this reference told you to run
seven, so the cheapest way past the gate was to delete the two highest-yield agents in the pass.
`verdict` is `confirmed`, `wrong`, `misleading`, or `unverifiable`. `severity` is `critical`,
`major`, or `minor`. `resolved` is required on `wrong` and `misleading`, and it closes a finding
only as the JSON literal `true` beside a `resolution` that says what changed in the plan, or that
the traveller accepted it — a bare `true` with no resolution, or `"yes"`, is refused, because
either one made a wrong finding vanish without anyone saying what was done about it. The severity
of a wrong or misleading finding is held to those three words; on a confirmed finding it ranks
nothing and is not read.

`plan` and `claims_checked` exist to make forgery cost something. `plan` binds the report to one
itinerary, so a single clean report cannot be handed to every trip; the checker compares it to
the file it was supplied for. `claims_checked` is the **list of plan pointers** that block actually
opened — `days[0].dining[1].venue_hours`, `budget.breakdown[2].per_person_high` — non-empty, unique
within its block, and every one of them has to resolve against the plan. Without it, a domain that
returns no findings is indistinguishable from a domain nobody ran, and "all five clean" is exactly
what a skipped pass looks like.

It was a *count* until that proved to be no evidence at all: an integer is a promise the same run
writes about itself, so a block whose verifier subagent died — a real failure mode — writes a small
number and the gate goes green with "verified" on a page someone books a train from. A list that has
to resolve costs more to fabricate than to earn. Pointing at a field whose value is null is fine;
examining an empty field is real work. One coverage rule is enforced on top: `sights_and_hours` must
cite every `days[].dining[]` card whose `hours_status` claims researched or verified, because that is
exactly where the measured defect lived.

Since 2.1 that rule reaches every dining card rather than a subset, and not by being widened: a card
may no longer name a `time_window` while its `hours_status` is `unverified`, and the renderer
requires every card to name one — so "researched or verified" is now the only legal state and every
card must be cited. The venue-existence and rating checks in that domain's row ride on the same
pointer, which is deliberate. Do not add a *separate* rating-coverage sentence here: a claim in this
file that no code measures is the exact defect class that produced the release, and this one already
has its backstop.

The checker also rejects a report dated before the plan's `generated_at`, since it cannot have
inspected a plan that did not exist.

<a id="rechecks"></a>
### Rechecking after a change

A verified save stamps a `verification_receipt` into the plan: a fingerprint for every section it
covered — each day by its date, each booking option by its id, and each other content block by
name. Keys the scripts write (the verification status, the gate stamp, the sidecar name, the
receipt itself) are not content and are left out. When the plan is saved again against the same
report, `check_verification` compares the plan with its receipt and names every section that
changed or was added. Each of those needs a `rechecks` entry in the report —
`{section, section_digest, checked_at, reason, claims_checked, findings}` — dated no earlier than
the report, citing pointers that resolve and stay inside that section, with findings held to the
rules above. `python scripts/new_verification_report.py --recheck --from-plan <plan.json> --report
<report.json>` appends one TODO entry per changed section to that report, in place, for you to
fill; the placeholder rule refuses it until someone has re-opened those parts. The page then lists
which parts were rechecked, and when — on a verified page only.

**The loop runs on what the scripts print.** Re-save the edited plan with `--overwrite` alone: a
save that replaces a verified copy reads that copy's report, and a delivered copy saved in place
keeps its own name (the slug comes from the file). The refusal prints the scaffold as a whole
command — this interpreter, absolute paths, `--receipt-from` when you edited a working copy rather
than the delivered one — and the scaffold prints the save that finishes the loop. Run each as
printed. A report copied beside its delivered plan names that plan, so the delivered copy
checks and saves against it. A copy delivered before receipts existed records nothing about what
its report covered: `--overwrite` alone refuses it and prints the scaffold for a fresh report — or
save it `--unverified` — because re-attaching its old report would re-certify any edit to it. Walked literally on 2026-09-24 before this existed, the same three steps sent an assistant
to a full re-verification, handed it `<plan.json>` placeholders, and wrote the amended report to
standard output where nothing read it.

**A section also covers the trip facts it was checked against.** `trip.traveler_count` is part of
every day, booking option, the budget and the transport overview; `trip.traveler_constraints` of
every day, booking option and the transport overview. Changing either asks for a recheck of each
of those, not of `trip` alone — see
[replanning.md#party-changes](replanning.md#party-changes). A section emptied since the verified
save counts as removed: nothing in it is left to verify.

A recheck covers the part **as it was when rechecked**, not the part from then on. The scaffold
records that version's `section_digest`, and an entry counts only while the part still has it: edit
the same day again and it needs a new entry (run the scaffold again; the old one stays as history).
Without this, one recheck of a day covered every later edit of it, and the page said the day had
been re-checked. For the same reason, write the entries after the part's final edit — a fix made
after scaffolding changes the digest, and the scaffold has to be run again.

A save that replaces a delivered copy with `--overwrite` compares against that copy's receipt when
the plan it is given carries none. The receipt is written into the workspace copy, never into the
file you keep editing, so re-saving your working file over the verified copy used to arrive with no
receipt and re-stamp the edit as verified.

Why by section and not by file: until 2026-09-24 the report bound a plan by file name and date only,
so a day moved from 13:30 to 14:00 after verification re-saved as verified with no banner. A
whole-file fingerprint would have closed that by making every edit cost the full seven-block pass
again — the price of swapping one dinner. Per section, only the part that moved is rechecked and
every other part keeps its verification. A receipt stamped against a different report date binds
nothing: a fresh full report is a fresh verification. A receipt bound to the report also replaces
the rule that a report may not predate the plan's `generated_at`: the receipt says section by
section what the report saw, so bumping `generated_at` along with a rechecked edit is not refused.

**What none of this can prove:** that a finding marked `resolved` was actually fixed. Code cannot
diff an edit it never saw. That is why every resolved finding carries a `resolution` string
naming the change — it is checkable by a human reading the report against the plan, and it is
the honest boundary of the automated gate.

## Cost, honestly

A five-domain fan-out plus two auditors on a six-day plan cost about 30 minutes of wall-clock
and 800k tokens in the first measured run. A second run, on a 4-day single-city trip, spent 691k
on verification alone inside a 1.18M total — so treat 700k as the honest figure for the pass and
do not expect a short trip to be proportionally cheaper. It scales with the number of *claims* in
the plan, not with the number of nights.

That is worth it for a trip someone will book and fly, and it is not worth it for a discovery
shortlist nobody has committed to.

**Where the money is not.** `claims_checked` as a pointer list adds roughly 250 tokens to a whole
report — 0.04% of the pass. Requiring the two auditors adds two agents that need no network at
all, and in the run that prompted the requirement they produced 27 of 55 findings and 5 of the 6
criticals. Neither is where a pass gets expensive; the domains that fetch are. If a pass needs to
be cheaper, narrow what each domain fetches, do not drop blocks.

So the scope depends on what is being delivered, and this is the one place the distinction
matters:

- **Construction** — all five domains plus both auditors. Seven blocks is what the schema accepts
  from a plan on the full pass, which is what a Construction plan almost always computes; a plan
  the code puts on the light tier owes four, and submitting seven is still accepted. Aim at seven,
  because a Construction plan is something the traveller books from.
- **Discovery** — `entry` and `seasonality` are the two that can eliminate a candidate outright,
  so verify those inline while scoring candidates. Do **not** write a report for them. Discovery
  produces an intermediate shortlist, not a saved plan, so no report is required and a partial
  one would fail `check_plan_consistency.py --verification` **at either tier** — `entry` and
  `seasonality` alone are missing `sights_and_hours`, `transport` and both auditors, and the light
  tier requires all four of those. The tier is not a way to make a Discovery report legal.

## Skipping it

`save_trip_deliverables.py --unverified` saves without a report. It is a real escape hatch, not
a formality, because forcing a 30-minute pass onto an early draft would only teach people to
route around the gate entirely.

What it costs: the saved plan records `verification_status: unverified`, and the rendered page
carries a **"not fact-checked" banner above everything else**, localized with the rest of the
page. That is deliberate — a flag stored only in JSON warns whoever opens the JSON, which is
never the person holding the itinerary at an airline counter. Never call such a page
booking-ready, and re-save it with `--verification` once the pass has run; the banner disappears
on its own when the report is supplied.
