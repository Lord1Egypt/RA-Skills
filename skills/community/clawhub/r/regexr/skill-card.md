## Description:

Create, test, and learn regular expressions with live matching. Use when validating patterns, checking groups, generating regex, linting syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Regexr as a command-line helper for creating, checking, explaining, converting, previewing, and documenting regular-expression work. Security evidence indicates the shipped script primarily records local input history and exports rather than implementing the full advertised regex functionality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regex inputs, samples, and exports may contain sensitive text because the script stores local command entries under ~/.local/share/regexr.

Mitigation: Do not use the skill with secrets, customer data, production samples, tokens, or proprietary snippets unless logging is disabled or protected with owner-only permissions.

Risk: The package is advertised as a regex helper, but security evidence says the shipped script mainly provides local history, search, and export behavior with weak controls.

Mitigation: Review the script before installation and verify that required regex checking, generation, linting, and preview behavior is implemented before relying on outputs.

Risk: Exports from ~/.local/share/regexr may preserve sensitive regex patterns or sample data.

Mitigation: Treat exported JSON, CSV, and text files as sensitive artifacts and review or delete them after use.

## Reference(s):

- [Regexr ClawHub page](https://clawhub.ai/bytesagain-lab/skills/regexr)
- [BytesAgain homepage](https://bytesagain.com)
- [Regexr documentation](https://bytesagain.com/skills/regexr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell examples and stdout text from the local CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local logs and exports under ~/.local/share/regexr.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
