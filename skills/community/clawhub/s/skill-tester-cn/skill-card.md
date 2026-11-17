## Description:

skill-tester-cn helps Claude Code users evaluate skills by analyzing skill definitions, generating test cases, running or simulating tests, scoring results, and producing Markdown test reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to test Claude Code skills against their documented triggers, workflows, resources, and expected behavior. It supports structured evaluation by generating test plans, recording observed behavior, assigning scores, and writing a Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actual execution of tests against powerful target skills may trigger the target skill's normal side effects.

Mitigation: Prefer simulated tests or review prompts first, and confirm the target skill scope before allowing actual execution.

Risk: Generated evaluations can be incomplete or misleading if the tested skill's behavior differs from its documentation.

Mitigation: Review the generated test cases, scores, observations, and recommendations before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/skill-tester-cn)
- [README](README.md)
- [Test report template](assets/test-report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown test report with scoring tables and concise evaluation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a timestamped Markdown test report in the current working directory when report generation is requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
