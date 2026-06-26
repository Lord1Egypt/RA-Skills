## Description: <br>
Guides agents through auditing, updating, validating, and syncing project documentation based on code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openghz](https://clawhub.ai/user/openghz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to identify documentation affected by code changes, update or create docs, validate the result, and record a documentation sync point for future incremental reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read repository contents and propose documentation edits or deletions. <br>
Mitigation: Use it in a trusted repository or isolated clone, review proposed changes, and require explicit approval before committing. <br>
Risk: Docs validation commands may execute local project scripts. <br>
Mitigation: Review validation commands before running them, especially in repositories with untrusted build scripts. <br>
Risk: An incorrect .docs-sync record can cause future incremental reviews to skip relevant code changes. <br>
Mitigation: Record the sync point only after documentation changes are reviewed and validation has completed. <br>


## Reference(s): <br>
- [Code to Documentation Mapping](references/CODE-TO-DOCS-MAPPING.md) <br>
- [Documentation Conventions Discovery Guide](references/DOC-CONVENTIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, proposed documentation edits, and configuration updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update documentation files and write a .docs-sync record after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
