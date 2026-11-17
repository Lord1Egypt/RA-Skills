## Description:

Post-completion self-review for coding agents that runs bounded simplify, harden, and micro-documentation passes on non-trivial code changes before signaling done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pskoett](https://clawhub.ai/user/pskoett)

### License/Terms of Use:


## Use Case:

Developers and coding-agent users use this skill after non-trivial code changes to run a bounded self-review that simplifies recent edits, checks for security and resilience gaps, and records small notes for non-obvious implementation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to automatically make cleanup and simple security edits to files changed in the current task.

Mitigation: Use it only where bounded agent edits are acceptable, keep the documented scope and budget limits enabled, and require normal review before merging.

Risk: The learning loop can persist generated rules into future agent instructions without clear approval controls.

Mitigation: Disable the learning loop or require explicit approval before it writes or promotes persistent agent instructions, especially in shared or production repositories.

Risk: Refactor stop hooks depend on the agent reliably pausing for human approval.

Mitigation: Test the target agent's approval behavior before production use and use the CI/headless variant when interactive approval cannot be trusted.

## Reference(s):

- [Agent Context Snippets](references/agent-context-snippets.md)
- [ClawHub Skill Page](https://clawhub.ai/pskoett/skills/simplify-and-harden)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and structured YAML summary examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May apply bounded edits to files changed in the current task and may append a structured review summary.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
