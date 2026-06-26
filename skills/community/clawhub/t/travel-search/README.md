# ✈️ travel-search

**The most complete free travel search skill for OpenClaw and AI agents.**

Search flights, hotels, car rentals, and ferries across multiple providers — all free, no API keys required. Real-time pricing with direct booking links.

[![ClawHub](https://img.shields.io/badge/ClawHub-travel--search-blue)](https://clawhub.ai/adrianetti/travel-search)

## Features

🛫 **Flights** — Search across Kiwi.com and Skiplagged with creative routing, hidden city fares, and flexible dates

🏨 **Hotels** — Compare prices across booking sites via Skiplagged and Trivago

🏠 **Airbnb** — Compare apartments and homes against hotels for the same stay (optional local MCP)

🚗 **Car Rentals** — Find the best deals via Skiplagged

⛴️ **Ferries** — Search 190+ operators across 33 countries via Ferryhopper

✈️ **Google Flights** — Widest airline coverage via `fli` (optional, local install)

## Why This Skill?

- **100% free** — No API keys, no registration, no paid tiers
- **Real-time data** — Live prices from actual providers, not cached or estimated
- **Direct booking links** — Every result includes a link to book immediately
- **Multi-provider** — Cross-reference prices across providers automatically
- **Modular** — Only loads what you need (flights, hotels, etc.)

## Install

```bash
openclaw skills install travel-search
```

Or clone directly:

```bash
git clone https://github.com/adrianetti/travel-search.git
cp -r travel-search ~/.openclaw/workspace/skills/
```

## Providers

| Provider | Type | Coverage | API Key |
|----------|------|----------|---------|
| [Kiwi.com](https://kiwi.com) | Flights | Worldwide, creative routing | 🆓 Free |
| [Skiplagged](https://skiplagged.com) | Flights + Hotels + Cars | Worldwide, hidden city fares | 🆓 Free |
| [Trivago](https://trivago.com) | Hotels | Worldwide, price comparison | 🆓 Free |
| [Airbnb MCP](https://github.com/borski/mcp-server-airbnb) | Apartments / homes | Short stays, groups, workcations | 🆓 Free (separate install required) |
| [Ferryhopper](https://ferryhopper.com) | Ferries | 33 countries, 190+ operators | 🆓 Free |
| [Google Flights](https://github.com/punitarani/fli) | Flights | Widest coverage | 🆓 Free (separate install required) |

All providers use the [MCP protocol](https://modelcontextprotocol.io/) (JSON-RPC 2.0 over HTTP) — no browser automation, no scraping.

## Usage Examples

Once installed, just ask your agent naturally:

- *"Find me cheap flights from Madrid to Tokyo in April"*
- *"Compare hotels in Rome for April 10-14"*
- *"What’s cheaper, Airbnb or hotel in Barcelona for 5 nights?"*
- *"Find the best apartment stay in Lisbon for a month"*
- *"What's the cheapest way to get from Oviedo to Rome?"*
- *"Find car rentals in Barcelona for next week"*
- *"Search ferries from Piraeus to Santorini in July"*
- *"Where can I fly cheap from Madrid?"* (uses Skiplagged's "anywhere" search)
- *"When is it cheapest to fly to London?"* (flexible date calendar)
- *"Plan me a 5-day trip to Rome with a budget of €800"* (full itinerary with prices)
- *"Build an itinerary for 2 weeks in Japan"* (day-by-day plan + flights + hotels)
- *"I want to visit Rome, Paris, and Amsterdam in 10 days — what's the best route?"*
- *"Eurotrip: 5 cities in 3 weeks, optimize for cheapest flights"*

## How It Works

The skill teaches AI agents to call travel provider MCP servers directly via `curl`. Each provider returns structured JSON with prices, routes, times, and booking links. The agent then formats and presents the best options.

```
User: "Find flights from Barcelona to Rome"
  → Agent loads references/flights.md
  → Calls Kiwi.com MCP API
  → Gets JSON with 15 flights, prices, deep links
  → Presents top 3-5 options grouped by cheapest/fastest/best value
```

## Skill Structure

```
travel-search/
├── SKILL.md                         # Core skill + decision guide
├── references/
│   ├── flights.md                   # Kiwi.com API docs
│   ├── skiplagged.md                # Skiplagged API docs  
│   ├── hotels.md                    # Trivago API docs
│   ├── airbnb.md                    # Airbnb MCP docs
│   ├── ferries.md                   # Ferryhopper API docs
│   └── google-flights.md            # fli / Google Flights docs
├── scripts/
│   └── mcp-call.sh                  # Helper script for MCP calls
└── ROADMAP.md                       # Upcoming features
```

## Roadmap

- **v1.1** ✅ — Trip Planner (full itinerary: flight + hotel + day-by-day + budget)
- **v1.2** ✅ — Smart Price & Value Engine (cross-provider comparison, value scoring, price calendars, deal detection)
- **v1.3** ✅ — Airbnb Integration (short-stay vs hotel comparison)
- **v1.4** ✅ — Multi-city Optimizer (cheapest route, day allocation, open-jaw, train alternatives)
- **v1.5** ✅ — Travel Intel (weather, visa, currency, transport, safety, connectivity)

See [ROADMAP.md](ROADMAP.md) for details.

## Contributing

PRs welcome! Especially for:
- New free travel provider integrations
- Improved API documentation
- Bug fixes and edge cases
- Translation of SKILL.md descriptions

## License

MIT
