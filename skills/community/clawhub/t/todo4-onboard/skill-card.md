## Description:

Sign up for Todo4 and connect this agent via MCP using an email OTP flow, with no browser or password required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panitw](https://clawhub.ai/user/panitw)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create or connect a Todo4 account from chat, verify the user by email OTP, and configure the agent's MCP access to Todo4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's email address and OTP to Todo4 and connects the agent to the user's Todo4 account.

Mitigation: Install and run the skill only when the user trusts Todo4 and intends to grant persistent agent access to the account.

Risk: The skill stores an agent token under ~/.openclaw/.env.

Mitigation: Restrict token file permissions, avoid sharing the file, and rotate or revoke the token if the environment is exposed.

Risk: The skill writes server-provided MCP configuration under ~/.openclaw/mcp_config.json.

Mitigation: Review the MCP configuration snippet before use and confirm it only configures the expected Todo4 server.

## Reference(s):

- [Todo4 Onboard ClawHub Page](https://clawhub.ai/panitw/skills/todo4-onboard)
- [Todo4 Publisher Profile](https://clawhub.ai/user/panitw)
- [Todo4 Website](https://todo4.io)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown-style chat responses with shell command execution and JSON configuration side effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects an email address and OTP, calls Todo4 APIs, writes MCP configuration, stores an agent token, and may return a single-use web login URL.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
