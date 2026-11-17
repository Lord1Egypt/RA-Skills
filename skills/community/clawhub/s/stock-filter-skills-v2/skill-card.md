## Description:

Guides an agent through configurable A-share stock screening, factor management, market-data setup, structured results, and export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individual investors, quantitative analysts, portfolio managers, and data analysts use this skill to configure A-share screening criteria, manage factors, process finance data, and export structured screening results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External finance-data APIs and API-key use can expose credentials or sensitive inputs.

Mitigation: Use scoped API keys in environment variables, avoid account-trading credentials, and confirm external API use before execution.

Risk: Broad command execution and exports can run unintended commands or overwrite important files.

Mitigation: Require confirmation before command execution or exports, set explicit output paths and timeouts, and avoid sensitive directories.

Risk: A-share screening results may be incomplete or unsuitable as direct investment advice.

Mitigation: Treat outputs as analysis support and require human review before investment or trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/stock-filter-skills-v2)
- [SkillHub homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, analysis, files]

**Output Format:** [Markdown guidance with structured JSON examples and JSON/CSV-style export instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use external finance-data APIs, environment-variable API keys, command execution, and explicit export paths.]

## Skill Version(s):

1.0.1 (source: evidence.release.version; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
