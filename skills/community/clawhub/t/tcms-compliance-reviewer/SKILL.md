---
slug: tcms-compliance-reviewer
displayName: Tcms Compliance Reviewer
name: tcms-compliance-reviewer
version: "1.1.9"
not_for:
  - Modifying the draft (review and fix suggestions only)
  - Legal review or contract compliance (content compliance focus)
  - Post-publication monitoring or takedown decisions
  - Fact-checking primary sources (citation-format and naming focus)
description: |
  Pre-publication compliance and quality reviewer. Checks factual citations, customer redaction, product naming, competitor rules, internal information, formatting, and AI traces; outputs a pre-review report and fix suggestions without modifying the original.
description_zh: "发布前合规审查器：检查事实引用、客户脱敏、产品命名、竞品规则、内部信息、格式与 AI 痕迹，输出预审报告与修改建议，不改原文。"

read_when:
  - 预审
  - 审核
  - 审稿
  - 终审
  - review
  - 检查初稿
  - fact check
  - 合规检查
  - 发布前审核
  - 发稿前检查
  - pre-publication review
metadata:
  openclaw:
    tags:
      - content-marketing
      - tech-product
      - compliance
      - fact-check
      - editorial-review
      - quality-control
      - b2b
disable: false
---

# Content Compliance Reviewer

Runs a pre-publication compliance and quality review on finished tech blogs, customer cases, product updates, or press releases. Only checks and reports — never auto-modifies the original.

## When to use

- Need to check data facts, customer redaction, product official names, competitor rules, and internal information in an article.
- Need to confirm citation traceability and formatting before publication.
- Need a pre-review report with an approval recommendation.

## Do not use

- Monthly performance analysis and content retrospectives — handled by `content-performance-analyst`.
- Auto-modifying or rewriting the original; provide only location and fix suggestions.
- Initial writing or channel adaptation.

## Input

```yaml
draft_path:
article_type: tech_blog | case_study | product_update | other
compliance_profile: path or object
  - brand_rules:
  - sensitive_terms:
  - product_public_status:
  - customer_redaction_policy:
  - competitor_policy:
review_requested_by:
```

The compliance profile is supplied by the project's private configuration. The generic engine uses logical fields; real paths and rule tables stay in the private layer.

## Workflow

### Step 1: [Deterministic] Load the draft and reference

1. Read the article under review.
2. Read the brand rules, sensitive-term list, product-public-status, and customer-redaction rules from the compliance profile.
3. Look up the corresponding product section in the knowledge base as needed, to verify data provenance.

### Step 2: [LLM] Item-by-item inspection

| # | Check | PASS description |
|---|---|---|
| 1 | Customer redaction | No real internal customer name; description cannot identify the customer |
| 2 | Product formal name | First mention uses the official full name |
| 3 | Competitor rules | No competitor company or product name |
| 4 | Data traceability | Each figure can be traced to an approved source |
| 5 | Internal information | No internal code names, project names or unconfirmed capabilities |
| 6 | Format and structure | Word count, brand title, closing and citation table comply |
| 7 | Content quality | Core message is clear, logic is consistent, no obvious AI template language |

Every item gets: `PASS` / `NEEDS_FIX` / `FAIL`.

### Step 3: [LLM] Generate pre-review report

Output:

```markdown
# Pre-Review Report

## Summary

| Item | Result | Note |
|---|---|---|
| Customer redaction | PASS/NEEDS_FIX/FAIL | |
| Product name | PASS/NEEDS_FIX/FAIL | |
| Competitor | PASS/NEEDS_FIX/FAIL | |
| Data traceability | PASS/NEEDS_FIX/FAIL | |
| Internal info | PASS/NEEDS_FIX/FAIL | |
| Format | PASS/NEEDS_FIX/FAIL | |
| Content quality | PASS/NEEDS_FIX/FAIL | |

## Specific issues

- Location, problem, suggested fix for each NEEDS_FIX or FAIL.

## Citation verification

| Claim | Source | Status |
|---|---|---|

## Overall assessment

- Publishable / Minor fixes / Major revision / Rewrite recommended

## Recommended approval level

- Level and rationale.
```

