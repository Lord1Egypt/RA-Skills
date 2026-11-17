## Description:

薪酬调研助手 - 查询岗位薪酬数据并生成分析报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanwan2qq](https://clawhub.ai/user/wanwan2qq)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to query role and city compensation data, compare salary ranges, and generate salary analysis reports. It also supports enterprise compensation data workflows when the user has authorization to upload, query, and export that data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Internal compensation data can be uploaded, queried broadly, or exported in reports without enough scoping safeguards.

Mitigation: Use the skill only with authorized compensation data and approve the sharing audience before query-all operations or report exports.

Risk: The skill executes an external salary-natural binary that is not bundled with the artifact.

Mitigation: Install salary-natural from a trusted, pinned path and verify the executable before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanwan2qq/skills/salary-research)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance]

**Output Format:** [Natural-language responses and reports, with optional Markdown, JSON, text, or CSV output from the salary CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the salary-natural executable; enterprise data uploads, query-all operations, and report exports should be limited to approved data and audiences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
