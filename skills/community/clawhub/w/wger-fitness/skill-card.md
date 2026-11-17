## Description:

Manage gym routines and fitness tracking in wger via API for viewing, editing, creating workouts, logs, nutrition plans, and progress analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjaspreet](https://clawhub.ai/user/0xjaspreet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage wger fitness data through API calls, including workout routines, workout logs, nutrition entries, goals, and progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an API token that can read and modify sensitive fitness data.

Mitigation: Use a token scoped to the intended wger instance, keep it in the environment, and avoid pasting it into prompts or shared logs.

Risk: POST and PATCH examples can change workout, nutrition, and goal records.

Mitigation: Require explicit approval before running write actions or automation that performs write actions.

Risk: The self-hosting example includes local-testing defaults that are unsuitable for durable deployments.

Mitigation: Change the database password, pin container image versions, and secure access before using the Docker setup beyond local testing.

## Reference(s):

- [wger API Endpoints Reference](references/api_endpoints.md)
- [Self-Host wger (Docker)](references/selfhost.md)
- [wger API Documentation](https://wger.readthedocs.io/en/latest/api.html)
- [ClawHub skill page](https://clawhub.ai/0xjaspreet/skills/wger-fitness)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, shell commands, Python script usage, and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or modify wger fitness data when the user supplies an API token and approves API write actions.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
