## Description: <br>
Use this skill as the default XCrawl entry point for direct XCrawl requests, including single-URL fetch, format selection, sync or async execution, and JSON extraction with prompt or json_schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wykings](https://clawhub.ai/user/wykings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to send direct XCrawl scrape requests for selected URLs, choose output formats, run sync or async extraction, and retrieve raw XCrawl API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs, extraction prompts, selected options, and optional webhook details are sent to XCrawl. <br>
Mitigation: Use the skill only for data you intend XCrawl to process, and avoid private account pages, session cookies, Authorization headers, internal URLs, and sensitive webhook destinations unless explicitly required. <br>
Risk: XCrawl API usage can consume account credits. <br>
Mitigation: Confirm the target URL scope and requested output formats before execution, especially for repeated or async requests. <br>


## Reference(s): <br>
- [XCrawl homepage](https://www.xcrawl.com/) <br>
- [XCrawl dashboard](https://dash.xcrawl.com/) <br>
- [ClawHub skill page](https://clawhub.ai/wykings/xcrawl) <br>
- [Publisher profile](https://clawhub.ai/user/wykings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Node examples plus raw JSON API responses when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local XCrawl API key configuration file and may consume XCrawl account credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
