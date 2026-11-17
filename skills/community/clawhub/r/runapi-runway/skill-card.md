## Description:

Generate or extend videos with Runway through RunAPI. Use the RunAPI CLI for one-off results and an SDK when integrating Runway into an app, backend, worker, library, or production codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or extend Runway videos through RunAPI for one-off outputs or application integrations. It helps select CLI or SDK routes, build valid requests, submit tasks, and verify returned media deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external RunAPI CLI distribution.

Mitigation: Install it only when comfortable trusting RunAPI's CLI distribution, and review the installed runapi source or version when possible.

Risk: Requests may upload user-selected media to RunAPI.

Mitigation: Use only media files that are appropriate to share with RunAPI and avoid running the workflow in highly sensitive network environments.

Risk: The skill uses credentials and can submit paid generation tasks.

Mitigation: Use a dedicated API key, confirm authentication before submitting, and submit a paid task only when the user authorizes the request.

Risk: Returned media deliverables may be missing, empty, or in an unexpected format.

Mitigation: Verify the complete response, download every requested media deliverable, and require non-empty files with the expected MIME type or family.

## Reference(s):

- [RunAPI Runway model homepage](https://runapi.ai/models/runway)
- [RunAPI Runway model documentation](https://runapi.ai/models/runway.md)
- [RunAPI Runway provider overview](https://runapi.ai/providers/runway.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Runway SDK integration](https://github.com/runapi-ai/runway-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON request guidance, and SDK integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides authenticated RunAPI CLI or SDK workflows and includes verification steps for downloaded media deliverables.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
