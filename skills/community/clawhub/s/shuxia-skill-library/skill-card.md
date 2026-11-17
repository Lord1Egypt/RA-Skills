## Description:

Use when creating, reviewing, or refining an agent skill and the goal is to make the skill more obedient, better bounded, and harder to misuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[immmmmmortal1](https://clawhub.ai/user/immmmmmortal1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to review, create, or refine agent skills with clearer boundaries, safer fallback behavior, reusable constraint patterns, and concrete revision guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to persist patterns from external skills into a hardcoded user-level Codex skill file without approval or provenance.

Mitigation: Review persistence behavior before installation, change the destination to a user-approved path, and require preview, provenance, and approval before writes.

Risk: Review or revision guidance could introduce incorrect or misleading changes to a skill.

Mitigation: Review generated findings and scan revised skills before deployment.

## Reference(s):

- [Server-resolved source repository](https://github.com/Immmmmmortal1/shuxia_skill_library)
- [ClawHub skill page](https://clawhub.ai/immmmmmortal1/skills/shuxia-skill-library)
- [Publisher profile](https://clawhub.ai/user/immmmmmortal1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review notes, structured analysis, and concrete skill revision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS, WARNING, or ERROR review findings tied to boundary dimensions.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
