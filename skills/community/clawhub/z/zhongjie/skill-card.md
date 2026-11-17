## Description:

zhongjie is a Chinese-language real-estate advisor agent that helps home buyers clarify requirements, research housing and policy context, compare properties, and maintain browser-visible notes and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morvanzhou](https://clawhub.ai/user/morvanzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External home buyers and real-estate advisors use this skill to structure buyer preferences, research neighborhoods, policies, and market context, and produce property recommendations with supporting notes and map-oriented data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive buyer, family, budget, commute, school, property-search, and map credential data in the local workspace.

Mitigation: Keep the server bound to localhost, do not expose the port on a network, and restrict or rotate AMap credentials.

Risk: The security guidance flags risky WeChat scraping behavior with unresolved TLS validation and domain-control concerns.

Mitigation: Avoid using the WeChat fetcher until TLS validation and domain controls are fixed.

Risk: The dashboard depends on local web content and editable Markdown-style data.

Mitigation: Prefer pinned dependencies and Markdown sanitization before relying on the dashboard.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morvanzhou/skills/zhongjie)
- [Demand dimensions and advisory method](references/dimensions.md)
- [Data file templates](references/data_templates.md)
- [School enrollment policies](references/school_enrollment_policies.md)
- [Map display guidance](references/map_display.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, local JSON data, shell commands, and browser dashboard content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local buyer profile, research notes, recommendation reports, property data, and dashboard configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
