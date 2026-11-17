## Description:

Automated integration-test skill for verifying creation, inspection, version updating, and deletion through the ClawHub REST API lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release automation maintainers use this skill to test the ClawHub skill lifecycle API against a named test slug, including publish, inspect, update, and cleanup operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle API testing can create, update, inspect, and delete ClawHub skill records.

Mitigation: Run it only with credentials and API environments limited to test resources and the named test slug.

Risk: A failed cleanup can leave the ephemeral test skill visible on ClawHub.

Mitigation: Inspect the named slug after test runs and delete leftover test releases before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/tosr-test-skill-1778050437)
- [Publisher Profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with REST API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
