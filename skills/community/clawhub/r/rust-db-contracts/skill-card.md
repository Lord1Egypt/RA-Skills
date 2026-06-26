## Description: <br>
Guides agents to enforce explicit database contracts for Rust + SeaORM projects, treating Entity files as the complete source of truth for database schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xiamu-ssr](https://clawhub.ai/user/Xiamu-ssr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to design or review Rust + SeaORM entity models and database operations with explicit schema contracts, type-safe fields, checked state transitions, transactional cross-table changes, and soft-delete query filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic database schema synchronization can make unintended changes to shared or production databases. <br>
Mitigation: Use migrations, backups, and review gates for shared or production databases before adopting automatic schema sync. <br>
Risk: The optional CI script uses local pattern checks and may fail builds or miss nuanced database-contract issues. <br>
Mitigation: Review the script rules before enabling CI enforcement and treat warnings as prompts for engineering review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xiamu-ssr/rust-db-contracts) <br>
- [Entity file complete example](references/ENTITY_EXAMPLE.md) <br>
- [Database contract check script](references/check_db_contracts.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Rust and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional local CI checks; review generated code and database schema synchronization plans before applying to shared or production databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
