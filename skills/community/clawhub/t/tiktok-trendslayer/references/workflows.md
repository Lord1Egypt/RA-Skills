# Advanced Workflow Guides

Detailed step-by-step guides for each advanced workflow. Read the relevant section when executing that workflow.

---

## Workflow 1: Multi-Region Category Analysis

### Purpose

Run cross-regional comparison of influencer landscapes across categories and markets to identify the best opportunities.

### When to Trigger

User asks for regional analysis, cross-market comparison, or says things like "compare US vs SG", "analyze Southeast Asia", "which market is best for 3C".

### Process

1. **Determine scope** — Ask user for target categories and regions (or suggest based on context).
   - Default categories: 3c, beauty, home
   - Default regions: US, SG, TH

2. **Fetch data** — Run `tiktok_slayer.sh` for each region x category combination.
   ```bash
   tiktok_slayer.sh --category 3c --region US,SG,TH --format json
   tiktok_slayer.sh --category beauty --region US,SG,TH --format json
   ```

3. **Read all output files** from `output/` directory.

4. **Analyze and compare:**
   - Engagement rate distribution per region
   - EC score ranking per region
   - Sales performance per region
   - Influencer density (how many active influencers per category)
   - Regional trends and patterns

5. **Generate report** with structure:
   ```
   # Regional Analysis Report: [Categories] across [Regions]

   ## Executive Summary (3-5 bullet points)

   ## [Region] — [Category]
   ### Top Influencers (table: name, followers, engagement, EC score)
   ### Key Insights (2-3 bullet points)

   ## Cross-Regional Comparison
   ### Engagement Rate Comparison (table: region x category)
   ### EC Score Comparison (table)
   ### Sales Performance Comparison (table)

   ## Recommendations
   ### Best Market for Each Category
   ### Priority Actions
   ```

### Output Format

- **MD**: Default for readability
- **Excel**: Use openpyxl — one sheet per region, one summary sheet for comparison
- **PDF**: Use reportlab for professional shareable report

---

## Workflow 2: Influencer Collaboration Plan

### Purpose

Generate a structured influencer collaboration proposal with tiered recommendations, pricing, and execution timeline.

### When to Trigger

User asks for influencer collaboration plan, partnership proposal, or says "how to work with these influencers", "create a collab plan".

### Process

1. **Fetch data** (if not already available):
   ```bash
   tiktok_slayer.sh --category <target> --region <market> --format json
   ```

2. **Read output files** and analyze each influencer.

3. **Score and tier influencers:**

   | Criteria | Weight | Scoring |
   |----------|--------|---------|
   | Engagement Rate | 30% | >15%=100, >10%=90, >5%=70 |
   | EC Score | 25% | >5=100, >4=80, >3=60 |
   | Follower Count | 20% | 1K-5K=90, 5K-20K=80, <1K=70 |
   | Sales Track Record | 15% | Has sales=100, No sales=60 |
   | Content Fit | 10% | Vertical=100, Partial=70 |

   **Tier assignment:**
   - Tier 1 (Priority): Score >= 85 — highest ROI potential
   - Tier 2 (Key): Score 70-84 — solid partners
   - Tier 3 (Supplementary): Score 50-69 — emerging or niche

4. **Generate collaboration plan:**
   ```
   # TikTok Influencer Collaboration Plan

   ## 1. Project Overview
   - Product focus, target markets, timeline

   ## 2. Influencer Selection Criteria
   - The scoring system above

   ## 3. Recommended Influencers

   ### Tier 1 — Priority Collaboration
   | Influencer | Region | Followers | Engagement | EC Score | Recommended Products | Collab Type | Expected Sales | Rate |
   | (table with details)

   ### Tier 2 — Key Collaboration
   (same table format)

   ### Tier 3 — Supplementary
   (same table format)

   ## 4. Collaboration Models
   - Content Collaboration: Provide samples, creator makes video
   - Direct Sales: Provide inventory, creator sells on their account
   - Brand Partnership: Monthly content plan, recurring

   ## 5. Compensation Framework
   | Tier | Follower Range | Engagement | Per-Video Rate |
   (table)

   ## 6. Execution Timeline
   - Phase 1: Outreach (Week 1)
   - Phase 2: Confirmation (Week 2)
   - Phase 3: Content Creation (Week 2-3)
   - Phase 4: Publishing (Week 3-4)
   - Phase 5: Review (Week 4)

   ## 7. KPIs and Evaluation
   | Metric | Target |
   | Video quality | High |
   | Conversion rate | 10%+ |
   | Monthly sales per influencer | Varies |

   ## 8. Risk Management
   - Influencer no-show, content quality, platform policy, payment
   ```

### Output Format

- **MD**: Default — editable and shareable
- **PDF**: Professional proposal format for sending to stakeholders
- **Excel**: Track influencer data, rates, and status

---

## Workflow 3: Product Selection List

### Purpose

Generate a prioritized, data-informed product selection list for TikTok Shop sellers.

### When to Trigger

User asks for product recommendations, what to sell, selection list, or says "what products to push", "create a product list".

