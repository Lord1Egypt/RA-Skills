## Description:

Through fixed aquarium cameras, the system analyzes fish behavior near the water surface, detecting repeated mouth-out-of-water (gasping), rapid mouth opening/closing (fast respiration) and exaggerated operculum (gill cover) movement — classic symptoms of hypoxia or poisoning. | 通过鱼缸固定摄像头，分析鱼类在水面附近的行为，检测鱼嘴反复探出水面（浮头）、张口快速开合（类似喘气）、鳃盖运动加剧等缺氧或中毒典型症状。当多条鱼同时出现上述行为且持续时间超过设定阈值（默认 60 秒）时，输出'氨氮中毒或缺氧风险预警'，提醒用户立即检测水质、换水或增氧。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium keepers and aquarium or aquaculture operators use it to review fixed-camera footage for visible signs of fish gasping and receive a structured visual risk report with suggested follow-up actions. The report is intended to prompt water-quality checks; it is not a confirmed diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious for account and credential handling and remote-service behavior beyond the stated aquarium-monitoring purpose.

Mitigation: Review the identity and service-request flow before use, and limit access to a dedicated account with only the permissions required.

Risk: Security guidance flags possible footage transfer without clear disclosure and says the supplied code does not establish the stated fish-analysis behavior.

Mitigation: Submit only footage you are authorized to share after confirming upload and retention terms; verify alerts with direct water testing and qualified aquatic-care advice.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-fish-gasping-ammonia-warning-analysis)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured analysis results with visible-behavior cues, risk level, suggested actions, and a report link; text status messages for requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical report queries return structured records.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata; artifact frontmatter reports 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
