## Description:

Analyze a bank or card CSV export to surface forgotten, unused, or redundant subscriptions, categorize them into cancel, review, and keep tiers, estimate annual spend, and output a markdown action table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zepoldani](https://clawhub.ai/user/zepoldani)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to analyze pasted transaction exports or manual subscription lists, identify recurring subscription charges, and prioritize which services to cancel, review, keep, or confirm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to paste sensitive bank or card transaction history, and server security evidence says the privacy assurances are not fully supportable.

Mitigation: Before use, minimize pasted data by removing account numbers, names, addresses, balances, transaction IDs, unrelated columns, and transactions not needed for subscription detection.

Risk: Pasted financial data may be processed under the configured model provider's privacy and retention policy.

Mitigation: Use only with a verified local/offline model setup or a model provider configuration whose privacy and retention terms are acceptable for the data.

Risk: Merchant inference can misidentify mangled transaction descriptors or overstate cancellation opportunities.

Mitigation: Treat uncertain merchants as confirm-before-action items and review cancellation recommendations before making financial changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zepoldani/skills/subscription-audit)
- [Subscription Audit Tracker](https://zepoldani.gumroad.com/l/huqic)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary, audit table, and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes subscription counts, monthly and annual spend estimates, cancel/review/keep/confirm tiers, and savings summary.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/SKILL.md frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
