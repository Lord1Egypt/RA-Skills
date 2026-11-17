## Description:

超能文献（Suppr）文档翻译 API。当用户需要翻译文档（Word、Excel、PowerPoint、PDF、TXT、HTML）、查询翻译状态或管理翻译任务时激活。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjg678](https://clawhub.ai/user/zjg678)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to submit documents or document URLs to Suppr for AI translation, then query task status, stop tasks, and retrieve translated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents, document URLs, and task metadata are sent to Suppr's API for translation.

Mitigation: Do not submit confidential files, internal URLs, or URLs containing access tokens unless approved and covered by the provider's retention and privacy terms.

Risk: The skill uses bearer-token authentication for the Suppr API.

Mitigation: Keep API keys scoped, protected, and out of shared prompts, logs, and generated examples.

## Reference(s):

- [Suppr API documentation](https://openapi.suppr.wilddata.cn/introduction.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with API endpoint descriptions, JSON examples, and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference user-provided documents, document URLs, language codes, task IDs, and bearer API keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
