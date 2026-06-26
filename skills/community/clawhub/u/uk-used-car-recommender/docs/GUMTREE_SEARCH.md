# Gumtree CLI Search Guide

Complete guide for using the integrated Gumtree search CLI to find live used car listings.

## Overview

The skill includes a built-in CLI tool that fetches real-time used car listings from Gumtree, allowing users to search directly from the conversation.

**CLI Location:** `~/.cursor/skills/uk-car-recommender/scripts/cli.py`

**Dependencies:** All dependencies are now local and self-contained:
- `gt_car_search/` - CLI implementation package (migrated locally)
- `scripts/cars/` - Web scraping and URL building modules (local)

**Python Requirements:** Python 3.10+ with:
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- lxml>=5.0.0

(Install with: `pip install -r requirements.txt`)

**Note:** All external dependencies have been migrated to the skill directory. See `DEPENDENCIES.md` for details.

---

## When to Use Gumtree Search

Use the CLI search when:
- User explicitly asks to "search Gumtree"
- User wants to see live listings ("show me actual cars for sale")
- After providing car recommendations, offer to search for real listings
- User has specific criteria ready (budget, location, make/model)

---

## Usage Pattern

### Step 1: Gather Search Criteria

Ask the user or use information from earlier conversation:
- Budget range
- Location (London, Manchester, or "uk" for nationwide)
- Make/Model
- Age preference
- Mileage limit
- Fuel type, transmission, body type
- Seller preference (trade/private)

### Step 2: Map Natural Language to CLI Parameters

| User Says | CLI Parameter | Example Values |
|-----------|--------------|----------------|
| Budget | `--min-price` / `--max-price` | `--max-price 10000` |
| Location | `--location` | `London`, `Manchester`, `uk` |
| Make/Model | `--make` / `--model` | `--make toyota --model yaris` |
| Age | `--year` | `up_to_3`, `up_to_5`, `up_to_10` |
| Mileage | `--mileage` | `up_to_30000`, `up_to_60000`, `up_to_80000` |
| Fuel type | `--fuel-type` | `petrol`, `diesel`, `electric`, `hybrid_electric` |
| Transmission | `--transmission` | `manual`, `automatic` |
| Body type | `--body-type` | `hatchback`, `suv`, `saloon`, `estate`, `mpv` |
| Seller | `--seller-type` | `trade`, `private` |
| Sort | `--sort` | `date`, `price_lowest_first`, `mileage_lowest_first` |

### Step 3: Execute Search Command

```bash
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --make toyota \
  --model yaris \
  --max-price 10000 \
  --location London \
  --year up_to_5 \
  --mileage up_to_60000 \
  --transmission automatic \
  --fuel-type petrol \
  --sort price_lowest_first \
  --limit 10
```

### Step 4: Parse JSON Output

The CLI returns JSON with this structure:

```json
{
  "ok": true,
  "source": "gumtreeDataLayer",
  "search_url": "https://www.gumtree.com/search?...",
  "total_results": 234,
  "total": 10,
  "items": [
    {
      "listing_id": "1512345678",
      "title": "2019 Toyota Yaris 1.5 Hybrid Icon 5dr CVT",
      "price": 9995,
      "price_display": "£9,995",
      "location": "Hackney, London",
      "url": "https://www.gumtree.com/p/toyota/...",
      "age": "3 days",
      "is_trade": true,
      "year": "2019",
      "mileage": "57,000 miles",
      "fuel_type": "Petrol",
      "engine_size": "1,496 cc",
      "seller_type_display": "Trade",
      "number_of_images": "5",
      "image_url": "https://i.ebayimg.com/00/s/MTAyNFg3Njg=/z/..."
    }
  ]
}
```

**New in v3.1:** The `image_url` field contains the primary listing image URL when available.

### Step 5: Present Results to User

Format results in a user-friendly way with images when available:

```
Found 234 used cars matching your criteria. Showing top 10 (sorted by price, lowest first):

---

**1. 2019 Toyota Yaris 1.5 Hybrid Icon**

![Car Image](https://i.ebayimg.com/00/s/MTAyNFg3Njg=/z/...)

💷 Price: £9,995
📍 Location: Hackney, London
📅 Year: 2019
🛣️ Mileage: 57,000 miles
⛽ Fuel: Petrol (Hybrid)
🏪 Seller: Trade
📸 Images: 5 photos available
🔗 Link: https://www.gumtree.com/p/toyota/...

Posted 3 days ago

---

**2. [Next listing...]**
```

**Image Display:**
- Use markdown image syntax: `![Car Image](image_url)`
- Images are typically 300x200px thumbnails
- If `image_url` is `null`, skip the image line
- Always include the "Images: X photos available" line to show total photo count

### Step 6: Offer Photo Analysis (Optional)

After presenting search results, offer to analyze listing photos:

**Trigger Phrases:**
- "Would you like me to analyze the photos for any of these cars?"
- "I can check the images for condition issues and verify the listing accuracy. Which one interests you?"

**When User Requests Analysis:**
1. Confirm which listing to analyze
2. Read IMAGE_ANALYSIS_GUIDE.md for detailed inspection methodology
3. Use Read tool to fetch the car image(s) from `image_url`
4. Perform systematic visual inspection following the guide
5. Report findings using the structured format (Listing Verification, Condition Assessment, Red Flags, Recommendation)

**Example User Request:**
- "Check the photos for listing #1"
- "Does the second car look genuine?"
- "Analyze the Toyota Yaris images"
- "What condition is that car in based on the photos?"

