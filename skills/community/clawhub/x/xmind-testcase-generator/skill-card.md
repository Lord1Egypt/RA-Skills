## Description:

Generates standardized XMind test-case files from requirements documents, with guidance for requirement review, code analysis, priority tagging, and case statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxl1779766474](https://clawhub.ai/user/wxl1779766474)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to turn requirement documents into structured XMind test-case maps, including module breakdowns, numbered steps, expected results, priority markers, and output statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch full requirement documents and inspect relevant local project code.

Mitigation: Invoke it only for explicit XMind test-case generation tasks and confirm the intended source document and repository scope before use.

Risk: The generator script writes generated XMind files under a fixed Desktop path.

Mitigation: Confirm the output location before execution and review generated files before sharing or relying on them.

Risk: The workflow asks the agent to modify the bundled generator script to build case data.

Mitigation: Review script changes before running the generator and keep edits limited to the test-case data function.

## Reference(s):

- [Skill release page](https://clawhub.ai/wxl1779766474/skills/xmind-testcase-generator)
- [gen_xmind.py API reference](artifact/reference.md)
- [XMind test-case generation specification](artifact/xmind-testcase.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance plus Python code edits and generated .xmind files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated XMind files are written by the bundled script, which reports total, smoke, and normal test-case counts.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
