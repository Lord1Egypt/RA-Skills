## Description:

Seedream Img Gen helps agents generate and save images through ByteDance Seedream models on Volcengine Ark, including text-to-image and Seedream 4.0+ image-to-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anpupil](https://clawhub.ai/user/anpupil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure Volcengine Ark credentials, choose Seedream model parameters, and call the bundled script or API examples to generate images from text or reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation tells users to print `ARK_API_KEY` in the terminal, which can expose secrets through shell history, logs, screen sharing, or copied output.

Mitigation: Verify that the variable is set without printing the secret value, and use a dedicated, low-privilege Volcengine API key for this skill.

Risk: Prompts and reference-image inputs are sent to an external Volcengine Ark image-generation service.

Mitigation: Avoid including secrets, sensitive personal data, confidential source material, or regulated content in prompts and image inputs.

Risk: Generated image URLs and downloaded files come from an external provider.

Mitigation: Treat returned URLs and downloaded files as external content, save them to an intentional path, and review outputs before reuse or publication.

Risk: The bundled script requires third-party Python dependencies.

Mitigation: Install dependencies in a virtual environment and review package sources before running the script.

## Reference(s):

- [Seedream API Reference](artifact/references/api_reference.md)
- [Volcengine Ark Official Documentation](https://www.volcengine.com/docs/82379)
- [ClawHub Skill Page](https://clawhub.ai/anpupil/skills/seedream-img-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with shell and Python code blocks; optional local image files when the generation script is executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Volcengine Ark API access; generated image URLs and downloaded files should be treated as external-provider content.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
