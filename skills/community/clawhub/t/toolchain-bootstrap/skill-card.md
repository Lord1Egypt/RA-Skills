## Description:

Bootstraps a new OpenClaw container by downloading a prebuilt toolchain archive, extracting it to /workspace, configuring environment variables, and verifying installed language tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize a new container with common development toolchains and to verify or list those tools after setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and extracts an unverified remote binary archive into /workspace.

Mitigation: Install only from a trusted release owner and prefer a version that verifies a pinned checksum or signature before extraction.

Risk: The setup can persistently change shell startup behavior by appending toolchain environment variables to ~/.bashrc.

Mitigation: Review environment changes before use and prefer opt-in PATH changes or a generated environment file that users source explicitly.

Risk: The archive is extracted directly into the workspace without a staging or containment step.

Mitigation: Extract into a staging directory first, inspect the contents, then move the expected toolchain files into place.

## Reference(s):

- [OpenClaw toolchain repository](https://github.com/TurinFohlen/openclaw-toolchain)
- [toolchain_v2.tar.gz release archive](https://github.com/TurinFohlen/openclaw-toolchain/releases/download/v2.0/toolchain_v2.tar.gz)
- [Environment template reference](references/env-template.txt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented setup, verification, and environment configuration guidance for an OpenClaw agent.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
