## Description:

V19 Causal Dependency Analyzer analyzes event sequences to produce causal dependency graphs, risk-weighted paths, and responsibility-chain attribution to the process constraint associated with a failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to submit failure-event sequences and protocol constraints for causal-path analysis, risk weighting, and responsibility attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may transmit sensitive incident details, internal module names, protocol thresholds, credentials, or proprietary data to an external endpoint.

Mitigation: Use sanitized test data unless the operator is trusted and privacy, retention, deletion, and credential-scope terms are clear.

Risk: The documented public key is not a reliable control for sensitive use.

Mitigation: Treat the public key as non-secret and avoid relying on it to protect confidential submissions.

## Reference(s):

- [V19 Causal Dependency Analyzer on ClawHub](https://clawhub.ai/liuyanfeng1234/skills/v19-causal-dependency-analyzer)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
- [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented workflow sends event and protocol data to a remote Cloudflare Tunnel endpoint and returns causal paths, risk weights, responsibility-chain entries, and suggested constraint changes.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
