## Description:

OpenClaw update check and upgrade assistant that checks current versus latest versions, analyzes changelog risk and recommendations, and can execute an explicitly confirmed update with pre-update recovery watchdog protection on macOS launchd or Linux systemd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzyling](https://clawhub.ai/user/lzyling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to assess whether an OpenClaw update is available, review changelog risk, and run a guarded update flow with recovery checks after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary watchdog state handling can create local abuse risk on shared machines.

Mitigation: Use a private owner-only state directory, create state files atomically, validate cleanup paths, and avoid loading executable paths from state.

Risk: Execute mode can modify the OpenClaw installation and register temporary user-level recovery jobs.

Mitigation: Require explicit user confirmation, pass ownership and dry-run checks, verify launchd or systemd watchdog arming before update, and clean up state and job artifacts after recovery.

Risk: Long-running OpenClaw subprocesses during update checks or recovery can leave unclear status if they hang.

Mitigation: Keep bounded timeouts around OpenClaw status, doctor, and recovery subprocesses and surface failures for manual review.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/lzyling/skills/update-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and structured JSON consumed from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check mode is read/report only; execute mode requires explicit confirmation and can create temporary user-level recovery jobs.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
