## Description:

Automates the ZhanFu WebDriver client and store browsers with local HTTP calls before connecting Playwright over CDP for user-directed browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzhang1997](https://clawhub.ai/user/zhangzhang1997)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and store operators use this skill to open, close, create, list, and configure ZhanFu stores, then perform guided Playwright automation in the store browser after a WebDriver port is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-value ZhanFu account credentials and store-management actions.

Mitigation: Use it only on trusted local machines, avoid entering owner or store passwords on shared or monitored systems, and provide credentials only when needed for the requested workflow.

Risk: Local automation can contact the wrong local service or an untrusted ZhanFu workflow if the environment is not verified.

Mitigation: Verify the real ZhanFu client is listening before login or store operations and stop when local communication cannot be confirmed.

Risk: Cache clearing, account changes, plugin changes, and client termination can alter store state or interrupt active work.

Mitigation: Require explicit user confirmation before running cache clearing, account update, plugin update, or client exit actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangzhang1997/skills/zhanfu-playwright)
- [ZhanFu WebDriver API reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON HTTP request examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may operate a local ZhanFu client, store accounts, browser sessions, plugins, download paths, and cache settings.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
