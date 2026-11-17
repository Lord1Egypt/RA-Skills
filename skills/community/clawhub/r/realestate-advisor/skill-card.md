## Description:

Realestate Advisor helps property owners, buyers, and home-switching users interpret real-estate market data through valuation ranges, comparable transactions, listing competition, market state, and decision signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External property owners, prospective buyers, and users planning a sale-and-purchase transition use this skill to request structured real-estate asset analysis, buyer affordability and property assessment, offer strategy, or transition risk guidance. The skill is intended to translate market signals into decision support, not to provide an official appraisal or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic maintenance behavior can delete old logs or cleanup workspace files.

Mitigation: Review and scope heartbeat maintenance before enabling the skill, and keep backups or approval controls for any file deletion workflow.

Risk: Persistent memory updates can retain user corrections or transaction context.

Mitigation: Avoid uploading account details, personal identifiers, unnecessary private addresses, or transaction metadata, and review retained memory before reuse.

Risk: Real-estate outputs may be incomplete or misleading when public market data is stale, sparse, or low confidence.

Mitigation: Require visible data sources and confidence notes, treat outputs as market reference only, and confirm material decisions with qualified local professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/realestate-advisor)
- [Publisher profile](https://clawhub.ai/user/perrykono-debug)
- [Skill definition](artifact/SKILL.md)
- [Runtime methodology](artifact/SOUL.md)
- [Data acquisition guidance](artifact/TOOLS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reports with structured sections, tables, valuation ranges, confidence notes, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded in cited market data or user-provided evidence, use ranges rather than single-point valuations, and show confidence limits.]

## Skill Version(s):

2.0.3 (source: ClawHub release evidence; artifact documentation references v2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
