# UK Used Car Recommender

Your smart used-car buying advisor for the UK market, specialising in reliable second-hand cars at the right price.

## 🆕 What's New: Data-Driven Recommendations

**Now recommends based on REAL market data, not just AI knowledge!**

When you ask for car recommendations, the skill will:
1. ✅ **Search real listings first** — Find actual cars for sale in your area and budget
2. ✅ **Dual-platform search** — Query both Gumtree + AutoTrader for comprehensive coverage
3. ✅ **Analyze market data** — Check availability, price distribution, typical condition
4. ✅ **Combine with expertise** — Merge reliability knowledge with real market availability
5. ✅ **Show evidence** — Present actual listings as proof of recommendations

**Before (Pure AI Inference):**
> "I recommend a Honda Jazz for £8k - typically reliable, good value"

**Now (Data-Driven + Dual-Platform):**
> "Searched London market across Gumtree + AutoTrader: Found 57 Honda Jazz listings (23 + 34), avg £8,980. Price validated across platforms. Best value-for-money with strong availability. Here are 5 actual examples currently for sale..."

**New: AutoTrader Integration**
- 🆕 Support for AutoTrader UK (Britain's largest car marketplace)
- 🆕 Dual-platform search for comprehensive market coverage
- 🆕 Cross-platform price validation
- 🆕 More accurate pricing and detailed vehicle information

See [docs/DATA_DRIVEN_RECOMMENDATION.md](docs/DATA_DRIVEN_RECOMMENDATION.md) and [docs/AUTOTRADER_INTEGRATION.md](docs/AUTOTRADER_INTEGRATION.md) for full details.

---

## Features

### 🔥 Core Capabilities

- **🎯 Data-Driven Recommendations** — Search real market listings FIRST, then recommend based on actual availability and prices
- **Expert 9-Stage Buying Journey** — Complete guidance from research to ownership
- **Real-Time Market Search** — Integrated Gumtree CLI search for live listings with images
- **AI Photo Analysis** — Verify listing accuracy, identify damage, detect clocking
- **Evidence-Based Advice** — Combine reliability knowledge with real market data

### 📊 Market Intelligence

- Budget-based recommendations with real price data
- **Sales data inference** - Predict popularity and sales speed without API access
- Availability analysis (how many cars actually for sale?)
- Price distribution and value-for-money scoring
- **Market hotness scoring** - Identify trending vs. slow-selling vehicles
- Age/mileage expectations from real listings
- Reliability ratings and common fault warnings

### 🔍 Due Diligence Tools

- MOT history interpretation and red flag detection
- HPI check guidance (outstanding finance, Cat S/N/D)
- Service history assessment
- Approved Used vs Private Sale comparisons
- Insurance group, VED, and ULEZ compliance advice

## Installation

This skill is installed in `~/.cursor/skills/uk-car-recommender/`.

### Dependencies

**All dependencies are now self-contained** — no external code dependencies required!

#### Basic Installation (Gumtree only)

The integrated search CLI requires Python 3.10+ and the following packages:

```bash
pip install -r ~/.cursor/skills/uk-car-recommender/requirements.txt
```

Or using `uv`:

```bash
uv pip install -r ~/.cursor/skills/uk-car-recommender/requirements.txt
```

**Required packages:**
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- lxml>=5.0.0

#### Enhanced Installation (Gumtree + AutoTrader) - RECOMMENDED ⭐

For dual-platform search with better data quality:

```bash
# Install basic dependencies first
pip install -r ~/.cursor/skills/uk-car-recommender/requirements.txt

# Add AutoTrader support
pip install autotrader_scraper
```

**Why install AutoTrader support?**
- ✅ Access to UK's largest car marketplace
- ✅ More accurate pricing and detailed vehicle info
- ✅ Cross-platform price validation
- ✅ Larger selection of vehicles

**Note:** If `autotrader_scraper` is not installed, the skill will automatically fall back to Gumtree-only search. See [docs/AUTOTRADER_INTEGRATION.md](docs/AUTOTRADER_INTEGRATION.md) for details.

**Note:** The `gt_car_search` package and all related modules are now included locally. See `DEPENDENCIES.md` for details on the migration.

## Usage

This skill activates automatically when you mention:
- "used car", "second-hand car", "pre-owned"
- "buy a used car", "best used car"
- "approved used", "nearly new"
- "MOT history", "HPI check", "service history"
- "reliable used cars", "high mileage", "low mileage"
- Any UK car brand with "used" (e.g. "used BMW", "used Toyota")

### Example Queries

**Stage 1-3: Research & Search**
- "I want to buy a used car for commuting, budget £10k"
- "What are the most reliable used SUVs under £15k?"
- "Find me a used Toyota in London under £8k"

**Stage 4-6: Inspection & Purchase**
- "What should I check when viewing a used Golf?"
- "How do I read MOT history?"
- "What's the difference between Cat S and Cat N?"

**Stage 7-8: Post-Purchase**
- "Do I need to tax my used car immediately?"
- "What insurance do I need for a used car?"

## Integrated Gumtree Search & Photo Analysis

When you ask to search Gumtree, the skill will:

1. Ask for your search criteria (or infer from context)
2. Execute live search using the CLI tool
3. Parse and present results in a user-friendly format with **car images** and direct links
4. **Offer AI photo analysis** to verify listing accuracy and identify issues

**Example:**

> "Find me a used Toyota under £10k in London, automatic, 5 years or newer"

The skill will execute:
```bash
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --make toyota \
  --max-price 10000 \
  --location London \
  --transmission automatic \
  --year up_to_5 \
  --sort date \
  --limit 10
```

And present structured results with prices, locations, images, and Gumtree links.

**Photo Analysis (NEW in v3.2):**

After presenting results, you can request:

> "Analyze the photos for listing #2"
> "Check the first car's condition from the images"
> "Does that Toyota look genuine?"

The AI will:
1. Download and analyze listing photos
2. Verify make/model/year/color match advertised details
3. Inspect bodywork, wheels, tyres, interior for damage/wear
4. Compare visible wear to claimed mileage (detect clocking)
5. Flag red flags: rust, accident damage, poor maintenance
6. Provide condition rating (🟢 Acceptable / 🟡 Minor Issues / 🟠 Moderate Concerns / 🔴 Red Flags)
7. Suggest price negotiation leverage or advise to walk away

**What It Checks:**
- Bodywork damage (dents, scratches, rust, resprays)
- Wheel condition (kerb rash, tyre wear, budget tyres)
- Interior wear (steering wheel, seats, dashboard)
- Mileage verification (wear vs claimed mileage)
- Accident signs (panel gaps, misalignment)
- Photo quality/transparency (missing angles = red flag)

## File Structure

```
uk-car-recommender/
├── SKILL.md                    # Main skill instructions (core only)
├── _meta.json                  # Skill metadata & trigger keywords
├── requirements.txt            # Python dependencies for CLI
├── README.md                   # This file
├── DEPENDENCIES.md             # ✅ Dependency migration documentation
├── docs/                       # 📚 Supplementary guides
│   ├── WORKFLOW_GUIDE.md      # Detailed Stage 1-9 buying process
│   ├── GUMTREE_SEARCH.md      # Complete Gumtree CLI guide
│   ├── UK_MARKET_REFERENCE.md # Budget strategies, ULEZ, faults, costs
│   ├── CONVERSATION_GUIDE.md  # Conversation tactics & error handling
│   └── IMAGE_ANALYSIS_GUIDE.md # Photo inspection methodology & red flags
├── gt_car_search/              # 📦 CLI implementation (migrated locally)
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py                 # Main CLI logic
└── scripts/                    # 🛠️ Gumtree CLI tool
    ├── cli.py                 # CLI entry point wrapper
    └── cars/
        ├── __init__.py
        ├── urls.py            # URL builder with filter parameters
        └── scraper.py         # HTML scraper & parser
```

**Progressive Disclosure:** SKILL.md contains core instructions and references detailed guides in `docs/`. The AI reads supplementary files only when needed.

## Supported Search Filters

- **Make/Model**: toyota, bmw, volkswagen, etc.
- **Budget**: --min-price, --max-price (in GBP)
- **Location**: London, Manchester, uk (default)
- **Age**: up_to_3, up_to_5, up_to_10, over_10
- **Mileage**: up_to_30000, up_to_60000, up_to_80000
- **Fuel**: petrol, diesel, electric, hybrid_electric
- **Transmission**: manual, automatic
- **Body Type**: hatchback, suv, saloon, estate, mpv, coupe
- **Seller**: trade (dealer), private
- **Sort**: date, price_lowest_first, mileage_lowest_first

See `scripts/cli.py --help` for complete options.

## Version History

- **v3.2.2** (2026-04-23) — 📦 Migrated all external dependencies locally
  - Copied `gt_car_search` package from external location to skill directory
  - Removed all external path dependencies
  - Created DEPENDENCIES.md to document migration
  - Skill is now fully self-contained and portable
- **v3.2.1** (2026-04-23) — 📁 Optimized directory structure
  - Created `docs/` directory for supplementary guides
  - Moved 5 guide files to `docs/` for cleaner root directory
  - Updated all file references to new paths
  - Clearer separation: core files in root, guides in docs, tools in scripts
- **v3.2.0** (2026-04-23) — 🔍 Added AI-powered photo analysis
  - Created IMAGE_ANALYSIS_GUIDE.md with systematic inspection methodology
  - Verify listing accuracy (make/model/year/color match)
  - Identify bodywork damage, rust, tyre wear, interior condition
  - Detect clocking (mileage tampering) by comparing wear to claims
  - Flag red flags: accident damage, poor maintenance, misrepresentation
  - Provide structured condition reports with negotiation advice
- **v3.1.0** (2026-04-23) — 🖼️ Added image display support
  - Gumtree CLI now extracts car image URLs
  - Search results display primary listing images
  - Updated output format to include visual previews
- **v3.0.0** (2026-04-23) — 🎯 Major refactor: Applied Progressive Disclosure pattern
  - SKILL.md reduced from 413 to 240 lines (-42%)
  - Created 4 supplementary guides: WORKFLOW_GUIDE.md, GUMTREE_SEARCH.md, UK_MARKET_REFERENCE.md, CONVERSATION_GUIDE.md
  - Main skill now contains core instructions only; detailed content loaded on-demand
- **v2.3.0** (2026-04-23) — Simplified Greeting section to eliminate duplication with Stage 1
- **v2.2.0** (2026-04-23) — Renumbered Buying Journey Workflow stages from 1-9 (previously 0-8)
- **v2.1.0** (2026-04-23) — Added Stage 0 (Initial Greeting & Requirements Gathering) to Buying Journey Workflow
- **v2.0.0** (2026-04-20) — Converted to used-car specialist with integrated Gumtree CLI
- **v1.0.0** (2026-04-20) — Initial UK car recommender

## License

MIT-0 (as per ClawHub requirements)
