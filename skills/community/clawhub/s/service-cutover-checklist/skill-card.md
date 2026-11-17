## Description:

Move a running service to another server: inventory, rehearsal, cutover runbook with measured downtime, rollback paths, and observation before the old copy is retired.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holgergruenhagen](https://clawhub.ai/user/holgergruenhagen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and service operators use this skill to plan and coordinate moving one running application, bot, workflow engine, or API and its data to another server. It helps prepare inventories, a rehearsed cutover runbook, measured downtime, rollback steps, and post-move checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cutover actions can interrupt production service or change external routing.

Mitigation: Keep production switching with the owner, and require approval for each active step after stating its target, action, and expected effects.

Risk: Migration data may contain personal information, and configuration may contain credentials.

Mitigation: Record data counts and checksums rather than records; record credential names and file paths only, never credential values.

Risk: Two active copies could duplicate scheduled jobs or send repeated external requests.

Mitigation: Keep jobs and outbound channels disabled during rehearsal and ensure only one production copy is active at a time.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/holgergruenhagen/skills/service-cutover-checklist)
- [Publisher profile](https://clawhub.ai/user/holgergruenhagen)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown inventories, plans, runbooks, checklists, and reports with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the named service and servers; separates read-only checks from active steps requiring approval.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
