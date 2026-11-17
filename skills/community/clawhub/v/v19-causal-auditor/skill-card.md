## Description:

V19 Causal Auditor automatically analyzes decision trails, detects causal conflicts, and generates audit recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run causal audits over agent decision records, identify contradictory or incomplete causal chains, and receive prioritized remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to submit decision-audit data and agent identity to an unverified temporary-looking external service.

Mitigation: Use redacted test data until the service operator, endpoint stability, retention terms, and deletion terms are verified.

Risk: Credential guidance is weak and includes a public experience key in the artifact.

Mitigation: Use per-user scoped credentials, rotate keys regularly, and avoid sharing production credentials in prompts, logs, or public documentation.

Risk: Audit results depend on the referenced remote service being trustworthy and available.

Mitigation: Review outputs before acting on them, and prefer an owner-controlled endpoint for production or commercial workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/skills/v19-causal-auditor)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Causal Dependency Analyzer](https://clawhub.com/skills/v19-causal-dependency-analyzer)
- [V19 Early Causal Graph Debugger](https://clawhub.com/skills/v19-early-causal-graph-debugger)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with curl command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns decision path annotations, highlighted causal anomalies, conflict scoring, and prioritized audit recommendations when the referenced service responds.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
