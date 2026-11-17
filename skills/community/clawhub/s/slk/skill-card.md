## Description:

Read, send, search, and manage Slack messages and DMs through the slk CLI for macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therohitdas](https://clawhub.ai/user/therohitdas)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to let an agent check Slack, read channels or DMs, search messages, manage drafts and saved items, and send or react to messages from the local user's Slack session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local Slack session credentials and caches token material, so an agent can act as the Slack user and credential material needs careful handling.

Mitigation: Install only when this behavior is intended, prefer one-time Keychain approval, avoid shared or managed machines, and treat ~/.local/slk/token-cache.json as sensitive.

Risk: The CLI can send messages, reactions, and drafts through the user's Slack session.

Mitigation: Review agent-generated write actions before execution and use draft commands when human review is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/therohitdas/skills/slk)
- [npm package: slkcli](https://www.npmjs.com/package/slkcli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown guidance with inline shell commands; invoked CLI commands return terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only Slack workflow that acts with the local user's Slack session.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
