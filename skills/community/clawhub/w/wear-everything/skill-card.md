## Description:

Creates on-model product images for shoes and accessories by combining a product photo with a model or scene reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and creative teams use the skill to turn footwear and accessory product photos into model-worn product imagery, guided by a model or scene reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product and model reference images may contain identifiable or confidential content and are sent to an external image provider.

Mitigation: Before submitting images, confirm which provider will receive them and review its data policies; use images you are authorized to share and avoid confidential or identifying content when possible.

Risk: The security review notes undeclared tool scope, an unpinned package command, and incomplete scan coverage, leaving some behavior unresolved.

Mitigation: Review the commands, dependencies, and provider configuration before use, and treat the scan result as incomplete rather than as assurance that all behavior was assessed.

## Reference(s):

- [Model flags reference](references/model-flags.md)
- [Provider CLI reference](references/provider-cli.md)
- [dLazy](https://dlazy.com)
- [dLazy CLI source](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Image files, Prompts, Shell commands]

**Output Format:** [Generated JPEG images, with image-generation prompts and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image results depend on the supplied photos, selected provider, and placement guidance.]

## Skill Version(s):

1.0.33 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
