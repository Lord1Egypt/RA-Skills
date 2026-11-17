## Description:

Session Manager helps OpenClaw users list, monitor, and clean inactive sessions, with optional scheduled cleanup and Nginx proxy/user setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx0018](https://clawhub.ai/user/zx0018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to keep OpenClaw session directories manageable through configurable retention, whitelists, dry-run cleanup, and status reporting. It can also help operators configure per-user proxy access when they have reviewed the Nginx and token-handling risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled cleanup can delete older OpenClaw session files.

Mitigation: Confirm max-age, minimum-session, and whitelist settings before enabling cron; use the dry-run mode before the first cleanup.

Risk: The proxy and user-creation scripts modify Nginx configuration with sudo privileges.

Mitigation: Review generated usernames, ports, and Nginx site files on a non-shared host before reloading Nginx.

Risk: OpenClaw tokens may be placed into redirect URLs or Nginx configuration by the proxy setup.

Mitigation: Use environment variables for token input, avoid shared or production hosts until token handling is fixed, and rotate any token previously used with the proxy setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zx0018/skills/session-manager-zx)
- [Publisher profile](https://clawhub.ai/user/zx0018)
- [OpenClaw project homepage](https://github.com/openclaw/openclaw)
- [OpenClaw Cron documentation](https://docs.openclaw.ai/cron)
- [OpenClaw Sessions documentation](https://docs.openclaw.ai/sessions)
- [OpenClaw session management best practices](https://docs.openclaw.ai/best-practices/sessions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, cron entries, cleanup logs, and optional Nginx site configuration when the user runs the bundled scripts.]

## Skill Version(s):

1.0.4 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
