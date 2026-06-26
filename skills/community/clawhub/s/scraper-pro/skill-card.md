## Description: <br>
Extract data from websites and APIs for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to collect structured public web or API data such as product prices, news articles, and datasets for later analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary websites and APIs. <br>
Mitigation: Review each scrape target before use and confirm permission, Terms of Service, and robots.txt expectations. <br>
Risk: TLS verification is disabled during fetching. <br>
Mitigation: Avoid sensitive sessions or credentials unless TLS verification is fixed and reviewed. <br>
Risk: Scraped output can contain sensitive or regulated data. <br>
Mitigation: Write outputs only to controlled locations where the data can be protected, reviewed, and deleted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/scraper-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON/CSV/Markdown output files, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write scraped data to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
