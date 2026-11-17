## Description:

Create new skills, modify existing skills, and validate skill quality for the FlagOS skills repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to scaffold, improve, validate, and evaluate reusable agent skills for the FlagOS skills repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently create or edit agent skills in a controlled skills repository.

Mitigation: Install and invoke it only for intended skill-development work, and review generated changes before committing or publishing.

Risk: Broad natural-language trigger guidance may activate the meta-skill during general skill-development discussions.

Mitigation: Prefer pinned or manually verified installation and explicit invocation when broad automatic activation is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wbavon/skills/skill-creator-flagos)
- [README](artifact/README.md)
- [Skill Writing Guide](artifact/references/writing-guide.md)
- [JSON Schemas](artifact/references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or modify persistent skill files when used by an agent with filesystem access.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
