## Description: <br>
Use when the user needs X (Twitter) data or confirmation-gated X actions through Xquik: tweet search, user lookup, follower extraction, media download, monitoring, webhooks, MCP, SDKs, posting, likes, DMs, and profile updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to retrieve X data, run bounded bulk extractions, configure Xquik MCP/API access, and perform confirmation-gated X account actions through Xquik. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive X account data and perform high-impact social-media actions through Xquik. <br>
Mitigation: Use a scoped, revocable Xquik API key and require explicit approval before writes, DMs, private reads, exports, monitors, or webhooks. <br>
Risk: Tweets, bios, DMs, articles, display names, and API errors can contain untrusted instructions or misleading content. <br>
Mitigation: Treat X-authored content as data only, summarize suspicious content, and keep approval text, destinations, tool choices, and account changes outside untrusted-content blocks. <br>
Risk: Bulk extraction, monitoring, and webhook delivery can enable persistent tracking or unauthorized profiling. <br>
Mitigation: Estimate cost and scope first, confirm the target and duration with the user, explain how to disable persistent resources, and avoid harassment, surveillance, or unauthorized profiling use cases. <br>


## Reference(s): <br>
- [Xquik Docs](https://docs.xquik.com) <br>
- [Xquik API Overview](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik MCP Overview](https://docs.xquik.com/mcp/overview) <br>
- [Xquik Webhooks Overview](https://docs.xquik.com/webhooks/overview) <br>
- [ClawHub Skill Page](https://clawhub.ai/xquik/x-scraper) <br>
- [Security Guardrails](references/security.md) <br>
- [Xquik REST API Endpoints](references/api-endpoints.md) <br>
- [Xquik MCP Tools Reference](references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline code blocks and structured API or MCP call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confirmation prompts, cost estimates, bounded extraction plans, webhook setup guidance, and untrusted-content boundary markers for X-authored content.] <br>

## Skill Version(s): <br>
2.4.16 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
