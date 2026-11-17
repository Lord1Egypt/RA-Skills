## Description:

Guides an agent to find or update Tokenrouter video model routing, then create and poll video generation tasks through the configured Tokenrouter endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yb98k999](https://clawhub.ai/user/yb98k999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify Tokenrouter channel and model routing for supported video models, apply minimal configuration edits when needed, and run asynchronous video generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify Tokenrouter routing configuration or restart local services.

Mitigation: Require a shown diff and explicit approval before config edits or service restarts.

Risk: The skill may send discovered API credentials, prompts, and image URLs to Tokenrouter endpoints.

Mitigation: Use only the existing server-issued Tokenrouter channel key for the matching endpoint and confirm sensitive prompts, image URLs, and credential scope before requests.

Risk: Incorrect model parameters or routing can cause failed or misdirected video generation requests.

Mitigation: Validate model-specific parameters and endpoint paths before making API calls, and stop on unsupported combinations.

## Reference(s):

- [Tokenrouter Video API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/yb98k999/skills/tokenrouter-generate-video)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed config diffs, API request bodies, polling results, and final video URLs.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
