## Description:

YOAP (Yongnian Open Agent Protocol) helps agents register human profiles, discover and match with people, exchange messages, coordinate negotiation threads, and use group channels through the yoap.io relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxinran2025-hash](https://clawhub.ai/user/huxinran2025-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to integrate agents with the YOAP relay for profile-based discovery, messaging, negotiation threads, and group coordination between people represented by agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes real-person profile, message, and meetup coordination data through the third-party yoap.io relay.

Mitigation: Use only profile and message details that users are comfortable sending to yoap.io, and avoid precise personal, contact, or meetup details until trust is established.

Risk: Webhook examples may be copied into production without adequate request authentication or abuse controls.

Mitigation: Add signature verification, replay protection, schema validation, rate limits, logging, and human approval before consequential actions.

Risk: Security evidence rates the release suspicious because privacy and authorization safeguards are weakly documented for real-person coordination.

Mitigation: Review the relay's privacy, authorization, and retention behavior before deployment, and keep human approval in the loop for matching, negotiation, and meetup workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huxinran2025-hash/skills/yoap-a2a)
- [Publisher Profile](https://clawhub.ai/user/huxinran2025-hash)
- [YOAP Relay](https://yoap.io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe API requests, webhook handling patterns, profile data, tokens, public keys, and negotiation or channel workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
