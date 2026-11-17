## Description:

Using fixed cameras in a smart greenhouse to analyze plant morphology in real time (e.g., leaf wilting angle, stem uprightness, leaf color changes) combined with environmental sensors (light intensity, temperature, humidity, soil moisture), an AI decision model outputs climate control commands including irrigation (pump/solenoid valve), shade-net opening, fan/wet-curtain on-off, heater on-off, etc. | 通过智能温室中的固定摄像头实时分析植物的形态（如叶片萎蔫角度、茎秆挺直度、叶色变化）以及结合环境传感器（光照强度、温度、湿度、土壤水分），利用AI决策模型输出环境调控指令，包括灌溉（水泵/电磁阀）、遮阳网开度、风机/湿帘启停、加热器开关等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Greenhouse operators and growers can use plant images or videos, optionally with environmental readings, to review signs of water, light, or temperature stress and receive prioritized suggestions for irrigation, shading, ventilation, or heating. They can also review historical analysis reports; recommendations should be checked against local controller safety policies before action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because account, credential, and report-management features are not clearly aligned with its greenhouse-analysis description, and scanners flag unintended external and persistent side effects.

Mitigation: Review and clarify account and credential handling, external media transfers, and export-only behavior before installation; consider avoiding installation until these points are addressed.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-greenhouse-climate-plant-feedback-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured JSON or Markdown analysis with prioritized action suggestions and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plant observations, environmental context, historical report entries, and action priorities; does not provide numeric actuator settings.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
