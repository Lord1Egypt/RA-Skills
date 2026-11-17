## Description:

Call SuperX AI art APIs to generate and edit images, create videos and music, make AI-styled QR codes, and check account balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waitkafuka](https://clawhub.ai/user/waitkafuka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route media-generation requests to SuperX APIs, choose suitable endpoints, build curl requests, and return generated media links with cost or status details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded media URLs, masks, audio or music prompts, and face images may be sent to SuperX and may consume account credits.

Mitigation: Confirm the user wants to use SuperX before generation, check balance when appropriate, and confirm that submitted media and prompts may be sent to the external service.

Risk: API keys could be exposed through shell commands or direct printing.

Mitigation: Use a protected secret mechanism or presence-only check for SUPERX_API_KEY, and never print the API key in logs, terminal output, or responses.

Risk: Face-swap or real-person media workflows may create consent and lawful-use concerns.

Mitigation: Avoid real-person or face-swap requests unless the user confirms consent and a lawful use.

## Reference(s):

- [SuperX API Reference](references/api-reference.md)
- [SuperX Art API Base URL](https://superx.chat/art/imgapi)
- [ClawHub Skill Page](https://clawhub.ai/waitkafuka/skills/superx-art-api)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance, Markdown]

**Output Format:** [Markdown with inline curl commands, JSON request bodies, and generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return external image, video, or music URLs, account balance information, costs, and API error messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
