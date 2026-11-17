## Description:

SysClaw operator skill for processing agent requests, reviewing issues, sending notifications, and managing the system_comm database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to let a SysClaw operator process database-backed agent requests, resolve reported issues, communicate outcomes, and coordinate approved infrastructure actions with human escalation for high-risk cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly approve and execute infrastructure changes over SSH from database requests without sufficiently tight controls.

Mitigation: Install only for a dedicated SysClaw operator with tightly restricted database and SSH credentials, and require human approval for deployments, service mutations, resource creation, software changes, and other high-risk actions.

Risk: Request processing could act on unauthorized or overly broad targets if request shape and target permissions are not constrained.

Mitigation: Add host, package, service, and path allowlists plus typed request schemas and requester-to-target authorization checks before enabling recurring processing.

Risk: Database grants may allow broader operational changes than intended.

Mitigation: Fix the documented worklog database grants and keep SysClaw database privileges limited to the specific tables and columns needed for request resolution, notifications, and audit logging.

## Reference(s):

- [Database Schema Reference](artifact/references/db-schema.md)
- [SysClaw Ops ClawHub Page](https://clawhub.ai/mbojer/skills/sysclaw-ops)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational decision guidance, database queries, permission guidance, and escalation workflow notes.]

## Skill Version(s):

1.6.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
