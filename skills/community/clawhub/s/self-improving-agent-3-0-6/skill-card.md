## Description:

Captures learnings, errors, feature requests, and corrections in markdown logs so agents can review and promote durable project knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raidan-ai](https://clawhub.ai/user/raidan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record command failures, user corrections, missing capabilities, integration failures, knowledge gaps, and reusable best practices for later review or promotion into project memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived notes can be promoted into future agent instructions or memory files without enough safeguards.

Mitigation: Keep learning files local by default, avoid recording secrets or private transcript content, and require explicit human approval before promotion into agent instruction or memory files.

Risk: Optional hook setup can automatically inject reminders or run detector scripts during agent workflows.

Mitigation: Do not enable hooks unless the exact scripts are bundled or pinned and independently reviewed.

## Reference(s):

- [Agent Skills specification](https://agentskills.io/specification)
- [ClawHub skill page](https://clawhub.ai/raidan-ai/skills/self-improving-agent-3-0-6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces logging templates and promotion guidance for local project memory files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
