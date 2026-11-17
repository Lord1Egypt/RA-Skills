## Description:

Use gitcrawl to search duplicate OpenClaw PRs/issues, group related work in prtags, and sync duplicate state to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw maintainers use this skill to assess whether pull requests or issues represent the same problem, gather duplicate evidence, and curate one coherent duplicate group and judgment in prtags. It returns a concise maintainer report and can let configured prtags integration sync group state to GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced companion skill could not be resolved, so scanner evidence is incomplete.

Mitigation: Review the skill contents and any referenced material before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/tag-duplicate-prs-issues)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands]

**Output Format:** [Markdown maintainer report with duplicate evidence, decision, confidence, and prtags actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
