## Description:

Enables an Openclaw agent to spawn child Openclaw agents for separable, parallel, or context-limited work while passing scoped task context and collecting results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparky0520](https://clawhub.ai/user/sparky0520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate clearly separable tasks to child Openclaw agents, including sequential handoffs, parallel gather workflows, and planned fire-and-forget work. It is intended for controlled agent workflows where provider credentials, shared context, and child tool access can be scoped by the parent agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child agents receive task snapshots through the selected model provider.

Mitigation: Sanitize progress_so_far before spawning and remove secrets, credentials, personal data, and unrelated context.

Risk: Tools passed to a child agent may grant file, network, or other operational capabilities.

Mitigation: Pass only the minimum trusted tools required for the child task, and omit tools when the child only needs to return text.

Risk: Provider behavior and dependencies vary by configured model.

Mitigation: Configure the correct provider environment variables, avoid embedding API keys in payloads, and pin LiteLLM in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sparky0520/skills/recursive-spawn)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce child-agent completion summaries or file paths when the helper script is used with appropriate tools.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
