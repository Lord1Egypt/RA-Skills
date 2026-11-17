## Description:

Captures agent learnings, errors, corrections, and feature requests in structured Markdown logs so future sessions can reuse important lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangkang5](https://clawhub.ai/user/wangkang5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record corrections, command failures, API or tool failures, missing capability requests, and reusable practices. High-value lessons can be promoted into agent memory or instruction files after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent session-derived logs may capture secrets, private details, or sensitive user context.

Mitigation: Redact secrets and private details before logging, keep logs project-scoped, and do not share session history across agents without consent.

Risk: Promoting learnings into agent instruction files can cause incorrect or misleading guidance to affect future behavior.

Mitigation: Require human review before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions, and periodically prune stale entries.

Risk: Global or every-prompt hooks can inject reminders broadly and affect unrelated sessions.

Mitigation: Prefer project-scoped opt-in setup and avoid empty every-prompt matchers unless that behavior is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangkang5/skills/wangkang-skill1)
- [OpenClaw integration guide](artifact/references/openclaw-integration.md)
- [Hook setup guide](artifact/references/hooks-setup.md)
- [Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and template entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning logs under .learnings/ and optional hook reminders when configured.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
