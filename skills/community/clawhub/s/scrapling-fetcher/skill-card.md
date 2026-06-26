## Description: <br>
Enables agents to fetch and extract structured data from websites using Scrapling HTTP, stealth browser, and dynamic browser modes for pages that may block simple fetches or require JavaScript rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Damirikys](https://clawhub.ai/user/Damirikys) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve page text, CSS or XPath-selected content, attributes, and JSON-formatted scrape results from websites they are authorized to access. It is suited to extraction workflows where standard fetch tools fail because of bot challenges, rate limits, or JavaScript-rendered pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary URLs and use anti-bot bypass behavior, which may conflict with site terms, paywalls, restricted content, or authorization boundaries. <br>
Mitigation: Use it only on sites the operator owns or is explicitly allowed to scrape, require clear approval before stealth or Cloudflare-bypass use, and avoid paywalls or restricted content. <br>
Risk: The Scrapling MCP server starts a local HTTP service that may be reachable by other local clients depending on the environment. <br>
Mitigation: Start the MCP server only in trusted, isolated environments and only when the operator understands who can reach the local service. <br>
Risk: Adaptive scraping can persist element fingerprints or other local state in the working directory. <br>
Mitigation: Run in a trusted workspace and review or remove generated local state when scraping sensitive targets. <br>


## Reference(s): <br>
- [Scrapling Patterns Reference](references/patterns.md) <br>
- [Scrapling PyPI package](https://pypi.org/project/scrapling/) <br>
- [ClawHub skill page](https://clawhub.ai/Damirikys/scrapling-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON scrape output, plus Markdown guidance with shell commands and Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the target URL, fetch mode, selector, and selected attribute; stealth and dynamic modes may use a local Chromium browser.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
