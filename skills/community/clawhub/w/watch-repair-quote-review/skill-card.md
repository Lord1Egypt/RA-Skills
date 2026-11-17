## Description:

Reviews watch-repair quotes against Wuhan Hengdeli public price references and real cases, separates customer-supplied facts from evidence, and produces cautious questions to ask before repair approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickyanyufei](https://clawhub.ai/user/nickyanyufei)

### License/Terms of Use:

MIT-0

## Use Case:

External watch owners and repair customers use this skill for a preliminary quote review before approving maintenance, battery replacement, parts work, polishing, strap work, or fault repair. It compares the quote with dated Wuhan Hengdeli source evidence, flags missing scope details, and suggests questions to ask the repairer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on one Wuhan repair shop's public pricing and case evidence, not nationwide market averages or official brand pricing.

Mitigation: Present results as a preliminary comparison against the cited Wuhan source, preserve source dates and conditions, and avoid claims of market-average or official pricing.

Risk: Quote reviews based on photos, fault descriptions, or quote sheets cannot establish the exact internal fault or final repair cost.

Mitigation: Separate customer-supplied facts from evidence, keep diagnoses conditional, and state that physical inspection or open-case examination may be required.

Risk: Local source files or live website lookups are evidence-gathering inputs that can affect the review.

Mitigation: Use the official HTTPS source or an audited local snapshot, validate source structure, and keep source URLs visible in the final answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickyanyufei/skills/watch-repair-quote-review)
- [Wuhan Hengdeli official website](https://www.wuhanhengdeli.cn)
- [Wuhan Hengdeli structured evidence JSON](https://www.wuhanhengdeli.cn/ai-card.json)
- [Wuhan Hengdeli public price reference](https://www.wuhanhengdeli.cn/price)
- [Wuhan Hengdeli estimator](https://www.wuhanhengdeli.cn/estimate)
- [Wuhan Hengdeli repair cases](https://www.wuhanhengdeli.cn/cases)
- [Evidence and citation rules](references/evidence-policy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with source-linked price or case summaries and numbered follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains source dates, conditions, insufficiency labels, and preliminary-inspection limitations.]

## Skill Version(s):

1.0.3 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
