---
name: uplo-insurance
description: AI-powered insurance knowledge management. Search policy documents, claims records, underwriting guidelines, and actuarial data with structured extraction.
---

# UPLO Insurance — Underwriting, Claims & Actuarial Intelligence

Insurance carriers generate and consume documentation at a pace that overwhelms traditional search: policy forms and endorsements, underwriting guidelines with tiered authority levels, claims adjuster manuals, actuarial rate filings, reinsurance treaties, producer commission schedules, and regulatory correspondence across 50+ state DOIs. UPLO structures this knowledge so underwriters, claims professionals, and compliance analysts can find definitive answers instead of chasing down the person who "just knows."

## Session Start

Insurance documentation carries significant classification requirements. Rate filing strategies, loss reserve analyses, reinsurance terms, and litigation management plans are typically restricted to specific functional areas.

```
get_identity_context
```

Review active directives. In insurance, these often reflect underwriting appetite changes, moratorium announcements (e.g., post-catastrophe writing freezes), or regulatory compliance deadlines.

```
get_directives
```

## When to Use

- An underwriter asks what the maximum policy limit is for a monoline cyber liability risk with revenue above $500M and whether the account requires home office referral
- Claims asks whether a water damage claim from a burst pipe is covered under the standard HO-3 form or excluded by the water damage endorsement attached to this program
- The compliance team needs to verify that the new personal auto rate filing was approved in all target states and identify which DOIs have outstanding objections
- Actuarial wants the historical loss development triangles for the commercial auto book to validate reserve adequacy
- A producer asks about the commission schedule differences between new business and renewal for the small commercial BOP program
- The reinsurance team needs to determine whether a specific large loss breaches the retention under the current property catastrophe treaty
- Someone in product development asks what competitors are offering for parametric flood coverage and whether the organization has any similar filed forms

## Example Workflows

### Complex Claim Coverage Determination

A commercial policyholder reports a claim involving water intrusion, resulting mold remediation, and business interruption. The claims examiner needs to piece together coverage from multiple forms.

```
search_knowledge query="commercial property policy form CP 00 10 coverage for water damage and resulting mold remediation"
```

```
search_knowledge query="business interruption waiting period and coverage trigger under the commercial property special form"
```

```
search_with_context query="mold exclusion endorsements attached to the small commercial property program and any sub-limit exceptions"
```

### State Regulatory Filing Compliance

The company is expanding its homeowners product into three new states. The compliance team needs to navigate each state's filing requirements.

```
search_knowledge query="prior approval versus file and use states for homeowners insurance rate and form filings"
```

```
search_with_context query="state-specific homeowners coverage requirements mandated coverages and prohibited exclusions for Florida Georgia and South Carolina"
```

```
search_knowledge query="DOI objection response templates and timeline requirements for rate filing interrogatories"
```

## Key Tools for Insurance

**search_knowledge** — Essential for coverage questions, which require exact policy language. Underwriters and claims adjusters need the specific form wording, not a paraphrase: `query="CGL occurrence definition and claims-made retroactive date provisions in the professional liability endorsement"`. Insurance is a business of precise language.

**search_with_context** — Insurance questions frequently involve layered relationships: a claim touches the policy form, endorsements, the underwriting file, the producer agreement, and potentially the reinsurance treaty. A query like `query="coverage analysis for the Johnson Manufacturing product liability claim including excess layers and reinsurance recovery potential"` requires graph traversal across these interconnected records.

**get_directives** — Underwriting appetite shifts frequently. A directive announcing "suspend new monoline D&O submissions for public companies" or "implement 25% rate increase minimum on Florida coastal property" must be checked before quoting or binding.

**export_org_context** — Useful for market conduct exam preparation, reinsurance treaty renewals, and board presentations. Provides a comprehensive view of the organization's operational structure, product lines, and strategic priorities.

**flag_outdated** — Insurance forms and guidelines are version-controlled but the old versions linger. If you find an underwriting guide referencing a withdrawn form number or a superseded rating algorithm, flag it: `entry_id="..." reason="References ISO CGL form CG 00 01 04 13; current edition is CG 00 01 12 24 with material changes to the AI liability exclusion"`

## Tips

- Insurance coverage questions hinge on exact policy language. Never summarize coverage provisions in your own words when the actual form wording is available — the difference between "arising out of" and "caused by" can determine millions in claim outcomes. Quote the form language directly.
- State-by-state regulatory variation is the norm in insurance. Any question about rates, forms, or market conduct must specify the state. A coverage that is standard in Texas may be prohibited in New York.
- Loss data and reserve information is actuarially sensitive. Premature disclosure of reserve inadequacy or development factor assumptions can have legal and financial consequences. Treat actuarial workpapers with the same sensitivity as pre-decisional legal documents.
- Reinsurance treaty terms use specialized language (occurrence excess, aggregate stop loss, reinstatement premiums) that general insurance knowledge may not cover. When a reinsurance question arises, search for treaty-specific documentation rather than relying on primary coverage knowledge.
