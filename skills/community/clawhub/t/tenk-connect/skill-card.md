## Description:

Connect your TenK account to your AI assistant. Log practice sessions, check progress, and manage your 10,000-hour journey from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscarcode9](https://clawhub.ai/user/oscarcode9)

### License/Terms of Use:

MIT

## Use Case:

External users connect an AI assistant to their TenK account to authenticate, log practice sessions, view tracked skills, check progress, and review recent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found confirmed input-handling flaws in the logging script that could allow crafted values to run local commands.

Mitigation: Review before installing; fix logging to pass user and API values as data, strictly validate minutes, and confirm state-changing log actions before use.

Risk: The skill accesses a TenK account and makes authenticated TenK API calls.

Mitigation: Authenticate only with the intended account, review requested actions before execution, and clear the local token with logout when access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oscarcode9/skills/tenk-connect)
- [TenK app](https://tenk.oventlabs.com)
- [Project homepage](https://github.com/OscarCode9/tenK)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TenK account plus curl and python3; stores an OAuth token in the user's local config directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
