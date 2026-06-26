# TokenBooks Limitations

What TokenBooks **doesn't** do. Read before deploying for financial tracking.

---

## What It Doesn't Do

### 1. **Real-Time Tracking**
TokenBooks analyzes **exported billing data**, not live API usage.

**Why:** Real-time tracking requires hooking into provider APIs, managing auth, handling rate limits, and dealing with billing delays. Out of scope for a local tool.

**Workaround:** Export billing data weekly/monthly and import. Automate with cron if needed.

---

### 2. **Automatic Data Import**
No automatic download from provider dashboards. You must manually export and import.

**Why:** Each provider has different auth mechanisms and export APIs. Automating this requires API keys, OAuth, and provider-specific code.

**Workaround:** 
- Download CSVs/JSON from provider dashboards manually
- Or script exports using provider APIs (outside TokenBooks)

---

### 3. **Cost Prediction**
TokenBooks shows what you **spent**, not what you **will spend**.

**Why:** Predicting future costs requires usage forecasting models, which require historical patterns and assumptions about future behavior.

**Workaround:** Use time series trends to estimate. E.g., "Last 7 days averaged $10/day → expect ~$300/month."

---

### 4. **Provider-Specific Features**
TokenBooks doesn't account for:
- Discounts or credits
- Tiered pricing
- Promotional rates
- Reserved capacity pricing

**Why:** These vary wildly by provider and change frequently. No standard model.

**Workaround:** 
- Export data **after** provider applies discounts (they usually do)
- Or manually adjust costs in CSV before importing

---

### 5. **Multi-Currency Support**
All costs assumed to be in USD. No automatic currency conversion.

**Why:** Currency conversion requires exchange rate APIs and introduces complexity.

**Workaround:** 
- Convert costs to USD before importing
- Or use a multiplier in your analysis scripts

---

### 6. **Task Tagging Enforcement**
TokenBooks can't automatically tag API calls with task names. You must add this data yourself.

**Why:** Providers don't expose task context in billing exports. This is user-provided metadata.

**Workaround:** 
- Add "task" column to your billing exports manually
- Or instrument your code to log task names alongside API calls, then join datasets

---

### 7. **Data Validation**
TokenBooks doesn't validate that imported data is correct. Garbage in, garbage out.

**Example:**
- If OpenAI CSV has wrong costs, TokenBooks will use them
- If timestamps are malformed, import might skip records silently

**Why:** Validating provider-specific data formats is brittle and provider-dependent.

**Workaround:** Spot-check imported data against provider dashboards.

---

### 8. **Granular Billing Details**
TokenBooks shows **aggregated** spending. It doesn't track:
- Individual API request IDs
- User-level attribution (unless in your export)
- Per-endpoint costs
- Batch vs. streaming pricing differences

**Why:** This level of detail isn't in standard billing exports.

**Workaround:** Use provider-specific analytics dashboards for deep dives.

---

### 9. **Historical Data Merging**
TokenBooks doesn't automatically merge overlapping imports. If you import January twice, you'll get duplicates.

**Why:** De-duplication requires unique identifiers per record. Billing exports often don't include request IDs.

**Workaround:** 
- Don't import the same data twice
- Or manually filter duplicates in JSON before analysis

---

### 10. **Provider Pricing Updates**
Model pricing in `config.json` is manually maintained. If providers change pricing, TokenBooks won't know unless you update config.

**Why:** No standard API for provider pricing. Changes announced via blog posts, docs, etc.

**Workaround:** 
- Check provider pricing pages quarterly
- Update MODEL_PRICING in config.json
- Or rely on costs from billing exports (already calculated by provider)

---

## Edge Cases

### Missing Cost Data
If your billing export has token counts but **no cost**, TokenBooks estimates cost using MODEL_PRICING from config. This may be inaccurate if:
- You have custom pricing agreements
- Provider changed pricing mid-month
- You're using a new model not in config

**Workaround:** Ensure exports include costs, or update config with accurate pricing.

---

### Non-Standard Export Formats
OpenAI and Anthropic exports are well-supported. Other providers (Google, Azure, etc.) require custom CSV mapping.

**Why:** No standard billing export format across providers.

**Workaround:** Use custom CSV parser with column mapping (see config_example.json).

---

### Timezone Handling
Timestamps in exports might be UTC, local time, or provider-specific. TokenBooks doesn't normalize timezones.

**Why:** Billing exports rarely include timezone metadata.

**Workaround:** 
- Check provider documentation for timestamp format
- Manually adjust if needed
- Or accept that daily breakdowns might be slightly off if crossing timezones

---

### Large Datasets
Loading hundreds of thousands of records into memory might be slow or cause OOM errors.

**Why:** Simple in-memory aggregation (no database).

**Workaround:** 
- Filter exports to recent months before importing
- Or split large datasets and analyze separately

---

## When NOT to Use TokenBooks

- **Enterprise cost management:** Use Datadog, CloudHealth, or provider-native dashboards
- **Real-time budget enforcement:** Need API-level controls, not post-hoc analysis
- **Automated billing reconciliation:** Need integration with accounting systems
- **Regulatory compliance:** Need certified cost tracking tools
- **Multi-team attribution:** Need user-level or project-level cost allocation built into exports

---

## When TO Use TokenBooks

- **Personal AI spending:** Track your own usage across providers
- **Small team budgets:** Quick monthly spend reports
- **Ad-hoc analysis:** "Where did we spend the most last month?"
- **Model cost comparison:** "Is GPT-4 worth the extra cost for our use case?"
- **Waste detection:** Find low-hanging fruit for cost savings
- **Offline analysis:** No internet, no cloud dashboards, just local data

---

## Honest Summary

TokenBooks is a **local, offline, post-hoc spending analyzer**. It doesn't track live, doesn't predict future costs, and doesn't automate imports. It's designed for individuals and small teams who want a unified view of AI spending without enterprise tooling.
