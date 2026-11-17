## Description:

Monitor your SoundCloud account, track artist releases, and get notified about new followers and likes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlinds](https://clawhub.ai/user/wlinds)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to connect an agent to SoundCloud, track selected artists, and receive account engagement or new-release notifications through chat or scheduled checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SoundCloud client credentials and access tokens can be exposed if ~/.openclaw/secrets/soundcloud.env or related terminal output is shared.

Mitigation: Use revocable SoundCloud credentials, protect ~/.openclaw/secrets/soundcloud.env, and avoid sharing terminal output from that file.

Risk: The security evidence flags a concrete credential-leak concern around OAuth tokens being sent before SoundCloud API URLs are validated.

Mitigation: Review before installing and prefer a release that validates SoundCloud API URLs before sending OAuth tokens.

Risk: SoundCloud display names, usernames, and track titles may contain prompt-like or Markdown content.

Mitigation: Keep output sanitization in place and review notifications before acting on user-controlled SoundCloud metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlinds/skills/soundcloud-watcher)
- [Project homepage](https://github.com/wlinds/OpenClaw-SoundCloud-Watcher)
- [npm package](https://www.npmjs.com/package/@akilles/soundcloud-watcher)
- [OpenClaw plugin documentation](https://docs.openclaw.ai/plugin)
- [SoundCloud app registration](https://soundcloud.com/you/apps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown command responses with inline shell commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SoundCloud account status, follower activity, track engagement, and new-release notifications; SoundCloud links can be disabled in configuration.]

## Skill Version(s):

2.4.0 (source: server release evidence, package.json, plugin manifest, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
