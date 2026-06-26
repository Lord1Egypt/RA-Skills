## Description: <br>
Use this skill for XCrawl scrape tasks, including single-URL fetch, format selection, sync or async execution, and JSON extraction with prompt or json_schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wykings](https://clawhub.ai/user/wykings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call XCrawl's single-page scrape API, choose output formats, run sync or async jobs, and return raw API responses for extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scrape requests can send target URLs, request headers, cookies, and page data to the XCrawl third-party service. <br>
Mitigation: Use the skill only with URLs and page data suitable for XCrawl, and avoid session cookies, authorization headers, internal-only URLs, and secrets unless intentionally shared. <br>
Risk: The skill depends on a local XCrawl API key stored in ~/.xcrawl/config.json. <br>
Mitigation: Protect the local config file and restrict runtime access to curl, node, and the required config path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wykings/xcrawl-scrape) <br>
- [XCrawl homepage](https://www.xcrawl.com/) <br>
- [XCrawl dashboard](https://dash.xcrawl.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Text] <br>
**Output Format:** [Markdown guidance with curl or Node commands and raw XCrawl API response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns endpoint and mode, request payload, raw response bodies, task metadata, and error details when requests fail.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
