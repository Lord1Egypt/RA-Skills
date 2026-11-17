## Description:

Helps agents and maintainers plan and execute GitHub-style development workflows, including bug fixing, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and teams use this skill to turn GitHub-style workflow requests into actionable plans, code or documentation changes, checklists, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keywords and implicit invocation may activate the skill for generic development requests.

Mitigation: Use it when the request specifically involves GitHub-style issue, PR, CLI, reliability, implementation, or setup-hardening workflows, and confirm scope before acting.

Risk: Generated code changes, commands, or workflow guidance may be incorrect for a specific repository or environment.

Mitigation: Review proposed changes and run the listed verification commands in the target workspace before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-035207)
- [Requirement plan](artifact/references/requirement-plan.md)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [Ask HN: Which GitHub features are needed in a code forge before you can migrate?](https://news.ycombinator.com/item?id=48744529)
- [3 dangers of being locked into a harness. Your context layer is true freedom](https://news.ycombinator.com/item?id=48745664)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with optional code blocks, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the immediate development task and should make assumptions, limits, and verification steps visible.]

## Skill Version(s):

0.20260702.35207 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
