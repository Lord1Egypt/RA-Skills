## Description:

Bria AI helps agents generate and edit images through Bria.ai APIs, including background removal, product imagery, upscaling, restyling, restoration, and batch visual-asset workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operations teams use this skill to generate, transform, and automate image assets through Bria.ai, including transparent cutouts, marketing visuals, e-commerce product photography, and photo restoration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and images may be sent to Bria.ai as a third-party service.

Mitigation: Use only approved images and prompts, and avoid sensitive personal or proprietary content unless the user has authorization.

Risk: Persistent Bria credentials are stored in ~/.bria/credentials.

Mitigation: Use the skill in a trusted single-user environment, protect the credentials file, and remove cached credentials when they are no longer needed.

Risk: The shell helper supports configurable API base and asynchronous status URL behavior.

Mitigation: Review the shell helper before use and keep the default Bria API endpoint unless a trusted deployment requires otherwise.

## Reference(s):

- [Bria Homepage](https://bria.ai)
- [ClawHub Skill Page](https://clawhub.ai/galbria/skills/test-should-be-removed)
- [Bria API Reference for Agents](https://docs.bria.ai/llms.txt)
- [API Endpoints Reference](references/api-endpoints.md)
- [Shell Client](references/code-examples/bria_client.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets and API call examples; API calls return image URLs or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and BRIA_API_KEY; may use ~/.bria/credentials for cached Bria credentials.]

## Skill Version(s):

0.0.2 (source: server release metadata; artifact metadata version 1.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
