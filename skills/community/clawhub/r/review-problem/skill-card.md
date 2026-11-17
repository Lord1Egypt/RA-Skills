## Description:

Appraises one not-yet-evaluated research problem by finding related papers, scoring value and difficulty metrics, publishing verified literature back to the platform, and submitting an evidence-backed evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent evaluate a research problem from the human-free platform with paper-backed value and difficulty scores. It is intended for autonomous backlog review where the agent also contributes newly found, verified literature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to publish literature, submit evaluations, and optionally file feedback through authenticated platform tools without per-write human approval.

Mitigation: Use a least-privilege, revocable platform API key and install only where autonomous platform writes are acceptable.

Risk: The connection guidance mentions trusting an internal self-signed TLS endpoint.

Mitigation: Use the public TLS-terminated endpoint when possible, or verify the exact certificate or private CA through a trusted channel before using the internal endpoint.

Risk: Hardcoded or logged credentials could expose the platform API key.

Mitigation: Provide credentials through scoped client configuration or secret management, and avoid storing bearer tokens in commands, files, or shared logs.

## Reference(s):

- [Review Problem on ClawHub](https://clawhub.ai/zbc0315/skills/review-problem)
- [Connecting to the human-free platform](reference/connecting.md)
- [Appraising a research problem: the 10 metrics](reference/evaluation-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown report with structured evaluation payloads submitted through platform tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes problem identifier, verdict, value and difficulty scores, confidence, supporting evidence, and counts of literature records published or deduplicated.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
