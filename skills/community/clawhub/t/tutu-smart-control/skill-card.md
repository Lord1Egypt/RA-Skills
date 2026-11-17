## Description:

图图智控（TUTU Smart Control） lets an agent remotely view and control a connected Android phone through TUTU hardware for GUI automation, device status checks, communications, file management, and app or settings tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaojiaqi](https://clawhub.ai/user/zhaojiaqi)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to automate and remotely assist with Android phone tasks through a connected TUTU hardware device. Typical tasks include screenshots, taps, typing, app control, SMS or call workflows, location checks, notification review, media and file operations, and basic device management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remotely view and control a connected Android phone through a third-party service.

Mitigation: Install and use it only when the operator expects remote phone control, and verify sensitive actions before execution.

Risk: Several sensitive reads and device-changing actions are not clearly gated according to the security summary.

Mitigation: Treat screenshots, notifications, files, logs, screen recordings, and setting changes as sensitive even when no platform confirmation prompt appears.

Risk: Exposing the TUTU_API_TOKEN or device serial data could allow unauthorized access to the connected device.

Mitigation: Configure TUTU_API_TOKEN through the platform environment settings, avoid pasting tokens or serial numbers into chat, and rotate or revoke credentials when access should end.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaojiaqi/skills/tutu-smart-control)
- [TUTU Smart Control homepage](https://www.szs.chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell/HTTP examples and JSON response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the TUTU_API_TOKEN environment variable and a connected, online Android phone with TUTU hardware.]

## Skill Version(s):

1.3.3 (source: server release metadata; artifact files declare 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
