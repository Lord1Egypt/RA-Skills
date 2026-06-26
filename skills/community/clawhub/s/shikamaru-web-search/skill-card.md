## Description: <br>
Searches the public web through Exa's hosted MCP endpoint to help agents find documentation, recent announcements, product pages, blog posts, comparisons, and current external context without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shikamaru-cc](https://clawhub.ai/user/shikamaru-cc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need web discovery before retrieval, such as finding official documentation, recent announcements, pricing, product pages, or comparison sources to inspect and cite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Exa's hosted MCP service and may include sensitive user-provided terms. <br>
Mitigation: Avoid submitting secrets, credentials, or confidential data in search queries. <br>
Risk: The VirusTotal check was pending in the available evidence. <br>
Mitigation: Review displayed permissions and runtime prompts before granting credentials or write access. <br>
Risk: Search results can be stale, incomplete, or conflicting. <br>
Mitigation: Fetch and inspect authoritative pages before relying on precise or high-impact claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shikamaru-cc/shikamaru-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search context with agent-authored Markdown summaries or citations when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs and snippets returned by Exa; no API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
