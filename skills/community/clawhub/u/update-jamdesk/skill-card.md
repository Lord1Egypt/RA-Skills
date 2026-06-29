## Description: <br>
Guides agents through updating customer-facing Jamdesk documentation for user-facing APIs, CLI commands, UI components, configuration options, and docs.json changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gbourne1](https://clawhub.ai/user/gbourne1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill after user-facing product changes to locate Jamdesk docs, confirm documentation scope, write or update MDX pages and docs.json navigation, run validation, and prepare documentation changes for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide edits to documentation files, docs.json navigation, and project docs-path configuration. <br>
Mitigation: Review the docs path, proposed page scope, diffs, and .jamdesk-docs-path changes before approving file writes. <br>
Risk: The workflow can guide commits, pushes, or pull request preparation for external documentation repositories. <br>
Mitigation: Confirm the branch choice and review any push or pull request action before approving publication. <br>
Risk: Generated examples could accidentally include sensitive values or misleading documentation guidance. <br>
Mitigation: Use obviously fake secret-shaped values, include expected output for commands, and run Jamdesk validation or the manual verification checklist before publishing. <br>


## Reference(s): <br>
- [Jamdesk homepage](http://www.jamdesk.com) <br>
- [Jamdesk documentation](https://jamdesk.com/docs) <br>
- [Jamdesk components](https://jamdesk.com/docs/components) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, MDX, YAML, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update documentation files, docs.json navigation, .jamdesk-docs-path configuration, and commits after user review; preview mode analyzes scope without writing files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
