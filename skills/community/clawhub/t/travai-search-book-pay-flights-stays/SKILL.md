---
name: TravAI
description: Search flights and stays, then create card or crypto payments via TravAI. Use when the user asks about flights, travel planning, booking trips, finding accommodation, or travel inspiration.
---

# TravAI

Use this skill when the user wants to search travel options or book a flight/stay through TravAI.

## Source of truth

If this skill conflicts with backend behavior, check the live OpenAPI schema:
```
https://api.travai.tech/openapi.json
```
Follow the live schema over this doc.

## Critical notes

- Search responses return `search_id` (not `search_hash`)
- Payment requests use `method` (`"CRYPTO"` or `"CARD"`) — not `type`
- Searches and offers **expire**; if any request fails with "not found" or `EXPIRED_OFFER`, re-run the search and use fresh IDs
- **Offer IDs are unique per search** — after re-running a search, you MUST use the new `offer_id` values from the new results; old offer IDs will not work with the new `search_id`
- For crypto payments, always return the **exact** amount, token, deposit address, and refund wallet — never round
- **Changes and cancellations** are not available via the API — direct users to support: https://t.me/travaiofficial or support@travai.tech

---

## API base

```
https://api.travai.tech
```

## Authentication

All endpoints (except sign-in and sign-up) require:

```
Authorization: Bearer {access_token}
```

Three ways to authenticate:

