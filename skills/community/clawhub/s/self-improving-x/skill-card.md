## Description:

Captures an agent's learnings, errors, corrections, and feature requests in structured markdown logs so future agents can review and promote reusable guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seepine](https://clawhub.ai/user/seepine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture operational lessons, errors, corrections, and feature requests as durable markdown records. It supports later review and controlled promotion of broadly useful lessons into project or agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable learning logs may capture sensitive conversation details, private URLs, tokens, personal data, or raw command output.

Mitigation: Keep .learnings local by default and redact secrets, private URLs, tokens, personal data, and raw command output before saving entries.

Risk: Promoting log entries into future-agent instruction files may change future agent behavior without enough user control.

Mitigation: Review every proposed promotion into AGENTS.md, CLAUDE.md, TOOLS.md, SOUL.md, or .github/copilot-instructions.md before accepting it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seepine/skills/self-improving-x)
- [Artifact README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown log entries and concise instruction updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .learnings markdown files and propose promotions into agent instruction files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
