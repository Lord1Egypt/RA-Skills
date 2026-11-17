## Description:

Batch queries first-publication image and video material spend for Tencent Ads accounts over a specified date range and returns aggregated performance metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tazdingoooo](https://clawhub.ai/user/tazdingoooo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, analysts, and agents use this skill to query Tencent Ads accounts for first-publication creative spend, impressions, clicks, conversions, and cost metrics across image and video materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may expose Tencent Ads API keys if credentials are pasted into chat or shell history.

Mitigation: Configure credentials through a secure local prompt or official provider flow, and avoid sharing API keys in chat.

Risk: The skill depends on external Tencent Ads tooling and npm installation steps.

Mitigation: Verify Tencent Ads installation links over HTTPS and pin required npm package versions before running setup commands.

Risk: The skill grants access to Tencent Ads reporting data for supplied account IDs.

Mitigation: Install and run it only in environments authorized to access those advertising accounts and review the skill before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tazdingoooo/skills/tencent-first-pub-material-query)
- [Tencent Ads skill installation guide](http://skills.ad.qq.com/install/tencentads.md)
- [Tencent Ads skills portal](https://skills.ad.qq.com/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration guidance]

**Output Format:** [JSON report data with optional Markdown summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Ads account IDs and a start/end date; queries accounts in batches of 20.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
