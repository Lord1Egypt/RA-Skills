## Description: <br>
Access Finland's Wilma school system from AI agents. Fetch schedules, homework, exams, grades, attendance/lesson notes (merkinnät), messages, and news via the wilma CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikarjal](https://clawhub.ai/user/aikarjal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, guardians, and authorized school-account users use this skill through an agent to retrieve Wilma schedules, homework, exams, grades, attendance notes, messages, and news as concise briefings or targeted lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive student data from Wilma and relies on stored login material in a local Wilma configuration file. <br>
Mitigation: Install only when the user trusts @wilm-ai/wilma-cli, protect the Wilma configuration file, and avoid sharing or logging TOTP secrets. <br>
Risk: Broad queries such as --all-students can retrieve more student data than intended. <br>
Mitigation: Prefer explicit --student and date filters, and use --all-students only when broad access is intended. <br>


## Reference(s): <br>
- [ClawHub Wilma listing](https://clawhub.ai/aikarjal/wilma) <br>
- [Wilma CLI GitHub link](https://github.com/aikarjal/wilmai) <br>
- [Wilma CLI website](https://wilm.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-oriented CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers non-interactive CLI commands with --json output.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
