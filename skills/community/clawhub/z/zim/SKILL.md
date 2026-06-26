---
name: zim
description: >-
  Agent travel middleware for searching flights, hotels, and car rentals,
  assembling policy-aware itineraries, managing traveler preferences, and
  preparing payment-ready booking workflows via Stripe Checkout.
  Uses Travelpayouts affiliate API and SerpApi for search aggregation.
  Includes a Python CLI/package, shell search scripts, and a WhatsApp
  conversational agent. Use when the user asks to search, compare, rank,
  assemble, approve, or prepare booking for flights, hotels, accommodations,
  car rentals, or full trips.
metadata:
  openclaw:
    requires:
      bins: ["python3", "bash", "curl", "jq"]
    capabilities:
      - id: stripe_checkout
        description: Creates Stripe Checkout sessions for payment collection (test mode by default)
        scope: payment
        requires_env: ["STRIPE_SECRET_KEY"]
      - id: travelpayouts_search
        description: Searches flights and hotels via Travelpayouts affiliate API
        scope: search
        requires_env: ["TRAVELPAYOUTS_TOKEN"]
      - id: serpapi_search
        description: Searches flights and hotels via SerpApi for Google Flights/Hotels results
        scope: search
        requires_env: ["SERPAPI_KEY"]
    sensitive_env:
      - STRIPE_SECRET_KEY
      - STRIPE_WEBHOOK_SECRET
      - TRAVELPAYOUTS_TOKEN
      - SERPAPI_KEY
      - OPENROUTER_API_KEY
---

# Zim — Agent Travel Middleware

Use Zim as a travel workflow engine, not a generic search helper. Accept structured or messy travel intent, apply policy and traveler preferences, assemble coherent booking-ready options, and state clearly what is and is not automated.

## What this package contains

This skill package includes:

- `SKILL.md` — operating instructions for the skill
- `scripts/search-flights.sh` — Travelpayouts/Aviasales flight search with cached-fare fallback
- `scripts/search-hotels.sh` — hotel deeplink generation for live availability lookup
- `scripts/search-cars.sh` — car rental comparison deeplinks
- `references/api-guide.md` — API/deeplink notes for Travelpayouts and related links
- `references/agent-to-agent-booking.md` — product model and truthfulness rules
- `zim/` — Python package implementing:
  - travel models and itinerary assembly
  - policy / approval logic
  - traveler preference storage
  - CLI commands (`zim flights`, `zim hotels`, `zim cars`, `zim trip`, `zim preferences`, `zim policy`)
  - booking state machine and local booking persistence
  - Stripe Checkout session creation for payment collection
  - placeholder booking executor that does **not** complete real supplier reservations
- `tests/` — package tests
- `pyproject.toml` — Python package metadata and dependency declarations

Do not describe this package as shell scripts only. It contains both shell helpers and a Python application.

## Runtime requirements

Require all of the following when using or publishing this skill:

- Python 3.10+
- Standard shell environment for bundled scripts
- Installed command-line tools used by the shell scripts:
  - `bash`
  - `curl`
  - `jq`
  - `python3`
- Python packages declared by the package metadata / environment:
  - `pydantic>=2.0`
  - `click>=8.0`
  - `httpx>=0.25`
  - `python-dateutil`
  - `stripe>=8.0`
- Optional dev/test packages when running tests:
  - `pytest>=7.0`
  - `pytest-asyncio>=0.21`
  - `respx>=0.21`

If a downstream environment expects `requirements.txt`, generate it from the package metadata or install from `pyproject.toml`. This package currently declares dependencies in `pyproject.toml`, not in a checked-in `requirements.txt` file.

## Required environment variables

Declare these explicitly when using the skill:

| Variable | Required | Purpose |
|---|---|---|
| `TRAVELPAYOUTS_TOKEN` | Yes for flight/hotel affiliate search | Travelpayouts / Aviasales token used for API access and affiliate attribution |
| `TRAVELPAYOUTS_MARKER` | Yes for production affiliate attribution consistency | Affiliate marker identifier for Travelpayouts deeplinks and tracking |
| `STRIPE_SECRET_KEY` | Yes for payment flow | Stripe secret key used to create and retrieve Checkout Sessions |
| `STRIPE_WEBHOOK_SECRET` | Yes for webhook verification in deployed payment flow | Stripe webhook signature secret |
| `ZIM_BASE_URL` | No | Base URL for Stripe success/cancel redirects; defaults to `http://localhost:8000` |

