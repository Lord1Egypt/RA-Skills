## Description:

Orchestrates QA analysis of requirement documents into traceable test cases, coverage reports, and risk assessments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to turn written requirements, attachments, or URLs into test scenarios, traceable test cases, coverage analysis, and reports. The full workflow depends on separately available companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced documents or URLs may expose sensitive information or lead the agent to read unintended files.

Mitigation: Use trusted documents, scope permitted paths and directories, and confirm URL fetches before analysis.

Risk: Installing companion skills via an unreviewed package command may run untrusted code.

Mitigation: Inspect and pin the installation source before running the suggested npx command.

Risk: The workflow may execute a local validation command without adequate confirmation.

Mitigation: Review the validation script and its input path, and approve local command execution before running it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-test-skills)
- [Workflow details](artifact/references/workflow-detail.md)
- [Input routing](artifact/references/routing.md)
- [Output format](artifact/references/format.md)
- [Workflow enforcement](artifact/references/enforcement.md)
- [Depth benchmarks](artifact/references/depth-benchmarks.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown analysis and reports plus UTF-8 CSV test cases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Nine-column CSV; unique test-case IDs and requirement/scenario traceability; coverage is limited to supplied requirements.]

## Skill Version(s):

1.8.0 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
