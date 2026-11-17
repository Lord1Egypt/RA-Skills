## Description:

Start voice calls via the OpenClaw voice-call plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to let agents initiate, continue, speak on, end, and inspect voice calls through the OpenClaw voice-call plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live provider use can place real outbound phone calls and incur provider charges.

Mitigation: Use the mock provider for testing and require confirmation before any real outbound call.

Risk: Incorrect live provider credentials or from-number configuration can route calls unexpectedly or fail at runtime.

Mitigation: Review provider credentials and from-number configuration before enabling Twilio, Telnyx, or Plivo.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockcloud/skills/voiceskill123)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe provider-specific setup for Twilio, Telnyx, Plivo, or mock voice-call providers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
