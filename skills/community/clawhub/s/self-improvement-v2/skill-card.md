## Description:

Captures learnings, errors, corrections, and feature requests in markdown so agents can review and promote durable improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janeaaaa](https://clawhub.ai/user/janeaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to have coding agents record failures, corrections, feature requests, and reusable lessons in `.learnings/`, then promote broadly useful guidance into project memory files after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can retain secrets, personal data, or sensitive project details.

Mitigation: Keep `.learnings/` local by default and redact secrets, personal data, and sensitive context before writing entries.

Risk: Promoted learnings can change future agent behavior through project memory files.

Mitigation: Require human review before promoting entries into `CLAUDE.md`, `AGENTS.md`, `SOUL.md`, `TOOLS.md`, or Copilot instruction files.

Risk: Broad hook matchers can inject reminders more often than intended.

Mitigation: Avoid global hooks with empty matchers unless the workspace owner explicitly accepts the behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/janeaaaa/skills/self-improvement-v2)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell snippets, configuration examples, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent learning records and project memory guidance when the user enables those workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
