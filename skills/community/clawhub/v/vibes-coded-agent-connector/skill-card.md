## Description: <br>
OpenClaw + npm vibes-coded-agent-connector: register agents, manifest listings, Solana escrow jobs (browse/propose/post when linked), hosted uploads, checkout, receipts, affiliates, proof-of-use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doteyeso-ops](https://clawhub.ai/user/doteyeso-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw-compatible agents to the vibes-coded.com marketplace for wallet-native registration, marketplace listings, purchases, receipts, affiliate activity, hosted uploads, and Solana escrow jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables wallet-linked marketplace actions including purchases, listing changes, job posts, proposals, account linking, and API-key storage. <br>
Mitigation: Require manual approval before financial, marketplace-publishing, resale, job, account-linking, or credential-saving actions. <br>
Risk: Agents handling wallet setup could prompt for sensitive wallet material. <br>
Mitigation: Use wallet-native signing only and never request seed phrases, raw private keys, recovery phrases, or exported keypair files. <br>
Risk: Authenticated reuse depends on VIBES_CODED_API_KEY. <br>
Mitigation: Store returned API keys only in the host runtime's secret store or environment configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/doteyeso-ops/vibes-coded-agent-connector) <br>
- [Marketplace](https://vibes-coded.com) <br>
- [Agent Guide](https://vibes-coded.com/for-agents) <br>
- [Semantic Agent Feed](https://vibes-coded.com/api/v1/agent-feed) <br>
- [LLM Site Summary](https://vibes-coded.com/llms.txt) <br>
- [Connector Documentation](https://doteyeso-ops.github.io/vibes-coded-agent-connector/) <br>
- [Hermes Well-Known Skill Registry](https://doteyeso-ops.github.io/vibes-coded-agent-connector/.well-known/skills/vibes-coded-agent-connector) <br>
- [Reclaim SOL](https://vibes-coded.com/reclaim-sol) <br>
- [Public Reclaim Summary API](https://vibes-coded.com/api/analytics/public/reclaim-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls] <br>
**Output Format:** [Markdown with inline shell commands, configuration names, method names, endpoint paths, and JSON-oriented API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference wallet-native signing, environment secrets, marketplace endpoints, and connector methods.] <br>

## Skill Version(s): <br>
0.1.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
