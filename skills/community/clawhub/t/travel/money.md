# Money — Budgets, Payment, And Where It Actually Goes

**Contents:** [Building The Number](#building-the-number) · [Per-Day Rates Are Learned, Not Looked Up](#per-day-rates-are-learned-not-looked-up) · [The Fee Stack](#the-fee-stack) · [Cards, Cash, And DCC](#cards-cash-and-dcc) · [Getting Cash](#getting-cash) · [Tipping And Bargaining](#tipping-and-bargaining) · [Tracking While Travelling](#tracking-while-travelling) · [Refunds, Chargebacks, Tax Reclaim](#refunds-chargebacks-tax-reclaim) · [Splitting With Other People](#splitting-with-other-people)

**Before quoting any cost**, read `## Spend Baselines` in `~/Clawic/data/travel/memory.md` and the dossier of any past trip to the same region. A rate they actually paid, with its date, beats every published estimate — and it is the one number this archive exists to produce.

## Building The Number

Every estimate is a total, in one currency, with the date it was made (SKILL.md Rule 3):

```
transport (both directions, whole party)
+ nights × lodging rate
+ days × daily rate (food, local transport, entries)
+ named one-offs (the permit, the pass, the guided day)
+ insurance
+ the fee stack
= total, ±20%, estimated <month year>
```

Name the four largest lines. Quote per party by default, per person only if `default_party` is `solo` or the user asks — mixing the two is the most common way an estimate is silently wrong by 2×.

Distinguish **committed** from **discretionary** in the trip's money table in `trips/<yyyy>-<place>.md`: transport and lodging are decided once and fixed; the daily rate is where a trip that runs over is actually recoverable.

## Per-Day Rates Are Learned, Not Looked Up

Published daily-budget figures are averages over travellers who are not this one. After the first trip to a region, the archive replaces them. Until then, use bands and say they are bands:

| Style | What it means in practice |
|---|---|
| `budget` | Dorms or the cheapest private room, self-catering or street food, public transport only, free sights |
| `midrange` | Mid-tier hotel or apartment, restaurants for one meal a day, occasional taxi, paid entries |
| `comfort` | Well-located hotel, restaurants without checking prices, taxis by default, guided days |

The multiplier between adjacent styles is typically around 2× on lodging and around 1.5× on the daily rate, and roughly nothing on transport — which is why "we could do this cheaply" rarely moves a long-haul total as much as expected.

Regional bands belong in `## Spend Baselines` with their currency, their date, and **what they covered**, because "€95 a day" means nothing without knowing whether lodging is inside it. Always store per person, per day, and always name the inclusions.

## The Fee Stack

The lines that make a careful estimate come in over budget (SKILL.md, Cost Lines People Forget). Each one is small; together they routinely add 10-20% to a short trip:

- Airport transfers, both ends, both directions
- Seat selection, checked bags, and any fee charged for checking in at the airport rather than online
- Resort fees and city tourist taxes, collected at the property, in local currency, absent from the platform's total
- Foreign transaction fees: typically 1-3% per card transaction
- ATM operator fees plus the home bank's fee, per withdrawal
- Visa and authorization fees, per traveller, non-refundable on rejection
- Data: roaming or an eSIM
- Deposits and pre-authorisations that freeze real money for days
- Booking-platform service fees and cleaning fees, added at the last screen

## Cards, Cash, And DCC

**Always pay in the local currency.** When a card terminal, a website or an ATM offers to bill in your home currency, that is dynamic currency conversion: the rate is set by the merchant's processor, not your bank, and it is worse — commonly by several percent, sometimes far more — on top of any fee your card already charges. There is no case in which accepting it is correct. Decline it every time, including on airline websites and hotel checkout screens where it is the pre-selected option.

Card strategy that survives a trip:

- **Two cards on two networks**, from two issuers, carried in two places. One skimmed, blocked or swallowed card is a normal event.
- **One card with no foreign transaction fee** as the default spend card; know the number before travelling, not after the statement.
- **Credit for anything with risk attached** — car hire deposits, tours paid in advance, an airline in financial trouble — because a chargeback is the only real recourse when a provider simply does not deliver.
- **Notify or check the issuer's travel policy** if the bank still blocks foreign use; most no longer need it, some still do.
- Contactless coverage is near-universal in some countries and near-absent in others; a card-only traveller in a cash economy is stuck. Check before assuming.

## Getting Cash

- Withdraw from a **bank-operated ATM**, in a larger amount and fewer times: fees are mostly per transaction, so four withdrawals cost four times as much as one.
- **Decline the conversion** at the ATM screen too — it is the same DCC in a different costume.
- Standalone ATMs in tourist areas and airports charge the most and are the ones offering the most aggressive conversion.
- Airport exchange counters are the worst rate available anywhere; take a small amount if arrival genuinely requires cash, and get the rest from an ATM in town.
- Carry a modest emergency reserve in a major currency, separate from the wallet.
- Cross a border with the equivalent of €10,000 / US$10,000 or more, including everyone in the party pooled, and it must be declared (`documents.md`).

## Tipping And Bargaining

Both are local rules and getting them wrong costs either money or goodwill. Two failure modes: applying a home-country tipping norm where service is included by law, and refusing to bargain where a quoted price is understood by both sides to be an opening. Look up the norm for the destination once and record it in the place file — it does not change, so it is a one-time cost that pays on every return trip.

## Tracking While Travelling

Ambition kills tracking. What survives is one number a day: total spent, in local currency, written down at the end of the day. Categories can be reconstructed from card statements later; a day missed cannot.

Write it into the trip dossier's money section, actual next to budget, so the variance is visible while there are still days left to correct it. At the debrief, the actual total and the per-day rate learned go into `## Spend Baselines` — that is what makes the next estimate for that region accurate instead of hopeful (`debrief.md`).

## Refunds, Chargebacks, Tax Reclaim

- **Cancellation refunds** follow the terms recorded at booking, and the deadline is in the property's local time (`bookings.md`).
- **Statutory refunds** are separate from goodwill vouchers: for a cancelled flight, a refund is generally owed if you decline the replacement, and a voucher is not a refund unless you accept it (`disruption.md`).
- **Chargebacks** are the backstop for services not delivered, with a time limit measured from the transaction or the intended service date. Ask the merchant first, document the refusal, then file — issuers reject chargebacks filed without evidence of trying.
- **VAT/GST reclaim** on goods leaving a country requires the form issued **at the point of purchase**, the goods available for inspection, and a customs stamp **before** the bag is checked. Every step is where people lose it, and the refund counter's cash option charges a commission the card option does not.
- Every refund and its date goes on the trip dossier, and any claim with an outcome becomes `artifacts/claim-<provider>-<yyyy-mm>.md`.

## Splitting With Other People

Agree the method before departure, not at the first restaurant (`companions.md`): one person pays and everyone settles at the end, a shared kitty topped up equally, or strict per-item. Whichever it is, one person keeps the running list and the agreement is written into the trip dossier — a group money argument is almost always about a rule nobody stated, not about the amounts.

**After any spend figure, rate, refund or claim**, write it in the same turn: the trip's money table in `trips/<yyyy>-<place>.md`, the learned rate in `## Spend Baselines` in `memory.md` with its currency and month, the claim in `artifacts/`, and any recurring travel cost such as a card annual fee in the shared `~/Clawic/data/finances/subscriptions.md`. Destinations and formats: `memory-template.md`.
