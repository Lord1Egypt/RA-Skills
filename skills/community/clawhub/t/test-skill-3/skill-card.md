## Description:

Validate a portable OpenClaw skill fixture for skill discovery, supported text files, frontmatter, and bundled-resource loading without external services or credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancymx-dev](https://clawhub.ai/user/nancymx-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automated test maintainers use this skill to validate that an OpenClaw skill fixture is complete, portable, and discoverable before packaging or testing file discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a shell verifier.

Mitigation: Review the script before execution; the server security evidence reports that it only checks bundled fixture files and prints a fixed success message.

Risk: The fixture is intended for local or automated validation rather than general end-user workflows.

Mitigation: Use it only to validate OpenClaw skill packaging, discovery, and bundled-resource completeness.

## Reference(s):

- [Fixture contract](references/fixture-contract.md)
- [Openclaw Test Skill on ClawHub](https://clawhub.ai/nancymx-dev/skills/test-skill-3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text verifier output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled verifier prints a fixed success message when required fixture files are present.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
