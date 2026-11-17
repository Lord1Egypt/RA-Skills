## Description:

Provides daily X (Twitter) entrepreneur influence rankings, follower-growth highlights, recent tweet analysis, 30-day topic summaries, paginated views, HTML reports, and subscription-oriented reporting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Finance media teams, investors, analysts, market teams, entrepreneurs, and professionals use this skill to monitor public X/Twitter entrepreneur rankings, follower-growth movements, recent posts, and topic trends. It helps produce conversational summaries and local HTML reports from RedFox ranking and timeline data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and contacts redfox.hk to retrieve ranking and public X/Twitter timeline data.

Mitigation: Install and run it only when that API-key use and network access are acceptable, and store the key through the documented environment variable configuration.

Risk: Generated reports are saved locally and may open in a browser.

Mitigation: Use --no-open when browser launch is not desired, and review generated report files before sharing.

Risk: The documented subscription feature depends on a separate workflow that is not included in the package.

Mitigation: Treat subscriptions as requiring explicit confirmation and a separately available scheduler or subscription implementation.

## Reference(s):

- [RedFox API reference](references/api_docs.md)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/x-entrepreneur-rank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON data files, local HTML reports, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY for RedFox API calls; generated reports are saved locally and browser opening can be disabled with --no-open.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
