## Description:

Comprehensive background investigation and profiling of customers, bloggers, and other individuals.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

External operators can use this skill to generate background-investigation reports for customers, bloggers, partners, vendors, or other individuals, including social profile summaries, content analysis, trust scores, and recommendations. The current artifact uses simulated data and should not be relied on for real decisions about people.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles people and can generate authoritative-looking investigation reports from simulated data.

Mitigation: Treat generated trust scores, verification status, and recommendations as non-decisional demonstration output unless the skill is redesigned around authorized data sources, documented provenance, and human review.

Risk: Background-investigation workflows can create privacy and data-protection exposure when applied to real people.

Mitigation: Require explicit consent or another lawful basis, minimize personal data collection, protect stored reports, and define retention and deletion rules before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/szzg007/skills/szzg007-background-investigation)
- [Publisher Profile](https://clawhub.ai/user/szzg007)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Example Investigation Report](artifact/background_investigation__20260401_224547.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON investigation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include target type, social media summary, content analysis, trust score, verification status, recommendation, key findings, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
