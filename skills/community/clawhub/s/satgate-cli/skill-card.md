## Description:

Satgate helps operators manage API access from the terminal by minting tokens, checking gateway status, validating tokens, and wrapping agent commands through SatGate enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wmattadeen-gif](https://clawhub.ai/user/wmattadeen-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Satgate to configure SatGate CLI, check gateway status, mint and validate access tokens, and run agent commands through a budget-enforced proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI depends on downloaded GitHub release binaries and may skip checksum verification when checksums are unavailable.

Mitigation: Use a pinned and audited release, verify checksums when available, install to a user-owned directory when possible, or build from source from a trusted checkout.

Risk: API keys and SatGate tokens may be exposed through shell environments, local config files, or shared MCP configuration.

Mitigation: Use short-lived least-privilege tokens, keep local config permissions restrictive, revoke unused credentials, and do not place real tokens in shared or committed files.

Risk: Wrapping untrusted commands can route their outbound traffic through a proxy that injects the SatGate bearer token.

Mitigation: Wrap only trusted commands, verify the tenant and gateway with satgate-cli status first, and validate tokens before relying on them.

## Reference(s):

- [SatGate homepage](https://satgate.io)
- [SatGate MCP connection page](https://cloud.satgate.io/cloud/mcp/connect)
- [ClawHub Satgate skill listing](https://clawhub.ai/wmattadeen-gif/skills/satgate-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CLI setup, token, validation, proxy wrapping, and MCP bridge guidance.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
