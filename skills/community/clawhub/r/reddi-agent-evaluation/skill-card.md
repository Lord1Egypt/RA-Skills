## Description:

Testing and benchmarking LLM agents, including behavioral testing, capability assessment, reliability metrics, and production monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design agent evaluations, benchmark agent behavior, and reason about reliability risks before production use. It focuses on behavioral regression tests, capability assessments, statistical evaluation, adversarial testing, and data leakage prevention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad agent-testing requests and provide general evaluation guidance where project-specific review is needed.

Mitigation: Review generated evaluation plans against the target agent, production environment, and reliability goals before adopting them.

Risk: LLM API scoring depends on the user's configured environment rather than executable code bundled with this skill.

Mitigation: Confirm any external scorer configuration, credentials, and model behavior before relying on score outputs.

Risk: Agent evaluations can miss production failures if based on single runs, narrow happy paths, or leaked test data.

Mitigation: Use repeated trials, adversarial and edge-case tests, behavioral contracts, and data leakage checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/reddi-agent-evaluation)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and evaluation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend evaluation patterns, test plans, rubrics, reliability metrics, and review checks for agent behavior.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata, released 2026-03-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
