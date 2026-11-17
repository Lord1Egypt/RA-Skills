## Description:

Automated integration test skill to verify creation, update, retrieval, and deletion workflows via the ClawHub REST API.

This skill is for research and development only.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to exercise ClawHub skill lifecycle workflows for a named ephemeral test skill, including publishing, inspecting, updating, and deleting it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes deletion against the real ClawHub service.

Mitigation: Use it only for the named ephemeral test skill and confirm the slug before any delete operation.

Risk: The artifact is intended for lifecycle testing and may indicate failed cleanup if still visible.

Mitigation: Treat installation or reuse as test-only unless a reviewer explicitly scopes it for another controlled test.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-skill-1787627998)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls]

**Output Format:** [Markdown guidance with REST API endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code; guidance is scoped to an ephemeral lifecycle test skill.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
