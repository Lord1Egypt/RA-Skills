## Description:

Skill Factory decomposes complex tasks into 3-6 independent, executable sub-skill structures and returns status-specific JSON without scheduling or executing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and orchestrator agents use this skill to turn a complex structured task into 3-6 independent sub-skill definitions with names, descriptions, input examples, and output examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated sub-skill structures can be incomplete or misleading if the required structured inputs are missing or low quality.

Mitigation: Review generated sub-skill definitions before use and rely on the skill's need_retry and error outputs when required context is absent.

Risk: The artifact documentation and examples are in Chinese, which may reduce reviewer comprehension for non-Chinese users.

Mitigation: Request localized output or human translation before approving the skill for teams that do not read Chinese.

## Reference(s):

- [Decomposition Patterns](references/decomposition-patterns.md)
- [Independence Check](references/independence-check.md)
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/smallkeyboy-skill-factory)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON with success, need_retry, and error variants]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful outputs include a stage, status, 3-6 proposed skills, reasoning, and next_action; retry and error outputs explain missing inputs or structural problems.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
