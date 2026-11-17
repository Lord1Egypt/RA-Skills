# Companions — Who Is Travelling Changes Everything

The party sets the pace, the budget, the destination shortlist and the failure modes. `default_party` in `config.yaml` says whose constraints apply by default; a specific trip overrides it.

**Contents:** [Whose Constraint Governs](#whose-constraint-governs) · [Children](#children) · [Babies And Toddlers](#babies-and-toddlers) · [One Parent, Or Not The Parent](#one-parent-or-not-the-parent) · [Groups](#groups) · [Money In A Group](#money-in-a-group) · [Elderly Parents And Reduced Mobility](#elderly-parents-and-reduced-mobility) · [Pets](#pets) · [Solo](#solo) · [Meeting People At The Destination](#meeting-people-at-the-destination)

**Before planning for anyone but the default party**, read `constraints_file` from `config.yaml`, `~/Clawic/data/health/profile.md` for anyone with a medical constraint, and the debrief of the last trip with the same party. The pace argument you are about to re-have was already resolved once.

## Whose Constraint Governs

The party's plan is governed by its **least flexible member**, on each dimension separately — and they are usually different people. The toddler sets the daily distance, the grandparent sets the stairs, the coeliac sets the restaurants, the person with the least leave sets the dates. Naming which person governs which dimension prevents the plan that quietly serves the loudest member.

`itinerary_density` drops by one level for every added constraint class: a couple at `balanced` travelling with a toddler and a grandparent plans at `loose`, one anchor a day (SKILL.md Rule 7).

## Children

- **Pace is the whole plan.** One anchor per day, near the accommodation, with an unstructured afternoon. Two anchors is a bad day for everyone.
- **Accommodation over location.** A place with a kitchen, laundry and space to be indoors beats a central room, because the failure mode is a rainy afternoon in a hotel room with nowhere to put anyone.
- **Documents**: children need their own passport everywhere, and their own authorization where one applies. Ages are counted **on the date of travel**, so a child turning 2 or 12 mid-trip changes the ticket price and the seat rules for the return leg (`bookings.md`).
- **Medical**: paediatric doses of anything carried, the vaccination schedule checked against the destination well ahead, and a plan for care abroad that names the facility (`health.md`).
- **Flights**: seats together are not guaranteed unless paid for or assigned at check-in on most carriers. Verify rather than assume.
- **Their own bag, their own responsibility**, sized to what they can actually carry, is the single change that most improves a family travel day.

## Babies And Toddlers

Infants under 2 usually travel on a lap for a small percentage of the adult fare on international routes and often free domestically, without a baggage allowance and without a seat — which is cheap and hard. A purchased seat with an approved car seat is the alternative, and it is the safer one.

Practical constraints: bassinet positions are limited, requested at booking and confirmed at check-in, never guaranteed; pushchairs are gate-checked and occasionally damaged; formula and milk are exempt from the liquids limit in reasonable quantities but must be declared at security; and ear pressure on descent is managed by feeding or a drink, which is worth planning for rather than discovering.

## One Parent, Or Not The Parent

A child travelling with one parent, a grandparent, or any adult who is not their legal guardian is stopped at borders in a growing number of countries. What resolves it: a **notarised consent letter** from the non-travelling parent or parents, with contact details, plus the child's birth certificate and, where surnames differ, evidence of the relationship. Prepare it before departure, in the destination's accepted form; it cannot be produced at the border. Divorced or separated parents should also carry the relevant court order where custody terms exist.

## Groups

- **Someone decides.** Groups without a named organiser default to the slowest possible consensus and the most expensive option. Agree who books what, before anything is booked.
- **Split the group by default.** Plan a daily anchor everyone attends and let the rest of the day fragment. Groups that try to stay together all day argue by day three.
- **Book in one name, or entirely separately** — never half and half. Half-and-half is where seats end up scattered and one person's change breaks four bookings.
- **Set the pace expectation explicitly** at the start: what time the day begins, whether meals are together, what happens if someone is late. Written down, once.
- Groups above roughly eight people cross a threshold into group rates, group check-ins and minimum-numbers contracts, which is a different kind of booking with deposits and named deadlines.

## Money In A Group

Agree the method **before departure** and write it into the trip dossier (`money.md`):

| Method | Works when |
|---|---|
| One payer, settle at the end | Everyone trusts one person to keep the list, and the amounts are similar |
| Shared kitty, topped up equally | Lots of small shared costs — taxis, groceries, entries |
| Strict per item | Widely different budgets, or people joining for part of the trip |

Whichever it is: one person keeps the running list, it is visible to everyone, and it is settled before people go home. The rule about who pays for the person who did not drink, did not eat the shared dish, or arrived on day three is agreed on day zero, not at the last dinner. Anything durable — the agreement, the final settlement — goes in `artifacts/group-<trip>.md`.

## Elderly Parents And Reduced Mobility

- **Request assistance at booking, and reconfirm 48 hours out** with each carrier. Airport wheelchair assistance and priority boarding are free and are provided far more reliably when pre-booked; on the day, unbooked assistance is a wait.
- **Distances are the hidden problem**: airport terminals, train platforms, cobbled streets, and the walk from the taxi drop to the actual door. Measure the accommodation's real accessibility, not its self-description — ask about steps to the entrance, lift dimensions, and bathroom layout, in writing.
- **Medication and insurance**: a full list with generic names, a doctor's letter, and a policy that covers pre-existing conditions, declared. Age loading on travel insurance is steep and unavoidable; the alternative is being uninsured, which is not an alternative (`health.md`).
- **Pace and heat**: fewer, longer stops; a rest built into the middle of the day rather than at the end; and heat treated as a hard constraint rather than a discomfort.
- Mobility equipment travels free on flights and is not counted against baggage, but it is handled and it is damaged; photograph it, label it, and carry the model details for repair.

## Pets

The lead time is **months, not weeks**, and every element is verified with the destination's own authority.

- Microchip **before** the rabies vaccination, or the vaccination does not count and must be repeated.
- Rabies vaccination with a waiting period before travel — commonly at least 21 days for EU entry.
- For entry from some countries, a **blood titre test** taken after vaccination followed by a further waiting period measured in months. This is the requirement that makes short-notice pet travel impossible.
- Health certificate issued inside a short window before travel by an authorised vet, plus any tapeworm treatment within a required window for certain destinations.
- Airline rules are separate from the country's: carrier breed restrictions, temperature embargoes, cabin carrier dimensions, and cargo-only routes.
- Some destinations have quarantine regardless of paperwork. Confirm before booking anything.

Write the paperwork facts into the shared `~/Clawic/data/pets/<name>.md` — identity is the animal's name, and this skill appends only the travel block, never the medical history (`memory-template.md`).

## Solo

Solo travel is cheaper per decision and more expensive per night: single supplements on tours and cruises are real, and a room costs the same for one. It is also the party with the most freedom to change plans, which makes refundable bookings genuinely worth their premium. The safety protocol — itinerary with one person at home, agreed check-in rhythm, arrival before dark — is in `safety.md`, and it is the same protocol regardless of who is travelling.

## Meeting People At The Destination

A host, a guide, a driver, a friend of a friend who turns out to matter afterwards goes in the shared box `~/Clawic/data/contacts/contacts.md` once — identity is email or handle, columns `name | role | preferred channel | context` — and the trip dossier references them **by name only**. Duplicating a person into a trip file is how two skills end up with different phone numbers for the same guide.

**After any trip with a non-default party**, write in the same turn: what the pace actually supported and what governed it into the trip debrief; the group money agreement and settlement into `artifacts/group-<trip>.md`; people who matter afterwards into `~/Clawic/data/contacts/contacts.md`; pet paperwork and its verification dates into `~/Clawic/data/pets/<name>.md`; and any accessibility fact about a place into `artifacts/place-<name>.md` with its `## Boxes` line. Destinations and protocols: `memory-template.md`.
