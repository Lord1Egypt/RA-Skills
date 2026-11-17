## Description:

Fetches a Weibo login QR code through OpenClaw browser integration and handles browser startup, page navigation, QR extraction, cookie checks, and retry flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmls](https://clawhub.ai/user/fmls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to automate Weibo QR-code login, restore an existing Weibo browser session from saved cookies, and save cookies after a successful scan for later reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup changes global OpenClaw settings, enables broad tool access, clears deny rules, runs the browser without sandboxing, and restarts the gateway.

Mitigation: Review the setup script and local OpenClaw policy before installation; run it only in an environment where those configuration changes are acceptable.

Risk: The skill stores reusable Weibo login cookies on disk.

Mitigation: Use only on trusted machines, protect the OpenClaw data directory, and remove saved cookies when persistent Weibo access is no longer needed.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [Weibo Login Page](https://passport.weibo.com/sso/signin)
- [Weibo Website](https://weibo.com/)
- [Playwright Mirror Used by Setup](https://npmmirror.com/mirrors/playwright)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status output, and a local PNG QR-code file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or reuses Weibo login cookies stored on disk and may require a gateway restart after setup.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
