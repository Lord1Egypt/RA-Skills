## Description: <br>
Sqlformat is a local Bash command-line toolkit for recording SQL formatting, linting, validation, conversion, template, and report activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill as a local command-line utility to record SQL review, style-check, migration, template, and reporting activity during development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL inputs are saved to local plain-text logs, which can retain production queries, secrets, customer data, or sensitive schema details. <br>
Mitigation: Do not enter sensitive SQL or production data, use a controlled local data directory, and regularly inspect or delete ~/.local/share/sqlformat/ logs and exported files. <br>
Risk: The security review says the skill advertises formatting and linting while mostly saving raw SQL inputs rather than acting as a real formatter or validator. <br>
Mitigation: Treat results as local activity records and verify SQL formatting, linting, validation, and dialect conversion with trusted database tooling before relying on them. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [CLI text output, plain-text logs, and optional JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command activity under ~/.local/share/sqlformat/ by default; SQLFORMAT_DIR can change the data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
