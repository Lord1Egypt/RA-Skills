---
name: shouxin-report
description: Use when handling a small-business bank credit investigation report under a fixed Excel template, from intake and material extraction through drafting, customer supplement list, financial analysis, examiner-style review, material-driven final audit, and iterative revision after review feedback.
metadata:
  short-description: Fixed-template smallbiz credit report workflow
---

# Shouxin Report

Use this skill for end-to-end small-business credit report work when there is a fixed template, especially `.xlsx` templates with protected structure, formulas, and standard disclosure sections.

Use it for:
- First-time customer credit report filing under a bank template
- Revising an existing credit report draft or optimization version
- Creating a separate customer-facing supplement checklist
- Financial-statement mapping, tax-table extraction, and bank-flow analysis
- Examiner-style final review and post-review revision

Do not use it for:
- Free-form narrative reports without a fixed template
- Pure legal opinions, audit reports, or valuation reports
- Tasks limited to a single isolated artifact when a narrower skill is enough
  - Use [$spreadsheet](/Users/daisy/.codex/skills/spreadsheet/SKILL.md) for spreadsheet-only work
  - Use [$credit-report-writing](/Users/daisy/.codex/skills/credit-report-writing/SKILL.md) for text-only credit writing

## Required Inputs

- Original template path
- Customer material directory
- Borrower/entity name
- Current working draft if one exists
- Bank-specific rules, forbidden edits, and output requirements
- Current credit terms if available:
  - amount
  - tenor
  - guarantee/enhancement structure
  - pledged IP if any

## Required Outputs

- Updated report draft or final workbook copy
- Structured extraction results as needed during work
- Customer-facing supplement checklist kept separate from the report body
- Final review findings and repair plan before final write-back

## Hard Rules

These rules are mandatory for every run:

1. Strictly separate template skeleton from customer content.
2. Never delete or compress fixed template titles, numbering, formulas, headers, field groups, or disclosure directories.
3. Evidence priority is fixed:
   - customer scans / original materials
   - external sources for auxiliary verification
   - current report text
4. Report body and customer supplement checklist must be separate deliverables.
5. The report body must not contain internal traces such as `待补充`, `待核实`, `待确认`, `补录`, `需客户补充`.
6. Financial analysis must follow `问题 -> 原因 -> 缓释/应对 -> 整体可控`.
7. Bank statements must be reviewed as a dedicated step, not merely quoted from prior drafts.
8. Fully use materials on:
   - top 5 suppliers/customers
   - existing financing
   - bank statements
   - tax filings
   - financial statements
   - payroll
   - related entities
   - IP / pledge assets
9. The final review must include a material-driven reverse audit:
   - ask what the materials already contain that the report still does not use well
10. Before final output, optimize only in-cell readability:
   - paragraph breaks
   - line breaks
   - wrapping
   - alignment
   - without breaking template layout

## Standard Workflow

Follow this order unless the user explicitly narrows scope.

### 1. Intake and Boundary Lock

- Confirm the original template, material directory, borrower name, and current draft.
- Identify what cannot be changed:
  - formulas
  - merged-cell layout
  - fixed section headers
  - numbering
  - standard disclosure items

### 2. Template Skeleton Identification

Create a mental or written split between:
- `A-class`: fixed template skeleton
- `B-class`: customer-specific content

If in doubt, treat the item as skeleton until proven otherwise.

### 3. Material Inventory and Classification

Classify the customer materials into:
- tax filings
- financial statements
- contracts
- payroll
- bank statements
- top 5 upstream/downstream
- financing/credit information
- related entities
- IP / pledge assets
- corporate profile / founder resume
- other official or third-party materials

### 4. Structured Extraction

Extract and normalize the materials before writing:
- tax tables:
  - period
  - cumulative sales
  - amount in yuan and 10k yuan
- financials:
  - three-period mapping
  - reclassification items
  - tie-out checks
- contracts:
  - customer/supplier
  - product/service
  - date
  - amount
  - term
- payroll:
  - month
  - headcount
  - payroll amount
- bank statements:
  - settlement bank
  - operating inflows/outflows
  - payroll/provident fund/payment patterns
  - interbank fund transfer patterns
- top 5 parties:
  - name
  - amount
  - share
  - years of cooperation
  - settlement method
  - related-party status
- existing financing:
  - bank
  - borrower
  - product
  - balance
  - maturity
  - guarantee mode
- related entities:
  - name
  - relation
  - known operating facts
- IP:
  - title
  - type
  - certificate/registration
  - status
  - pledge value if already provided

### 5. Draft Population Under the Template Skeleton

Populate only within the skeleton:
- business profile
- procurement and sales channel tables
- operating overview
- financial areas
- financial commentary
- key disclosures
- history
- other matters
- proposal / approval opinion sections

Never replace a required structured disclosure block with one summary paragraph.

### 6. Customer Supplement Split

Only after fully checking materials and auxiliary public info:
- move unresolved gaps into a separate customer supplement checklist
- never leave unresolved gap language in the report body

For customer-facing checklists:
- use plain language
- avoid internal review jargon
- do not ask again for materials already provided

### 7. Language Optimization

Improve the body for examiner readability:
- make business profile and operating overview distinct
- front-load strengths and qualification highlights
- write compact, factual, approval-oriented paragraphs
- avoid promotional tone

### 8. Financial Analysis Deepening

Write finance as credit analysis, not textbook commentary.

Must cover:
- revenue and tax consistency
- working-capital occupation
- receivables/inventory logic
- debt structure
- equity support
- financing pressure
- repayment source
- risk control and mitigants

