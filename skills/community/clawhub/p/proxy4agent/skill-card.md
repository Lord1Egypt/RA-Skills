## Description:

Residential proxy for AI agents that fetches URLs through real IPs, supports geo-targeting and sticky sessions, and can return proxied web content for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldentrii](https://clawhub.ai/user/goldentrii)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Proxy4agent to route web fetch, search, and render tasks through configured residential or HTTP proxy providers for public web content, geo-targeted access, sticky sessions, and JavaScript-heavy pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to route requests through residential proxies and promotes anti-bot bypass behavior.

Mitigation: Use it only with websites and proxy providers you are authorized to access, and confirm that the workflow complies with applicable site and provider terms.

Risk: Proxy providers can observe request URLs and response content in transit.

Mitigation: Do not send sensitive internal URLs, API keys, personal data, or confidential content through the proxy.

Risk: The setup examples use unpinned npx execution of third-party code with proxy credentials.

Mitigation: Prefer a pinned or otherwise verified install command, such as the reviewed package version in the release evidence, before providing credentials.

## Reference(s):

- [Proxy4agent GitHub Homepage](https://github.com/Goldentrii/proxy4agent)
- [Proxy4agent ClawHub Skill Page](https://clawhub.ai/goldentrii/skills/proxy4agent)
- [Novada](https://www.novada.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell command examples; runtime tool outputs can be markdown, raw text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proxy-backed fetch and render outputs depend on configured provider credentials; search and browser rendering require optional provider credentials.]

## Skill Version(s):

1.6.3 (source: server release evidence; artifact frontmatter says 1.6.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