### Process

1. **Fetch market data:**
   ```bash
   tiktok_slayer.sh --category <target> --region <market> --format json
   ```

2. **Analyze influencer landscape** to understand what sells:
   - Average product prices in the market
   - Sales volumes and GMV patterns
   - Category gaps and opportunities

3. **Generate product selection list** based on:
   - Market data (price ranges that convert)
   - Platform trends (seasonal demand)
   - Influencer compatibility (what products match available influencers)

4. **Structure the list:**
   ```
   # Product Selection List: [Category] — [Month/Year]

   ## Executive Summary
   - Top 3 recommended product types
   - Optimal price band
   - Expected monthly profit range

   ## Product Selection

   ### Category: [e.g., Phone Accessories — Charging]
   | Product | Specs | Price Range | Target Market | Est. Conversion | Priority | Notes |
   | (table with 5-8 products per sub-category)

   ### Category: [e.g., Phone Accessories — Protection]
   (same format)

   ## Pricing Strategy
   | Price Band | Product Types | Conversion Rate | Profit Margin | Recommendation |
   | $5-10 | ... | 15-20% | 80-120% | ... |
   | $10-20 | ... | 12-18% | 60-100% | ... |
   | $20-40 | ... | 8-14% | 40-70% | ... |
   | $40-80 | ... | 6-10% | 30-50% | ... |

   ## Revenue Forecast
   | Product | Unit Price | Cost | Profit | Monthly Target | Monthly Profit |
   | (table with totals)

   ## Risk Assessment
   - Inventory risk, quality risk, competition risk
   ```

### Output Format

- **MD**: Quick review and editing
- **Excel**: Best for tracking — one sheet per section (Products, Pricing, Revenue)
- **PDF**: Professional report for team sharing

---

## Workflow 4: Video Hook Strategy

### Purpose

Create actionable video content strategies with specific hook types, scripts, and content calendar matched to products and influencers.

### When to Trigger

User asks for video strategy, content plan, hook ideas, or says "create video scripts", "what hooks to use", "content calendar".

### Process

1. **Identify target products** (from Workflow 3 or user-provided).

2. **Match hook types to products:**

   | Hook Type | Conversion Rate | Difficulty | Best For |
   |-----------|----------------|------------|----------|
   | Drop Test | 12-18% | Medium | Cases, screen protectors |
   | Comparison Review | 10-15% | Medium | Power banks, earphones |
   | Quick Unboxing | 9-14% | Low | All products |
   | Scene Application | 8-12% | Medium | Stands, speakers |
   | Price Impact | 11-16% | Low | All products |

3. **Generate video scripts** (3-5 scripts minimum):
   ```
   # Script: [Hook Type] — [Product]

   ## Meta
   - Product: [name]
   - Hook Type: [type]
   - Target Conversion: [X-Y%]
   - Duration: [X] seconds
   - Assigned Influencer: [name]

   ## Storyboard
   | Time | Scene | Voiceover/Subtitle | SFX |
   | 0-3s | ... | ... | ... |
   | 3-8s | ... | ... | ... |
   | (full scene breakdown)

   ## Key Points
   - 3-5 bullet points on execution

   ## CTA
   - Link, urgency, next step
   ```

4. **Create content calendar** matching scripts to influencers and dates:
   ```
   # Content Calendar: [Month]

   ## Week 1 ([dates]) — [Theme]
   | Date | Product | Hook Type | Influencer | Expected Conversion |

   ## Week 2 ([dates]) — [Theme]
   (same format)

   ## Week 3-4...
   ```

5. **Summarize strategy:**
   - Hook type vs conversion rate analysis
   - Influencer assignment matrix
   - Content volume targets
   - Success metrics

### Output Format

- **MD**: Scripts and calendar (primary format)
- **Excel**: Calendar + tracking sheet
- **PDF**: Professional pitch deck for team/stakeholders

---

## Output Format Reference

### When to Use Each Format

| Format | Best For | How to Generate |
|--------|----------|-----------------|
| **MD** | Readability, editing, git versioning | Write directly |
| **JSON** | Machine processing, API integration | Script `--format json` |
| **PDF** | Professional reports, sharing with stakeholders | Use `reportlab` Python library |
| **Excel** | Data management, tracking, calculations | Use `openpyxl` Python library |

### PDF Generation (Python with reportlab)

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
# Use English content to avoid CJK font issues
# Or register a CJK font if Chinese output is needed:
# from reportlab.pdfbase import pdfmetrics
# pdfmetrics.registerFont(TTFont('PingFang', '/System/Library/Fonts/PingFang.ttc'))
```

### Excel Generation (Python with openpyxl)

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
# Use English for cell content to avoid encoding issues
# Font: Calibri (available on all platforms)
```

### File Naming Convention

Reports go to the project output directory:
```
[report_type]_[category]_[date].[format]

Examples:
  selection_list_3c_20260324.md
  collab_plan_3c_US_20260324.pdf
  video_hooks_beauty_20260324.xlsx
  regional_analysis_20260324.pdf
```
