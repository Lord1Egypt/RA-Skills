## Description:

Reformat any repo's README to follow the WIP Computer standard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to generate, stage, validate, and assemble README content that follows the WIP Computer standard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deploy path has a command-injection risk when used on an untrusted repository.

Mitigation: Use the skill only on repositories you control, run --dry-run first, review generated README-init-* files, and avoid --deploy on untrusted checkouts until shell command construction is fixed.

Risk: Generated README content may overwrite or move existing documentation during deploy.

Mitigation: Review staged README-init-* files before deploy and keep changes under version control so README and TECHNICAL.md updates can be inspected or reverted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-readme-format)
- [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [Universal Interface Spec](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can stage README-init-*.md files for review, validate README structure, and assemble README.md and TECHNICAL.md during deploy.]

## Skill Version(s):

1.9.72 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
