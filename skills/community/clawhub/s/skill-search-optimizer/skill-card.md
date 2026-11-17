## Description:

Optimize agent skills for discoverability on ClawdHub/MoltHub. Use when improving search ranking, writing descriptions for semantic search, understanding how the registry indexes skills, testing search visibility, or analyzing why a skill isn't being found.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and skill publishers use this skill to improve ClawdHub skill discoverability by writing searchable descriptions, testing registry search results, and comparing competing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm CLI commands can change behavior between runs.

Mitigation: Pin and verify the molthub CLI version before running commands from the skill.

Risk: Installing competing skills without review can introduce untrusted content into the local workspace.

Mitigation: Inspect competitor skills before installing them and use a sandbox with minimal filesystem and environment access.

Risk: Publishing local skill contents could expose unintended sensitive material.

Mitigation: Check local skill files for secrets before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/skill-search-optimizer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and checklist-style review prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx for the documented molthub CLI examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
