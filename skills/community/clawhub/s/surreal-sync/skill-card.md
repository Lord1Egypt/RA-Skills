## Description: <br>
Data migration and synchronization to SurrealDB from MongoDB, PostgreSQL, MySQL, Neo4j, Kafka, and JSONL, including full and incremental CDC sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[24601](https://clawhub.ai/user/24601) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to plan and run migrations or synchronization jobs from common data systems into SurrealDB. It helps produce installation commands, source-specific CLI invocations, and configuration guidance for full sync and CDC workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database migration commands can affect production data or copy sensitive records if used against the wrong source or target. <br>
Mitigation: Test against staging first, use least-privilege migration accounts, and verify the selected source, target, namespace, and database before running commands. <br>
Risk: Connection strings and database passwords may be exposed if pasted directly into shell history, logs, or shared prompts. <br>
Mitigation: Use safer secret handling where the CLI supports it and avoid embedding real database passwords directly in shell commands. <br>
Risk: The installed surreal-sync crate or upstream repository may differ from the reviewed skill release. <br>
Mitigation: Verify the crate or upstream repository before installation and prefer a pinned trusted version. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/24601/surreal-sync) <br>
- [surrealdb/surreal-sync upstream repository](https://github.com/surrealdb/surreal-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database connection strings, SurrealDB endpoint settings, namespace and database names, CDC setup notes, and staging-test guidance.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
