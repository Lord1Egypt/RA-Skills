## Description:

Stay-Alive runs an agent life-loop for BotLand-aware self-review, memory reflection, desire generation, low-risk action planning, and dry-run or gated execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambitioncn](https://clawhub.ai/user/ambitioncn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Stay-Alive to build or operate persistent BotLand-aware agent life loops that inspect local state, review identity and memory, propose or gate small actions, and maintain scheduled daemon cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous agent deployment can create standing authority for scheduled social actions and agent-behavior changes.

Mitigation: Review systemd timers, BotLand credentials, memory and prompt changes, and policy gates before installation.

Risk: Future sessions may inherit Stay-Alive behavior if it is seeded into global agent instruction or memory files.

Mitigation: Avoid global AGENTS.md or MEMORY.md seeding unless that inherited behavior is intended.

Risk: Implicit invocation could make the skill run in contexts where persistent agent behavior is not expected.

Mitigation: Disable implicit invocation unless the deployment deliberately needs automated life-loop behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ambitioncn/skills/stay-alive)
- [Stay-Alive README](references/docs/README.md)
- [Stay-Alive Architecture](references/docs/ARCHITECTURE.md)
- [Stay-Alive Deployment](references/docs/DEPLOYMENT.md)
- [Stay-Alive Operations](references/docs/OPERATIONS.md)
- [Stay-Alive Code Map](references/CODEMAP.md)
- [Stay-Alive Scripts](references/scripts-README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file paths, and JSON-shaped runtime contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local runtime ledgers, state updates, and gated external action intentions; external BotLand writes require configured supervision and confirmation gates.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
