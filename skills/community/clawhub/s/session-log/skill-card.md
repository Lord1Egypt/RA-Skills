## Description:

Lightweight session logging for OpenClaw agents that creates timestamped session files and appends concise topic summaries during conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meigesir](https://clawhub.ai/user/meigesir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain persistent local conversation summaries across session resets and to support daily multi-agent recap workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent session logs may contain secrets or sensitive personal data if agents write them into summaries.

Mitigation: Keep logs in a known workspace sessions folder and instruct agents not to include secrets or sensitive personal data.

Risk: Local session summaries may be retained longer than intended.

Mitigation: Define and apply a retention or deletion policy for generated session log files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meigesir/skills/session-log)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local Markdown session log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent local session files under a configured sessions directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
