## Description:

Create and manage SimpleLogin email aliases from the command line. Protect your real email with secure, private aliases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcclawd](https://clawhub.ai/user/mcclawd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, list, enable, disable, and delete SimpleLogin aliases, and to create contacts or reverse aliases for private email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent SimpleLogin API-key access that can create contacts and enable, disable, or delete aliases.

Mitigation: Limit use to trusted agents and sessions, review proposed account-changing actions, and prefer disabling aliases before deletion.

Risk: The included reverse-alias test script is flagged as unsafe for untrusted alias or contact values.

Mitigation: Run the test script only with trusted alias and contact inputs until its jq and JSON handling are hardened.

Risk: A leaked SimpleLogin API key could allow account-changing actions.

Mitigation: Store the API key in a password manager or session-scoped environment variable and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcclawd/skills/simplelogin-cli)
- [SimpleLogin](https://simplelogin.io)
- [SimpleLogin open source project](https://github.com/simple-login)
- [SimpleLogin aliases API endpoint](https://app.simplelogin.io/api/aliases?page_id=0)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, a SimpleLogin account, and SIMPLELOGIN_API_KEY or ~/.openclaw/secrets/simplelogin.json.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
