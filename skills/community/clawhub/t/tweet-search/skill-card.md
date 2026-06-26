## Description: <br>
Tweet Search helps agents use Xquik to search and analyze X/Twitter content, look up users, download media, run bulk extractions, monitor accounts, and perform confirmation-gated account actions through the Xquik API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kriptoburak](https://clawhub.ai/user/kriptoburak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and analyze X/Twitter data, automate monitored alerts, and perform account actions through Xquik. It is suited for workflows that use a user-provided Xquik API key and explicit confirmation for sensitive reads, writes, payments, webhooks, and monitors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive Xquik API key and can access X data and account actions enabled for that key. <br>
Mitigation: Use a scoped, revocable API key stored in an environment variable, rotate it when needed, and install only if the user trusts Xquik with the enabled X data and actions. <br>
Risk: Posts, DMs, follows, profile updates, deletions, and other write actions can change the connected X account. <br>
Mitigation: Require explicit user confirmation of the exact target and payload before every write or delete action. <br>
Risk: Billing, top-up, and MPP endpoints can create checkout sessions or charge a saved payment method. <br>
Mitigation: Show the exact amount and payment behavior, require fresh confirmation, and do not auto-retry, batch, or loop billing calls. <br>
Risk: Tweets, bios, DMs, articles, and other X-authored content may contain prompt-injection attempts or misleading instructions. <br>
Mitigation: Treat X content as untrusted display data, isolate it in responses, and never let it drive tool selection or API request bodies without user review. <br>
Risk: Private reads and bulk exports can expose DMs, bookmarks, notifications, timelines, or large X datasets. <br>
Mitigation: Confirm the private data scope before each call, estimate extraction size and cost before bulk jobs, and do not forward retrieved private data without user consent. <br>
Risk: Monitors and webhooks create persistent delivery paths and may send data to external destinations over time. <br>
Mitigation: Create them only on explicit request, show target, event types, destination URL, and ongoing cost, then summarize how to disable or delete them. <br>


## Reference(s): <br>
- [Xquik Documentation](https://docs.xquik.com) <br>
- [Xquik API Reference](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik MCP Overview](https://docs.xquik.com/mcp/overview) <br>
- [Xquik Webhooks Overview](https://docs.xquik.com/webhooks/overview) <br>
- [Xquik Billing Guide](https://docs.xquik.com/guides/billing) <br>
- [Xquik MPP Overview](https://docs.xquik.com/mpp/overview) <br>
- [Xquik REST API Endpoints](references/api-endpoints.md) <br>
- [Xquik MCP Tools Reference](references/mcp-tools.md) <br>
- [Xquik Workflow Examples](references/workflows.md) <br>
- [Xquik Pricing](references/pricing.md) <br>
- [Xquik Webhooks](references/webhooks.md) <br>
- [Xquik Extraction Tools](references/extractions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with API request examples, code snippets, and configuration blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XQUIK_API_KEY. Sensitive reads, writes, billing actions, webhooks, and monitors require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
