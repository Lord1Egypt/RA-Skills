## Description: <br>
Browse and summarize websites, extract content from URLs, search the web for information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankebuaa](https://clawhub.ai/user/tankebuaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search the public web, fetch webpage text, and summarize or extract information from public URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to user-provided or search-result URLs, which can expose sensitive URLs, internal hostnames, or private data if supplied. <br>
Mitigation: Use it for public web searches and public webpages, and avoid secrets, credential-bearing URLs, private customer data, localhost links, internal hostnames, and cloud metadata addresses unless that access is intentional. <br>
Risk: Fetched pages can be incomplete when sites depend on JavaScript, block automated access, require login, or primarily contain audio or video. <br>
Mitigation: Treat returned content as a partial public-web view and verify important results against additional sources or direct site access when accuracy matters. <br>
Risk: Running the helper script directly requires Python dependencies that could introduce supply-chain risk if installed from untrusted sources. <br>
Mitigation: Install direct script dependencies only from trusted package sources and review the environment before execution. <br>


## Reference(s): <br>
- [Web Browsing Usage Guide](references/usage-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional JSON-like search or fetch results and inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return webpage content snippets, search result titles, URLs, summaries, or extraction guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
