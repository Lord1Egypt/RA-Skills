## Description:

A high-fidelity token management and model stabilization skill that implements the Zown "Atomic Pipeline" to reduce Gemini token-per-minute rate limit issues during heavy engineering, multi-step code generation, or 429 recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtovd](https://clawhub.ai/user/gtovd)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide agents through token-conscious task execution, context pruning, cooldown decisions, and Gemini-focused Q&A workflows when rate limits or large prompts are a concern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to edit persistent memory or identity files.

Mitigation: Require explicit user approval before any memory, identity, or long-lived context file is created, summarized, compacted, or overwritten.

Risk: The skill can route prompts through an external Gemini CLI.

Mitigation: Confirm what content will be sent externally before invoking the CLI, and avoid sending secrets, private code, or regulated data.

Risk: The skill refers to running an unbundled cooldown script.

Mitigation: Do not run referenced scripts unless they are present, reviewed, and approved in the local workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtovd/skills/zown-gemini-governor)
- [Publisher profile](https://clawhub.ai/user/gtovd)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask an agent to summarize memory files, pause execution, or use an external Gemini CLI; supervise those actions before execution.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
