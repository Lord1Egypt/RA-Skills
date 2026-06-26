---
name: ticket-price-compare
version: 1.2.6
description: This skill should be used when the user wants to compare and search for flight or train ticket prices across multiple platforms. It supports both domestic (China) and international routes, fetches real-time train availability via 12306, uses Firecrawl to render Ctrip JS pages for detailed flight data (flight numbers, times, aircraft types, prices), generates direct search links for all major booking platforms and airline official websites, provides WeChat mini program quick links for mobile search, and highlights discount conditions. Trigger scenarios include: searching for cheap flights, comparing train ticket prices, finding international flight deals, looking for the best ticket booking platform, or asking about ticket discount conditions.
environment_variables:
  - name: FIRECRAWL_API_KEY
    required: false
    description: "Firecrawl API key for JS rendering of Ctrip flight pages. Register at firecrawl.dev. Free tier available (500 credits/month)."
  - name: TEQUILA_API_KEY
    required: false
    description: "Kiwi.com Tequila API key for international flight data. Self-service registration is closed."
  - name: AMADEUS_CLIENT_ID
    required: false
    description: "Amadeus API client ID. Self-service registration is closed."
  - name: AMADEUS_CLIENT_SECRET
    required: false
    description: "Amadeus API client secret. Self-service registration is closed."
network_access:
  - domain: kyfw.12306.cn
    purpose: "12306 train schedule & fare queries (public API, no auth)"
  - domain: flights.ctrip.com
    purpose: "Ctrip PC flight search page (scraping / Firecrawl JS rendering)"
  - domain: m.ctrip.com
    purpose: "Ctrip mobile H5 flight page (Firecrawl fallback for price calendar)"
  - domain: flight.qunar.com
    purpose: "Qunar flight search page (link generation)"
  - domain: api.firecrawl.dev
    purpose: "Firecrawl /v2/scrape API for JS rendering (optional, requires FIRECRAWL_API_KEY)"
  - domain: api.tequila.kiwi.com
    purpose: "Kiwi.com Tequila flight search API (optional, requires TEQUILA_API_KEY)"
  - domain: api.amadeus.com
    purpose: "Amadeus production API (optional, requires AMADEUS credentials)"
  - domain: test.api.amadeus.com
    purpose: "Amadeus test API (optional, for development)"
---

# Ticket Price Compare - Multi-Platform Ticket Price Comparison

## Overview

This skill enables real-time comparison of flight and train ticket prices. It fetches **real-time train availability** via 12306 (no API key needed), and uses **Firecrawl to render Ctrip JS pages** for detailed flight data when `FIRECRAWL_API_KEY` is set. It also generates direct search links for all major booking platforms and **WeChat mini program quick links** for convenient mobile search. Tequila/Amadeus APIs are available as optional fallbacks for users who already have keys. Discount conditions and restrictions are clearly listed separately.

## Data Sources

