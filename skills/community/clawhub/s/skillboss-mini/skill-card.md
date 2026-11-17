## Description:

Swiss-knife for AI agents with 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, SMS, and smart routing for cost saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skillboss to call hosted AI models and utility endpoints through a single API key for generation, search, parsing, messaging, and model-routing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke external hosted model and utility APIs, which may transmit prompts, files, audio, phone numbers, recipient lists, or other sensitive data outside the agent environment.

Mitigation: Require user approval before sending private, regulated, or secret data through the API, and configure agents to avoid including credentials or sensitive documents in requests unless explicitly approved.

Risk: The skill documents email, SMS, OTP, notification, and batch-send capabilities that can contact real recipients.

Mitigation: Require explicit confirmation before any email, SMS, OTP, notification, or batch-send action, including confirmation of recipient addresses or phone numbers and message content.

## Reference(s):

- [Skillboss API base URL](https://api.heybossai.com/v1)
- [Skillboss website](https://www.skillboss.co)
- [Skillboss ClawHub listing](https://clawhub.ai/yshuolu/skills/skillboss-mini)
- [Publisher profile](https://clawhub.ai/user/yshuolu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl examples, model identifiers, endpoint parameters, and response field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
