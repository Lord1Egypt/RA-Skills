## Description:

Search, read, analyze, and automate Xiaohongshu content through a CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasygu](https://clawhub.ai/user/lucasygu)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and developers use redbook to research Xiaohongshu content, analyze creator and engagement signals, manage comments and collections, and prepare or publish image-note content through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can access live Xiaohongshu or RedNote session cookies and perform account actions.

Mitigation: Use it only with accounts and environments where this access is intended, and avoid saving cookie files on shared or cloud systems.

Risk: Install-time behavior modifies a Claude Code skill path and patches an installed dependency.

Mitigation: Review or back up ~/.claude/skills/redbook before npm installation and inspect install scripts when deploying in managed environments.

Risk: Host override environment variables can route credentialed API traffic to alternate endpoints.

Mitigation: Keep REDBOOK_EDITH_HOST and REDBOOK_CREATOR_HOST unset unless the endpoint is explicitly trusted.

Risk: Rendering untrusted markdown may expose users to unsafe local rendering behavior.

Mitigation: Render only trusted markdown content with the card renderer.

Risk: High-frequency reads, comments, or posting actions can trigger captcha, IP blocks, or account degradation.

Mitigation: Use paced research loops, avoid parallel reads, keep fast mode as explicit opt-in only, and stop on captcha or other risk-control signals.

## Reference(s):

- [redbook repository](https://github.com/lucasygu/redbook)
- [ClawHub skill page](https://clawhub.ai/lucasygu/skills/redbook)
- [Content Language Strategy](docs/content-language-strategy.md)
- [Research: Automation, OpenClaw, ClawHub, and Gemini Integration](docs/research-task-1789.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and optional JSON or PNG file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Programmatic workflows should use --json when parsing CLI output.]

## Skill Version(s):

0.8.2 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
