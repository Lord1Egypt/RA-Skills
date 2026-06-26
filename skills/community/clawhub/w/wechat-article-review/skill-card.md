## Description: <br>
文案诊断助手帮助内容创作者、运营、市场营销和媒体团队基于公众号文章草稿、链接或文档生成摘要、诊断结论、行动建议和可复用交付物。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operations, marketing, and media teams use this skill to review WeChat public-account articles and turn drafts, public links, or uploaded documents into summaries, diagnoses, prioritized recommendations, and reusable deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article drafts, uploaded review files, public links, audience and goal details, brand restrictions, tenant metadata, and profile context may be sent to ai-skills.ai under the user's API key. <br>
Mitigation: Use only with data approved for that provider; avoid confidential client work, unpublished proprietary marketing plans, regulated content, or sensitive personal data unless the provider's data handling is approved. <br>
Risk: The security summary flags weak consent boundaries for sending user content to an external AI service. <br>
Mitigation: Confirm the intended invocation and review parameters before execution, especially when the article or surrounding context is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/wechat-article-review) <br>
- [Form schema](references/form-schema.json) <br>
- [Skill configuration](references/skill.json) <br>
- [AI Skills service](https://ai-skills.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command output when invoked through the runner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summaries, diagnostic items, reusable artifacts, and execution metadata; requires AISKILLS_API_KEY for runner execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
