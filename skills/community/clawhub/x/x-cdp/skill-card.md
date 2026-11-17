## Description:

Automate X (Twitter) through Chromium CDP to post tweets, reply, quote-retweet, and publish articles using an existing logged-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stwith](https://clawhub.ai/user/stwith)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare and execute X/Twitter posting workflows, including tweets, replies, quote retweets, and X Premium articles. It is intended for controlled use with a logged-in browser profile and explicit confirmation before public posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in X browser profile and can publish public content.

Mitigation: Use a dedicated Chromium profile and account, keep the CDP port local, run dry-run first, and require explicit confirmation before posting.

Risk: Setup can install and prioritize unpinned dependencies from /tmp.

Mitigation: Install pinned dependencies in a project-controlled directory before use and avoid the default /tmp dependency flow.

Risk: Account checks can fail open before article publishing.

Mitigation: Treat the --account check as unreliable for article publishing until account detection fails closed, and confirm the target account manually before publishing.

## Reference(s):

- [X CDP Automation on ClawHub](https://clawhub.ai/stwith/skills/x-cdp)
- [X DOM Selectors Reference](references/selectors.md)
- [Chromium downloads](https://www.chromium.org/getting-involved/download-chromium/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live runs can publish content through a logged-in X browser session; dry runs compose content and save screenshots under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
