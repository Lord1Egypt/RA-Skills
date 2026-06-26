## Description: <br>
V19治理协议公开一致性测试套件v1.0.0。任何外部开发者可零配置运行此脚本，验证Agent是否符合V19治理协议基础认证标准。五套测试：健康检查、自助注册、审计调用、Schema一致性、文档可达性。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to understand and run a zero-configuration V19 governance protocol conformance check covering health, registration, audit calls, schema consistency, and documentation reachability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted package references an external Python conformance script that was not included in the reviewed artifact. <br>
Mitigation: Confirm the script source and inspect V19_Conformance_Test_Suite.py before running it. <br>
Risk: Following the documentation may contact external services and create registration or audit records. <br>
Mitigation: Run the checks only in an environment where contacting the referenced services and creating those records is acceptable. <br>


## Reference(s): <br>
- [V19 Governance Protocol Spec](https://clawhub.com/skills/v19-governance-protocol-spec) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/v19-conformance-test-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The package is documentation-only; referenced test execution may contact external services and create registration or audit records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
