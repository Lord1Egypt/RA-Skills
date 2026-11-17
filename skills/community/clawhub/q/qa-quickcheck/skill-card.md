## Description:

AI-driven daily QA assistant for PR static review, dynamic functional testing, regression strategy, and structured test reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houyang995](https://clawhub.ai/user/houyang995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to run quick static checks or standard PR checks that combine static audit, dynamic HTTP testing, Git diff regression scope, and structured defect reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad automatic testing power that can run project code, probe endpoints, and execute test templates.

Mitigation: Use it only on repositories and services you control, preferably in an isolated test environment with minimal environment variables.

Risk: Standard mode may start a project and send dynamic HTTP checks to the configured target URL.

Mitigation: Review and approve startup commands, target URLs, generated configs, and template files before running Standard mode; avoid production targets.

Risk: Untrusted templates or unpinned package downloads can make automated test execution unsafe.

Mitigation: Avoid untrusted templates and unpinned downloads, and review the exact files and commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houyang995/skills/qa-quickcheck)
- [Scheduler and global constraints](references/00-调度器.md)
- [Defect severity and numbering rules](references/00-A-缺陷定级与编号规则.md)
- [Report template and traceability mapping](references/00-B-报告模板与追溯映射.md)
- [Regression testing strategy](references/00-D-回归测试策略.md)
- [Time budget and timeout handling](references/00-E-时间预算与超时处理.md)
- [Test data management strategy](references/00-F-测试数据管理策略.md)
- [Static code audit](references/01-静态代码审计.md)
- [Test design methodology](references/02-0-测试设计方法论.md)
- [Dynamic functional testing](references/02-动态功能测试.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown test report with structured summary, conclusions, defects, and report path fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create test-report.md and temporary test files when the agent follows Standard mode.]

## Skill Version(s):

1.0.3 (source: frontmatter, manifest, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
