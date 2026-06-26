## Description: <br>
Zhipu helps agents summarize public ZhipuAI product and documentation pages, including model capabilities, pricing, quotas, and documentation links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to gather lightweight summaries from public ZhipuAI pages, including model capabilities, pricing, quotas, service status, and documentation links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for public ZhipuAI pages only and should not be used for private account data or restricted content. <br>
Mitigation: Use unauthenticated public pages, avoid sign-in flows, and do not provide private account data to the agent. <br>
Risk: Public product, pricing, quota, and documentation pages can change or load dynamically. <br>
Mitigation: Verify important findings against the current public page and wait for dynamic content before summarizing. <br>
Risk: Excessive automated access could violate platform rules or access expectations. <br>
Mitigation: Respect ZhipuAI platform rules and apply conservative request frequency controls. <br>


## Reference(s): <br>
- [ZhipuAI homepage](https://www.zhipuai.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/zhipu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted model, pricing, quota, service-status, and documentation-link fields from public pages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