1. **Sign up** — new user
2. **Sign in** — returning user
3. **Paste token** — user copies from [https://app.travai.tech/profile](https://app.travai.tech/profile)

### Sign In

```
POST /auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secret"
}
```

Response (200):

```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### Sign Up

```
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secret",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

Response (200):

```json
{
  "message": "User created successfully",
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### Get current user

```
GET /auth/me
Authorization: Bearer {access_token}
```

Response (200):

```json
{
  "user_id": 1,
  "email": "user@example.com",
  "role": "customer",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00",
  "currency": "USD"
}
```

### Error responses

Any failed request may return:

```json
{ "detail": "Human-readable error description" }
```

Always check for `detail` in non-2xx responses and surface the message to the user.

---

## Endpoints

### Search flights

```
POST /searches
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "type": "FLIGHT",
  "origin_iata": "LON",
  "destination_iata": "LIS",
  "departure_date": "2025-10-10",
  "return_date": "2025-10-17",
  "customers": [
    { "type": "ADULT" },
    { "type": "CHILD", "age": 10 }
  ]
}
```

| Field | Required | Notes |
|---|---|---|
| `type` | yes | `"FLIGHT"` |
| `origin_iata` | yes | 3-letter IATA code (uppercase, e.g. `"LON"`) |
| `destination_iata` | yes | 3-letter IATA code (uppercase, e.g. `"LIS"`) |
| `departure_date` | yes | `YYYY-MM-DD` |
| `return_date` | no | omit for one-way |
| `customers` | yes | array of `CustomerAge` (see below) |

**`CustomerAge` object:**

| Field | Required | Notes |
|---|---|---|
| `type` | no (default: `ADULT`) | `ADULT`, `CHILD`, `SENIOR`, `HELD_INFANT` |
| `age` | required for `CHILD` and `HELD_INFANT` | integer |

Customer type rules:
- `HELD_INFANT` — under 2 years old
- `CHILD` — between 2 and 18 years old
- `ADULT` — default
- `SENIOR` — senior traveller

Response (200):

```json
{
  "search_id": "abc123",
  "total_offers": 42,
  "best_offers": [ /* top 3 offers */ ]
}
```

| Field | Description |
|---|---|
| `search_id` | Identifier for this search — use in all subsequent calls |
| `total_offers` | Total number of offers matching the search |
| `best_offers` | The 3 best offers (sorted by price/quality) |

**Direct-flight filtering:** To find direct flights, only keep offers where the total segment count across all slices equals the number of slices (i.e. 1 segment per slice = no stops).

### Search stays

```
POST /searches
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "type": "STAY",
  "location_anchor": {
    "value": "Abu Dhabi",
    "type": "city"
  },
  "check_in_date": "2026-03-05",
  "check_out_date": "2026-03-10",
  "rooms": 1,
  "guests": 1,
  "radius_km": 50
}
```

| Field | Required | Default | Notes |
|---|---|---|---|
| `type` | yes | — | `"STAY"` |
| `location_anchor` | yes | — | see `StaysSearchAnchor` below |
| `check_in_date` | yes | — | `YYYY-MM-DD` |
| `check_out_date` | yes | — | `YYYY-MM-DD` |
| `rooms` | no | `1` | 1–8 |
| `guests` | no | `1` | number of adult guests |
| `radius_km` | no | `50` | search radius in km around the anchor |

**`StaysSearchAnchor` object:**

| Field | Required | Description |
|---|---|---|
| `value` | yes | Reference point text, e.g. `"Milano"`, `"London center"`, `"LHR"` |
| `type` | yes | One of: `airport`, `city`, `city_center`, `region`, `address`, `place`, `others` |

Anchor type guide:
- `airport` — 3-letter IATA code (e.g. `"LHR"`)
- `city` — city name (e.g. `"Abu Dhabi"`)
- `city_center` — city centre / downtown (e.g. `"London center"`)
- `region` — neighbourhood / district (e.g. `"Manhattan"`)
- `address` — street address (e.g. `"Via G.B. Pioda 10"`)
- `place` — landmark / point of interest (e.g. `"Parque Edgar Sampaio Fontes"`)
- `others` — anything else

Response (200):

```json
{
  "search_id": "def456",
  "total_offers": 15,
  "best_offers": [ /* top 3 offers */ ]
}
```

| Field | Description |
|---|---|
| `search_id` | Identifier for this search — use in all subsequent calls |
| `total_offers` | Total number of offers matching the search |
| `best_offers` | The 3 best offers |

### List offers

```
GET /searches/{search_id}/offers?limit=20&offset=0
Authorization: Bearer {access_token}
```

| Parameter | Required | Default | Description |
|---|---|---|---|
| `search_id` | yes (path) | — | `search_id` from `POST /searches` |
| `limit` | no (query) | `20` | Max offers to return (1–200) |
| `offset` | no (query) | `0` | Offset for pagination |

Response (200):

```json
{
  "total_offers": 42,
  "offers": [ /* paginated list of offer summaries */ ]
}
```

| Field | Description |
|---|---|
| `total_offers` | Total number of offers for this search |
| `offers` | Paginated slice of offer summaries |

### Get single offer

```
GET /searches/{search_id}/offers/{offer_id}
Authorization: Bearer {access_token}
```

Response (200): a single offer summary object.

### Offer pricing (flights)

```
GET /searches/{search_id}/offers/{offer_id}/pricing
Authorization: Bearer {access_token}
```

| Path parameter | Description |
|---|---|
| `search_id` | `search_id` from `POST /searches` |
| `offer_id` | Offer ID from `best_offers` or the paginated offers list |

Response (200): a flat offer summary dict with full pricing details (final price, segments, airlines, etc.).

Error (410): returns `{ "detail": "EXPIRED_OFFER" }` if the offer is no longer available. When this happens, inform the user and re-run the search.

### Hotel rates

```
GET /searches/{search_id}/offers/{offer_id}/rates
Authorization: Bearer {access_token}
```

| Path parameter | Description |
|---|---|
| `search_id` | `search_id` from `POST /searches` |
| `offer_id` | Hotel offer ID from `best_offers` or the paginated offers list |

Response (200): a list of room objects, each containing room details (name, description, size, max occupancy, photos, beds) and nested `rates` array with pricing, payment type, and cancellation conditions.

### Rate pricing (stays)

```
GET /searches/{search_id}/offers/{offer_id}/rates/{rate_id}/pricing
Authorization: Bearer {access_token}
```

| Path parameter | Description |
|---|---|
| `search_id` | `search_id` from `POST /searches` |
| `offer_id` | Hotel offer ID |
| `rate_id` | Rate ID from the rates list |

Response (200): a stay summary with full pricing details (total amount, currency, accommodation info, room breakdown).

Error (410): returns `{ "detail": "EXPIRED_OFFER" }` if the rate is no longer available. When this happens, inform the user and re-run the search.

### Hotel photo gallery

```
GET /searches/{search_id}/offers/{offer_id}/photos
```

No authentication required. Returns an interactive HTML photo gallery for the hotel.

| Path parameter | Description |
|---|---|
| `search_id` | `search_id` from `POST /searches` |
| `offer_id` | Hotel offer ID |

**How to present to the user:** Build the full gallery URL and share it as a clickable link:

```
https://api.travai.tech/searches/{search_id}/offers/{offer_id}/photos
```

Do **not** share individual photo URLs from the API response — they are CDN-signed and will not load in the browser. Always use the gallery link instead.

The gallery features keyboard navigation (arrow keys), click-to-advance, and a thumbnail strip.

Individual photos can also be accessed at `/searches/{search_id}/offers/{offer_id}/photos/{index}` (0-based) if needed for embedding.

### List tokens

```
GET /tokens
Authorization: Bearer {access_token}
```

Response (200): a flat list of supported crypto tokens. Each item represents one asset on one blockchain.

```json
[
  { "assetId": "nep141:wrap.near", "blockchain": "NEAR", "symbol": "NEAR" },
  { "assetId": "nep141:usdc.near", "blockchain": "NEAR", "symbol": "USDC" },
  { "assetId": "eth:0xabc...", "blockchain": "Ethereum", "symbol": "USDC" }
]
```

| Field | Description |
|---|---|
| `assetId` | Token identifier — use as `origin_asset` in a CRYPTO payment |
| `blockchain` | Blockchain network the token lives on |
| `symbol` | Token symbol (e.g. `"NEAR"`, `"USDC"`) |

**Token selection guidance:**
- **Group by `blockchain`** when presenting to the user
- Prefer **stablecoins** (USDC, USDT) for payment unless the user requests otherwise
- When user asks for a specific token/network, match by `symbol` + `blockchain`
- Always confirm the exact `assetId` before proceeding

After the user picks a token, ask for their wallet address on that token's `blockchain` to use as `refund_to`.

### Initiate payment

```
POST /payments
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Payment methods:** `CRYPTO` or `CARD`. Use the `method` field (not `type`).

