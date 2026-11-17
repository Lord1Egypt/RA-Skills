## Description:

Wxpush helps agents configure and send WeChat template message push notifications through edgeone, wxpush, or go-wxpush API modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shisheng820](https://clawhub.ai/user/shisheng820)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Wxpush to configure WeChat push-message credentials and produce curl or Python commands for sending template messages through a selected API mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat AppSecret, API tokens, and recipient identifiers may be sent to third-party push endpoints.

Mitigation: Prefer a self-hosted or explicitly trusted HTTPS endpoint before sending credentials or message content.

Risk: Credentials placed in URL query strings can be exposed through shell history, logs, browser history, or intermediary systems.

Mitigation: Avoid putting tokens or AppSecrets in URLs; prefer POST bodies or authorization headers where the selected API mode supports them.

Risk: Previously used credentials may already have been exposed through unsafe URL-based examples or third-party service use.

Mitigation: Rotate any WeChat AppSecret, token, or related credential that was transmitted in a URL or sent to an untrusted endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shisheng820/skills/wxpush)
- [EdgeOne API documentation](references/edgeone.md)
- [Wxpush API documentation](references/wxpush.md)
- [Go-WXPush API documentation](references/go-wxpush.md)
- [WXPush-edgeone project](https://github.com/shisheng820/WXPush-edgeone)
- [frankiejun/wxpush project](https://github.com/frankiejun/wxpush)
- [hezhizheng/go-wxpush project](https://github.com/hezhizheng/go-wxpush)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate API requests that include WeChat push-message credentials; users should review endpoint trust and credential handling before use.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
