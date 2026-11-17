## Description:

Task Cost Estimator profiles an AI task, matches it against model options, and estimates cost in value, quality, balanced, or local modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before AI work to choose a cost-effective model for a described task and estimate per-run or daily spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command fetches unpinned code from GitHub.

Mitigation: Install from a reviewed, pinned commit or trusted release in a virtual environment and without elevated privileges.

Risk: The CLI stores aggregate usage history under ~/.hermes/.

Mitigation: Review the local state file policy for your environment and use --reset-bonus when that stored history should be removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/task-cost-estimator)
- [HermesMade repository](https://github.com/minirr890112-byte/HermesMade)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plain text CLI output with task profile, ranked model recommendations, and cost estimates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write aggregate usage history under ~/.hermes/task-cost-history.json when the CLI runs.]

## Skill Version(s):

1.1.0 (source: evidence release and SKILL.md frontmatter; pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