### Step 4: [Deterministic] Save

Save to: `content/drafts/{original-name}-compliance-review.md`

Execution summary:

```markdown
## Execution Summary
- Article reviewed:
- Results: N pass / M needs-fix / K fail
- Overall: publishable | minor-fix | major-fix | rewrite
- Critical issues:
```

## Pre-publish strengthened checks (backstop for high-frequency rework points)

Beyond the seven general checks, run mandatory checks on high-frequency rework points (corresponding to the P0/P1 items found by the claim / cross-material governance lines). These are also the pre-publish backstop for `content-writer`'s expression red lines:

- **P0 naming consistency**: the tech-blog product's external name must match verbatim the already-published authoritative materials of the same campaign (press release / official site / official account); must not add its own version number or suffix (e.g. if the external name is uniformly "X", the blog must not write "X 2.0"). Inconsistency = FAIL.
- **P0 meta-language / self-reference**: sentences that break the frame — "this article…", "the press release makes it clear that…", "deserves its own section", "back to the overall narrative" — = FAIL; replace with a direct content transition.
- **P0 business jargon**: four-character slogans like "多、快、好、省" = FAIL; rewrite in engineering dimensions (load coverage / execution efficiency / operations experience / resource efficiency).
- **P1 absolutist phrasing**: scan for "naturally connected / seamless / inevitable / certain / zero" etc.; require a bounded qualifier instead.
- **P1 out-of-scope scenarios**: landing industries/scenarios without a knowledge-base or published-article source must be marked `[needs confirmation]` or removed; do not list scenarios from memory (e.g. an industry/scenario needs internal-source backing).
- **P1 faithful transcription vs quantified claims**: infrastructure capabilities backed by an architecture diagram may be stated; quantified speedup multiples without an official figure = FAIL.

> When publishing externally and multiple materials on the same topic already exist, after a PASS pre-review it is recommended to also run the three-piece governance line — `claim-to-source-auditor` + `cross-material-consistency-auditor` + `tech-content-review-panel` — before finalizing.

## Hard Rules

1. Never modify the original draft. Only report issues and suggestions.
2. Data checks must reference an approved source. Missing sources receive a fail.
3. Any real customer name hit is an automatic fail.
4. Employer or unrelated brand names must not appear in outward-facing content unless the piece is officially co-branded; a hit is a fail even when the sentence is otherwise correct.
5. Unconfirmed product capabilities receive a needs-fix.
6. Competitor named references must be flagged.
7. Internal code names or project names are an automatic fail.
8. Human confirmation required before marking the review complete and handing off to adaptation.

## Failure Handling

| Scenario | Action |
|---|---|
| Draft not found | List available drafts for the user |
| Compliance profile missing | Warn and skip brand/sensitive-term checks; flag as incomplete |
| Knowledge-base section unavailable | Mark all data items as unverifiable |
| Draft has no citation table | Mark data traceability as FAIL (no source table means no figure can be checked against an approved source, per Hard Rule 2) and list it as a blocking issue |
| Competitor, customer or product policy changed | Request updated profile before proceeding |

## Output Format

```text
content/drafts/{original-name}-compliance-review.md
```

## Verification

- [ ] All seven inspection items evaluated.
- [ ] Every data claim checked against approved source.
- [ ] Every real customer name flagged.
- [ ] Report saved without modifying the original draft.
- [ ] Execution summary includes next action.

---

## 中文摘要

Content Compliance Reviewer 是发布前合规与质量预审 Skill：检查事实引用、客户脱敏、产品口径、竞品规则、内部信息、格式与 AI 痕迹，只报告不修改原文。除七项通用检查外，对高发返工点做强制兜底（P0 命名一致性/元语言/商务腔，P1 绝对化/超范围场景/量化断言），与 content-writer 的表达红线前后呼应。多份同主题物料对外发布前，建议再跑 claim-to-source + cross-material + tech-content-review 三件套治理线。
