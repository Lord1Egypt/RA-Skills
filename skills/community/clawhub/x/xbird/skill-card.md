## Description:

Use when the user asks to tweet, post threads, read tweets, search Twitter/X, check mentions, manage engagement, update profile assets, upload media, or interact with Twitter accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[checkra1neth](https://clawhub.ai/user/checkra1neth)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an agent to Twitter/X workflows, including reading timelines and tweets, searching, posting, engagement actions, profile updates, media uploads, and x402-metered calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP process uses live Twitter/X session cookies and can perform account actions such as posting, following, profile updates, and media uploads.

Mitigation: Use a dedicated account where practical, avoid shared plaintext secret storage, revoke exposed sessions promptly, and require manual confirmation before write or profile-changing actions.

Risk: Paid x402 calls can require wallet signing through an optional private key.

Mitigation: Use a dedicated low-value wallet, review charges before paid calls, and avoid storing the private key in shared configs.

Risk: Installation runs mutable third-party npm package code through npx.

Mitigation: Pin and review the npm package before use and install only after accepting the third-party code execution risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/checkra1neth/skills/xbird)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate read, write, profile, media, and paid x402 Twitter/X MCP operations.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
