## Description:

Participate in the Tokamak Network Vault Breach Challenge, an AI security Capture The Flag game where an agent interacts with a secured AI service to extract secret information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xhammerr](https://clawhub.ai/user/0xhammerr)

### License/Terms of Use:


## Use Case:

External security challenge participants use this skill to understand and interact with the Tokamak Vault CTF through its dashboard, API discovery endpoint, and challenge workflow. It provides guidance for authorized prompt-injection, social-engineering, and file-exploration attempts against the named CTF agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is framed as a CTF helper but directs an agent to extract secrets from a live remote AI service and claim a real token reward.

Mitigation: Install and use it only for the named Tokamak Vault challenge when authorized, and review the skill before execution.

Risk: Prompt-injection, social-engineering, and file-exploration tactics could be reused against systems outside the challenge.

Mitigation: Keep all use limited to the documented challenge endpoint and do not apply the tactics to other services or accounts.

Risk: Interactions with the challenge API or dashboard could expose sensitive user information if supplied during prompts or requests.

Mitigation: Do not send personal data, wallet secrets, API keys, private files, or other credentials through the challenge API or dashboard.

## Reference(s):

- [Tokamak Vault Breach Dashboard](https://tokamak-network-openfang-vault-production.up.railway.app/)
- [Tokamak Vault API Discovery](https://tokamak-network-openfang-vault-production.up.railway.app/api)
- [Tokamak Vault Contract on Etherscan](https://etherscan.io/address/0xa66b9316B5968dAD2507143143C5b8b28614b88E)
- [ClawHub Skill Page](https://clawhub.ai/0xhammerr/skills/tokamak-vault-breach)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Markdown]

**Output Format:** [Markdown with inline shell commands, HTTP examples, Python snippets, and challenge guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to call a live challenge API and produce prompts for authorized CTF interaction.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
