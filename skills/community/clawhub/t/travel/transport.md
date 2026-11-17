# Transport — Trains, Driving, Ferries, And Getting Around

Ground movement, once the flights exist. Fare search for flights is `flight`; hire-car pricing and comparison is `car-rental`. This is the decision layer and the paperwork.

**Contents:** [Choosing The Mode](#choosing-the-mode) · [Rail](#rail) · [Rail Passes: Price The Actual Legs](#rail-passes-price-the-actual-legs) · [Driving Abroad](#driving-abroad) · [Hiring A Car: The Traps That Are Not Price](#hiring-a-car-the-traps-that-are-not-price) · [Own Car, Own Country Or Not](#own-car-own-country-or-not) · [Ferries](#ferries) · [Local Transport](#local-transport) · [Transfers](#transfers)

**Before choosing a mode**, read the place file for the destination if `## Boxes` names one, and `restrictions` in `config.yaml` — a stated train-over-plane threshold, a licence the traveller does not hold, or a mobility constraint eliminates options before any comparison starts.

## Choosing The Mode

Compare **door to door, total cost, and what it does to the day** — never terminal to terminal:

| Distance / situation | Usually right | Switch when |
|---|---|---|
| Under ~300 km in a country with fast rail | Train: city centre to city centre, no airport buffers | The route requires two changes and a bus, or rail fares are unregulated and last-minute |
| 300-800 km with high-speed rail | Train, once airport transfers and the 2-hour buffer are added to the flight | The rail journey exceeds ~4.5 h door to door and the flight is direct |
| Anywhere with poor rail and dispersed sights | Car: the freedom is the product | Cities at both ends, where a car is a parking problem with a rental cost attached |
| Islands, or a coast with short hops | Ferry, which is transport and sightseeing at once | Sea conditions in season, or a schedule that consumes a whole day |
| Inside a city | Public transport plus walking | Late night, heavy luggage, or a genuinely unsafe route (`safety.md`) |
| Anything else | Price the two realistic options door to door, with the transfers, and say which day is better | — |

A `train_over_plane_hours` preference, once stated, settles this class of decision without re-deriving it every trip.

## Rail

- **Advance fares** on operators that use them (much of Europe, the UK, some Asian networks) open months ahead and rise steeply; walk-up fares on regulated networks do not, which is why "book trains early" is right in one country and irrelevant in the next.
- **Reservations are separate from tickets** on many high-speed and international services, and are compulsory on some. A valid pass with no reservation is a passenger not allowed to board.
- **Night trains** convert a travel day into a night and a hotel cost, and they are the one case where transport time is genuinely free. Book couchettes early; they sell out first.
- **Station, not city**: large cities have several terminals and a connection between two of them is a taxi, not a platform change. Check which station both legs use.
- **Validation** still exists on some regional networks; an unvalidated ticket is a fine even when it was bought legitimately.
- Luggage on trains is self-service and unlimited in practice, which is a real advantage over flying for gear-heavy trips.

## Rail Passes: Price The Actual Legs

A pass is worth it or not, and the answer is arithmetic, not reputation:

1. List the **actual journeys** intended, with dates.
2. Price each one as an individual advance ticket on the operator's own site.
3. Add the **compulsory reservation fees** the pass does not cover — this is what kills passes on the French, Spanish and Italian high-speed networks, and on international services.
4. Compare against the pass price plus the same reservation fees.

Passes win for many journeys, spontaneous routing, and networks with unregulated walk-up fares. They lose for a small number of long journeys that can be booked in advance. Record the outcome in the trip dossier so the next trip to the same region does not redo the exercise.

## Driving Abroad

- **International Driving Permit**: required in a long list of countries, valid typically one year, and issued only in the country of the licence **before departure** — it cannot be obtained abroad. A national licence alone is refused by police and by some rental desks (`documents.md`).
- **Which side, and the fatigue that comes with it**: the first hour on the unfamiliar side is the dangerous one, and roundabouts and turns across traffic are where it goes wrong. Do not schedule an unfamiliar-side arrival drive after a long-haul flight.
- **Mandatory equipment** varies and is enforced by fine: warning triangle, high-visibility vest for each occupant, spare bulbs, breathalyser, winter tyres or chains in season by law rather than by weather.
- **Environmental and access zones**: city centre restrictions requiring a windscreen sticker or a pre-registration, with automated fines that arrive months later via the rental company plus an administration fee.
- **Tolls**: some networks require a transponder or a pre-paid online registration that cannot be done at the barrier.
- **Motorbikes and scooters**: most travel insurance excludes injury without the correct licence class for that engine size, and a helmet. A scooter hired casually abroad is frequently an uninsured vehicle with an uninsured rider (`safety.md`).
- **Alcohol limits abroad are lower than at home in many countries, and zero in some.**

## Hiring A Car: The Traps That Are Not Price

- **The excess, not the daily rate**, is the number. A cheap rate with a large excess plus the desk's own waiver costs more than the mid rate that included it; a separate annual excess policy bought at home is usually the cheapest route, and the desk will still block the excess on the card.
- **A credit card in the main driver's name** is required for the deposit almost everywhere; a debit card is refused at many desks even where the booking accepted it.
- **Photograph and video every panel, the wheels, the roof and the windscreen** before leaving, and again on return, timestamped. Damage claims after return are the single most common rental dispute.
- **Fuel policy**: full-to-full is the only one that does not carry a markup.
- **Cross-border restrictions** are common and frequently absolute; taking a car into a country the contract excludes voids the insurance.
- **Additional drivers, young-driver surcharges and one-way fees** are the lines added at the desk.

## Own Car, Own Country Or Not

Taking the user's own vehicle abroad adds paperwork: insurance cover extended to the destination and in writing, breakdown cover valid abroad, the registration document carried, and the country-specific mandatory equipment above. The vehicle itself lives in the shared box `~/Clawic/data/vehicles/<plate>.md` (identity is the plate) — write the travel-relevant facts there, and reference the vehicle from the trip dossier by plate only, never duplicating the record.

## Ferries

Book vehicle space in advance in season, because foot passengers get on and cars do not. Check-in closes far earlier than for flights — often 45-90 minutes for vehicles. Cabins on overnight crossings sell out before seats. Rough-sea cancellations are a normal seasonal event on exposed routes, so a ferry on the last possible day before a flight is a single point of failure.

## Local Transport

Buy the multi-day or stored-value card at the airport station on arrival if the city has one; it is usually cheaper than individual tickets by the second day, and it removes the daily ticket-machine friction. Learn the one local rule that catches visitors — validation, boarding by the front door, a flat fare zone that ends where the tourist sights do — and record it in the place file. Ride apps have wildly different coverage by city and country: check availability before assuming, and have a cash fallback.

## Transfers

Airport to accommodation decided **before landing**, both directions, with the cost known. The return transfer is the one people improvise and overpay, and it is also the one with a hard deadline. For an early departure, book it the night before and confirm it exists; a 05:00 taxi that was never actually booked is a missed flight (`travel-day.md`).

**After any trip involving ground transport**, write in the same turn: the pass-versus-tickets arithmetic and its outcome into the trip dossier; the transfer that worked, the local transport rule, and the driving quirk into `artifacts/place-<name>.md` with its `## Boxes` line; and any vehicle fact into `~/Clawic/data/vehicles/<plate>.md`. Formats and shared-box protocol: `memory-template.md`.
