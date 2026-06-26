## Description: <br>
Use this skill for XCrawl map tasks, including site URL discovery, regex filtering, scope estimation, and crawl planning before full-site crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wykings](https://clawhub.ai/user/wykings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and agents use this skill to discover URLs for a target site, apply regex filters, estimate crawl scope, and plan selective crawling before a full-site crawl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an XCrawl API key stored in a local config file. <br>
Mitigation: Store the key only in `~/.xcrawl/config.json`, restrict file access, and avoid sharing logs or examples that contain the key. <br>
Risk: Selected target URLs, regex filters, crawl options, and resulting discovered URLs are sent through XCrawl. <br>
Mitigation: Run mapping only for authorized sites and review the target scope before using the skill on private or sensitive domains. <br>
Risk: Mapping requests may consume XCrawl credits and discovered paths may reveal site structure. <br>
Mitigation: Set explicit limits and filters, review credit availability before running, and avoid publishing raw responses that expose sensitive paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wykings/xcrawl-map) <br>
- [XCrawl homepage](https://www.xcrawl.com/) <br>
- [XCrawl dashboard](https://dash.xcrawl.com/) <br>
- [XCrawl Map API endpoint](https://run.xcrawl.com/v1/map) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Raw XCrawl API response with Markdown context, request payload details, and error details when requests fail] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the endpoint used, request payload, raw map response body, and request errors; summaries are only produced when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
