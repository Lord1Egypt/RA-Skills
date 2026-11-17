## Description:

Guides TikTok product-selection decisions by combining Qinghu product, video, influencer, seller, product-detail, 1688 sourcing, and optional ERP listing workflows into an actionable selection report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and agents use this skill to evaluate TikTok product opportunities across demand, content traction, influencer supply, competition, sourcing, and optional listing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires a Qinghu API token.

Mitigation: Review token handling before installation and provide only the token needed for the intended Qinghu account.

Risk: The workflow can call paid Qinghu tools.

Mitigation: Review the proposed tool list and cost notice before approving calls, and verify reported point costs after execution.

Risk: Larger datasets may be exported to local files or shared through links by default.

Mitigation: Explicitly request no local export or no link sharing when an in-chat summary is sufficient.

Risk: ERP listing actions can distribute selected product links using configured templates.

Mitigation: Confirm listing links, destination accounts, and templates before approving any distribution step.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-tiktok-decision)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with concise recommendations, optional exported table files, and confirmation prompts for paid calls or listing actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product-selection recommendations, supporting data summaries, source and margin notes, ERP listing results, and Qinghu point-cost reporting.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
