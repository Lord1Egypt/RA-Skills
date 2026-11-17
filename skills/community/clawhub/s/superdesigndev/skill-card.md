## Description:

Superdesign helps frontend developers analyze existing UI, create design-system context, and generate or iterate UI/UX design drafts through the Superdesign CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayzeedesign](https://clawhub.ai/user/jayzeedesign)

### License/Terms of Use:


## Use Case:

Developers and frontend teams use this skill to collect UI context from a repository, establish a design system, create Superdesign drafts, iterate design variations, and prepare implementation guidance after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote instructions can change workflow behavior between runs.

Mitigation: Review fetched guideline files before execution and pin trusted copies for sensitive or regulated projects.

Risk: The workflow may install or update a global npm CLI and require SuperDesign login.

Mitigation: Require explicit approval for global installs or updates and verify CLI authentication state before running design commands.

Risk: The skill can send selected repository source files to the SuperDesign service.

Mitigation: Use a non-sensitive repository or sandbox when possible, and review or redact context files before remote transmission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayzeedesign/skills/superdesigndev)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jayzeedesign)
- [Superdesign Init Guidelines](https://raw.githubusercontent.com/superdesigndev/superdesign-skill/main/skills/superdesign/INIT.md)
- [Superdesign Workflow Guidelines](https://raw.githubusercontent.com/superdesigndev/superdesign-skill/main/skills/superdesign/SUPERDESIGN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated design-context files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .superdesign context files, invoke the Superdesign CLI, and produce design drafts or implementation guidance after user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