#### CRYPTO payment

```json
{
  "method": "CRYPTO",
  "origin_asset": "{assetId from GET /tokens}",
  "refund_to": "{user wallet address}",
  "offers": [ /* see offer object below */ ]
}
```

| Field | Required | Description |
|---|---|---|
| `method` | yes | `"CRYPTO"` |
| `origin_asset` | yes | `assetId` of the token selected by the user from `GET /tokens` |
| `refund_to` | yes | User's wallet address on the selected token's network — refunds go here in the same currency |
| `offers` | yes | Selected offers to pay for |

Response (200):

```json
{
  "payment_id": 123,
  "itinerary_id": 456,
  "deposit_address": "travai.near",
  "amount_in": "1000000",
  "amount_in_formatted": "1.00",
  "total_amount": 100,
  "currency": "USD"
}
```

| Field | Description |
|---|---|
| `payment_id` | Payment identifier (use to check status via `GET /payments/{payment_id}`) |
| `itinerary_id` | Itinerary identifier (use to get confirmations via `GET /itineraries/{itinerary_id}/offers`) |
| `deposit_address` | Address to send tokens to |
| `amount_in_formatted` | **Exact** amount of tokens to send — must match exactly, do not round |
| `amount_in` | Raw token amount (integer string) |
| `total_amount` | Fiat equivalent in smallest unit (cents) |
| `currency` | ISO currency code (e.g. `"USD"`) |

#### CARD payment

```json
{
  "method": "CARD",
  "success_url": "https://app.travai.tech/?payment=success",
  "cancel_url": "https://app.travai.tech/?payment=cancel",
  "offers": [ /* see offer object below */ ]
}
```

| Field | Required | Description |
|---|---|---|
| `method` | yes | `"CARD"` |
| `success_url` | yes | Always `"https://app.travai.tech/?payment=success"` |
| `cancel_url` | yes | Always `"https://app.travai.tech/?payment=cancel"` |
| `offers` | yes | Selected offers to pay for |

Response (200):

```json
{
  "payment_id": 123,
  "itinerary_id": 456,
  "payment_url": "https://checkout.stripe.com/...",
  "total_amount": 100,
  "currency": "USD"
}
```

| Field | Description |
|---|---|
| `payment_id` | Payment identifier (use to check status via `GET /payments/{payment_id}`) |
| `itinerary_id` | Itinerary identifier (use to get confirmations via `GET /itineraries/{itinerary_id}/offers`) |
| `payment_url` | URL for the user to complete card payment |
| `total_amount` | Amount in smallest currency unit (cents) |
| `currency` | ISO currency code (e.g. `"USD"`) |

### Get payment status

```
GET /payments/{payment_id}
Authorization: Bearer {access_token}
```

| Path parameter | Description |
|---|---|
| `payment_id` | Payment ID from the `POST /payments` response |

Response (200): full payment record including `status`, `fiat_amount`, `fiat_currency`, `token_amount`, `token_asset`, `created_at`, `updated_at`.

Payment statuses: `PENDING`, `PENDING_DEPOSIT`, `INCOMPLETE_DEPOSIT`, `KNOWN_DEPOSIT_TX`, `PROCESSING`, `SUCCESS`, `REFUNDED`, `FAILED`, `ERROR`.

### Get itinerary offers

