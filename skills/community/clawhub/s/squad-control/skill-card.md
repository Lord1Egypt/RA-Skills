## Description:

Integrate with Squad Control kanban for AI agent task orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgan](https://clawhub.ai/user/wgan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to connect OpenClaw agents to Squad Control tasks, dispatch worker and reviewer sessions, create GitHub PRs, and report status back to the kanban workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated agents receive Squad Control API keys and may receive GitHub tokens for private repository cloning, pushing, PR creation, and merge workflows.

Mitigation: Install only for trusted Squad Control instances and workspaces; prefer workspace-scoped keys, fine-grained repository tokens, protected branches, and human approval before merges.

Risk: Account-scoped API keys can expose tasks and workspace configuration across multiple workspaces to dispatched agents.

Mitigation: Use workspace-scoped keys when possible and limit account-scoped keys to environments where all connected workspaces and task sources are trusted.

Risk: Secrets may appear in agent prompts, shell environments, logs, or session transcripts during task dispatch.

Mitigation: Redact API keys and GitHub tokens from logs and sessions, and avoid embedding credentials directly in cron messages, clone URLs, or persistent files.

## Reference(s):

- [Squad Control Skill Page](https://clawhub.ai/wgan/skills/squad-control)
- [Squad Control Homepage](https://squadcontrol.ai)
- [Setup Guide](references/setup.md)
- [API Reference](references/api.md)
- [Advanced Flows Reference](references/advanced-flows.md)
- [Workspace Config Reference](references/workspace-config.md)
- [Poll Result Schema](references/poll-result.schema.json)
- [Review Checklist](references/review-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, shell commands, and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce GitHub pull requests, Squad Control task status updates, review verdicts, and structured POLL_RESULT JSON during agent workflows.]

## Skill Version(s):

1.4.0 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
