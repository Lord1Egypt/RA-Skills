## Description:

根据提供的网站页面自动生成测试用例，支持 UI 测试、功能测试、流程测试、异常测试、权限测试和兼容性测试，并可输出 Markdown 表格和 CSV。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linzetai](https://clawhub.ai/user/linzetai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to inspect a supplied web page and generate structured UI, functional, workflow, exception, permission, and compatibility test cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may open and inspect authenticated or private web pages provided by the user.

Mitigation: Confirm the target page and scope before inspection, and avoid exposing sensitive pages or data unless the user has permission.

Risk: The skill may save generated test cases as Markdown or CSV files.

Mitigation: Ask the agent to confirm filenames and output locations before writing files.

Risk: Generated test cases can be incomplete or misleading if dynamic content, modals, permissions, or asynchronous loading are not captured.

Mitigation: Review the generated cases against the live page state and repeat snapshots after key interactions or loading delays.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linzetai/skills/web-test-case-generator)

## Skill Output:

**Output Type(s):** [text, markdown, csv, guidance]

**Output Format:** [Markdown tables and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated test cases may be prioritized as P0, P1, P2, or P3 and organized by feature module, test point, prerequisites, steps, and expected result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
