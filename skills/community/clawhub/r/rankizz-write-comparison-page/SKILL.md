---
name: rankizz-write-comparison-page
description: Research and write a balanced product comparison or versus page using consistent criteria, current sources, normalized pricing, use-case verdicts, limitations, and clear publisher disclosure. Use when a user asks for "A vs B," "our tool vs competitor," a software comparison, feature comparison, buyer decision page, or migration comparison. Rankizz keyword and SERP data is optional; current evidence for both products is required.
---

# Write a comparison page

Help a defined buyer choose between two products. Apply the same evidence standard to both, especially when the publisher owns one product.

Read [references/comparison-evidence.md](references/comparison-evidence.md) before researching or drafting.

## Define the comparison

Resolve:

- the two products, the intended buyer, and the job being compared
- region, currency, team size, expected usage, and buying horizon
- decisive criteria and non-negotiable requirements
- comparable plans, billing periods, seats, usage units, and add-ons
- migration, integration, deployment, support, privacy, and security needs
- what the publisher has directly tested
- ownership, affiliate, sponsorship, or other commercial relationship
- research and pricing cutoff date

A useful comparison has a boundary. If the products serve different jobs, say so and compare only the overlapping decision.

## Build evidence symmetrically

Prefer each product's official pricing, documentation, limits, changelog, policies, security information, and terms for factual capability claims. Use independent sources for experience or reliability claims the vendors cannot prove.

Build the evidence matrix before writing:

| Criterion | Product A | Product B | Test or source | Date | Confidence |
| --- | --- | --- | --- | --- | --- |

Use `verified`, `partly verified`, or `not verified`. Absence from a marketing page does not prove a feature is absent. Do not convert account access, documentation reading, or a demo video into hands-on testing.

For feature rows, describe behavior and relevant limits instead of using checkmarks:

| Need | Product A | Product B | Why it matters |
| --- | --- | --- | --- |
| Client approvals | Email guest review, no paid seat | Reviewer needs paid seat | Changes cost for agencies with many clients |

Rankizz is optional. Connected keyword or live SERP data can clarify query intent and prioritize reader questions, but it cannot decide the product verdict. Hosted calls require at least 10 credits.

## Normalize the price

Record:

- currency, taxes, and region
- monthly or annual commitment
- price per seat, workspace, usage unit, or flat account
- minimum seats and included usage
- overages, required add-ons, implementation, and contract terms
- trial versus permanently free plan
- date checked

When possible, calculate one or more disclosed reader scenarios. For example: `5 editors + 20 guests + expected monthly usage`. Label assumptions and do not estimate negotiated pricing as fact.

## Reach a segmented verdict

Do not crown a universal winner. Decide by constraint:

- choose A when its evidenced advantage matters more than its tradeoff
- choose B when the opposite is true
- choose neither when a non-negotiable requirement is missing

If the publisher owns Product A, disclose it before the first verdict. Name important areas where Product B wins. A fair conclusion may still favor the publisher's product, but the evidence must support it.

## Write the page

### Direct answer

Open with the primary difference, who should choose each product, and the evidence date. Do not delay the answer behind generic category history.

### At-a-glance table

Include best fit, decisive strength, decisive limitation, normalized starting or scenario cost, and testing status.

### Methodology

Explain the audience, criteria, source hierarchy, tests, price assumptions, and commercial relationship.

### Criterion sections

For each criterion:

1. state what the buyer needs
2. describe Product A with evidence and limits
3. describe Product B at the same depth
4. explain which buyer benefits from the difference
5. name a winner only when the evidence supports one

Cover only decision-relevant areas. A long feature inventory can hide the differences that matter.

### Pricing and true cost

Show comparable plans, important limits, and scenario math. Separate published price from likely total cost and unverified enterprise charges.

### Final decision

Use `choose A if`, `choose B if`, and `choose neither if`. Include switching or migration concerns where relevant.

## Do and do not

