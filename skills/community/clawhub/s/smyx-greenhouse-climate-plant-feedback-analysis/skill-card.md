## Description:

Analyzes greenhouse plant images or videos alongside environmental sensor readings and returns structured assessments and climate-control recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Greenhouse operators and automation teams use the skill to assess plant stress from images or videos and sensor readings, review prioritized actions such as irrigation or ventilation, and query prior analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unexplained persistent user and credential handling, as well as possible analysis activity despite a no-analysis option.

Mitigation: Wait for the publisher to explain these behaviors; before use, confirm the no-analysis option does not run analysis and restrict runtime file, network, and shell access.

Risk: Media and identity data may leave the local environment, and security review coverage is partial because a referenced path was missing.

Mitigation: Review outbound data handling and ensure the missing path and all referenced behavior are assessed before installation.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-greenhouse-climate-plant-feedback-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report with findings, prioritized control recommendations, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plant and environmental observations, action priorities, and historical report links.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
