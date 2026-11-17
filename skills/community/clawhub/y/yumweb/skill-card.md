## Description:

yumweb lets local AI agents operate a persistent, already-authenticated Edge, Chrome, or Chromium browser session for browsing, tab control, page reading, screenshots, typing, JavaScript evaluation, and X workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use yumweb to let local agents operate a dedicated, persistent, already-authenticated Chromium browser session for browsing, reading pages, navigating tabs, screenshots, form interaction, JavaScript evaluation, and X timeline or posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive broad control over an authenticated browser profile, including access to logged-in sites.

Mitigation: Use a dedicated low-risk browser profile and accounts, avoid sensitive inboxes and commerce sessions unless needed, and treat the profile directory as credential material.

Risk: The skill can submit content or actions through logged-in websites, including public X posts, forms, purchases, or JavaScript evaluation.

Mitigation: Require manual approval before posts, purchases, form submissions, or eval commands, and only run trusted JavaScript.

Risk: The browser automation endpoint and dependencies can increase local attack surface if configured loosely.

Mitigation: Keep the remote debugging endpoint restricted to loopback, avoid wildcard origins before serious use, and pin dependencies for deployment.

## Reference(s):

- [yumweb ClawHub skill page](https://clawhub.ai/yumyumtum/skills/yumweb)
- [Playwright Python documentation](https://playwright.dev/python/)
- [yumweb repository link declared in README](https://github.com/yumyumtum/yumweb.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Files, Shell commands, Configuration]

**Output Format:** [Command-line stdout with text, markdown, HTML, or JSON responses; screenshots are written as PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser-read output defaults to 8000 characters and may be truncated; actions operate on the active tab of the persistent local browser profile.]

## Skill Version(s):

0.1.0 (source: release evidence and RELEASE_NOTES_v0.1.0.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
