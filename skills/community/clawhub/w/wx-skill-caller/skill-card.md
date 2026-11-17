## Description:

Forwards free-form chat, Chinese questions, help requests, conversational messages, and other general text input to the WX backend skill API and returns the backend JSON response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heqq-github](https://clawhub.ai/user/heqq-github)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to hand ordinary chat, Chinese-language questions, help requests, and other open-ended text to a third-party WX backend service. It is not intended for tasks that explicitly require local file editing, shell execution, web search, image analysis, or media generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad user messages may be sent to an external WX backend, including secrets, credentials, private business data, regulated data, or content intended to remain local.

Mitigation: Use only with clear opt-in for external processing and avoid sending sensitive, regulated, private, credential, or local-only task content.

Risk: The agent receives responses controlled by the external backend, creating response-control and reliability concerns.

Mitigation: Review returned JSON before relying on it, and route file editing, shell execution, web search, image analysis, and media generation requests to direct agent tools as described by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heqq-github/skills/wx-skill-caller)
- [WX backend API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON response or JSON error object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts a single content string to the external WX backend with a 30-second timeout; HTTP, network, and JSON parsing failures are returned as structured JSON errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
