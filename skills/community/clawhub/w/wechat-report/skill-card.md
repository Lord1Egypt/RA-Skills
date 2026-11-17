## Description:

Generates a structured comparison report for multiple WeChat Official Account articles under one topic, including article metadata, engagement status, content structure, writing tags, and optional downstream Feishu sync preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Content and marketing operators use this skill to compare several WeChat Official Account articles for a topic, inspect engagement availability, and summarize reusable writing patterns. Agents can use it to turn a frontmatter-based request into a local Markdown report and raw JSON dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network and browser automation are under-scoped and may access arbitrary URLs from request Markdown or seed URLs.

Mitigation: Run only in a sandboxed workspace, review request Markdown and seed URLs before execution, and prefer versions that enforce mp.weixin.qq.com URL allowlisting and redirect validation.

Risk: The Playwright profile can reuse browser session state under .cache/wechat-report-playwright.

Mitigation: Avoid logging into accounts through the reused profile unless that session reuse is acceptable, or use a temporary browser profile and clear cached browser state after use.

Risk: Dependency provenance is harder to review because pinned dependency lockfiles are not included in the artifact evidence.

Mitigation: Install dependencies in an isolated environment and review dependency versions before running the skill.

## Reference(s):

- [Wechat Report on ClawHub](https://clawhub.ai/abigale-cyber/skills/wechat-report)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, json, guidance]

**Output Format:** [Local Markdown report plus raw JSON data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a comparison report and raw structured data under content-production/inbox; Feishu sync is prepared but requires separate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
