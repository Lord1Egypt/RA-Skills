## Description:

Integrates with TimeDoctor API to pull employee time tracking data, worklogs, statistics, and productivity metrics using simple Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jehadurre](https://clawhub.ai/user/jehadurre)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to let an agent retrieve and summarize TimeDoctor workforce data such as worklogs, user lists, project activity, timesheets, payroll settings, and screenshots for authorized company accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles TimeDoctor passwords and long-lived JWT tokens.

Mitigation: Use a manually provisioned token from a proper secret store, avoid pasting passwords or raw tokens into agent chat, and avoid storing six-month tokens in shell profile files.

Risk: The skill can expose sensitive employee, payroll, worklog, productivity, screenshot, and screencast data.

Mitigation: Install and run it only for authorized TimeDoctor companies, use least-privilege account permissions, and review outputs before sharing them.

## Reference(s):

- [TimeDoctor skill homepage](https://github.com/JehadurRE/timedoctor-openclaw-skill)
- [TimeDoctor API documentation](https://timedoctor.redoc.ly/)
- [ClawHub skill page](https://clawhub.ai/jehadurre/skills/timedoctor-skill)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON from Python CLI commands, typically summarized by the agent as Markdown tables, lists, or concise text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authorized TimeDoctor token and, for most commands, a company identifier.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
