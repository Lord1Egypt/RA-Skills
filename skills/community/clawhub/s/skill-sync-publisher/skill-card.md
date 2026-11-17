## Description:

Safely validate, publish, and track a local SKILL.md directory across GitHub, Awesome Codex Plugins, HOL Registry, skills.sh, SkillsMP, LobeHub, ClawHub, and Cursor Directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyewang](https://clawhub.ai/user/liuyewang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to preflight, publish, update, register, and synchronize one local SKILL.md directory across selected skill marketplaces while preserving user confirmation and platform state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned external npm publisher may change behavior between runs.

Mitigation: Avoid the HOL adapter until @hol-org/registry is pinned, or run it in a restricted environment with minimal credentials.

Risk: Review and checking gaps could allow unintended sensitive files to be published.

Mitigation: Use dry-run mode, manually inspect git diff for the skill directory, and run an independent secret scan before publishing.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review carefully before installing or running authenticated publishing commands.

## Reference(s):

- [Platform matrix](references/platform-matrix.md)
- [Security policy](references/security-policy.md)
- [State schema](references/state-schema.md)
- [ClawHub skill page](https://clawhub.ai/liuyewang/skills/skill-sync-publisher)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local publishing CLIs after confirmation; dry-run and status flows can emit machine-readable JSON.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