```
GET /itineraries/{itinerary_id}/offers
Authorization: Bearer {access_token}
```

| Path parameter | Description |
|---|---|
| `itinerary_id` | Itinerary ID from the `POST /payments` response |

Response (200): list of itinerary offer items, each with `itinerary_offer_id`, `type`, `provider`, `price`, `currency`, `status`, `booking_summary`, `created_at`.

### Offer object (inside `offers` array in payment request)

```json
{
  "type": "FLIGHT",
  "search_id": "abc123",
  "offer_id": "offer_xyz",
  "customers": [
    {
      "email": "jane@example.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "date_of_birth": "1989-04-23",
      "gender": "FEMALE",
      "nationality": "UA",
      "country_code": "380",
      "phone_number": "632816433",
      "title": "MS"
    }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `type` | yes | `"FLIGHT"` or `"STAY"` |
| `search_id` | yes | `search_id` from the search step |
| `offer_id` | yes (FLIGHT) | Offer ID from the search results |
| `rate_id` | yes (STAY) | Rate ID from the hotel rates step |
| `customers` | yes | Traveller details (see below) |

### Customer object (inside offer `customers` array)

| Field | Required | Example |
|---|---|---|
| `first_name` | yes | `Jane` |
| `last_name` | yes | `Doe` |
| `title` | yes | `MR`, `MRS`, `MS`, `DR` |
| `gender` | yes | `MALE` or `FEMALE` |
| `date_of_birth` | yes | `1989-04-23` (YYYY-MM-DD) |
| `nationality` | yes | `UA`, `GB`, `US` (ISO 3166-1 alpha-2) |
| `country_code` | yes | `380` (phone country code, no `+`) |
| `phone_number` | yes | `632816433` (without country code) |
| `email` | yes | `jane@example.com` |

**IMPORTANT:** `first_name`, `last_name`, and `date_of_birth` must exactly match the traveller's international passport. Always remind the user of this before collecting their details.

---

## Workflow checklists

### Flight booking checklist

1. **Authenticate** — sign in, sign up, or accept a pasted token
2. **Gather details** — origin, destination, dates, passengers
3. **Search** — `POST /searches` with `type: "FLIGHT"`
4. **Present best offers** — show price, airlines, stops, duration
5. **Filter if needed** — e.g. direct flights only (1 segment per slice)
6. **Confirm pricing** — `GET /searches/{search_id}/offers/{offer_id}/pricing`
7. **Handle expiry** — if 410, re-run search and start from step 3
8. **Collect traveller details** — warn about passport matching first
9. **Choose payment method** — crypto or card
10. **If crypto** — `GET /tokens`, present grouped by blockchain (prefer stablecoins), collect wallet address for refund
11. **Create payment** — `POST /payments` with `method` field
12. **Present payment instructions:**
    - Crypto: exact `amount_in_formatted` + token + `deposit_address` + refund wallet
    - Card: full untruncated `payment_url`
13. **Check status if asked** — `GET /payments/{payment_id}`

### Stay booking checklist

1. **Authenticate** — sign in, sign up, or accept a pasted token
2. **Gather details** — destination, check-in/out dates, rooms, guests
3. **Search** — `POST /searches` with `type: "STAY"`
4. **Present best offers** — show property name, price per night, rating, distance. Share the photo gallery link: `https://api.travai.tech/searches/{search_id}/offers/{offer_id}/photos` — do NOT share raw photo URLs
5. **Get rates** — immediately `GET /searches/{search_id}/offers/{offer_id}/rates` when user picks a hotel
6. **Present rates** — room type, price, amenities, cancellation policy
7. **Confirm pricing** — immediately `GET .../rates/{rate_id}/pricing` when user picks a rate
8. **Handle expiry** — if 410, re-run search and start from step 3
9. **Collect traveller details** — warn about passport matching first
10. **Choose payment method** — crypto or card
11. **Create payment** — include `rate_id` in offer object, use `method` field
12. **Present payment instructions** (same as flight)
13. **Check status if asked** — `GET /payments/{payment_id}`

---

## Nearby Airports Database

Many cities are served by multiple airports. Always check this mapping before searching — run parallel searches for all relevant airports and compare results.

If a city is not listed below but the user mentions a country or region, use your knowledge of IATA codes to identify all relevant airports.

### Europe — Western

