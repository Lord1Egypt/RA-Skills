## Description: <br>
Helps agents launch and manage a public resolved.sh business presence with pages, subdomains, custom domains, data storefronts, paid service endpoints, Pulse activity feeds, follower audiences, and payment-backed registration or renewal flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hichana](https://clawhub.ai/user/hichana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and autonomous agents use this skill to publish and operate an internet-facing agent business presence, including registration, page updates, domain setup, monetized datasets, paid services, activity feeds, and lead capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over public pages, domains, data sales, activity feeds, contacts, service endpoints, and payout-related settings. <br>
Mitigation: Keep explicit user approval enabled for publishing, dataset sales, domain changes, service endpoints, payout-address updates, lead capture, Pulse events, and all paid actions. <br>
Risk: Public pages, feeds, service listings, and datasets may expose secrets, personal data, internal identifiers, or sensitive operational details. <br>
Mitigation: Review content before publication and avoid sending secrets, personal data, internal identifiers, or sensitive operational details to public pages, feeds, listings, or datasets. <br>
Risk: Paid registration, renewal, domain purchase, and marketplace flows can spend funds or affect revenue routing. <br>
Mitigation: Require deliberate user opt-in before autonomous payments and confirm action, current price, and destination details before paid or payout-related operations. <br>


## Reference(s): <br>
- [resolved-sh ClawHub release](https://clawhub.ai/hichana/resolved-sh) <br>
- [resolved.sh full LLM spec](https://resolved.sh/llms.txt) <br>
- [resolved.sh OpenAPI spec](https://resolved.sh/openapi.json) <br>
- [resolved.sh x402 payment spec](https://resolved.sh/x402-spec) <br>
- [Coinbase x402 TypeScript SDK](https://github.com/coinbase/x402) <br>
- [resolved-sh skill repository](https://github.com/resolved-sh/skill) <br>
- [rstack repository](https://github.com/resolved-sh/rstack) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with HTTP examples, shell commands, JSON payloads, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read RESOLVED_SH_API_KEY from the environment and may prepare public page content, service endpoint settings, data marketplace settings, Pulse events, domain changes, and payment actions.] <br>

## Skill Version(s): <br>
0.1.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
