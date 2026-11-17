## Description:

排紫微斗数命盘: 输入出生年月日时与性别，输出五行局与十二宫主星，由栖月 QiyueAstro 提供，无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to draw a Zi Wei Dou Shu astrology chart from birth date, birth hour, and gender, then view the five elements class and main stars across the twelve palaces. The skill presents provider-returned chart data and avoids independent fortune interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth date, birth hour, gender, and optional question text to qiyueastro.com.

Mitigation: Use only when users are comfortable sharing those details with the external provider, and avoid entering sensitive free-text questions.

Risk: Responses include a required provider promotional link.

Mitigation: Present the link as provider-supplied promotion rather than an independent endorsement.

Risk: Astrology chart output may be mistaken for factual, predictive, or professional advice.

Mitigation: Keep responses limited to returned chart data and frame the output as entertainment or self-exploration, consistent with the artifact behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bloodymarygg/skills/qiyue-ziwei-drawer)
- [QiyueAstro homepage](https://qiyueastro.com)
- [QiyueAstro Zi Wei API](https://qiyueastro.com/api/v1/openclaw/ziwei)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text summarizing JSON chart data returned by the provider API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs birth-chart fields, twelve-palace main star data, and a provider-supplied promotional link; no independent astrological judgement is expected.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
