## Description:

Veo, Veo 3.1 Fast - Google AI video generation models for AI agents. 1080p HD output, reference image support, intelligent audio generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekton](https://clawhub.ai/user/seekton)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to create, stream, poll, list, and inspect Monet API video-generation tasks for Google Veo models, including reference-image workflows and aspect-ratio selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented upload command uses verbose curl output that can expose the Authorization header in logs.

Mitigation: Remove the -v flag unless Authorization headers are safely redacted, and avoid storing command output that may contain secrets.

Risk: Prompts, reference images, and generated content are sent to monet.vision for processing.

Mitigation: Use this skill only for content approved for submission to monet.vision, and keep MONET_API_KEY in a secure environment variable or secrets manager.

## Reference(s):

- [ClawHub Veo Skill](https://clawhub.ai/seekton/skills/veo-skill)
- [Monet API Platform](https://monet.vision)
- [Monet API Keys](https://monet.vision/skills/keys)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance requires MONET_API_KEY and includes asynchronous, streaming, polling, listing, and file-upload API examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
