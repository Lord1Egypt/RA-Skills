## Description:

Guides agents through macOS 12+ SYSU campus workflows that sync supported tasks into Apple Calendar and Apple Reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qybaihe](https://clawhub.ai/user/qybaihe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn SYSU campus scheduling, homework, reservation, career, leave, travel, and work-study requests into checked commands that can create or update Apple Calendar events and Reminders on supported Macs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime is installed from mutable npm package code and can perform write-capable actions against Apple Calendar, Apple Reminders, and SYSU account state.

Mitigation: Install only if the publisher qybaihe is trusted, prefer pinned npm versions, review the resolved package before running npx/npm, and require explicit confirmation before --confirm or Apple-write commands.

Risk: Apple sync depends on macOS Calendar/Reminders permissions and a working native bridge.

Mitigation: Run sysu-anything-apple apple doctor before the first sync or after macOS permission changes, and stop if the doctor check fails.

Risk: Some campus workflows distinguish preview-only, local-import, and remote-write behavior, which can lead to misleading local items if commands are chosen loosely.

Mitigation: Check the relevant SYSU login or status command first, use detail/local-import commands for local-only events, and reserve --confirm for intended remote writes.

## Reference(s):

- [SYSU Anything Apple overview](references/overview.md)
- [Career Apple integration](references/career.md)
- [Libic Apple integration](references/libic.md)
- [ClawHub skill page](https://clawhub.ai/qybaihe/skills/sysu-anything-apple)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON-output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend --json for machine-readable command output; write-capable actions should be gated by runtime checks and explicit confirmation.]

## Skill Version(s):

0.3.6 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
