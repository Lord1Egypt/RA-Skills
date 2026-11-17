## Description:

Guides agents through verifying tests and choosing how to merge, push for review, retain, or discard a completed OpenClaw development branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill after implementation is complete and tests pass to select a controlled branch integration path: local merge, push and pull request, retain the branch, or discard the work after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users who do not read Chinese may misunderstand the branch workflow prompts.

Mitigation: Use the skill only when comfortable with Chinese-language Git workflow instructions, or translate and review the prompts before acting.

Risk: The discard path can permanently delete a local feature branch.

Mitigation: Confirm the target base branch, feature branch, and commit list before entering the required discard confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/axelhu/skills/superpowers-finishing-branch)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the user to choose a branch-finishing option and requires explicit confirmation before destructive discard.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