| City / Country | Airports (IATA) |
|---|---|
| London / UK | LHR, LGW, STN, LTN, LCY |
| Manchester / UK | MAN, LPL (Liverpool, 1h) |
| Edinburgh / UK | EDI, GLA (Glasgow, 1h) |
| Paris / France | CDG, ORY, BVA |
| Nice / France | NCE |
| Lyon / France | LYS |
| Amsterdam / Netherlands | AMS, EIN (Eindhoven), RTM (Rotterdam) |
| Brussels / Belgium | BRU, CRL (Charleroi) |
| Berlin / Germany | BER |
| Frankfurt / Germany | FRA, HHN (Hahn) |
| Munich / Germany | MUC, NUE (Nuremberg, nearby) |
| Düsseldorf / Germany | DUS, CGN (Cologne, 1h), DTM (Dortmund) |
| Hamburg / Germany | HAM |
| Zurich / Switzerland | ZRH, BSL (Basel), BRN (Bern) |
| Geneva / Switzerland | GVA |
| Vienna / Austria | VIE, BTS (Bratislava, 80km) |
| Dublin / Ireland | DUB, SNN (Shannon), ORK (Cork) |

### Europe — Southern

| City / Country | Airports (IATA) |
|---|---|
| Milan / Italy | MXP, LIN, BGY (Bergamo) |
| Rome / Italy | FCO, CIA (Ciampino) |
| Naples / Italy | NAP |
| Venice / Italy | VCE, TSF (Treviso) |
| Florence / Italy | FLR, PSA (Pisa, 1h) |
| Bologna / Italy | BLQ |
| Catania / Sicily | CTA, PMO (Palermo) |
| Madrid / Spain | MAD |
| Barcelona / Spain | BCN, GRO (Girona), REU (Reus) |
| Malaga / Spain | AGP |
| Valencia / Spain | VLC |
| Seville / Spain | SVQ |
| Alicante / Spain | ALC |
| Palma de Mallorca / Spain | PMI |
| Lisbon / Portugal | LIS |
| Porto / Portugal | OPO |
| Athens / Greece | ATH |
| Thessaloniki / Greece | SKG |
| Istanbul / Turkey | IST, SAW (Sabiha Gökçen) |
| Antalya / Turkey | AYT |

### Europe — Northern

| City / Country | Airports (IATA) |
|---|---|
| Stockholm / Sweden | ARN, BMA, NYO (Skavsta), VST (Västerås) |
| Copenhagen / Denmark | CPH, BLL (Billund), AAR (Aarhus) |
| Oslo / Norway | OSL, TRF (Torp), RYG (Rygge) |
| Helsinki / Finland | HEL, TMP (Tampere) |
| Reykjavik / Iceland | KEF, RKV |

### Europe — Eastern & Central

| City / Country | Airports (IATA) |
|---|---|
| Prague / Czech Republic | PRG |
| Warsaw / Poland | WAW, WMI (Modlin) |
| Krakow / Poland | KRK |
| Gdansk / Poland | GDN |
| Wroclaw / Poland | WRO |
| Budapest / Hungary | BUD |
| Bucharest / Romania | OTP, BBU (Băneasa) |
| Sofia / Bulgaria | SOF |
| Kyiv / Ukraine | KBP, IEV (Zhuliany) |
| Belgrade / Serbia | BEG |
| Zagreb / Croatia | ZAG |
| Split / Croatia | SPU |
| Dubrovnik / Croatia | DBV |
| Riga / Latvia | RIX |
| Vilnius / Lithuania | VNO |
| Tallinn / Estonia | TLL |
| Bratislava / Slovakia | BTS, VIE (Vienna, 60km) |

### Middle East

| City / Country | Airports (IATA) |
|---|---|
| Dubai / UAE | DXB, DWC (Al Maktoum) |
| Abu Dhabi / UAE | AUH |
| Doha / Qatar | DOH |
| Riyadh / Saudi Arabia | RUH |
| Jeddah / Saudi Arabia | JED |
| Muscat / Oman | MCT |
| Bahrain | BAH |
| Kuwait | KWI |
| Amman / Jordan | AMM |
| Tel Aviv / Israel | TLV |
| Beirut / Lebanon | BEY |
| Cairo / Egypt | CAI |
| Sharm El Sheikh / Egypt | SSH |
| Hurghada / Egypt | HRG |

### Asia — East

| City / Country | Airports (IATA) |
|---|---|
| Tokyo / Japan | NRT (Narita), HND (Haneda) |
| Osaka / Japan | KIX (Kansai), ITM (Itami) |
| Seoul / South Korea | ICN (Incheon), GMP (Gimpo) |
| Beijing / China | PEK (Capital), PKX (Daxing) |
| Shanghai / China | PVG (Pudong), SHA (Hongqiao) |
| Guangzhou / China | CAN |
| Shenzhen / China | SZX |
| Hong Kong | HKG |
| Taipei / Taiwan | TPE (Taoyuan), TSA (Songshan) |

