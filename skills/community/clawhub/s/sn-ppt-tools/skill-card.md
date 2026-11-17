## Description:

Use when another PPT Skill needs web search, image search or download, or image generation and the host Agent's equivalent native capability is absent or has failed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this bundled support skill from PPT workflows that need web search, image search, image downloads, or image generation when the host agent's equivalent native capability is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests and image-generation prompts may disclose presentation content to external providers.

Mitigation: Use trusted HTTPS provider endpoints and send only presentation content approved for those services.

Risk: Credentials in a shared user environment file may have broader scope than these tools need.

Mitigation: Set SN_PPT_ENV_FILE to a dedicated configuration file containing only the required settings.

## Reference(s):

- [Capability policy](references/capability-policy.md)
- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-ppt-tools)

## Skill Output:

**Output Type(s):** [JSON, Image files]

**Output Format:** [JSON search results and status objects; downloaded or generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are saved within the caller-provided deck directory.]

## Skill Version(s):

2026.10.29 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
