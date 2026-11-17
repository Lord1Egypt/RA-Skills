## Description:

QuiverAI Quickstart guides agents through configuring a QuiverAI API key, installing the Node.js SDK, and making SVG generation requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charmmm718](https://clawhub.ai/user/charmmm718)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to set up QuiverAI credentials, install the SDK, and make first SVG generation requests through the SDK or REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to QuiverAI's API and successful calls may consume account credits.

Mitigation: Use the skill only with an intended QuiverAI account, review prompts before sending, and monitor account credit usage.

Risk: The skill requires a bearer API key in QUIVERAI_API_KEY.

Mitigation: Store the key in environment or secret management, never commit it, and rotate it if exposed.

Risk: The quickstart installs @quiverai/sdk from npm.

Mitigation: Verify the package source and version before installing in controlled environments.

## Reference(s):

- [QuiverAI Homepage](https://quiver.ai)
- [QuiverAI API Reference](https://docs.quiver.ai/api-reference/introduction)
- [QuiverAI Pricing](https://docs.quiver.ai/api/pricing)
- [QuiverAI Text to SVG Model](https://docs.quiver.ai/models/text-to-svg)
- [QuiverAI Image to SVG Model](https://docs.quiver.ai/models/image-to-svg)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown with inline shell and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QUIVERAI_API_KEY and may describe requests that consume QuiverAI account credits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
