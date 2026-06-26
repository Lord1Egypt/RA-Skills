# openclaw-skill-uexcorp-sc

⭐ Advanced OpenClaw/ShibaClaw skill for Star Citizen trade data and market management via UEXcorp API.

## What it does

This skill transforms your agent into a professional Star Citizen trade advisor, leveraging the [UEXcorp](https://uexcorp.space) community database to maximize your profits.

### 📈 Market Intelligence
- 💰 **Live Prices**: Query commodity buy/sell prices by terminal or globally.
- ⛏️ **Mining Data**: Track raw material prices and find the best selling points for ores/gases.
- 🛸 **Logistics**: Get ship/vehicle cargo capacities and purchase prices.
- 🪐 **Navigation**: Map terminals, planets, moons, and star systems.
- 🗺️ **Route Optimization**: Generate the most profitable trade routes based on your ship's capacity.

### 🚀 Advanced Features
- 🖼️ **Image-to-Post**: Upload a photo of an item; the agent identifies it, researches the current lowest market prices, and helps you create a listing.
- 📤 **Market Contribution**: Update the community database with live prices you find in-game.
- 📝 **Trade Postings**: Create WTS (Want to Sell) or WTB (Want to Buy) listings directly via the API.
- � **Post-Trade Analysis**: Calculate net profit, margin percentages, and trade efficiency (profit per SCU/hour).

## Installation

1. Copy the `SKILL.md` file into your OpenClaw/ShibaClaw skills folder:
   - OpenClaw: `~/.openclaw/skills/uexcorp-sc/SKILL.md`
   - ShibaClaw: `<workspace>/skills/uexcorp-sc/SKILL.md`

2. Get your API token at [uexcorp.space/api/apps](https://uexcorp.space/api/apps)

3. Add your token to your config:
```json
{
  "skills": {
    "entries": {
      "uexcorp-sc": {
        "apiToken": "YOUR_TOKEN_HERE"
      }
    }
  }
}
```

4. Restart your agent session and you're good to go 🚀

## Example prompts

**Market Research:**
- *"What's the price of Laranite at Lorville?"*
- *"Where is the cheapest place to buy Quantanium right now?"*
- *"Best trade route from ArcCorp with a C2 Hercules?"*

**Trading & Listings:**
- *(Upload Image)* $\rightarrow$ *"I want to sell this. Find the lowest prices and post it for me."*
- *"I'm selling 100 units of Gold at New Babbage for 600cr, create a trade post."*

**Analysis & Contribution:**
- *"I just sold 500 SCU of Titanium for 200cr each, bought at 120cr. How much profit did I make?"*
- *"The price of Gold in Lorville is now 550cr, please update the database."*

## Data source

All data is community-sourced via [UEXcorp API 2.0](https://uexcorp.space/api/documentation/). 
*Note: Prices may slightly differ from live in-game values.*

## License

MIT