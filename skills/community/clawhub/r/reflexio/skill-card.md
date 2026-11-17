## Description:

Captures user facts and procedural corrections into .reflexio/ so the agent can retrieve relevant memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyiilluu](https://clawhub.ai/user/yyiilluu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Reflexio to preserve useful preferences, facts, procedural corrections, and workflow playbooks across OpenClaw sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-term memory from conversations in plaintext .reflexio files.

Mitigation: Use it only in workspaces where durable conversation memory is intended, and avoid sessions containing secrets or sensitive data.

Risk: The skill modifies persistent workspace instructions through HEARTBEAT.md and active-memory configuration.

Mitigation: Review the heartbeat block and active-memory scope before enabling the plugin.

Risk: Session-end extraction and consolidation can write, merge, or delete memory entries automatically.

Mitigation: Review generated .reflexio profiles and playbooks periodically and remove incorrect or unwanted entries.

## Reference(s):

- [Reflexio on ClawHub](https://clawhub.ai/yyiilluu/skills/reflexio)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory files plus text and JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and searches .reflexio/ profile and playbook files; includes TTL, deduplication, and consolidation behavior.]

## Skill Version(s):

1.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
