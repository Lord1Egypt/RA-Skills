## Description: <br>
Interact with Veillabs privacy-focused DEX API for cross-chain swaps, private seed distributions, and transaction tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veillabsapp](https://clawhub.ai/user/veillabsapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect supported Veillabs assets, estimate cross-chain swaps, create private swap or seed-distribution workflows, and track transaction status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help set up crypto swaps and seed distributions that move funds and may be irreversible. <br>
Mitigation: Before any action, require the agent to show the exact source and destination assets, networks, amount, recipient addresses, split percentages, expected output, deposit address, and API URL for manual approval. <br>
Risk: Wallet and transaction metadata may be visible to Veillabs, service providers, or public blockchains despite privacy-focused wording. <br>
Mitigation: Disclose metadata exposure before use and proceed only when the user accepts the privacy tradeoff. <br>
Risk: A misconfigured VEILLABS_BASE_URL could send requests to an untrusted endpoint. <br>
Mitigation: Confirm the configured API URL before calls and install the skill only when the Veillabs publisher and endpoint are trusted. <br>


## Reference(s): <br>
- [Veillabs API Reference](references/api-reference.md) <br>
- [Veillabs Homepage](https://trade.veillabs.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/veillabsapp/veillabs-ai) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/veillabsapp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoints, transaction tracking IDs, configuration values, and confirmation checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