### 9. Examiner-Style Review

Review the report as an examiner:
- logic conflicts
- stale numbers/dates
- shallow analysis
- inconsistent formulas
- unclosed reasoning
- underused materials

### 10. Material-Driven Reverse Audit

This step is mandatory before final output.

Ask:
- What does the material clearly contain that the report still does not use well?
- Are top-5 counterparties fully turned into stability conclusions?
- Are bank statements used to support operating continuity and repayment source?
- Is existing financing written as structure, not merely a total balance?
- Are founder background, qualifications, and IP support translated into credit language?

### 11. Final Consistency Check

Check:
- cross-section numerical consistency
- tax/financial/bank-statement/payroll alignment
- formula retention
- skeleton retention
- old-case residue
- forbidden internal phrases

### 12. In-Cell Formatting Polish

Only optimize inside cells:
- split long text into 2-4 logical paragraphs
- preserve numbering
- use line breaks
- set wrap text
- top-align and left-align long narrative cells

## Recommended Agent / Subagent Architecture

Use the minimum set that fits the job, but the following architecture is the default.

### Main Orchestrator

`Fixed-Template-Credit-Report-Orchestrator`
- Owns sequencing, evidence priority, skeleton protection, final judgment, and write-back

### Core Subagents

`Template-Structure-Guard`
- Detects and protects skeleton sections
- Must be enabled whenever the template has fixed disclosure blocks

`Data-Extractor`
- Extracts tax filings, financials, contracts, payroll, bank flows, top-5 parties, financing, related entities, IP
- Must be enabled when source materials are large or mixed-format

`Finance-Mapping`
- Maps statements to template fields, handles reclassification and tie-out
- Must be enabled when there is a financial statement section

`Finance-Analysis-Writer`
- Writes financial commentary, payroll analysis, true revenue ratio, working-capital logic
- Must be enabled when the report has material financial commentary

`Narrative-Polisher-for-CreditReview`
- Writes business profile, operating overview, history, risk/reasonability narrative
- Must be enabled when the report is for examiner reading

`Client-Friendly-Checklist-Writer`
- Produces customer-facing supplement checklist in plain language
- Skip only if the materials are already complete

`Credit-Examiner-Reviewer`
- Simulates reviewer questions and catches weak reasoning
- Must be enabled before finalization for complex or high-stakes files

`Credit-Report-Defense-Analyst`
- Responds to examiner findings and decides what should or should not be added
- Use whenever final reviewer pushback is expected

`Material-First-Validator`
- Rechecks facts against scans and statements, especially bank flows
- Must be enabled before final write-back

`Excel-Cell-Formatting-Polisher`
- Improves readability inside cells without changing the layout
- Use for Excel-based final deliverables

## Analysis Standards by Module

### Business Profile
- State what the company does, core products/services, solution capability, and business scale
- Use tax sales to anchor scale
- If qualifications and founder background materially support credit quality, translate them into examiner language

### Operating Overview
- Focus on business chain, applications, top 5 counterparties, stability, and proof of continuity
- Use contracts, top-5 tables, bank statements, payroll, tax and financial statements together

### Financial Commentary
- Start from the current period
- Explain not only movement, but business reason
- Always close with mitigants and controllability

### Existing Financing and Banking Relationship
- Write structure, not just the total balance
- If materials show multiple banks, products, or light-guarantee credit acceptance, turn that into a positive credit signal
- Use settlement volume, payroll bank, and average balance when available

### Working-Capital / True Revenue Ratio
- Preserve original formula logic
- Update inputs from current materials
- If some inputs remain partially unresolved, preserve the formula structure and only update confirmed base variables

### Related Entities
- Keep the report body factual and limited to what is supported
- Put missing income, liability, and financing fields into the customer supplement checklist

## Anti-Footgun Checks

Run these before final output:

1. Skeleton check
- Have any fixed headings, numbering, formulas, tables, or disclosure directories been removed or collapsed?

2. Old-value check
- Search for old dates, old borrower names, old revenue figures, stale ratios, and placeholder text.

3. Internal-trace check
- Search for:
  - `待补充`
  - `待核实`
  - `待确认`
  - `补录`
  - `需客户补充`
  - `前文已述，本处无需填写`

4. Material-use check
- For each key material set, ask whether it has been turned into examiner-facing conclusions:
  - top 5 upstream/downstream
  - existing financing
  - bank statements
  - payroll
  - tax filings
  - IP / pledge assets
  - founder background

5. Formula check
- Confirm formulas remain formulas and input cells carry the new values.

## Review-Feedback Revision Mechanism

When a reviewer returns comments:

1. Split comments into:
- hard errors
- evidence gaps
- depth/clarity issues

2. Recheck source materials first.
3. If the material already answers the issue, revise the report before requesting supplements.
4. If the material does not answer it, add only the missing item to the supplement list.
5. Re-run:
- examiner review
- material reverse audit
- consistency check

## Reuse on a New Customer

For each new customer:
- keep the same skeleton-first workflow
- rebuild the material inventory from scratch
- never carry over prior borrower facts or old ratios
- regenerate all top-5, financing, tax, financial, and bank-flow conclusions from the new materials
- create a fresh supplement list only for genuine unresolved gaps

## Continuous Update Guidance

Update this skill whenever a project reveals:
- a new template pitfall
- a new stale-value pattern
- a stronger examiner objection pattern
- a reusable extraction method
- a better way to convert raw materials into credit conclusions

When updating:
- prefer improving checklists and guardrails over adding long explanations
- keep the skill concise
- only add reference files if a topic becomes too detailed for SKILL.md