Important notes:

- `TRAVELPAYOUTS_TOKEN` enables the current search scripts.
- `TRAVELPAYOUTS_MARKER` should be treated as required configuration for a production deployment even if some current scripts reuse the token as a marker fallback.
- `STRIPE_SECRET_KEY` should be `sk_test_...` in the current beta/test setup.
- Live Stripe mode is **not** a default assumption.

## External services and API dependencies

Zim depends on these external services:

### Travelpayouts / Aviasales
Used for:
- flight search API calls
- affiliate deeplink generation
- hotel affiliate/search deeplinks

### Stripe
Used for:
- hosted Checkout Session creation
- payment status retrieval
- webhook-based payment confirmation flows

### Linked booking/search destinations
Zim may generate outbound deeplinks to:
- Aviasales
- Hotellook
- Booking.com
- Google Hotels
- Kayak
- Discover Cars
- Rentalcars.com
- Economy Bookings

These links are for comparison or manual completion unless a real provider executor is added.

## Payment and booking boundaries

Be precise about what Zim does today.

### Current payment state

- Stripe Checkout integration exists.
- Stripe is currently intended for **test mode / MVP flows**.
- Live mode requires a verified Stripe account plus proper operational setup.
- Do **not** imply live payment collection is production-ready unless that has actually been configured and verified.

### Current booking execution state

- The bundled `PlaceholderExecutor` does **not** create real airline, hotel, or car rental reservations.
- Zim can create booking-ready options, approval summaries, and payment requests.
- After payment, actual provider reservation automation is still pending unless a real executor is added.
- Do not say `booked` in plain language unless supplier-side booking execution truly happened.

Preferred truthful language:
- `booking-ready options assembled`
- `awaiting approval`
- `payment link created`
- `payment collected; provider reservation still requires execution/manual completion`

Avoid false claims like:
- `your trip is fully booked`
- `payment completed and reservation confirmed`
unless a real provider confirmation exists.

## Payment-data disclosure

Zim includes payment orchestration via Stripe, but payment-card handling is intentionally limited.

- Zim creates Stripe Checkout Sessions server-side using `STRIPE_SECRET_KEY`.
- Zim stores Stripe session IDs, payment status, totals, and related booking metadata.
- Zim attaches booking metadata such as booking ID / trip ID to Stripe objects.
- Zim may prefill customer email into Stripe Checkout.
- Zim does **not** directly collect, process, or store raw card numbers, CVCs, or full payment method details in the current architecture.
- Card entry is intended to occur on Stripe-hosted checkout pages.
- Webhook verification requires `STRIPE_WEBHOOK_SECRET` in deployed flows.

Treat booking/payment metadata as sensitive operational data even though raw card data is not stored by the package.

## Quick start

### Shell scripts

```bash
# Flights
bash scripts/search-flights.sh LHR DXB 2025-12-15 2025-12-20 usd 5

# Hotels
bash scripts/search-hotels.sh "Dubai" 2025-12-15 2025-12-18 usd 10

# Cars
bash scripts/search-cars.sh "Dubai Airport" 2025-12-15 2025-12-18
```

### Python CLI

```bash
# Install package locally
python3 -m pip install .

# Search flights
zim flights LHR DXB 2026-04-15 --return-date 2026-04-20 --cabin business

# Search hotels
zim hotels Dubai 2026-04-15 2026-04-20 --stars-min 4

# Search cars
zim cars "Dubai Airport" 2026-04-15 2026-04-20 --car-class suv

# Assemble full itinerary
zim trip LHR DXB 2026-04-15 --return-date 2026-04-20 --mode business --human
```

## WhatsApp Conversational Agent

When handling travel messages on the **WhatsApp channel**, use the Zim WhatsApp agent for a smoother conversational experience with stateful multi-turn flows (search → select → confirm → book).

### How to invoke

```bash
bash /home/ubuntu/.openclaw/workspace/zim/scripts/zim-wa.sh "<user message>" "whatsapp:<user_phone>"
```

This returns JSON: `{"response": "...", "success": true/false}`

