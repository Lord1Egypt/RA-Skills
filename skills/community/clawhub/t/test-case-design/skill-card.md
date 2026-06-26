## Description: <br>
这项技能帮助用户为功能、API、AI Agent 和多平台场景生成、编写、设计并标准化软件测试用例，不涉及测试计划、测试策略或自动化脚本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassianran](https://clawhub.ai/user/cassianran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this Chinese-language skill to produce structured Markdown test cases for functional testing, API testing, AI Agent testing, and platform-specific scenarios. It is intended for test-case design only, not test strategy, penetration testing, load testing, or automation script generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or example test cases may include sample usernames, passwords, bearer tokens, or API keys. <br>
Mitigation: Replace sample credentials and tokens with placeholders before sharing or storing generated test cases. <br>
Risk: Requests mentioning Agent may trigger this skill even when the user only intended a general agent discussion. <br>
Mitigation: Use the skill for explicit test-case design tasks and review Agent-related outputs for relevance before relying on them. <br>
Risk: The skill is focused on test-case writing and does not create test plans, security scans, load tests, or automation scripts. <br>
Mitigation: Use separate planning, security, performance, or automation workflows for those activities. <br>


## Reference(s): <br>
- [Skill definition](SKILL.md) <br>
- [测试用例通用规则](references/templates/common-rules.md) <br>
- [测试用例输出格式规范](references/examples/format-spec.md) <br>
- [功能测试](references/core-capabilities/functional-testing.md) <br>
- [接口测试](references/core-capabilities/api-testing.md) <br>
- [AI Agent 测试](references/core-capabilities/agent-testing.md) <br>
- [通用测试检查清单](references/checklists/common-checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/cassianran/test-case-design) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs standardized test cases and self-check guidance; does not produce automation scripts.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
