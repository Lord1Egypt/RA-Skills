## Description:

Provides a VAT/GST pre-check for cross-border sellers operating through Shopee, Lazada, TikTok Shop, and other sales channels in six Southeast Asian markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border sellers use this skill to review draft filing data and marketplace statements for common VAT/GST rate, registration, low-value goods, fulfillment, filing-deadline, pricing-display, and customs-declaration issues. It provides a preliminary report and next steps, not tax filing or a compliance determination.

### Deployment Geography for Use:

Southeast Asia: Singapore, Thailand, Indonesia, the Philippines, Vietnam, and Malaysia.

## Known Risks and Mitigations:

Risk: Uploaded filing data or platform statements may contain tax identifiers, bank details, customer information, credentials, or unrelated transactions.

Mitigation: Prefer aggregate sales figures, redact sensitive and unrelated information before uploading, and check the agent provider's upload and retention practices.

Risk: A preliminary pre-check may be mistaken for proof of tax compliance or definitive advice on rapidly changing local rules.

Mitigation: Treat the report as preliminary, verify flagged rules with the relevant tax authority, and confirm registration or filing questions with a local tax agent.

## Reference(s):

- [Deadlines reference](artifact/references/deadlines.md)
- [VAT/GST rule table](artifact/references/rule-table.md)
- [ClawHub skill page](https://clawhub.ai/snowhola/skills/southeast-asia-vat-precheck)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown risk summary, findings table, and prioritized next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-check only; missing information is marked cannot determine, volatile rules are flagged for verification, and the skill does not file returns or register sellers.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
