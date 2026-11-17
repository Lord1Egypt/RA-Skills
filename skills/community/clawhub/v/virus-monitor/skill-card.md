## Description:

Virus Monitor helps agents summarize public virus-monitoring signals for Vienna from Austrian wastewater and sentinel surveillance sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to monitor SARS-CoV-2, influenza, and RSV activity for Vienna using public Austrian health dashboards and reports. Its output should be treated as informational monitoring data, not medical advice or an official diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake public virus-monitoring summaries for medical advice or official diagnosis.

Mitigation: Present results as informational surveillance data and direct users to qualified health professionals or official public health guidance for decisions.

Risk: External public health dashboards may be delayed, unavailable, or updated on different schedules.

Mitigation: Communicate source freshness and reporting delays when summarizing trends.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pasogott/skills/virus-monitor)
- [Nationales Abwassermonitoring](https://abwassermonitoring.at)
- [MedUni Wien Sentinel System](https://viro.meduniwien.ac.at)
- [AGES Abwasser Dashboard](https://abwasser.ages.at)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries depend on external public health dashboards that may update weekly or have reporting delays.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
