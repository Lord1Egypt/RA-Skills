## Description: <br>
ProxyClaw provides AI agents with IPLoop residential proxy access for fetching, scraping, SERP-style search, geo-targeted requests, and optional bandwidth-sharing setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ultronprime2026](https://clawhub.ai/user/ultronprime2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to route web fetches, scraping tasks, and SERP-style searches through IPLoop residential proxies, including country, city, session, and ASN targeting. The skill also documents account, API key, SDK, and optional node-reward workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Residential proxy scraping can route requests to third-party sites in ways that may violate site policies, laws, or internal data-handling rules. <br>
Mitigation: Use only for approved targets and data classes, and require human review before sending internal URLs, authenticated sessions, customer data, or regulated data through the proxy. <br>
Risk: The skill requires an IPLoop API key and includes examples that can expose long-lived credentials if copied into shell history or local files. <br>
Mitigation: Store credentials in approved secret stores or scoped environment variables, rotate keys regularly, and avoid placing keys in command history, localStorage, synced dotfiles, or committed files. <br>
Risk: The optional Docker or binary node can share the operator's residential IP and bandwidth with third-party traffic. <br>
Mitigation: Run node-reward components only with explicit operator approval, on dedicated infrastructure where bandwidth sharing is permitted, and with monitoring and removal procedures in place. <br>
Risk: The artifact documents account registration, device registration, balance checks, and cashout flows that may affect billing or payouts. <br>
Mitigation: Treat account, device, billing, and payout operations as manual workflows requiring explicit human confirmation rather than autonomous agent actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ultronprime2026/proxyclaw) <br>
- [Publisher profile](https://clawhub.ai/user/ultronprime2026) <br>
- [ProxyClaw website](https://proxyclaw.ai) <br>
- [IPLoop platform](https://iploop.io) <br>
- [IPLoop API Reference](docs/API.md) <br>
- [SERP Search API](docs/SERP.md) <br>
- [Support API](docs/SUPPORT-API.md) <br>
- [IPLoop Node Rewards](REWARDS.md) <br>
- [Docker node setup](earn/DOCKER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON snippets, and inline shell or code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fetched or scraped remote web content when an API key and network access are available.] <br>

## Skill Version(s): <br>
2.5.2 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
