## Description: <br>
TikTok Shop influencer analytics, product selection, and content strategy toolkit that fetches creator data via EchoTik API, optionally fetches product trending data via TikTok Shop Partner API, then generates multi-region analysis reports, influencer collaboration plans, prioritized product selection lists, and video hook strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skovely](https://clawhub.ai/user/skovely) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and commerce analysts use this skill to gather TikTok Shop creator and product market signals, compare regions, plan influencer collaborations, prioritize products, and draft video hook strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user-provided EchoTik credentials and may use a TikTok Shop access token. <br>
Mitigation: Use limited-scope credentials where possible, rotate credentials regularly, and avoid exposing tokens in shared prompts, logs, or generated reports. <br>
Risk: Selected categories and regions are sent to EchoTik and, when product mode is enabled, TikTok Shop APIs. <br>
Mitigation: Confirm that the selected market data can be shared with those services before running the skill. <br>
Risk: Generated reports may include commercial strategy, creator data, product selections, or forecasts. <br>
Mitigation: Write reports to a dedicated output directory, review them before sharing or acting on them, and apply appropriate access controls. <br>
Risk: External API availability, permissions, rate limits, or token expiry can affect report completeness. <br>
Mitigation: Verify credentials, endpoint access, and API responses before relying on generated recommendations. <br>


## Reference(s): <br>
- [ClawHub Release](https://clawhub.ai/skovely/tiktok-trendslayer) <br>
- [API Reference](references/api_docs.md) <br>
- [Advanced Workflow Guides](references/workflows.md) <br>
- [Output Format Examples](references/output_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown reports; workflow guidance may support PDF or Excel deliverables with additional tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ECHOTIK_AUTH_HEADER for EchoTik data; TIKTOK_SHOP_API_KEY enables product data; writes generated reports to a local output directory.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
