## Description:

Regression testing framework for AgentSkills that analyzes a target skill, runs script-layer assertions and AI-layer semantic scoring, and outputs a Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to regression test AgentSkills by running script assertions, simulated or real agent checks, and Markdown reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regression tests can run shell commands from TEST.md or generated cases.

Mitigation: Run only in a disposable sandbox or against trusted skills, inspect TEST.md and generated cases first, and avoid executing generated script_cmd values.

Risk: The OpenClaw backend can create a cron probe job for agent integration testing.

Mitigation: Force --backend api when OpenClaw cron behavior is not intended, and review or remove any probe jobs after testing.

Risk: A report upload hook can execute a user-provided script.

Mitigation: Set SR_REPORT_UPLOAD_HOOK only to a trusted script and review the upload destination before sharing reports.

Risk: LLM-as-judge scores are directional and may not be reliable for high-stakes decisions.

Mitigation: Use detailed reports and human review before relying on regression results for release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/skill-regression)
- [TEST template reference](references/TEST_template.md)
- [Report structure reference](references/report_structure.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports with JSON result files, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run script-layer tests, AI-layer scoring, optional OpenClaw agent checks, and an optional trusted report upload hook.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact SKILL.md Version field)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
