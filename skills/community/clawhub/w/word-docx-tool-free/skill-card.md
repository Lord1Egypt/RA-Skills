## Description: <br>
Creates, reads, and edits Word documents, including formatting, template-based generation, table-of-contents creation, and single-task document workflows for personal use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent create, inspect, and update Word docx files for reports, contracts, and other everyday documents. The free edition is positioned for personal single-document tasks and basic template workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify local Word documents, which may expose sensitive document contents or overwrite important files. <br>
Mitigation: Provide explicit file paths, avoid unnecessary sensitive inputs, and review generated output before saving over original documents. <br>
Risk: Cleanup or delete actions could remove files unexpectedly. <br>
Mitigation: Confirm any cleanup, delete, or overwrite action before execution and keep backups for important documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/word-docx-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Word documents, JSON status responses, Markdown guidance, and inline Python or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require explicit local file paths and Python docx tooling when creating or editing documents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
