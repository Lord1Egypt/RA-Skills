## Description:

Automatic token optimization during interaction with behavioral rules, plugin synergy, and workspace analysis for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyound87](https://clawhub.ai/user/beyound87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Token Pilot to audit and reduce agent token use through persistent agent rules, workspace cleanup guidance, cron and model routing recommendations, and configuration suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent changes to every agent's AGENTS.md can alter future agent behavior or duplicate existing rules.

Mitigation: Review the initialization preview, avoid --yes on first install, keep backups, and inspect overlap warnings before accepting changes.

Risk: Automatic cleanup modes can move or delete local workspace files without strong safeguards.

Mitigation: Run audit or recommendation modes first, manually inspect affected paths, and keep backups before using apply modes on important workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beyound87/skills/token-pilot)
- [README](artifact/README.md)
- [Token Pilot Core Rules](artifact/references/TOKEN-PILOT-CORE.md)
- [Cron Job Token Optimization](artifact/references/cron-optimization.md)
- [Workspace File Organization for Minimal Token Cost](artifact/references/workspace-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and JSON code blocks, plus text reports from bundled Node.js scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent guidance; scripts may write agent instruction files, generated catalog files, or workspace changes when users approve execution modes.]

## Skill Version(s):

3.8.0 (source: server release evidence; artifact frontmatter reports 3.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
