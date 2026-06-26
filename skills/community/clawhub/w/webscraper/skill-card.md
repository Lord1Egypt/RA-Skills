## Description: <br>
Extracts readable markdown or plain text from allowed public web pages for article, documentation, product, and tutorial lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LesliePie](https://clawhub.ai/user/LesliePie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch and convert public web pages into readable content for summarization, documentation lookup, and product information extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching URLs can disclose request metadata to target sites or access private, internal, or login-required resources if misused. <br>
Mitigation: Use only public pages the user is allowed to fetch, and avoid private, internal, or login-required URLs unless that access is explicitly intended. <br>
Risk: Scraping can violate robots.txt, site terms, copyright expectations, or overload target sites. <br>
Mitigation: Respect robots.txt and site terms, prefer official APIs where available, and use delays or rate limits for repeated requests. <br>
Risk: Optional npm installs or shell commands can introduce package and command-execution risk. <br>
Mitigation: Review commands and packages before running them, especially global npm installs and shell pipelines. <br>


## Reference(s): <br>
- [OpenClaw Web Tool Documentation](https://docs.openclaw.ai/tools/web) <br>
- [ClawHub WebScraper Release](https://clawhub.ai/LesliePie/webscraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with source attribution and optional summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use curl, Node.js, or OpenClaw web_fetch; supports optional content-length limits when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
