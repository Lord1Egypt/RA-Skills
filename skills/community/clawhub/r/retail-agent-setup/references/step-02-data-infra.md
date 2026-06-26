# Step 02 — Data Infrastructure Assessment

## Goal
Understand what data the store has, where it lives, how fresh it is, and what's missing.
Produces a **Data Map** that guides Step 03 (import) and Step 05 (skills config).

---

## The 6 Data Dimensions

For each dimension, ask the user to rate current state using the prompts below.

### Dimension 1: Product Data
> "Tell me about your product catalog."

| Question | Why It Matters |
|----------|---------------|
| How many SKUs? | Determines import strategy (< 500 manual OK, > 500 needs script) |
| Do you have product descriptions? | Core for knowledge-base Q&A |
| Are there images? | Needed for visual recommendation skill |
| How often does the catalog change? | Determines sync frequency |
| Do variants exist? (size/color/etc.) | Impacts inventory query complexity |

**Health check:**
- ✅ Healthy: Full catalog in ERP/POS with descriptions + images, updated weekly
- ⚠️ Partial: Has SKUs but no descriptions; or descriptions exist only in printed brochures
- ❌ Poor: No digital catalog; staff memorize products

---

### Dimension 2: Inventory Data
> "How do you track what's in stock right now?"

| Question | Why It Matters |
|----------|---------------|
| Is stock tracked digitally? | Enables live inventory queries |
| How often is data updated? (real-time/daily/weekly) | Affects answer accuracy |
| Is it at SKU level or just product level? | Determines variant query capability |
| Are there multiple locations? (stockroom vs floor) | Multi-location inventory |
| How accurate is the data? (shrinkage, lag) | Affects confidence level in answers |

**Freshness tiers:**
| Tier | Update Frequency | Agent Behavior |
|------|-----------------|----------------|
| Real-time | Syncs per transaction | Answer confidently |
| Near-real-time | Syncs hourly | Answer with timestamp caveat |
| Daily | Overnight batch | Answer with "as of yesterday" caveat |
| Weekly | Manual count | Disable live inventory; use soft answers |

---

### Dimension 3: Sales & Transaction Data
> "Can you access your sales history?"

Useful for: promotion effectiveness, product recommendations, staff performance reports.

| Data Type | Use Case |
|-----------|---------|
| Daily sales by SKU | Product recommendation ranking |
| Return/refund records | Complaint handler context |
| Customer purchase history | Personalized recommendations |
| Staff performance data | Manager dashboard skill |
| Seasonal trends | Promotion planning |

**If no sales data:** Skip sales-dependent skills; enable after data accumulates.

---

### Dimension 4: Staff Data
> "Do you have a staff list or org chart?"

Needed for: escalation routing, shift scheduling skill, manager dashboard.

| Data Needed | Format |
|-------------|--------|
| Staff names + roles | List or org chart |
| Contact info (WeCom/phone) | For escalation routing |
| Shift schedule | For on-call routing |
| Permission levels | For L1–L3 escalation in Step 09 |

**Minimum required:** At least one escalation contact (manager) for Step 09.

---

### Dimension 5: Customer / Member Data
> "Do you have a membership database?"

| Data Type | Sensitivity | Use Case |
|-----------|------------|---------|
| Member count | Low | Scope planning |
| Purchase history | High | Personalized recommendations |
| Contact info | High | Campaign skill (future) |
| Points balance | Medium | Loyalty query skill |
| Demographic info | High | Segment targeting |

⚠️ **Privacy note:** Do not import customer PII into the knowledge base. Use anonymized
aggregates or reference the CRM API directly via the inventory-query skill.

---

### Dimension 6: Policy & Operations Documents
> "Do you have written policies for returns, exchanges, warranties, or promotions?"

These are the highest-value data source for immediate agent usefulness.

| Document Type | Format Accepted | Priority |
|--------------|-----------------|---------|
| Return & exchange policy | PDF, Word, image, text | 🔴 Critical |
| Warranty policy | PDF, Word, text | 🔴 Critical |
| Current promotions / pricing rules | PDF, Excel, image, text | 🔴 Critical |
| Store hours & location | Text | 🟡 High |
| Brand story / product FAQs | PDF, Word, text | 🟡 High |
| Staff handbook / training materials | PDF, Word | 🟢 Medium |
| Supplier & reorder info | Excel, text | 🟢 Medium |

---

## Output Format

After collecting responses, produce the **Data Map**:

```
DATA MAP — [Store Name]
═══════════════════════════════════════════════
DIMENSION        STATUS     FORMAT      PRIORITY
─────────────────────────────────────────────
Product catalog  ⚠️ Partial  Excel       🔴 Step 1
Inventory        ✅ Live     ERP API     🔴 Step 2
Sales history    ✅ Good     ERP export  🟡 Step 3
Staff list       ✅ Good     Text/WeCom  🟡 Step 4
Member data      ❌ None     —           🟢 Later
Policy docs      ⚠️ Partial  PDF + Word  🔴 Step 1
═══════════════════════════════════════════════
Import queue (in priority order):
  1. Return policy PDF
  2. Product catalog Excel
  3. Current promotions doc
  4. Staff list for escalation
```

Save this as `data_map` in agent memory before proceeding to Step 03.

---

## Decision Rules

- If **product data is missing entirely**: Stop after Step 03. A knowledge-base-only agent
  using only policy docs is still useful — launch it, then add product data iteratively.
- If **all data is digital and API-accessible**: Recommend skipping file imports in Step 03
  and going straight to API connections in Step 05.
- If **customer PII data is offered**: Accept only aggregated/anonymized data. Redirect
  individual records to be queried via CRM API, not stored in the knowledge base.
