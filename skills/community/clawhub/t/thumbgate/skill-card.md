## Description:

Stop your AI from making the same mistake twice with Pre-Action Gates that block repeat hallucinations, retry loops, and known-bad tool calls before they reach the model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use ThumbGate to capture repeated agent mistakes as prevention rules, block known-bad tool calls before execution, and keep an audit trail of prevented actions across supported AI coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm initializer can install persistent pre-tool hooks across agent configurations without enough scoping or rollback detail.

Mitigation: Review the npm package and hook changes before installation, use a pinned and audited version, run with least privilege, and confirm disable or uninstall steps.

Risk: Hook-based blocking can interrupt legitimate agent tool calls if prevention rules are too broad or stale.

Mitigation: Review captured rules before enabling them broadly and keep a documented process for updating or disabling rules that block intended work.

## Reference(s):

- [ThumbGate ClawHub listing](https://clawhub.ai/igorganapolsky/skills/thumbgate)
- [ThumbGate homepage](https://thumbgate-production.up.railway.app)
- [ThumbGate dashboard](https://thumbgate-production.up.railway.app/dashboard)
- [npm package: thumbgate](https://www.npmjs.com/package/thumbgate)
- [Skill-disclosed repository](https://github.com/IgorGanapolsky/ThumbGate)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the thumbgate CLI binary; outputs guidance for installing, configuring, and using pre-action gates.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
