## Description: <br>
Segment CDP integration with API key authentication. Manage sources, destinations, contacts, segments, and tracking events for customer data platform operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to connect Segment through ClawLink, inspect Segment sources and destinations, manage customer data platform resources, and send identify, track, page, screen, group, batch, and import events with user confirmation for writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Segment account and uses sensitive credentials through ClawLink. <br>
Mitigation: Review requested account connections and displayed permissions before installation, and use Segment API keys with the least access needed for the intended workspace. <br>
Risk: Write operations can create, update, delete, revoke, or send data to Segment resources. <br>
Mitigation: Preview and explicitly confirm the target resource and intended effect before any write or destructive operation. <br>
Risk: Identify, track, page, screen, group, batch, and historical import calls can send customer or event data to Segment. <br>
Mitigation: Confirm identities, payload contents, and timestamps before sending data, and avoid placing raw credentials or unnecessary sensitive data in chat. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/segment-cdp) <br>
- [Segment API Documentation](https://docs.segment.io/apis) <br>
- [Segment Sources](https://docs.segment.io/connections/sources) <br>
- [Segment Destinations](https://docs.segment.io/connections/destinations) <br>
- [Segment Identify API](https://docs.segment.io/connections/sources/catalog/libraries/server/http-api/#identify) <br>
- [Segment Track API](https://docs.segment.io/connections/sources/catalog/libraries/server/http-api/#track) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide ClawLink tool calls that read Segment data or perform confirmed write operations against a connected Segment workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
