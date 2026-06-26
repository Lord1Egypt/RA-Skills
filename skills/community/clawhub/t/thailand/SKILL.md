---
name: Thailand
slug: thailand
version: 1.0.0
changelog: "Initial release with nationwide Thailand guidance for visitors, residents, remote workers, students, and founders."
homepage: https://clawic.com/skills/thailand
description: Choose the best Thailand base for travel, remote work, expat life, or business with visa clarity, cost reality, and local operating playbooks.
metadata: {"clawdbot":{"emoji":"🇹🇭","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/thailand/` does not exist or is empty, read `setup.md` and begin naturally.

## When to Use

User asks about Thailand for travel, relocation, remote work, education, retirement, or business setup. Agent gives practical, current, region-level guidance with legal and cultural context.

## Architecture

Memory lives in `~/thailand/`. See `memory-template.md` for structure.

```bash
~/thailand/
└── memory.md     # Trip or relocation context
```

## Quick Reference

| Topic | File |
|-------|------|
| **Visitors** | |
| Must-see routes and what to skip | `visitor-attractions.md` |
| Itineraries (7, 14, 21 days) | `visitor-itineraries.md` |
| Where to stay by travel profile | `visitor-lodging.md` |
| Practical tips and local friction points | `visitor-tips.md` |
| **Regions and Bases** | |
| Nationwide region comparison | `regions-index.md` |
| Bangkok strategy | `regions-bangkok.md` |
| Chiang Mai and the north | `regions-chiang-mai.md` |
| Phuket and the Andaman coast | `regions-phuket.md` |
| Gulf islands and secondary bases | `regions-islands.md` |
| Isan and deep north routes | `regions-north.md` |
| Decision framework by budget and goals | `regions-choosing.md` |
| **Food** | |
| Thai food landscape | `food-overview.md` |
| Street food playbook | `food-street.md` |
| Core Thai dishes and regional styles | `food-thai.md` |
| International dining and premium options | `food-international.md` |
| Best areas by city and style | `food-areas.md` |
| Dietary and food safety constraints | `food-practical.md` |
| **Practical** | |
| Moving and settling | `resident.md` |
| Flights, rail, ferries, urban transit | `transport.md` |
| Cost of living and budgeting | `cost.md` |
| Safety and legal risk | `safety.md` |
| Seasons, weather, and air quality | `climate.md` |
| SIM, banking, apps, admin | `local.md` |
| **Career and Long Stays** | |
| Visa strategy and compliance checkpoints | `visas.md` |
| Digital nomad and remote-work reality | `nomad.md` |
| Teaching English pathways | `teaching.md` |
| Tech ecosystem and hiring market | `tech.md` |
| Business setup and tax posture | `business.md` |
| **Lifestyle** | |
| Culture, etiquette, and norms | `culture.md` |
| Healthcare and insurance planning | `healthcare.md` |
| Nightlife by city and island | `nightlife.md` |
| Expat and local lifestyle fit | `lifestyle.md` |
| Thai language and communication basics | `language.md` |
| **System files** | |
| Setup flow and activation defaults | `setup.md` |
| Memory schema and update rules | `memory-template.md` |
| Research source pack | `sources.md` |

## Core Rules

### 1. Identify User Intent Before Giving Places
- Separate user intent into trip, relocation, remote work, retirement, education, or business.
- Match recommendations to timeline and risk tolerance first, then suggest regions.

### 2. Thailand Is Multiple Distinct Markets
Thailand is not one homogeneous destination:
- Bangkok is high-opportunity, high-friction, and transit-heavy.
- Chiang Mai is lower cost and easier pace, but weaker salary density.
- Phuket and islands are lifestyle-heavy with seasonal pricing spikes.
- Isan and secondary provinces deliver lower costs but fewer English-friendly services.
Use region files before answering housing, work, or schooling questions.

### 3. Visa and Entry Rules Drive Feasibility
- Entry pathways, extensions, and reporting obligations change frequently.
- TDAC, eVisa, and visa class details must be checked before a user books flights or signs long leases.
- Use `visas.md` first for any plan beyond a short holiday.

### 4. Current Data Snapshot (March 2026)

| Item | Typical Range |
|------|---------------|
| 1BR Bangkok central | THB 18,000-45,000 per month |
| 1BR Chiang Mai central | THB 10,000-25,000 per month |
| 1BR Phuket main zones | THB 20,000-60,000 per month |
| Street food meal | THB 50-120 |
| Mid-range dinner for two | THB 700-1,800 |
| Domestic flight sale fare | THB 900-2,500 one-way |
| Intercity rail 2nd class | THB 300-1,200 route-dependent |

### 5. Seasonality Is Operational, Not Cosmetic
- Hot season and humid heat change daytime productivity.
- Rainy season can disrupt ferries, roads, and island logistics.
- Burning season in the north can make air quality a primary constraint.
Use `climate.md` and `safety.md` when user plans dates.

### 6. Cost in Thailand Is Two-Speed
- Local food and simple housing can be low-cost.
- Imported goods, premium areas, and international schools escalate budgets quickly.
- Family budgets are usually dominated by housing, schooling, and healthcare quality tier.
Use `cost.md` and region files before saying "Thailand is cheap."

### 7. Mobility Strategy Changes Outcomes
- Bangkok rewards BTS/MRT proximity.
- Islands require weather-aware ferry and flight buffers.
- Remote northern routes often need car or motorbike confidence.
Use `transport.md` and avoid one-size-fits-all transport advice.

### 8. Cultural Respect Is Practical Risk Management
- Temple etiquette, dress, and behavior norms materially affect user experience.
- Monarchy-related speech and online behavior are legal-risk topics.
- Nightlife and cannabis/alcohol assumptions vary by zone and enforcement context.
Use `culture.md` and `safety.md` for high-risk behavior guidance.

### 9. Source-Critical Guidance
- Prefer official Thai or embassy sources for entry, visa, and legal constraints.
- Present prices as ranges with date context.
- Tell users what to re-check before spending money on flights, schools, leases, or company setup.
Use `sources.md` for primary references.

## Thailand-Specific Traps

- Treating Thailand as one market and choosing the wrong base for the goal.
- Booking tight island transfers in monsoon windows with no buffer day.
- Assuming visa rules are static across years and nationalities.
- Signing annual rentals before testing commute, flood exposure, and neighborhood noise.
- Underestimating burning season exposure in north Thailand.
- Overcommitting to scooters without licensing and insurance readiness.
- Assuming premium private hospitals exist at equal quality in every province.
- Running business activity on tourist status without legal setup.
- Using exact budget claims with no variance for high season.
- Ignoring local holiday and festival effects on transport and prices.

## Legal Awareness

- Monarchy-related legal risk is serious; advise strict caution in speech and social posting.
- Drug and controlled-substance law exposure can be severe; rules have changed and must be re-checked.
- Visa overstay, unauthorized work, and incomplete immigration reporting create legal and travel risks.
- Road incidents are a major risk area; licensing and insurance compliance matter.
- Business and employment activities require the correct legal entity and permit posture.

See `visas.md`, `safety.md`, and `business.md` for details.

## Security & Privacy

**Data that stays local:** Preferences and planning context in `~/thailand/`.

**This skill does NOT:** Access files outside `~/thailand/` or make undeclared network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and itinerary structure
- `expat` - Relocation planning and adaptation workflows
- `food` - Deeper dining strategy and cuisine personalization
- `startup` - Founder operations and execution systems
- `dubai` - Another international relocation and city strategy benchmark

## Feedback

- If useful: `clawhub star thailand`
- Stay updated: `clawhub sync`
