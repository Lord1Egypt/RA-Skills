## Description:

Solve complex problems by interleaving reasoning with actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncatbot](https://clawhub.ai/user/simoncatbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to structure exploratory, tool-heavy work as repeated reasoning, action, and observation cycles. It is intended for research, debugging, data analysis, API work, and other multi-step tasks where the next step depends on observed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could treat illustrative examples as permission to run migrations, deployments, sensitive queries, or external communications.

Mitigation: Require explicit approval, environment scoping, and change review before executing high-impact actions proposed during a ReAct session.

Risk: Example payment code could be copied into production with incomplete server-side amount validation and error handling.

Mitigation: Treat payment examples as instructional only and redesign production payment flows with server-side validation, idempotency, webhook verification, and security review.

Risk: Iterative tool use can drift beyond the original task or expose sensitive operational data.

Mitigation: Define allowed tools, data scopes, stop criteria, and observation-recording rules before applying the loop to sensitive systems.

## Reference(s):

- [ReAct Loop skill page](https://clawhub.ai/simoncatbot/skills/react-loop)
- [Detailed examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with structured thought, action, observation, and final-answer sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed tool calls, commands, code snippets, investigation notes, and recommendations for review before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
