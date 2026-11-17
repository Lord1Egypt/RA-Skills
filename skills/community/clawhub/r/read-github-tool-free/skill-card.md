## Description: <br>
Reads a single GitHub repository through gitmcp.io so an agent can fetch repository documentation, semantically search docs, search code by exact terms, and retrieve linked external URL content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to inspect an individual GitHub repository without cloning it, especially when they need a quick project overview, documentation search, or exact code lookup. It is suited to lightweight open source learning, API usage research, and technical evaluation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact gitmcp.io and external URLs requested by the user. <br>
Mitigation: Install and use it only when outbound access to those destinations is acceptable for the repository content and user request. <br>
Risk: The optional callback_url can send processing results or status data to a user-provided destination. <br>
Mitigation: Avoid callback_url unless the destination is trusted and the user understands what information may be sent. <br>
Risk: Repository summaries and search results can be incomplete or affected by service availability, network limits, and exact-match search constraints. <br>
Mitigation: Review important findings against the source repository before relying on them for technical or security decisions. <br>


## Reference(s): <br>
- [Read Github Tool Free on ClawHub](https://clawhub.ai/thcjp/skills/read-github-tool-free) <br>
- [gitmcp.io service](https://gitmcp.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown responses with code snippets, command examples, repository summaries, search results, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fetched documentation, exact code-search matches, external URL content, status information, and logs depending on the requested operation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
