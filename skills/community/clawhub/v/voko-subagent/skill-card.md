## Description:

Creates OpenClaw Gateway subagents to handle VOKO visitor messages using provided prompts or visitor data assembled from a local VOKO database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech-fcc-sys](https://clawhub.ai/user/tech-fcc-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running VOKO in OpenClaw Gateway use this skill to create subagents that draft customer-service replies, route responses to visitor UIDs, suggest intimacy scores, flag owner attention, and update tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callers can influence which local VOKO database path and visitor messages are used, which can expose or mix visitor data if the skill is available to untrusted callers.

Mitigation: Install only in a controlled OpenClaw Gateway, restrict dbPath to an approved directory, and bind requested message IDs to the supplied visitorUid.

Risk: Subagent output can affect reply routing because the result includes a destination UID.

Mitigation: Do not let model output choose the final to_uid; enforce the caller-validated visitorUid when routing replies.

Risk: The release evidence flags vulnerable dependencies and missing privacy guidance for visitor data.

Mitigation: Update vulnerable dependencies before production use and document privacy handling for visitor records, prompts, replies, and tags.

## Reference(s):

- [Voko Subagent ClawHub Release](https://clawhub.ai/tech-fcc-sys/skills/voko-subagent)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON result delimited by ===RESULT=== and ===END=== markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reply text, destination UID, intimacy suggestion, owner-attention flag, attention reason, tag changes, run ID, and status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
