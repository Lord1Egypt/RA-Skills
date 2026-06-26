# Analyze Meta Ads Performance

**Purpose:** Retrieve and analyze Meta ad campaign performance metrics with DTC benchmark comparisons and actionable recommendations.

**When to Use:**
- User asks about ad performance, ROAS, ad spend, or campaign metrics
- User wants to know which ad or creative is winning
- User needs audience or creative breakdowns
- Routine performance check-ins

**Prerequisites:**
- `META_ADS_ACCESS_TOKEN` and `META_ADS_ACCOUNT_ID` in `.env`
- Active or recently active campaigns in the ad account

---

## Workflow Steps

### Step 1: Account Summary

**Description:** Get the high-level account overview with DTC benchmarks.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --summary --period 7
```

**What you see:**
- Spend, impressions, reach, frequency
- Clicks, CTR, CPC, CPM
- Purchases, add-to-cart, CPA, ROAS
- DTC benchmark comparison (GOOD/OK/LOW/HIGH ratings)

**DTC Benchmark Ranges:**
| Metric | Good | OK | Needs Work |
|--------|------|----|------------|
| CTR | >1.5% | 1-1.5% | <1% |
| CPM | <$15 | $15-25 | >$25 |
| CPA | <$30 | $30-50 | >$50 |
| ROAS | >3x | 2-3x | <2x |
| Frequency | 1-3 | 3-5 | >5 (ad fatigue) |

---

### Step 2: Campaign Comparison

**Description:** Compare campaigns to find top/bottom performers.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --campaigns --period 7
```

**Analysis points:**
- Which campaign has the highest ROAS?
- Which campaign has the lowest CPA?
- Are any campaigns spending without converting?
- Is budget allocated to the best performers?

---

### Step 3: Campaign Deep Dive

**Description:** For the most important campaign(s), get daily trends and breakdowns.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --campaign CAMPAIGN_ID --period 14
```

**Analysis points:**
- Is performance trending up or down?
- Are we past Meta's learning phase (~50 conversions / 7 days)?
- Which ad sets are outperforming?
- Which individual ads are winning?

---

### Step 4: Creative Analysis

**Description:** Understand which creative elements are performing best.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --ads --period 7
```

**Analysis points:**
- Which image variants get the highest CTR?
- Which primary text drives the most conversions?
- Which headline has the best engagement?
- Are there clear winners to scale or losers to cut?

---

### Step 5: Audience Insights

**Description:** Check demographic and placement performance.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --audience --period 7
```

**Analysis points:**
- **Age:** Which age groups convert best? Any wasted spend on non-converting ages?
- **Gender:** Performance difference between male/female?
- **Platform:** Facebook vs Instagram — where does the audience engage?
- **Device:** Mobile vs desktop conversion rates?
- **Placement:** Feed vs Stories vs Reels effectiveness?

---

### Step 6: Recommendations

**Description:** Based on all data, provide actionable next steps.

**Framework for recommendations:**

**If ROAS > 3x:** Scale budget 20-30%. Test new audiences.
**If ROAS 2-3x:** Hold budget. Optimize creative (test new images/copy).
**If ROAS < 2x:** Audit targeting. Pause worst performers. Test new angles.

**If CTR < 1%:** Creative isn't resonating. Test new hooks/images.
**If CTR > 2% but low ROAS:** Traffic quality issue. Check landing page conversion rate.

**If Frequency > 4:** Ad fatigue setting in. Refresh creative or expand audience.
**If CPM rising:** Competition increasing. Try new placements or audiences.

**Common actions:**
- Kill ads with spend but zero conversions after 3+ days
- Increase budget on ad sets with CPA below target
- Duplicate winning ad sets with new audiences
- Refresh creative when frequency exceeds 4

---

### Step 7: Sync Data (Optional)

**Description:** Save all data locally for cross-channel analysis.

**Actions:**
```bash
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --sync --period 30
```

Data saved to `Analytics/meta-ads/` for use with growth dashboard and content analysis scripts.

---

## Outputs

**Primary Output:**
- Performance summary with benchmark comparisons
- Campaign/ad set/ad level metrics
- Audience and creative breakdowns
- Actionable recommendations

**Where outputs are stored:**
- Console output for immediate review
- `Analytics/meta-ads/` when --sync is used
- CSV export available via --export

---

## Error Handling

**No data available:**
- Campaigns may be too new (need 24+ hours for data)
- Check that campaigns are ACTIVE (not PAUSED)
- Try a longer --period

**API errors:**
- Verify credentials with `uv run ~/.claude/skills/MetaAds/tools/Publish.py --check`
- Rate limiting is handled automatically with exponential backoff
- If persistent, wait 15 minutes and retry

---

**Last Updated:** 2026-02-07
