## Description:

AI financial analyst with institutional-grade data covering A-shares, HK stocks, US stocks, ETFs, and indices. Supports real-time quotes, sector/industry analysis, financial metrics, and concept themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17817942676](https://clawhub.ai/user/17817942676)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Stocki to route market-data questions, financial analysis, sector research, and quantitative backtesting tasks through the Stocki CLI and remote gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair and install flows can replace or delete the installed skill from mutable remote sources.

Mitigation: Review before installing or running doctor, and back up local changes before using reinstall paths.

Risk: The API key is sent to whichever gateway URL is configured.

Mitigation: Use the official Stocki gateway unless another endpoint is intentionally trusted.

Risk: Stocki responses and downloaded artifacts come from a remote service, and portfolio details may be sensitive.

Mitigation: Treat outputs as remote service content and include portfolio details only after explicit user consent.

## Reference(s):

- [Stocki ClawHub Skill Page](https://clawhub.ai/17817942676/skills/stocki)
- [Artifact README](artifact/README.md)
- [Artifact Install Guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown analysis, CLI status text, and downloaded report or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instant mode returns direct answers; quant mode can produce task IDs, summaries, reports, and attachments.]

## Skill Version(s):

0.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
