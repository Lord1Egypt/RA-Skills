## Description:

Use this skill to manage Short.io branded short links via their REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godsboy](https://clawhub.ai/user/godsboy)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to create, list, inspect, delete, archive, and report on Short.io branded short links from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script handles URL input and a secrets file in ways that could run local commands under the user's account.

Mitigation: Review before installing, avoid untrusted URL inputs, and only use a SHORTIO_SECRETS_FILE path that you fully control.

Risk: The Short.io API key grants link-management authority for the connected account.

Mitigation: Use a Short.io API key whose permissions and account scope are acceptable for the agent workflow, and rotate it if exposure is suspected.

Risk: The current helper sources shell code from the configured secrets file.

Mitigation: Prefer parsing the API key as data instead of sourcing the file before broad deployment.

## Reference(s):

- [Short.io](https://short.io)
- [Short.io API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/godsboy/skills/short-io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHORT_IO_API_KEY and the curl, jq, python3, and column command-line tools.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
