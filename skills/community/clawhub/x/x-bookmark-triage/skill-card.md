## Description:

Automatically triages X/Twitter bookmarks into structured Discord knowledge cards using Claude Haiku scoring, with scheduled polling, backlog sweeping, manual URL handling, and optional unbookmarking after capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremyknows](https://clawhub.ai/user/jeremyknows)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn saved X/Twitter bookmarks and manually dropped URLs into searchable Discord knowledge cards with relevance tiers, freshness labels, topics, tags, and proposed next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically remove X bookmarks after processing.

Mitigation: Use read-only X OAuth scopes or run backlog sweeps with --no-unbookmark until deletion is explicitly intended and guarded by confirmed Discord delivery.

Risk: OAuth, Discord, and Anthropic credentials are required for normal operation.

Mitigation: Store tokens in protected environment or secrets files, restrict file permissions, and rotate any credential exposed during setup or execution.

Risk: The .env-loading wrapper sources workspace configuration before running the poller.

Mitigation: Run the wrapper only from a trusted workspace and review local environment files before enabling scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeremyknows/skills/x-bookmark-triage)
- [OAuth setup guide](artifact/references/oauth-setup.md)
- [Cron setup guide](artifact/references/cron-setup.md)
- [Adapting guide](artifact/references/adapting.md)
- [X Developer Platform](https://developer.x.com)
- [Discord developer applications](https://discord.com/developers/applications)
- [Anthropic Console](https://console.anthropic.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown knowledge cards, setup guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts structured cards to Discord and writes local token and seen-URL state files during operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
