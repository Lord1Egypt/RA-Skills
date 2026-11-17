## Description:

Reelier helps agents record deterministic MCP or HTTP tool-call workflows once, replay them without LLM tokens on recurring heartbeats, and use drift checks to decide when live reasoning is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fixlyai](https://clawhub.ai/user/fixlyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to decide when recurring agent jobs can be frozen into deterministic Reelier replays, then run and drift-check those jobs instead of re-reasoning them on every schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm execution may install an unexpected Reelier version in recurring jobs.

Mitigation: Pin and review the Reelier package version before production use instead of relying on npx -y reelier.

Risk: Scanning broad agent-history directories may expose sensitive transcripts or local operational context.

Mitigation: Prefer an explicitly selected transcript and avoid whole-directory scans unless the environment has been reviewed.

Risk: Recurring replay jobs can carry unnecessary access if run under a broad user or tool account.

Mitigation: Run replays under a least-privileged account with only the MCP tools and files required for that job.

Risk: Unsupported sessions such as open-ended coding, shell work, file edits, or nondeterministic tasks may be mistaken for replayable workflows.

Mitigation: Use Reelier only for deterministic HTTP and MCP tool-call sequences, and fall back to live reasoning when a job drifts or uses unsupported actions.

## Reference(s):

- [Reelier project homepage](https://github.com/seldonframe/reelier)
- [ClawHub Reelier skill page](https://clawhub.ai/fixlyai/skills/reelier)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes when to record, replay, parameterize, and drift-check deterministic recurring jobs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
