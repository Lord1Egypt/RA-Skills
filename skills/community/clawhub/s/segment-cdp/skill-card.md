## Description:

Segment CDP integration with API key authentication. Manage sources, destinations, contacts, segments, and tracking events for customer data platform operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to Segment through ClawLink, inspect Segment sources and destinations, and perform customer data operations such as identify, track, batch import, and write-key rotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an external ClawLink plugin to access a connected Segment workspace.

Mitigation: Install only when the publisher and ClawLink connection are trusted, and verify the plugin publisher and version before enabling it.

Risk: Write-capable operations can create identity and event records, import data, delete sources, or revoke source write keys.

Mitigation: Review write previews and confirm the target resource and intended effect before approving write, destructive, import, or key-rotation actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/segment-cdp)
- [Segment API Documentation](https://docs.segment.io/apis)
- [Segment Sources](https://docs.segment.io/connections/sources)
- [Segment Destinations](https://docs.segment.io/connections/destinations)
- [Segment Identify API](https://docs.segment.io/connections/sources/catalog/libraries/server/http-api/#identify)
- [Segment Track API](https://docs.segment.io/connections/sources/catalog/libraries/server/http-api/#track)
- [ClawLink Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance depends on the live Segment tool catalog exposed through ClawLink.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
