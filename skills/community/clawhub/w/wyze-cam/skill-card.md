## Description:

View and control Wyze cameras, including snapshots or thumbnails, siren, floodlight or spotlight, motion and notification toggles, recording, and power, through the unofficial wyze-node API client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelportugal](https://clawhub.ai/user/noelportugal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect named Wyze cameras, retrieve a thumbnail or live snapshot, and perform explicit camera controls such as siren, lights, motion detection, notifications, recording, and power.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private camera imagery and Wyze account credentials.

Mitigation: Install it only in environments where the agent is approved to use those credentials and view camera images.

Risk: The skill can perform state-changing camera controls, including siren, lights, motion detection, notifications, recording, and power.

Mitigation: Require explicit camera names and confirm sensitive actions before execution, especially siren activation or cameras associated with garages or doors.

Risk: Dependency installation may use unpinned packages.

Mitigation: Pin dependencies or install from a reviewed lockfile before deployment.

Risk: Snapshot output paths can be caller-chosen.

Mitigation: Prefer the default temporary snapshot path or restrict output paths to trusted locations.

## Reference(s):

- [Wyze Cam ClawHub Skill](https://clawhub.ai/noelportugal/skills/wyze-cam)
- [wyze-node npm Package](https://www.npmjs.com/package/wyze-node)
- [Wyze Developer API Console](https://developer-api-console.wyze.com/#/apikey/view)
- [wyze-node Client Homepage](https://github.com/noelportugal/wyze-node)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output, thumbnail URLs, status confirmations, and local JPEG snapshot paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Node.js, Wyze credentials, a cached login token, and optional WebRTC dependencies for live snapshots.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
