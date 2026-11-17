## Description:

回归测试用例生成器。当软件发生变更时，根据变更影响范围自动推荐需要执行的回归测试用例，并生成优先级排序，帮助测试团队快速聚焦。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnllk](https://clawhub.ai/user/gnllk)

### License/Terms of Use:

MIT-0

## Use Case:

Testing teams, QA engineers, and release owners use this skill to turn a change description into a prioritized regression test checklist with estimated execution time. It is intended for planning regression coverage after code changes, bug fixes, release preparation, and requirement changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation keywords are broad and may surface this skill during general regression testing discussions.

Mitigation: Use it when the user explicitly wants regression test planning or test case recommendations.

Risk: Recommendations come from a fixed built-in template library rather than the user's actual test management system.

Mitigation: Review generated test lists against project-specific requirements, current test inventory, and recent defect history before relying on them for release decisions.

## Reference(s):

- [测试用例优先级判断指南](references/test-case-priority.md)
- [测试用例分类参考](references/test-categories.md)
- [ClawHub skill page](https://clawhub.ai/gnllk/skills/regression-test-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown regression test checklist with priority groups, test case IDs, test types, and estimated execution time.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are generated from a fixed built-in template library and keyword matching.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
