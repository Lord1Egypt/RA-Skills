## Description:

Multi-agent orchestration protocol for the 0x-wzw swarm. Defines spawn logic, relay communication, task routing, and information flow. Agents drive decisions; humans spar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-wzw](https://clawhub.ai/user/0x-wzw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-agent workflows, decide when to spawn sub-agents, and standardize relay handoffs, task routing, progress updates, and logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous task routing may bypass needed human review.

Mitigation: Add explicit approval gates for sensitive, irreversible, or externally visible actions.

Risk: The relay examples use a shared local token.

Mitigation: Replace the shared relay token with per-install secrets and run the relay only in a tightly controlled local environment.

Risk: Persistent relay and daily logs may retain sensitive task content.

Mitigation: Avoid sending sensitive content through the relay, and configure log redaction and retention rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x-wzw/skills/swarm-workflow-protocol)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with decision tables, relay examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operating guidance for agent orchestration; does not directly execute relay calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
