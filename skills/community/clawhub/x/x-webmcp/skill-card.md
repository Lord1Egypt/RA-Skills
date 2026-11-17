## Description:

Connect to X and Grok through the built-in local-mcp X adapter and one fixed UXC link. Use when the user wants to read timelines, inspect tweets, post on X, or chat with Grok from an authenticated browser profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect a dedicated authenticated X browser profile to local-mcp for reading X timelines, inspecting tweets, posting or replying on X, publishing articles, and chatting with Grok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a persistent signed-in X profile, which may expose account access if the profile is shared or reused.

Mitigation: Use a dedicated isolated X profile and install only when agent access to that profile is intended.

Risk: Tweet, reply, upload, and article publishing actions can create public content from the authenticated account.

Mitigation: Require explicit user confirmation and dry-run review before any public write or publish action.

Risk: Implicit invocation can make the bridge available without a direct user request naming the skill.

Mitigation: Review invocation policy before install and keep write actions gated by confirmation.

Risk: Browser automation dependencies and session state can drift over time.

Mitigation: Prefer a pinned or lockfile-managed Playwright install and check authentication/session status before using tools.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Link Creation Helper](scripts/ensure-links.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command-output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a persistent authenticated X browser profile and may require dry-run review before public write actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
