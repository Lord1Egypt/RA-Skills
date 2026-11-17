## Description:

Validate JSON-exported Tailwind CSS configuration files for structural issues, content path problems, theme misconfiguration, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit JSON-exported Tailwind CSS configs before production builds or CI enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exporting a Tailwind JavaScript or TypeScript config with Node can execute code from an untrusted project.

Mitigation: Use this skill on trusted projects, require a pre-generated JSON config, or run export steps in a disposable environment with no credentials and no network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/tailwind-config-validator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON validator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text, JSON, and summary report formats; strict mode can fail CI on warnings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
