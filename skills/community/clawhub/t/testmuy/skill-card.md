## Description:

Captures learnings, errors, corrections, and feature requests in Markdown so OpenClaw agents can review and promote recurring lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nightsquirrl](https://clawhub.ai/user/nightsquirrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, feature requests, and recurring workflow lessons for later review. OpenClaw users can optionally enable a hook that reminds agents to review learnings and records redacted session-end error excerpts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved learning entries can influence future agent behavior when promoted into workspace memory files.

Mitigation: Keep .learnings out of version control where appropriate, review entries before promotion, and require explicit human approval before changes to SOUL.md, TOOLS.md, or AGENTS.md.

Risk: The optional OpenClaw hook can copy transcript excerpts into persistent error logs.

Mitigation: Enable the hook only in trusted workspaces, review auto-detected entries before retaining them, and avoid shared or untrusted workspaces unless transcript path handling is fixed.

Risk: Captured notes may contain sensitive operational context if users or agents log too much detail.

Mitigation: Follow the skill guidance to avoid secrets, tokens, private keys, environment variables, raw transcripts, and full source or configuration files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nightsquirrl/skills/testmuy)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Entry Examples](artifact/references/examples.md)
- [Uninstall Guide](artifact/references/uninstall.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown entries with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or append .learnings Markdown files; the optional OpenClaw hook can append truncated, redacted session-end error excerpts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
