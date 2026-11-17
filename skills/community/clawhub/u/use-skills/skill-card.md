## Description:

Helps choose relevant installed skills for complex requests and briefly shows the working set before answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyrusse](https://clawhub.ai/user/cyrusse)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to select an appropriate working set of installed skills for requests that span planning, implementation, review, testing, writing, design, or documentation. It helps the agent present the selected working set before continuing with one unified result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route multi-domain requests through additional installed skills, which can broaden the guidance used for a task.

Mitigation: Choose Restricted mode when minimal extra skill involvement is preferred, and review the working-set block before continuing.

Risk: Global installation of a third-party meta-skill can affect skill selection across many tasks.

Mitigation: Review the source before global installation and pin the installer and repository revision where possible.

Risk: Ambiguous requests or vague mode wording can lead to a working set that does not match the user's intent.

Mitigation: Ask for an explicit All related, Recommended, or Restricted mode choice before workspace exploration when no reusable prior choice exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyrusse/skills/use-skills)
- [Publisher profile](https://clawhub.ai/user/cyrusse)
- [README](artifact/README.md)
- [Reference](artifact/REFERENCE.md)
- [Example prompts](artifact/examples/prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown, plain text blocks, code snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Begins with a compact mode and working-set block when used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
