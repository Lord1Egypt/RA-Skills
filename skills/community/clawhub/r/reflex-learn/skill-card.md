## Description:

Detects repeated queries as implicit negative feedback and non-repetition as positive feedback, enabling continuous learning by writing reflections and patterns to MEMORY.md and SOUL.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaventures](https://clawhub.ai/user/kaventures)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Reflexlearn to let an agent record implicit feedback from repeated or unrepeated user queries and turn that feedback into local memory, pending guidance, and response-pattern updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-derived prompt content can be logged locally and used to influence future agent behavior.

Mitigation: Install only when that persistence is acceptable, keep MODE set to cautious, and regularly inspect and prune MEMORY.md, SOUL.md, reflex_history.json, and reflexlearn-pending.md.

Risk: The security summary reports that persistent behavior files may be updated without the review gate the skill claims to use.

Mitigation: Disable or avoid heartbeat reinforcement until SOUL.md writes are staged for review, and manually review pending updates before applying them.

Risk: The install path depends on package and model downloads before offline use.

Mitigation: Use an isolated environment, prefer pinned dependencies, and review the install script's listed PyPI and Hugging Face operations before confirming installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaventures/skills/reflex-learn)
- [Publisher profile](https://clawhub.ai/user/kaventures)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown entries, JSON history, and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local OpenClaw memory, pending-review, history, and pattern files under ~/.openclaw/.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
