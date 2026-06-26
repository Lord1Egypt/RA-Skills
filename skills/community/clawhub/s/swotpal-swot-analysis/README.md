# 📊 SWOTPal — SWOT Analysis Skill for OpenClaw

Professional SWOT analysis and competitive comparison for any company, product, or strategic topic — directly from your AI assistant.

---

## Features

- **Instant SWOT analysis** — Generate structured Strengths, Weaknesses, Opportunities, and Threats for any topic
- **Competitive comparison** — Side-by-side "X vs Y" analysis across key business dimensions
- **Two operating modes** — Works without an API key (free) or with one (pro features + cloud sync)
- **12 languages** — English, Chinese, Japanese, Korean, Spanish, French, German, Portuguese, Italian, Russian, Arabic, Hindi
- **Formatted output** — Clean markdown tables ready for reports, presentations, or documentation
- **Cloud sync (Pro)** — Analyses saved to your SWOTPal account with a full web editor
- **Graceful fallback** — If the API is down, automatically switches to local generation

---

## Quick Start

### Install

```bash
clawhub install swotpal-swot-analysis
```

### Basic Usage

```
> swot Netflix

## Netflix SWOT Analysis

| Strengths | Weaknesses |
|---|---|
| 1. Global subscriber base of 260M+ across 190 countries | 1. Rising content costs exceeding $17B annually |
| 2. Industry-leading recommendation algorithm | 2. Increasing subscriber churn in mature markets |
| ... | ... |

| Opportunities | Threats |
|---|---|
| 1. Ad-supported tier driving new revenue stream | 1. Intensifying competition from Disney+, Amazon, Apple |
| 2. Live sports and events expansion | 2. Password-sharing crackdown risks user backlash |
| ... | ... |
```

```
> compare Tesla vs BYD
> swot分析 星巴克
> 竞品对比 Netflix vs Disney+
```

---

## Two Modes

### Free Mode (No API key)

Works out of the box. The skill uses a structured expert prompt template to generate analyses with the AI assistant's own capabilities. Great for quick, one-off analyses.

### Pro Mode (With API key)

Set your `SWOTPAL_API_KEY` environment variable to unlock:

- **Data-enriched analysis** — Server-side generation with proprietary data sources
- **Cloud sync** — Every analysis is saved to your SWOTPal account
- **Web editor** — Edit, refine, and export analyses at swotpal.com
- **Analysis history** — List and revisit past analyses from the CLI
- **Usage tracking** — See your remaining analysis quota

```bash
export SWOTPAL_API_KEY="sk_your_key_here"
```

---

## Example Output

### SWOT Analysis

```
## Netflix SWOT Analysis

| Strengths | Weaknesses |
|---|---|
| 1. 260M+ paid subscribers across 190+ countries | 1. Content costs exceeding $17B/year |
| 2. Best-in-class recommendation engine (80% of views) | 2. Limited presence in live sports |
| 3. Strong original content brand (Squid Game, Wednesday) | 3. Subscriber growth plateauing in North America |
| 4. Early mover advantage in ad-supported streaming | 4. High debt load from content investments |
| 5. Proven ability to monetize password sharing | 5. Dependence on English-language content pipeline |

| Opportunities | Threats |
|---|---|
| 1. Live sports rights (WWE Raw, NFL Christmas games) | 1. Disney+, Amazon, Apple intensifying competition |
| 2. Gaming expansion with Netflix Games platform | 2. Regulatory pressure in EU and Asia markets |
| 3. Ad-tier revenue projected to reach $5B by 2027 | 3. AI-generated content disrupting production costs |
| 4. Emerging market growth in APAC and LATAM | 4. Economic downturn driving subscription fatigue |
| 5. Licensing content to third parties selectively | 5. Talent costs inflating due to streaming wars |

🔗 View & edit: https://swotpal.com/app/editor/abc123
📊 42 analyses remaining
```

### Versus Comparison

```
## Tesla vs BYD — Competitive Comparison

| Dimension | Tesla | BYD | Edge |
|---|---|---|---|
| Market Position | Premium EV leader, ~20% global EV share | #1 EV seller by volume, dominant in China | BYD |
| Revenue / Scale | $96.8B revenue (2024) | $89.5B revenue (2024), higher unit volume | Tesla |
| Product Strength | Model Y best-selling EV globally | Broad lineup from $10K to $150K | BYD |
| Innovation | FSD, Dojo supercomputer, 4680 cells | Blade Battery, vertical integration | Tie |
| Brand & Reputation | Aspirational global brand | Strong in China/Asia, growing in EU | Tesla |
| Key Weaknesses | Over-reliance on Elon Musk, quality issues | Limited brand recognition in US | Tesla |
| Growth Outlook | Robotaxi bet, energy storage growth | Expanding into EU, LATAM, SE Asia | BYD |

**Overall Verdict:** BYD leads on volume and cost competitiveness, while Tesla retains the edge in brand, margins, and Western markets. BYD's international expansion is the key variable to watch.
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/public/v1/swot` | Generate a SWOT analysis |
| `POST` | `/api/public/v1/versus` | Generate a competitive comparison |
| `GET` | `/api/public/v1/analyses` | List all saved analyses |
| `GET` | `/api/public/v1/analyses/:id` | Get a specific analysis by ID |

All endpoints require `Authorization: Bearer $SWOTPAL_API_KEY` header.

Base URL: `https://swotpal.com`

---

## Commands

| Command | Description |
|---|---|
| `swot [topic]` | Generate SWOT analysis |
| `analyze [topic]` | Generate SWOT analysis (alias) |
| `compare X vs Y` | Competitive comparison |
| `my analyses` | List saved analyses (Pro) |
| `show analysis [id]` | View analysis detail (Pro) |

Works in English, Chinese (中文), Japanese (日本語), and more.

---

## Get API Key

Get your free API key at **[swotpal.com/openclaw](https://swotpal.com/openclaw)** to unlock Pro mode with cloud sync, web editor, and data-enriched analyses.

| Plan | Analyses / month | Price |
|---|---|---|
| Free | 5 | $0 |
| Pro | 100 | $9.9/mo |
| Team | Unlimited | $29.9/mo |

---

## Links

- **Website:** [swotpal.com](https://swotpal.com)
- **Get API Key:** [swotpal.com/openclaw](https://swotpal.com/openclaw)
- **SWOT Examples:** [swotpal.com/examples](https://swotpal.com/examples)
- **Blog:** [swotpal.com/blog](https://swotpal.com/blog)
- **Issues & Feedback:** [github.com/SWOTPal/openclaw-skill/issues](https://github.com/SWOTPal/openclaw-skill/issues)

---

**License:** MIT
