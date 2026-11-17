## Description:

Tencent News integrated information service for news, fact-checking, weather and weather alerts, and Gaokao admission-data queries and application planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Tencent News content, fact-check claims with Tencent Jiaozhen, query China weather and weather alerts, and produce Gaokao admission-data answers or application-planning guidance from the Tencent News CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install or update the Tencent News CLI through remote installer scripts.

Mitigation: Install only when the TencentNews publisher and remote source are trusted; prefer downloading, inspecting, or verifying the installer before execution.

Risk: API-key setup commands can expose secrets if users paste real keys into chat or leave commands in shell history.

Mitigation: Keep real API keys local, use placeholders in agent conversations, and consider clearing or avoiding shell history for key-setting commands.

Risk: Generated Gaokao HTML reports may include CLI-provided logo URLs or other remote resources.

Mitigation: Treat generated HTML as potentially network-capable and review it before opening, sharing, or deploying it in a sensitive environment.

## Reference(s):

- [Tencent News Skill Page](https://clawhub.ai/tencentnewsteam/skills/tencent-news)
- [TencentNewsTeam Publisher Profile](https://clawhub.ai/user/tencentnewsteam)
- [Fact-checking Guide](references/factcheck.md)
- [Weather Query Guide](references/weather.md)
- [Weather Alert Guide](references/weather-alert.md)
- [Gaokao Volunteer Planning Guide](references/gaokao-volunteer.md)
- [Environment Setup Guide](references/env-setup-guide.md)
- [Installation Guide](references/installation-guide.md)
- [Update Guide](references/update-guide.md)
- [Gaokao HTML Interaction Reference](references/gaokao-html-interaction-reference.html)
- [Tencent News API Key Exchange](https://news.qq.com/exchange?scene=appkey)
- [Tencent Jiaozhen AI Fact-checking](https://view.inews.qq.com/ai/agent/UTR2025041800262600?no-redirect=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance, HTML files]

**Output Format:** [Markdown responses with inline shell commands and optional single-file HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in successful Tencent News CLI responses; install, update, and API-key guidance may be returned when the local environment is not ready.]

## Skill Version(s):

1.2.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
