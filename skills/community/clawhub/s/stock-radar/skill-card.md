## Description:

选股雷达 helps agents support A-share stock analysis with 8-dimension scoring, hot-sector scanning, and Dragon-Tiger List capital-flow analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for structured A-share market analysis, including stock scoring, sector hotspot summaries, capital-flow interpretation, and troubleshooting guidance for data/API issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell-command capability and generic file handling beyond the narrow stock-analysis task.

Mitigation: Use it only in an environment where command execution is acceptable, restrict read/exec permissions where possible, and review proposed commands before running them.

Risk: Stock-analysis outputs may rely on external A-share data sources or user-provided API credentials.

Mitigation: Configure only the minimum required data-source credentials, keep keys in environment variables, and verify source data before using outputs for investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/stock-radar)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown with structured JSON examples and troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference API key setup for A-share data sources and may propose command execution or file handling when the host agent permits those tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
