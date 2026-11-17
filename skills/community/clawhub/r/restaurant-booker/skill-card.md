## Description:

Book restaurant reservations by phone - the agent sends requests to PollyReach, which calls the restaurant, handles the conversation, and returns the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alionkissadeer](https://clawhub.ai/user/alionkissadeer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal assistants use this skill to request restaurant reservations by phone, including time, party size, language, and special requests. It also supports related PollyReach phone-agent workflows such as activation, balance checks, inbound call summaries, and inbound prompt updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broader phone-agent behavior than restaurant booking, including outbound calls, inbound call answering, transcript handling, and prompt updates.

Mitigation: Use it only when that broader PollyReach phone-agent capability is intended, and confirm the user's call target, purpose, and authorization before initiating calls.

Risk: The skill stores a reusable PollyReach token in a local credentials file.

Mitigation: Protect the credentials file, avoid sharing it, and remove or rotate the token when the skill is no longer needed.

Risk: Inbound call polling and transcript retrieval can expose caller content and may create consent or call-recording obligations.

Mitigation: Enable scheduled polling only when explicitly needed, disclose AI call handling where required, and follow applicable consent and privacy requirements before using inbound or recording features.

## Reference(s):

- [Restaurant Booker on ClawHub](https://clawhub.ai/alionkissadeer/skills/restaurant-booker)
- [PollyReach](https://pollyreach.ai)
- [PollyReach Agent Dashboard](https://agent.pollyreach.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, call status, call summaries, transcripts, recording or detail links, balance status, and activation status.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