| Do | Do not |
| --- | --- |
| Define one buyer and job | Compare products in the abstract |
| Use identical criteria and evidence depth | Scrutinize the competitor while repeating the publisher's claims |
| Describe feature behavior and limits | Fill tables with unexplained checkmarks |
| Normalize price and calculate disclosed scenarios | Compare a monthly price with an annual per-seat price |
| State what was tested and how | Claim hands-on experience without doing the work |
| Give each product meaningful wins and losses | Use token praise for the competitor before choosing the publisher |
| Label unknowns as unverified | Infer absence or weakness from missing documentation |
| Disclose ownership or affiliate interests early | Present owned-product content as independent editorial review |
| Use a segmented verdict | Declare one product best for everyone |
| Refresh current facts before changing the date | Update the timestamp while leaving stale prices |

## Examples

### Weak feature comparison

> Product A has powerful automation, while Product B offers basic automation.

The terms are undefined and the evidence is missing.

### Better feature comparison

> Product A can trigger an approval step when a status changes and can require two named reviewers. Product B can assign one reviewer but does not document multi-reviewer approval. Product A fits regulated teams that need separation of duties; Product B is simpler for a single-editor workflow. Documentation checked 16 August 2026.

### Better price comparison

> For five editors on annual billing, A costs $600 per year and includes unlimited guests. B costs $480 per year for five seats, but client reviewers consume seats; with ten reviewers, the published total becomes $1,440. This scenario excludes tax and assumes every reviewer needs simultaneous access.

### Honest verdict

Good:

> Choose A for no-seat client review. Choose B if its native warehouse integration removes a manual export step. Neither is suitable if self-hosting is mandatory.

Bad:

> A wins because it offers the best overall value and more innovative features.

## Add the publication package

Provide a descriptive H1, concise title and page-specific description, stable slug, contextual internal links, source links, representative image brief, update date, and structured data only when visible content qualifies. Avoid duplicate versus pages with reversed product order or minor keyword substitutions.

## Limitations

- Public plans may omit negotiated pricing, enterprise limits, implementation fees, and regional differences.
- Documentation proves stated behavior, not reliability, usability, support quality, or performance at scale.
- A limited trial cannot represent every workflow or long-term product experience.
- Product facts change. Date every snapshot and identify facts that must be refreshed.
- Do not invent tests, customer opinions, security conclusions, benchmarks, or feature gaps.
- The comparison cannot guarantee rankings, purchases, or fit for every organization.

## Output template

```markdown
# [Product A] vs [Product B]: which is better for [specific audience or job]?

[Direct, segmented answer with the decisive difference and research date.]

Disclosure: [ownership, affiliate, sponsorship, or access relationship]

## At a glance
| Decision | Product A | Product B |
| --- | --- | --- |
| Best for | | |
| Decisive strength | | |
| Main limitation | | |
| Comparable price | | |
| Evidence status | | |

## How we compared them
- Buyer and job:
- Criteria and disqualifiers:
- Hands-on work:
- Source hierarchy:
- Pricing assumptions and cutoff:

## [Criterion that changes the decision]
### Product A
[Behavior, limit, evidence]

### Product B
[Behavior, limit, evidence]

### Which is better for this criterion?
[Segmented conclusion or no winner]

[Repeat only for decision-relevant criteria]

## Pricing and true cost
| Scenario | Product A | Product B | Assumptions |
| --- | --- | --- | --- |

## Choose Product A if
- [Constraint and evidence]

## Choose Product B if
- [Constraint and evidence]

## Choose neither if
- [Missing non-negotiable requirement]

## Research notes
- Last checked:
- Unverified facts:
- Refresh triggers:

## Editorial QA
- [ ] Both products receive the same evidence standard
- [ ] Feature rows explain behavior and limits
- [ ] Pricing uses comparable units and disclosed assumptions
- [ ] Every verdict has an audience boundary
- [ ] Ownership and affiliate relationships are prominent
- [ ] Unknowns remain unverified
- [ ] No invented testing or customer experience
```
