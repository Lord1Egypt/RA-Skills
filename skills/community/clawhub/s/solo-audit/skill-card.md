## Description: <br>
Audit helps agents review markdown-heavy knowledge bases for broken links, missing or inconsistent frontmatter, tag inconsistencies, orphaned files, content quality issues, and coverage gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical writers, and knowledge-base maintainers use this skill to audit markdown projects and produce a KB Audit Report with prioritized issues and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run an unreviewed project link-checking script during link checking. <br>
Mitigation: Run it from the intended knowledge-base directory and require explicit review and approval before executing any discovered link-checking script. <br>
Risk: The skill reads markdown files in the current project to audit frontmatter, links, tags, orphaned files, and coverage gaps. <br>
Mitigation: Install and invoke it only in projects where the agent is allowed to inspect the markdown knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/solo-audit) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fortunto2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit report with tables, lists, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect markdown files and propose or run link-checking commands when approved.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
