## Description:

面向中国普通高考常规批次考生的腾讯高考志愿填报工具，用于查询一分一段、省控线、院校或专业历年录取数据，并根据省份、分数、位次、选科和偏好生成院校优先或专业优先的冲稳保志愿参考方案及 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and education-support agents use this skill to query Tencent News CLI Gaokao admissions data and prepare regular-batch application references for Chinese Gaokao candidates. It supports score-rank, control-line, school, major, recommendation, and HTML report workflows when the required CLI and API key are available.

### Deployment Geography for Use:

China (CLI-supported provincial regions for regular Gaokao candidates)

## Known Risks and Mitigations:

Risk: The skill directs users to remote installer scripts and operating-system security-warning workarounds.

Mitigation: Install only when TencentNews is trusted, prefer verified downloads with signatures or hashes, and do not bypass Gatekeeper or SmartScreen unless the binary has been independently verified.

Risk: API keys may be exposed if users paste real credentials into shared chats, logs, or command histories.

Mitigation: Use placeholders in guidance, keep real keys local to the user's terminal, and avoid echoing, recording, or sharing credentials.

Risk: Admissions recommendations can be misleading if CLI data is unavailable, incomplete, stale, or outside the skill's regular-batch service scope.

Mitigation: Use only successful, non-empty CLI responses, stop when required data cannot be verified, and require users to independently confirm final admissions decisions with official sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencentnewsteam/skills/tencent-gaokao-college-application)
- [Installation guide](references/installation-guide.md)
- [API Key configuration guide](references/env-setup-guide.md)
- [Update guide](references/update-guide.md)
- [Gaokao HTML interaction reference](references/gaokao-html-interaction-reference.html)
- [Tencent News CLI API Key page](https://news.qq.com/exchange?scene=appkey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with optional local HTML reports and inline shell or PowerShell commands for setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Business results must come from successful Tencent News CLI responses and include the required disclaimer; missing or unsupported data should stop recommendation generation rather than be inferred.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
