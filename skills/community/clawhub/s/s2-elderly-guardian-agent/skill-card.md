## Description:

S2 零隐私老人健康哨兵，通过多模态感知和本地活动日志记录来广播跌倒预警，不执行物理解锁或救援裁定。

This skill is for research and development only.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

S2-CLA

## Use Case:

External caregivers, home-care developers, and smart-home integrators can use this agent to simulate or prototype privacy-preserving elder fall alerts that write local ADL logs and broadcast health events to a trusted local bus. The shipped license restricts commercial deployment without explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records sensitive health and activity events as local ADL JSON logs.

Mitigation: Use only with explicit agreement from the monitored person or an authorized caregiver, and define retention, deletion, and encryption controls before deployment.

Risk: The optional S2_BUS_ENDPOINT can share fall-alert health events with another service.

Mitigation: Configure S2_BUS_ENDPOINT only for a trusted, authenticated local service and verify approved recipients before enabling alert sharing.

Risk: The fall-detection output is assistive and may be wrong or incomplete.

Mitigation: Keep professional medical, caregiver, or upstream controller review in the decision path and do not treat the agent as a replacement for medical devices or personnel.

## Reference(s):

- [S2 Elderly Whitepaper](S2_ELDERLY_WHITEPAPER.md)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-elderly-guardian-agent)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local ADL JSON logs under s2_bas_governance/elderly_care and optionally send JSON health alerts to S2_BUS_ENDPOINT.]

## Skill Version(s):

1.0.3 (source: server release metadata and package.json; SKILL.md and _meta.json list 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
