## Description:

Manages installed skill registration, version tracking, update checks, and update policy configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chsengni](https://clawhub.ai/user/chsengni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register installed skills, track versions, configure update checks, and review available updates before installing or updating skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent memory and installed-skill update records.

Mitigation: Review MEMORY.md and skills_registry.json changes before keeping them, and keep update checks disabled unless needed.

Risk: The skill can contact or fetch updates from insufficiently constrained remote URLs.

Mitigation: Review every update URL, register only trusted GitHub or ClawHub sources, and verify the exact version before cloning or downloading updates.

## Reference(s):

- [Registry Format Reference](artifact/references/registry_format.md)
- [Skill Registry Script](artifact/scripts/skill_registry.py)
- [ClawHub Skill Page](https://clawhub.ai/chsengni/skills/skills-update-manager)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON status records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local skills_registry.json file and update MEMORY.md when actions are run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
