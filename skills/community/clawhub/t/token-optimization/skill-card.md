## Description:

Reduce OpenClaw per-turn prompt costs by 70%+ through file splitting, prompt caching, context pruning, and model routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw token usage, split always-loaded workspace files, configure prompt caching, tune context pruning, and route low-value work to cheaper models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace file pruning or configuration edits may remove useful context or change OpenClaw behavior.

Mitigation: Review and back up AGENTS.md, MEMORY.md, BOOTSTRAP.md, and openclaw.json before applying the guide.

Risk: Installing an unpinned latest branch may include unreviewed changes.

Mitigation: Prefer a reviewed ClawHub release or a specific commit, then confirm caching and pruning settings fit the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jack-yang-ai/skills/token-optimization)
- [OpenClaw Prompt Caching docs](https://docs.openclaw.ai/reference/prompt-caching)
- [Session Pruning docs](https://docs.openclaw.ai/concepts/session-pruning)
- [Gateway Configuration](https://docs.openclaw.ai/gateway/configuration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guide with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewed optimization steps; it has no hidden code or automatic behavior.]

## Skill Version(s):

1.1.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
