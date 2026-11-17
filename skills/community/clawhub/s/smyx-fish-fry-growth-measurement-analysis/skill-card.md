## Description:

Analyzes fry images or video containing a known-size reference object to estimate body length and growth rate and produce growth reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquaculture workers and ornamental fish breeders use this skill to track fry body length and growth over time from periodic tank images or videos, then review population statistics and growth reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags account and credential handling, remote identity transmission, and behavior that may not match the stated fry-growth purpose.

Mitigation: Before installation, review account and credential handling, identity transmission, permissions, and export-only behavior; proceed only if you can verify them.

Risk: The security scan was partial and could not resolve one local reference, leaving some evidence incomplete.

Mitigation: Review the unresolved reference and verify the skill's behavior before relying on its outputs.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-fry-growth-measurement-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Structured growth measurements and reports with summaries, statistics, alerts, and report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Measurements depend on a visible known-size reference object and suitable camera positioning.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
