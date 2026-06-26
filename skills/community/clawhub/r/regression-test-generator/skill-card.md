## Description: <br>
回归测试用例生成器会根据软件变更影响范围推荐需要执行的回归测试用例，并生成优先级排序，帮助测试团队快速聚焦。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnllk](https://clawhub.ai/user/gnllk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA teams, test engineers, and release owners use this skill to turn software change descriptions into prioritized regression test recommendations with estimated effort. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad regression-testing trigger phrases may activate the skill when the user only mentions testing casually. <br>
Mitigation: Confirm the user intends to request regression test planning before relying on the generated recommendations. <br>
Risk: Regression test recommendations may be incomplete or unsuitable for regulated, safety-critical, or release-blocking decisions. <br>
Mitigation: Review recommendations against project requirements, risk controls, and test management records before relying on them. <br>


## Reference(s): <br>
- [回归测试用例生成器 ClawHub page](https://clawhub.ai/gnllk/regression-test-generator) <br>
- [测试用例优先级判断指南](references/test-case-priority.md) <br>
- [测试用例分类参考](references/test-categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown regression test recommendation list with priorities, test types, and estimated effort] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are generated from a change description and should be reviewed before release decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
