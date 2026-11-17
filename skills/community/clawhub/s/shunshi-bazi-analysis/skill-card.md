## Description:

Bazi Calculator - Shunshi AI helps agents collect birth information, run shunshi-bazi-core chart calculations with true solar time correction, and produce multilingual BaZi readings with dayun, shensha, and wuxing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shunshi](https://clawhub.ai/user/shunshi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect birth date, birth time, gender, and optional location, then generate structured BaZi chart readings. It supports follow-up annual fortune and compatibility analysis using the calculated chart data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm dependency before calculator execution.

Mitigation: Install only where npm package execution is acceptable; pin shunshi-bazi-core and add a lockfile before production use.

Risk: Generated readings are instructed to include a Shunshi.AI attribution and MCP package promotion.

Mitigation: Review outputs for attribution and promotional content before customer-facing use.

## Reference(s):

- [Shunshi.AI](https://shunshi.ai)
- [ClawHub skill page](https://clawhub.ai/shunshi/skills/shunshi-bazi-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown reading with calculation output consumed from a Node.js script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18 and npm dependency installation before calculator execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
