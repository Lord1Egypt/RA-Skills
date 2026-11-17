## Description:

Manage gym routines and fitness tracking in wger via API for viewing, editing, creating workouts, logs, nutrition plans, and progress analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjaspreet](https://clawhub.ai/user/0xjaspreet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to automate wger fitness workflows, including workout logging, routine review, nutrition tracking, goal updates, and progress reporting through API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change sensitive fitness data in a connected wger account.

Mitigation: Use a limited token, store it in the environment, and require explicit user approval before create or update actions.

Risk: Self-hosted wger deployments can expose personal data if deployed with weak defaults or broad network access.

Mitigation: Use unique secrets, restrict access to loopback or VPN, enable HTTPS, and pin container versions.

## Reference(s):

- [wger API Endpoints Reference](references/api_endpoints.md)
- [Self-Host wger (Docker)](references/selfhost.md)
- [wger API documentation](https://wger.readthedocs.io/en/latest/api.html)
- [ClawHub skill page](https://clawhub.ai/0xjaspreet/skills/wger-openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Code, Configuration]

**Output Format:** [Markdown with inline shell commands, API request examples, and Python script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or execute API requests that read or update wger fitness data when authorized by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
