# Task: A/B Test (Hypothesis Validation)

Evaluate multiple versions of a page change: identify changes, form hypotheses, validate with data.

## Inputs

- `base_metric`: Per-version page metrics
- `block_data[]`: Per-version block data
- `campaign_name`: User-defined experiment name
- `campaign_type`: `inline` (page-edit) | `popup` | `redirect` (different URL per version)
- `campaign_description`: User-written experiment intent
- `version_infos[]`: `{ versionName, versionRate, isControlGroup }`
- `language`: CHINESE | ENGLISH | JAPANESE (default ENGLISH)

## Campaign Type Handling

| Type | Change identification method |
|------|------------------------------|
| `inline` | Use `abTest` records on blocks (primary) |
| `popup` | Use `abTest` records on blocks (primary) |
| `redirect` | Compare `contentSummary` across URLs with hedging language; ALL blocks from both versions are comparison points |

## Version Naming

- When `version_infos` provided: use `versionName` as label, identify control via `isControlGroup`
- When not provided: identify control from blocks where `abTest == null`; use "Control Group"/"Test Version" labels
- `versions[]` order MUST match `version_infos[]` order
- Lead with Test version as primary subject, Control as baseline

## Analysis Flow

### Step 1 — Identify Changes

For each version, list blocks that were modified/added/removed.

**Using abTest field** (for inline/popup):
- `abTest[].type` → concrete description:
  - `CHANGE_IMAGE` / `ADD_IMAGE` → "image changed/added"
  - `EDIT_CONTENT` → use the literal `content` value
  - `ADD_CALL_TO_ACTION` → "CTA added, pointing to: [link]"
  - `CHANGE_STYLE` → "style changed: [literal value]"
- `strategy` MUST be derived ONLY from abTest records, NOT from contentSummary or guessing

**For redirect** (campaign_type === "redirect"):
- Different URL per version — entire page differs; `abTest` records are absent by design
- ALL blocks from BOTH versions are comparison points (no filtering, no truncation)
- Derive `strategy` by comparing `contentSummary` across versions at equivalent positions
- MUST hedge with uncertainty language for every content assertion:
  - CN: 「据截图显示，该区块似乎…」
  - JA: 「スクリーンショットによると〜のようです」
  - EN: "Based on the available screenshot, the block appears to..."
- Do NOT use `campaign_description` or `versionName` as substitute for actual content comparison

**When abTest is null** (inline/popup only): State "no recorded modifications" — do NOT infer changes from context

**campaign_name/campaign_description**: Treat as user-provided context for understanding intent.
Do NOT derive `strategy` from campaign_description. Strategy MUST come from abTest records only.

### Step 2 — Form Hypotheses

Each hypothesis answers: which user stage is it improving? What friction is it reducing?

- `hypothesis_name`: Direct proposition (e.g. "Moving booking form above fold reduces exit rate")
- MUST NOT contain labels like "假设", "Hypothesis", "仮説"
- **Hypothesis de-duplication**: If multiple hypotheses point to the SAME changed blocks (same change
  basis), MUST merge them into one. Present alternatives as alternative explanations under same
  hypothesis, not as separate entries repeating the same change basis.

### Multi-version Coverage (3+ versions)

When 3 or more versions exist:
- `change_content.versions[]` MUST contain entry for EVERY version (not just Control + one Test)
- `data_performance[].change` MUST cite values for ALL versions
  - e.g. "コントロール76.5%、テストA 72.1%、テストB 68.3%"
- Do NOT silently drop any version's data

### Step 3 — Validate with Data

- Cite 1-3 key metric changes (page-level + block-level)
- Separate facts from hypotheses
- Allow 1-2 alternative explanations

### win_version_index Determination

**Conversion is the ultimate business outcome**:
1. If conversionsRate differs meaningfully → version with HIGHER conversionsRate wins
2. If conversionsRate equal/negligible → fall back to hypothesis metric direction
3. If conversionsRate unavailable → fall back to hypothesis metric

**Narrative rule**: result_summary MUST mention BOTH hypothesis metric AND conversionsRate result.
If hypothesis improved but CVR didn't → state explicitly.

### Step 4 — Directional Consistency Self-Check

Before output, verify:
1. Direction-language match for all metric descriptions
2. Numeric direction vs language consistency
3. win_version_index alignment (must point to higher CVR version)
4. key_findings type consistency (warning if hypothesis not validated)

## Output Format (human-readable Markdown report)

Write the entire report in the target language. Placeholders below are in English for clarity.

```markdown
# A/B Test Analysis Report

> **Conclusion**: [one-sentence hook title]

[detailed conclusion summary]

**Key Findings**:
- ✅ [success finding]
- ❌ [failure finding]
- ⚠️ [warning finding]

---

## Hypothesis Validation

### [hypothesis_name — direct proposition, NO label words like "Hypothesis"]

**Winning version**: [versionName]
**Result**: [one-sentence, mentions BOTH hypothesis metric AND CVR]

#### Changes Made

| Version | Affected blocks | Strategy |
|---------|----------------|----------|
| [versionName_0] | [block_name list] | [from abTest records only] |
| [versionName_1] | [block_name list] | [from abTest records only] |

#### Data Performance

| Metric | Change |
|--------|--------|
| [metricLabel] | [delta description, use block_name not block_id] |

#### Root Cause Analysis
- **[topic]**: [explanation]

(repeat for each hypothesis)

---

## Recommendations
1. [actionable next step]
2. [actionable next step]
```

## FORBIDDEN

- Setting win_version_index to version with LOWER conversionsRate when other has HIGHER
- Describing metric as "improved" when it moved in worse direction
- Writing "低下" when numeric value actually increased
- Using contentSummary to describe what changed (use abTest records instead)
- Using campaign_description to derive strategy (it's context only, not authoritative)
- Vague strategy descriptions ("optimized", "improved", "revamp") without explicit abTest evidence
- Asserting specific content facts as definitive based solely on contentSummary
- Silently dropping version data when 3+ versions exist
