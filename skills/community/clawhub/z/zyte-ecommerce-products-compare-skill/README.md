# Zyte E-Commerce Products Compare Skill
 
## 🚀 What this is

Compare products across the internet using AI + real-time web scraping.

Powered by:
- Claude (reasoning)
- Zyte API (data extraction)

## 🔥 Demo Query

Compare iPhone 15:<URL> vs Pixel 8:<URL>

Ever wanted to compare products before buying? While some sites offer product comparison as a built-in feature, what if you want to compare products across different sites? 

Enter product-compare skill, an AI agent skill that extracts structured product data from any e-commerce URL using the [Zyte API](https://www.zyte.com/zyte-api/) and generates side-by-side comparison tables with intelligent purchase recommendations.
 
Paste 2–20 product URLs from any online store, describe what you're looking for, and get a clear comparison table with a recommendation, powered by Zyte's AI product extraction.
 
## What it does
 
1. **Fetches** structured product data (name, price, brand, rating, specs, availability) from any e-commerce site via the Zyte API
2. **Compares** products in a normalized markdown table, handling mixed currencies, missing fields, and different data formats
3. **Recommends** the best option based on your stated intent (e.g. "best value", "most durable", "best for running")
4. **Warns you honestly** if none of the products match what you're actually looking for
 
## Example
 
> *"Compare these 3 products and help me pick the best one for daily use"*
> *(paste 3 product URLs)*
 
The skill fetches all URLs **in parallel**, parses the Zyte API responses, and outputs:
 
- A comparison table with price, brand, rating, availability, and key specs
- A "Key Differences" section highlighting what matters for your decision
- A recommendation with reasoning (Best Overall, Best Value, Best Premium)
- Data notes listing any failed URLs, currency mismatches, or incomplete data
 
## Skill structure
 
```
zyte-ecommerce-products-compare-skill/
├── SKILL.md                          # Workflow instructions for the AI agent
├── scripts/
│   ├── fetch_products.py             # Parallel product fetcher (stdlib only)
│   └── parse_product.py              # Response parser (handles Zyte edge cases)
├── references/
│   └── zyte-api-notes.md             # API reference notes and known gotchas
└── README.md                         # This file
```
 
## Prerequisites
 
- **Python 3.8+** (standard library only — no pip installs needed)
- **Zyte API key** — [sign up for free](https://www.zyte.com/sign-up/) (includes $5 free credit)
 
## Installation
 
### Claude.ai (Web / Desktop / Mobile)
 
1. **Download** this repository as a ZIP:
   - Click the green **Code** button → **Download ZIP**
   - Or use: `https://github.com/<owner>/zyte-ecommerce-products-compare-skill/archive/refs/heads/main.zip`
 
2. **Upload** the ZIP to Claude:
   - Go to **Settings** → **Customize** → **Skills**
   - Click **Add Skill** and upload the ZIP file
   - Make sure **Code execution and file creation** is enabled in **Settings** → **Capabilities**
 
3. **Set your API key** — when prompted during first use, provide your Zyte API key. The skill will ask you to export it:
   ```
   export ZYTE_API_KEY="your_api_key_here"
   ```
 
> **Note:** The ZIP must contain the skill folder at the root level, not just the loose files.
 
### Claude Code
 
Download this repo as .zip and upload it to claude skill tab or copy the skill folder into your Claude Code skills directory:
 
```bash
# Clone the repo
git clone https://github.com/apscrapes/zyte-ecommerce-products-compare-skill
 
# Copy to your personal skills directory (available across all projects)
cp -r zyte-ecommerce-products-compare-skill ~/.claude/skills/
 
# Or copy to a specific project's skills directory
cp -r zyte-ecommerce-products-compare-skill /path/to/project/.claude/skills/
```
 
Claude Code will auto-detect and register the skill. Set your API key:
 
```bash
export ZYTE_API_KEY="your_api_key_here"
```
 
### OpenClaw
 
#### Option A — Install as a managed skill
 
Copy the skill folder into OpenClaw's managed skills directory:
 
```bash
# Clone the repo
git clone https://github.com/apscrapes/zyte-ecommerce-products-compare-skill
 
# Copy to OpenClaw's managed skills directory
cp -r zyte-ecommerce-products-compare-skill ~/.openclaw/skills/
```
 
Then add the skill entry to your `openclaw.json`:
 
```json
{
  "skills": {
    "entries": {
      "zyte-ecommerce-products-compare-skill": {
        "enabled": true,
        "env": {
          "ZYTE_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```
 
Restart the OpenClaw gateway for the skill to be picked up.
 
#### Option B — Workspace skill
 
Copy into your agent's workspace skills:
 
```bash
cp -r zyte-ecommerce-products-compare-skill ~/.openclaw/workspace/skills/
```
 
#### Option C — Paste the GitHub link
 
You can also paste this repository's GitHub URL directly into your OpenClaw chat and ask the assistant to install it. OpenClaw will handle the setup in the background.
 
## Usage
 
Once installed, just talk naturally:
 
- *"Compare these products and tell me which is the best deal"* + paste URLs
- *"Which of these should I buy for outdoor hiking?"* + paste URLs
- *"Product showdown — paste these 3 URLs and help me decide"*
 
The skill triggers automatically when it detects product comparison intent and e-commerce URLs.
 
### What you need to provide
 
| Input | Required | Example |
|-------|----------|---------|
| Product URLs | Yes (2+) | Any e-commerce product page URL |
| Intent | No | "best for daily running", "most durable", "best value" |
| API key | Yes | Set as `ZYTE_API_KEY` environment variable |
 
### Supported sites
 
Any e-commerce site that Zyte's AI extraction supports — which is virtually all of them. The Zyte API uses browser-based AI rendering, so it works on JavaScript-heavy SPAs, server-rendered pages, and everything in between.
 
## How it works
 
1. **Parallel fetching** — `scripts/fetch_products.py` fires all API requests concurrently (up to 5 at a time), cutting fetch time by 60–80% compared to sequential calls
2. **Smart parsing** — `scripts/parse_product.py` handles the edge cases in Zyte's responses: control characters that crash jq, brand fields that vary between string and object format, gzip-compressed responses, and missing data
3. **Rate-limit aware** — the Zyte API uses RPM-based limits (1,400/min default), not concurrency limits. The fetcher auto-retries HTTP 429 responses with exponential backoff
4. **Graceful failures** — if one URL fails, the rest still get compared. Failed URLs are listed in the output with the reason
 
## Technical details
 
- **Zero external dependencies** — uses only Python 3.8+ standard library (`urllib.request`, `concurrent.futures`, `gzip`, `json`)
- **Zyte API payload** — `{"url": "...", "product": true}` (minimal, no conflicting flags)
- **Output format** — markdown comparison table + key differences + recommendation
- **Error handling** — per-URL error isolation, automatic 429 retry, gzip decompression, control character tolerance
 
## API costs
 
Zyte charges per successful extraction. Product extraction costs vary by site tier (typically $0.001–$0.01 per request). A 3-product comparison costs roughly $0.003–$0.03. You are **not charged** for failed requests or rate-limit responses. See [Zyte pricing](https://docs.zyte.com/zyte-api/pricing.html) for details.
 
## Troubleshooting
 
| Problem | Solution |
|---------|----------|
| `ZYTE_API_KEY` not found | Export it: `export ZYTE_API_KEY="your_key"` |
| DNS resolution errors | Run: `echo "nameserver 8.8.8.8" > /etc/resolv.conf` |
| HTTP 422 from Zyte | The payload has conflicting fields — check `references/zyte-api-notes.md` |
| `jq` parse errors | Don't use jq — use `scripts/parse_product.py` which handles control chars |
| All URLs return "no product data" | The sites may require browser rendering (already the default), or the URLs aren't product pages |
 
 
## Credits
 
- [Zyte API](https://www.zyte.com/zyte-api/) for the product extraction engine
- Built as a skill for [Claude](https://claude.ai), [Claude Code](https://code.claude.com), and [OpenClaw](https://openclaw.ai)
 
