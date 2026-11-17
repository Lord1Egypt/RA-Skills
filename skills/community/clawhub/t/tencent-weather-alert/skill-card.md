## Description:

腾讯天气预警 is a one-time Tencent Weather alert and abnormal weather lookup skill for Chinese locations, covering rain, snow, haze, air quality, cold wave, high temperature, and typhoon alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for a one-time weather warning or abnormal weather check for a Chinese location. The skill checks local Tencent News CLI readiness, guides setup when needed, and returns only the current Tencent Weather result without subscription, scheduled checks, proactive push, retries, or fallback sources.

### Deployment Geography for Use:

Global; queries are designed for Chinese locations.

## Known Risks and Mitigations:

Risk: Installation or update instructions may run unverified remote shell or PowerShell code on the user's machine.

Mitigation: Review the installer source and prefer a verified installer, checksum, or signed package; avoid running setup from an elevated or administrator shell.

Risk: The skill requires Tencent API key configuration.

Mitigation: Do not send a real API key to the agent; enter it only in the local terminal after deciding to trust the Tencent CLI and installer path.

Risk: Weather alert answers depend on the current Tencent CLI result and may omit alerts when the CLI returns no warning section.

Mitigation: Treat responses as one-time lookups, keep Tencent Weather source attribution, and do not infer future safety or supplement with alternate data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencentnewsteam/skills/tencent-weather-alert)
- [tencent-news-cli API key page](https://news.qq.com/exchange?scene=appkey)
- [Installation guide](references/installation-guide.md)
- [Update guide](references/update-guide.md)
- [Environment setup guide](references/env-setup-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown or plain text with weather alert details, source attribution, and setup commands when required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-off query result only; no subscriptions, scheduled checks, proactive push, retries, or fallback data sources.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
