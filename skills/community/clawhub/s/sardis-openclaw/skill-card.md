## Description:

Enable AI agents to make secure, policy-controlled payments through Sardis Payment OS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill package to connect OpenClaw agents to Sardis wallet, payment, policy, card, identity, escrow, compliance, and spending analytics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys can be forwarded through the packaged server to a caller-supplied API destination.

Mitigation: Use tightly scoped Sardis API keys, do not expose the skill server without authentication, and remove caller control of API destinations before production use.

Risk: Financial actions may execute without the packaged server enforcing the controls declared in the skill documentation.

Mitigation: Require explicit human approval for payments, bridges, card issuance, and policy changes, and enforce policy checks outside the skill before executing money movement.

Risk: Unpinned dependencies can change behavior after release.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/efedurmaz16/skills/sardis-openclaw)
- [Sardis homepage](https://sardis.sh)
- [Sardis documentation](https://sardis.sh/docs)
- [Sardis API reference](https://api.sardis.sh/v2/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Sardis API credentials and may guide payment, wallet, policy, card, identity, escrow, compliance, and analytics API actions.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
