# Usability ROI module

Load for every task-driven interface, or when the user asks for usability within a conversion-page
audit. When both modules apply, keep usability findings separate from conversion-content findings.

Citation keys: **M04** = Marcus 2004 (AM+A white paper). **LN08** = Loveday & Niehaus 2008.
Full references in `../ATTRIBUTION.md`.

## Where usability pays

Marcus (2004) groups the financial effects of usable interface design into these areas. Use them to
name the *kind* of value a usability fix produces.

| Area | What changes | Typical measure | Source |
|---|---|---|---|
| Development | Less rework, shorter schedules | Development hours, cost of late changes | M04, "Development: Reduce Costs" |
| Maintenance | Fewer post-release fixes | Change requests, maintenance spend | M04, "Reduce maintenance costs" |
| Sales | More traffic, retention, appeal | Visits, conversion, returning customers | M04, "Sales: Increase Revenues" |
| Use | Higher success rate, fewer errors, faster work | Task success, error rate, time on task | M04, "Use: Improve Effectiveness" |
| Support and training | Fewer help requests, shorter training | Support contacts, training hours | M04, "Decrease support costs"; "Reduce training/documentation cost" |
| Risk | Lower exposure to disputes and safety incidents | Incidents, claims | M04, "Other ROI Factors: Litigation deterrence and safety" |

The earlier a usability problem is found, the cheaper it is to fix; the white paper reports an
order-of-magnitude rise in cost at each later stage (Gilb 1988, as cited in M04). Marcus shows that
design options are widest and change costs lowest in the requirements phase (M04,
"Development: Reduce Costs").

## Usability factors to score

Score each as Pass / Partial / Fail / N/A, the same way as the content criteria.

| ID | Factor | Check | Financial link | Source |
|---|---|---|---|---|
| US-1 | Findability | A visitor can locate the target content or product in few steps | Lost visitors and lost sales | M04, "Sales: Increase Revenues"; LN08, ch. 5, ch. 6 |
| US-2 | Navigation | Structure is predictable; the visitor knows where they are | Traffic reaching converting pages | M04, "Sales: Increase Revenues"; LN08, ch. 5 |
| US-3 | Search and filtering | Search returns the expected items; filters narrow results | Lead and sale volume | M04, "Sales: Increase Revenues"; LN08, ch. 6 |
| US-4 | Form efficiency | Data entry is short, clearly labelled, and forgiving | Completions; throughput | M04, "Use: Improve Effectiveness"; LN08, ch. 8 |
| US-5 | Error prevention and recovery | Errors are prevented where possible and easy to recover from | Support cost; abandonment | M04, "Use: Improve Effectiveness"; LN08, ch. 8 |
| US-6 | Task success | A first-time user can finish the main task unaided | Productivity; support and training cost | M04, "Use: Improve Effectiveness" |
| US-7 | Learnability | The interface can be used with little or no training | Training and documentation cost | M04, "Use: Improve Effectiveness" |
| US-8 | Returning-user experience | Repeat visits are at least as easy as the first | Retention and repeat revenue | M04, "Sales: Increase Revenues" |

Neither source gives direct evidence on page load time or accessibility. If the user asks about
them, say they are outside this skill's sources and do not attach a citation.

## Evidence the white paper reports

Use these to explain *why* a factor matters. All are secondary citations: the figures come from the
studies named, as reported by Marcus (2004). They date from 1981–2001. Never present them as current
benchmarks, and never apply a figure from one product to another.

| Topic | Reported finding | Cite as |
|---|---|---|
| Cost of late fixes | Fixing a problem costs roughly ten times more in development than in design, and a hundred times more after release | Gilb 1988, as cited in M04 |
| Development time | Usability engineering shortened development by about a third to a half in the cases reported | Scerbo & Bosert 1991, as cited in Bias & Mayhew 1994, as cited in M04 |
| Maintenance share | Most software life-cycle cost falls in maintenance, much of it from unmet user requirements | Pressman 1992, as cited in M04 |
| Findability | Across 15 large sites, users found the information they sought in 42% of attempts | Spool / User Interface Engineering 1998, as cited in Nielsen 1998, as cited in M04 |
| Search redesign | One property site raised successful home searches from 62% to 98% and lead generation by more than 150% | Vividence 2001, as cited in M04 |
| Returning customers | A returning customer was reported to spend about twice as much as a new one | Nielsen 1997, as cited in M04 |
| Screen redesign | Redesigned screens raised throughput by 25% and cut errors by 25% in one case | Gallaway 1981, as cited in M04 |
| Support calls | Interface improvements cut help-desk calls sharply in several vendor cases | Karat 1990, 1994, as cited in Bias & Mayhew 1994, as cited in M04 |
| Training | A graphical interface cut training by 35% in one reported case | Dray & Karat 1994, as cited in M04 |

For the complete list, the original figures, and the full reference list, read the white paper
itself (see `../ATTRIBUTION.md`). This table is a short paraphrased selection, not a reproduction.

## Valuing a usability fix

When the goal is not a sale, estimate cost avoided:

```
Annual value = (contacts or hours avoided per year) × (cost per contact or hour)
ROI (%)      = (Annual value − Investment) ÷ Investment × 100
```

The benefit categories are from M04; the ROI formula is the same as in `roi-model.md`. Use the
user's own volumes and costs. Do not substitute figures from the table above.

## Prioritizing

- Fix problems on the path with the heaviest drop-off first (LN08, ch. 3).
- Prefer fixes found early; the same problem costs more at every later stage (M04, "Development: Reduce Costs").
- Measure before and after on the same metric: task success, error rate, conversion, or support
  contacts (LN08, ch. 3; M04, "Use: Improve Effectiveness").
