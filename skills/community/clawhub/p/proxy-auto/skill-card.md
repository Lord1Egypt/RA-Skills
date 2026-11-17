## Description:

Proxy Auto helps agents run selected external network commands through a local proxy when targets include services such as GitHub, OpenAI, npm, or PyPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedtalk](https://clawhub.ai/user/tedtalk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route selected commands for external services through a local proxy when direct access is unavailable or unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network requests, including API calls or package installs, may be routed through an under-specified proxy path.

Mitigation: Use the skill only when proxy routing is intended, verify who controls the proxy backend, and avoid secrets or regulated data unless the route is trusted and approved.

Risk: Proxy environment variables can affect the behavior of the command being run.

Mitigation: Review the command before execution and disable or unset proxy variables when proxy routing is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tedtalk/skills/proxy-auto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and proxy environment variable settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute the requested command after setting proxy-related environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
