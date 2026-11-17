# Health — Vaccines, Medication, Insurance, Arriving Functional

Requirements and recommendations change by outbreak and by year. This file gives the **lead times and the decision structure**; a travel clinic or the destination's health authority gives the current requirement. Anything in the Red Flags table of `SKILL.md` outranks everything here: route to a clinician.

**Contents:** [The Lead-Time Ladder](#the-lead-time-ladder) · [Vaccines: Required Versus Recommended](#vaccines-required-versus-recommended) · [Malaria And Other Prophylaxis](#malaria-and-other-prophylaxis) · [Carrying Medication Across Borders](#carrying-medication-across-borders) · [Insurance: What Actually Pays](#insurance-what-actually-pays) · [Jet Lag](#jet-lag) · [Food, Water, Altitude, Sun](#food-water-altitude-sun) · [The Medical Kit](#the-medical-kit) · [Getting Care Abroad](#getting-care-abroad)

**Before answering anything medical**, read `~/Clawic/data/health/profile.md` (shared box: vaccinations with dates, allergies, current medication, conditions) and `constraints_file` from `config.yaml`. A vaccination already held and still valid is the most common thing a traveller pays for twice.

## The Lead-Time Ladder

Medical readiness, not visas, is usually the thing that makes a trip impossible at short notice. Booking date determines what is achievable:

| Lead time | What it unlocks |
|---|---|
| 6-8 weeks | A travel clinic appointment plus multi-dose vaccine courses (rabies pre-exposure, Japanese encephalitis, hepatitis B) — these are the courses that cannot be compressed |
| 4 weeks | Single-dose vaccines with time to develop immunity; yellow fever certificate becomes valid 10 days after the dose |
| 2-3 weeks | Mefloquine started, if that is the prophylaxis chosen, because tolerance is assessed before departure |
| 1 week | Prescription refills sized for the trip, medication letters, dental check for a long or remote trip |
| 1-2 days | Atovaquone-proguanil or doxycycline started |
| On the day | Nothing medical. A same-week trip to a high-risk area is a trip taken with the protection you already have |

Buying insurance is its own clock and it starts at the **first trip payment**, not at departure (below).

## Vaccines: Required Versus Recommended

- **Required** means entry is refused without the certificate. In practice this is yellow fever, and it keys off **every country transited**, not just the destination — a connection through an endemic country can trigger it. The certificate becomes valid 10 days after the dose and, under the 2016 WHO amendment, is valid for life.
- **Recommended** means nobody checks, and it is where the actual risk lives: hepatitis A, typhoid, rabies pre-exposure for remote or animal-contact travel, Japanese encephalitis for rural stays in season, tick-borne encephalitis for forested Europe.
- **Routine** is the one people skip: tetanus every 10 years, measles for anyone born after the vaccine but before two documented doses, and whatever the destination is currently seeing an outbreak of.

Rabies pre-exposure vaccination does not remove the need for treatment after a bite — it removes the need for immunoglobulin, which is exactly the component unavailable in the places where bites happen. That is the argument for it, and it is the one people get wrong.

## Malaria And Other Prophylaxis

Prophylaxis choice is a clinician's decision. What belongs in a travel plan is the **timing constraint**, because it sets the appointment date:

| Regimen | Start | Continue after leaving |
|---|---|---|
| Atovaquone-proguanil | 1-2 days before | 7 days |
| Doxycycline | 1-2 days before | 4 weeks |
| Mefloquine | 2-3 weeks before, so tolerance is known before departure | 4 weeks |

The post-trip half is where compliance collapses and where the infections come from. Bite avoidance is not optional alongside any of them: an insect repellent with a proven active ingredient, long sleeves at dusk and dawn, a treated net where rooms are not screened. Dengue, chikungunya and Zika have no prophylaxis at all, and their mosquito bites during the day — a different behaviour pattern from malaria's.

**Fever after a malaria-area trip is an emergency for three months, not three days.** The travel history is the diagnostic clue, and it is only useful if volunteered.

## Carrying Medication Across Borders

The rule people assume — "it is my prescription, so it is fine" — is false in a long list of countries.

- **Check the destination's controlled-substance list** for every medication being carried, generic name in hand. Stimulants for ADHD, strong painkillers, some sleep medications, cannabis-derived products including CBD, and some ordinary cold and sinus remedies are controlled or banned somewhere popular.
- **Carry in the original labelled packaging**, in hand luggage, in the quantity that matches the trip length. Bulk quantities look like importation.
- **A doctor's letter** with the generic name, the dose, the condition and the traveller's name is the document that resolves questions at a border, and it must be written before departure.
- **Brand names do not travel.** Record the generic name in the shared health profile — asking a pharmacist in another country for a brand they have never heard of is the failure mode.
- **Split the supply** across two bags where possible, and carry more than the trip length: a two-day delay with a one-day margin of insulin or anticonvulsant is a medical emergency, not an inconvenience.
- Time-zone shifts change the dosing schedule for anything taken at fixed intervals. Work it out before flying, not at 3 a.m.

## Insurance: What Actually Pays

Buy it with the **first non-refundable payment**, not before departure. In the market where these products originate, the waivers worth having — pre-existing condition cover, and cancel-for-any-reason — typically expire ~14-21 days after that first payment and cannot be bought back later. Late purchase costs the cover, not the premium.

Read four things in any policy, and record them in the policy's row in `## Documents`:

| Clause | What to look for |
|---|---|
| Medical evacuation cap | The number that matters. An air ambulance from a remote region is the scenario the policy exists for, and hospital-bill cover without evacuation cover is a policy for the easy case |
| Pre-existing conditions | Almost always excluded without a declared waiver, and the definition includes conditions under investigation, not just diagnosed |
| Activity exclusions | Motorbikes and scooters (with or without a valid licence for that class), diving beyond a depth, skiing off-piste, any altitude above a stated metres figure, and anything paid to a guide |
| Advisory clause | Cover can void the day the home government raises an advisory for that area, even mid-trip (`safety.md`) |

Card-provided cover is real but narrow: it usually requires the trip to have been paid on that card, excludes pre-existing conditions, and caps evacuation far below a standalone policy. It is defensible for short trips inside good public-healthcare systems. Record whatever cover already exists in the ledger's `## Card Benefits` section — `## Loyalty` in `memory.md`, or `programs.md` once split — so it is not bought twice (`loyalty.md`).

Reciprocal state healthcare agreements (the European ones, and various bilateral schemes) cover treatment, never repatriation, and never a private clinic. They are a supplement, not a policy.

## Jet Lag

Adjustment runs at roughly **a day per time zone crossed**, and eastward is slower than westward because the body drifts long more easily than short. Three levers, in order of effect:

1. **Light at the right end of the day.** Travelling east: bright light in the destination's morning, avoid it in the evening. Travelling west: the reverse. Getting this backwards actively delays adjustment.
2. **Local time from the moment you board**, including meals. Nothing dictated by the departure time-zone helps.
3. **Sleep pressure**, not sedation: a short nap capped at 20-30 minutes before mid-afternoon, and no long recovery sleep on arrival day.

For trips of two nights or fewer, staying on home time deliberately beats a half-adaptation that leaves you wrong in both. Deeper sleep mechanics: the `sleep` skill.

## Food, Water, Altitude, Sun

- **Water**: the rule is what the *locals with the same gut flora* do, adjusted for the fact that yours is different. Sealed bottles, boiled, or filtered; and the invisible sources are ice, salads rinsed in tap water, and brushing teeth.
- **Food**: hot, cooked, and busy. A stall with turnover is safer than an empty restaurant with a tablecloth.
- **Travellers' diarrhoea**: oral rehydration first and always; anti-motility medication only for a functional emergency such as a bus journey, and never with blood or fever (Red Flags).
- **Altitude**: ascend slowly above ~2,500 m, and treat headache with unsteadiness or breathlessness at rest as descend-now (Red Flags). Acclimatisation cannot be bought with fitness.
- **Sun and heat**: the exposure that burns people is the one they were not sunbathing for — a boat, a glacier, a full day walking a city. Heat illness in a humid climate arrives faster than thirst does.

## The Medical Kit

The kit is not a pharmacy: it is what is hard to buy at 2 a.m. in an unfamiliar country. Oral rehydration salts, the traveller's own prescriptions in original packaging plus margin, painkillers they know they tolerate, an antihistamine, blister care, a wound dressing and antiseptic, insect repellent, and anything a diagnosed condition needs on hand — an adrenaline auto-injector, an inhaler, glucose. Store the standing list as `artifacts/packing-medical.md` and refine it after each trip (`kit.md`).

## Getting Care Abroad

Before departure: the insurer's 24-hour line and policy number on the emergency card, physically, and the destination's emergency number, which is not 911 or 112 everywhere. Many insurers require notification **before** treatment for anything non-emergency, and paying out of pocket without that call is how a valid policy declines a valid claim.

At the point of care: keep every receipt, the diagnosis in writing, and the prescription; photograph them the same day. Ask for the report in a language the insurer can read, or note that a translation will be needed. Pharmacies in much of the world dispense a wider range without prescription than the traveller expects, which solves small problems fast — with the generic name, not the brand.

**After any vaccination, prescription, insurance purchase or medical event abroad**, write it in the same turn: vaccinations, allergies, medication and conditions to `~/Clawic/data/health/profile.md` (shared box protocol in `memory-template.md`); the policy provider, number, evacuation cap and exclusions to `## Documents` with its renewal in `## Due`; a medical event and its receipts into the trip dossier, and the claim into `artifacts/claim-<provider>-<yyyy-mm>.md`.
