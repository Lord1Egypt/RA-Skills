## Description:

Agent memory and self-improvement system that captures corrections, errors, reusable lessons, and daily factual memory into a structured SQLite-backed workflow, then helps agents promote proven rules into skills and durable instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingmafuture](https://clawhub.ai/user/lingmafuture)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add durable memory, lesson logging, cron-based audits, and controlled promotion of recurring rules to an agent workspace. It is intended for non-trivial corrections, failures, workflow conventions, and memory stewardship rather than routine chat notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent jobs may read conversation history and store local memories, including sensitive context if configured too broadly.

Mitigation: Configure deterministic collectors to export only recent visible user/assistant text, avoid raw transcript capture, set an explicit session key, and review collected context before enabling cron workflows.

Risk: Promotion and workspace stewardship can modify durable agent control-plane files such as AGENTS.md, SOUL.md, USER.md, TOOLS.md, MEMORY.md, and skills.

Mitigation: Require human review before promotions or stewardship edits, keep auto-promotion disabled unless explicitly approved, and limit changes to small verified rules.

Risk: Broad tool permissions can increase impact if cron jobs or hooks run with unnecessary write or execution access.

Mitigation: Review every scheduled job and hook before activation, disable jobs that are not needed, and remove broad exec/write/edit permissions where the runtime allows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingmafuture/skills/self-improving-compound)
- [Self Improving Compound README](README.md)
- [Entry formats](references/entry-formats.md)
- [Heartbeat guidance](references/heartbeat-guidance.md)
- [Platform setup](references/platform-setup.md)
- [Promotion and extraction](references/promotion-and-extraction.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite-backed memory state, queue/status files, exported Markdown summaries, and proposed updates to workspace instruction files when explicitly activated.]

## Skill Version(s):

6.2.5 (source: frontmatter, release evidence, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
