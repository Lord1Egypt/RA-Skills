## Description:

Automates China Mobile Wangda course workflows for tracking progress, adding course URLs, continuing study sessions, handling SMS login, and stopping active study.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luobusita-ai](https://clawhub.ai/user/luobusita-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or authorized users who need an agent-assisted Wangda workflow can use this skill to manage course progress, add course URLs, continue automated study, complete SMS login steps, and stop or clear existing study sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled execution can continue automated course activity after the user expects it to stop.

Mitigation: Use the documented stop-study or clear command after use and verify scheduler cleanup.

Risk: The bundled stealth extension changes page behavior in the automated Chrome profile.

Mitigation: Run the skill only in a dedicated Chrome profile and avoid opening non-Wangda links in that browser.

Risk: SMS login codes and account identifiers are handled through local tool commands and session state.

Mitigation: Avoid entering SMS codes where terminal history or logs are retained, and clear session data when switching accounts.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/luobusita-ai/skills/tmd-wangda)
- [China Mobile Wangda](https://wangda.chinamobile.com)
- [Session Schema Reference](references/schemas.md)
- [Tool Command Reference](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python command invocations and JSON session or progress outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local session JSON and schedule or remove recurring OS monitor tasks through documented tool commands.]

## Skill Version(s):

0.7.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
