## Description:

Route beginner-friendly natural-language requests for TradeAlpha news and login into the TradeAlpha plugin tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwei2](https://clawhub.ai/user/jiuwei2)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to route natural-language market news and TradeAlpha login requests to the TradeAlpha plugin tools. It is intended for concise news summaries and login/token-refresh flows when the required plugin tools are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News and login requests are sent to the external TradeAlpha service at quantaccess.lxaa.top.

Mitigation: Install only when the user intentionally trusts that service with news queries and TradeAlpha credentials.

Risk: The skill can prompt for account credentials and persist returned tokens in a local config file.

Mitigation: Prefer TRADEALPHA_API_KEY when possible, do not echo passwords or tokens, and review or delete the local token file when token persistence is not desired.

Risk: The README publishing command uses npx clawhub@latest, which can resolve to a newer publisher package.

Mitigation: Pin the clawhub package version before reusing the publishing command.

## Reference(s):

- [TradeAlpha service homepage](https://quantaccess.lxaa.top)
- [ClawHub skill page](https://clawhub.ai/jiuwei2/skills/tradealpha-open-platform)
- [ClawHub publisher profile](https://clawhub.ai/user/jiuwei2)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text summaries with structured tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the TradeAlpha plugin tools tradealpha_news and tradealpha_login; uses TRADEALPHA_API_KEY when available and may rely on local token persistence.]

## Skill Version(s):

0.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
