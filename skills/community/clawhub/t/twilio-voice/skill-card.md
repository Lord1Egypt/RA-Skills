## Description:

Twilio Voice gives agents instructions for placing and managing Twilio-backed phone calls, conferences, recordings, IVR sessions, and live call interactions through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to let agents place authorized calls, run IVR or live-call sessions, manage conferences, and retrieve recordings or transcripts for business communication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real outbound calls and alter live calls or conferences.

Mitigation: Require human confirmation for outbound calls, redirects, conference changes, and hangups, and only use phone numbers the operator is authorized to control.

Risk: The skill can record calls, retrieve recordings, and process transcripts.

Mitigation: Configure call-recording consent, transcript retention, access controls, and recording deletion approvals before production use.

Risk: The skill can send DTMF digits or PIN-like input during live calls.

Mitigation: Keep DTMF entry scoped to approved workflows and avoid exposing secrets, wallet data, signatures, payment headers, or other credentials in prompts or logs.

Risk: Caller input in live or IVR sessions could drive unsafe downstream tool use.

Mitigation: Treat caller speech and DTMF as untrusted input, prevent unauthenticated callers from triggering other connected tools, and use callback URL allowlists.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/twilio-voice)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/twilio-voice)
- [Generated Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown instructions with JSON request examples and generated action schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT tool calls may return JSON with call status, transcripts, recording metadata, session summaries, warnings, or validation outcomes.]

## Skill Version(s):

1.0.0 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
