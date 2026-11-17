# Travel Day — Connections, Security, Borders, Customs

The day of movement has its own failure modes, and almost all of them are decided weeks earlier by how the itinerary was built.

**Contents:** [Buffers By Ticket Structure](#buffers-by-ticket-structure) · [Airport Arrival Times](#airport-arrival-times) · [Bags](#bags) · [What Cannot Fly](#what-cannot-fly) · [Security And The Liquids Rule](#security-and-the-liquids-rule) · [Immigration](#immigration) · [Customs On The Way Home](#customs-on-the-way-home) · [Long Flights](#long-flights) · [Arrival In A New Country](#arrival-in-a-new-country)

**Before building or approving any travel day**, read `risk_posture` in `config.yaml` and `artifacts/place-<name>.md` for either end if `## Boxes` names one: the queue that took 40 minutes last time is the reason this itinerary is either fine or impossible.

## Buffers By Ticket Structure

The single question is **who owns the miss** (SKILL.md Rule 5):

| Structure | Who owns a missed connection | Buffer |
|---|---|---|
| One ticket, one carrier | The carrier: rebooked, usually at no cost, and bags are through-checked | The published minimum connection time is a floor, not a target |
| One ticket, partner carriers | Still the carrier, with more friction | MCT plus a margin; verify bags are through-checked to the final destination |
| Separate tickets | You do. The second carrier owes nothing and sells you a new ticket at the walk-up fare | **≥3 h international, ≥2 h domestic** |
| Separate tickets, last departure of the day | You do, and there is no later flight | Not a connection. It is a hotel night |
| Any structure, bag must be re-checked | You do, for the time | Add the arrival-hall and re-check time before applying anything above |

Scale by `risk_posture`: `tight` accepts the published MCT on one ticket, `padded` adds an hour to everything and refuses self-transfers under four hours. Three other multipliers: a connection through a hub in a country requiring a transit visa is not a connection at all (`documents.md`); a first flight scheduled to land after the last connecting departure of the day has no recovery; and any itinerary whose first leg is the last flight of the evening has a delay on it every time weather moves.

**Build the day backwards from the fixed point** — the tour that starts at 09:00, the ferry that sails once — not forwards from the departure.

## Airport Arrival Times

Baseline **2 hours international, 90 minutes domestic**, from the door of the terminal, and add:

- +30-60 min for a bag drop at a busy hub, or where check-in closes early (many carriers close 45-60 min before departure and the closure is absolute)
- +30 min for a large airport where the gate is a train ride away
- Whatever the place file recorded last time
- Nothing for online check-in and hand baggage only — that is the case the baseline already describes

Check-in closing, not boarding, is the deadline that strands people. Boarding closes typically 15-20 minutes before departure and the aircraft leaves without a passenger who is in the terminal.

## Bags

- **Weigh at home.** Excess-baggage charges at the counter are priced as a penalty, and a bag 2 kg over costs more than the next fare class would have.
- **Carry-on limits are dimensions and weight**, and the weight is enforced unpredictably by carrier and airport. A bag that fits everywhere in the US may be refused in Europe or Asia.
- **In hand luggage, always**: medication, documents, one change of clothes, chargers, valuables, anything irreplaceable, and the keys to whatever is at the other end.
- **Never in checked baggage**: lithium batteries and power banks, cash, jewellery, laptops in many airline conditions of carriage.
- **Track it**: a Bluetooth tracker in the bag turns "the airline does not know where it is" into a location, which changes the conversation entirely (`disruption.md`).
- **Photograph the packed bag and its contents** before check-in. It is the evidence a lost-baggage claim needs and nobody has.

## What Cannot Fly

The rules that catch normal travellers, all of them stable and all of them enforced:

| Item | Rule |
|---|---|
| Power banks and spare lithium batteries | **Carry-on only, never checked.** Up to 100 Wh freely; 100-160 Wh needs airline approval; above 160 Wh is refused |
| Devices with batteries installed | Checked is allowed by most carriers but the device must be off, not in sleep |
| Aerosols and flammables | Limited quantities; camping gas, lighter fuel and some hair products are refused outright |
| Sharp objects | Checked only; a pocket knife in hand luggage is confiscated, every time |
| Food, plants, seeds, meat, dairy | An agriculture question at the destination, not a security one — and the fines are large. Declare, or leave it behind |
| Duty-free liquids bought in transit | Sealed tamper-evident bag with the receipt visible, or the next security checkpoint takes it |
| Souvenirs from protected species | Coral, ivory, some shells, some timber, some traditional medicines: seizure plus prosecution under CITES |

## Security And The Liquids Rule

Assume the **100 ml per container, one transparent litre bag** rule unless the specific airport publishes otherwise. Newer scanners are lifting it at some airports and not others, and the rule that applies is the one at the airport you are standing in — including the connecting one, where a bottle bought at the first airport can be taken.

Electronics out unless the lane says otherwise, coats and belts off, and everything back in the bag before leaving the belt: the most common actual loss at security is a laptop left in a tray.

## Immigration

- **Answer what is asked**, briefly and consistently with what the form says. Purpose, duration, address, funds. Volunteering plans that sound like work when the entry is as a visitor is the single most common cause of secondary questioning.
- **Carry the evidence for what you claimed**: the return ticket, the address, the insurance, the funds — an officer asking for proof of an assertion is routine (`documents.md`).
- **Both entry and exit days count** against a rolling allowance; log the crossing in `## Presence`.
- **Automated gates** do not always stamp, and an unstamped entry can be a problem later where the stamp is the evidence of compliance. Where the country still stamps, check it happened.
- Refusal of entry is an airline problem before it is a border problem: the carrier flies you back and bills you.

## Customs On The Way Home

The limit is what is brought **in**, including gifts, things bought duty-free in transit, and anything shipped. Alcohol, tobacco and a total value threshold are the usual three; exceeding any one requires a declaration and payment, and non-declaration is what converts a small tax into a penalty.

The VAT-refund sequence, in this order and no other: buy with the form issued at the shop → get the customs stamp **before checking the bag**, with the goods available → claim the refund at the counter or by post. The card refund is usually worth more than the cash one after commission (`money.md`).

## Long Flights

Movement every couple of hours, hydration, and compression socks for anyone with a risk factor — the DVT window extends about two weeks after the flight, and calf pain or breathlessness in that period is the Red Flags table, not a strain. Set the watch to destination time on boarding and eat on that schedule (`health.md`). Download everything before leaving, including the offline map, the boarding passes and the address of the first night, because arrival is the moment with no data.

## Arrival In A New Country

The first ninety minutes, in order: cash or card confirmed working, data working or the eSIM activated, the transfer to the accommodation already decided before landing, and the address written down in the local language and script. The airport taxi decision made in advance is worth more than any other single arrival preparation — it is where the scams are concentrated (`safety.md`) and where an exhausted traveller pays four times the fare.

**After any travel day that produced something worth knowing** — a queue time, a transfer that worked, a connection that was too tight, a security rule enforced differently — write it in the same turn into `artifacts/place-<name>.md` for that airport or city, with its `## Boxes` line, and record the crossing in `## Presence` if days are counted. Destinations and formats: `memory-template.md`.
