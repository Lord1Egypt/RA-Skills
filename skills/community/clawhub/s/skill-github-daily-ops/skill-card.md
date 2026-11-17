## Description:

Daily GitHub repo health check + safe Dependabot auto-merge. Outputs markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and repository maintainers use this skill to generate daily GitHub health reports for organization repositories and optionally automate Dependabot PR handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependabot automation may merge pull requests without sufficiently strict severity and CI safeguards.

Mitigation: Use a narrowly scoped GitHub token, restrict execution to intended repositories, and avoid unattended --merge-dependabot runs until the merge policy fails closed on unknown severity, missing CI, and pending CI.

Risk: The shell daily-ops script can push unpushed commits from its configured workspace.

Mitigation: Do not run the shell daily-ops script unless that workspace and remote are intended for automated pushes and local changes have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-github-daily-ops)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and a GitHub token; can target an organization or comma-separated repositories.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
