## Description: <br>
Applies pending database migration files against the target database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to apply structured schema recommendations, remove selected indexes, and receive a JSON execution report for schema optimization, CI/CD integration, and index maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drop database indexes based on a recommendation file, so incorrect or untrusted recommendations may remove indexes that are still needed. <br>
Mitigation: Preview and approve the exact index list, test on a non-production database copy first, and keep rollback steps for recreating removed indexes. <br>
Risk: Database access with broad privileges could make an unintended recommendation affect production schema state. <br>
Mitigation: Run with least-privilege database credentials, restrict write access to the recommendation file, and audit executed changes before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ink5725/schema-migrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [JSON execution report and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports execution timestamp, indexes migrated, errors, and completion status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
