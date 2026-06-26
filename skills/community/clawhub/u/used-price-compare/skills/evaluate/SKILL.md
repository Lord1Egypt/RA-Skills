---
name: evaluate
description: |
  In-depth second-hand listing evaluation from listing URLs: trust, value, photos.
  Optional vision model (e.g. Qwen-VL) for image analysis. Lower seller weight on Gumtree.
  Triggers on: evaluate item, trustworthy, worth it, analyze seller, compare listings,
  评估商品, 靠谱吗, 值不值, 分析卖家.
version: 0.6.4
---

# Item evaluation

Analyze **value for money** and **listing trustworthiness** from a buyer's perspective.
With a vision model configured, run image authenticity and text–image consistency checks.

> If the user writes in Chinese, see [../../references/zh-CN.md](../../references/zh-CN.md) (Evaluate section).

## Skill boundaries (mandatory)

**Allowed CLI subcommands only:**

| Subcommand | Purpose |
|------------|---------|
| `fetch-detail` | Fetch one listing detail page |
| `evaluate` | Fetch and evaluate one or more listings |
| `summarize` | Full flow: fetch, score, comparative summary |
| `vision-config` | Show or initialize vision model config |

---

## Intent routing

1. User provides URL(s) + evaluate / legit / worth it → evaluation flow.
2. User picked URLs from compare results for comparison → `summarize`.
3. User only wants raw detail fields → `fetch-detail`.

## Capabilities

### 1. Fetch listing details

From a supported URL, extract:

- **Listing**: title, description, condition, images
- **Seller**: name, ratings, review count, member since, location
- **Other**: posted time, views, shipping, return policy

### 2. Scoring dimensions

Focus on **value** and **description + image trust**; seller score is secondary.

#### With vision model (recommended)

| Dimension | Weight | Notes |
|-----------|--------|-------|
| Description trust | 20% | Detail, title accuracy, red flags |
| Image analysis | 20% | Real photos vs stock, text–image match, visible condition |
| Price competitiveness | 25% | vs median of peer listings |
| Condition | 15% | Stated grade vs description |
| Seller trust | 10% | Ratings, volume, account age (Gumtree: 5%) |
| Risk signals | 10% | Combined penalties (Gumtree: 15%) |

#### Without vision model

| Dimension | Weight | Notes |
|-----------|--------|-------|
| Description + image count | 35% | Detail, photo count, title accuracy |
| Price competitiveness | 30% | vs median |
| Condition | 15% | Stated grade |
| Seller trust | 10% | (Gumtree: 5%) |
| Risk signals | 10% | (Gumtree: 15%) |

> **Gumtree**: sparse seller data → seller weight 5%, extra weight on risk signals.

### 3. Vision model (optional)

With `--vision-model`, images are sent to an OpenAI-compatible vision API (e.g. Qwen-VL) for:

- **Authenticity** — real photos vs stock/watermarked images
- **Text–image match** — visuals vs title/description
- **Visible condition** — wear and defects visible in photos
- **Risk signals** — watermarks, heavy editing, hidden defects

### 4. Recommendations

- **Strongly recommended** — strong scores, no major flags
- **Recommended** — good overall, minor issues
- **Proceed with caution** — notable risk factors
- **Not recommended** — serious red flags or likely scam

## Vision config

Merged priority (low → high):

1. `~/.config/used-price-compare/vision.json`
2. Env: `VISION_API_BASE`, `VISION_API_KEY`, `VISION_MODEL`
3. CLI: `--vision-model`

### Init config

```bash
python scripts/cli.py vision-config init
```

Template at `~/.config/used-price-compare/vision.json`:

```json
{
  "model": "qwen-vl-max",
  "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "api_key": "",
  "max_images": 5,
  "timeout": 60
}
```

Set `api_key` locally (never commit secrets).

### Show config

```bash
python scripts/cli.py vision-config show
```

### Config fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `model` | string | Vision model name | `""` |
| `api_base` | string | OpenAI-compatible API base URL | `""` |
| `api_key` | string | API key | `""` |
| `max_images` | int | Max images per listing | `5` |
| `timeout` | int | Request timeout (seconds) | `60` |

Env vars override the file when set. Image analysis runs only when model, base URL, key, and `--vision-model` are all available; otherwise heuristic scoring applies.

## Workflow

### Fetch detail

```bash
python scripts/cli.py fetch-detail \
  --url "https://www.gumtree.com/p/..."
```

### Evaluate (no vision)

```bash
python scripts/cli.py evaluate \
  --urls "https://www.gumtree.com/p/...,https://www.ebay.co.uk/itm/..."
```

### Evaluate (with vision)

```bash
python scripts/cli.py evaluate \
  --urls "https://www.gumtree.com/p/...,https://www.ebay.co.uk/itm/..." \
  --vision-model qwen-vl-max
```

### Full summary (recommended)

```bash
python scripts/cli.py summarize \
  --urls "https://www.gumtree.com/p/...,https://www.ebay.co.uk/itm/..." \
  --vision-model qwen-vl-max
```

### Parameters

| Parameter | Description | Commands |
|-----------|-------------|----------|
| `--url` | Single listing URL | `fetch-detail` |
| `--urls` | Comma-separated URLs | `evaluate`, `summarize` |
| `--vision-model` | Vision model name | `evaluate`, `summarize` |
| `action` | `show` (default) or `init` | `vision-config` |
| `--force` | Overwrite existing config | `vision-config init` |

## Output format

### Results table

```
🔍 Listing evaluation

Rank | Title              | Price | Platform | Photos | Condition | Score  | Verdict
1    | iPhone 15 Pro 128GB| £750  | Gumtree  | 5      | Like new  | 8.5/10 | Recommended
```

### Per-listing narrative

Explain from a buyer's perspective why each listing is recommended or not.

### Final advice

- Best value pick (with link)
- Runner-up
- Listings to avoid and why

## Supported URLs

| URL pattern | Platform | Adapter |
|-------------|----------|---------|
| `*.ok.com` | OK.com | `ok/detail` |
| `*.ebay.*` | eBay | `ebay/detail` |
| `*.gumtree.com` | Gumtree | `gumtree/detail` |
| `*.amazon.*` | Amazon | `amazon/detail` |

## Failure handling

- **Unsupported URL**: only the four platforms above.
- **Parse failure**: show successes; report failed URLs.
- **bb-browser down**: check daemon status.
- **Vision API failure**: fall back to non-vision scoring; do not abort the run.
