## Description:

Extracts query parameters from a URL and saves them into a MySQL database for later processing or analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lin-shiwu](https://clawhub.ai/user/lin-shiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to persist URL query parameters into a MySQL table for later processing or analysis. It is suited to single-URL ingestion workflows where database persistence is expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe database defaults could expose or alter MySQL data.

Mitigation: Use a restricted MySQL account and replace the default root/root credentials before running the skill.

Risk: URL-derived identifiers and stored values may create SQL injection or data handling risk.

Mitigation: Use only trusted URLs, validate identifiers before database writes, and avoid URLs containing tokens or personal data.

Risk: Raw query parameters may be printed or persisted without clear user awareness.

Mitigation: Avoid printing raw parameters in shared logs and document what data is stored and retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lin-shiwu/skills/save-mysql)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python script usage and environment configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints insertion status and writes URL query parameter values to a MySQL table.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
