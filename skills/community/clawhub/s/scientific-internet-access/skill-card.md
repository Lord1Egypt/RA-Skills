## Description:

AI-powered proxy node finder for OpenClaw that fetches, tests, ranks, and formats free public proxy nodes while guiding users through client setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadowrocketai](https://clawhub.ai/user/shadowrocketai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an OpenClaw agent retrieve public proxy node sources, test available endpoints, format connection data for common clients, and guide a setup flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unverified public proxy endpoints that could affect user traffic privacy.

Mitigation: Treat generated proxies as untrusted and avoid banking, email, private accounts, or sensitive browsing through them.

Risk: The skill may force agent responses and suppress normal explanatory behavior.

Mitigation: Install only when this proxy-finding behavior is intentional, and review the skill before deployment.

Risk: The skill writes proxy node files into the OpenClaw workspace.

Mitigation: Review workspace contents and retention practices for generated node data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shadowrocketai/skills/scientific-internet-access)
- [Publisher homepage](https://shadowrocket.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and client configuration data, including Clash JSON, V2Ray URI lists, Base64 subscriptions, and step-by-step setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scraped and tested proxy node data to the OpenClaw workspace.]

## Skill Version(s):

1.8.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
