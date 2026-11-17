## Description:

用优稿把链接、主题或正文按自定义流程串成文章，组合生成、降 AI 改写、多图、检测、排版与存稿。适用于链接成文、重复创作流水线、接续保存流程；可复用已授权的本机自动发布设置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

External creators can use this skill to process a chosen saved or custom Yougao workflow for a link, topic, or source text. It returns the workflow results and available article files, reports, and links for continuing the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow steps may spend account credits.

Mitigation: Preview the estimated cost, set an authorized spending limit, and execute within that limit.

Risk: The shared API key remains stored locally until disconnected, and disconnecting does not revoke it.

Mitigation: Use only the permissions needed and revoke the key through the account site when it is no longer needed.

Risk: Optional publishing may be incomplete or reach an unintended destination.

Mitigation: Authorize publishing destinations explicitly and verify the result for each target; a submitted status does not mean public publication succeeded.

Risk: Remote service and PC-client behavior were outside this artifact review.

Mitigation: Check current provider guidance and inspect actual workflow and publishing statuses before treating work as complete.

## Reference(s):

- [API 手册](references/api.md)
- [助手运行指南](references/client.md)
- [安装与使用](references/安装与使用.md)
- [链接成文流程示例](references/link-workflow.json)
- [优稿 AI 接入文档](https://yougao.top/ai.md)
- [优稿 API 契约](https://yougao.top/api/v1/openapi.json)
- [优稿技能使用指南](https://yougao.top/downloads/yougao-skills-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML files, Detection reports, JSON result data, Task and editing links]

**Output Format:** [Article text and workflow results, with Markdown/HTML/TXT files, reports, and links when produced by the selected steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deliverables depend on the selected workflow steps and may include paid services or optional publishing status.]

## Skill Version(s):

1.4.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
