## Description:

Use the zentao CLI to login and query ZenTao products and bugs. ZENTAO_URL usually includes /zentao.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:


## Use Case:

Developers and teams using ZenTao use this skill to install the zentao CLI, log in to a ZenTao instance, and query products, bugs, bug details, and assigned work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI runs code from the @leeguoo/zentao-mcp npm package.

Mitigation: Install only if the package and publisher are trusted, and prefer a pinned reviewed version when available.

Risk: The login workflow uses ZenTao credentials and writes them to a local configuration file.

Mitigation: Avoid placing real passwords directly in shared shell commands or logs, and verify that the saved config file is readable only by the owner or rotate credentials when needed.

## Reference(s):

- [zentao ClawHub skill page](https://clawhub.ai/leeguooooo/skills/zentao)
- [@leeguoo/zentao-mcp npm package](https://www.npmjs.com/package/@leeguoo/zentao-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide use of JSON output flags exposed by the zentao CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
