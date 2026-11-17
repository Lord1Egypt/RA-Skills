## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jambo-jet-love](https://clawhub.ai/user/jambo-jet-love)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to install and operate the gog CLI for Google Workspace workflows such as searching Gmail, sending mail, listing calendar events, searching Drive, managing contacts, and reading or updating Sheets and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged materials include broader Google account authority than the root skill description.

Mitigation: Review OAuth scopes before use, enable only required services, prefer read-only scopes where possible, and use the command allowlist for agent runs.

Risk: The nested Gmail gateway instructions would route Gmail traffic through Maton and require a Maton API key.

Mitigation: Avoid the nested Maton Gmail gateway unless that routing is explicitly intended, and protect MATON_API_KEY as a credential.

Risk: The bundled email-tracking functionality can create privacy and consent concerns.

Mitigation: Avoid email tracking unless there is a clear consent and privacy basis for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jambo-jet-love/skills/tmp)
- [gog CLI documentation](https://gogcli.sh)
- [Publisher profile](https://clawhub.ai/user/jambo-jet-love)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-oriented command guidance when recommending gog CLI scripting workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