**Analysis Output Structure:**
```
# 🖼️ Image Analysis Report: [Car Title]

## Listing Verification
✅/⚠️/🔴 Make/Model, Year, Color, Trim verification

## Condition Assessment
🟢/🟡/🟠/🔴 Bodywork, Wheels & Tyres, Interior, Cleanliness

## Red Flags
[List any critical issues or "None detected"]

## Recommendation
[Overall assessment and next steps]

**Price Negotiation Leverage:** [If minor issues found]
**Next Steps:** [What to request/verify]
```

See [IMAGE_ANALYSIS_GUIDE.md](IMAGE_ANALYSIS_GUIDE.md) for complete inspection checklist and red flag identification.

---

## Complete Parameter Reference

### Required Parameters

None — you can run a search with no filters (returns all used cars in UK)

### Optional Filters

**Budget:**
- `--min-price <amount>` — Minimum price in GBP
- `--max-price <amount>` — Maximum price in GBP

**Location:**
- `--location <place>` — City name or "uk" for nationwide
- `--distance <miles>` — Search radius (10, 25, 50 miles)

**Vehicle Details:**
- `--make <brand>` — toyota, bmw, ford, etc.
- `--model <model>` — yaris, 3-series, focus, etc.
- `--year <range>` — up_to_1, up_to_3, up_to_5, up_to_10, over_10
- `--mileage <range>` — up_to_15000, up_to_30000, up_to_60000, up_to_80000, over_80000

**Type & Features:**
- `--fuel-type <type>` — petrol, diesel, electric, hybrid_electric, gas_bi_fuel
- `--transmission <type>` — manual, automatic
- `--body-type <type>` — hatchback, suv, saloon, estate, coupe, convertible, mpv
- `--engine-size <range>` — up_to_999, 1000_to_1999, 2000_to_2999
- `--colour <color>` — white, black, silver, blue, red, etc.
- `--doors <number>` — 2, 3, 4, 5

**Seller:**
- `--seller-type <type>` — trade, private (can specify multiple)

**Output:**
- `--sort <method>` — date, relevance, price_lowest_first, price_highest_first, distance, mileage_lowest_first, year_newest_first
- `--limit <number>` — Number of results (default: 10)

---

## Common Search Examples

### Example 1: Budget Commuter
```bash
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --max-price 8000 \
  --location London \
  --fuel-type petrol \
  --transmission automatic \
  --year up_to_8 \
  --sort price_lowest_first \
  --limit 10
```

### Example 2: Family SUV
```bash
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --body-type suv \
  --min-price 15000 \
  --max-price 25000 \
  --location Manchester \
  --year up_to_4 \
  --seller-type trade \
  --sort date \
  --limit 15
```

### Example 3: Specific Model
```bash
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --make bmw \
  --model 3-series \
  --transmission automatic \
  --year up_to_3 \
  --location uk \
  --sort price_lowest_first \
  --limit 20
```

### Example 4: Electric Car
```bash
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --fuel-type electric \
  --max-price 20000 \
  --location London \
  --year up_to_5 \
  --sort mileage_lowest_first \
  --limit 10
```

---

## Troubleshooting

### Empty Results

If `total: 0`, try:
1. Relaxing age filter (increase `--year` range)
2. Removing mileage limit
3. Expanding location to `uk` instead of specific city
4. Removing color filter
5. Checking for typos in make/model names

### Error Output

If `ok: false`, the error message will be in the JSON. Common issues:
- Invalid parameter value
- Network timeout (retry once)
- Gumtree temporarily unavailable

### Performance

- Searches typically complete in 3-5 seconds
- Results are live from Gumtree
- No caching — each search is fresh

---

## Tips for Best Results

1. **Start Broad, Then Narrow** — Begin with basic filters (budget, location), then add specifics
2. **Use Sensible Limits** — `--limit 10` is usually sufficient; too many results overwhelm users
3. **Sort Strategically** — `price_lowest_first` for budget buyers, `date` for latest listings, `mileage_lowest_first` for low-mileage seekers
4. **Check Seller Type** — Trade dealers offer more protection; private sales are cheaper
5. **Provide Context** — After showing results, advise users on what to check (HPI, MOT, viewing)

---

## Integration with Workflow

**Stage 4 (Finding the Right Car)** is the ideal time to offer Gumtree search:

1. User has defined requirements (Stage 1-2)
2. You've recommended 2-3 models (Stage 3)
3. User is ready to see actual listings (Stage 4)

**Suggested Dialogue:**

"I recommend the Toyota Yaris for your needs. Would you like me to search Gumtree right now for available Toyota Yaris listings in London under £8k? I can show you live listings with direct links."

Then execute the search and present results.

**After Presenting Results:**

"I found [X] matching cars. Would you like me to analyze the photos for any of these to check their condition and verify the listing accuracy? I can identify potential issues like bodywork damage, rust, tyre wear, or signs of accident repair."

**If User Requests Photo Analysis:**
1. Read [IMAGE_ANALYSIS_GUIDE.md](IMAGE_ANALYSIS_GUIDE.md) for inspection methodology
2. Fetch images using Read tool
3. Perform systematic visual inspection
4. Report findings with severity classification (🟢 Acceptable / 🟡 Minor Issues / 🟠 Moderate Concerns / 🔴 Red Flags)
5. Provide negotiation leverage and next steps advice
