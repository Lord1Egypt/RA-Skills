## Description: <br>
SIGAA helps agents authenticate to SIGAA academic portals and retrieve student or professor information such as enrollment status, grades, academic history, schedules, classes, students, and pending attendance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegantonov](https://clawhub.ai/user/olegantonov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, professors, and authorized academic support users use this skill to let an agent access SIGAA through an institutional account and summarize portal information. It is useful for checking enrollment requests, grades, academic history, class schedules, professor classes, student lists, and pending attendance entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SIGAA institutional credentials and creates authenticated sessions for academic portal access. <br>
Mitigation: Install only when the agent is intended to access a SIGAA account, keep SIGAA_USER and SIGAA_PASSWORD out of shared or logged environments, and unset credentials after use. <br>
Risk: A misconfigured SIGAA_URL or unexpected CAS redirect could send credentials or session traffic to the wrong host. <br>
Mitigation: Verify SIGAA_URL and any CAS redirect host before login. <br>
Risk: Academic workflows may affect sensitive enrollment, attendance, or grade-related information. <br>
Mitigation: Require explicit confirmation before any enrollment, attendance, or grade-changing workflow. <br>


## Reference(s): <br>
- [ClawHub SIGAA listing](https://clawhub.ai/olegantonov/sigaa) <br>
- [Publisher profile](https://clawhub.ai/user/olegantonov) <br>
- [Project homepage](https://github.com/olegantonov/sigaa-openclaw-skill) <br>
- [Institutions and login URLs](references/institutions.md) <br>
- [Student portal guide](references/student-guide.md) <br>
- [Professor portal guide](references/professor-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and tabular academic portal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIGAA_URL, SIGAA_USER, and SIGAA_PASSWORD environment variables plus curl, python3, and grep.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
