## Description:

Provides guidance, API references, and shell helper examples for generating, editing, upscaling, restoring, and removing backgrounds from images with Bria.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levdavid1](https://clawhub.ai/user/levdavid1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to route image-generation and image-editing requests through Bria.ai, including background removal, product imagery, social assets, image restoration, and automated visual-content pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected images, image URLs, and prompts to Bria.ai.

Mitigation: Use only images and prompts appropriate for a third-party cloud service, and avoid sensitive or regulated content unless approved.

Risk: The skill stores reusable Bria credentials locally.

Mitigation: Restrict permissions on ~/.bria and rotate or remove credentials when they are no longer needed.

Risk: The shell helper relies on local environment variables and API responses while handling authenticated requests.

Mitigation: Run the helper only in trusted environments and avoid use where BRIA_API_BASE or responses could be influenced by untrusted parties.

## Reference(s):

- [API Endpoints Reference](references/api-endpoints.md)
- [Shell Client](references/code-examples/bria_client.sh)
- [Full Bria API Docs for Agents](https://docs.bria.ai/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/levdavid1/skills/test-security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Bria.ai API calls, authentication steps, endpoint selections, and generated image URLs when used by an agent.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact metadata reports 1.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
