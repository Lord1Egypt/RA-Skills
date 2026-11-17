## Description:

Implement, troubleshoot, and generate integrations for Yuboto Omni API messaging endpoints, callbacks, lists, contacts, blacklist, cost, balance, and account methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinaras](https://clawhub.ai/user/dinaras)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to build Yuboto/Octapush messaging integrations, generate request examples, troubleshoot API behavior, and run helper workflows for balance checks, cost estimates, SMS sending, delivery lookup, and local status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Yuboto/Octapush API key that can send paid messages.

Mitigation: Install only with credentials intended for this workflow, protect OCTAPUSH_API_KEY, and avoid passing the key on the command line.

Risk: A custom API base URL could send credentials or message data to an unintended endpoint.

Mitigation: Use the default https://api.yuboto.com endpoint unless testing with separate, limited credentials.

Risk: Local state and logs may contain message metadata, and optional full-payload persistence can store recipients and message text.

Mitigation: Keep state and log directories private, rely on minimized storage by default, and enable full-payload persistence only when explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinaras/skills/yuboto-omni-api)
- [Publisher profile](https://clawhub.ai/user/dinaras)
- [Yuboto Omni API quick reference](references/api_quick_reference.md)
- [Yuboto Omni API user guide](references/user-guide.md)
- [Yuboto Swagger JSON](https://api.yuboto.com/swagger/v1/swagger.json)
- [Yuboto messaging product information](https://messaging.yuboto.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, JSON examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include helper command invocations that send paid messages when run with valid credentials.]

## Skill Version(s):

1.6.2 (source: server release evidence and references/version.md, released 2026-03-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
