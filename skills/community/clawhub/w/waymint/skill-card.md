## Description:

Link your OpenClaw agent to its wayMint ERC-8004 on-chain identity certificate and provide the configured identity URL when identity or verification is requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maksika](https://clawhub.ai/user/maksika)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to configure an OpenClaw agent's wayMint chain and ERC-8004 agent ID, then share the resulting certificate URL when identity or verification questions arise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad, unverified proof-of-human trust claims.

Mitigation: Present the wayMint certificate as an operator-configured third-party identity link and avoid treating it as automatic proof that an agent is trustworthy or human-operated.

Risk: The artifact text still references the older /8004 command while release notes say the slash command was fixed to /waymint.

Mitigation: Prefer /waymint in user-facing guidance and verify command naming before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maksika/skills/waymint)
- [wayMint identity service](https://8004.way.je)
- [wayMint registration](https://8004.way.je/register)
- [wayMint agent API](https://8004.way.je/api/agent/{chain}/{id})
- [wayMint owner API](https://8004.way.je/api/owner/{address})

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with identity URLs and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WAYMINT_CHAIN and WAYMINT_AGENT_ID configuration values to form wayMint identity, agent lookup, and owner lookup URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
