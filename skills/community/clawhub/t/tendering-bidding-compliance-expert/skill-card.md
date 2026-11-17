## Description:

Tendering Bidding Compliance Expert is a Chinese-first agent skill for PRC tendering-and-bidding compliance Q&A, document review, bid rejection risk checks, violation signal analysis, and objection or complaint guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, bidding, compliance, and legal-support users can use this skill to research PRC tendering-and-bidding requirements, review tender or bid materials for compliance risks, identify rejection risks, and prepare objection or complaint guidance. It is scoped away from government procurement goods and services matters and does not replace professional legal advice.

### Deployment Geography for Use:

Global; intended subject matter is PRC tendering and bidding compliance.

## Known Risks and Mitigations:

Risk: Users may treat legal compliance guidance as a substitute for qualified legal advice.

Mitigation: The skill should frame outputs as research and document-check support, preserve its no-formal-legal-opinion boundary, and recommend professional counsel for material decisions.

Risk: Confidential bid or tender materials may be processed through the configured knowledge-base workflow.

Mitigation: Users should avoid submitting confidential materials unless they accept that processing path and have appropriate authorization.

Risk: Tendering-and-bidding questions can be confused with excluded government procurement matters.

Mitigation: The skill should first check procurement subject, funding source, and project type, then refuse or redirect government procurement goods and services scenarios.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/tendering-bidding-compliance-expert)
- [Publisher profile](https://clawhub.ai/user/chesaram)
- [Feedback issues](https://github.com/一线评标专家/bidding-compliance-advisor/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with XML-style source, legal-basis, risk, and element-analysis tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first compliance guidance with risk tables, source-status tags, and explicit government-procurement boundary handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
