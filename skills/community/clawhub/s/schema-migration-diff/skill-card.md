## Description: <br>
Analyze differences between knowledge graph schema versions and generate migration plans and scripts for safe schema evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to compare knowledge graph schema versions, identify entity, property, relationship, and constraint changes, and plan migrations for RDF, OWL, or property graph systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Cypher, SPARQL, or Python migrations could change production graph data in unintended ways. <br>
Mitigation: Run generated scripts in staging first, keep current backups, and prepare a rollback path before production execution. <br>
Risk: Property rename or removal steps can cause data loss if copied fields are not validated first. <br>
Mitigation: Validate migrated values and keep deprecated properties during a transition period before removing old fields. <br>
Risk: Schema diff output may miss domain-specific constraints or operational dependencies that are not present in the supplied schemas. <br>
Mitigation: Review the diff report and migration plan with graph owners before execution, especially for constraints, cardinality changes, and relationship direction changes. <br>


## Reference(s): <br>
- [Migration Patterns](artifact/references/migration-patterns.md) <br>
- [Example Migrations](artifact/examples/example-migrations.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/schema-migration-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with Cypher, SPARQL, or Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated migration scripts should be reviewed, tested on staging data, and paired with backups and rollback plans before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
