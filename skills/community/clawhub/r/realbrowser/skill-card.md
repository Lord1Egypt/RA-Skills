## Description:

Lets your AI agent drive a real Chrome session, either your own or one from an opted-in marketplace participant, for authorized QA flows, accessibility audits, synthetic monitoring, support-dashboard automation, and permitted data collection where headless or scripted requests are not enough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iwedmak](https://clawhub.ai/user/iwedmak)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA engineers, accessibility reviewers, monitoring operators, and support teams use this skill to drive real Chrome sessions on sites they own or are authorized to operate on. It is intended for workflows where JavaScript execution, full page layout, screenshots, browser interaction, or a real user environment is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches an unpinned third-party ceki-sdk package and may modify the Python environment.

Mitigation: Install only after reviewing the package source and prefer a pinned SDK version in an isolated environment.

Risk: Marketplace sessions are visible to the remote browser host and may expose sensitive task content.

Mitigation: Use Self mode for sensitive work and do not enter personal credentials, payment data, or private content into marketplace sessions.

Risk: Marketplace rentals can incur real per-minute charges until the session is stopped.

Mitigation: Stop each rental promptly with the documented stop command and monitor active sessions during use.

Risk: Browser automation can violate site rules or legal requirements when used without authorization.

Mitigation: Use the skill only on sites the user owns or is explicitly authorized to operate on, and honor Terms of Service, robots.txt, access controls, and consent preferences.

## Reference(s):

- [ClawHub RealBrowser listing](https://clawhub.ai/iwedmak/skills/realbrowser)
- [Ceki homepage](https://ceki.me)
- [ceki-sdk on PyPI](https://pypi.org/project/ceki-sdk/)
- [Ceki Chrome extension](https://browser.ceki.me/install)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, code snippets, and browser session output files such as screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill primarily guides agents to invoke the ceki CLI or SDK; browser state may be returned through screenshots, snapshots, chat messages, session identifiers, and local session files.]

## Skill Version(s):

0.1.1 (source: server evidence and manifest.json; changelog released 2026-06-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
