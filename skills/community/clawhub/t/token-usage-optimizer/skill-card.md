## Description: <br>
Maximize your Claude Code subscription value with smart usage monitoring and burn rate optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rusel95](https://clawhub.ai/user/rusel95) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code subscribers use this skill to monitor five-hour and seven-day usage quotas, receive threshold alerts, and judge whether their subscription usage is under, over, or on pace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Claude OAuth tokens and local Claude credential files. <br>
Mitigation: Review the scripts before installation, restrict token files to owner-only permissions, and rotate tokens if exposure is suspected. <br>
Risk: The cron workflow can silently interact with local Claude authentication state. <br>
Mitigation: Use the cron workflow only after review, or run reports manually when automatic credential checks are not acceptable. <br>
Risk: Browser-token extraction can expose password-equivalent OAuth credentials. <br>
Mitigation: Prefer Claude CLI authentication and avoid copying browser tokens unless the operational risk is understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rusel95/token-usage-optimizer) <br>
- [Anthropic OAuth Usage API](references/api-endpoint.md) <br>
- [Token Extraction Guide](references/token-extraction.md) <br>
- [Claude Code Subscription Plans](references/plans.md) <br>
- [Claude Code Pricing](https://claude.ai/pricing) <br>
- [Anthropic API Docs](https://docs.anthropic.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text usage reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cached usage percentages, alert state, and human-readable reports; setup scripts configure local OAuth token storage.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
