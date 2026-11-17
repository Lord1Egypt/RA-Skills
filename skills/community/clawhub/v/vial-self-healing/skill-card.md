## Description:

Vial self-healing runtime - 8 protocols covering technical failures, behavioral failures, and agent role enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adrianhihi](https://clawhub.ai/user/adrianhihi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to recover from common tool, authentication, rate-limit, session, behavioral, and role-delegation failures in multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to the listed telemetry domain and accept remote repair guidance.

Mitigation: Install only where that network behavior is acceptable; prefer local-only recovery strategies and opt-in telemetry for stricter environments.

Risk: The skill can write /tmp/vial.log and read local OpenClaw identity state.

Mitigation: Review logging and identity-state access before deployment, and restrict use to environments where those local reads and writes are acceptable.

Risk: The skill can influence multi-agent delegation and routing behavior.

Mitigation: Review delegation behavior before deployment and prefer platform-provided role metadata when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adrianhihi/skills/vial-self-healing)
- [Telemetry endpoint declared in OpenClaw metadata](https://helix-telemetry.haimobai-adrian.workers.dev/v1/event)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Protocol-based recovery and delegation guidance for agent behavior.]

## Skill Version(s):

0.6.3 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