### Asia — Southeast

| City / Country | Airports (IATA) |
|---|---|
| Bangkok / Thailand | BKK (Suvarnabhumi), DMK (Don Mueang) |
| Phuket / Thailand | HKT |
| Chiang Mai / Thailand | CNX |
| Singapore | SIN |
| Kuala Lumpur / Malaysia | KUL, SZB (Sultan Abdul Aziz Shah) |
| Jakarta / Indonesia | CGK (Soekarno-Hatta) |
| Bali / Indonesia | DPS |
| Manila / Philippines | MNL |
| Ho Chi Minh City / Vietnam | SGN |
| Hanoi / Vietnam | HAN |
| Phnom Penh / Cambodia | PNH |
| Siem Reap / Cambodia | REP |
| Yangon / Myanmar | RGN |

### Asia — South & Central

| City / Country | Airports (IATA) |
|---|---|
| Delhi / India | DEL |
| Mumbai / India | BOM |
| Bangalore / India | BLR |
| Colombo / Sri Lanka | CMB |
| Maldives | MLE |
| Kathmandu / Nepal | KTM |
| Almaty / Kazakhstan | ALA |
| Tbilisi / Georgia | TBS |
| Yerevan / Armenia | EVN |
| Baku / Azerbaijan | GYD |
| Tashkent / Uzbekistan | TAS |

### Africa

| City / Country | Airports (IATA) |
|---|---|
| Johannesburg / South Africa | JNB, HLA (Lanseria) |
| Cape Town / South Africa | CPT |
| Nairobi / Kenya | NBO |
| Addis Ababa / Ethiopia | ADD |
| Casablanca / Morocco | CMN |
| Marrakech / Morocco | RAK |
| Tunis / Tunisia | TUN |
| Lagos / Nigeria | LOS |
| Accra / Ghana | ACC |
| Dar es Salaam / Tanzania | DAR |
| Zanzibar / Tanzania | ZNZ |
| Mauritius | MRU |

### North America

