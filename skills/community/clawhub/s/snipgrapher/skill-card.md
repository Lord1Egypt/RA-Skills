## Description:

Configure and use snipgrapher to generate polished code snippet images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcollina](https://clawhub.ai/user/mcollina)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to configure snipgrapher and generate reproducible code snippet images for documentation, social posts, changelogs, and release assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run snipgrapher from npm with automatic confirmation, which can execute an unpinned package version.

Mitigation: Pin an exact reviewed snipgrapher package version or install it as a locked project dependency, and review config changes before they are written.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcollina/skills/snipgrapher)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include explicit output paths for generated SVG, PNG, or WebP snippet images.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
