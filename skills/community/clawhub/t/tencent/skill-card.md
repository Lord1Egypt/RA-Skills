## Description: <br>
Navigate Tencent products, Tencent Cloud services, and WeChat ecosystem decisions with region-aware planning and official-source verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business teams use this skill to classify Tencent-related requests, compare Tencent Cloud and WeChat ecosystem options, verify official sources, and plan region-sensitive rollouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save lightweight local Tencent planning notes under ~/tencent. <br>
Mitigation: Review local memory files periodically and avoid saving secrets, billing exports, raw customer data, or copied console tokens. <br>
Risk: Research queries and page requests may be sent to Tencent documentation and product sites. <br>
Mitigation: Use official Tencent sources for product claims and avoid sending sensitive account or customer details in research queries. <br>
Risk: Console, payment, or account-changing actions could affect real Tencent services if approved too broadly. <br>
Mitigation: Require explicit user approval with the exact account, region, and action before any account-level execution. <br>


## Reference(s): <br>
- [Tencent skill page](https://clawhub.ai/ivangdavila/tencent) <br>
- [Tencent corporate site](https://www.tencent.com) <br>
- [Tencent Cloud mainland documentation](https://cloud.tencent.com) <br>
- [Tencent Cloud international documentation](https://www.tencentcloud.com) <br>
- [WeChat developer documentation](https://developers.weixin.qq.com) <br>
- [WeCom documentation](https://work.weixin.qq.com) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/ecosystem-map.md](artifact/ecosystem-map.md) <br>
- [artifact/decision-framework.md](artifact/decision-framework.md) <br>
- [artifact/cloud-platform.md](artifact/cloud-platform.md) <br>
- [artifact/mainland-vs-global.md](artifact/mainland-vs-global.md) <br>
- [artifact/source-validation.md](artifact/source-validation.md) <br>
- [artifact/rollout-checklist.md](artifact/rollout-checklist.md) <br>
- [artifact/setup.md](artifact/setup.md) <br>
- [artifact/memory-template.md](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with decision records, checklists, and occasional shell commands for local setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory file templates and concise decision records when the user approves saved context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
