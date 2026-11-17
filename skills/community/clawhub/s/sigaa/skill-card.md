## Description:

SIGAA helps agents authenticate to SIGAA academic-management portals and retrieve student or professor information through institution-specific web scraping workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegantonov](https://clawhub.ai/user/olegantonov)

### License/Terms of Use:

MIT

## Use Case:

Students, professors, and authorized support agents use this skill to check SIGAA enrollment status, grades, academic history, schedules, class lists, attendance, and professor portal information for supported Brazilian institutions.

### Deployment Geography for Use:

Brazil, for supported SIGAA institutions

## Known Risks and Mitigations:

Risk: Credential submissions may reach an unintended SIGAA or CAS host if destination validation is weak.

Mitigation: Set SIGAA_URL only to the exact HTTPS URL for the intended institution and review or fix the login flow so credentials are submitted only to approved SIGAA/CAS hosts.

Risk: Institutional passwords may be exposed through curl process arguments during login.

Mitigation: Avoid real, reused, or high-privilege accounts until the login script is reviewed or changed to avoid password exposure in process arguments.

Risk: The skill accesses sensitive academic records and session cookies.

Mitigation: Use only authorized SIGAA accounts, keep generated cookie files private, and review outputs before sharing or storing them.

## Reference(s):

- [Project homepage](https://github.com/olegantonov/sigaa-openclaw-skill)
- [SIGAA ClawHub listing](https://clawhub.ai/olegantonov/skills/sigaa)
- [Institutions and Login URLs](references/institutions.md)
- [Student Portal Guide](references/student-guide.md)
- [Professor Portal Guide](references/professor-guide.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIGAA_URL, SIGAA_USER, and SIGAA_PASSWORD environment variables plus curl, python3, and grep.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter states 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
