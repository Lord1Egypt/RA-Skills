## Description:

A Hermes Agent skill that lets an agent manage calendars, tasks, reminders, and alert delivery from plain-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[37rb](https://clawhub.ai/user/37rb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let a Hermes Agent create, query, edit, complete, and deliver alerts for personal schedule items, tasks, events, notes, goals, and jots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent local dispatcher that runs stored alert commands and modifies the reminder database.

Mitigation: Install only in environments where that local scheduled behavior is acceptable, review configured alert commands before use, and monitor dispatcher output for delivery problems.

Risk: Security evidence flags a real email-alert command-injection risk in the current email alert template.

Mitigation: Avoid or disable email alerts until the email route uses structured subprocess execution instead of the flagged shell template.

Risk: Security guidance recommends a pinned tklr-dgraham dependency before setup.

Mitigation: Pin and review the tklr-dgraham version used during installation before deploying the skill for routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/37rb/skills/tklr-reminders)
- [Source homepage](https://github.com/37Rb/hermes-skills/tree/main/skills/tklr-reminders)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [README](README.md)
- [How it works](references/how-it-works.md)
- [Setting up tklr-reminders](references/setup.md)
- [Using the wrapper](references/using-the-wrapper.md)
- [tklr syntax reference](references/tklr-syntax.md)
- [Alert configuration example](templates/alerts-config-example.toml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-language responses with agent-run shell commands and local configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Hermes Agent on Linux or macOS with hermes and tklr available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
