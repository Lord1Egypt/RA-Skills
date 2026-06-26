# Ticket Price Compare - Multi-Platform Ticket Price Comparison

[![Version](https://img.shields.io/badge/Version-v1.2.6-blue)]()
[![Skill Type](https://img.shields.io/badge/Type-AI%20Skill-blue)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

> Real-time multi-platform flight and train ticket price comparison Skill. Supports domestic/international routes, 12306 real-time seat availability, Firecrawl-powered detailed flight data, no API key required for core features.

## Highlights

- **Firecrawl-Powered Flight Data** - Renders Ctrip JS pages via Firecrawl, gets detailed flight numbers, times, aircraft types, and prices
- **Real-Time Train Seat Availability** - Direct 12306 public endpoint, returns actual schedules, seats, and fares
- **Zero Configuration Core** - 12306 train queries work out of the box; Firecrawl enhances flight data when API key is set
- **Multi-Source Flight Comparison** - Firecrawl / Ctrip scraping / Tequila / Amadeus multiple data sources
- **Domestic + International Routes** - Supports both Chinese and English city names
- **Platform Search Links** - One-click access to Ctrip, Qunar, Fliggy, Tongcheng, Skyscanner, Google Flights, etc.
- **Airline Official Sites** - Covers 10 Chinese + 13 international airlines
- **WeChat Mini Program Links** - Mini program search tips for convenient mobile search
- **Discount Condition Alerts** - Auto-lists student tickets, child tickets, refund/change rules

## Data Sources

| Data Source | Type | API Key Required | Description |
|-------------|------|:--------------:|-------------|
| **Firecrawl + Ctrip** | JS Rendering | Optional | Renders Ctrip flight pages, gets individual flight numbers, times, aircraft types, and prices. Set `FIRECRAWL_API_KEY` to enable. Register at [firecrawl.dev](https://firecrawl.dev) |
| 12306 | Public API | No | Real-time train seat availability and fares |
| Ctrip Scraping | Direct HTTP | No | Basic flight info without JS rendering (limited data) |
| Tequila | REST API | Optional | Kiwi.com flight data (registration closed) |
| Amadeus | REST API | Optional | Global flight data (registration closed) |

## What's New in v1.2.0

- **Firecrawl Integration** - Added `FirecrawlScraper` class that uses Firecrawl's `/v2/scrape` API to render Ctrip's JavaScript-heavy flight search pages, extracting detailed flight data (flight numbers, departure/arrival times, aircraft types, individual cabin prices, transfer details)
- **Dual-Source Flight Scraping** - PC page (primary) returns per-flight details; mobile H5 page (fallback) returns price calendar with daily lowest prices
- **Smart Parsing** - Robust markdown parser extracts structured flight data from Ctrip's rendered output, handling various cabin classes and transfer flights
- **Proxy Optimization** - Switched from `proxy: "auto"` to `proxy: "basic"` for better reliability with Chinese booking sites
- **Enhanced Train Prices** - 12306 `queryTicketPrice` endpoint integration for actual fare data per seat type

## Quick Start (Zero Config)

The script uses only Python standard library, no extra packages needed. Train tickets (12306) work out of the box:

```bash
python scripts/ticket_search.py Beijing Guangzhou 2026-05-01 train
```

Flight search also works without any API key (provides platform links for manual comparison):

```bash
python scripts/ticket_search.py Beijing Guangzhou 2026-05-01 flight
```

> **Tip**: To get detailed flight prices (flight numbers, times, aircraft types) instead of just links, set the `FIRECRAWL_API_KEY` environment variable. See [API Key Setup Guide](#api-key-setup-guide) below.

## API Key Setup Guide

All API keys are **optional**. The script works without any configuration (train data always available, flight links always provided). API keys only enhance the flight data quality.

### Key Required vs Optional Summary

| API Key | Required? | What It Enables | Registration Status |
|---------|:---------:|----------------|---------------------|
| `FIRECRAWL_API_KEY` | **Recommended** | Detailed Ctrip flight data (flight numbers, times, aircraft, prices) | **Open** - Free tier available |
| `TEQUILA_API_KEY` | No | Kiwi.com international flight data | **Closed** |
| `AMADEUS_CLIENT_ID` + `AMADEUS_CLIENT_SECRET` | No | Amadeus global flight data | **Closed** |

---

### 1. Firecrawl API Key (Recommended - Free Tier Available)

Firecrawl renders Ctrip's JavaScript-heavy flight pages, extracting detailed flight data that direct HTTP requests cannot get.

#### Step 1: Register

1. Go to [https://firecrawl.dev](https://firecrawl.dev)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with Google/GitHub/email
4. Free tier includes **500 credits/month** (each scrape = 1 credit)

#### Step 2: Get Your API Key

1. After login, go to the **Dashboard**
2. Copy your **API Key** (format: `fc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

#### Step 3: Set Environment Variable

**Linux / macOS** (temporary, current session only):
```bash
export FIRECRAWL_API_KEY="fc-your-actual-api-key-here"
```

**Linux / macOS** (permanent, add to `~/.bashrc` or `~/.zshrc`):
```bash
echo 'export FIRECRAWL_API_KEY="fc-your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows CMD** (temporary, current window only):
```cmd
set FIRECRAWL_API_KEY=fc-your-actual-api-key-here
```

**Windows CMD** (permanent, system-level):
```cmd
setx FIRECRAWL_API_KEY "fc-your-actual-api-key-here"
```
> Note: `setx` takes effect in **new** terminal windows, not the current one.

**Windows PowerShell** (temporary, current session only):
```powershell
$env:FIRECRAWL_API_KEY = "fc-your-actual-api-key-here"
```

**Windows PowerShell** (permanent, user-level):
```powershell
[Environment]::SetEnvironmentVariable("FIRECRAWL_API_KEY", "fc-your-actual-api-key-here", "User")
```
> Note: Takes effect in **new** PowerShell sessions.

#### Step 4: Verify

```bash
python scripts/ticket_search.py Beijing Shanghai 2026-05-01 flight
```
If you see `Data Source: Ctrip (via Firecrawl)` in the output, the key is working.

> **No pip install needed** - the script calls Firecrawl's REST API directly via Python's built-in `urllib` library.

---

### 2. Tequila API Key (Optional - Registration Closed)

Kiwi.com Tequila API for international flight data. **Self-service registration is no longer available.**

If you already have a key:

**Linux / macOS:**
```bash
export TEQUILA_API_KEY="your-tequila-api-key"
```

**Windows CMD:**
```cmd
set TEQUILA_API_KEY=your-tequila-api-key
```

**Windows PowerShell:**
```powershell
$env:TEQUILA_API_KEY = "your-tequila-api-key"
```

---

### 3. Amadeus API Keys (Optional - Registration Closed)

Amadeus API for global flight data. **Self-service registration is closed.**

If you already have keys, you also need to install the SDK:

```bash
pip install amadeus>=12.0.0
```

Then set both environment variables:

**Linux / macOS:**
```bash
export AMADEUS_CLIENT_ID="your-client-id"
export AMADEUS_CLIENT_SECRET="your-client-secret"
```

**Windows CMD:**
```cmd
set AMADEUS_CLIENT_ID=your-client-id
set AMADEUS_CLIENT_SECRET=your-client-secret
```

**Windows PowerShell:**
```powershell
$env:AMADEUS_CLIENT_ID = "your-client-id"
$env:AMADEUS_CLIENT_SECRET = "your-client-secret"
```

---

### Environment Variable Quick Reference

| Variable | Where to Get | Format | Required? |
|----------|-------------|--------|:---------:|
| `FIRECRAWL_API_KEY` | [firecrawl.dev](https://firecrawl.dev) Dashboard | `fc-xxxx...` | Recommended |
| `TEQUILA_API_KEY` | Kiwi.com (closed) | String | No |
| `AMADEUS_CLIENT_ID` | Amadeus (closed) | String | No |
| `AMADEUS_CLIENT_SECRET` | Amadeus (closed) | String | No |

> **Note**: Environment variables set via `export`/`set`/`$env:` are session-only and will be lost when you close the terminal. Use `setx` (Windows) or add to `~/.bashrc` (Linux/macOS) for persistence.

## Usage

### Train Ticket Search

```bash
python scripts/ticket_search.py Beijing Guangzhou 2026-04-20 train
```

### Flight Ticket Search

```bash
python scripts/ticket_search.py Beijing Guangzhou 2026-04-20 flight
```

### Combined Search (Flight + Train)

```bash
python scripts/ticket_search.py Beijing Guangzhou 2026-04-20 all
```

### International Routes

```bash
python scripts/ticket_search.py Shanghai Tokyo 2026-06-15 flight
python scripts/ticket_search.py Shanghai Tokyo 2026-06-15 all
```

## Output Examples

### Flight Ticket Output (with Firecrawl)

```
=== Flight Search Results ===
Departure: Beijing  Arrival: Shanghai  Date: 2026-04-25
Data Source: Ctrip (via Firecrawl)

Flight     Airline         Aircraft      Depart  Arrive    Price
CA1501     Air China       Boeing 737    07:30   09:45     CNY 520
MU5101     China Eastern   Airbus A320   08:00   10:20     CNY 480
CZ6901     China Southern  Airbus A321   09:00   11:15     CNY 460
...

Platform Search Links:
- Ctrip: https://flights.ctrip.com/...
- Qunar: https://flight.qunar.com/...
- Skyscanner: https://www.skyscanner.net/...
```

### Train Ticket Output

```
=== 12306 Real-Time Query Results ===
Departure: Beijing  Arrival: Guangzhou  Date: 2026-04-20

Train    Departure->Arrival       Time          Duration  Second Class  First Class
G303     Beijing Xi->Guangzhou South  10:00-17:17   7:17     CNY 1033     CNY 1488
D923     Beijing Xi->Guangzhou South  20:22-06:47   10:25    CNY 709      -
Z13      Beijing Fengtai->Guangzhou Baiyun  14:25-12:36+1  22:11   -   CNY 251 (Hard Sleeper)
```

## Project Structure

```
ticket-price-compare/
+-- SKILL.md                        # Skill definition (triggers, workflow)
+-- README.md                       # This file
+-- .gitignore
+-- references/
|   +-- platforms_guide.md          # Detailed per-platform discount conditions
+-- scripts/
    +-- ticket_search.py            # Core search script (~2200 lines)
    +-- requirements.txt            # Dependencies (core has zero dependencies)
    +-- skyscanner_lib/             # Skyscanner affiliate link builder
```

## Technical Details

- **Core Zero Dependencies** - `ticket_search.py` uses only Python standard library (`urllib`, `json`, `ssl`)
- **Firecrawl JS Rendering** - Calls Firecrawl `/v2/scrape` API with `waitFor: 15000ms` and `proxy: "basic"` to render Ctrip's React-based flight search pages, then parses the resulting markdown
- **Dual-Source Ctrip** - PC page (`flights.ctrip.com`) for per-flight details; mobile H5 (`m.ctrip.com`) for price calendar fallback
- **12306 Endpoints** - Uses `leftTicket/queryZ` for schedules + `queryTicketPrice` for actual fares, no login required
- **City Name Mapping** - Built-in 200+ Chinese city/station name to IATA/telegraph code mapping
- **SSL Security** - All connections use full TLS verification. 12306 endpoints never bypass SSL — if certificate verification fails, train data is unavailable for that request but all other features (flight search, platform links) still work.
- **Encoding Compatibility** - Auto-handles Windows console UTF-8 encoding issues

## Flight Data Source Priority

1. **Firecrawl + Ctrip PC** (if `FIRECRAWL_API_KEY` set) - Best quality: individual flights, times, aircraft, prices
2. **Firecrawl + Ctrip Mobile** (fallback) - Price calendar with daily lowest prices
3. **Direct Ctrip Scraping** (no API key) - Limited data, may not work due to JS rendering
4. **Tequila API** (if key set) - International flights
5. **Amadeus API** (if keys set) - Global flights
6. **Platform Links Only** - If no data source returns prices, provides direct links for manual search

## As an AI Skill

This Skill can be used on AI skill platforms such as CodeBuddy / ClawHub. It auto-triggers when users ask:

- "Find me flights from Beijing to Guangzhou"
- "How much is Shanghai to Tokyo on April 20"
- "Check train ticket seat availability"
- "Which platform has the cheapest flights"
- "What student ticket discounts are available"

## License

MIT
