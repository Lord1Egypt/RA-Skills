## Description:

Diagnoses plant nutrient deficiency or excess based on computer vision and plant physiology, outputs targeted fertilization suggestions for precision nutrient management. | 植物营养诊断技能，基于计算机视觉与植物生理学，通过叶片特征诊断氮磷钾及微量元素缺乏或过剩，输出精准施肥建议

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Growers, agronomy advisors, and agents can use this skill to analyze plant leaf images or videos for nutrient deficiencies, excesses, likely physiological causes, and fertilization suggestions. It can also query account-linked historical diagnosis reports from the cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant images, videos, or URLs are sent to a Life Emergence cloud service for analysis.

Mitigation: Install only when cloud processing is acceptable, disclose the upload behavior to users, and confirm production HTTPS endpoints before deployment.

Risk: The skill can silently create or reuse cloud identities and query account-linked history.

Mitigation: Require explicit consent for account and history actions, and disclose how report history is associated with users.

Risk: Local workspace data may store identity records and tokens.

Mitigation: Review token storage before approval and remove or restrict persistent local credentials unless they are essential.

Risk: Plant nutrition diagnosis may be incomplete or misleading without soil testing and local agronomic context.

Mitigation: Treat results as fertilization guidance and confirm recommendations with soil tests or local agricultural extension advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-nutrition-diagnosis-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API interface documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured diagnosis results, fertilization guidance, cloud report links, and Markdown tables for history queries.]

## Skill Version(s):

1.0.11 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
