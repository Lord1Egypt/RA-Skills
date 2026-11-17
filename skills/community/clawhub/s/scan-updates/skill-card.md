## Description:

Scan registered Gitea or Obsidian Git material sources manually or on a schedule, detect added modified or deleted files, create incremental compilation jobs, and update source fingerprints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to detect changes in registered Gitea or Obsidian Git material sources and turn those changes into incremental compilation jobs. It supports both user-triggered scans and scheduled scans for personal or team knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Gitea administrator-backed write authority can allow excessive repository access if the token or invocation path is misused.

Mitigation: Use a least-privilege Gitea token, enforce HTTPS, restrict who can invoke the scripts, and keep scheduler-only actions behind trusted system controls.

Risk: Weak authorization around system identity and standalone deletion actions can let updates or deletion markers be applied outside the intended actor or team context.

Mitigation: Require explicit actor, source, and team authorization checks for system-triggered and standalone deletion flows before exposing the skill to ordinary agent commands.

Risk: Mutable scan input files in temporary paths can let stale or modified update data affect incremental jobs.

Mitigation: Store scan outputs in a controlled location, bind them to the source and actor, validate them before job creation, and use restrictive filesystem permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/scan-updates)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration]

**Output Format:** [Markdown instructions with bash command examples and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OpenClaw context fields and Gitea environment variables to scan sources, create jobs, and report interactive-card payloads.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
