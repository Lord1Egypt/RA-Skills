## Description:

Session Hygiene helps OpenClaw operators prevent sessions.json bloat by archiving stale isolated sessions to daily JSONL files and keeping the live session store lean.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halbotley](https://clawhub.ai/user/halbotley)

### License/Terms of Use:


## Use Case:

Developers and operators managing OpenClaw instances use this skill to configure scheduled or manual cleanup of stale session records while retaining archived history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled job can modify the live OpenClaw session store and may rewrite or delete session records.

Mitigation: Run the script with --dry-run first, back up sessions.json and sessions-archive, and use an explicit --sessions-path before enabling automation.

Risk: The cleanup workflow may lack sufficient atomic-write, locking, or retention safeguards for some deployments.

Mitigation: Review or improve atomic-write, locking, and retention handling before production use.

## Reference(s):

- [Session Hygiene ClawHub Page](https://clawhub.ai/halbotley/skills/session-hygiene)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron setup guidance, script invocation commands, and tuning parameters for session archive retention.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
