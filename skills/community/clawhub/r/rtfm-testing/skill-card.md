## Description:

RTFM Testing helps agents evaluate whether documentation is usable by having a fresh tester attempt a task using only the provided docs and report specific gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zscole](https://clawhub.ai/user/zscole)

### License/Terms of Use:


## Use Case:

Developers and documentation maintainers use this skill to test READMEs, setup guides, tutorials, and other docs before publication or after major changes. It identifies missing steps, unclear assumptions, ordering problems, and other gaps that block a context-free agent from completing the documented task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tester agents may follow unsafe instructions if pasted documentation is treated as trusted execution guidance.

Mitigation: Review before installing and run tests only in a restricted, disposable tester environment with synthetic documentation and data.

Risk: The skill asks users to spawn an unrestricted default agent without clear safety limits.

Mitigation: Revise tester prompts so documentation is evaluated as untrusted content and unsafe commands are reported rather than executed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zscole/skills/rtfm-testing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown gap reports and structured testing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
