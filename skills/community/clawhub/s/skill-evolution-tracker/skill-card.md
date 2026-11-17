## Description:

Tracks Nova skill version history, monitors configured expert information sources, and prepares update reports and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catplus-eric](https://clawhub.ai/user/catplus-eric)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to track skill versions, review monitored source updates, and generate Markdown update reports before approving skill changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases could invoke the skill during unrelated skill-management conversations.

Mitigation: Review and narrow activation phrases before deployment if accidental invocation would disrupt normal workflows.

Risk: The skill maintains local version history and generates local report files.

Mitigation: Install it only where local skill history and generated reports are expected, and review the target paths before running the monitoring script.

Risk: The source describes monthly web monitoring, LLM diffing, and enterprise WeChat notifications that the security guidance says should not be relied on unless implemented and approved.

Mitigation: Treat those capabilities as requiring environment-specific implementation review and explicit approval before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catplus-eric/skills/skill-evolution-tracker)
- [Publisher profile](https://clawhub.ai/user/catplus-eric)
- [Navalmanack](https://navalmanack.com/)
- [Rau source profile](https://www.linkedin.com/posts/rauchg)
- [The Vercel Journey with Guillermo Rauch](https://refactoring.fm/p/the-vercel-journey-with-guillermo)
- [Addy Osmani blog](https://addyosmani.com/blog/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON-compatible status data, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local version history and report files when its monitoring script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
