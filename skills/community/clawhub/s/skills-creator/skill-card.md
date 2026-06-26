## Description: <br>
Guides users through creating, reviewing, improving, and publishing OpenClaw skills using structured workflows, best practices, and quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jau123](https://clawhub.ai/user/jau123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and skill maintainers use this skill to create new OpenClaw skills, review existing SKILL.md files, retrofit older skills, and add documented API-integration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills could obscure external transfers, credential use, command execution, or publishing behavior if scanner-avoidance wording is applied too broadly. <br>
Mitigation: Review generated skill text before publishing and require it to describe external transfers, credentials, commands, and publishing behavior accurately. <br>
Risk: Generated API-wrapper or shell-script examples could be treated as ready to run without user review. <br>
Mitigation: Present generated scripts and commands for user review and confirmation before execution, and declare required binaries and environment variables in metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jau123/skills-creator) <br>
- [Best Practices for OpenClaw Skills](references/best-practices.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Skill Template](assets/skill-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter examples, Markdown tables, and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce skill files, review tables, suggested shell commands, and configuration snippets for user review.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
