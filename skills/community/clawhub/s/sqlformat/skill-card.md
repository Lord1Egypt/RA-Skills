## Description:

Provides a Bash command-line toolkit that claims SQL formatting, linting, validation, conversion, and template workflows while recording command inputs to local logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers may use this skill to record and review SQL-related formatting, linting, validation, dialect conversion, and template workflow notes from the command line. Because the security evidence says the artifacts mainly persist inputs in plaintext logs, use it only with non-sensitive SQL and schema details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL inputs, schema details, customer data, or secrets may be saved in persistent plaintext local logs and exports.

Mitigation: Use only non-sensitive SQL, set SQLFORMAT_DIR to an isolated location, review generated logs and exports, and delete them when no longer needed.

Risk: The security evidence says the artifacts mainly record SQL inputs rather than implement real SQL formatting or linting.

Mitigation: Validate formatting, linting, and migration decisions with a trusted SQL formatter or linter before relying on them in code reviews, migrations, or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/sqlformat)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write and export local plaintext log files under the configured SQLFORMAT_DIR.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
