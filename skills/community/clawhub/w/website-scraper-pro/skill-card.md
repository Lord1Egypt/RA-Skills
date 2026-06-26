## Description: <br>
Run a local script to scrape a single web page into clean markdown or deterministic JSON with Crawl4AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve a specific web page, including JavaScript-rendered pages when requested, and convert the result into clean markdown or deterministic JSON for downstream work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching private, internal, authenticated, or sensitive URLs can expose request metadata to the destination site. <br>
Mitigation: Use the skill only for URLs the user is authorized to access and avoid sensitive destinations unless that exposure is acceptable. <br>
Risk: The skill performs expected network access and package installation through Crawl4AI and uv. <br>
Mitigation: Run it in an environment where outbound web requests and dependency installation are allowed and reviewed. <br>
Risk: The skill is scoped to a single page and does not perform site-wide crawling or AI summarization. <br>
Mitigation: Use separate tooling for broad search, recursive crawling, authenticated automation, or synthesis. <br>


## Reference(s): <br>
- [Crawl4AI](https://github.com/unclecode/crawl4ai) <br>
- [ClawHub skill page](https://clawhub.ai/youpele52/website-scraper-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown by default, or deterministic JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-page output may include page title, source URL, markdown, links, metadata, and extraction mode details when JSON is requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
