# Restroom Demand & Queueing — Reference

## The two failure modes

**Mode 1: under the code minimum.** Legal/permit problem. Fixture
counts below the adopted plumbing code's occupancy table block the
certificate of occupancy. Boring, tabular, non-negotiable.

**Mode 2: code-compliant but burst-broken.** Comfort/brand problem.
Codes size for steady-state occupancy; events create pulsed demand.
This is why a fully-legal theater still has a 20-minute women's line
at intermission. Almost every memorable restroom disaster is Mode 2.

## Demand constants (model defaults)

Visits per person per hour by venue (bladder-and-beverage driven;
sports/festival higher due to alcohol volume, offices lower):

| Venue | visits/person/hr |
|-------|------------------|
| office | 0.25 |
| school-day | 0.30 |
| theater | 0.30 |
| conference | 0.35 |
| wedding | 0.40 |
| concert | 0.45 |
| sports | 0.50 |
| festival | 0.55 |

Median occupancy per fixture visit:

| Fixture | seconds |
|---------|--------:|
| urinal | 35 |
| stall (WC) | 95 |
| lavatory (sink) | 20 |

These medians come from time-motion studies of public restroom use;
tail behavior (stall visits 3-5 min) is why stalls are queuing
bottlenecks. Adjust stall occupancy upward for venues where a
meaningful share of visits are non-urinary (family venues, medical
facilities).

## The queueing core: M/M/c and Erlang-C

Arrivals Poisson with rate λ (people/sec), service exponential with
rate μ = 1/occupancy per fixture, c fixtures in parallel. Expected
wait:

```
Erlang-B:  B(0)=1;  B(k) = ρ̂ B(k-1) / (k + ρ̂ B(k-1)),  ρ̂ = λ/μ
Erlang-C:  C = B(c)·c·μ / (c·μ − λ)
E[wait]    = C / (c·μ − λ)
```

Stability requires ρ = λ/(cμ) < 1 — above that, the queue grows
without bound and the "wait" is meaningless (report as OVERLOAD).

### Burst (event) mode

A break dumps N·s people (s = burst share, default 0.4) into a
T-minute window. Two numbers matter:

- **Burst utilization** ρ_burst = (N·s/T) / (c/occupancy). ≥1 means
  the fixtures can never drain the burst within the window.
- **Drain time** = N·s·occupancy / c — how long until the last person
  is served, measured FROM BURST START. Compare against the window
  plus acceptable lingering (5 min).

Empirical burst shares: halftime at sports ~0.4-0.5, theater
intermission ~0.35-0.45, conference session breaks ~0.3-0.4 (lower if
organizers stagger tracks), festival continuous (~no burst, use
sustained mode).

## Fixture minimum tables (IPC-style ladder)

Simplified assembly occupancy ladder (female WC / male WC / male
urinals / female lavs / male lavs):

| Occupants | F WC | M WC | M Ur | F Lav | M Lav |
|----------:|-----:|-----:|-----:|------:|------:|
| ≤25  | 1 | 1 | 1 | 1 | 1 |
| ≤50  | 2 | 1 | 1 | 1 | 1 |
| ≤75  | 3 | 2 | 1 | 2 | 2 |
| ≤100 | 4 | 2 | 1 | 2 | 2 |
| ≤150 | 6 | 3 | 2 | 3 | 3 |
| ≤250 | 8 | 4 | 3 | 4 | 4 |
| ≤400 | 12 | 6 | 4 | 6 | 5 |
| ≤600 | 16 | 8 | 6 | 8 | 7 |
| ≤800 | 20 | 10 | 8 | 10 | 8 |
| ≤1200| 30 | 15 | 12 | 15 | 12 |

Beyond 1200: scale ~1 WC/100 occupants female, ~1/200 male, urinals
~1/200.

**Critical caveat:** this is a planning aid, not the code. IPC and
UPC (IAPMO) tables differ in detail; states/cities amend both. The
audit mode is for early design and gut-checks — the stamped drawing
must cite the locally adopted edition.

## The stall/urinal asymmetry (why women wait)

With equal populations and equal visit rates:

- Men's throughput: urinal occupancy 35 s → ~103 visits/hr/fixture
- Women's throughput: stall occupancy 95 s → ~38 visits/hr/fixture

Same demand, 2.7x service time ⇒ for equal waits, ~2.7x the fixtures.
"Potty parity" laws (now adopted in many US jurisdictions, UK, and
elsewhere) push ratios toward 2:1 female:male fixtures precisely
because of this arithmetic. The `demand` mode makes the asymmetry
visible in utilization percentages.

## All-gender conversion math

Converting a binary split restroom block to all-stall:

- Lost urinals move their users onto stalls at 2.7x the service time.
- Rule of thumb: replace every 2 urinals with ~1.5-2 additional
  stalls to hold the same men's wait, THEN size total stalls for the
  combined population at the stall service rate.
- Door-count math: total fixtures must rise in conversion; a 1:1 swap
  of urinal→stall usually improves women's wait at the cost of men's.

## Mitigation ladder (cheapest first)

1. **Stagger the break** — split intermission into two waves, or
   schedule session gaps 10 min apart across tracks. Cuts burst
   share; free.
2. **Lengthen the window** — a 20-min instead of 15-min intermission
   drops burst λ by 25%.
3. **Convert WCs to urinals** (men's) — triples fixture throughput
   in plumbing-capacity terms if the drain supports it.
4. **Add stalls** — the only fix that helps the female/stall queue.
5. **Distributed banks** — a remote second restroom location splits
   the arrival stream (people join the nearer line); effectively
   raises c.

## What this model does NOT cover

- ADA/accessibility fixture counts and clearances (separate tables)
- Portable toilets (different service model — see event-rental
  industry ratios: ~1 unit/50 attendees for 4-hr events as a start)
- Cleaning/maintenance cycles (throughput killers at festivals)
- Fixture trap/drain sizing (vent and stack engineering)

## Validation notes

Erlang-C overestimates wait when arrivals are not Poisson (scheduled
breaks are sharper than exponential) and underestimates when balking
occurs (people leave when they see a long line). In burst mode, read
TIGHT as "bad" and FAIL as "very bad" rather than trusting minute
values; the utilization and drain-time numbers are the robust ones.
