## Description: <br>
QA QuickCheck helps agents run PR-oriented static review, dynamic HTTP checks, regression planning, and structured QA reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houyang995](https://clawhub.ai/user/houyang995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to run quick static checks or standard pre-merge QA flows and produce a structured test report with defects, security observations, regression scope, and gate conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Standard mode and helper scripts can perform active project and network testing that may affect services if pointed at the wrong target. <br>
Mitigation: Run only in an isolated test environment, avoid production services, and review base_url, HTTP test configuration, and any post URL before execution. <br>
Risk: The data factory supports custom JavaScript expressions from templates. <br>
Mitigation: Do not use untrusted template files or the $custom data-factory feature unless the expression has been reviewed. <br>
Risk: Generated or configured HTTP tests can create test data or leave residual records if cleanup is incomplete. <br>
Mitigation: Use dedicated test data, require rollback or cleanup records for writes, and verify cleanup results in the final report. <br>


## Reference(s): <br>
- [QA QuickCheck ClawHub Page](https://clawhub.ai/houyang995/skills/qa-quickcheck) <br>
- [Scheduler and Global Constraints](references/00-调度器.md) <br>
- [Static Code Audit](references/01-静态代码审计.md) <br>
- [Dynamic Functional Testing](references/02-动态功能测试.md) <br>
- [Report Template and Traceability Mapping](references/00-B-报告模板与追溯映射.md) <br>
- [Regression Test Strategy](references/00-D-回归测试策略.md) <br>
- [Test Data Management Strategy](references/00-F-测试数据管理策略.md) <br>
- [QA Pro Suite](https://clawhub.ai/skills/qa-pro-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown test report with structured defect lists, traceability tables, gate conclusions, and inline command/config guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Quick and Standard modes; Standard may run dynamic HTTP checks and regression-focused test planning when the target project environment is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
