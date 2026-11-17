## Description:

旅行途中紧急情况行动指南，覆盖护照丢失、航班取消、医疗急救、被盗被抢、自然灾害、交通事故、法律纠纷7大场景，内置55国紧急电话和中国驻外使领馆联系方式，零配置即用。暑假旅行应急指南，领事保护紧急救助

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to look up local emergency numbers, Chinese embassy or consulate contacts, and step-by-step Chinese-language guidance for common overseas travel emergencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emergency numbers and embassy contacts can become outdated or vary by location.

Mitigation: Verify time-sensitive contact information against official local emergency services or consular sources during real emergencies.

Risk: Users may treat the guidance as a substitute for professional medical, legal, or consular assistance.

Mitigation: Use the skill as a first-reference checklist and contact qualified emergency, medical, legal, airline, insurance, or consular authorities as appropriate.

Risk: The artifact declares PROXY_TOKEN even though the security summary indicates no network access and no need for secrets.

Mitigation: Do not provide secrets unless the platform separately documents a concrete runtime requirement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/travel-emergency-guide)
- [Chinese Consular Service Network](http://cs.mfa.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown text, with JSON error responses for unsupported command input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline reference responses for emergency numbers, embassy information, and scenario-based action steps.]

## Skill Version(s):

2.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
