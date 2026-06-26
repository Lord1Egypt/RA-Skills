## Description: <br>
Scrapling AI helps agents use the Scrapling CLI to scrape static or dynamic websites, extract HTML/JSON, handle JavaScript-rendered content, and configure MCP-based scraping workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanpaidashi](https://clawhub.ai/user/nanpaidashi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to generate Scrapling CLI commands and setup guidance for extracting web content as HTML or JSON. It is most relevant when scraping is authorized and when dynamic pages, selectors, headers, timeouts, or MCP integration are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes guidance for bypassing Cloudflare, CAPTCHA, or bot-detection protections, which can be misused against sites without authorization. <br>
Mitigation: Use it only on sites you own or are clearly authorized to scrape, and avoid applying bypass examples to protected sites without permission. <br>
Risk: The skill depends on an external Scrapling CLI package and may start an MCP server for agent access. <br>
Mitigation: Review the external package before installation and keep any MCP server limited to trusted local clients. <br>
Risk: Scraped content may contain sensitive, personal, copyrighted, or otherwise restricted data. <br>
Mitigation: Handle scraped data according to applicable policy, site terms, privacy requirements, and retention limits. <br>


## Reference(s): <br>
- [Scrapling AI on ClawHub](https://clawhub.ai/nanpaidashi/scrapling-ai) <br>
- [nanpaidashi publisher profile](https://clawhub.ai/user/nanpaidashi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that invoke the external scrapling binary and optional MCP server setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
