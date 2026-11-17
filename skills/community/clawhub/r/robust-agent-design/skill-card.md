## Description:

Apply robust Agent design patterns for building fault-tolerant, state-driven automation systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhbb2000](https://clawhub.ai/user/bhbb2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or refactor agent systems that need explicit state management, retries, compensation transactions, graceful degradation, and coordinated recovery from failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference Python templates include file-based state persistence that can overwrite arbitrary writable paths if adopted directly.

Mitigation: Make disk persistence opt-in, restrict state paths to an application-owned directory, use safe file creation permissions, and validate loaded state before use.

Risk: The sample checksum is not a security integrity control.

Mitigation: Use appropriate cryptographic integrity checks when persisted state or messages cross trust boundaries.

## Reference(s):

- [Agent template](references/agent_template.py)
- [Compensation example](references/compensation_example.py)
- [ClawHub skill page](https://clawhub.ai/bhbb2000/skills/robust-agent-design)
- [ClawHub publisher profile](https://clawhub.ai/user/bhbb2000)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with Python examples, architecture patterns, and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include state schemas, retry policies, compensation flows, graceful degradation strategies, and reference Python templates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