| City / Country | Airports (IATA) |
|---|---|
| New York / USA | JFK, EWR (Newark), LGA (LaGuardia) |
| Los Angeles / USA | LAX, BUR (Burbank), LGB (Long Beach), ONT, SNA (Orange County) |
| San Francisco / USA | SFO, OAK (Oakland), SJC (San Jose) |
| Chicago / USA | ORD (O'Hare), MDW (Midway) |
| Miami / USA | MIA, FLL (Fort Lauderdale), PBI (West Palm Beach) |
| Washington DC / USA | IAD (Dulles), DCA (Reagan), BWI (Baltimore) |
| Dallas / USA | DFW, DAL (Love Field) |
| Houston / USA | IAH, HOU (Hobby) |
| Boston / USA | BOS |
| Seattle / USA | SEA |
| Atlanta / USA | ATL |
| Denver / USA | DEN |
| Las Vegas / USA | LAS |
| Honolulu / USA | HNL |
| Toronto / Canada | YYZ, YTZ (Billy Bishop) |
| Montreal / Canada | YUL |
| Vancouver / Canada | YVR |
| Mexico City / Mexico | MEX, NLU (Felipe Ángeles) |
| Cancun / Mexico | CUN |

### South America

| City / Country | Airports (IATA) |
|---|---|
| São Paulo / Brazil | GRU (Guarulhos), CGH (Congonhas), VCP (Campinas) |
| Rio de Janeiro / Brazil | GIG (Galeão), SDU (Santos Dumont) |
| Buenos Aires / Argentina | EZE (Ezeiza), AEP (Aeroparque) |
| Santiago / Chile | SCL |
| Lima / Peru | LIM |
| Bogota / Colombia | BOG |
| Medellin / Colombia | MDE, EOH (Olaya Herrera) |
| Cartagena / Colombia | CTG |

### Oceania

| City / Country | Airports (IATA) |
|---|---|
| Sydney / Australia | SYD |
| Melbourne / Australia | MEL, AVV (Avalon) |
| Brisbane / Australia | BNE |
| Perth / Australia | PER |
| Auckland / New Zealand | AKL |
| Queenstown / New Zealand | ZQN |
| Fiji | NAN |

---

## Smart Flight Search Strategy

This is the core of intelligent search. Always follow this protocol.

### Step 1 — Identify all relevant airports

Before searching, check the Nearby Airports Database for both origin and destination. If the city has multiple airports, plan parallel searches.

**Example:** User says "London to Milan" — search LHR->MXP, LHR->LIN, LHR->BGY, LGW->MXP, LGW->LIN, LGW->BGY, STN->MXP, STN->BGY in parallel. Surface cheapest overall.

### Step 2 — Run parallel searches

Always launch multiple searches simultaneously using parallel tool calls:
- All relevant airport combinations
- If flexible dates: target date +/-1 day (+/-2 days if user explicitly flexible)

**Flexible date matrix example** (+/-1 day, 1 origin, 1 destination = 3 searches):
- departure_date - 1 day
- departure_date (requested)
- departure_date + 1 day

If user says they are flexible or "around that date", go +/-2 days (5 searches).

### Step 3 — Analyse and surface best options

After collecting all results:
1. Find the **cheapest overall** across all airport/date combinations — highlight it
2. Find the **fastest** (fewest stops, shortest duration) — highlight separately
3. Find the **best value** (price + duration balanced)
4. Flag anything unusual: next-day arrival, very long layover (>4h), overnight layover, short layover (<60min — warn about connection risk)

### Step 4 — Auto-fallback if 0 results

If a search returns 0 offers:
1. Immediately try adjacent dates (+/-1 day) without asking the user
2. Try nearby airports automatically
3. Only if all fallbacks return 0, inform the user and suggest alternatives

### Step 5 — Proactively ask about flexibility

After showing results, if prices are high (>$300 for short-haul, >$700 for medium-haul), proactively say:
> "Prices on this date are on the higher side. Would you like me to check +/-1-2 days to find a cheaper option?"

---

## Human Travel Agent Behaviours

Act like an experienced travel agent, not a search engine.

### Always flag these automatically (without being asked):
- **Next-day arrival**: "Note: this flight arrives on April 18th, not April 17th — overnight layover in Copenhagen."
- **Short layover (<60 min)**: "Warning: 45-min connection in Frankfurt is very tight — any delay on the first leg could cause a miss."
- **Baggage not included**: "No bags included — adding checked baggage will increase the price."
- **Non-refundable**: "This ticket is non-refundable and non-changeable."
- **Instant payment required**: "This fare requires immediate payment — price may not be held."
- **Train might be better**: For routes under 500-600 km where the total door-to-door time by train competes with flying (e.g. Paris-Brussels, Berlin-Amsterdam, London-Paris), proactively mention: "For this route, a train might be faster and more convenient door-to-door — though I can only book flights here."

### Presentation style:
- Lead with the **cheapest** option and mark it clearly
- Show a **"best overall"** pick that balances price, duration, and convenience — with a brief reason why
- When showing a connecting flight with a bad layover city, note it naturally: "This goes via Oslo — a bit of a detour, but it's the cheapest same-day option."
- Use conversational language alongside tables. E.g.: "I found 174 flights — here are the 3 worth looking at:"
- If the user's requested date has no good options, proactively show the best option on adjacent dates even if not asked

### When searching multi-city / complex itineraries:
- Break the trip into segments and search each independently in parallel
- Consider departure airports for return legs — e.g. if user ends in Maastricht, check BRU, EIN, AMS for return
- Always note which airport the return departs from — it may require travel time

### Price intelligence:
- If the same route shows wildly different prices across dates (e.g. Friday vs Tuesday), proactively mention: "Tuesday departures are significantly cheaper on this route — worth considering if you have flexibility."
- If baggage fees would make a "cheap" fare more expensive than a higher-priced fare with bags included, flag it: "Adding a bag to the $89 fare would bring it to ~$140 — the $125 Lufthansa fare with bags included may actually be better value."

---

## Flight Results Display Format

### 1. Header

Always start with a header containing route, dates, passengers, and total offers found.

**Template:**
```
## [City] [IATA] -> [City] [IATA] | [Departure date] - [Return date] | [N] adults
Found [X] offers. Here are the best:
```

### 2. Result Groups

All results are divided into three groups in strict order:

**Group 1 — Cheapest**
Header: `### Cheapest`
- 3-5 offers with lowest price, sorted ascending
- If same price — pick shortest total travel time

**Group 2 — Fastest**
Header: `### Fastest`
- 3 offers with shortest total duration (outbound + return)
- Even if already in "cheapest" — show here separately
- Sorted by duration ascending

**Group 3 — Other options**
Header: `### Other options`
- 2-3 interesting offers not in groups above
- E.g. different airline, different departure airport, good price/time balance

### 3. Table Format

**Round trip:**

| Route out | Departure -> Arrival (duration) | Class | Route back | Departure -> Arrival (duration) | Class | Price |
|---|---|---|---|---|---|---|

**One way:**

| Route | Departure -> Arrival (duration) | Class | Price |
|---|---|---|---|

**Column rules:**

**Route (out / back):**
- Format: City IATA -> City IATA (with city name next to each code)
- Include layovers in the chain
- If direct — mark "(direct)"
- Examples: `Bangkok BKK -> Kuala Lumpur KUL -> Singapore SIN`, `Amsterdam AMS -> Barcelona BCN (direct)`

**Departure -> Arrival (duration):**
- Date format: dd/mm
- Time format: hh:mm (local time)
- Duration: Xh Ym (segment duration only, not total)
- If arrival next day — add `+1` after arrival time and include arrival date
- Normal example: `06/10 06:00 -> 11:25 (4h 25m)`
- Next day example: `06/10 23:00 -> 06/11 03:30 +1 (4h 30m)`

**Class:** Economy / Business / First

**Price:**
- With currency sign: $330.60 or EUR 298
- Lowest price in group — bold
- "Best pick" offer — mark as best pick before price

### 4. Caption Under Table

After each table — one italic line with key details.

**Key info to include per offer:**
- Airline name
- Baggage included / not included
- Refundable / non-refundable
- Changes allowed / not allowed
- Short connection warning (under 60 min)
- Long layover warning (over 6h)
- Direct flight indicator
- Layover city

**Caption template:**
```
*[Airline] · baggage included · non-refundable · ...*
```

**Next-day arrival — always use `+1`:**
- `+1` goes right after arrival time in table cell
- Always include arrival date next to it
- Example: `05/11 23:25 -> 05/12 06:25 +1`

### 5. Summary Block

After all tables — a summary block with:

**5.1 Cheapest**
```
Cheapest: [Airline] — [price]. [pros]. But: [cons].
```

**5.2 Best pick**
A reasoned recommendation — not always the cheapest. Consider: direct vs layover, refund, baggage, price difference.
```
Best pick: [Airline], [route] — [price] ([difference] more). [conditions]. [One-sentence rationale].
```

**5.3 Warnings (if any)**
Each warning — separate line. Must mention:
- Next-day arrival
- Short connection
- Long layover
- Baggage not included in cheap fares
- Departure from different airport

**5.4 Call to action**
Last line — always offer to proceed to booking:
```
Want to book? Name your preferred option and I'll request exact pricing and details.
```

### 6. Language

Always respond in the language the user is writing in. The structure stays the same regardless of language.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| 422 `method` field required | Sent `type` instead of `method` in payment request | Use `"method": "CRYPTO"` or `"method": "CARD"` |
| `Search ... not found` | Search expired or invalid `search_id` | Re-run `POST /searches` and use fresh `search_id` |
| 404 `Offer ... not found in search` | Offer ID from a different/old search | Re-run search and use `offer_id` values from the new results |
| 410 `EXPIRED_OFFER` | Offer or rate is no longer available | Re-run search, pick a fresh offer, then retry |
| 422 on signup | Sent `name` instead of `first_name`/`last_name` | Use separate `first_name` and `last_name` fields |
| Unsupported token | Token/chain mismatch | Call `GET /tokens` and pick a valid `assetId` |
| Redirect loop on POST | Trailing-slash routing issue | Ensure POST goes to `/payments` (no trailing slash) |

---

## Changes and cancellations

Booking changes and cancellations **cannot** be done via the API. The user must contact support directly:

- **Telegram:** https://t.me/travaiofficial
- **Email:** support@travai.tech

Response time: within 24 hours.

When a user asks to change or cancel a booking, do not attempt any API calls — instead, direct them to one of the support channels above.

---

## Support

For any technical issues, questions, or problems with the API:

- **Telegram:** https://t.me/travaiofficial
- **Email:** support@travai.tech

We will reply within 24 hours.

---

## Tips

- Always authenticate before making API calls
- Always check the Nearby Airports Database before searching — run parallel searches for all relevant airports
- If the user gives flexible dates or "around that time", search +/-2 days automatically
- If a search returns 0 results, auto-retry with adjacent dates and nearby airports before telling the user
- Present flight offers sorted by price, but always highlight a "best overall" pick with a brief reason
- For round trips, always include both departure and return dates
- For stays, present offers highlighting price per night, rating, and proximity to the city centre
- When the user's intent is ambiguous, ask whether they need a flight, a stay, or both
- Always flag next-day arrivals, overnight layovers, short connections, and missing baggage proactively
- For short-haul routes (<600km), mention the train option even though TravAI can't book it
- For crypto payments, present the deposit info clearly and warn not to round amounts or substitute tokens
