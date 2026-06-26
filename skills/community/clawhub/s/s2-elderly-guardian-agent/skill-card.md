## Description: <br>
S2 零隐私老人健康哨兵，多模态感知并本地记录活动日志，仅向总线广播跌倒预警，不包含任何物理越权操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
S2-CLA <br>


## Use Case: <br>
External caregivers, home-care integrators, and developers use this skill to model an elder-care sentinel that records local activity logs and broadcasts critical fall alerts to a trusted care or smart-home bus. It is intended for assistive monitoring workflows where any physical rescue action remains delegated to a higher-authority system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores activity and health-event logs that may be sensitive in elder-care settings. <br>
Mitigation: Use only with explicit consent from the monitored person or an authorized caregiver, use pseudonymous subject identifiers, restrict file permissions, and define retention and deletion controls before deployment. <br>
Risk: Configured bus broadcasts may transmit health alerts outside the local environment. <br>
Mitigation: Set S2_BUS_ENDPOINT only to a trusted internal service and define clear access rules for any downstream care or smart-home system. <br>
Risk: The skill is assistive fall monitoring and is not a substitute for professional medical devices, caregivers, or emergency services. <br>
Mitigation: Keep human review and higher-authority emergency workflows in the loop, and validate behavior before using it in any real elder-care environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/spacesq/s2-elderly-guardian-agent) <br>
- [S2 Elderly Whitepaper](artifact/S2_ELDERLY_WHITEPAPER.md) <br>
- [Elderly Chronos Dashboard Configuration](artifact/visualizations/elderly_chronos_dashboard.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance, Python code, JSON configuration, local JSON activity logs, and JSON health-alert payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write ADL logs under s2_bas_governance/elderly_care and may post alert payloads to S2_BUS_ENDPOINT when configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
