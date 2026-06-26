## Description: <br>
Web scraping using Chrome + WebMCP as the primary method for web crawling tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sweihub](https://clawhub.ai/user/sweihub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scrape and interact with JavaScript-rendered websites through Chrome + WebMCP, especially finance pages, stock forums, news pages, and search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls the user's host Chrome browser, which may expose logged-in pages, private pages, or active browsing state. <br>
Mitigation: Use a separate browser profile or sandbox where possible, and avoid logged-in or private pages unless that access is intentional. <br>
Risk: The skill instructs the agent to close tabs and leave only one about:blank tab during cleanup. <br>
Mitigation: Save or separate important tabs before use, and keep scraping work isolated from normal browsing. <br>
Risk: Dynamic finance and news sites may block scraping or return incomplete content while JavaScript is still loading. <br>
Mitigation: Wait for page snapshots after JavaScript loads, retry carefully, and use fallback sources when anti-scraping controls interfere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sweihub/spider) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Chrome/WebMCP action examples and URL templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser action payloads, target URLs, extraction steps, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
