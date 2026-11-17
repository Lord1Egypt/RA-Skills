## Description:

Guide an existing OpenClaw operator through the SprintX handoff proof packet with the minimum safe steps: verify prerequisites, connect with sx auth, select the project, send the first event and artifact, then confirm read-back with sx status and sx brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terry3838](https://clawhub.ai/user/terry3838)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to connect an existing OpenClaw runtime to an existing SprintX account and project through a narrow, verifiable handoff flow. It helps them authenticate, select project context, send a first event and artifact, and confirm read-back with SprintX CLI status commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The flow may install an unpinned external SprintX CLI package.

Mitigation: Review or pin @sprint-x/cli before global installation in controlled environments, and run sx --help before using the handoff flow.

Risk: The proof packet sends handoff metadata and artifact references to SprintX.

Mitigation: Review the SprintX project ID before sending commands and avoid using secrets or sensitive files as artifact references.

Risk: Token-based authentication can expose credentials if handled through chat.

Mitigation: Use browser-approved sx auth by default and do not paste access tokens into chat.

## Reference(s):

- [Source Of Truth](references/source-of-truth.md)
- [SprintX OpenClaw Handoff Quickstart](https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart)
- [SprintX CLI Quickstart](https://www.sprintx.co.kr/docs/getting-started/cli-quickstart)
- [SprintX CLI Quickstart Korean](https://www.sprintx.co.kr/docs/getting-started/cli-quickstart.ko)
- [SprintX CLI Auth Boundary](https://github.com/terry3838/SprintX/blob/main/docs/engineering/SX_AUTH_V1.md)
- [SprintX Product Boundary And Runtime Contract](https://github.com/terry3838/SprintX/blob/main/docs/engineering/TECH_SPEC.md)
- [ClawHub Skill Page](https://clawhub.ai/terry3838/skills/sprintx-openclaw-handoff)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist-style operator guidance with pass/fail signals and recovery steps.]

## Skill Version(s):

0.1.3 (source: frontmatter, package.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
