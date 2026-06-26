## Description: <br>
Use this skill for XCrawl search tasks, including keyword search request design, location and language controls, result analysis, and follow-up crawl or scrape planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wykings](https://clawhub.ai/user/wykings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run XCrawl keyword searches with explicit geography, language, and result-limit controls, then return the endpoint, request payload, raw API response, and errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to XCrawl and the skill depends on an API key stored in `~/.xcrawl/config.json`. <br>
Mitigation: Use only when that data sharing and local key storage are acceptable, and keep the config file scoped to the required XCrawl credential. <br>
Risk: Declared local file and edit permissions are broader than the skill says it needs. <br>
Mitigation: Constrain runtime permissions to curl, node, and the specific config file wherever the host agent supports permission scoping. <br>
Risk: Raw API responses are external content and may contain untrusted or misleading text. <br>
Mitigation: Treat raw XCrawl responses as data, not instructions, and review them before acting on extracted content. <br>


## Reference(s): <br>
- [XCrawl homepage](https://www.xcrawl.com/) <br>
- [XCrawl dashboard](https://dash.xcrawl.com/) <br>
- [ClawHub skill page](https://clawhub.ai/wykings/xcrawl-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wykings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples plus raw API response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw upstream search responses unless the user explicitly requests a summary.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence metadata and release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
