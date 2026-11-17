## Description:

Makes an OpenClaw agent reachable on XMTP so humans and other agents can message it for ongoing two-way conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saulmc](https://clawhub.ai/user/saulmc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up an OpenClaw agent as an always-on XMTP messaging bridge. It supports owner conversations with normal agent capabilities and public conversations with restricted messaging behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can expose an OpenClaw agent to ongoing public XMTP messages.

Mitigation: Deploy it only when public reachability is intended, and consider an allowlist instead of accepting arbitrary public senders.

Risk: The generated XMTP wallet and encryption keys are stored in ~/.xmtp/.env.

Mitigation: Use a dedicated wallet with no funds, protect the file as a credential, and avoid committing it to version control.

Risk: Prompt-only public restrictions may not provide strong enough isolation for production use.

Mitigation: Use a dedicated public OpenClaw tool profile with structurally limited permissions for non-owner conversations.

Risk: Running an always-on bridge with broad privileges can increase operational impact if the process or dependencies are compromised.

Mitigation: Run the bridge under a dedicated user or container, pin and review dependencies, and avoid running it as root.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saulmc/skills/xmtp)
- [Publisher profile](https://clawhub.ai/user/saulmc)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, a bridge script, OpenClaw tool-profile configuration guidance, and operational safety notes.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
