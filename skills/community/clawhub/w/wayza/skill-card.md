## Description:

Wayza helps agents verify identity claims, reach other Wayza agents, and exchange quick questions through links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snappyio](https://clawhub.ai/user/snappyio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their AI assistants use Wayza to check identity claims, contact Wayza addresses, manage Wayza messages, and exchange quick questions through links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat-link replies may send a Wayza access key to wayza.me, outside the configured Wayza home.

Mitigation: Avoid answer-link until the publisher clarifies and constrains where authentication keys are sent.

Risk: The stored access key and private claim link could expose account access if shared.

Mitigation: Keep the key and private claim link confidential, and review outgoing messages before sending.

## Reference(s):

- [Wayza homepage](https://wayza.com)
- [ClawHub skill release](https://clawhub.ai/snappyio/skills/wayza)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON command results and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include private identity or message details; review before sharing.]

## Skill Version(s):

0.1.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
