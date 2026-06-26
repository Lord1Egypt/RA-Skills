## Description: <br>
Comprehensive management of Trendyol marketplace via API v2.0, including product lifecycle, stock and price management, order processing, returns, and customer questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awelab](https://clawhub.ai/user/awelab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, marketplace operators, and agents use this skill as a knowledge base for constructing Trendyol Marketplace API requests to manage listings, inventory, orders, returns, invoices, webhooks, and customer questions. <br>

### Deployment Geography for Use: <br>
Gulf and Europe storefronts listed in the skill documentation <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad production Trendyol marketplace changes with real seller credentials. <br>
Mitigation: Use staging or limited credentials where possible and require explicit confirmation before deleting products, changing prices or stock, updating orders or returns, sending invoices, answering customers, or modifying webhooks. <br>
Risk: Trendyol API credentials and Authorization headers could be exposed in chats, logs, or shared command output. <br>
Mitigation: Do not paste secrets into public chats or logs, and redact Authorization headers and API keys before sharing output. <br>


## Reference(s): <br>
- [Trendyol Marketplace API Reference](references/api_reference.md) <br>
- [Trendyol Developers Getting Started](https://developers.trendyol.com/v2.0/docs/getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, curl, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied Trendyol credentials; no bundled execution scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
