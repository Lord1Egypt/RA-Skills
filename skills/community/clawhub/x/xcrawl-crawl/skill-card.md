## Description: <br>
Use this skill for XCrawl crawl tasks, including bulk site crawling, crawler rule design, async status polling, and delivery of crawl output for downstream scrape and search workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wykings](https://clawhub.ai/user/wykings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit bounded XCrawl site crawls, configure crawl, request, and output options, poll crawl results, and pass raw crawl outputs to downstream scrape or search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Overly broad crawl scopes can reach unintended pages and consume XCrawl credits. <br>
Mitigation: Confirm the business objective, set explicit crawl boundaries, and use crawler limits, include rules, exclude rules, and depth limits before starting a crawl. <br>
Risk: Sending private or internal URLs, cookies, authorization headers, or sensitive request data can expose protected content to the crawl service. <br>
Mitigation: Avoid private or internal targets and sensitive headers unless strictly necessary, and review request cookies and headers before submission. <br>
Risk: Webhook callbacks can send crawl events or related data to an unintended destination. <br>
Mitigation: Review webhook URLs and webhook headers before enabling callbacks. <br>
Risk: The XCrawl API key is stored in a local config file and can be exposed if the file or command output is mishandled. <br>
Mitigation: Read the key only from ~/.xcrawl/config.json, avoid printing it, and keep the local config file access restricted. <br>


## Reference(s): <br>
- [XCrawl homepage](https://www.xcrawl.com/) <br>
- [XCrawl dashboard](https://dash.xcrawl.com/) <br>
- [XCrawl Crawl API base URL](https://run.xcrawl.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown containing endpoint flow, request payload JSON, raw API response bodies, and error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Raw passthrough by default; summaries only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
