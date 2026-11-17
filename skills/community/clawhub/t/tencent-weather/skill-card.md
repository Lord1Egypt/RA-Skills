## Description:

Weather information lookup tool covering Chinese cities and counties for current weather, forecasts, and weather alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Tencent weather data for Chinese city and county locations, including current conditions, forecasts, lifestyle indexes, traffic restrictions where available, and local weather alerts. The skill also guides users through CLI installation, updates, and local API key setup when the environment is not ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands fetch and execute mutable remote scripts without evidence of signature or checksum verification.

Mitigation: Prefer a versioned, signed, or checksum-verified installer and review the downloaded script or binary before execution.

Risk: The skill depends on a local API key flow for Tencent's news CLI.

Mitigation: Have users enter API keys locally only; do not request, log, echo, or store real API keys in agent responses or reports.

Risk: Weather results and setup behavior depend on the installed CLI state and configured credentials.

Mitigation: Run the provided state check first and stop with actionable setup guidance when the CLI or API key is unavailable instead of switching to another weather data source.

## Reference(s):

- [tencent-news-cli manual installation guide](references/installation-guide.md)
- [tencent-news-cli manual update guide](references/update-guide.md)
- [tencent-news-cli API key configuration guide](references/env-setup-guide.md)
- [API Key acquisition page](https://news.qq.com/exchange?scene=appkey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text, with shell commands when setup or troubleshooting is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather answers should preserve CLI-provided sections and include Tencent weather source attribution when producing user-facing weather results.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
