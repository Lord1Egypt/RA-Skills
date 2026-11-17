## Description:

Production-safe Ubuntu maintenance orchestrator: runs daily apt security updates, tracks non-security updates across apt/npm/pnpm/brew with quarantine + auto-review, applies only approved updates, rotates logs/state, and generates clear 09:00 MSK Telegram reports (including what was actually installed).

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiceman161](https://clawhub.ai/user/spiceman161)

### License/Terms of Use:


## Use Case:

Developers and system operators use this skill to maintain Ubuntu/OpenClaw hosts, apply security updates, track non-security apt/npm/pnpm/brew updates, and produce daily operational reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs privileged package changes on the host.

Mitigation: Review the privileged command paths and sudoers policy before enabling it; keep dry-run mode enforced until the expected commands and state changes are confirmed.

Risk: Some behavior updates installed OpenClaw skills automatically or during report-related flows.

Mitigation: Require OpenClaw skill updates to run as a separate reviewed action, and keep report generation read-only.

Risk: The scanner guidance calls out mismatches between documented sudo safety claims and actual privileged operations, including autoremove.

Mitigation: Align documentation with the actual privileged commands and remove autoremove or require explicit operator approval for it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spiceman161/skills/sys-updater)
- [README](artifact/README.md)
- [How sys-updater Works](artifact/docs/how-it-works.md)
- [Sudoers Setup](artifact/docs/sudoers.md)
- [Operations](artifact/docs/operations.md)
- [Auto-Review System](artifact/docs/AUTO_REVIEW.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and operational report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write JSON state files and logs when its maintenance scripts are run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
