## Description:

Validate a portable OpenClaw skill fixture for discovery, text-file support, frontmatter, and bundled-resource loading without external services or credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancymx-dev](https://clawhub.ai/user/nancymx-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to validate OpenClaw skill discovery, packaging, frontmatter parsing, and bundled-resource loading in local or automated tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle includes a shell verifier that users may execute locally.

Mitigation: Review the verifier before running it; the security evidence indicates it only checks bundled files and prints a success message.

## Reference(s):

- [Fixture contract](references/fixture-contract.md)
- [ClawHub skill page](https://clawhub.ai/nancymx-dev/skills/test-skill-6)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with inline shell commands and plain-text verifier output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No network, credential, package-install, or external-service dependency.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