### Firecrawl + Ctrip (Primary for Flight Data, Optional API Key)
- Uses Firecrawl's `/v2/scrape` API to render Ctrip's JavaScript-heavy flight search pages
- **PC page** (primary): Returns individual flight numbers, times, aircraft types, and prices
- **Mobile H5 page** (fallback): Returns price calendar with daily lowest prices across dates
- Requires `FIRECRAWL_API_KEY` environment variable. Register at [firecrawl.dev](https://firecrawl.dev)
- Falls back gracefully to direct scraping if not configured

### Ctrip Direct Scraping (No API Key Needed)
- Attempts direct HTTP request to Ctrip flight search pages
- **No registration or API key required** - works out of the box
- Limited data: Ctrip renders pages via JavaScript, so direct scraping may not always return prices. In that case, platform links are provided for manual search.

### 12306 (Train Tickets, No API Key Needed)
- Uses 12306 public `leftTicket/queryZ` endpoint for real-time train availability
- Uses 12306 public `queryTicketPrice` endpoint for actual fares per seat type
- Supports major Chinese cities with station code auto-mapping

### Optional APIs (For Existing Key Holders Only)
- **Kiwi.com Tequila API**: If `TEQUILA_API_KEY` is set (registration may no longer be available)
- **Amadeus API**: If `AMADEUS_CLIENT_ID` + `AMADEUS_CLIENT_SECRET` are set (registration is closed)
- These are used as fallbacks only when web scraping returns no results

## Core Capabilities

### 1. Flight Ticket Search

```bash
python scripts/ticket_search.py "<departure>" "<arrival>" "<date>" flight
```
- Domestic: `python scripts/ticket_search.py "Beijing" "Shanghai" "2026-05-01" flight`
- International: `python scripts/ticket_search.py "Shanghai" "Tokyo" "2026-06-15" flight`

**Data sources (in order of priority)**:
1. Firecrawl + Ctrip PC page (if `FIRECRAWL_API_KEY` set) - Best quality: individual flights, times, aircraft, prices
2. Firecrawl + Ctrip Mobile H5 (fallback) - Price calendar with daily lowest prices
3. Ctrip Direct Scraping (no API key, limited data)
4. Tequila API (if API key configured)
5. Amadeus API (if API keys configured)

**Covered domestic platforms**: Ctrip, Qunar, Fliggy, Tongcheng, Tuniu

**Covered international platforms**: Skyscanner, Google Flights, Kayak, Momondo, Expedia, Booking.com

**Covered airline official sites**: 10 Chinese + 13 international airlines

### 2. Train Ticket Search with Real-Time Availability

```bash
python scripts/ticket_search.py "<departure>" "<arrival>" "<date>" train
```

**Real-time data from 12306**: Returns actual train schedules with:
- Train code & type (High-Speed/EMU/Express/Fast)
- Departure/arrival stations & times
- Duration
- Available seat types & counts (Business Class/First Class/Second Class/Hard Sleeper/Hard Seat etc.)
- Actual fares per seat type

### 3. Combined Search (Flight + Train)

```bash
python scripts/ticket_search.py "<departure>" "<arrival>" "<date>" all
```

Train results are automatically excluded for international routes.

## Output Sections

The script generates structured output with these sections (in order):

1. **Route Summary** - Departure, arrival, date, route type
2. **Data Source Status** - Whether Firecrawl/scraping/APIs returned live data
3. **Real-Time Flight Prices** - Table of flight offers with prices (if available)
4. **Transfer Details** - Multi-segment flight details (if any transfers)
5. **Flight Discount Conditions** - Refund/change rules, baggage limits, cabin restrictions
6. **Real-Time Train Info** - Table of actual trains with seat availability and fares (if domestic)
7. **Train Discount Conditions** - Student tickets, child tickets, change rules
8. **Platform Links** - Direct search URLs for all booking platforms
9. **Airline Official Sites** - Direct links to airline websites
10. **WeChat Mini Program Quick Links** - Mobile H5 links + WeChat mini program search tips for Ctrip/Fliggy/Tongcheng/Qunar and major airlines
11. **Search Tips** - Route-specific advice

### Discount Conditions

Always include the dedicated "Discount Conditions / Restrictions" section. Reference `references/platforms_guide.md` for detailed per-platform discount conditions. Load this file when:
- User asks about specific discount conditions
- Presenting results that include discounted fares
- User asks which platform has the best deals for their situation

## Workflow

1. **Collect query parameters**: Get departure city, arrival city, and travel date. If date not specified, ask. Default ticket type to "all".

2. **Execute search**: Run `scripts/ticket_search.py` with the parameters.

3. **Present results**: Show the **complete output** from the script. **IMPORTANT**: Do NOT summarize or omit train ticket price information. Always include:
   - **Train ticket prices** - The "票价（余票）" column contains actual fares like `二等座¥305(有) / 一等座¥488(12)`. This is real-time pricing data from 12306 and MUST be shown to the user.
   - **Flight prices** (if available from Firecrawl, scraping, or API)
   - All platform links for comparison
   - Discount conditions section
   - Search tips

4. **If no flight prices returned**: Inform the user that real-time flight prices could not be fetched automatically, and recommend clicking the platform links to compare prices manually. **Always mention that 12306 train data with real-time prices is available for domestic routes.**

5. **When user asks for "all" or combined search**: Present train results and flight results side by side. Do NOT skip or truncate the train price table even when flight data is extensive.

## Date Flexibility

If a user asks for "cheapest dates" or "price trends":
- Run the script with multiple date parameters to compare
- For domestic flights: Also suggest Ctrip/Qunar price calendar features
- For international flights: Suggest Skyscanner "cheapest month" or Google Flights date grid

## Important Notes

- **Primary method**: Firecrawl + Ctrip (if API key set) - renders JS pages, gets detailed flight data
- **Fallback scraping**: Direct Ctrip HTTP request - no API key needed, but limited data due to JS rendering
- **Fallback APIs**: Tequila/Amadeus - only for users who already have keys; registration is closed for new users
- **Without any flight data**: Platform search links are always provided (users click to see prices)
- **12306 train data** is always real-time (no API key needed)
- **SSL verification**: All connections use full TLS verification. 12306 endpoints never bypass SSL — if certificate verification fails, train data is unavailable for that request but all other features (flight search, platform links) still work.
- **Firecrawl proxy**: Uses `proxy: "basic"` for optimal reliability with Chinese booking sites
- Prices vary in real-time; recommend checking 2-3 platforms for confirmation
- Airline official websites sometimes offer exclusive prices not available on OTA platforms
- Always remind users about potential discount conditions before booking
