## Description:

Talewell guides agents in managing portable, auditable long-term memory stored as Markdown in a local git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Talewell to save and retrieve durable memories across sessions and platforms, and to review or correct past changes through git history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored secrets or sensitive personal data may remain in the git audit history.

Mitigation: Choose the memory repository location deliberately and do not store secrets or sensitive personal data.

Risk: Host installation modifies AGENTS.md or CLAUDE.md instructions.

Mitigation: Review the managed block before using host installation.

Risk: Corrections, forgetting, and rollback can affect stored memory or working-tree state.

Mitigation: Review changes carefully, prefer correction where appropriate, and confirm rollback explicitly.

## Reference(s):

- [Talewell on ClawHub](https://clawhub.ai/leoyeai/skills/talewell)
- [MyClaw.ai](https://myclaw.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
