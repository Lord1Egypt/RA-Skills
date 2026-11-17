## Description:

Generate Unraid DockerMan user template XML files from structured input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashanzzz](https://clawhub.ai/user/ashanzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Unraid administrators use this skill to generate DockerMan XML templates for container images, including ports, volumes, environment variables, web UI settings, and optional deployment to the Unraid template directory after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DockerMan XML or startup overrides could change how a container starts or runs.

Mitigation: Inspect generated XML before import and avoid ENTRYPOINT bypass unless it is specifically needed.

Risk: User-controlled output paths, Docker parameters, startup commands, and volume mappings could lead to unsafe container settings or arbitrary writable file overwrite.

Mitigation: Use only trusted inputs, pin Docker images, and require explicit user review before choosing --output, --extra-params, --post-args, startup commands, or volume mappings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashanzzz/skills/unraid-xml-generator)
- [Skill definition](artifact/SKILL.md)
- [Template generator script](artifact/scripts/generate_template.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with XML snippets, shell commands, and generated Unraid DockerMan XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated XML should be inspected before import or deployment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
