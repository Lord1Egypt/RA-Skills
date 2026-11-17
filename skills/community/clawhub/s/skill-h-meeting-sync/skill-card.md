## Description:

Runs an OpenClaw cron workflow every 25 minutes to synchronize Tencent Meeting status with Gitea meeting records, handling cancellations, reschedules, new pending meetings, and archival cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining Gitea-based meeting records use this skill to keep repository meeting metadata aligned with Tencent Meeting schedules. It supports recurring automation for detecting cancellations, reschedules, new unassigned meetings, and aged cancelled or rescheduled meeting folders that should be archived.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a powerful Gitea token and can automatically write, update, and delete meeting repository files.

Mitigation: Use a dedicated low-privilege bot token limited to the required repositories and review repository permissions before deployment.

Risk: The default example configuration uses a non-HTTPS Gitea endpoint, which can expose meeting data and credentials in transit.

Mitigation: Configure only an HTTPS Gitea endpoint and reject untrusted or unexpected .env content during setup.

Risk: The cron workflow can automatically change meeting statuses, create pending records, append logs, and archive-delete old meeting files.

Mitigation: Run first against limited repositories, review logs, and keep the documented cancellation and rescheduling checks in place.

Risk: The installer may alter the runtime environment in ways that are harder to audit.

Mitigation: Prefer a pinned virtualenv-based setup before using the skill in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/skill-h-meeting-sync)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [JSON, HTML, Shell commands, Configuration]

**Output Format:** [JSON command responses with status fields, repository paths, archive summaries, and embedded HTML email payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may update or delete Gitea repository files; notification sending is delegated to a separate email skill.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
