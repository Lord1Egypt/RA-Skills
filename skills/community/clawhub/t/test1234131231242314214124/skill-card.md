## Description:

在代码提交前或任务完成后使用，进行代码审查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lky115](https://clawhub.ai/user/lky115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure Chinese-language code reviews before code submission or after task completion, focusing on correctness, readability, maintainability, testing, and embedded-domain concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked broadly around task completion or submission.

Mitigation: Configure agent skill selection so this checklist is used only for intended code-review workflows.

Risk: Checklist-guided review can miss project-specific correctness, security, or test requirements.

Mitigation: Use the generated review as supporting guidance and keep human or project-specific validation in the release process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lky115/skills/test1234131231242314214124)
- [Publisher profile](https://clawhub.ai/user/lky115)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown review report with severity-grouped findings and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language code review structure with Critical, Important, Minor, and Nitpick severity categories.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
