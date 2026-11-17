## Description:

Help choose, compare options, prioritize, or decide an agent's next step using Jev; show which judgments Jev contributed, accept corrections, and reuse scoped preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutd](https://clawhub.ai/user/cutd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs structured help comparing options, prioritizing tradeoffs, or deciding a workflow branch with Jev-assisted judgments and a correction loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local setup and preference data and sends relevant decision context to the Jev/TypeSafe API when invoked.

Mitigation: Install only if that data sharing is acceptable; use XJEV_HOME or --no-setup for tighter local control and periodically review or revoke saved policies.

Risk: Decision guidance can be wrong if candidate facts, constraints, or evidence are incomplete or stale.

Mitigation: Verify hard constraints before calling Jev, treat unknown decisive facts as gaps to resolve, and re-evaluate stale decisions before relying on them.

Risk: A recommendation could be mistaken for permission to take an external action.

Mitigation: Keep the decision receipt separate from execution; the runtime does not authorize payment, publishing, messaging, or other real-world actions.

## Reference(s):

- [Runtime contract](references/runtime.md)
- [Feedback and scoped request learning](references/learning.md)
- [Synthetic comparison example](references/examples/compare.json)
- [TypeSafe API documentation](https://docs.typesafe.ai/api)
- [TypeSafe confidence documentation](https://docs.typesafe.ai/confidence)
- [OpenAI Codex skills documentation](https://developers.openai.com/codex/skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown decision cards with inline shell commands and JSON command receipts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Jev contribution attribution, decision IDs, policy IDs, rankings, and next-step guidance; no command authorizes external execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
