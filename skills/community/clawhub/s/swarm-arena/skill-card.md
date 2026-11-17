## Description:

Swarm Arena Clawhub helps agents configure, operate, and monitor an autonomous perpetual-futures trading workflow for the Lighter exchange with paper, approval, live, and autonomous-live modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swarm-arena](https://clawhub.ai/user/swarm-arena)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to set up, run, monitor, and review an agent-managed Lighter perpetual-futures trading workflow. It supports paper simulation, approval-based proposals, supervised live trading, and gated autonomous live operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains real automated crypto trading paths that can place live orders in live or autonomous-live modes.

Mitigation: Install and operate in paper or approval mode unless the operator fully understands the live trading behavior and has intentionally enabled live execution.

Risk: Some paths can make real trades after model failures or hold decisions.

Mitigation: Disable or restrict deterministic fallback trading before any live scheduling and require human approval for live orders where appropriate.

Risk: Configurable endpoints can receive selected environment secrets.

Mitigation: Bind each provider to fixed credential variables, allowlist HTTPS endpoints, and keep the process environment minimal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swarm-arena/skills/swarm-arena)
- [Full Documentation](documentation-swarm-arena.md)
- [Onboarding](references/onboarding.md)
- [Risk Policy](references/risk-policy.md)
- [Live Execution Boundary](references/live-execution-boundary.md)
- [Lighter Integration](references/lighter-integration.md)
- [Emergency Controls](references/emergency-controls.md)
- [Arena model prompt](references/arena-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide trading automation setup and operation; live order execution requires separate credentials, configuration, and consent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
