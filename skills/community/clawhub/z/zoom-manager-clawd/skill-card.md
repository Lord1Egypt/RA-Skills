## Description:

Manage Zoom meetings via OAuth API. Create, list, delete, and update events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnagin](https://clawhub.ai/user/vnagin)

### License/Terms of Use:


## Use Case:

Teams and developers use this skill to create, list, inspect, update, and delete Zoom meetings from an agent or CLI using Zoom Server-to-Server OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad account-level Zoom permissions and can create, update, and delete meetings.

Mitigation: Use a dedicated least-privilege Zoom OAuth app, grant only scopes required for the intended workflow, and review sensitive commands before execution.

Risk: Some legacy scripts read Zoom credentials from config.json, which can leave secrets on disk.

Mitigation: Use the environment-variable based CLI path, avoid storing credentials in files, and rotate any secret that was saved in config.json.

Risk: Meeting deletion, meeting updates, and default cloud recording behavior can affect participants and retained meeting data.

Mitigation: Confirm meeting IDs, schedule changes, and recording expectations before running update, delete, or create commands on a real Zoom account.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vnagin/skills/zoom-manager-clawd)
- [Zoom App Marketplace](https://marketplace.zoom.us/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and Zoom OAuth credentials in ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, and ZOOM_ACCOUNT_ID.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
