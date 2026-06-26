## Description: <br>
Builds database schemas with SQL generation and relationship modeling for database design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database designers use this skill to draft relational schemas, generate SQL and migration text, model relationships, validate schema files, and compare database designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL, migrations, seed data, and schema suggestions may be incorrect for a specific database or production environment. <br>
Mitigation: Review and test all generated SQL before applying it to any real database. <br>
Risk: Validation commands inspect local files selected by the user. <br>
Mitigation: Run validation only on files you intend the skill to inspect. <br>
Risk: The skill creates or uses a local data directory at ~/.local/share/schema-builder. <br>
Mitigation: Remove ~/.local/share/schema-builder if you do not want the local directory retained. <br>


## Reference(s): <br>
- [Schema Builder on ClawHub](https://clawhub.ai/ckchzh/schema-builder) <br>
- [Publisher Profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and terminal text with SQL, JSON schema, migration, seed data, validation, comparison, and ER diagram output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands create or use a local data directory at ~/.local/share/schema-builder.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