Send the `response` text back to the user on WhatsApp.

### Conversation flow

The WhatsApp agent maintains state per user automatically:
1. User sends a natural language travel request → agent returns search results
2. User replies with 1, 2, or 3 → agent shows selection summary, asks YES/NO
3. User says YES → agent returns booking confirmation + deeplink
4. User says CANCEL at any point → resets to fresh search

State persists across calls via SQLite, so multi-message conversations work.

### When to use the WhatsApp agent vs direct CLI

- **WhatsApp channel messages** → use the WhatsApp agent (`zim-wa.sh`)
- **Structured agent-to-agent requests** → use the Python CLI (`zim flights`, `zim hotels`)
- **Quick searches for non-chat contexts** → use shell scripts (`search-flights.sh`)

## Agent workflow

### Parse into a structured travel object

Extract as many of these fields as possible:

**Core trip fields**
- traveler name / profile
- mode: `business` or `personal`
- origin city / airport
- destination city / airport
- departure date
- return date
- trip purpose
- total budget or category budgets

**Flight fields**
- cabin class
- direct only vs flexible
- airline preferences
- refundability / flexibility
- preferred departure window
- no red-eye preference

**Hotel fields**
- hotel style: luxury / boutique / business / budget
- star minimum
- nightly cap
- neighborhood / landmark / meeting proximity
- chain preference

**Car fields**
- pickup location
- dropoff location if different
- car type / class
- provider preference

**Policy / workflow fields**
- approval threshold
- vendor restrictions
- class restrictions
- location radius rule
- whether the agent is allowed to auto-book vs recommend only

If key fields are missing, ask only for the minimum needed to continue.

Convert city names to IATA codes before flight search where needed. Common defaults:
- London → LHR
- Dubai → DXB
- New York → JFK
- Paris → CDG
- Singapore → SIN
- Tokyo → HND/NRT

Convert dates to `YYYY-MM-DD`.

### Business vs personal mode

Apply ranking differently by mode.

**Business mode**
- prioritize direct flights
- prefer refundable / flexible fares when possible
- keep hotels near the meeting area / business district
- enforce policy caps before presenting results
- optimize for time, reliability, and compliance over small savings

**Personal mode**
- prioritize price/value unless preferences override
- allow more creative routing
- surface boutique / character-rich stays when relevant
- optimize for experience and fit

### Running searches

Use the Python CLI when you want structured JSON for agent consumption. Use shell scripts when you want simple direct output and live deeplinks.

## Assemble an itinerary, not disconnected results

Default behavior is to combine flight + hotel + car into a coherent recommendation when the request implies a trip.

Preferred response structure:
1. Trip summary
2. Recommended flight
3. Recommended hotel
4. Recommended car (if relevant)
5. Why this is the best fit
6. Action state — booking-ready / approval-needed / missing info

## Presenting results

### Flights
- If structured results exist, list airline / route / price / dates / deeplink
- If exact-date results are unavailable, say so clearly and provide nearby cached fare context plus a live Aviasales search link

### Hotels
- Present as live hotel search options or structured Python results depending on tool path used
- Explain relevance: proximity, style, business suitability, or value

### Cars
- Present comparison links or structured Python results depending on tool path used
- If a car class or airport pickup was requested, say so explicitly

## Approval and state handling

When total cost exceeds threshold or any item is out of policy, say approval is required.

When payment has not been started, say so.
When payment link/session exists, say so.
When provider execution is still placeholder/manual, say so.

## Preference memory

Surface recurring preferences as durable travel preferences when relevant:
- preferred airlines
- seat preference
- no red-eye
- hotel style
- hotel star floor
- car class

## Error handling

- If `TRAVELPAYOUTS_TOKEN` is not set, explain that affiliate-linked flight/hotel search cannot run.
- If `STRIPE_SECRET_KEY` is not set, explain that checkout session creation cannot run.
- If exact flight results are empty, use nearby cached fares plus a live Aviasales link.
- If hotel APIs are unreliable, prefer working deeplinks over fake structured listings.
- If an external API errors, report it plainly and preserve working manual paths.

## References

Read these only when needed:

- API details and deeplink formats: `references/api-guide.md`
- Booking model / truthfulness guidance: `references/agent-to-agent-booking.md`
