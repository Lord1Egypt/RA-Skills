## Description:

Helps agents fetch recent content and updates from websites and platforms such as YouTube, GitHub, Instagram, Reddit, news sites, and blogs without using a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heqi201255](https://clawhub.ai/user/heqi201255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to discover available RSSHub routes, fetch feed content, and manage persistent feed subscriptions through the airsstool CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install mutable third-party tooling.

Mitigation: Prefer pinned releases and install in a dedicated, nonprivileged environment before use.

Risk: The skill can require running a local RSSHub Docker service.

Mitigation: Ask for explicit confirmation before deployment and review Docker configuration before starting services.

Risk: Some feeds may require API keys, cookies, or tokens in environment configuration.

Mitigation: Handle secrets securely, avoid casually placing credentials in .env files, and use scoped or disposable credentials where possible.

Risk: Persistent subscriptions can be changed or deleted through CLI commands.

Mitigation: Confirm destructive subscription actions and inspect existing paths before removing feeds or groups.

## Reference(s):

- [airsstool](https://github.com/heqi201255/airsstool)
- [RSSHub deployment documentation](https://docs.rsshub.app/deploy/)
- [ClawHub skill page](https://clawhub.ai/heqi201255/skills/site-feeds)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide airsstool requests that return Markdown, RSS, Atom, JSON, RSS3, or brief text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
