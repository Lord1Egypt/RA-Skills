## Description: <br>
网页抓取工具免费版 helps agents fetch text from a single public web page, extract content with CSS selectors, and save scraping results to a file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal productivity users use this skill to scrape text, article content, page metadata, or selected fields from one public URL at a time. It is best suited to explicit, user-directed single-page extraction rather than authenticated, bulk, or JavaScript-rendered crawling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged broad trigger wording and underspecified file-writing behavior for automatic installation. <br>
Mitigation: Review before installing, narrow trigger language if needed, and choose output paths deliberately. <br>
Risk: Scraping can capture sensitive, authenticated, or restricted content if used on the wrong target. <br>
Mitigation: Use only for explicit, user-directed scraping of public single URLs and avoid saving sensitive or authenticated page content. <br>
Risk: The free version does not support JavaScript rendering, authentication, proxies, pagination, or bulk crawling. <br>
Mitigation: Confirm the needed content is available in static public HTML and use CSS selectors for precise extraction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/scrape-web-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and extracted text or file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write scraped content to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
