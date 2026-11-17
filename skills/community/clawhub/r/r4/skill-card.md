## Description:

Access and manage credentials, secrets, and domain registrations using the R4 platform with environment-variable injection and API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukezirngibl](https://clawhub.ai/user/lukezirngibl)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve scoped secrets from R4, run commands with injected environment variables, and manage domain search, purchase, and DNS operations through R4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or inject sensitive credentials into agent-run commands.

Mitigation: Use a tightly scoped R4 vault, avoid printing or logging secret values, and do not run untrusted commands through `r4 run`.

Risk: The skill can affect billing or ownership by purchasing domains and changing DNS records.

Mitigation: Require explicit approval before domain purchases, DNS changes, or actions that use billing authority.

Risk: The skill can supply credentials to third-party services.

Mitigation: Require explicit approval before sending credentials to third-party services and limit available vault items to the task scope.

## Reference(s):

- [R4 API Documentation](https://r4.dev/docs/api-reference)
- [ClawHub R4 Skill](https://clawhub.ai/lukezirngibl/skills/r4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes secret-handling and domain-management guidance; users should avoid exposing raw secret values in logs or command output.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
