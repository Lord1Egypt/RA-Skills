## Description:

ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径，从快速信息梳理、系统分析到超万字专家报告全流程覆盖，依托多轮推理与多源数据整合，高效完成企业分析、市场洞察、招商研究等复杂任务，一站式提升研究效率与决策质量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhushanwei](https://clawhub.ai/user/zhushanwei)

### License/Terms of Use:


## Use Case:

External users and research teams use this skill to submit research prompts to ZeeLin Deep Research, choose deep or expert research modes, poll for completion, and retrieve generated reports. It is intended for enterprise analysis, market insight, company research, policy review, technical comparison, investment analysis, and similar research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and generated reports are sent to ZeeLin and may include sensitive business content.

Mitigation: Do not submit secrets, regulated data, or sensitive business material unless provider terms and workspace policies have been reviewed.

Risk: The skill retrieves generated reports through returned URLs and may forward downloaded files or copied report text.

Mitigation: Inspect returned report URLs and files before forwarding, and avoid shared hosts or predictable temporary paths for sensitive reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhushanwei/skills/zeelin-deep-research)
- [ZeeLin Deep Research service](https://desearch.zeelin.cn)
- [ZeeLin registration and API key page](https://desearch.zeelin.cn/skill-activity)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, API calls]

**Output Format:** [Markdown with inline bash code blocks and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a DESEARCH_API_KEY credential; generated research reports are retrieved through ZeeLin report URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
