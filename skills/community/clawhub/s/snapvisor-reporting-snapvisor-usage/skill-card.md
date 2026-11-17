## Description:

Reports SnapVisor account builds, screenshots, project usage trends, members, and pending invites without changing account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

SnapVisor account users can review build and screenshot counts, usage trends by project and period, and, when authorized, team members and pending invites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Team reports can expose member and pending-invite information.

Mitigation: Request team details only when needed and review the SnapVisor OAuth scopes, especially account:admin.

## Reference(s):

- [Reporting Snapvisor Usage on ClawHub](https://clawhub.ai/devino/skills/snapvisor-reporting-snapvisor-usage)
- [devino publisher profile](https://clawhub.ai/user/devino)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Short report with totals, a period trend table, and optional project and team details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; reports only returned data and does not estimate costs.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
