## Description:

Integrate Reclaim Protocol verification of data from online accounts, author verification providers, and investigate verification sessions with the Reclaim Builder MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madhavanmalolan](https://clawhub.ai/user/madhavanmalolan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Reclaim Protocol verification into an app, research or author supported providers, and investigate verification sessions, events, and callback delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A pending or failed verification could be mistaken for a verified claim and lead to an incorrect access decision.

Mitigation: Check the observed session status and verify the callback or proof on the server before granting access or benefits.

Risk: Account credentials or personal account data could be exposed during verification setup.

Mitigation: Have account holders complete their own sign-in and consent; never request passwords or private keys in chat or display stored credentials.

## Reference(s):

- [Reclaim Builder](https://build.reclaimprotocol.org)
- [OpenClaw MCP setup documentation](https://docs.openclaw.ai/tools/mcp)
- [Reclaim developer-tools repository](https://github.com/reclaimprotocol/developer-tools)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
