## Description: <br>
A Chinese-language system-dynamics skill that helps agents set system boundaries, identify stocks, flows, feedback, and delays, analyze high-leverage intervention points, and design interventions with second- and third-order effect simulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to structure system-dynamics analysis in Chinese, including system boundary definition, stock-flow mapping, feedback and delay analysis, intervention point evaluation, and markdown report delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms such as feedback loops or leverage points may activate the system-dynamics methodology when the user did not intend it. <br>
Mitigation: Ask for or respect explicit user confirmation before applying the methodology when the request is general or ambiguous. <br>
Risk: System-dynamics reports can become misleading if the agent invents facts, system elements, cases, or data. <br>
Mitigation: Use only verified facts supplied by the user or available evidence, and mark uncertain cases, data, or assumptions as needing verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/system-dynamics) <br>
- [System dynamics catalog and dependency topology](references/system-dynamics-catalog.md) <br>
- [System dynamics methodology requirements](references/system-dynamics-requirements.md) <br>
- [System dynamics exemplar index](references/exemplars.md) <br>
- [M0 task-domain coordination exemplar](references/exemplars/M0-任务域协调范本.md) <br>
- [M1 system boundary exemplar](references/exemplars/M1-系统边界确定范本.md) <br>
- [M2 stock-flow identification exemplar](references/exemplars/M2-存量流量识别范本.md) <br>
- [M3 feedback-delay analysis exemplar](references/exemplars/M3-反馈延迟分析范本.md) <br>
- [M4 high-leverage intervention point exemplar](references/exemplars/M4-高杠杆干预点分析范本.md) <br>
- [M5 result delivery exemplar](references/exemplars/M5-结果交付范本.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, structured analysis tables, dependency flows, and intervention guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language methodology outputs grounded in user-provided facts and explicit uncertainty marking] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
