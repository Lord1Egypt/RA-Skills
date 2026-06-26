# Zim API Integration Guide

## Travelpayouts / Aviasales

Base documentation: https://support.travelpayouts.com/hc/en-us/categories/200358578

### Flight Search — Prices for Dates

```
GET https://api.travelpayouts.com/aviasales/v3/prices_for_dates
```

| Param | Required | Description |
|---|---|---|
| `origin` | Yes | IATA code (e.g. LHR) |
| `destination` | Yes | IATA code (e.g. DXB) |
| `departure_at` | Yes | YYYY-MM-DD |
| `return_at` | No | YYYY-MM-DD |
| `currency` | No | Default: usd |
| `limit` | No | Max results (default 10) |
| `sorting` | No | price (default), route, distance_unit_price |
| `token` | Yes | TRAVELPAYOUTS_TOKEN |

Response fields:
- `data[].origin`, `data[].destination` — IATA codes
- `data[].departure_at`, `data[].return_at` — ISO datetime
- `data[].price` — integer price in specified currency
- `data[].airline` — 2-letter airline IATA code
- `data[].flight_number` — flight number
- `data[].transfers` — number of stops
- `data[].link` — partial deeplink path

### Flight Search — Cheap Prices

```
GET https://api.travelpayouts.com/v1/prices/cheap
```

| Param | Required | Description |
|---|---|---|
| `origin` | Yes | IATA code |
| `destination` | Yes | IATA code |
| `depart_date` | No | YYYY-MM |
| `return_date` | No | YYYY-MM |
| `currency` | No | Default: rub |
| `token` | Yes | TRAVELPAYOUTS_TOKEN |

### Flight Deeplinks

Format:
```
https://www.aviasales.com/search/{ORIGIN}{DEST}{DDMM}1?marker={TOKEN}
```

Example for LHR→DXB on Dec 15 with return Dec 20:
```
https://www.aviasales.com/search/LHR1512DXB20121?marker=YOUR_TOKEN
```

Full deeplink with flight link from API:
```
https://www.aviasales.com{link}&marker={TOKEN}
```

### Airline IATA Codes

Map 2-letter codes to names using:
```
GET https://api.travelpayouts.com/data/en/airlines.json
```

---

## Hotels

The legacy `engine.hotellook.com/api/v2/*` endpoints are unreliable / returning 404 in current testing.
For this skill, use live deeplink search flows instead of pretending we have stable structured hotel API results.

### Primary hotel deeplink

```
https://search.hotellook.com/hotels?destination={city}&checkIn={YYYY-MM-DD}&checkOut={YYYY-MM-DD}&marker={TOKEN}&currency={currency}
```

### Backup links

```text
Booking.com:
https://www.booking.com/searchresults.html?ss={city}&checkin={YYYY-MM-DD}&checkout={YYYY-MM-DD}&selected_currency={CURRENCY}

Google Hotels:
https://www.google.com/travel/hotels/{city}?checkin={YYYY-MM-DD}&checkout={YYYY-MM-DD}&curr={CURRENCY}
```

### Important note

Hotel results in this skill currently return live search links rather than structured hotel listings. This is deliberate: better to provide reliable working deeplinks than broken or misleading API output.

---

## Car Rentals

Travelpayouts does not have a dedicated car rental API. Fallback approach:

### Kayak Affiliate Links

```
https://www.kayak.com/cars/{location}/{pickup_date}/{return_date}?a=openclaw
```

Date format: YYYY-MM-DD

### Discover Cars Affiliate

```
https://www.discovercars.com/search?location={location}&pickup={date}&dropoff={date}&marker={TOKEN}
```

### Rentalcars.com Affiliate

```
https://www.rentalcars.com/search?location={location}&driversAge=30&puDay={DD}&puMonth={MM}&puYear={YYYY}&doDay={DD}&doMonth={MM}&doYear={YYYY}
```

---

## Rate Limits

- Travelpayouts: ~200 requests/minute per token
- Hotellook: ~100 requests/minute per token
- Cache endpoints return cached data (may be up to 48h old)
- For real-time prices, users should click deeplinks to see live pricing on provider sites

## Affiliate Tracking

**Critical:** ALL deeplinks must include the `marker` parameter set to `TRAVELPAYOUTS_TOKEN` for commission tracking. Without the marker, clicks are not attributed and no commission is earned.
