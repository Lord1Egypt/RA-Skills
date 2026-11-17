## Description:

Orchestrate a TaskFlow-managed ingestion job that validates, packages, and publishes an OpenClaw skill folder to the ClawHub registry, then verifies the published artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to run an auditable, resumable ClawHub publish flow for agent skill folders, with validation before the live registry write and verification after publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish step can perform an irreversible external registry write without a clear human approval gate.

Mitigation: Run dry-run validation first and require explicit manual approval immediately before the live publish command.

Risk: Reference patterns construct child-agent commands from publish arguments.

Mitigation: Use trusted, reviewed skill folders; sanitize slug, name, version, and changelog values; and prefer structured argument passing over command strings.

Risk: The verification script uses a node -e metadata read pattern involving the published slug.

Mitigation: Avoid the node -e slug interpolation pattern and use a safer structured metadata reader for verification.

## Reference(s):

- [Published ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/taskflow-clawhub-publish)
- [TaskFlow orchestration reference](artifact/references/flow.ts)
- [Publish command reference](artifact/references/publish.sh)
- [Verification command reference](artifact/references/inspect.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and TypeScript reference snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces TaskFlow state guidance, ClawHub publish and verification commands, and install or inspect checks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
