## Description:

Exercise a portable OpenClaw skill bundle in tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancymx-dev](https://clawhub.ai/user/nancymx-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to validate portable OpenClaw skill discovery, supported text files, frontmatter, and bundled resource loading without network services, credentials, or package installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a shell verifier that reads files from the fixture directory and prints validation status.

Mitigation: Run the verifier only against the intended fixture directory after reviewing the bundled script and file inventory.

## Reference(s):

- [Fixture contract](artifact/references/fixture-contract.md)
- [ClawHub skill page](https://clawhub.ai/nancymx-dev/skills/test-skill-5)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text, configuration]

**Output Format:** [Markdown with inline shell commands and fixed text verifier output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled verifier prints a fixed success message when required fixture files are present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
