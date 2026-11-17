## Description:

Guides an agent to open Weibo's official browser login page for QR-code authentication, validate the signed-in session, and preserve cookies for later authorized Weibo use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs a user-approved Weibo browser session before later authorized content retrieval or posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A logged-in Weibo browser session may persist through saved cookies after the immediate login task is complete.

Mitigation: Use only accounts and actions the user explicitly authorizes, then log out or clear browser cookies when the session should no longer remain available.

Risk: Frequent or automated Weibo activity can encounter anti-scraping controls.

Mitigation: Avoid frequent operations and keep activity within Weibo-authorized, user-approved workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bombfuock/skills/weibo-login)
- [Weibo Login Page](https://weibo.com/login)

## Skill Output:

**Output Type(s):** [Guidance, Browser actions, Configuration instructions]

**Output Format:** [Markdown with inline browser action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user QR-code approval and may rely on persisted browser cookies.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
