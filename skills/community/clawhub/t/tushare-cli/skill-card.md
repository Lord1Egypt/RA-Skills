## Description:

Tushare data query CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoforever](https://clawhub.ai/user/alsoforever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to query Tushare financial data from the command line, including stock basics, financial indicators, daily market data, and financial news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TUSHARE_TOKEN for authenticated requests to an external financial-data API.

Mitigation: Install only when Tushare access is intended, provide the token through the environment, and avoid exposing it in prompts, logs, or shared command history.

Risk: Unreviewed stock-code input can cause unintended API queries or confusing results.

Mitigation: Use normal Tushare stock-code formats and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alsoforever/skills/tushare-cli)
- [Publisher profile](https://clawhub.ai/user/alsoforever)
- [Tushare](https://tushare.pro)
- [Project homepage](https://aigogoai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TUSHARE_TOKEN for authenticated Tushare API requests.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
