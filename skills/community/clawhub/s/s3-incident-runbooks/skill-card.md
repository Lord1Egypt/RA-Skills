## Description:

Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, incident commanders, and on-call teams use this skill to create or adapt incident response runbooks for detection, triage, mitigation, recovery, escalation, and stakeholder communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example operational commands may affect production systems if copied without review.

Mitigation: Confirm the target service, approval path, backups, rollback plan, and incident commander direction before using database termination, VACUUM, delete, failover, Kubernetes rollout, scaling, or feature-flag actions.

Risk: Generic templates may omit service-specific owners, thresholds, dependencies, and rollback constraints.

Mitigation: Customize placeholders for the service and validate the runbook during review, game days, or post-incident updates before relying on it during a live incident.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/solomonneas/skills/s3-incident-runbooks)
- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable incident runbook templates, escalation matrices, communication examples, and example operational commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
