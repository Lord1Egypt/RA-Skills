## Description: <br>
A local YouTube content management app that helps creators generate topic ideas, scripts, SEO titles, descriptions, tags, thumbnail copy, publishing records, and performance summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baolige2023](https://clawhub.ai/user/baolige2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External YouTube creators and channel operators use this skill to plan videos, generate draft content assets, record publishing metrics, and review recent performance trends from a local web interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unclear payment handling and billing semantics. <br>
Mitigation: Review SkillPay billing behavior before installing or using the skill, and avoid production use until the publisher documents charges, providers, and user consent clearly. <br>
Risk: The security review flags embedded service keys. <br>
Mitigation: Do not rely on bundled credentials; require user-supplied scoped credentials and rotate any exposed keys before deployment. <br>
Risk: The skill contacts SkillPay and SiliconFlow and may share prompts or generated content with third-party services. <br>
Mitigation: Avoid sensitive channel plans or drafts unless data sharing with those providers is acceptable and documented. <br>
Risk: The security guidance calls for disabling public debug serving. <br>
Mitigation: Run only in a controlled local environment and disable debug/public serving before any broader deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baolige2023/youtube-content-manager) <br>
- [SkillPay billing endpoint declared by the skill](https://skillpay.me/api/v1/billing) <br>
- [SiliconFlow chat completions endpoint declared by the skill](https://api.siliconflow.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Configuration] <br>
**Output Format:** [Web UI text and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates draft YouTube planning assets and stores publishing records locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
