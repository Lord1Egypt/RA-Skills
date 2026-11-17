## Description:

Identity infrastructure for AI agents - register identities, issue tokens, delegate to sub-agents, revoke credentials, manage policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhijitjavelin](https://clawhub.ai/user/abhijitjavelin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a ZeroID identity service for AI agents, including registering identities, issuing tokens, delegating access to sub-agents, revoking credentials, and managing credential policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful identity credentials through a configurable API URL.

Mitigation: Use only a trusted ZeroID server, confirm ZEROID_BASE_URL is the intended HTTPS origin, and use the least-privileged ZEROID_API_KEY available.

Risk: Credential revocation and agent deactivation commands can disrupt downstream access.

Mitigation: Double-check credential IDs and agent IDs before revocation or deactivation.

Risk: Secrets may be exposed through shell history when commands include credentials or tokens.

Mitigation: Avoid pasting secrets into shell history where possible and handle API keys and tokens as sensitive credentials.

## Reference(s):

- [ZeroID GitHub](https://github.com/highflame-ai/zeroid)
- [Quickstart Notebook](https://github.com/highflame-ai/zeroid/blob/main/examples/zeroid_quickstart.ipynb)
- [Interactive API Docs](https://auth.highflame.ai/docs)
- [ClawHub Skill Page](https://clawhub.ai/abhijitjavelin/skills/zeroid)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request and response examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZEROID_API_KEY, ZEROID_BASE_URL, and curl.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
