## Description:

Persistent thread memory for OpenClaw agents across Moltbook, Hacker News, Reddit, Discord, and Twitter/X; it tracks threads, surfaces new replies, and keeps a feed cursor so agents do not reread the same posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ubgb](https://clawhub.ai/user/ubgb)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use Undersheet to give OpenClaw agents persistent awareness of tracked threads and new feed posts across supported social and community platforms. It is useful for heartbeat workflows where an agent needs concise activity summaries and durable per-platform state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post through configured platform accounts, which can publish unintended or duplicate content if enabled carelessly.

Mitigation: Use read-only credentials where possible, grant least-privilege account permissions, and review any workflow that calls posting methods before deployment.

Risk: The Moltbook adapter includes a CAPTCHA-solving posting flow.

Mitigation: Avoid the Moltbook CAPTCHA-solving posting flow unless the platform owner has explicitly approved that use.

Risk: Credential, token, cookie, state, and proxy files are stored locally in user configuration paths.

Mitigation: Store those files in private directories, restrict file permissions, and rotate platform tokens if local state is exposed.

Risk: Artifact documentation includes mutable remote install commands that fetch files from a branch tip.

Mitigation: Install from the ClawHub release or pin and verify downloaded files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ubgb/skills/undersheet)
- [UnderSheet homepage](https://github.com/ubgb/undersheet)
- [Discord developer applications](https://discord.com/developers/applications)
- [Twitter/X developer portal](https://developer.twitter.com/en/portal/dashboard)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI summaries with JSON state and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and platform credentials for authenticated adapters; read-only use is available for some platforms.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata; artifact SKILL.md lists 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
