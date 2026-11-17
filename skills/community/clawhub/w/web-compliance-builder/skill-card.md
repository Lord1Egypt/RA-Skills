## Description:

Classify a web business, then identify, draft, and checklist the compliance pages, notices, disclosures, user flows, and launch gates it needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and website owners use this skill to classify a site or app, generate fact-bound compliance pages and checklists, and audit existing policies for missing, inadequate, or mismatched requirements. It supports ecommerce, SaaS, subscriptions, marketplaces, apps, AI product sites, newsletters, affiliate or lead-generation pages, and cross-border stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce incorrect, incomplete, or stale legal-compliance guidance for a specific jurisdiction, platform, or business model.

Mitigation: Treat outputs as drafting and issue-spotting support only, keep the required disclaimer, and have qualified counsel review high-risk, regulated, sensitive-data, children-focused, cross-border, marketplace, subscription, or AI use cases.

Risk: A generic policy or checklist could be misleading if it is not tied to the site's actual data, tracking, transactions, regions, and platform dependencies.

Mitigation: Run the structured intake first, classify the business before drafting, omit unsupported clauses, and require evidence for checklist and launch-gate items.

Risk: Existing policy pages can contradict operational practice, such as tracking before consent or undisclosed cross-border fulfillment.

Mitigation: Use audit mode to inventory existing pages, mark mismatches and missing legal requirements as blocking, and remediate the highest-severity gaps before launch.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clarezoe/skills/web-compliance-builder)
- [Audit Workflow](references/audit-workflow.md)
- [Business Types](references/business-types.md)
- [Checklist Framework](references/checklist-framework.md)
- [Jurisdictions](references/jurisdictions.md)
- [Page Requirements](references/page-requirements.md)
- [Policy Templates](references/policy-templates.md)
- [Source Register](references/source-register.md)
- [Deep Research Report](research/deep-research-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts and tables, JSON intake/checklist data, and shell commands for local helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include requirement labels, evidence fields, uncertainty labels, legal-review flags, and launch-gate pass/fail status.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
